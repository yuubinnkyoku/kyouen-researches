#!/usr/bin/env python3
"""Independent bounded-weight audit of >1/4 hyperplane sections.

Enumerates nondecreasing positive integer coefficient multisets, then
computes all subset-sum multiplicities by exact integer dynamic programming.
The unbounded theorem is proved separately; this is only a finite audit.
"""
from collections import Counter
from itertools import combinations_with_replacement
from math import comb


def histogram(weights):
    counts = {0: 1}
    for w in weights:
        nxt = counts.copy()
        for s, multiplicity in counts.items():
            nxt[s + w] = nxt.get(s + w, 0) + multiplicity
        counts = nxt
    return counts


def verify(max_weight=10, max_support=8):
    examined = 0
    hit_counts = Counter()
    for k in range(1, max_support + 1):
        for weights in combinations_with_replacement(range(1, max_weight + 1), k):
            examined += 1
            distribution = histogram(weights)
            hits = [(r, n) for r, n in distribution.items() if 4 * n > (1 << k)]
            if len(set(weights)) > 1:
                assert not hits, (weights, hits)
            else:
                expected = {
                    r * weights[0]: comb(k, r)
                    for r in range(k + 1)
                    if 4 * comb(k, r) > (1 << k)
                }
                assert dict(hits) == expected, (weights, hits, expected)
                hit_counts[k] += 1
    print(
        f"PASS: {examined} nondecreasing weight vectors; "
        f"max_weight={max_weight}; max_support={max_support}"
    )
    print(
        "uniform weight vectors with >quarter sections by support:",
        dict(sorted(hit_counts.items())),
    )
    for d in (7, 8, 9, 10):
        expected = 128 * comb(d + 1, 8)
        assert expected == 128 * (comb(d, 7) + comb(d, 8))
        print(f"d={d}: exact-35/128 hyperplane formula {expected}")


if __name__ == "__main__":
    verify()
