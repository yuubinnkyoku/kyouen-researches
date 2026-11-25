#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Synthetic tamper tests for the K1166 part-gate completeness verifier."""
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
EXPERIMENT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(EXPERIMENT, "scripts"))

from verify_part_gate_completeness import PART_SPECS, inspect_pair, load_json  # noqa: E402


AUDIT_FIXTURE = os.path.join(EXPERIMENT, "output", "battery1", "harness-audit.json")


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


class PartGateCompletenessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = load_json(AUDIT_FIXTURE)
        cls.gates = cls.audit["gates"]

    def make_pair(self, root):
        runs = {}
        for tag in ("b1", "b2"):
            run = os.path.join(root, tag, "run")
            os.makedirs(os.path.join(run, "parts"), exist_ok=True)
            write_json(os.path.join(run, "harness-audit.json"), self.audit)
            for filename, prefix, expected in PART_SPECS:
                subset = {k: v for k, v in self.gates.items() if k.startswith(prefix)}
                self.assertEqual(len(subset), expected)
                write_json(os.path.join(run, "parts", filename), {"gates": subset})
            runs[tag] = run
        return runs["b1"], runs["b2"]

    def load_part(self, run, filename):
        return load_json(os.path.join(run, "parts", filename))

    def save_part(self, run, filename, obj):
        write_json(os.path.join(run, "parts", filename), obj)

    def test_valid_exact_partition_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            b1, b2 = self.make_pair(tmp)
            record = inspect_pair(b1, b2)
            self.assertEqual(record["status"], "PASS")
            self.assertEqual(record["gate_count"], 17)

    def test_missing_gate_in_both_batteries_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            b1, b2 = self.make_pair(tmp)
            key = next(iter(self.load_part(b1, "k1136.json")["gates"]))
            for run in (b1, b2):
                obj = self.load_part(run, "k1136.json")
                del obj["gates"][key]
                self.save_part(run, "k1136.json", obj)
            self.assertEqual(inspect_pair(b1, b2)["status"], "FAIL")

    def test_extra_gate_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            b1, b2 = self.make_pair(tmp)
            obj = self.load_part(b1, "k1136.json")
            obj["gates"]["unexpected_gate"] = {"pass": True}
            self.save_part(b1, "k1136.json", obj)
            self.assertEqual(inspect_pair(b1, b2)["status"], "FAIL")

    def test_duplicate_gate_across_parts_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            b1, b2 = self.make_pair(tmp)
            key, value = next(iter(self.load_part(b1, "k1136.json")["gates"].items()))
            obj = self.load_part(b1, "pin.json")
            obj["gates"][key] = value
            self.save_part(b1, "pin.json", obj)
            self.assertEqual(inspect_pair(b1, b2)["status"], "FAIL")

    def test_altered_gate_detail_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            b1, b2 = self.make_pair(tmp)
            obj = self.load_part(b1, "k1137.json")
            key = next(iter(obj["gates"]))
            obj["gates"][key] = {"pass": True, "detail": {"tampered": True}}
            self.save_part(b1, "k1137.json", obj)
            self.assertEqual(inspect_pair(b1, b2)["status"], "FAIL")

    def test_cross_battery_part_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            b1, b2 = self.make_pair(tmp)
            obj = self.load_part(b2, "tampers.json")
            obj["gates"]["tamper1_cert_body_fail_closed"]["detail"]["offset"] = 300008
            self.save_part(b2, "tampers.json", obj)
            self.assertEqual(inspect_pair(b1, b2)["status"], "FAIL")

    def test_duplicate_json_object_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            b1, b2 = self.make_pair(tmp)
            key = next(iter(self.gates))
            path = os.path.join(b1, "parts", "pin.json")
            with open(path, "w", encoding="utf-8") as f:
                f.write('{"gates":{"' + key + '":{"pass":true},"' + key + '":{"pass":true}}}\n')
            self.assertEqual(inspect_pair(b1, b2)["status"], "FAIL")

    def test_audit_gate_order_tamper_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            b1, b2 = self.make_pair(tmp)
            for run in (b1, b2):
                audit = load_json(os.path.join(run, "harness-audit.json"))
                audit["gates_ordered"] = list(reversed(audit["gates_ordered"]))
                write_json(os.path.join(run, "harness-audit.json"), audit)
            self.assertEqual(inspect_pair(b1, b2)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
