#!/usr/bin/env python3
"""Exact maximal-safe polynomial for one fully exchangeable class.

No repository dependencies; Python >=3.10. The two routines share only input data.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations
from math import comb
from random import Random


def orbit_types(k: int, h: int):
    return [(s, a) for s in range(k + 1) for a in range(1 << h)
            if s != 0 or a != 0]


def expanded_edges(k: int, h: int, orbits):
    out = []
    for s, a in orbits:
        for xs in combinations(range(k), s):
            mask = sum(1 << x for x in xs) | (a << k)
            out.append(mask)
    return tuple(out)


def direct_polynomial(k: int, h: int, edges):
    n = k + h
    def safe(mask):
        return all(mask & edge != edge for edge in edges)
    return Counter(mask.bit_count() for mask in range(1 << n)
                   if safe(mask) and all(not safe(mask | (1 << i))
                                         for i in range(n) if not mask >> i & 1))


def orbit_polynomial(k: int, h: int, orbits):
    # This algorithm never constructs any concrete edge containing X.
    capacity = [k] * (1 << h)
    for t in range(1 << h):
        for s, a in orbits:
            if a & t == a:
                capacity[t] = min(capacity[t], s - 1)
    result = Counter()
    for t, c in enumerate(capacity):
        if c < 0:
            continue
        if all(capacity[t | (1 << y)] < c
               for y in range(h) if not t >> y & 1):
            result[t.bit_count() + c] += comb(k, c)
    return result


def run():
    total = 0
    for k, h in [(3, 2), (2, 2)]:
        types = orbit_types(k, h)
        assert len(types) == (k + 1) * (1 << h) - 1
        for mask in range(1 << len(types)):
            orbits = [types[i] for i in range(len(types)) if mask >> i & 1]
            expected = direct_polynomial(k, h, expanded_edges(k, h, orbits))
            actual = orbit_polynomial(k, h, orbits)
            assert expected == actual, (k, h, mask, expected, actual)
            total += 1
        print(f'exhaustive: k={k}, h={h}, orbit-families={1 << len(types)}')
    rng = Random(20261020)
    for k, h, cases in [(4, 3, 1200), (5, 3, 1000), (6, 2, 1000)]:
        types = orbit_types(k, h)
        for _ in range(cases):
            p = rng.uniform(.05, .95)
            orbits = [item for item in types if rng.random() < p]
            expected = direct_polynomial(k, h, expanded_edges(k, h, orbits))
            actual = orbit_polynomial(k, h, orbits)
            assert expected == actual, (k, h, orbits, expected, actual)
            total += 1
        print(f'random: k={k}, h={h}, cases={cases}')
    # Witness: full exchangeability and nontrivial binomial coefficient.
    k, h, orbits = 4, 1, [(3, 0), (1, 1)]
    got = orbit_polynomial(k, h, orbits)
    assert got == Counter({1: 1, 2: 6}), got
    assert got == direct_polynomial(k, h, expanded_edges(k, h, orbits))
    print(f'witness k=4,h=1,orbits={orbits},polynomial={dict(sorted(got.items()))}')
    print(f'PASS total={total} independent brute-force comparisons')


if __name__ == '__main__':
    run()
