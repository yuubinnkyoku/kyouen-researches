from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
import complete_s5_via_s6_local as runner


class AdaptiveBoundaryTests(unittest.TestCase):
    def test_loss_witness_stops_parent_dispatch(self):
        children = {(1, 0), (2, 0), (3, 0)}
        calls = []

        def solve(key, legal):
            calls.append(key)
            return (2 if key == (1, 0) else 1), 10, 0.0

        outcomes, new = runner.run_adaptive(
            [(10, 0)], [sorted(children)], {key: {0} for key in children},
            {key: 1 for key in children}, {}, solve, 1)
        self.assertEqual(outcomes, ["LOSS"])
        self.assertEqual(calls, [(1, 0)])
        self.assertEqual(len(new), 1)

    def test_win_requires_full_boundary(self):
        children = {(1, 0), (2, 0)}
        calls = []

        def solve(key, legal):
            calls.append(key)
            return 1, 4, 0.0

        outcomes, _ = runner.run_adaptive(
            [(10, 0)], [sorted(children)], {key: {0} for key in children},
            {key: 1 for key in children}, {}, solve, 1)
        self.assertEqual(outcomes, ["WIN"])
        self.assertEqual(set(calls), children)
        self.assertEqual(runner.classify(set(), {}), "WIN")

    def test_unknown_is_not_retried(self):
        a, b = (1, 0), (2, 0)
        children = {a, b}
        calls = []

        def solve(key, legal):
            calls.append(key)
            return 0, 12, 0.0

        incidence = {key: {0} for key in children}
        legal = {key: 1 for key in children}
        initial = {a: 0}
        outcomes, _ = runner.run_adaptive([(10, 0)], [[a, b]], incidence, legal,
                                          initial, solve, 1)
        self.assertEqual(outcomes, ["UNKNOWN"])
        self.assertEqual(calls, [b])
        calls.clear()
        outcomes, _ = runner.run_adaptive([(10, 0)], [[a, b]], incidence, legal,
                                          initial, solve, 1)
        self.assertEqual(outcomes, ["UNKNOWN"])
        self.assertEqual(calls, [])

    def test_exact_conflict_fails_closed(self):
        verdicts = {(1, 0): 2}
        with self.assertRaisesRegex(ValueError, "conflict"):
            runner.merge_verdict(verdicts, (1, 0), 1)

    def test_audit_rejected_conflicts_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "conflicts"):
            runner.validate_saved_audit({"run_status": "ok", "rejected_conflicts": [{"key": [1, 0]}]})
        with self.assertRaisesRegex(ValueError, "run_status"):
            runner.validate_saved_audit({"run_status": "failed"})

    def test_real_safe_child_replay_validation(self):
        # First canonical key in next3-hard1-s6-probes.csv; retain it inline so
        # this regression does not depend on generated output files being present.
        key, legal = (1297318167664136192, 0), 62
        runner.checked_key(key, 6)

        def row(legal_value=legal, is_or=1):
            return ["replay", 0, 6, legal_value, is_or, 0, 1, 17, 0, key[0], key[1]]

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "valid.csv"
            path.write_text(",".join(map(str, row())) + "\n", encoding="utf-8", newline="\n")
            self.assertEqual(runner.parse_replay(path, key, legal), (1, 17))
            path.write_text(",".join(map(str, row(legal + 1))) + "\n", encoding="utf-8", newline="\n")
            with self.assertRaisesRegex(ValueError, "mismatch"):
                runner.parse_replay(path, key, legal)
            path.write_text(",".join(map(str, row(is_or=0))) + "\n", encoding="utf-8", newline="\n")
            with self.assertRaisesRegex(ValueError, "mismatch"):
                runner.parse_replay(path, key, legal)
            replay = ",".join(map(str, row())) + "\n"
            path.write_text(replay + replay, encoding="utf-8", newline="\n")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                runner.parse_replay(path, key, legal)

    def test_parent_loss_stops_only_exclusive_work(self):
        witness, exclusive, other = (1, 0), (2, 0), (3, 0)
        calls = []

        def solve(key, legal):
            calls.append(key)
            return (2 if key == witness else 1), 5, 0.0

        outcomes, _ = runner.run_adaptive(
            [(10, 0), (20, 0)], [[witness, exclusive], [other]],
            {witness: {0}, exclusive: {0}, other: {1}},
            {witness: 1, exclusive: 2, other: 3}, {}, solve, 1)
        self.assertEqual(outcomes, ["LOSS", "WIN"])
        self.assertEqual(calls, [witness, other])
        self.assertNotIn(exclusive, calls)

    def test_win_parent_stops_all_new_dispatch(self):
        first, later = (1, 0), (2, 0)
        calls = []

        def solve(key, legal):
            calls.append(key)
            return 1, 9, 0.0

        outcomes, _ = runner.run_adaptive(
            [(10, 0), (20, 0)], [[first], [later]], {first: {0}, later: {1}},
            {first: 1, later: 2}, {}, solve, 1)
        self.assertEqual(outcomes, ["WIN", "UNKNOWN"])
        self.assertEqual(calls, [first])


if __name__ == "__main__":
    unittest.main()
