#!/usr/bin/env python3
"""Exhaustive signature-count mex verifier for four incomparable forbidden edges.

Run: python verify_venn.py
No external packages required. The rank bound is 2, 3, or 4.
"""
from collections import Counter
from functools import lru_cache
import json

EXPECTED = {
    2: (70, (15, 12, 19, 24), 3, 5),
    3: (2760, (953, 923, 434, 438, 12), 4, 8),
    4: (37592, (13508, 13427, 5111, 5270, 240, 36), 5, 9),
}
MASKS = range(1, 16)

@lru_cache(maxsize=None)
def grundy(counts):
    sizes = [sum(counts[p-1] for p in MASKS if p & (1 << i)) for i in range(4)]
    children = set()
    for p in MASKS:
        if counts[p-1] and all(sizes[i] > 1 for i in range(4) if p & (1 << i)):
            nxt = list(counts)
            nxt[p-1] -= 1
            children.add(grundy(tuple(nxt)))
    value = 0
    while value in children:
        value += 1
    return value

def enumerate_rank(rank):
    histogram = Counter()
    min_witness = None
    total = 0
    counts = []
    remaining = [rank] * 4

    def recurse(p):
        nonlocal total, min_witness
        if p == 16:
            if any(rank - r < 2 for r in remaining):
                return
            for i in range(4):
                for j in range(4):
                    if i != j and not any(
                        counts[q-1] and (q & (1 << i)) and not (q & (1 << j))
                        for q in MASKS
                    ):
                        return
            g = grundy(tuple(counts))
            histogram[g] += 1
            total += 1
            n = sum(counts)
            if min_witness is None or g > min_witness[0] or (g == min_witness[0] and n < min_witness[1]):
                min_witness = (g, n, counts.copy())
            return
        cap = min(remaining[i] for i in range(4) if p & (1 << i))
        for value in range(cap + 1):
            counts.append(value)
            for i in range(4):
                if p & (1 << i):
                    remaining[i] -= value
            recurse(p + 1)
            for i in range(4):
                if p & (1 << i):
                    remaining[i] += value
            counts.pop()

    recurse(1)
    expected_n, expected_hist, expected_max, expected_min_n = EXPECTED[rank]
    assert total == expected_n
    assert tuple(histogram[g] for g in range(len(expected_hist))) == expected_hist
    assert sum(histogram.values()) == total
    assert min_witness[0:2] == (expected_max, expected_min_n)
    return {
        'rank': rank, 'labeled_signature_cases': total,
        'grundy_histogram': {str(k): histogram[k] for k in sorted(histogram)},
        'max_grundy': expected_max, 'minimum_core_vertices_for_max': expected_min_n,
        'first_minimum_witness_signature_counts': min_witness[2],
    }

if __name__ == '__main__':
    print(json.dumps([enumerate_rank(r) for r in (2, 3, 4)], ensure_ascii=False, indent=2))
