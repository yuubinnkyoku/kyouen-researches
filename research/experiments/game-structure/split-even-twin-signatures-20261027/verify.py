#!/usr/bin/env python3
"""Independent adjacency-bitset Node Kayles audit for even signature classes."""
from functools import lru_cache
from itertools import product
import random


def direct_grundy(k, multiplicities, free=0):
    """Construct named vertices, then use closed-neighborhood deletion."""
    sigs = [s for s, count in multiplicities.items() for _ in range(count)]
    n = k + len(sigs) + free
    adj = [0] * n
    for i in range(k):
        for j in range(i + 1, k):
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    for j, sig in enumerate(sigs, k):
        adj[j] = sig
        for i in range(k):
            if sig & (1 << i):
                adj[i] |= 1 << j

    @lru_cache(None)
    def solve(mask):
        if mask == 0:
            return 0
        isolated = 0
        active = mask
        rest = mask
        while rest:
            bit = rest & -rest
            rest ^= bit
            i = bit.bit_length() - 1
            if not (adj[i] & mask):
                isolated ^= 1
                active ^= bit
        if active != mask:
            return solve(active) ^ isolated
        seen = set()
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            i = bit.bit_length() - 1
            seen.add(solve(mask & ~(adj[i] | bit)))
        ans = 0
        while ans in seen:
            ans += 1
        return ans

    return solve((1 << n) - 1)


def formula(k, multiplicities, free=0):
    if k == 0:
        return free & 1
    full = (1 << k) - 1
    return (2 if multiplicities.get(full, 0) else 1) ^ (free & 1)


def audit(k, allowed, count_vectors, label):
    checks = 0
    for counts in count_vectors:
        mult = {s: 2 * c for s, c in zip(allowed, counts) if c}
        for free in (0, 1):
            expected = formula(k, mult, free)
            actual = direct_grundy(k, mult, free)
            assert actual == expected, (label, k, mult, free, actual, expected)
            checks += 1
    print(f"{label}: k={k} configurations={checks//2} checks={checks} all_match")


def main():
    for k in range(1, 4):
        types = list(range(1, 1 << k))
        audit(k, types, product((0, 1), repeat=len(types)), "all-signatures exhaustive")
    k = 4
    types = [s for s in range(1, 1 << k) if s.bit_count() <= 2]
    audit(k, types, product((0, 1), repeat=len(types)), "degree-two exhaustive")
    rng = random.Random(20261027)
    for k, ncases in [(4, 120), (5, 80), (6, 30)]:
        types = list(range(1, 1 << k))
        cases = []
        for _ in range(ncases):
            chosen = rng.sample(types, rng.randrange(0, min(5, len(types)) + 1))
            cases.append(tuple(1 if s in chosen else 0 for s in types))
        audit(k, types, cases, "unrestricted random")
    # Boundary: an odd signature can violate the formula.
    assert direct_grundy(1, {1: 1}) == 1
    assert direct_grundy(1, {1: 2}) == 2
    print("boundary: one leaf g=1, two identical leaves g=2")


if __name__ == "__main__":
    main()
