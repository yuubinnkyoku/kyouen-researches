#!/usr/bin/env python3
"""Independent checks for the pendant-clique Node Kayles formula.

No external dependencies. Run: python3 verify.py
"""
from functools import lru_cache
from itertools import product
import random


def closed_formula(counts):
    """Grundy of a clique with private pendant leaves; excludes free isolates."""
    z = sum(a == 0 for a in counts)
    o = sum(a % 2 == 1 for a in counts)
    e = sum(a > 0 and a % 2 == 0 for a in counts)
    if z:
        if o == 0:
            return 1
        return 3 if o % 2 == 0 else 2
    if e == 0:
        return o % 2
    if o == 0:
        return 2 if e == 1 else 1
    return 3 if o % 2 else 2


def direct_graph(counts, free=0):
    """Independent graph construction and closed-neighborhood deletion recursion."""
    c = len(counts)
    n = c + sum(counts) + free
    adj = [0] * n
    for i in range(c):
        for j in range(i):
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    k = c
    for i, a in enumerate(counts):
        for _ in range(a):
            adj[i] |= 1 << k
            adj[k] |= 1 << i
            k += 1

    @lru_cache(None)
    def g(remaining):
        child = set()
        todo = remaining
        while todo:
            bit = todo & -todo
            todo ^= bit
            v = bit.bit_length() - 1
            child.add(g(remaining & ~(adj[v] | bit)))
        ans = 0
        while ans in child:
            ans += 1
        return ans

    return g((1 << n) - 1)


def independent_type_recurrence():
    """A second, independent proof-obligation check for all z,o,e<=12."""
    @lru_cache(None)
    def g(z, o, e):
        if z + o + e == 0:
            return 0
        s = o & 1
        children = set()
        if z:
            children.add(s)
        if o:
            children.add(s ^ 1)
            children.add(g(z, o - 1, e))
        if e:
            children.add(s)
            children.add(g(z, o, e - 1) ^ 1)
        return next(i for i in range(5) if i not in children)

    for z, o, e in product(range(13), repeat=3):
        sample = [0] * z + [1] * o + [2] * e
        got = g(z, o, e)
        want = closed_formula(sample)
        assert got == want, (z, o, e, got, want)
    return 13**3


def main():
    type_cases = independent_type_recurrence()
    exhaustive = 0
    for c in range(6):
        for counts in product(range(4), repeat=c):
            want = closed_formula(counts)
            got = direct_graph(counts)
            assert got == want, (counts, got, want)
            exhaustive += 1
    rng = random.Random(20261027)
    random_cases = 0
    for _ in range(40):
        c = rng.randrange(0, 7)
        counts = tuple(rng.randrange(0, 5) for _ in range(c))
        free = rng.randrange(0, 2)
        want = closed_formula(counts) ^ (free & 1)
        got = direct_graph(counts, free)
        assert got == want, (counts, free, got, want)
        random_cases += 1
    print(f"type_recurrence={type_cases} exhaustive_graphs={exhaustive} random_graphs={random_cases}")
    print("maximum_formula=3; sharp_example=(0,1,1), value=", closed_formula((0, 1, 1)))


if __name__ == "__main__":
    main()
