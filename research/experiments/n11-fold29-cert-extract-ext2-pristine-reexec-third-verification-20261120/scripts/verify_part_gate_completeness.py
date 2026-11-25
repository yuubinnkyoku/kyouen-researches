#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail-closed exact partition check for K1166 third-verification battery parts.

The original assembler checked that each part was non-empty and that all
present entries passed. This companion verifier additionally proves that the
five part maps reconstruct the pinned 43-gate audit exactly, with no missing,
extra, duplicate, or altered gate.
"""
import hashlib
import json
import os
import sys

AUDIT_SHA256 = "cf6a26abf0a459bcfb42bbb2d649ace5d3d1f1a5aee63a01af1de8b79d6a145f"
AUDIT_BYTES = 15549
AUDIT_GATE_COUNT = 43
AUDIT_SCHEMA = "n11-fold29-win8-cert-extract-ext-second-verification-20261120-v1"
AUDIT_EXPERIMENT = "n11-fold29-win8-cert-extract-ext-second-verification-20261120"

PART_SPECS = (
    ("pin.json", "g_pin_", 1),
    ("k1136.json", "k1136_", 13),
    ("k1137.json", "k1137_", 13),
    ("k1139.json", "k1139_", 13),
    ("tampers.json", "tamper", 3),
)


def no_duplicate_object_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key: " + key)
        result[key] = value
    return result


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=no_duplicate_object_keys)


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def inspect_battery(run_dir, tag):
    checks = {}
    part_bytes = {}

    def gate(name, ok, detail=None):
        checks[name] = {"pass": bool(ok)}
        if detail is not None:
            checks[name]["detail"] = detail

    audit_path = os.path.join(run_dir, "harness-audit.json")
    audit = None
    audit_raw = None
    if os.path.isfile(audit_path):
        try:
            audit_raw = read_bytes(audit_path)
            audit = load_json(audit_path)
        except Exception as exc:
            audit = None
            audit_raw = None
            audit_error = type(exc).__name__
        else:
            audit_error = None
    else:
        audit_error = "missing"

    gate("g_" + tag + "_audit_byte_pin",
         audit_raw is not None and len(audit_raw) == AUDIT_BYTES and
         sha256_bytes(audit_raw) == AUDIT_SHA256,
         {"bytes": len(audit_raw) if audit_raw is not None else None,
          "sha256": sha256_bytes(audit_raw) if audit_raw is not None else None,
          "expected_bytes": AUDIT_BYTES, "expected_sha256": AUDIT_SHA256,
          "error": audit_error})

    audit_gates = audit.get("gates") if isinstance(audit, dict) else None
    audit_shape_ok = (
        isinstance(audit, dict) and
        audit.get("schema") == AUDIT_SCHEMA and
        audit.get("experiment") == AUDIT_EXPERIMENT and
        audit.get("status") == "PASS" and
        audit.get("gate_count") == AUDIT_GATE_COUNT and
        isinstance(audit_gates, dict) and
        len(audit_gates) == AUDIT_GATE_COUNT and
        audit.get("gates_ordered") == sorted(audit_gates) and
        audit.get("missing_parts") == [] and
        all(isinstance(v, dict) and v.get("pass") is True
            for v in audit_gates.values())
    )
    gate("g_" + tag + "_audit_schema_and_43_gate_completeness",
         audit_shape_ok,
         {"expected_gate_count": AUDIT_GATE_COUNT,
          "actual_gate_count": len(audit_gates) if isinstance(audit_gates, dict) else None,
          "status": audit.get("status") if isinstance(audit, dict) else None,
          "ordered_keys_match": bool(isinstance(audit_gates, dict) and
                                     audit.get("gates_ordered") == sorted(audit_gates))})

    merged = {}
    duplicate_keys = []
    for filename, prefix, expected_count in PART_SPECS:
        path = os.path.join(run_dir, "parts", filename)
        raw = None
        obj = None
        error = None
        if os.path.isfile(path):
            try:
                raw = read_bytes(path)
                obj = load_json(path)
                part_bytes[filename] = raw
            except Exception as exc:
                error = type(exc).__name__
        else:
            error = "missing"

        part_gates = obj.get("gates") if isinstance(obj, dict) else None
        is_map = isinstance(part_gates, dict)
        actual_count = len(part_gates) if is_map else None
        count_ok = is_map and actual_count == expected_count
        prefix_ok = is_map and all(isinstance(k, str) and k.startswith(prefix)
                                   for k in part_gates)
        values_ok = is_map and all(isinstance(v, dict) and v.get("pass") is True
                                   for v in part_gates.values())
        local_duplicates = []
        if is_map:
            for key, value in part_gates.items():
                if key in merged:
                    local_duplicates.append(key)
                    duplicate_keys.append(key)
                else:
                    merged[key] = value

        gate("g_" + tag + "_part_" + filename.replace(".json", ""),
             error is None and count_ok and prefix_ok and values_ok and
             not local_duplicates,
             {"expected_count": expected_count, "actual_count": actual_count,
              "prefix": prefix, "prefix_ok": bool(prefix_ok),
              "all_present_entries_pass": bool(values_ok),
              "duplicate_keys": sorted(local_duplicates), "error": error})

    exact_map_ok = (
        isinstance(audit_gates, dict) and
        len(merged) == AUDIT_GATE_COUNT and
        not duplicate_keys and
        merged == audit_gates
    )
    gate("g_" + tag + "_parts_exactly_reconstruct_pinned_audit",
         exact_map_ok,
         {"merged_gate_count": len(merged),
          "audit_gate_count": len(audit_gates) if isinstance(audit_gates, dict) else None,
          "duplicate_keys": sorted(duplicate_keys),
          "missing_keys": sorted(set(audit_gates or {}) - set(merged)),
          "extra_keys": sorted(set(merged) - set(audit_gates or {}))})

    return checks, part_bytes


def inspect_pair(battery1_run, battery2_run):
    checks = {}
    parts_by_battery = {}
    for tag, run_dir in (("b1", battery1_run), ("b2", battery2_run)):
        local, part_bytes = inspect_battery(run_dir, tag)
        checks.update(local)
        parts_by_battery[tag] = part_bytes

    cross = {}
    for filename, _, _ in PART_SPECS:
        a = parts_by_battery["b1"].get(filename)
        b = parts_by_battery["b2"].get(filename)
        cross[filename] = a is not None and b is not None and a == b
    checks["g_cross_battery_all_five_parts_byte_identical"] = {
        "pass": bool(cross) and all(cross.values()),
        "detail": cross,
    }

    ok = all(v.get("pass") is True for v in checks.values())
    return {
        "schema": "k1166-third-verification-part-gate-completeness-v1",
        "experiment": "n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120",
        "status": "PASS" if ok else "FAIL",
        "gate_count": len(checks),
        "gates": checks,
        "expected_part_gate_counts": {
            filename: count for filename, _, count in PART_SPECS
        },
        "interpretation_guard": [
            "This is a supplemental integrity check of battery part completeness.",
            "It does not create or extend any WIN/LOSS verdict or close any S6 row.",
            "The standard 11x11 empty board and named two-stone roots remain UNKNOWN.",
        ],
    }


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 2:
        print("usage: verify_part_gate_completeness.py BATTERY1_RUN_DIR BATTERY2_RUN_DIR")
        return 2
    record = inspect_pair(argv[0], argv[1])
    if record["status"] != "PASS":
        print(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True))
        return 1
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "output", "part-gate-completeness.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps({"status": "PASS", "gate_count": record["gate_count"],
                      "out": "output/part-gate-completeness.json"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
