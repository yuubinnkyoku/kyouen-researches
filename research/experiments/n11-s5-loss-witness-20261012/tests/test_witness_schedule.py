import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXP / "scripts"))

import prepare_candidates


class ScheduleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.targets = json.loads((EXP / "input/targets.json").read_text(encoding="utf-8"))
        cls.schedule = prepare_candidates.make_schedule(
            cls.targets, prepare_candidates.Board(cls.targets["board_size"]))

    def test_frozen_sample_is_six_independently_sourced_s5_loss_roots(self):
        self.assertEqual(len(self.schedule["roots"]), 6)
        self.assertEqual({r["target"]["s4_group"] for r in self.schedule["roots"]},
                         {"latest-s4", "previous-s4"})
        self.assertTrue(all(r["source_row"]["verdict"] == 2 for r in self.schedule["roots"]))
        self.assertTrue(all(r["target"]["expected_verdict"] == 2 for r in self.schedule["roots"]))

    def test_s6_orders_are_geometry_only_and_deterministic(self):
        for root in self.schedule["roots"]:
            by_key = root["key_order_screen"]
            by_legal = root["legal_count_order_screen"]
            self.assertEqual(len(by_key), 5)
            self.assertEqual(len(by_legal), 5)
            self.assertEqual(by_key, sorted(by_key, key=lambda c: int(c["key"])))
            self.assertEqual(by_legal, sorted(by_legal, key=lambda c: (c["legal"], int(c["key"]))))
            self.assertTrue(all(c["stones"] == 6 for c in by_key + by_legal))

    def test_common_node_ceiling_matches_five_child_screen(self):
        budget = self.schedule["budget_protocol"]
        self.assertEqual(budget["per_s5_total_node_cap"],
                         budget["s6_child_node_cap"] * budget["max_s6_candidates_per_parent"])


if __name__ == "__main__":
    unittest.main()
