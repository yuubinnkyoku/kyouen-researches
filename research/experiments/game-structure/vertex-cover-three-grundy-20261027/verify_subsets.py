#!/usr/bin/env python3
"""Independent bitset Node Kayles on each of the 17,496 actual graphs.

No signature projection is used in the game recursion. Additionally
checks 256 larger multiplicity examples against the proven compression.
"""
from itertools import product
from collections import Counter
from random import Random
from time import monotonic

PAIRS = ((0, 1), (0, 2), (1, 2))


def brute(edges, counts, free=0):
    # Vertices 0,1,2 form the cover; remaining vertices are distinct.
    adjacency = [0] * 3
    for e, (u, v) in enumerate(PAIRS):
        if (edges >> e) & 1:
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
    for s, c in enumerate(counts, 1):
        for _ in range(c):
            v = len(adjacency)
            adjacency.append(s)
            for u in range(3):
                if (s >> u) & 1:
                    adjacency[u] |= 1 << v

    adjacency.extend([0] * free)  # Isolated vertices.

    memo = {0: 0}

    def visit(bits):
        if bits in memo:
            return memo[bits]
        child_values = 0
        remaining = bits
        while remaining:
            bit = remaining & -remaining
            v = bit.bit_length() - 1
            remaining -= bit
            child = visit(bits & ~(bit | adjacency[v]))
            child_values |= 1 << child
        g = 0
        while (child_values >> g) & 1:
            g += 1
        memo[bits] = g
        return g

    return visit((1 << len(adjacency)) - 1), len(memo)


def main():
    from verify_signatures import sg
    started = monotonic()
    distribution = Counter()
    visited_states = 0
    for edges in range(8):
        for counts in product(range(3), repeat=7):
            direct, nstates = brute(edges, counts)
            compressed = sg(7, edges, counts)
            assert direct == compressed, (edges, counts, direct, compressed)
            distribution[direct] += 1
            visited_states += nstates
        print("edge mask", edges, "seconds", round(monotonic() - started, 2),
              "visited states", visited_states, flush=True)
    assert dict(sorted(distribution.items())) == {
        0: 3735, 1: 3264, 2: 3695, 3: 4603, 4: 2199
    }
    assert visited_states == 6706678
    sharp = (0, 0, 0, 0, 1, 2, 1)
    assert brute(0, sharp)[0] == 4
    assert brute(0, sharp, free=1)[0] == 5

    # Independent checks of uncompressed 3- and 4-copy classes.
    rng = Random(20261027)
    extra = 0
    for edges in range(8):
        while extra < (edges + 1) * 32:
            counts = tuple(rng.randrange(5) for _ in range(7))
            if sum(counts) > 12:
                continue
            reduced = tuple(0 if c == 0 else 1 if c % 2 else 2
                            for c in counts)
            direct, _ = brute(edges, counts)
            assert direct == sg(7, edges, reduced), (edges, counts, direct)
            extra += 1
    print("extra parity checks", extra)
    print("distribution", dict(sorted(distribution.items())))
    print("visited states", visited_states, "seconds", round(monotonic()-started, 2))


if __name__ == "__main__":
    main()
