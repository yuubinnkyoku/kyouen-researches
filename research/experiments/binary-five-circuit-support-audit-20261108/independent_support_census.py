#!/usr/bin/env python3
"""Independent exhaustive support-distribution audit for five-point binary affine circuits.

No matrix ranks or previously published counting formula are used.
"""
from collections import Counter
from itertools import combinations
from math import comb

def census(d):
    counts = Counter()
    for points in combinations(range(1 << d), 5):
        edges = set()
        support = 0
        for bit in range(d):
            ones = [i for i, x in enumerate(points) if (x >> bit) & 1]
            if len(ones) in (0, 5):
                continue
            support += 1
            minority = ones if len(ones) == 2 else [i for i in range(5) if i not in ones]
            if len(minority) != 2:
                break
            edges.add(tuple(minority))
        else:
            degrees = [sum(i in edge for edge in edges) for i in range(5)]
            if sorted(degrees) == [0, 1, 1, 1, 3]:
                counts[support] += 1
    return counts

def stirling_three(k):
    return (3 ** k - 3 * 2 ** k + 3) // 6

if __name__ == "__main__":
    for d in (3, 4, 5):
        actual = census(d)
        expected = {k: 2 ** d * comb(d, k) * stirling_three(k)
                    for k in range(3, d + 1)}
        assert dict(actual) == expected, (d, actual, expected)
        print(f"d={d}: {dict(sorted(actual.items()))}; total={sum(actual.values())}")
