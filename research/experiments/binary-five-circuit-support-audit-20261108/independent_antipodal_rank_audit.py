#!/usr/bin/env python3
"""Independent rank-based audit of antipodal pairs in binary five-point circuits."""
from itertools import combinations
from collections import Counter

P = 1009  # Every 5x5 0/1 determinant has |det| <= 5! = 120.

def rank_mod(rows):
    a = [r[:] for r in rows]
    rank = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][j] % P), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][j], -1, P)
        for i in range(rank + 1, len(a)):
            z = a[i][j] * inv % P
            for k in range(j, len(a[0])):
                a[i][k] = (a[i][k] - z * a[rank][k]) % P
        rank += 1
        if rank == len(a):
            break
    return rank

def census(d):
    circuits = 0
    pair_counts = Counter()
    fixed_pair = 0
    for pts in combinations(range(1 << d), 5):
        rows = [[1] + [(x >> j) & 1 for j in range(d)] for x in pts]
        if rank_mod(rows) != 4:
            continue
        if any(rank_mod([rows[i] for i in range(5) if i != omit]) != 4
               for omit in range(5)):
            continue
        circuits += 1
        support = [j for j in range(d)
                   if len({(x >> j) & 1 for x in pts}) == 2]
        pairs = [(i, k) for i in range(5) for k in range(i + 1, 5)
                 if all((pts[i] ^ pts[k]) & (1 << j) for j in support)]
        pair_counts[len(pairs)] += 1
        if any(pts[i] == 0 and pts[k] == (1 << d) - 1 for i, k in pairs):
            fixed_pair += 1
    return circuits, pair_counts, fixed_pair

if __name__ == "__main__":
    for d, expected_total, expected_fixed in [(3, 8, 2), (4, 160, 12), (5, 2080, 50)]:
        total, pair_counts, fixed = census(d)
        assert (total, pair_counts, fixed) == (
            expected_total, Counter({1: expected_total}), expected_fixed)
        print(f"d={d}: circuits={total}, antipodal_counts={dict(pair_counts)}, fixed_pair={fixed}")
