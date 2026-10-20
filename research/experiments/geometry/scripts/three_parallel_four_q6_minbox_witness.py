#!/usr/bin/env python3
"""Exact circle equations and full q=6 Grundy table for the 7x4 witness."""
from collections import Counter
from fractions import Fraction
from itertools import combinations

ROWS = {0: (0, 3, 4, 5), 1: (0, 2, 5, 6), 3: (2, 3, 4, 6)}
POINTS = tuple((x, y) for y, xs in ROWS.items() for x in xs)


def circle(p, q, r):
    (x, y), (u, v), (w, z) = p, q, r
    det = (u - x) * (z - y) - (v - y) * (w - x)
    if not det:
        return None
    b1 = x*x+y*y-u*u-v*v
    b2 = x*x+y*y-w*w-z*z
    A = Fraction(b1 * (z - y) - b2 * (v - y), det)
    B = Fraction((u - x) * b2 - (w - x) * b1, det)
    C = -x*x-y*y-A*x-B*y
    return A, B, C


def main():
    circles = {}
    for i, j, k in combinations(range(12), 3):
        coeff = circle(POINTS[i], POINTS[j], POINTS[k])
        if coeff is None:
            continue
        A, B, C = coeff
        mask = sum(1 << t for t, (x, y) in enumerate(POINTS)
                   if x*x+y*y+A*x+B*y+C == 0)
        if mask.bit_count() >= 6:
            circles[coeff] = mask
    expected = {(-8, -4, 15), (-7, -3, 12), (-5, -1, 0)}
    assert set(circles) == expected
    assert all(mask.bit_count() == 6 for mask in circles.values())
    safe = [all(mask & f != f for f in circles.values()) for mask in range(1 << 12)]
    grundy = [-1] * (1 << 12)
    maximal = Counter()
    for mask in range((1 << 12) - 1, -1, -1):
        if not safe[mask]:
            continue
        children = [grundy[mask | (1 << i)] for i in range(12)
                    if not (mask >> i & 1) and safe[mask | (1 << i)]]
        if not children:
            maximal[mask.bit_count()] += 1
        mex = 0
        while mex in children:
            mex += 1
        grundy[mask] = mex
    print('circles:', sorted(circles))
    print('safe:', sum(safe))
    print('empty_grundy:', grundy[0])
    print('grundy_hist:', sorted(Counter(g for g in grundy if g >= 0).items()))
    print('maximal_hist:', sorted(maximal.items()))
    print('winning_first_moves:', sum(grundy[1 << i] == 0 for i in range(12)))
    assert sum(safe) == 3915 and grundy[0] == 0
    assert maximal == {9: 8, 10: 24}


if __name__ == '__main__':
    main()
