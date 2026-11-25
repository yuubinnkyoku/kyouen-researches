#!/usr/bin/env python3
"""Independent exhaustive audit of the split-graph root-only parity criterion.

The oracle uses named vertices and direct closed-neighborhood deletion; it does
not implement the two-move parity proof or any split-specific recursion.
"""
from functools import lru_cache
from random import Random


def direct_grundy(k: int, signatures: tuple[int, ...]) -> int:
    n = k + len(signatures)
    adjacency = [0] * n
    for i in range(k):
        for j in range(i + 1, k):
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    for a, mask in enumerate(signatures, start=k):
        adjacency[a] = mask
        for i in range(k):
            if mask & (1 << i):
                adjacency[i] |= 1 << a
    closed = [adjacency[i] | (1 << i) for i in range(n)]

    @lru_cache(None)
    def go(s: int) -> int:
        outcomes = set()
        rem = s
        while rem:
            bit = rem & -rem
            i = bit.bit_length() - 1
            rem ^= bit
            outcomes.add(go(s & ~closed[i]))
        g = 0
        while g in outcomes:
            g += 1
        return g

    return go((1 << n) - 1)


def prediction(k: int, signatures: tuple[int, ...]) -> int | None:
    if k == 0:
        return len(signatures) % 2
    deg = [sum(bool(mask & (1 << i)) for mask in signatures) for i in range(k)]
    parity = {d % 2 for d in deg}
    if len(parity) != 1:
        return None
    d = deg[0] % 2
    universal = (1 << k) - 1 in signatures
    if d == 0 and universal:
        return None
    return 1 ^ (len(signatures) % 2) ^ d


def check(k: int, signatures: tuple[int, ...]):
    expected = prediction(k, signatures)
    actual = direct_grundy(k, signatures)
    if (expected is None and actual < 2) or (expected is not None and actual != expected):
        raise AssertionError((k, signatures, expected, actual))
    return actual


def main():
    tested = 0
    hist = {}
    for k in range(1, 6):
        max_m = 4 if k <= 4 else 3
        for m in range(max_m + 1):
            for bits in range(1 << (k * m)):
                signatures = tuple((bits >> (k * j)) & ((1 << k) - 1) for j in range(m))
                g = check(k, signatures)
                hist[g] = hist.get(g, 0) + 1
                tested += 1
    rng = Random(20261030)
    for k in range(1, 9):
        for _ in range(600):
            m = rng.randrange(0, 13)
            signatures = tuple(rng.randrange(1 << k) for _ in range(m))
            g = check(k, signatures)
            hist[g] = hist.get(g, 0) + 1
            tested += 1
    assert check(1, (1, 1)) == 2
    assert check(2, (3, 3)) == 2
    assert check(3, (3, 5, 6)) == 0
    tested += 3
    print(f"PASS {tested} labeled graphs; root Grundy histogram {sorted(hist.items())}")


if __name__ == '__main__':
    main()
