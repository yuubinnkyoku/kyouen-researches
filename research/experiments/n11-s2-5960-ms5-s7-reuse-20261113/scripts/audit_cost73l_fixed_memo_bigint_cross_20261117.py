#!/usr/bin/env python3
"""Cross-audit the pinned cost73l fixed-memo battery and BigInt certificate audit.

This checks agreement among three already-published result files. It does not
run the certificate verifier or read/reconstruct the 61 MB certificate band.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113"
INPUTS = {
    "battery": BASE / "output/class2-lane-fixed-memo-battery-73l-20261117.json",
    "manifest": BASE / "output/class2-lane-cost73l-certificates/class2-lane-cost73l-win7-certificates-20261117.json",
    "bigint": BASE / "output/class2-lane-cost73l-certificates-bigint-independent-reverification-20261117.json",
}
PINS = {
    "battery": "963dccc777340974981eb3799e753657b3743e53",
    "manifest": "6e0a94aba212ba54bb5329fbea4643c9dcdb1ec4",
    "bigint": "547fe617abc179ff47f3607079d3ca8c1de4359b",
}
OUTPUT = BASE / "output/class2-lane-cost73l-fixed-memo-bigint-cross-audit-20261117.json"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()


def unique_by_bit(records: list[dict], label: str) -> dict[int, dict]:
    result = {}
    for record in records:
        bit = record["bit"]
        if bit in result:
            raise AssertionError(f"{label}: duplicate bit {bit}")
        result[bit] = record
    return result


def main() -> None:
    raw = {name: path.read_bytes() for name, path in INPUTS.items()}
    actual_pins = {name: git_blob_sha(data) for name, data in raw.items()}
    if actual_pins != PINS:
        raise AssertionError(f"input blob pin mismatch: {actual_pins}")

    battery, manifest, bigint = (
        json.loads(raw[name]) for name in ("battery", "manifest", "bigint")
    )
    b = battery["per_bit"]
    m = manifest["certificates"]
    v = bigint["entries"]
    bm = unique_by_bit(b, "battery")
    mm = unique_by_bit(m, "manifest")
    vm = unique_by_bit(v, "bigint")
    expected_bits = sorted(mm)

    checks = []

    def record(name: str, ok: bool, detail: dict) -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    record(
        "population_and_bit_sets",
        len(b) == len(m) == len(v) == 32 and sorted(bm) == expected_bits == sorted(vm),
        {"battery": len(b), "manifest": len(m), "bigint": len(v),
         "bits_match": sorted(bm) == expected_bits == sorted(vm)},
    )

    mismatches = []
    for bit in expected_bits:
        x, y, z = bm[bit], mm[bit], vm[bit]
        pairs = {
            "rows_battery_manifest": (x["rows"], y["rows"]),
            "md5_battery_manifest": (x["md5"], y["md5"]),
            "md5_battery_bigint": (x["md5"], z["joined_md5"]),
            "sha256_manifest_bigint": (y["sha256"], z["joined_sha256"]),
            "rows_battery_bigint": (x["rows"], z["verifier_rows"]),
            "root_manifest_bigint": (y["root"], z["root_hex"]),
            "mobility_manifest_bigint": (y["loser_mobility"], z["verifier_root_mobility"]),
            "terminal_range_manifest_bigint": (
                y["terminal_stone_range"], z["verifier_terminal_range"]
            ),
            "verifier_status": (z["verifier_status"], "PASS"),
            "union_missing": (z["verifier_union_missing"], 0),
            "union_extra": (z["verifier_union_extra"], 0),
            "byte_identical": (x["byte_identical"], True),
        }
        for field, (actual, expected) in pairs.items():
            if actual != expected:
                mismatches.append({"bit": bit, "field": field,
                                   "actual": actual, "expected": expected})

    record("per_bit_cross_agreement", not mismatches,
           {"mismatch_count": len(mismatches), "mismatches": mismatches})

    fixed_nodes = sum(x["fixB_nodes"] for x in b)
    verbatim_nodes = sum(x["published_verbatim_nodes"] for x in b)
    rows = sum(x["rows"] for x in b)
    visited = sum(x["verifier_visited_states"] for x in v)
    terminals = sum(x["verifier_terminal_count"] for x in v)
    reply_edges = sum(x["verifier_loser_reply_edges"] for x in v)
    ratio = fixed_nodes / verbatim_nodes

    record("fixed_node_total",
           fixed_nodes == battery["fixB_total_nodes"] == 52_079_030,
           {"per_bit_sum": fixed_nodes, "recorded_total": battery["fixB_total_nodes"]})
    record("verbatim_node_total",
           verbatim_nodes == battery["published_verbatim_ms23_total_nodes"]
           == manifest["totals"]["extraction_nodes"] == 424_657_112,
           {"per_bit_sum": verbatim_nodes,
            "battery_total": battery["published_verbatim_ms23_total_nodes"],
            "manifest_total": manifest["totals"]["extraction_nodes"]})
    record("strategy_row_total",
           rows == battery["published_rows_total"] == manifest["totals"]["rows"]
           == sum(x["verifier_rows"] for x in v) == 1_693_203,
           {"battery_sum": rows, "manifest_total": manifest["totals"]["rows"],
            "bigint_sum": sum(x["verifier_rows"] for x in v)})
    record("byte_identity_and_gates",
           all(x["byte_identical"] for x in b)
           and battery["gates"]["byte_identical_32of32"]
           and battery["gates"]["fatal_zero"]
           and battery["gates"]["fbt_drops_zero"]
           and battery["gates"]["rows_match_32of32"],
           {"byte_identical": sum(x["byte_identical"] for x in b),
            "gates": battery["gates"]})
    record("fixed_memo_ratio",
           math.isclose(ratio, battery["fixB_ratio_vs_published"], abs_tol=0.00005)
           and math.isclose(ratio, 0.12263783774802292, abs_tol=1e-14),
           {"ratio": ratio, "reduction": 1 - ratio, "speedup": 1 / ratio})
    record("bigint_aggregate",
           all(x["verifier_status"] == "PASS" for x in v)
           and visited == 3_599_832 and terminals == 613_366
           and reply_edges == 3_178_030,
           {"pass": sum(x["verifier_status"] == "PASS" for x in v),
            "visited_states": visited, "terminal_count": terminals,
            "loser_reply_edges": reply_edges})

    best = min(b, key=lambda x: x["ratio_vs_published"])
    worst = max(b, key=lambda x: x["ratio_vs_published"])
    report = {
        "schema": "n11-cost73l-fixed-memo-vs-bigint-cross-audit-20261117-v1",
        "date": "2026-11-17",
        "basis": {"blob_pins": actual_pins},
        "checks": checks,
        "check_count": len(checks),
        "all_checks_pass": all(x["ok"] for x in checks),
        "totals": {
            "certificates": len(b),
            "fixed_extraction_nodes": fixed_nodes,
            "verbatim_extraction_nodes": verbatim_nodes,
            "fixed_to_verbatim_ratio": ratio,
            "node_reduction": 1 - ratio,
            "speedup": 1 / ratio,
            "byte_identical_certificates": sum(x["byte_identical"] for x in b),
            "strategy_rows": rows,
            "bigint_visited_states": visited,
            "bigint_terminal_count": terminals,
            "bigint_loser_reply_edges": reply_edges,
            "best_per_bit_ratio": {
                "bit": best["bit"], "ratio_rounded": best["ratio_vs_published"]
            },
            "worst_per_bit_ratio": {
                "bit": worst["bit"], "ratio_rounded": worst["ratio_vs_published"]
            },
        },
        "interpretation_boundary": [
            "This is a cross-audit of pinned result files, not a fresh run of the BigInt verifier.",
            "The fixed-memo battery reports byte identity with the published certificate bytes; this audit cross-checks those per-bit claims against the manifest and BigInt result records.",
            "WIN7-D10 proves only an individual seven-stone root within depth 10; REFUTED-D10 is not a LOSS proof.",
            "The standard 11x11 empty board, both two-stone roots, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
        ],
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\\n")
    if not report["all_checks_pass"]:
        raise SystemExit("cross-audit failed; inspect " + str(OUTPUT))
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
