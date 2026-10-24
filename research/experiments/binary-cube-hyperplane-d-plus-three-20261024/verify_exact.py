"""Exact integer certificates for binary-hypercube hyperplane avoidance.

Each listed d+3 vertex set is checked on all C(d+3,2) subsets of d+1
vertices.  A nonzero augmented determinant means affine independence.
"""
from collections import Counter
from itertools import combinations

WITNESSES = {
    6: [0, 54, 40, 39, 21, 2, 62, 59, 14],
    7: [0, 56, 109, 70, 72, 117, 87, 97, 35, 13],
    8: [0, 118, 145, 79, 161, 210, 125, 237, 195, 166, 42],
    9: [0, 479, 220, 421, 240, 205, 445, 167, 150, 458, 359, 1],
    10: [0, 398, 511, 619, 457, 220, 766, 879, 868, 966, 886, 1000, 917],
}


def determinant(rows):
    """Exact fraction-free Bareiss elimination, with row swaps."""
    a = [row[:] for row in rows]
    n = len(a)
    prev, sign = 1, 1
    for k in range(n - 1):
        pivot_row = next((i for i in range(k, n) if a[i][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                assert numerator % prev == 0
                a[i][j] = numerator // prev
            a[i][k] = 0
        prev = pivot
    return sign * a[-1][-1]


def verify():
    for d, points in WITNESSES.items():
        assert len(points) == d + 3
        assert len(set(points)) == len(points)
        assert all(0 <= x < (1 << d) for x in points)
        determinants = []
        for subset in combinations(points, d + 1):
            matrix = [[1] + [(x >> i) & 1 for i in range(d)] for x in subset]
            determinants.append(determinant(matrix))
        counts = Counter(abs(v) for v in determinants)
        assert 0 not in counts, (d, counts)
        assert len(determinants) == (d + 3) * (d + 2) // 2
        print(
            f"d={d} points={len(points)} minors={len(determinants)} "
            f"min_abs={min(counts)} max_abs={max(counts)}"
        )


if __name__ == "__main__":
    verify()
