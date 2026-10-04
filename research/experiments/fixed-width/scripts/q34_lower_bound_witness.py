#!/usr/bin/env python3
"""Independent audit for the 3xm, q=4 lower-bound witness at m=23.

The game forbids four collinear or four concyclic lattice points.
This script checks the witness with two exact predicates:

1. translated lifted determinant;
2. a geometric predicate using exact Fraction circumcenters.

It also checks both predicates on every 4-subset of the full 3x23 board,
then verifies safety and maximality of the 8-stone witness.
"""
from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

M = 23
WITNESS_ROWS = {
    0: [4, 15, 18],
    1: [18, 19],
    2: [9, 12, 18],
}

Point = tuple[int, int]


def cross(a: Point, b: Point, c: Point) -> int:
    return ((b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0]))


def forbidden_det(points: tuple[Point, Point, Point, Point]) -> bool:
    """Zero translated incircle determinant = one line or one circle."""
    a, b, c, d = points
    x4, y4 = d
    rows = []
    for x, y in (a, b, c):
        X, Y = x - x4, y - y4
        rows.append((X, Y, X * X + Y * Y))
    (x1, y1, r1), (x2, y2, r2), (x3, y3, r3) = rows
    det = (
        r1 * (x2 * y3 - y2 * x3)
        - r2 * (x1 * y3 - y1 * x3)
        + r3 * (x1 * y2 - y1 * x2)
    )
    return det == 0


def forbidden_geometric(points: tuple[Point, Point, Point, Point]) -> bool:
    """Independent exact characterization by line/circumcircle geometry."""
    a = points[0]
    if all(cross(a, points[1], p) == 0 for p in points[2:]):
        return True

    tri = None
    fourth = None
    for ids in combinations(range(4), 3):
        aa, bb, cc = (points[i] for i in ids)
        if cross(aa, bb, cc) != 0:
            tri = (aa, bb, cc)
            fourth = points[next(i for i in range(4) if i not in ids)]
            break
    assert tri is not None and fourth is not None
    aa, bb, cc = tri

    A1 = 2 * (bb[0] - aa[0])
    B1 = 2 * (bb[1] - aa[1])
    C1 = bb[0] * bb[0] + bb[1] * bb[1] - aa[0] * aa[0] - aa[1] * aa[1]
    A2 = 2 * (cc[0] - aa[0])
    B2 = 2 * (cc[1] - aa[1])
    C2 = cc[0] * cc[0] + cc[1] * cc[1] - aa[0] * aa[0] - aa[1] * aa[1]
    den = A1 * B2 - A2 * B1
    assert den != 0

    ox = Fraction(C1 * B2 - C2 * B1, den)
    oy = Fraction(A1 * C2 - A2 * C1, den)

    def radius2(p: Point) -> Fraction:
        return (Fraction(p[0]) - ox) ** 2 + (Fraction(p[1]) - oy) ** 2

    return radius2(aa) == radius2(fourth)


def main() -> None:
    board = [(x, y) for y in range(3) for x in range(M)]
    witness = sorted((x, y) for y, xs in WITNESS_ROWS.items() for x in xs)
    witness_set = set(witness)

    forbidden_count = 0
    for quad in combinations(board, 4):
        q = tuple(quad)
        d = forbidden_det(q)
        g = forbidden_geometric(q)
        assert d == g, ("predicate mismatch", q, d, g)
        forbidden_count += int(d)

    bad_witness_quads = [
        list(q) for q in combinations(witness, 4)
        if forbidden_det(tuple(q))
    ]
    assert not bad_witness_quads

    blocking = []
    for p in board:
        if p in witness_set:
            continue
        blocker = None
        for tri in combinations(witness, 3):
            if forbidden_det(tuple(tri) + (p,)):
                blocker = tri
                break
        assert blocker is not None, ("unblocked point", p)
        blocking.append({
            "point": list(p),
            "triple": [list(q) for q in blocker],
        })

    result = {
        "board": {"width": 3, "length": M, "q": 4},
        "witness_rows": {str(y): WITNESS_ROWS[y] for y in range(3)},
        "stone_count": len(witness),
        "row_counts": [len(WITNESS_ROWS[y]) for y in range(3)],
        "full_capacity": 9,
        "safe": True,
        "maximal": True,
        "empty_points": len(board) - len(witness),
        "blocked_empty_points": len(blocking),
        "middle_row_empty_points": M - len(WITNESS_ROWS[1]),
        "middle_row_blocked_empty_points": sum(
            1 for item in blocking if item["point"][1] == 1
        ),
        "unblocked_empty_points": [],
        "board_forbidden_quadruples": forbidden_count,
        "predicate_agreement_all_board_quadruples": True,
        "witness_forbidden_quadruples": 0,
        "conclusion": "M_{3,4} >= 24",
    }

    out = Path(__file__).resolve().parents[1] / "output" / "q34_lower_bound_witness.json"
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
