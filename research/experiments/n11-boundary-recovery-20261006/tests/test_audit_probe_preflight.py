"""Fail-closed tests for exact-source binding of n=11 probe schedules."""
import copy
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from audit_probe_preflight import validate_audits  # noqa: E402


class PreflightAuditTests(unittest.TestCase):
    def setUp(self):
        self.keys = {(1, 2), (3, 4), (5, 6)}
        self.raw = {
            "schema": "n11-s5-raw-history-audit-v1",
            "requested_budget": 15000000,
            "targets": {"sha256": "targets", "count": 3,
                        "keys": [[1, 2], [3, 4], [5, 6]]},
            "current_cache": {"sha256": "cache", "target_exact_intersection": 0,
                              "hits": {}},
            "prior_exact": {},
            "exact_verdict_conflicts": [],
            "prior_unknown_same_budget_or_higher": [
                {"key": [3, 4], "budget": 15000000, "verdict": 0},
                {"key": [3, 4], "budget": 20000000, "verdict": 0}],
            "dispatch_ready_keys": [[1, 2], [5, 6]],
        }
        self.saved = {
            "schema": "n11-next3-saved-s6-parent-boundary-audit-v1",
            "current_cache": {"sha256": "cache"},
            "targets": {"sha256": "targets",
                        "parents": [{"key": list(k), "outcome": "UNKNOWN"}
                                    for k in sorted(self.keys)],
                        "status_counts": {"UNKNOWN": 3}},
            "cache_comparison": {"new_exact": 0, "unknown_parents": 3,
                                 "opposite_verdict_conflicts": []},
            "source_audit": {"exact_conflict_count": 0,
                             "source_hashes_validated": True},
        }

    def run_audit(self, raw=None, saved=None, budget=15000000):
        return validate_audits(self.keys, "targets", "cache",
                               self.raw if raw is None else raw,
                               self.saved if saved is None else saved, budget)

    def test_exhausted_unknown_excluded_without_inferred_verdict(self):
        ready, blocked = self.run_audit()
        self.assertEqual(ready, {(1, 2), (5, 6)})
        self.assertEqual(blocked, {(3, 4)})

    def test_changed_budget_requires_new_raw_audit(self):
        with self.assertRaisesRegex(ValueError, "budget"):
            self.run_audit(budget=16000000)

    def test_legacy_budgetless_audit_rejected(self):
        raw = copy.deepcopy(self.raw)
        del raw["requested_budget"]
        with self.assertRaisesRegex(ValueError, "budget"):
            self.run_audit(raw=raw)

    def test_invalid_budget_rejected(self):
        with self.assertRaisesRegex(ValueError, "budget"):
            self.run_audit(budget=0)

    def test_same_count_wrong_raw_parent_set_rejected(self):
        raw = copy.deepcopy(self.raw)
        raw["targets"]["keys"][0] = [99, 100]
        with self.assertRaisesRegex(ValueError, "current targets"):
            self.run_audit(raw=raw)

    def test_same_count_wrong_saved_parent_set_rejected(self):
        saved = copy.deepcopy(self.saved)
        saved["targets"]["parents"][0]["key"] = [99, 100]
        with self.assertRaisesRegex(ValueError, "same UNKNOWN parents"):
            self.run_audit(saved=saved)

    def test_saved_target_hash_rejected(self):
        saved = copy.deepcopy(self.saved)
        saved["targets"]["sha256"] = "stale"
        with self.assertRaisesRegex(ValueError, "current target file"):
            self.run_audit(saved=saved)

    def test_saved_cache_hash_rejected(self):
        saved = copy.deepcopy(self.saved)
        saved["current_cache"]["sha256"] = "stale"
        with self.assertRaisesRegex(ValueError, "different exact cache"):
            self.run_audit(saved=saved)

    def test_unmerged_exact_result_rejected(self):
        raw = copy.deepcopy(self.raw)
        raw["prior_exact"] = {"1,2": 1}
        with self.assertRaisesRegex(ValueError, "unmerged exact"):
            self.run_audit(raw=raw)

    def test_saved_s6_new_exact_rejected(self):
        saved = copy.deepcopy(self.saved)
        saved["cache_comparison"]["new_exact"] = 1
        with self.assertRaisesRegex(ValueError, "new exact"):
            self.run_audit(saved=saved)

    def test_saved_source_hash_check_required(self):
        saved = copy.deepcopy(self.saved)
        saved["source_audit"]["source_hashes_validated"] = False
        with self.assertRaisesRegex(ValueError, "hash/conflict"):
            self.run_audit(saved=saved)

    def test_invalid_blocked_verdict_rejected(self):
        raw = copy.deepcopy(self.raw)
        raw["prior_unknown_same_budget_or_higher"][0]["verdict"] = 1
        with self.assertRaisesRegex(ValueError, "same-budget UNKNOWN"):
            self.run_audit(raw=raw)

    def test_blocked_budget_too_low_rejected(self):
        raw = copy.deepcopy(self.raw)
        raw["prior_unknown_same_budget_or_higher"][0]["budget"] = 500
        with self.assertRaisesRegex(ValueError, "same-budget UNKNOWN"):
            self.run_audit(raw=raw)

    def test_blocked_key_in_dispatch_rejected(self):
        raw = copy.deepcopy(self.raw)
        raw["dispatch_ready_keys"].append([3, 4])
        with self.assertRaisesRegex(ValueError, "targets minus blocked"):
            self.run_audit(raw=raw)

    def test_saved_parent_duplicate_rejected(self):
        saved = copy.deepcopy(self.saved)
        saved["targets"]["parents"][1]["key"] = [1, 2]
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.run_audit(saved=saved)

    def test_64bit_identity_not_rounded(self):
        a = 10448351135499550784
        b = a + 1
        self.keys = {(a, 0), (b, 0)}
        self.raw["targets"]["count"] = 2
        self.raw["targets"]["keys"] = [[a, 0], [b, 0]]
        self.raw["dispatch_ready_keys"] = [[a, 0], [b, 0]]
        self.raw["prior_unknown_same_budget_or_higher"] = []
        self.saved["targets"]["parents"] = [
            {"key": [a, 0], "outcome": "UNKNOWN"},
            {"key": [b, 0], "outcome": "UNKNOWN"}]
        self.saved["targets"]["status_counts"] = {"UNKNOWN": 2}
        self.saved["cache_comparison"]["unknown_parents"] = 2
        self.assertEqual(self.run_audit(), (self.keys, set()))

    def test_budget_attestation_is_saved_not_injected(self):
        raw_script = (SCRIPTS / "audit_s5_raw_history.py").read_text(encoding="utf-8")
        verifier = (SCRIPTS / "verify_dual_tight_probe_preflight.py").read_text(encoding="utf-8")
        self.assertIn('"requested_budget": args.budget', raw_script)
        self.assertNotIn('raw_for_validation["requested_budget"]', verifier)
        self.assertIn('target_keys, target_sha, cache_sha, raw, saved, args.budget', verifier)

    def test_both_preparers_call_strict_validator(self):
        for name in ("prepare_dual_tight_probe.py",
                     "prepare_dual_tight_ready_subset_probe.py"):
            with self.subTest(name=name):
                text = (SCRIPTS / name).read_text(encoding="utf-8")
                self.assertIn("validate_audits(", text)
                self.assertIn("args.budget", text)


if __name__ == "__main__":
    unittest.main()
