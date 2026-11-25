#!/usr/bin/env python3
"""Independent named-vertex Node Kayles verification for the two-center theorem.

No formula-specific recurrence is used to evaluate a game.  Each individual
vertex is an available move; the move deletes its closed neighborhood.
"""
from functools import lru_cache
from itertools import product


def predicted(p, q, m):
    if p == q == m == 0:
        return 0
    if max(p, q) <= 2:
        return 2
    if min(p, q) <= 2:
        return 4
    return 3


def build(p, q, m, a=1, b=1, ra=None, rb=None, ds=None):
    assert a > 0 and b > 0 and a % 2 == b % 2 == 1
    ra = ra if ra is not None else [2] * p
    rb = rb if rb is not None else [2] * q
    ds = ds if ds is not None else [2] * m
    assert len(ra) == p and len(rb) == q and len(ds) == m
    assert all(x > 0 and x % 2 == 0 for x in ra + rb + ds)

    k = 2 + p + q + m
    adj = [((1 << k) - 1) ^ (1 << i) for i in range(k)]

    def leaf(parents):
        j = len(adj)
        adj.append(0)
        for i in parents:
            adj[i] |= 1 << j
            adj[j] |= 1 << i

    for _ in range(a):
        leaf([0])
    for _ in range(b):
        leaf([1])
    for i, count in enumerate(ra):
        for _ in range(count):
            leaf([0, 2 + i])
    for i, count in enumerate(rb):
        for _ in range(count):
            leaf([1, 2 + p + i])
    for i, count in enumerate(ds):
        for _ in range(count):
            leaf([2 + p + q + i])
    return [x | (1 << i) for i, x in enumerate(adj)]


def direct_grundy(closed_neighborhoods):
    @lru_cache(None)
    def g(mask):
        if not mask:
            return 0
        nimber_bits = 0
        seen_children = set()
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            remaining -= bit
            i = bit.bit_length() - 1
            child = mask & ~closed_neighborhoods[i]
            if child not in seen_children:
                seen_children.add(child)
                nimber_bits |= 1 << g(child)
        mex = 0
        while (nimber_bits >> mex) & 1:
            mex += 1
        return mex

    value = g((1 << len(closed_neighborhoods)) - 1)
    return value, g.cache_info().currsize


def verify():
    base_cases = 0
    nonuniform_cases = 0
    maximum_states = 0
    largest_case = None

    for p, q, m in product(range(5), range(5), range(3)):
        if p > q:
            continue
        graph = build(p, q, m)
        if len(graph) > 25:
            continue
        value, states = direct_grundy(graph)
        assert value == predicted(p, q, m), (p, q, m, value)
        base_cases += 1
        if states > maximum_states:
            maximum_states, largest_case = states, (p, q, m, len(graph))

    for p, q, m in product(range(4), range(4), range(2)):
        if p > q:
            continue
        for a, b in [(1, 3), (3, 1), (3, 3)]:
            ra = [2 + 2 * (i % 2) for i in range(p)]
            rb = [2 + 2 * (i % 2) for i in range(q)]
            ds = [2 + 2 * (i % 2) for i in range(m)]
            graph = build(p, q, m, a, b, ra, rb, ds)
            if len(graph) > 23:
                continue
            value, states = direct_grundy(graph)
            assert value == predicted(p, q, m), (p, q, m, a, b, value)
            nonuniform_cases += 1
            if states > maximum_states:
                maximum_states, largest_case = states, (
                    p, q, m, a, b, len(graph)
                )

    print("base:", base_cases)
    print("nonuniform:", nonuniform_cases)
    print("total:", base_cases + nonuniform_cases)
    print("maximum states:", maximum_states, "at", largest_case)
    print("PASS")


if __name__ == "__main__":
    verify()
