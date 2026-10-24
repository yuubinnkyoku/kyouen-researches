#!/usr/bin/env python3
"""Exact coplanarity and all-safe game audit for 2 x k x m small prisms.

Independent counterpart: independent.cpp, which uses 4x4 permutation determinants.
"""
from collections import Counter
from itertools import combinations
from math import gcd


def determinant3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def coplanar(p, q, r, s):
    return determinant3(tuple(q[i] - p[i] for i in range(3)),
                        tuple(r[i] - p[i] for i in range(3)),
                        tuple(s[i] - p[i] for i in range(3))) == 0


def collinear_triples_2d(k, m):
    return (sum((k - a) * m * (a - 1) for a in range(1, k))
            + sum(k * (m - b) * (b - 1) for b in range(1, m))
            + sum(2 * (k - a) * (m - b) * (gcd(a, b) - 1)
                  for a in range(1, k) for b in range(1, m)))


def audit(k, m):
    points = [(x, y, z) for x in range(2) for y in range(k) for z in range(m)]
    n = len(points)
    assert n <= 18, "Full subset enumeration is intended for n<=18"
    forbidden = [sum(1 << i for i in ids) for ids in combinations(range(n), 4)
                 if coplanar(*(points[i] for i in ids))]
    by_highest_bit = [[] for _ in range(n)]
    for b in forbidden:
        by_highest_bit[b.bit_length() - 1].append(b)
    safe = bytearray(1 << n)
    safe[0] = 1
    levels = [[] for _ in range(7)]
    levels[0].append(0)
    for s in range(1, 1 << n):
        highest = s.bit_length() - 1
        if safe[s ^ (1 << highest)] and all(s & b != b for b in by_highest_bit[highest]):
            safe[s] = 1
            size = s.bit_count()
            assert size <= 6
            levels[size].append(s)
    g = bytearray(1 << n)
    h = bytearray(1 << n)
    terminal = Counter()
    nimber_hist = []
    for size in range(6, -1, -1):
        hist = Counter()
        for s in levels[size]:
            children = [s | (1 << i) for i in range(n)
                        if not s >> i & 1 and safe[s | (1 << i)]]
            if not children:
                terminal[size] += 1
            used = {g[t] for t in children}
            value = 0
            while value in used:
                value += 1
            g[s] = value
            used = {h[t] for t in children}
            value = 1 if not children else 0
            while value in used:
                value += 1
            h[s] = value
            hist[g[s]] += 1
        nimber_hist.append((size, dict(sorted(hist.items()))))
    triple_maximal = terminal[3]
    if k >= 2 and m >= 2:
        assert triple_maximal == 2 * collinear_triples_2d(k, m)
    return dict(board=(2, k, m), forbidden=len(forbidden),
                safe_layers=[len(x) for x in levels], terminal=dict(sorted(terminal.items())),
                g0=g[0], h0=h[0],
                first_g=sorted(Counter(g[1 << i] for i in range(n)).items()),
                first_h=sorted(Counter(h[1 << i] for i in range(n)).items()),
                first_winning=[points[i] for i in range(n) if g[1 << i] == 0],
                swap_failures=sum(1 for s in range(1 << n) if safe[s] and
                                  h[s] != ((1 - g[s]) if g[s] in (0, 1) else g[s])),
                nimber_hist=sorted(nimber_hist))


def check_witness():
    witness = [(0, 0, 0), (0, 0, 1), (0, 1, 0),
               (1, 0, 1), (1, 1, 2), (1, 2, 0)]
    assert all(not coplanar(*quad) for quad in combinations(witness, 4))
    print("witness_2x3x3", witness, "all_15_quadruples_non_coplanar=True")


if __name__ == "__main__":
    check_witness()
    for k, m in [(2, 2), (2, 3), (3, 2), (3, 3)]:
        result = audit(k, m)
        for name in ("board", "forbidden", "safe_layers", "terminal", "g0", "h0",
                     "first_g", "first_h", "first_winning", "swap_failures"):
            print(name, result[name])
        print("nimber_hist", result["nimber_hist"])
        print()
