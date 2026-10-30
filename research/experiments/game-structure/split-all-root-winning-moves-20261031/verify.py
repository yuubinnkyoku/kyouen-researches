#!/usr/bin/env python3
"""Independent exact mex audit of an all-opening theorem for split Node Kayles.

A center is indexed 0..k-1, independent vertices k..k+m-1.
"""
from functools import lru_cache
from itertools import product
from random import Random


def predict(k, signatures):
    m = len(signatures)
    allc = (1 << k) - 1
    degrees = [sum((s >> c) & 1 for s in signatures) for c in range(k)]
    odd = sum((degrees[c] & 1) << c for c in range(k))
    even = allc ^ odd
    center_wins = tuple(c for c in range(k) if (degrees[c] & 1) == (m & 1))
    independent_wins = []
    for i, s in enumerate(signatures):
        t = allc ^ s
        if m & 1:
            good = (t & even) == 0
        else:
            good = t != 0 and (t & odd) == 0 and not any(
                i != j and (s | other) == allc
                for j, other in enumerate(signatures)
            )
        if good:
            independent_wins.append(k + i)
    return center_wins + tuple(independent_wins)


def exact(k, signatures):
    m = len(signatures)
    n = k + m
    adj = [0] * n
    for c in range(k):
        adj[c] = ((1 << k) - 1) ^ (1 << c)
    for i, s in enumerate(signatures):
        adj[k+i] = s
        for c in range(k):
            if (s >> c) & 1:
                adj[c] |= 1 << (k+i)
    @lru_cache(None)
    def grundy(remaining):
        values = set()
        v = remaining
        while v:
            bit = v & -v
            p = bit.bit_length() - 1
            values.add(grundy(remaining & ~(adj[p] | bit)))
            v ^= bit
        mex = 0
        while mex in values:
            mex += 1
        return mex
    allv = (1 << n) - 1
    wins = []
    for p in range(n):
        if grundy(allv & ~(adj[p] | (1 << p))) == 0:
            wins.append(p)
    return tuple(wins), grundy(allv)


def run():
    cases = 0
    zero = 0
    max_g = 0
    for k, max_m in [(0, 7), (1, 5), (2, 5), (3, 4), (4, 4), (5, 3)]:
        for m in range(max_m+1):
            for signatures in product(range(1 << k), repeat=m):
                expected = predict(k, signatures)
                actual, g = exact(k, signatures)
                if expected != actual:
                    raise AssertionError((k, signatures, expected, actual, g))
                if (len(expected) == 0) != (g == 0):
                    raise AssertionError((k, signatures, expected, g))
                cases += 1
                zero += g == 0
                max_g = max(max_g, g)
    rng = Random(20261031)
    for _ in range(5000):
        k = rng.randrange(1, 10)
        m = rng.randrange(0, 15)
        signatures = tuple(rng.randrange(1 << k) for _ in range(m))
        expected = predict(k, signatures)
        actual, g = exact(k, signatures)
        if expected != actual:
            raise AssertionError((k, signatures, expected, actual, g))
        cases += 1
        zero += g == 0
        max_g = max(max_g, g)
    print(f'PASS: {cases} configurations, {zero} zero-Grundy roots, max root Grundy {max_g}; exact winning move sets agree')
    print('Witness A (k=3, signatures=(3,5,6,0)):', predict(3, (3,5,6,0)), exact(3, (3,5,6,0)))
    print('Witness B (k=2, signatures=(3,3)):', predict(2, (3,3)), exact(2, (3,3)))


if __name__ == '__main__':
    run()
