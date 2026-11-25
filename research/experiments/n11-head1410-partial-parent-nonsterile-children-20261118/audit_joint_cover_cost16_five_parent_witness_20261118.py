#!/usr/bin/env python3
"""Independent exact-cover audit for the five-parent cost-16 joint witness.

This verifier deliberately does not import the published blossom/matching code
or the generated global-candidate-roots JSONL. It reconstructs the 112 target
rows from the pinned head-1410 worklist, K0865 sterile census, and head-1410
to head-1476 fold ledger; then it independently enumerates every legal
S6-to-S7 survival extension using exact integer determinants.

The resulting candidate-root coverage universe has maximum span 2. The
published 56-root witness is independently checked to cover each of the 112
target rows exactly once, with every selected seven-stone root safe. Therefore
56 is the exact minimum candidate-root cover size (lower bound 112/2 and a
witness attaining it). This is cover planning only: no root is thereby a
WIN7-D10 certificate.
"""
from __future__ import annotations

import csv
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXP = ROOT / "research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118"
OUT = EXP / "output/joint-cover-cost16-five-parent-independent-audit-20261118.json"

PINS = {
    "worklist": (
        ROOT / "research/experiments/n11-class2-lane-closability-ranking-20261116/output/class-frontier-remaining-s6-worklist-1410-20261116.csv",
        "2fee1d0718547a62e346d35f5858d7913e37c097",
    ),
    "census": (
        ROOT / "research/experiments/n11-head1410-receipt-unclosability-census-20261116/output/n11-head1410-receipt-unclosability-census-20261116.json",
        "9c251da3138c5cb0516e097be5e5d0427dfaf5f0",
    ),
    "ledger": (
        EXP / "output/fold-chain-ledger-1410-1476-crosscheck-20261118.json",
        "e8785d509e8a11a37c0d03cc450455a14708c34d",
    ),
    "joint": (
        EXP / "output/joint-parent-cover-sharing-cost16-20261118.json",
        "40581746dc3304bdaff4b1934fd6f1d3d2981ea5",
    ),
}

PARENTS = [
    "00000000000000403800000008000000",  # individual minimum 6
    "00000000000000821082000000000000",  # individual minimum 9
    "00000000000000003800000008002000",  # individual minimum 12
    "00000000000000003800000009000000",  # individual minimum 15
    "00000000000000003800000008001000",  # individual minimum 16
]
EXPECTED_PARENT_ROWS = [11, 18, 23, 29, 31]
EXPECTED_SPAN_HISTOGRAM = {"1": 4885, "2": 1657}
N = 11
CELLS = N * N


def git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def read_pinned(name: str) -> bytes:
    path, expected = PINS[name]
    data = path.read_bytes()
    actual = git_blob_sha(data)
    if actual != expected:
        raise SystemExit(f"input pin mismatch for {name}: {actual} != {expected}")
    return data


def xy(i: int) -> tuple[int, int]:
    return i % N, i // N


def transform_xy(x: int, y: int, t: int) -> tuple[int, int]:
    if t == 0:
        return x, y
    if t == 1:
        return y, N - 1 - x
    if t == 2:
        return N - 1 - x, N - 1 - y
    if t == 3:
        return N - 1 - y, x
    if t == 4:
        return N - 1 - x, y
    if t == 5:
        return x, N - 1 - y
    if t == 6:
        return y, x
    return N - 1 - y, N - 1 - x


def canon(mask: int) -> str:
    best = None
    for t in range(8):
        out = 0
        for i in range(CELLS):
            if (mask >> i) & 1:
                x, y = xy(i)
                tx, ty = transform_xy(x, y, t)
                out |= 1 << (ty * N + tx)
        if best is None or out < best:
            best = out
    return f"{best:032x}"


def bit_indices(mask: int) -> list[int]:
    result = []
    while mask:
        low = mask & -mask
        result.append(low.bit_length() - 1)
        mask ^= low
    return result


def det3(a: int, b: int, c: int) -> int:
    pts = [xy(i) for i in (a, b, c)]
    p, q, r = [(x * x + y * y, x, y) for x, y in pts]
    return (
        p[0] * (q[1] * r[2] - q[2] * r[1])
        - p[1] * (q[0] * r[2] - q[2] * r[0])
        + p[2] * (q[0] * r[1] - q[1] * r[0])
    )


def det4(a: int, b: int, c: int, d: int) -> int:
    return det3(a, b, c) - det3(a, b, d) + det3(a, c, d) - det3(b, c, d)


def is_safe(mask: int) -> bool:
    stones = bit_indices(mask)
    return all(
        det4(a, b, c, d) != 0
        for a, b, c, d in itertools.combinations(stones, 4)
    )


