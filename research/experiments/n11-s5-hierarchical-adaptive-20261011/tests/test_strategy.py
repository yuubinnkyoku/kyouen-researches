from __future__ import annotations

import gzip
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EX = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EX / "scripts"))

from analyze import build_report  # noqa: E402
from strategy import LOSS, UNKNOWN, WIN, choose_strategy, fixed_first_outcome  # noqa: E402


class FixedPlayerPolarityTests(unittest.TestCase):
    def test_s5_and_layer_requires_all_wins_or_one_loss(self) -> None:
        self.assertEqual(fixed_first_outcome(5, [WIN, WIN, LOSS], 90), LOSS)
        self.assertEqual(fixed_first_outcome(5, [WIN, WIN], 2), WIN)
        self.assertEqual(fixed_first_outcome(5, [WIN, WIN], 3), UNKNOWN)
        self.assertEqual(fixed_first_outcome(5, [WIN, UNKNOWN], 2), UNKNOWN)

    def test_s6_or_layer_requires_one_win_or_all_losses(self) -> None:
        self.assertEqual(fixed_first_outcome(6, [LOSS, WIN], 90), WIN)
        self.assertEqual(fixed_first_outcome(6, [LOSS, LOSS], 2), LOSS)
        self.assertEqual(fixed_first_outcome(6, [LOSS, LOSS], 3), UNKNOWN)
        self.assertEqual(fixed_first_outcome(6, [LOSS, UNKNOWN], 2), UNKNOWN)

    def test_zero_child_terminal_polarity(self) -> None:
        self.assertEqual(fixed_first_outcome(4, [], 0), LOSS)
        self.assertEqual(fixed_first_outcome(5, [], 0), WIN)

    def test_bad_or_incomplete_evidence_is_rejected_or_unknown(self) -> None:
        self.assertEqual(fixed_first_outcome(5, [WIN], 2), UNKNOWN)
        with self.assertRaises(ValueError):
            fixed_first_outcome(5, [3], 1)
        with self.assertRaises(ValueError):
            fixed_first_outcome(5, [WIN, WIN], 1)


class StrategyRoutingTests(unittest.TestCase):
    def test_saved_s6_boundary_recovers_exact_s5_polarity(self) -> None:
        plan = choose_strategy(
            goal="s5_win",
            expected_s6_children=3,
            direct_s5_verdict=UNKNOWN,
            saved_s6_verdicts={"a": WIN, "b": WIN, "c": WIN},
            direct_s5_attempted=True,
        )
        self.assertEqual((plan["mode"], plan["verdict"]), ("C", WIN))

    def test_partial_s6_loss_is_a_s5_loss_witness(self) -> None:
        plan = choose_strategy(
            goal="s5_loss",
            expected_s6_children=4,
            saved_s6_verdicts={"a": WIN, "b": LOSS},
        )
        self.assertEqual((plan["mode"], plan["verdict"]), ("C", LOSS))

    def test_d_orders_by_measured_cost_without_predicting_outcome(self) -> None:
        plan = choose_strategy(
            goal="s5_loss",
            expected_s6_children=3,
            saved_s6_verdicts={"a": WIN, "b": UNKNOWN},
            s6_children=["a", "b", "c"],
            s6_cost_hints={"b": 100, "c": 900},
        )
        self.assertEqual(plan["mode"], "D")
        self.assertEqual(plan["next_s6"], ["b", "c"])
        self.assertFalse(plan["cost_order_is_outcome_prediction"])
        self.assertEqual(plan["verdict"], UNKNOWN)

    def test_s5_win_without_controlled_cost_data_does_not_guess_a_or_b(self) -> None:
        plan = choose_strategy(
            goal="s5_win",
            expected_s6_children=90,
            direct_s5_verdict=UNKNOWN,
            direct_s5_attempted=True,
        )
        self.assertIsNone(plan["mode"])
        self.assertEqual(plan["action"], "require_same_environment_paired_benchmark")

    def test_only_zero_trusted_leaf_certificate_selects_e(self) -> None:
        plan = choose_strategy(
            goal="s5_loss",
            expected_s6_children=1,
            independent_proof={"verified": True, "trusted_leaf_count": 0, "root_verdict": LOSS},
        )
        self.assertEqual((plan["mode"], plan["verdict"]), ("E", LOSS))
        with self.assertRaises(ValueError):
            choose_strategy(
                goal="s5_loss",
                expected_s6_children=1,
                independent_proof={"verified": True, "trusted_leaf_count": 1, "root_verdict": LOSS},
            )


class SavedExperimentAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report, cls.manifest = build_report()

    def test_k0374_and_direct_replay_measurements(self) -> None:
        outcomes = self.report["outcomes"]
        self.assertEqual(outcomes["direct_15m"]["verdict"], "UNKNOWN")
        self.assertEqual(outcomes["direct_15m"]["actual_nodes"], 15_000_000)
        self.assertEqual(outcomes["s6_initial"], {
            "distinct_children": 90,
            "WIN": 85,
            "LOSS": 0,
            "UNKNOWN": 5,
            "nodes": 22_933_619,
        })
        self.assertEqual(outcomes["s6_escalations"]["WIN"], 5)
        self.assertEqual(outcomes["s6_full_split"]["total_nodes"], 29_794_287)
        self.assertEqual(outcomes["derived_s5"], "WIN")

    def test_equal_cap_prefix_remains_unknown_and_current_boundary_rebuilt(self) -> None:
        cap = self.report["same_15m_node_cap"]["split_prefix"]
        self.assertEqual(cap["nodes"], 15_000_000)
        self.assertEqual(cap["derived_s5"], "UNKNOWN")
        self.assertTrue(cap["final_row_censored"])
        current = self.report["strategy_router"]["current_s4"]
        self.assertEqual(current["outcomes"], {"LOSS": 40, "WIN": 0, "UNKNOWN": 66})
        self.assertFalse(self.report["strategy_router"]["current_s4_dispatch"])
        self.assertFalse(self.report["resource_comparison"]["node_cost_reduction_demonstrated"])

    def test_raw_hash_tampering_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            altered = Path(temporary) / "raw"
            shutil.copytree(EX / "input/raw", altered)
            target = altered / "s6-batch1.out.csv.gz"
            text = gzip.decompress(target.read_bytes()).decode("utf-8")
            changed = text.replace(",1,", ",2,", 1)
            self.assertNotEqual(text, changed)
            target.write_bytes(gzip.compress(changed.encode("utf-8"), mtime=0))
            with self.assertRaises(ValueError):
                build_report(altered)


if __name__ == "__main__":
    unittest.main()
