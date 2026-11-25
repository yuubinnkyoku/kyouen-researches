#!/usr/bin/env python3
"""Independent named-vertex closed-neighborhood mex on deterministic samples.

No clique-mask quotient, parity-bit recurrence, or orbit canonicalization.
This is a sample audit, NOT a second exhaustive proof.
"""
from functools import lru_cache
from random import Random

K = 5
TARGET = 7
TYPES = [s for s in range(1, 1 << K) if s.bit_count() >= 2 and s != TARGET]


def direct(counts):
    supports = [s for s in sorted(counts) for _ in range(counts[s])]
    n = K + len(supports)
    neighbors = [0] * n
    for c in range(K):
        neighbors[c] = ((1 << K) - 1) ^ (1 << c)
    for j, s in enumerate(supports):
        v = K + j
        for c in range(K):
            if s & (1 << c):
                neighbors[c] |= 1 << v
                neighbors[v] |= 1 << c

    @lru_cache(None)
    def grundy(mask):
        options = set()
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            remaining -= bit
            v = bit.bit_length() - 1
            options.add(grundy(mask & ~(neighbors[v] | bit)))
        g = 0
        while g in options:
            g += 1
        return g

    return grundy((1 << n) - 1)


def check(items):
    counts = {1 << c: 1 for c in range(K)}
    counts.update(items)
    g0 = direct(counts)
    counts[TARGET] = 2
    g2 = direct(counts)
    assert g0 == g2, (items, g0, g2)


def main():
    rng = Random(20261029)
    total = 0
    for k in (0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12):
        sample = 1 if k == 0 else (12 if k <= 4 else 20 if k <= 8 else 3 if k == 10 else 2)
        for t in range(sample):
            chosen = rng.sample(TYPES, k)
            doubled = set(rng.sample(chosen, min(k, t % 3 if k <= 8 else 0)))
            counts = {s: (2 if s in doubled else 1) for s in chosen}
            check(counts)
            total += 1
        print(f"independent k={k} checked={sample}", flush=True)
    assert total == 134
    print(f"PASS independent_named_cases={total} (before/after each)")


if __name__ == "__main__":
    main()
