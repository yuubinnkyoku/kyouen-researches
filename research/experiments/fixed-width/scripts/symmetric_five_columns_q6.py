#!/usr/bin/env python3
"""Exact two-pair-sum enumeration and 15-point Grundy DP for 3x5 q=6.
The mathematical classification for arbitrary real u>v>0 is in the report.
"""
from collections import defaultdict, Counter
from itertools import combinations


def edges_by_pairsum(u, v, a, b):
    xs = (-u, -v, 0, v, u)
    ys = (0, a, a + b)
    sums = defaultdict(list)
    for i, j in combinations(range(5), 2):
        sums[xs[i] + xs[j]].append((i, j, xs[i] * xs[j]))
    edges = set()
    for pairs in sums.values():
        for low, mid, high in __import__('itertools').product(pairs, repeat=3):
            p0, p1, p2 = low[2], mid[2], high[2]
            if b * (p0 - p1) + a * (p2 - p1) != a * b * (a + b):
                continue
            edge = 0
            for row, pair in enumerate((low, mid, high)):
                edge |= (1 << (5 * row + pair[0])) | (1 << (5 * row + pair[1]))
            edges.add(edge)
    return sorted(edges), sums


def solve(edges):
    n = 15
    limit = 1 << n
    safe = bytearray([1]) * limit
    for mask in range(limit):
        if any(mask & e == e for e in edges):
            safe[mask] = 0
    g = bytearray(limit)
    maximal = Counter()
    distribution = Counter()
    for mask in range(limit - 1, -1, -1):
        if not safe[mask]:
            continue
        values = set()
        for i in range(n):
            if mask >> i & 1 == 0 and safe[mask | (1 << i)]:
                values.add(g[mask | (1 << i)])
        if not values:
            maximal[mask.bit_count()] += 1
        nim = 0
        while nim in values:
            nim += 1
        g[mask] = nim
        distribution[nim] += 1
    return {
        'circles': len(edges), 'safe': sum(safe), 'root': g[0],
        'max_g': max(distribution), 'maximal': dict(sorted(maximal.items())),
        'g_counts': dict(sorted(distribution.items())),
        'pairwise_intersections': sorted((x & y).bit_count() for x, y in combinations(edges, 2)),
    }


def main():
    # Three genuinely non-arithmetic column sets, plus the exceptional progression.
    cases = (
        ('generic_off', 3, 1, 1, 1, 0, 32768, 1),
        ('generic_one', 3, 1, 1, 7, 1, 32256, 0),
        ('generic_two', 3, 1, 2, 2, 2, 31776, 1),
        ('exceptional_four', 2, 1, 1, 1, 4, 30866, 1),
        ('generic_ratio_3_2', 3, 2, 1, 4, 1, 32256, 0),
    )
    for name, u, v, a, b, expected_edges, expected_safe, expected_root in cases:
        edges, sums = edges_by_pairsum(u, v, a, b)
        out = solve(edges)
        assert (out['circles'], out['safe'], out['root']) == (expected_edges, expected_safe, expected_root), (name, out)
        print(name, 'u,v,a,b=', (u, v, a, b), out)
        print('  repeated sums=', {s: [(i, j) for i, j, _ in p] for s, p in sums.items() if len(p) > 1})
        print('  edges=', [[(i % 5, i // 5) for i in range(15) if e >> i & 1] for e in edges])


if __name__ == '__main__':
    main()
