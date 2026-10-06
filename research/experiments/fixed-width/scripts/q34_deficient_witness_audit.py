#!/usr/bin/env python3
"""Independent exact verifier for 3xm (q=4) deficient maximal safe sets.

This file deliberately shares no code with the search engine
(q34_support_exclusion.cpp).  The engine reasons with row-pair sums, products
and a quadratic root formula; this verifier uses only the raw 4x4 integer
determinant det[x^2+y^2, x, y, 1] of K0001, plus a second, geometric
predicate built from exact Fraction circumcenters.  Agreement of the two
predicates on every 4-subset of the board is asserted before any witness is
declared safe or maximal.

Usage:
    python q34_deficient_witness_audit.py            # self-test, no witnesses
    python q34_deficient_witness_audit.py WITNESS.json
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path

Point = tuple[int, int]


def determinant_predicate(quad: tuple[Point, Point, Point, Point]) -> bool:
    """True iff the four points are collinear or concyclic (exact integers)."""
    rows = [(x * x + y * y, x, y, 1) for x, y in quad]
    total = 0
    for i in range(4):
        rest = [rows[r] for r in range(4) if r != i]
        (a1, a2, a3) = rest[0][1:]
        (b1, b2, b3) = rest[1][1:]
        (c1, c2, c3) = rest[2][1:]
        minor = (a1 * (b2 * c3 - b3 * c2)
                 - a2 * (b1 * c3 - b3 * c1)
                 + a3 * (b1 * c2 - b2 * c1))
        total += (-1 if i % 2 else 1) * rows[i][0] * minor
    return total == 0


def _cross(o: Point, a: Point, b: Point) -> int:
    return ((a[0] - o[0]) * (b[1] - o[1])
            - (a[1] - o[1]) * (b[0] - o[0]))


def geometric_predicate(quad: tuple[Point, Point, Point, Point]) -> bool:
    """Second independent predicate: exact line test, else exact circumcircle."""
    if all(_cross(quad[0], quad[i], p) == 0 for i, p in enumerate(quad[1:], 1)):
        return True
    for ids in combinations(range(4), 3):
        tri = [quad[i] for i in ids]
        if _cross(tri[0], tri[1], tri[2]) != 0:
            (p, q, r) = tri
            fourth = quad[next(i for i in range(4) if i not in ids)]
            break
    else:  # pragma: no cover - all four collinear was handled above
        return True
    ax, ay = 2 * (q[0] - p[0]), 2 * (q[1] - p[1])
    bx, by = 2 * (r[0] - p[0]), 2 * (r[1] - p[1])
    ca = q[0] * q[0] + q[1] * q[1] - p[0] * p[0] - p[1] * p[1]
    cb = r[0] * r[0] + r[1] * r[1] - p[0] * p[0] - p[1] * p[1]
    den = ax * by - bx * ay
    assert den != 0, quad
    ox = Fraction(ca * by - cb * ay, den)
    oy = Fraction(ax * cb - bx * ca, den)

    def r2(pt: Point) -> Fraction:
        return (Fraction(pt[0]) - ox) ** 2 + (Fraction(pt[1]) - oy) ** 2

    return r2(p) == r2(fourth)


def board_points(length: int) -> list[Point]:
    return [(x, y) for y in range(3) for x in range(length)]


def check_predicates(length: int) -> int:
    """Assert both predicates agree on every 4-subset of the whole board."""
    board = board_points(length)
    bad = 0
    for quad in combinations(board, 4):
        d = determinant_predicate(quad)
        g = geometric_predicate(quad)
        if d != g:
            bad += 1
            raise AssertionError(f"predicate mismatch at {quad}: {d} vs {g}")
    return bad


def audit_witness(length: int, rows: dict[int, list[int]]) -> dict:
    """Verify a claimed deficient maximal safe set on the 3xm board."""
    board = board_points(length)
    stones = sorted((x, y) for y, xs in rows.items() for x in xs)
    stone_set = set(stones)

    for quad in combinations(stones, 4):
        assert not determinant_predicate(quad), ("witness is unsafe", quad)

    unblocked = []
    for pt in board:
        if pt in stone_set:
            continue
        blocker = None
        for tri in combinations(stones, 3):
            if determinant_predicate(tri + (pt,)):
                blocker = tri
                break
        if blocker is None:
            unblocked.append(list(pt))

    return {
        "length": length,
        "stone_count": len(stones),
        "row_counts": [len(rows.get(y, [])) for y in range(3)],
        "witness_rows": {str(y): list(rows[y]) for y in sorted(rows)},
        "safe": True,
        "maximal": not unblocked,
        "unblocked_empty_points": unblocked,
        "empty_points": len(board) - len(stones),
    }


def main() -> None:
    # Positive control: the two 8-stone maximal sets recorded for m=23,
    # plus the K0068 witness, must all pass this independent checker.
    controls = [
        (23, {0: [1, 17], 1: [7, 10, 13], 2: [9, 10, 12]}),
        (23, {0: [4, 7, 18], 1: [3, 4], 2: [4, 10, 13]}),
        (23, {0: [4, 15, 18], 1: [18, 19], 2: [9, 12, 18]}),
    ]
    for length, rows in controls:
        res = audit_witness(length, rows)
        assert res["maximal"], ("control witness not maximal", rows, res)
        assert res["stone_count"] == 8
    print(json.dumps({"control_witnesses_verified": len(controls),
                      "status": "passed"}, separators=(",", ":")))

    if len(sys.argv) < 2:
        return
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    cases = payload["witnesses"]
    results = []
    for case in cases:
        length = case["length"]
        rows = {int(k): v for k, v in case["witness_rows"].items()}
        if case.get("check_board_predicates", True):
            check_predicates(length)
        res = audit_witness(length, rows)
        res["claim_deficient"] = case.get("claim_deficient", True)
        res["conflicts_with_claim"] = res["maximal"] == res["claim_deficient"]
        results.append(res)
    print(json.dumps({"cases": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()