#!/usr/bin/env python3
"""Exact independent checks for the nested-neighborhood probability maximum.

No third-party dependencies. Run: python3 verify.py
"""
from fractions import Fraction
from itertools import permutations
from math import factorial


def predicted(degrees):
    if not degrees:
        return Fraction(1)
    if 0 in degrees:
        return Fraction(0)
    result = Fraction(1)
    for i, d in enumerate(sorted(degrees), 1):
        result *= Fraction(d + i - 1, d + i)
    return result


def subset_dp(neighborhoods, m):
    """Independent inclusion-exclusion formula using union cardinalities."""
    k = len(neighborhoods)
    h = [Fraction(0)] * (1 << k)
    h[0] = Fraction(1)
    unions = [0] * (1 << k)
    for s in range(1, 1 << k):
        bit = s & -s
        i = bit.bit_length() - 1
        unions[s] = unions[s ^ bit] | neighborhoods[i]
        denom = s.bit_count() + unions[s].bit_count()
        h[s] = sum((h[s ^ (1 << i)] for i in range(k) if s & (1 << i)), Fraction(0)) / denom
    return sum(((-1 if s.bit_count() & 1 else 1) * h[s] for s in range(1 << k)), Fraction(0))


def direct_markov(neighborhoods, m):
    """Direct recursion over named vertices and closed-neighborhood deletion."""
    k = len(neighborhoods)
    n = k + m
    adj = [0] * n
    for i in range(k):
        for j in range(k):
            if i != j:
                adj[i] |= 1 << j
        for j in range(m):
            if neighborhoods[i] & (1 << j):
                adj[i] |= 1 << (k + j)
                adj[k + j] |= 1 << i
    memo = {}

    def rec(mask):
        if not mask:
            return Fraction(1)
        if mask in memo:
            return memo[mask]
        result = Fraction(0)
        for v in range(k, n):
            if mask & (1 << v):
                result += rec(mask & ~(adj[v] | (1 << v)))
        result /= mask.bit_count()
        memo[mask] = result
        return result

    return rec((1 << n) - 1)


def columns_are_chain(neighborhoods, m):
    columns = [sum(1 << i for i, row in enumerate(neighborhoods) if row & (1 << j)) for j in range(m)]
    return all((a & b) in (a, b) for a in columns for b in columns)


def run():
    checked = direct_checked = strict_checked = 0
    groups = {}
    for k, m in [(1, 5), (2, 5), (3, 4), (4, 3), (4, 4)]:
        group_max = {}
        for code in range(1 << (k * m)):
            rows = [(code >> (i * m)) & ((1 << m) - 1) for i in range(k)]
            ds = tuple(sorted(row.bit_count() for row in rows))
            actual = subset_dp(rows, m)
            bound = predicted(ds)
            assert actual <= bound, (k, m, rows, actual, bound)
            if 0 not in ds:
                chain = columns_are_chain(rows, m)
                assert (actual == bound) == chain, (k, m, rows, actual, bound, chain)
                strict_checked += 1
            group_max[ds] = max(actual, group_max.get(ds, Fraction(-1)))
            if code % max(1, (1 << (k * m)) // 160) == 0:
                independent = direct_markov(rows, m)
                assert independent == actual, (k, m, rows, actual, independent)
                direct_checked += 1
            checked += 1
        for ds, mx in group_max.items():
            assert mx == predicted(ds), (k, m, ds, mx, predicted(ds))
        groups[(k, m)] = len(group_max)
        print(f'k={k} m={m} configurations={1 << (k*m)} degree_classes={len(group_max)} verified')
    perm_checks = 0
    for ds in [(1, 2), (1, 2, 3), (2, 2, 3), (1, 3, 3), (2, 3, 4)]:
        m = max(ds)
        n = m + len(ds)
        wins = 0
        for order in permutations(range(n)):
            pos = [0] * n
            for idx, v in enumerate(order):
                pos[v] = idx
            if all(min(pos[:d]) < pos[m+i] for i, d in enumerate(ds)):
                wins += 1
        assert Fraction(wins, factorial(n)) == predicted(ds)
        perm_checks += 1
    print(f'PASS configurations={checked} strict_positive_degree={strict_checked} '
          f'named_vertex_checks={direct_checked} permutation_checks={perm_checks} '
          f'degree_classes={sum(groups.values())}')
    for ds in [(1, 2, 3), (2, 3, 4), (2, 2, 2)]:
        print(f'degrees={ds} sharp_upper={predicted(ds)}')


if __name__ == '__main__':
    run()
