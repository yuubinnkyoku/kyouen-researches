#!/usr/bin/env python3
"""Exact, independent integer-square audit of 49..96 two-hit-row witnesses.

For each of four specified circles, compute the shortest window containing
k distinct two-hit rows. No floating-point arithmetic or search cutoff.
"""
from math import isqrt

DATA = (
    (1602250, 49, [1086, 1126, 1140, 1153, 1167, 1181, 1185, 1216,
                   1226, 1241, 1244, 1248, 1257, 1258, 1262, 1266]),
    (4165850, 65, [1972, 2003, 2009, 2014, 2029, 2034, 2038, 2042]),
    (8011250, 73, [2762, 2795, 2797, 2807, 2815, 2822, 2827, 2828]),
    (11856650, 81, [3235, 3253, 3288, 3297, 3321, 3343, 3349, 3382,
                    3385, 3400, 3420, 3426, 3435, 3440, 3442, 3444]),
)


def two_hit_ordinates(n):
    assert n % 4 == 2
    r = isqrt(n)
    found = []
    for Y in range(-r, r + 1):
        if Y % 2 == 0:
            continue
        sq = n - Y * Y
        if sq <= 0:
            continue
        X = isqrt(sq)
        if X > 0 and X * X == sq and X % 2 == 1:
            found.append((Y, X))
    return found


def verify():
    total = 0
    for n, k0, expected in DATA:
        rows = two_hit_ordinates(n)
        assert len(rows) == k0 + len(expected) - 1, (n, len(rows))
        ordinates = [y for y, _ in rows]
        for i, want in enumerate(expected):
            k = k0 + i
            windows = [(ordinates[j+k-1] - ordinates[j]) // 2 + 1
                       for j in range(len(rows) - k + 1)]
            w = min(windows)
            assert w == want, (n, k, w, want)
            j = windows.index(w)
            lo = ordinates[j]
            C = -lo
            D, rem = divmod(1 + C*C - n, 4)
            assert rem == 0
            for Y, X in rows[j:j+k]:
                y = (Y-lo)//2
                for signed_x in (-X, X):
                    x = (signed_x-1)//2
                    assert x*x + y*y + x - C*y + D == 0
                    assert 0 <= y < w
            total += 1
            print(f'k={k} w={w} N={n} Y=[{lo},{ordinates[j+k-1]}]')
    assert total == 48
    print('PASS 48 certified construction bounds')


if __name__ == '__main__':
    verify()
