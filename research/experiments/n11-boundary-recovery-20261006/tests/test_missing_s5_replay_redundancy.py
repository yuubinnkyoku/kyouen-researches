"""Failure and positive regression tests for n11 missing replay redundancy auditing."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from audit_missing_s5_replay_redundancy import (
    analyze, geometry, missing_s5_keys, read_exact_cache,
)  # noqa: E402

LOSS_KEY = (1297036692682703008, 128)
UNKNOWN_KEY = (10412322338480590880, 0)


class MissingReplayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.raw = self.base / "research/experiments"
        self.raw.mkdir(parents=True)
        self.cache = self.base / "exact.cache"
        self.cache.write_text(
            f"s5verdict,{LOSS_KEY[0]},{LOSS_KEY[1]},5,2,0\n"
        )
        self.ref = {
            "schema": "n11-s5-raw-history-audit-v1",
            "scanned_csv_sources": [
                {"path": f".local/n11/one/s5-{LOSS_KEY[0]}-{LOSS_KEY[1]}.out.csv",
                 "s5_replay_rows": 1},
                {"path": f".local/n11/two/s5-{UNKNOWN_KEY[0]}-{UNKNOWN_KEY[1]}.out.csv",
                 "s5_replay_rows": 1},
                {"path": ".local/n11/three/metadata.csv", "s5_replay_rows": 0},
            ],
        }
        self.add_replay(LOSS_KEY, 2, "loss.csv")
        self.add_replay(UNKNOWN_KEY, 0, "unknown.csv")

    def add_replay(self, key, verdict, name, budget=15000000):
        f = self.raw / name
        f.write_text(
            f"replay,1,5,80,0,{budget},{verdict},{budget},0,"
            f"{key[0]},{key[1]}\n"
        )
        return f

    def test_keys_safe_and_canonical(self):
        self.assertTrue(geometry(LOSS_KEY))
        self.assertTrue(geometry(UNKNOWN_KEY))

    def test_positive_evidence_does_not_upgrade_unknown(self):
        result = analyze(self.ref, self.raw, self.cache, base=self.base)
        self.assertEqual(result["status"], "KEY_EVIDENCE_COMPLETE")
        self.assertEqual(result["historical_missing_local_csv"], 3)
        self.assertEqual(result["historical_missing_one_s5_csv"], 2)
        self.assertEqual(result["missing_keys_already_exact_in_cache"], 1)
        self.assertEqual(result["uncached_keys_with_only_saved_15m_unknown"], 1)
        self.assertEqual(result["saved_exact_cache_conflicts"], [])
        self.assertIsNone(result["keys"][f"{UNKNOWN_KEY[0]},{UNKNOWN_KEY[1]}"]
                          ["cache_exact_verdict"])

    def test_missing_unknown_record_rejected(self):
        (self.raw / "unknown.csv").unlink()
        report = analyze(self.ref, self.raw, self.cache, base=self.base)
        self.assertEqual(report["status"], "INCOMPLETE")
        self.assertEqual(report["uncached_keys_without_sufficient_saved_raw"], 1)

    def test_below_budget_unknown_not_sufficient(self):
        self.add_replay(UNKNOWN_KEY, 0, "unknown.csv", budget=1000)
        report = analyze(self.ref, self.raw, self.cache, base=self.base)
        self.assertEqual(report["status"], "INCOMPLETE")

    def test_exact_conflict_rejected(self):
        self.add_replay(LOSS_KEY, 1, "loss.csv")
        report = analyze(self.ref, self.raw, self.cache, base=self.base)
        self.assertEqual(report["status"], "INCOMPLETE")
        self.assertEqual(report["saved_exact_cache_conflicts"], [list(LOSS_KEY)])

    def test_uncached_exact_not_unknown(self):
        self.add_replay(UNKNOWN_KEY, 2, "unknown.csv")
        report = analyze(self.ref, self.raw, self.cache, base=self.base)
        self.assertEqual(report["status"], "INCOMPLETE")

    def test_multirow_unrecovered_source_rejected(self):
        self.ref["scanned_csv_sources"][2]["s5_replay_rows"] = 2
        with self.assertRaisesRegex(ValueError, "non-singleton"):
            missing_s5_keys(self.ref)

    def test_duplicate_missing_key_rejected(self):
        self.ref["scanned_csv_sources"].append({
            "path": f".local/n11/copy/s5-{LOSS_KEY[0]}-{LOSS_KEY[1]}.out.csv",
            "s5_replay_rows": 1,
        })
        with self.assertRaisesRegex(ValueError, "duplicate"):
            missing_s5_keys(self.ref)

    def test_noncanonical_missing_key_rejected(self):
        self.ref["scanned_csv_sources"][0]["path"] = (
            ".local/n11/fake/s5-3-0.out.csv"
        )
        with self.assertRaisesRegex(ValueError, "unsafe"):
            missing_s5_keys(self.ref)

    def test_conflicting_exact_cache_rejected(self):
        with self.cache.open("a") as f:
            f.write(f"s5verdict,{LOSS_KEY[0]},{LOSS_KEY[1]},5,1,0\n")
        with self.assertRaisesRegex(ValueError, "conflicting exact cache"):
            read_exact_cache(self.cache)

    def test_archived_receipt_preserves_full_64bit_keys(self):
        root = Path(__file__).resolve().parents[4]
        path = root / ("research/experiments/n11-boundary-recovery-20261006/"
                       "output/post-bd547ab0-vanished-s5-key-evidence-receipt-20261008.json")
        data = json.loads(path.read_text(encoding="utf-8"))
        samples = data["uncached_saved_unknown_examples"]
        self.assertEqual(len(samples), 8)
        seen = set()
        for item in samples:
            key = item["key"]
            self.assertEqual(len(key), 2)
            self.assertTrue(all(isinstance(k, str) and k.isdecimal() for k in key))
            self.assertGreater(int(key[0]), 2**53)
            seen.add(tuple(key))
            source = root / item["saved_replay_file"]
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),
                             item["sha256"])
            with source.open(encoding="utf-8-sig", newline="") as f:
                rows = list(csv.reader(f))
            row = rows[item["line"] - 1]
            self.assertEqual([row[9], row[10]], key)
            self.assertEqual(int(row[5]), item["budget"])
            self.assertEqual(row[6], "0")
        self.assertEqual(len(seen), 8)

    def test_script_does_not_authorize_source_gate_override(self):
        s = (SCRIPTS / "audit_missing_s5_replay_redundancy.py").read_text()
        self.assertIn("no historical source-coverage gate override", s)


if __name__ == "__main__":
    unittest.main()
