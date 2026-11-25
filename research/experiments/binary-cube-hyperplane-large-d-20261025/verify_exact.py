"""Exact integer verification of general-position witnesses in the binary cube.

Input records (witnesses.txt, produced by search.cpp):

    d m
    v0 v1 ... v_{m-1}

For every record two independent exact arguments are checked:

  A. all C(m, d+1) subsets of d+1 vertices have nonzero augmented determinant
     (fraction-free Bareiss elimination on Python integers), and
  B. the left null space of the m x (d+1) augmented matrix has dimension
     m - (d+1) and every t x t column minor of an integer null basis is
     nonzero, t = m - (d+1); by matroid duality this is equivalent to A.

Exit status is nonzero if any check fails.
"""
import sys
from fractions import Fraction
from itertools import combinations
from math import comb, lcm


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


def augmented(points, d):
    return [[1] + [(x >> i) & 1 for i in range(d)] for x in points]


def left_null_basis(rows):
    """Exact rational basis of {z : z @ rows = 0} (left null space).

    Row-reduces [A | I]; rows beyond the rank vanish on the A block and their
    identity parts are independent left null vectors.
    """
    m = len(rows)
    n = len(rows[0])
    a = [[Fraction(rows[r][c]) for c in range(n)]
         + [Fraction(1) if i == r else Fraction(0) for i in range(m)]
         for r in range(m)]
    rank = 0
    for col in range(n):
        piv = next((r for r in range(rank, m) if a[r][col] != 0), None)
        if piv is None:
            continue
        a[rank], a[piv] = a[piv], a[rank]
        inv = 1 / a[rank][col]
        a[rank] = [x * inv for x in a[rank]]
        for r in range(m):
            if r != rank and a[r][col] != 0:
                f = a[r][col]
                a[r] = [x - f * y for x, y in zip(a[r], a[rank])]
        rank += 1
    basis = [a[r][n:] for r in range(rank, m)]
    return basis, rank


def integer_scale(vec):
    """Scales a rational vector by the lcm of its denominators."""
    denominators = [f.denominator for f in vec if f != 0]
    if not denominators:
        return [0] * len(vec)
    scale = 1
    for dd in denominators:
        scale = lcm(scale, dd)
    return [int(f * scale) for f in vec]


def verify_record(d, m, points):
    assert len(points) == m, (d, m, len(points))
    assert len(set(points)) == m
    assert all(0 <= x < (1 << d) for x in points)
    dets = [
        determinant(augmented(subset, d))
        for subset in combinations(points, d + 1)
    ]
    zeros = sum(1 for v in dets if v == 0)
    assert zeros == 0, (d, m, "zero minors", zeros)
    assert len(dets) == comb(m, d + 1)
    rows = augmented(points, d)
    basis, rank = left_null_basis(rows)
    t = m - (d + 1)
    assert rank == d + 1, (d, m, "rank", rank)
    assert len(basis) == t, (d, m, "nullity", len(basis))
    nb = [integer_scale(v) for v in basis]
    dual_minors = 0
    for cols in combinations(range(m), t):
        sub = [[nb[r][c] for c in cols] for r in range(t)]
        assert determinant(sub) != 0, (d, m, "zero dual minor", cols)
        dual_minors += 1
    assert dual_minors == len(dets)
    return {
        "d": d,
        "m": m,
        "minors": len(dets),
        "min_abs": min(abs(v) for v in dets),
        "max_abs": max(abs(v) for v in dets),
        "dual_minors": dual_minors,
    }


def read_records(path):
    records = []
    with open(path) as fh:
        tokens = fh.read().split()
    i = 0
    while i < len(tokens):
        d, m = int(tokens[i]), int(tokens[i + 1])
        i += 2
        points = [int(x) for x in tokens[i:i + m]]
        i += m
        records.append((d, m, points))
    return records


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "witnesses.txt"
    records = read_records(path)
    if not records:
        print("no records")
        return 1
    for d, m, points in records:
        info = verify_record(d, m, points)
        print(
            f"d={d} m={m} minors={info['minors']} "
            f"min_abs={info['min_abs']} max_abs={info['max_abs']} "
            f"dual_minors={info['dual_minors']} OK"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
