#!/usr/bin/env python3
"""Derive a conservative hybrid-seed plan from the published cost73k summary.

This script does not reconstruct keys, insert a seed, or run the game engine.
It proves only the set-cardinality arithmetic and the insertion-order bound
for appending the 2-way-only records after the existing boundary-4way seed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED_INPUT_BLOB = "b97c9334f04f98f6ba7bb8a4c8b1de9689810d5e"
EXPECTED_ORCHESTRATOR_BLOB = "5ac1e3c0ec47ec3f9ae63ed709362feb5a1df213"
INPUT_NAME = "worker-split4-boundary-memo-merge-73k-20261117.json"
ORCHESTRATOR_NAME = "measure_worker_split4_boundary_memo_merge_73k_20261117.py"


def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\\0"
    return hashlib.sha1(header + data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def derive(document: dict, loader_order_verified: bool) -> dict:
    comparison = document["final4_vs_seed2"]
    final4 = document["cascade_merge"]["final"]
    seedrun = document["seedrun"]["seed"]
    reference = document["published_reference"]

    final4_keys = final4["occupied_after"]
    seed2_keys = reference["merged2_occupied_after"]
    shared = comparison["shared"]
    only_seed2 = comparison["only_in_seed2"]
    only_final4 = comparison["only_in_final4"]
    union_keys = shared + only_seed2 + only_final4

    require(final4_keys == shared + only_final4,
            "boundary FINAL4 partition does not close")
    require(seed2_keys == shared + only_seed2,
            "published 2-way partition does not close")
    require(union_keys == final4_keys + only_seed2,
            "hybrid union != FINAL4 plus 2-way-only keys")
    require(union_keys == seed2_keys + only_final4,
            "hybrid union != 2-way plus FINAL4-only keys")
    require(document["gates"]["final4_monotone"] is True,
            "FINAL4 is not certified monotone over shared 2-way keys")
    require(comparison["value_violations"] == 0,
            "shared key values have a monotonicity violation")
    require(seedrun["seeded"] == final4_keys,
            "published boundary seedrun count differs from FINAL4 key count")
    require(loader_order_verified,
            "seedMemo file-order behavior was not verified")

    max_extra_failures = only_seed2
    ms24_failure_upper = seedrun["failed"] + max_extra_failures
    return {
        "schema": "n11-class2-lane-hybrid-seed-union-design-73k-20261117-v1",
        "date": "2026-11-17",
        "lane": "n11 class2-lane long-term (cost73k)",
        "status": "DESIGN_DERIVED_NOT_MEASURED",
        "source_counts": {
            "boundary_final4_keys": final4_keys,
            "published_2way_seed_keys": seed2_keys,
            "shared_keys": shared,
            "only_in_boundary_final4": only_final4,
            "only_in_published_2way_seed": only_seed2,
            "shared_value_violations": comparison["value_violations"],
            "boundary_final4_seed_md5": final["seed_md5"],
            "published_2way_seed_md5": reference["merged2_seed_md5"],
        },
        "derived_hybrid": {
            "key_count": union_keys,
            "construction": (
                "Keep boundary FINAL4 records in existing order under one "
                "header; append only-in-2way records in deterministic key "
                "order, without a second header."
            ),
            "is_superset_of_both_by_published_set_counts": True,
            "initial_load_factor_ms_1_25": union_keys / (1 << 25),
            "extra_keys_as_fraction_of_final4": only_seed2 / final4_keys,
            "seed_loader_consumes_lines_in_file_order": loader_order_verified,
            "base_insertions_preserved_if_extras_are_appended": True,
            "max_additional_insert_failures_after_base": max_extra_failures,
        },
        "capacity_bounds": {
            "boundary_final4_seedrun_ms_1_24_seeded": seedrun["seeded"],
            "boundary_final4_seedrun_ms_1_24_failed": seedrun["failed"],
            "hybrid_ms_1_24_failure_upper_bound_if_appended": ms24_failure_upper,
            "hybrid_ms_1_24_failure_rate_upper_bound": ms24_failure_upper / union_keys,
            "hybrid_ms_1_25_failure_count": None,
            "hybrid_ms_1_25_band_nodes": None,
            "warning": (
                "The published 28-failure MS=1<<25 run used the node-balanced "
                "4-way seed (4,985,986 keys), not this boundary-preserving "
                "FINAL4 seed (4,975,265 keys); its failure count is not transferable."
            ),
        },
        "checks": {
            "final4_partition": True,
            "seed2_partition": True,
            "union_arithmetic": True,
            "shared_values_monotone": True,
            "loader_consumes_input_in_file_order": loader_order_verified,
        },
        "next_measurement": [
            "Reconstruct the exact 262 only-in-2way key/value records from the pinned 2-way and boundary-4way distinct tables.",
            "Append them after FINAL4 without reordering existing FINAL4 records; use one KYOENWM2 header.",
            "Run the hybrid seed at MS=1<<25 and record inserted/failed counts, conflict count, and full record-identity results.",
            "Run all 22 roots and require 22/22 certificate byte identity; compare per-bit nodes against boundary-4way-only and node-balanced-4way seeds.",
        ],
        "interpretation_guard": (
            "Design arithmetic only. The 262 records have not been reconstructed "
            "or inserted; no hybrid seedrun or band search was executed; no new "
            "WIN/LOSS verdicts, certificate bytes, or receipt folds. Standard 11x11 remains UNKNOWN."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path(__file__).resolve().parent.parent / "output" / INPUT_NAME)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent.parent / "output" / "hybrid-seed-union-design-73k-20261117.json")
    parser.add_argument("--skip-pins", action="store_true", help="fixture-only test mode")
    args = parser.parse_args()

    input_bytes = args.input.read_bytes()
    document = json.loads(input_bytes)
    if not args.skip_pins:
        require(git_blob_sha(input_bytes) == EXPECTED_INPUT_BLOB,
                "input Git blob SHA mismatch")
        orchestrator = Path(__file__).resolve().parent / ORCHESTRATOR_NAME
        orchestrator_bytes = orchestrator.read_bytes()
        require(git_blob_sha(orchestrator_bytes) == EXPECTED_ORCHESTRATOR_BLOB,
                "orchestrator Git blob SHA mismatch")
        source = orchestrator_bytes.decode("utf-8")
        start = source.index("export function seedMemo")
        end = source.index('"""', start)
        loader_body = source[start:end]
        loader_order_verified = (
            "for (const l of lines)" in loader_body and ".sort(" not in loader_body
        )
    else:
        loader_order_verified = True

    result = derive(document, loader_order_verified)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "hybrid_keys": result["derived_hybrid"]["key_count"],
        "ms25_load": result["derived_hybrid"]["initial_load_factor_ms_1_25"],
        "ms24_failure_upper_bound": result["capacity_bounds"]["hybrid_ms_1_24_failure_upper_bound_if_appended"],
        "ms25_failure_count": None,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
