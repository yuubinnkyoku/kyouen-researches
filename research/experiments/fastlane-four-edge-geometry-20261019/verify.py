#!/usr/bin/env python3
"""Exact 4x4 determinant enumeration and subset Grundy DP (no dependencies)."""
from itertools import combinations

POINTS = (
    (12, 8), (-8, 0), (2, 0), (-2, 0), (3, 5), (0, 4),
    (0, -4), (24, -16), (12, -4), (24, -4), (12, -16),
)
EXPECTED = (
    (0, 6, 9, 10), (1, 2, 5, 6),
    (3, 4, 5, 6), (7, 8, 9, 10),
)
CHILDREN = (4, 0, 0, 0, 0, 2, 1, 3, 3, 0, 0)
HISTOGRAM = (585, 586, 224, 230, 9, 1)


def determinant_bareiss(rows):
    """Fraction-free exact determinant with pivoting."""
    n = len(rows)
    a = [list(row) for row in rows]
    sign, previous = 1, 1
    for k in range(n - 1):
        if a[k][k] == 0:
            j = next((j for j in range(k + 1, n) if a[j][k]), None)
            if j is None:
                return 0
            a[k], a[j] = a[j], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def main():
    assert len(set(POINTS)) == 11
    forbidden = []
    for ids in combinations(range(11), 4):
        rows = [(x, y, x*x + y*y, 1) for x, y in (POINTS[i] for i in ids)]
        if determinant_bareiss(rows) == 0:
            forbidden.append(ids)
    assert tuple(forbidden) == EXPECTED, forbidden

    edge_masks = [sum(1 << i for i in e) for e in forbidden]
    count = 1 << len(POINTS)
    safe = [all((mask & e) != e for e in edge_masks) for mask in range(count)]
    grundy = [0] * count
    histogram = [0] * 6
    for mask in range(count - 1, -1, -1):
        if not safe[mask]:
            continue
        seen = {
            grundy[mask | (1 << i)]
            for i in range(11)
            if not (mask & (1 << i)) and safe[mask | (1 << i)]
        }
        value = 0
        while value in seen:
            value += 1
        assert value < 6
        grundy[mask] = value
        histogram[value] += 1
    children = tuple(grundy[1 << i] for i in range(11))
    assert sum(safe) == 1635
    assert grundy[0] == 5
    assert children == CHILDREN
    assert tuple(histogram) == HISTOGRAM
    print(f"PASS: {len(forbidden)} forbidden, {sum(safe)} safe, "
          f"root={grundy[0]}, children={children}, histogram={histogram}")


if __name__ == "__main__":
    main()
