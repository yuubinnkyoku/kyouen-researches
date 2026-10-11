#!/usr/bin/env python3
"""Construct 128 rigorous lower-bound witnesses using Gaussian integer factorization.

Only the two explicitly selected norms are considered.  This is NOT a proof
that the resulting widths are globally optimal, nor an exhaustive norm search.
"""
import csv
from math import isqrt, prod
from pathlib import Path

FACTORS = [
    [(2, 1), (5, 2), (13, 2), (17, 1), (29, 1), (37, 1), (41, 1)],
    [(2, 1), (5, 2), (13, 1), (17, 1), (29, 1), (37, 1), (41, 1), (53, 1)],
]


def multiply(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def power(a, n):
    z = (1, 0)
    for _ in range(n):
        z = multiply(z, a)
    return z


def two_squares_prime(p):
    if p == 2:
        return (1, 1)
    for a in range(1, isqrt(p) + 1):
        b = isqrt(p - a * a)
        if a * a + b * b == p:
            return (a, b)
    raise AssertionError(f"not a sum of two squares: {p}")


def all_two_hit_v(factors):
    zlist = [(1, 0)]
    for p, exponent in factors:
        a, b = two_squares_prime(p)
        choices = [multiply(power((a, b), j), power((a, -b), exponent - j))
                   for j in range(exponent + 1)]
        zlist = [multiply(z, c) for z in zlist for c in choices]
    n = prod(p ** e for p, e in factors)
    values = set()
    for x, y in zlist:
        assert x * x + y * y == n
        for dx, v in ((x, y), (y, x)):
            if dx != 0:
                values.add(v)
                values.add(-v)
    return n, sorted(v for v in values if v % 2 == 1)


def best_window(vs, k):
    return min(((vs[i + k - 1] - vs[i]) // 2 + 1, vs[i], vs[i + k - 1])
               for i in range(len(vs) - k + 1))


def generate(path):
    families = [all_two_hit_v(factors) for factors in FACTORS]
    assert [(n, len(v)) for n, v in families] == [(6319594450, 288), (25764500450, 384)]
    records = []
    for k in range(257, 385):
        opts = [(best_window(vs, k), n) for n, vs in families if len(vs) >= k]
        (width, lo, hi), n = min(opts)
        b = 1
        c = lo
        assert (b * b + c * c - n) % 4 == 0
        d = (b * b + c * c - n) // 4
        records.append(dict(k=k, width=width, norm=n, B=b, C=c, D=d,
                            first_v=lo, last_v=hi))
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    for k in (257, 288, 289, 300, 320, 350, 384):
        print(records[k - 257])
    print(f'PASS {len(records)} constructions, norms={list(n for n, _ in families)}')


if __name__ == '__main__':
    generate(Path(__file__).resolve().parent.parent / 'output' / 'double_rows_257_384.csv')
