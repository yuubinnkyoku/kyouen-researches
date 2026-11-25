#!/usr/bin/env python3
"""Independent split-clique recurrence for two Node Kayles witnesses."""
from functools import lru_cache

WITNESSES = (
    (7, (3, 3, 5, 9, 9, 20, 20, 32, 36, 36, 48, 65, 65), 7),
    (6, (3, 3, 4, 4, 5, 9, 9, 16, 20, 20, 33, 33), 6),
)


def clique_recurrence(k, signatures):
    """Subset recurrence over clique vertices, not named-vertex deletion."""
    limit = 1 << k
    parity = [sum(bool(s & x) for s in signatures) % 2 for x in range(limit)]
    g = [0] * limit
    for x in range(1, limit):
        options = set()
        for c in range(k):
            if x & (1 << c):
                options.add(sum(bool(s & x) and not (s & (1 << c)) for s in signatures) % 2)
        for s in set(signatures):
            if s & x:
                y = x & ~s
                options.add(g[y] ^ parity[x] ^ parity[y] ^ 1)
        mex = 0
        while mex in options:
            mex += 1
        g[x] = mex
    return g[-1]


def direct_recurrence(k, signatures):
    """Separate direct graph solver, deleting closed neighborhoods of named vertices."""
    n = k + len(signatures)
    neighbors = [0] * n
    for i in range(k):
        for j in range(k):
            if i != j:
                neighbors[i] |= 1 << j
    for j, s in enumerate(signatures):
        assert s > 0 and s.bit_count() <= 2 and s < (1 << k)
        for i in range(k):
            if s & (1 << i):
                neighbors[i] |= 1 << (k + j)
                neighbors[k + j] |= 1 << i
    assert all((neighbors[k + i] >> k) == 0 for i in range(len(signatures)))
    full = (1 << n) - 1
    reachable = 0
    stack = [0]
    while stack:
        i = stack.pop()
        if reachable & (1 << i):
            continue
        reachable |= 1 << i
        remaining = neighbors[i] & ~reachable
        while remaining:
            b = remaining & -remaining
            remaining -= b
            stack.append(b.bit_length() - 1)
    assert reachable == full, "Witness must be connected"

    @lru_cache(None)
    def sg(mask):
        values = set()
        remaining = mask
        while remaining:
            b = remaining & -remaining
            remaining -= b
            i = b.bit_length() - 1
            values.add(sg(mask & ~(neighbors[i] | b)))
        mex = 0
        while mex in values:
            mex += 1
        return mex

    children = [sg(full & ~(neighbors[i] | (1 << i))) for i in range(n)]
    return sg(full), children, sg.cache_info().currsize


if __name__ == "__main__":
    for k, signatures, expected in WITNESSES:
        via_clique = clique_recurrence(k, signatures)
        via_graph, children, states = direct_recurrence(k, signatures)
        assert via_clique == via_graph == expected
        assert set(range(expected)) <= set(children) and expected not in children
        print(f"k={k} n={k + len(signatures)} g={expected} states={states}")
        print("children:", children)
