#!/usr/bin/env python3
"""Independent named-vertex Node Kayles test for the center-pair parity theorem.

The evaluator uses the original graph and closed-neighborhood deletion; neither
F/E recurrences nor the star theorem are used in the computation.
"""
from functools import lru_cache
from itertools import product


def predicted(p, q, m, ab):
    n = p + q + m
    if ab & 1:
        return 3 if n == 0 else 0
    if n == 0:
        return 0
    if max(p, q) <= 2:
        return 2
    if min(p, q) <= 2:
        return 4
    return 3


def build(p, q, m, a=1, b=1, ab=0, ra=None, rb=None, ds=None):
    assert a > 0 and b > 0 and a % 2 == b % 2 == 1
    ra = [2] * p if ra is None else ra
    rb = [2] * q if rb is None else rb
    ds = [2] * m if ds is None else ds
    assert len(ra) == p and len(rb) == q and len(ds) == m
    assert ab >= 0 and all(x > 0 and x % 2 == 0 for x in ra + rb + ds)
    k = 2 + p + q + m
    adj = [((1 << k) - 1) ^ (1 << i) for i in range(k)]

    def leaf(parents):
        j = len(adj)
        adj.append(0)
        for i in parents:
            adj[i] |= 1 << j
            adj[j] |= 1 << i

    for _ in range(a):
        leaf((0,))
    for _ in range(b):
        leaf((1,))
    for i, count in enumerate(ra):
        for _ in range(count):
            leaf((0, 2 + i))
    for i, count in enumerate(rb):
        for _ in range(count):
            leaf((1, 2 + p + i))
    for i, count in enumerate(ds):
        for _ in range(count):
            leaf((2 + p + q + i,))
    for _ in range(ab):
        leaf((0, 1))
    return [x | (1 << i) for i, x in enumerate(adj)]


def grundy(closed):
    @lru_cache(None)
    def g(mask):
        if not mask:
            return 0
        bits = 0
        seen = set()
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            remaining -= bit
            i = bit.bit_length() - 1
            child = mask & ~closed[i]
            if child not in seen:
                seen.add(child)
                bits |= 1 << g(child)
        mex = 0
        while (bits >> mex) & 1:
            mex += 1
        return mex

    result = g((1 << len(closed)) - 1)
    return result, g.cache_info().currsize


def run():
    counts = {"uniform": 0, "nonuniform": 0, "one_center_even": 0, "boundary": 0}
    max_states = 0
    max_case = None

    def check(label, p, q, m, a, b, ab, ra, rb, ds):
        nonlocal max_states, max_case
        graph = build(p, q, m, a, b, ab, ra, rb, ds)
        if len(graph) > 20:
            return
        value, states = grundy(graph)
        expected = predicted(p, q, m, ab)
        assert value == expected, (label, p, q, m, a, b, ab, value, expected)
        counts[label] += 1
        if states > max_states:
            max_states, max_case = states, (label, p, q, m, a, b, ab, len(graph))

    for p, q, m, ab in product(range(4), range(4), range(2), range(4)):
        if p > q:
            continue
        check("uniform", p, q, m, 1, 1, ab, [2]*p, [2]*q, [2]*m)

    for p, q, m, ab in product(range(4), range(4), range(2), range(4)):
        if p > q:
            continue
        for a, b in [(1, 3), (3, 1), (3, 3)]:
            ra = [2 + 2*(i%2) for i in range(p)]
            rb = [4 - 2*(i%2) for i in range(q)]
            ds = [2 + 2*(i%2) for i in range(m)]
            check("nonuniform", p, q, m, a, b, ab, ra, rb, ds)

    # Larger, sharp-transition boundary cases (not a complete parameter box).
    for p, q, m, a, b, ab in [
        (3, 3, 0, 1, 1, 1), (3, 3, 0, 1, 1, 3),
        (3, 3, 0, 1, 1, 2), (4, 0, 0, 1, 1, 1),
        (4, 1, 0, 1, 1, 1), (3, 2, 0, 3, 1, 1),
        (3, 2, 0, 1, 3, 1), (0, 0, 3, 1, 1, 1),
        (0, 0, 3, 1, 1, 2), (1, 1, 2, 1, 1, 1),
        (2, 2, 1, 1, 1, 3),
    ]:
        graph = build(p, q, m, a, b, ab)
        value, states = grundy(graph)
        expected = predicted(p, q, m, ab)
        assert value == expected, (p, q, m, a, b, ab, value, expected)
        counts["boundary"] += 1
        if states > max_states:
            max_states, max_case = states, ("boundary", p, q, m, a, b, ab, len(graph))

    # Separate one-center even-private-leaf lemma, including nonuniform counts.
    for q, s in product(range(5), range(3)):
        ra = [2 + 2*(i%2) for i in range(q)]
        ds = [4 - 2*(i%2) for i in range(s)]
        k = 1 + q + s
        adj = [((1 << k)-1) ^ (1 << i) for i in range(k)]
        def leaf(parents):
            j = len(adj)
            adj.append(0)
            for i in parents:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
        for _ in range(4):
            leaf((0,))
        for i, c in enumerate(ra):
            for _ in range(c):
                leaf((0, 1+i))
        for i, c in enumerate(ds):
            for _ in range(c):
                leaf((1+q+i,))
        if len(adj) > 20:
            continue
        value, states = grundy([x | (1<<i) for i, x in enumerate(adj)])
        assert value == (2 if s == 0 and q <= 1 else 1), (q, s, value)
        counts["one_center_even"] += 1
        if states > max_states:
            max_states, max_case = states, ("one_center_even", q, s, len(adj))

    print("counts:", counts)
    print("total:", sum(counts.values()))
    print("maximum states:", max_states, "case:", max_case)
    print("PASS")


if __name__ == "__main__":
    run()