def main() -> None:
    checks = []

    def check(name: str, condition: bool, detail=None) -> None:
        checks.append({
            "name": name,
            "pass": bool(condition),
            "detail": "" if detail is None else detail,
        })

    worklist_bytes = read_pinned("worklist")
    census_bytes = read_pinned("census")
    ledger_bytes = read_pinned("ledger")
    joint_bytes = read_pinned("joint")

    worklist = list(csv.DictReader(worklist_bytes.decode("utf-8").splitlines()))
    census = json.loads(census_bytes)
    ledger = json.loads(ledger_bytes)
    joint = json.loads(joint_bytes)

    worklist_hex = [row["s6_canonical_hex"] for row in worklist]
    closed = set(ledger["derived"]["closed_rows_66"])
    sterile = {row["hex"] for row in census["sterile_row_registry"]}
    open_rows = sorted(set(worklist_hex) - closed - sterile)

    check("worklist.count", len(worklist) == 6438, len(worklist))
    check("worklist.unique", len(set(worklist_hex)) == 6438, len(set(worklist_hex)))
    check("closed.rows", len(closed) == 66, len(closed))
    check("sterile.rows", len(sterile) == 35, len(sterile))
    check("open.rows", len(open_rows) == 6337, len(open_rows))

    targets = {parent: set() for parent in PARENTS}
    for row_hex in open_rows:
        mask = int(row_hex, 16)
        stones = bit_indices(mask)
        if len(stones) != 6 or canon(mask) != row_hex:
            raise SystemExit(f"invalid/noncanonical S6 row: {row_hex}")
        parents_of_row = {
            canon(mask ^ (1 << bit))
            for bit in stones
        }
        for parent in PARENTS:
            if parent in parents_of_row:
                targets[parent].add(row_hex)

    target_counts = [len(targets[parent]) for parent in PARENTS]
    check("parent.row-counts", target_counts == EXPECTED_PARENT_ROWS, target_counts)
    target_union = set().union(*targets.values())
    check("parent.targets-disjoint", len(target_union) == sum(target_counts) == 112,
          {"union": len(target_union), "sum": sum(target_counts)})

    row_owner = {}
    for parent, rows in targets.items():
        for row_hex in rows:
            if row_hex in row_owner:
                raise SystemExit(f"target row belongs to two parents: {row_hex}")
            row_owner[row_hex] = parent

    root_rows = defaultdict(set)
    candidate_occurrences = 0
    target_rows_safe = 0
    for row_hex in sorted(target_union):
        mask = int(row_hex, 16)
        stones = bit_indices(mask)
        if not is_safe(mask):
            raise SystemExit(f"unsafe target S6 row: {row_hex}")
        target_rows_safe += 1
        for cell in range(CELLS):
            if (mask >> cell) & 1:
                continue
            if any(
                det4(a, b, c, cell) == 0
                for a, b, c in itertools.combinations(stones, 3)
            ):
                continue
            candidate_occurrences += 1
            root_hex = canon(mask | (1 << cell))
            root_rows[root_hex].add(row_hex)

    span_histogram = Counter(len(rows) for rows in root_rows.values())
    span_json = {str(k): span_histogram[k] for k in sorted(span_histogram)}
    max_span = max(span_histogram)

    check("candidate.occurrences", candidate_occurrences == 8199, candidate_occurrences)
    check("candidate.distinct-roots", len(root_rows) == 6542, len(root_rows))
    check("candidate.span-histogram", span_json == EXPECTED_SPAN_HISTOGRAM, span_json)
    check("candidate.max-span", max_span == 2, max_span)
    check("candidate.all-roots-safe", all(is_safe(int(root, 16)) for root in root_rows),
          len(root_rows))
    check("target.rows-safe", target_rows_safe == 112, target_rows_safe)

    joint_result = next(
        result for result in joint["derived"]["joint_results"]
        if result["subset"] == PARENTS
    )
    candidate_cross_parent_count = sum(
        1 for covered_rows in root_rows.values()
        if len({row_owner[row_hex] for row_hex in covered_rows}) > 1
    )
    witness_roots = joint_result["witness_roots"]
    check("published.joint-summary",
          joint_result["rows_union"] == 112
          and joint_result["candidates"] == 8199
          and joint_result["distinct_roots"] == 6542
          and joint_result["maxspan"] == 2
          and joint_result["max_matching"] == 56
          and joint_result["witness_size"] == 56
          and joint_result["exact"] is True,
          {
              "rows_union": joint_result["rows_union"],
              "candidates": joint_result["candidates"],
              "distinct_roots": joint_result["distinct_roots"],
              "max_matching": joint_result["max_matching"],
              "witness_size": joint_result["witness_size"],
          })
    check("witness.count", len(witness_roots) == 56, len(witness_roots))
    check("witness.unique", len(set(witness_roots)) == 56, len(set(witness_roots)))

    coverage = Counter()
    witness_pairs = []
    cross_parent_count = 0
    for root_hex in witness_roots:
        root_mask = int(root_hex, 16)
        stones = bit_indices(root_mask)
        if len(stones) != 7 or canon(root_mask) != root_hex:
            raise SystemExit(f"invalid/noncanonical witness root: {root_hex}")
        if not is_safe(root_mask):
            raise SystemExit(f"unsafe witness root: {root_hex}")
        covered_rows = sorted(root_rows.get(root_hex, set()))
        if len(covered_rows) != 2:
            raise SystemExit(
                f"witness root does not cover exactly two target rows: "
                f"{root_hex} -> {covered_rows}"
            )
        coverage.update(covered_rows)
        owners = {row_owner[row_hex] for row_hex in covered_rows}
        if len(owners) == 2:
            cross_parent_count += 1
        witness_pairs.append({"root": root_hex, "rows": covered_rows})

    coverage_histogram = Counter(coverage.get(row_hex, 0) for row_hex in target_union)
    check("witness.roots-safe", True, 56)
    check("witness.each-covers-two", len(witness_pairs) == 56
          and all(len(pair["rows"]) == 2 for pair in witness_pairs), 56)
    check("witness.partitions-target", coverage_histogram == Counter({1: 112}),
          {str(k): v for k, v in sorted(coverage_histogram.items())})
    check("candidate.cross-parent-count",
          candidate_cross_parent_count == joint_result["cross_parent_roots"],
          {"independent": candidate_cross_parent_count,
           "published": joint_result["cross_parent_roots"]})
    check("witness.cross-parent-count", cross_parent_count == 10,
          cross_parent_count)

    lower_bound = (len(target_union) + max_span - 1) // max_span
    check("minimum.lower-bound", lower_bound == 56, lower_bound)
    check("minimum.witness-attains-bound", len(witness_roots) == lower_bound,
          {"witness": len(witness_roots), "lower_bound": lower_bound})

    all_pass = all(item["pass"] for item in checks)
    output = {
        "schema": "n11-joint-cover-cost16-five-parent-independent-audit-20261118-v1",
        "date": "2026-11-18",
        "base_main": "0ce32ace2dae155da1f2e49b95fe07ec0f08067d",
        "method": (
            "Independent Python reconstruction from pinned worklist/census/ledger/joint output; "
            "D4 canonicalization and det4 survival-move enumeration are implemented locally. "
            "No blossom code or generated candidate-root JSONL is imported."
        ),
        "inputs": {
            name: {"path": str(path.relative_to(ROOT)), "git_blob_sha1": pin}
            for name, (path, pin) in PINS.items()
        },
        "derived": {
            "open_s6_rows": len(open_rows),
            "target_rows_by_parent": {
                parent: len(targets[parent]) for parent in PARENTS
            },
            "target_union_rows": len(target_union),
            "candidate_occurrences": candidate_occurrences,
            "distinct_d4_roots": len(root_rows),
            "root_coverage_histogram": span_json,
            "maximum_root_span": max_span,
            "witness_root_count": len(witness_roots),
            "cross_parent_candidate_roots": candidate_cross_parent_count,
            "cross_parent_witness_roots": cross_parent_count,
            "target_rows_covered_exactly_once": sum(
                1 for row_hex in target_union if coverage.get(row_hex, 0) == 1
            ),
            "minimum_candidate_root_cover_size": lower_bound,
            "witness_pairs": witness_pairs,
        },
        "checks": checks,
        "check_count": len(checks),
        "all_pass": all_pass,
        "interpretation_guard": (
            "This proves the exact minimum size of the candidate-root cover for the 112-row "
            "union only. It does not prove that any selected root has a WIN7-D10 certificate, "
            "does not close an S5 parent, and does not assign LOSS to REFUTED-D10 or STERILE rows."
        ),
        "unknown_status": (
            "Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, "
            "S2 {59,60}, and classes 1/2/4 remain UNKNOWN."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not all_pass:
        raise SystemExit("audit checks failed")
    print(json.dumps({
        "all_pass": all_pass,
        "check_count": len(checks),
        "target_union_rows": len(target_union),
        "candidate_occurrences": candidate_occurrences,
        "distinct_d4_roots": len(root_rows),
        "span_histogram": span_json,
        "witness_root_count": len(witness_roots),
        "cross_parent_witness_roots": cross_parent_count,
        "minimum_candidate_root_cover_size": lower_bound,
        "output": str(OUT.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
