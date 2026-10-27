#!/usr/bin/env python3
"""Verify odd complete pair-incidence Node Kayles theorem by independent recursions."""
from __future__ import annotations
from functools import lru_cache
from itertools import product
from random import Random


def predicted(a: int, b: int, c: int) -> int:
    k = a + b + c
    if k == 0:
        return 0
    if k == 1:
        return 2 if c else 1
    if k == 2:
        return (1, 2, 3)[b]
    if b == 0:
        return int(k % 4 in (1, 2))
    if b == k:
        return int(k % 4 in (0, 1))
    return 2 + ((b & 1) ^ ((k // 2) & 1))


@lru_cache(None)
def by_types(a: int, b: int, c: int) -> int:
    """Exact move-type recurrence; no use of predicted formula."""
    k = a + b + c
    if not k:
        return 0
    opts: set[int] = set()
    z = ((k - 1) * (k - 2) // 2) & 1
    if a + c:
        opts.add((b + z) & 1)
    if b:
        opts.add((b - 1 + z) & 1)
        opts.add(by_types(0, a + c, b - 1))
    if c:
        opts.add(by_types(0, a + c - 1, b) ^ 1)
    for e in range(3):
        if e == 0 and k - b < 2:
            continue
        if e == 1 and (not b or b == k):
            continue
        if e == 2 and b < 2:
            continue
        opts.add(by_types(0, b - e, k - 2 - b + e) ^ (e & 1))
    mex = 0
    while mex in opts:
        mex += 1
    return mex


def by_named_graph(k: int, leaves: tuple[int, ...], pairs: dict[tuple[int, int], int]):
    """Independent graph construction and closed-neighborhood deletion."""
    adj: list[int] = [0] * k

    def add_edge(i: int, j: int):
        adj[i] |= 1 << j
        adj[j] |= 1 << i

    for i in range(k):
        for j in range(i):
            add_edge(i, j)
    for i, t in enumerate(leaves):
        for _ in range(t):
            v = len(adj)
            adj.append(0)
            add_edge(i, v)
    for (i, j), r in pairs.items():
        for _ in range(r):
            v = len(adj)
            adj.append(0)
            add_edge(i, v)
            add_edge(j, v)
    n = len(adj)
    assert n <= 23, n

    @lru_cache(None)
    def grundy(mask: int) -> int:
        opts = set()
        rest = mask
        while rest:
            bit = rest & -rest
            rest -= bit
            v = bit.bit_length() - 1
            opts.add(grundy(mask & ~(adj[v] | bit)))
        mex = 0
        while mex in opts:
            mex += 1
        return mex

    return grundy((1 << n) - 1), grundy.cache_info().currsize


def run() -> None:
    total = 0
    for k in range(101):
        for a in range(k + 1):
            for b in range(k - a + 1):
                c = k - a - b
                observed = by_types(a, b, c)
                expected = predicted(a, b, c)
                assert observed == expected, (a, b, c, observed, expected)
                total += 1
    print(f"type-recurrence vs closed form: {total} complete (a,b,c) states, k<=100")

    direct_count = 0
    reached = 0
    for k in range(1, 5):
        pairs = {(i, j): 1 for i in range(k) for j in range(i)}
        for leaves in product(range(3), repeat=k):
            a = leaves.count(0)
            b = sum(t & 1 for t in leaves)
            c = k - a - b
            observed, states = by_named_graph(k, leaves, pairs)
            assert observed == predicted(a, b, c), (k, leaves, observed)
            direct_count += 1
            reached += states
    print(f"named-vertex direct recurrence, k<=4 and all leaves in {{0,1,2}}: {direct_count} graphs, {reached} reached states")

    rng = Random(20261028)
    mixed_count = 0
    mixed_states = 0
    for k in (3, 4, 5, 6):
        for _ in range(120):
            leaves = tuple(rng.randrange(4) for _ in range(k))
            pairs = {(i, j): rng.choice((1, 3, 5)) for i in range(k) for j in range(i)}
            n = k + sum(leaves) + sum(pairs.values())
            if n > 21:
                continue
            a = leaves.count(0)
            b = sum(t & 1 for t in leaves)
            c = k - a - b
            observed, states = by_named_graph(k, leaves, pairs)
            assert observed == predicted(a, b, c), (k, leaves, pairs, observed)
            mixed_count += 1
            mixed_states += states
    print(f"named-vertex direct recurrence, independently odd pair multiplicities: {mixed_count} graphs, {mixed_states} reached states")


if __name__ == '__main__':
    run()
