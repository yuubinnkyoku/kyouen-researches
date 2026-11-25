#!/usr/bin/env python3
"""All 8*3**7 vertex-cover-three signatures, using parity-compressed transitions.

K0336 proves that positive equal-link independent classes may be reduced
to one (odd) or two (even) vertices without changing the Grundy value.
"""
from functools import lru_cache
from itertools import product
from collections import Counter

# Cover-edge bits: 0--1, 0--2, 1--2.
PAIRS = ((0, 1), (0, 2), (1, 2))


def normalize(mask, edges, counts):
    """Project neighbor signatures to surviving cover; return counts and free parity.

    counts[s-1] is 0, 1 or 2 for nonempty signature s.
    """
    d = [0] * 7
    f = 0
    for s, c in enumerate(counts, 1):
        if not c:
            continue
        t = s & mask
        if not t:
            f ^= c & 1
        else:
            prev = d[t - 1]
            d[t - 1] = 1 if (prev + c) & 1 else 2
    return tuple(d), f


@lru_cache(None)
def sg(mask, edges, counts):
    assert all(c == 0 or ((i + 1) & mask) == i + 1
               for i, c in enumerate(counts))
    options = set()

    # Choose one of the remaining cover vertices.
    for v in range(3):
        if not (mask >> v) & 1:
            continue
        remaining = mask & ~(1 << v)
        for e, (a, b) in enumerate(PAIRS):
            if (edges >> e) & 1:
                if a == v:
                    remaining &= ~(1 << b)
                if b == v:
                    remaining &= ~(1 << a)
        # Neighbors of v outside the cover are removed; others survive.
        raw = tuple(0 if s & (1 << v) else counts[s - 1]
                    for s in range(1, 8))
        nxt, free = normalize(remaining, edges, raw)
        options.add(sg(remaining, edges, nxt) ^ free)

    # Choose a vertex in one of the nonempty neighbor-signature classes.
    for s, c in enumerate(counts, 1):
        if not c:
            continue
        remaining = mask & ~s
        raw = list(counts)
        raw[s - 1] -= 1
        nxt, free = normalize(remaining, edges, raw)
        options.add(sg(remaining, edges, nxt) ^ free)

    g = 0
    while g in options:
        g += 1
    return g


def main():
    distribution = Counter()
    witnesses = {}
    by_cover_edges = {}
    for edges in range(8):
        counts_by_value = Counter()
        for counts in product(range(3), repeat=7):
            g = sg(7, edges, counts)
            counts_by_value[g] += 1
            distribution[g] += 1
            witnesses.setdefault(g, (edges, counts))
        by_cover_edges[edges] = dict(sorted(counts_by_value.items()))
    assert dict(sorted(distribution.items())) == {
        0: 3735, 1: 3264, 2: 3695, 3: 4603, 4: 2199
    }
    assert witnesses[4] == (0, (0, 0, 0, 0, 1, 2, 1))
    assert max(g ^ 1 for g in distribution) == 5  # One isolated vertex.
    print("distribution", dict(sorted(distribution.items())))
    print("general maximum with isolated vertices", max(g ^ 1 for g in distribution))
    print("maximum", max(distribution), "witness", witnesses[4])
    print("by cover-edge mask", by_cover_edges)
    print("memo", sg.cache_info())


if __name__ == "__main__":
    main()
