#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Third, independent geometric reconstruction of residual-23 triple providers.

The checker enumerates triples of residual six-point D4 classes, not
23-row-plus-two-points expansions. Safety is decided by a 4x4 determinant
expanded over all 24 permutations, independent of the two published 3x3
predicates.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

INPUT_SHA256 = "51e7a465e18646097073e4f8231f89cbff327d05f9bfeac102e57c754b4ff822"
EXPECTED_SOURCE_PINS = {
    "k1097_refsolve_json_sha256": "2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40",
    "k1102_second_verification_json_sha256": "d0b5d845c234cf51c55555295f1fe3042f262cccaa0e2923c9c4205d6b6e168b",
    "eight_root_decision_json_sha256": "c5aaf83e23b6a716e981aaff745996668c60edba164fb3f5288b60ff9b8ac4d1",
}
SCHEMA = "n11-residual23-triple-provider-third-geometry-20261120-v1"


def need(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit("FAIL: " + message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bit_positions(mask: int) -> list[int]:
    out = []
    while mask:
        low = mask & -mask
        out.append(low.bit_length() - 1)
        mask ^= low
    return out


def transform_point(p: int, t: int) -> int:
    x, y = p % 11, p // 11
    if t == 0:
        X, Y = x, y
    elif t == 1:
        X, Y = 10 - y, x
    elif t == 2:
        X, Y = 10 - x, 10 - y
    elif t == 3:
        X, Y = y, 10 - x
    elif t == 4:
        X, Y = 10 - x, y
    elif t == 5:
        X, Y = x, 10 - y
    elif t == 6:
        X, Y = y, x
    else:
        X, Y = 10 - y, 10 - x
    return 11 * Y + X


TRANSFORMS = tuple(
    tuple(transform_point(p, t) for p in range(121))
    for t in range(8)
)


def transform_mask(mask: int, t: int) -> int:
    result = 0
    for p in bit_positions(mask):
        result |= 1 << TRANSFORMS[t][p]
    return result


def canonical(mask: int) -> int:
    return min(transform_mask(mask, t) for t in range(8))


def det4_permutation(points: tuple[int, int, int, int]) -> int:
    matrix = []
    for p in points:
        x, y = p % 11, p // 11
        matrix.append((x, y, x * x + y * y, 1))
    total = 0
    for perm in itertools.permutations(range(4)):
        inversions = sum(
            perm[i] > perm[j]
            for i in range(4)
            for j in range(i + 1, 4)
        )
        product = 1
        for i, j in enumerate(perm):
            product *= matrix[i][j]
        total += -product if inversions & 1 else product
    return total


def first_forbidden_quad(mask: int):
    points = bit_positions(mask)
    for quad in itertools.combinations(points, 4):
        if det4_permutation(quad) == 0:
            return {
                "indices": list(quad),
                "coordinates_xy": [[p % 11, p // 11] for p in quad],
            }
    return None


def child_orbits(root: int) -> set[int]:
    points = bit_positions(root)
    children = set()
    for removed in itertools.combinations(points, 2):
        child = root ^ (1 << removed[0]) ^ (1 << removed[1])
        children.add(canonical(child))
    return children


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    input_bytes = Path(args.input).read_bytes()
    input_sha = sha256_bytes(input_bytes)
    need(input_sha == INPUT_SHA256, "input fixture SHA-256 pin")
    fixture = json.loads(input_bytes)
    need(fixture.get("schema") == "n11-residual23-triple-provider-third-geometry-input-20261120-v1",
         "input schema")
    need(fixture.get("source_pins") == EXPECTED_SOURCE_PINS, "source pin metadata")

    rows_hex = fixture["residual_rows"]
    excluded_hex = fixture["refuted_d10_roots_excluded"]
    expected_availability = fixture["expected_per_row_triple_availability"]
    rows = [int(x, 16) for x in rows_hex]
    excluded = {int(x, 16) for x in excluded_hex}

    need(len(rows) == 23 and len(set(rows)) == 23, "23 distinct residual rows")
    need(len(excluded_hex) == 50 and len(excluded) == 50, "50 distinct excluded roots")
    need(len(expected_availability) == 23, "expected availability length")

    row_checks = []
    for i, row in enumerate(rows):
        need(row.bit_count() == 6, f"row {i} has six stones")
        need(canonical(row) == row, f"row {i} is D4-canonical")
        bad = first_forbidden_quad(row)
        need(bad is None, f"row {i} is safe")
        row_checks.append(True)

    excluded_checks = []
    for i, root in enumerate(sorted(excluded)):
        need(root.bit_count() == 8, f"excluded root {i} has eight stones")
        need(canonical(root) == root, f"excluded root {i} is D4-canonical")
        bad = first_forbidden_quad(root)
        need(bad is None, f"excluded root {i} is safe8")
        excluded_checks.append(True)

    # Every triple of distinct residual rows, under all 8^3 orientations.
    # If its union has 8 points, it uniquely determines the containing root.
    # The exhaustive histogram below proves no union has fewer than 8 points.
    union_hist = Counter()
    candidate_roots = set()
    row_triples = 0
    orientation_triples = 0
    for i, j, k in itertools.combinations(range(23), 3):
        row_triples += 1
        for ti, tj, tk in itertools.product(range(8), repeat=3):
            orientation_triples += 1
            union = (
                transform_mask(rows[i], ti)
                | transform_mask(rows[j], tj)
                | transform_mask(rows[k], tk)
            )
            size = union.bit_count()
            union_hist[size] += 1
            if size == 8:
                candidate_roots.add(canonical(union))

    need(row_triples == 1771, "C(23,3) row triples")
    need(orientation_triples == 906752, "C(23,3)*8^3 orientation triples")
    need(min(union_hist) == 8, "no three residual rows fit in fewer than eight points")
    need(union_hist[8] == 3384, "size-eight orientation unions")

    candidate_records = []
    availability = [0] * 23
    safe_count = 0
    unsafe_count = 0
    excluded_safe_count = 0
    eligible_count = 0
    candidate_coverage_hist = Counter()

    for root in sorted(candidate_roots):
        covered = child_orbits(root).intersection(rows)
        covered_indices = sorted(rows.index(row) for row in covered)
        candidate_coverage_hist[len(covered_indices)] += 1
        need(len(covered_indices) == 3, "every candidate root covers exactly three residual rows")

        forbidden = first_forbidden_quad(root)
        is_safe = forbidden is None
        is_excluded = root in excluded

        if is_safe:
            safe_count += 1
            if is_excluded:
                excluded_safe_count += 1
                classification = "safe_but_refuted_d10_excluded"
            else:
                eligible_count += 1
                classification = "eligible_triple_provider"
                for idx in covered_indices:
                    availability[idx] += 1
        else:
            unsafe_count += 1
            classification = "unsafe_cocircular_quadruple"
            need(not is_excluded, "excluded REFUTED-D10 root must be safe8")

        candidate_records.append({
            "root": f"{root:032x}",
            "covered_row_indices": covered_indices,
            "classification": classification,
            "forbidden_quad": forbidden,
        })

    need(len(candidate_roots) == 423, "423 canonical candidate roots")
    need(candidate_coverage_hist == Counter({3: 423}), "candidate coverage histogram")
    need(safe_count == 316 and unsafe_count == 107, "safe/unsafe candidate split")
    need(excluded_safe_count == 19, "19 safe candidates excluded by REFUTED-D10 list")
    need(eligible_count == 297, "297 eligible triple providers")
    need(sum(availability) == 891, "availability sum is 3*297")
    need(availability == expected_availability, "per-row availability equals pinned decision")
    need([i for i, n in enumerate(availability) if n == 0] == [1, 2, 21],
         "exactly the three published zero-provider rows")

    zero_details = []
    zero_root_union = set()
    for idx, count in enumerate(availability):
        if count != 0:
            continue
        roots_for_row = [
            rec for rec in candidate_records if idx in rec["covered_row_indices"]
        ]
        zero_root_union.update(int(rec["root"], 16) for rec in roots_for_row)
        need(len(roots_for_row) in (4, 5), "zero-row candidate-root count is 4 or 5")
        need(all(rec["classification"] != "eligible_triple_provider"
                 for rec in roots_for_row), "zero row has no eligible triple provider")
        zero_details.append({
            "row_index": idx,
            "row": rows_hex[idx],
            "eligible_triple_provider_count": 0,
            "candidate_root_count": len(roots_for_row),
            "safe_excluded_root_count": sum(
                rec["classification"] == "safe_but_refuted_d10_excluded"
                for rec in roots_for_row
            ),
            "unsafe_root_count": sum(
                rec["classification"] == "unsafe_cocircular_quadruple"
                for rec in roots_for_row
            ),
        })

    zero_union_records = [
        rec for rec in candidate_records
        if int(rec["root"], 16) in zero_root_union
    ]
    need(len(zero_root_union) == 8, "eight distinct roots across the three zero rows")
    need(sum(r["classification"] == "unsafe_cocircular_quadruple"
             for r in zero_union_records) == 5, "five unsafe zero-row candidate roots")
    need(sum(r["classification"] == "safe_but_refuted_d10_excluded"
             for r in zero_union_records) == 3, "three safe but excluded zero-row candidate roots")

    checks = [
        {"name": "fixture-sha256", "ok": True},
        {"name": "23-residual-rows-canonical-safe", "ok": all(row_checks)},
        {"name": "50-excluded-roots-canonical-safe8", "ok": all(excluded_checks)},
        {"name": "all-906752-row-orientation-triples-enumerated", "ok": True},
        {"name": "no-union-smaller-than-eight", "ok": True},
        {"name": "423-canonical-candidate-roots", "ok": True},
        {"name": "4x4-permutation-determinant-safety-classification", "ok": True},
        {"name": "316-safe-107-unsafe", "ok": True},
        {"name": "19-safe-candidates-excluded", "ok": True},
        {"name": "297-eligible-triple-providers", "ok": True},
        {"name": "all-23-per-row-counts-match-pinned-decision", "ok": True},
        {"name": "zero-provider-rows-explained-by-eight-candidate-roots", "ok": True},
    ]

    result = {
        "schema": SCHEMA,
        "status": "third-independent-geometric-reconstruction-passed",
        "inputs": {
            "fixture_sha256": input_sha,
            "source_pins": EXPECTED_SOURCE_PINS,
            "residual_rows": 23,
            "excluded_refuted_d10_roots": 50,
        },
        "method": {
            "enumeration_unit": "three distinct residual six-stone D4 classes with all 8^3 orientations",
            "safety_predicate": "4x4 determinant of rows (x, y, x^2+y^2, 1), expanded over all 24 permutations",
            "coverage_predicate": "all C(8,6)=28 children, each D4-canonicalized independently",
            "independence_note": "does not call either published 3x3 determinant predicate or the 23-row-plus-two-points universe generator",
        },
        "enumeration": {
            "residual_row_triples": row_triples,
            "orientation_triples": orientation_triples,
            "union_size_histogram": {str(k): union_hist[k] for k in sorted(union_hist)},
            "candidate_root_classes": len(candidate_roots),
            "candidate_coverage_histogram": {str(k): candidate_coverage_hist[k]
                                             for k in sorted(candidate_coverage_hist)},
            "safe_candidate_roots": safe_count,
            "unsafe_candidate_roots": unsafe_count,
            "safe_candidates_in_refuted_d10_exclusion": excluded_safe_count,
            "eligible_triple_providers_in_P3": eligible_count,
            "eligible_coverage_histogram": {"3": eligible_count},
            "per_row_triple_availability": availability,
            "availability_sum": sum(availability),
        },
        "zero_provider_rows": zero_details,
        "zero_rows_candidate_root_union": [
            {
                "root": rec["root"],
                "covered_row_indices": rec["covered_row_indices"],
                "classification": rec["classification"],
                "forbidden_quad_xy": (
                    rec["forbidden_quad"]["coordinates_xy"]
                    if rec["forbidden_quad"] is not None else None
                ),
            }
            for rec in zero_union_records
        ],
        "checks": checks,
        "checks_all_ok": all(c["ok"] for c in checks),
        "interpretation_guard": [
            "This is a finite geometric provider reconstruction, not a game-theoretic verdict.",
            "REFUTED-D10 is not a LOSS proof.",
            "No S6 row is closed and no receipt is created by this audit.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
        ],
    }

    output_bytes = (json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
    Path(args.output).write_bytes(output_bytes)
    print(json.dumps({
        "status": result["status"],
        "output_sha256": sha256_bytes(output_bytes),
        "output_bytes": len(output_bytes),
        "checks": len(checks),
        "candidate_root_classes": len(candidate_roots),
        "safe": safe_count,
        "unsafe": unsafe_count,
        "excluded_safe": excluded_safe_count,
        "eligible_triple_providers": eligible_count,
        "zero_rows": [x["row"] for x in zero_details],
        "zero_union_roots": len(zero_root_union),
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
