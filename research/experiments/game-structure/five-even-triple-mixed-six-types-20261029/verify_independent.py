#!/usr/bin/env python3
"""Independent named-vertex Node Kayles verification of 226 fixed samples.

Unlike verify.cpp, this deletes closed neighborhoods in the actual graph,
with no center-mask recurrence, signature projection, or parity shortcut.
"""
from functools import lru_cache
from itertools import combinations, product
from random import Random

K = 5
TARGET = 0b00111
TYPES = [s for s in range(1, 1 << K) if s.bit_count() >= 2 and s != TARGET]


def direct(counts):
    signatures = []
    for s, multiplicity in sorted(counts.items()):
        signatures.extend([s] * multiplicity)
    n = K + len(signatures)
    neighbors = [0] * n
    for i in range(K):
        for j in range(K):
            if i != j:
                neighbors[i] |= 1 << j
    for j, s in enumerate(signatures):
        v = K + j
        for i in range(K):
            if s & (1 << i):
                neighbors[i] |= 1 << v
                neighbors[v] |= 1 << i

    @lru_cache(None)
    def grundy(mask):
        children = set()
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            remaining -= bit
            v = bit.bit_length() - 1
            children.add(grundy(mask & ~(neighbors[v] | bit)))
        g = 0
        while g in children:
            g += 1
        return g

    return grundy((1 << n) - 1)


def check(items):
    counts = {1 << i: 1 for i in range(K)}
    counts.update(items)
    before = direct(counts)
    counts[TARGET] = 2
    after = direct(counts)
    assert before == after, (items, before, after)


def main():
    tests = 0
    for t in range(2):
        for chosen in combinations(TYPES, t):
            for multiplicities in product((1, 2), repeat=t):
                check(dict(zip(chosen, multiplicities)))
                tests += 1
    rng = Random(20261029)
    for t in (2, 3, 4, 5, 6):
        for _ in range(35):
            chosen = rng.sample(TYPES, t)
            check({s: rng.choice((1, 2)) for s in chosen})
            tests += 1
    assert tests == 226
    print(f"PASS independent_named_cases={tests} (before/after each)")


if __name__ == "__main__":
    main()
