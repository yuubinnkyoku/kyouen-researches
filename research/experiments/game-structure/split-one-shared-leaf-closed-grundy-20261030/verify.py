#!/usr/bin/env python3
"""Independent named-graph Node Kayles checks and finite induction table audit."""
from functools import lru_cache
from collections import Counter
from itertools import product
import random


def mex(values):
    values = set(values)
    result = 0
    while result in values:
        result += 1
    return result


@lru_cache(None)
def private(z, o, e):
    """Grundy recurrence for clique centers with private leaves only."""
    if z + o + e == 0:
        return 0
    p = o & 1
    children = []
    if z or e:
        children.append(p)
    if o:
        children.extend((p ^ 1, private(z, o - 1, e)))
    if e:
        children.append(private(z, o, e - 1) ^ 1)
    return mex(children)


def formula(a, b, z, o, e):
    """Closed formula for one leaf shared by the first two centers."""
    pa, pb, po = a & 1, b & 1, o & 1
    if z:
        if pa != pb:
            return 3 if po == 0 else 2
        if pa == 0:
            return 2 if po == 0 else 3
        return 0 if o == 0 else (3 if po else 2)
    if pa != pb:
        return 2 if po == 0 else 3
    if pa == 0:
        if not e:
            return 1 if po == 0 else 0
        return 3 if po == 0 else 2
    if o == 0:
        return 3 if e == 0 else 0
    return 2 if po else 3


def formula_children(a, b, z, o, e):
    """All legal move types; G children are strictly smaller in o+e."""
    p = (a + b + o) & 1
    children = [(b + o) & 1, (a + o) & 1,
                private(z, o, e) ^ ((a + b) & 1)]
    if z or e:
        children.append(p ^ 1)
    if o:
        children.append(p)
    if a:
        children.append(
            private(z, o + ((b + 1) & 1),
                    e + (1 - ((b + 1) & 1))) ^ ((a - 1) & 1)
        )
    if b:
        children.append(
            private(z, o + ((a + 1) & 1),
                    e + (1 - ((a + 1) & 1))) ^ ((b - 1) & 1)
        )
    if o:
        children.append(formula(a, b, z, o - 1, e))
    if e:
        children.append(formula(a, b, z, o, e - 1) ^ 1)
    return children


def named_graph(t, isolates=0):
    """Build every named vertex and compute mex by closed-neighborhood deletion."""
    k = len(t)
    n = k + sum(t) + 1 + isolates
    adj = [1 << i for i in range(n)]
    for i in range(k):
        for j in range(i + 1, k):
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    pos = k
    for i, count in enumerate(t):
        for _ in range(count):
            adj[i] |= 1 << pos
            adj[pos] |= 1 << i
            pos += 1
    for i in (0, 1):
        adj[i] |= 1 << pos
        adj[pos] |= 1 << i

    @lru_cache(None)
    def rec(mask):
        if not mask:
            return 0
        children = []
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            i = bit.bit_length() - 1
            children.append(rec(mask & ~adj[i]))
        return mex(children)

    value = rec((1 << n) - 1)
    return value, rec.cache_info().currsize


def main():
    checks = 0
    for a, b, z, o, e in product(range(4), range(4), range(2),
                                  range(6), range(4)):
        expected = formula(a, b, z, o, e)
        observed = mex(formula_children(a, b, z, o, e))
        assert observed == expected, (a, b, z, o, e, expected, observed)
        checks += 1

    assert {formula(a, b, z, o, e)
            for a, b, z, o, e in product(range(3), range(3),
                                          range(2), range(4), range(3))
            } == set(range(4))

    cases = states = 0
    hist = Counter()
    for a, b, z, o, e in product(range(4), range(4), range(3),
                                  range(3), range(3)):
        t = (a, b) + (0,) * z + (1,) * o + (2,) * e
        if len(t) + sum(t) + 1 > 18:
            continue
        for isolates in (0, 1):
            actual, visited = named_graph(t, isolates)
            expected = formula(a, b, z, o, e) ^ isolates
            assert actual == expected, (a, b, z, o, e, isolates,
                                        actual, expected)
            cases += 1
            states += visited
            hist[actual] += 1

    rng = random.Random(20261030)
    random_cases = 0
    for _ in range(400):
        a, b = rng.randrange(5), rng.randrange(5)
        others = [rng.randrange(7) for _ in range(rng.randrange(5))]
        t = (a, b) + tuple(others)
        if len(t) + sum(t) + 1 > 18:
            continue
        z = others.count(0)
        o = sum(v > 0 and v % 2 == 1 for v in others)
        e = sum(v > 0 and v % 2 == 0 for v in others)
        actual, visited = named_graph(t)
        expected = formula(a, b, z, o, e)
        assert actual == expected, (t, actual, expected)
        random_cases += 1
        states += visited

    print("induction_representatives=", checks)
    print("named_graph_cases=", cases)
    print("random_named_graph_cases=", random_cases)
    print("named_graph_states_sum=", states)
    print("named_graph_root_histogram=", dict(sorted(hist.items())))
    print("all checks passed")


if __name__ == "__main__":
    main()
