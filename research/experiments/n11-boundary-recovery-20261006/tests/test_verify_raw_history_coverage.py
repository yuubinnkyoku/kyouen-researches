"""Regression tests for complete, hash-audited n11 replay-source inventories."""
from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from verify_raw_history_coverage import sha, verify_coverage  # noqa: E402


class HistoryCoverageTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.filename = "research/experiments/replay.csv"
        self.file = self.root / self.filename
        self.file.parent.mkdir(parents=True)
        self.file.write_bytes(b"replay,1,5,80,0,15000000,0,15000000,0,1,2\n")
        self.reference = self.audit()
        self.current = self.audit()
        self.current["requested_budget"] = 15000000

    def audit(self):
        data = self.file.read_bytes()
        row = {"path": self.filename, "sha256": sha(data), "bytes": len(data),
               "s5_replay_rows": 1}
        return {
            "schema": "n11-s5-raw-history-audit-v1",
            "targets": {"path": "probe.csv", "sha256": "0"*64, "count": 1,
                        "keys": [[10448351135499550784, 0]]},
            "current_cache": {"sha256": "1"*64},
            "scanned_csv_sources": [row],
            "csv_files_examined": 1,
            "s5_replay_rows_examined": 1,
        }

    def test_identical_source_passes(self):
        result = verify_coverage(self.reference, self.current, self.root)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["missing_csv"], 0)

    def test_missing_source_inventory_fails(self):
        self.current["scanned_csv_sources"] = [{
            **self.current["scanned_csv_sources"][0],
            "path": "another.csv",
        }]
        self.file2 = self.root / "another.csv"
        self.file2.write_bytes(self.file.read_bytes())
        result = verify_coverage(self.reference, self.current, self.root)
        self.assertEqual(result["missing_csv"], 1)
        self.assertEqual(result["missing_s5_replay_rows"], 1)
        self.assertEqual(result["status"], "FAIL")

    def test_really_missing_file_fails(self):
        self.file.unlink()
        result = verify_coverage(self.reference, self.current, self.root)
        self.assertEqual(result["altered_csv"], 1)
        self.assertEqual(result["status"], "FAIL")

    def test_crlf_to_lf_recovered_hash_passes(self):
        data = self.file.read_bytes()
        self.file.write_bytes(data.replace(b"\n", b"\r\n"))
        self.reference = self.audit()
        self.file.write_bytes(data)
        self.current = self.audit()
        self.current["requested_budget"] = 15000000
        result = verify_coverage(self.reference, self.current, self.root)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["normalized_crlf_to_lf"], 1)

    def test_content_tamper_detected(self):
        self.file.write_bytes(b"replay,1,5,80,0,15000000,1,15000000,0,1,2\n")
        self.current = self.audit()
        self.current["requested_budget"] = 15000000
        result = verify_coverage(self.reference, self.current, self.root)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["altered_csv"], 1)

    def test_old_row_count_tamper_detected(self):
        self.reference["scanned_csv_sources"][0]["s5_replay_rows"] = 2
        self.reference["s5_replay_rows_examined"] = 2
        result = verify_coverage(self.reference, self.current, self.root)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["altered_csv"], 1)

    def test_stale_current_report_detected(self):
        self.file.write_bytes(self.file.read_bytes() + b"\n")
        result = verify_coverage(self.reference, self.current, self.root)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["altered_csv"], 1)

    def test_target_mismatch_fails_closed(self):
        self.reference["targets"]["keys"] = [[10448351135499550785, 0]]
        with self.assertRaisesRegex(ValueError, "different targets"):
            verify_coverage(self.reference, self.current, self.root)

    def test_cache_mismatch_fails_closed(self):
        self.reference["current_cache"]["sha256"] = "2"*64
        with self.assertRaisesRegex(ValueError, "exact cache"):
            verify_coverage(self.reference, self.current, self.root)

    def test_budgetless_current_fails_closed(self):
        del self.current["requested_budget"]
        with self.assertRaisesRegex(ValueError, "requested_budget"):
            verify_coverage(self.reference, self.current, self.root)

    def test_duplicate_inventory_rejected(self):
        self.current["scanned_csv_sources"].append(
            copy.deepcopy(self.current["scanned_csv_sources"][0]))
        self.current["csv_files_examined"] = 2
        self.current["s5_replay_rows_examined"] = 2
        with self.assertRaisesRegex(ValueError, "duplicate"):
            verify_coverage(self.reference, self.current, self.root)

    def test_traversal_rejected(self):
        row = self.current["scanned_csv_sources"][0]
        row["path"] = "../replay.csv"
        with self.assertRaisesRegex(ValueError, "escapes repository"):
            verify_coverage(self.reference, self.current, self.root)

    def test_invalid_totals_rejected(self):
        self.current["csv_files_examined"] = 10
        with self.assertRaisesRegex(ValueError, "summary totals"):
            verify_coverage(self.reference, self.current, self.root)

    def test_new_file_allowed_and_audited(self):
        other = self.root / "research/experiments/extra.csv"
        other.write_bytes(b"# comment\n")
        self.current["scanned_csv_sources"].append({
            "path": "research/experiments/extra.csv",
            "sha256": sha(other.read_bytes()),
            "bytes": len(other.read_bytes()), "s5_replay_rows": 0})
        self.current["csv_files_examined"] = 2
        result = verify_coverage(self.reference, self.current, self.root)
        self.assertEqual((result["new_csv"], result["status"]), (1, "PASS"))

    def test_dispatch_validator_requires_historical_baseline(self):
        verifier = (SCRIPTS / "verify_dual_tight_probe_preflight.py").read_text()
        self.assertIn('"--historical-raw-audit"', verifier)
        self.assertIn('coverage["status"] != "PASS"', verifier)


if __name__ == "__main__":
    unittest.main()
