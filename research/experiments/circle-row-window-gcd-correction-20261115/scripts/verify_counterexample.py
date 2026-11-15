#!/usr/bin/env python3
"""Exact regression for the corrected circle row-window denominator lemma.

Run from the repository root:
  python research/experiments/circle-row-window-gcd-correction-20261115/scripts/verify_counterexample.py
Uses only the Python standard library and prints deterministic JSON.
"""
from fractions import Fraction
from itertools import combinations
from math import gcd, isqrt
import json


def lattice_points_on_circle():
    # 9(x+2)^2 + (3y+14)^2 = 325.
    # sqrt(325) < 19 gives -18 <= 3y+14 <= 18, hence -10 <= y <= 1.
    points = set()
    for y in range(-10, 2):
        remainder = 325 - (3 * y + 14) ** 2
        if remainder < 0 or remainder % 9:
            continue
        square = remainder // 9
        root = isqrt(square)
        if root * root == square:
            points.add((-2 - root, y))
            points.add((-2 + root, y))
    return sorted(points)


def row_difference_gcd(rows):
    rows = sorted(rows)
    g = 0
    for y in rows[1:]:
        g = gcd(g, y - rows[0])
    return g


def main():
    points = lattice_points_on_circle()
    expected_points = [
        (-8, -5), (-7, -8), (-4, 1),
        (0, 1), (3, -8), (4, -5),
    ]
    assert points == expected_points
    assert all(9 * (x + 2) ** 2 + (3 * y + 14) ** 2 == 325
               for x, y in points)

    rows = sorted({y for _, y in points})
    beta = Fraction(-14, 3)
    twice_beta = 2 * beta
    q = twice_beta.denominator
    w = 10
    d = len(rows)
    g = row_difference_gcd(rows)
    floor_bound = (w - 1) // (d - 1)
    ceil_bound = (w - 1 + (d - 1) - 1) // (d - 1)
    gaps = sorted({rows[j] - rows[i]
                   for i in range(d) for j in range(i + 1, d)})

    assert rows == [-8, -5, 1]
    assert q == 3
    assert g == 3
    assert g <= floor_bound == 4
    assert (4 * g) % q == 0
    assert (4 * ceil_bound) % q != 0
    assert all((4 * delta) % q == 0 for delta in gaps)

    # Exhaust all row subsets in a 7-row window for the cases used by K0830.
    seven_row_counts = {}
    for double_rows in (4, 5):
        count = 0
        for subset in combinations(range(7), double_rows):
            subset_gcd = row_difference_gcd(subset)
            bound = (7 - 1) // (double_rows - 1)
            assert subset_gcd <= bound
            if double_rows == 5:
                assert subset_gcd == 1
                assert 4 * subset_gcd == 4
            else:
                assert subset_gcd in (1, 2)
                assert 8 % (4 * subset_gcd) == 0
            count += 1
        seven_row_counts[str(double_rows)] = count

    result = {
        "circle_equation": "9(x+2)^2 + (3y+14)^2 = 325",
        "center": {"x": "-2", "y": "-14/3"},
        "twice_beta_reduced": "-28/3",
        "q": q,
        "points": [list(point) for point in points],
        "double_rows": rows,
        "window": {"first_row": -8, "last_row": 1, "w": w},
        "d": d,
        "gcd_of_row_differences": g,
        "floor_bound": floor_bound,
        "old_ceil_bound": ceil_bound,
        "q_divides_4g": True,
        "q_divides_4_old_ceil": False,
        "pairwise_gaps": gaps,
        "seven_row_subset_counts": seven_row_counts,
        "result": "PASS",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
