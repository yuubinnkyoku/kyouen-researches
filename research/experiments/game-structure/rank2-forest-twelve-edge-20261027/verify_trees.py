#!/usr/bin/env python3
"""Complete unlabeled-tree enumeration up to 12 edges, with two SG recurrences.

Python standard library only. Trees are adjacency-bitmask tuples.
"""
from collections import Counter
from functools import lru_cache

EXPECTED = {
    1: (0, 1), 2: (0, 0, 1), 3: (1, 1),
    4: (0, 0, 1, 2), 5: (2, 4), 6: (1, 2, 5, 3),
    7: (11, 11, 0, 0, 1), 8: (6, 7, 14, 18, 2),
    9: (41, 42, 7, 4, 8, 4), 10: (35, 36, 72, 66, 11, 14, 1),
    11: (173, 174, 49, 62, 43, 50),
    12: (195, 209, 336, 340, 122, 85, 5, 9),
}

def canonical(a):
    """Complete unrooted-tree isomorphism invariant via all rooted encodings."""
    n = len(a)
    def rooted(v, parent):
        return "(" + "".join(sorted(
            rooted(u, v) for u in range(n)
            if a[v] & (1 << u) and u != parent
        )) + ")"
    return min(rooted(v, -1) for v in range(n))

def available_sg(a):
    n = len(a)
    @lru_cache(None)
    def rec(available):
        seen = {rec(available & ~(a[v] | (1 << v)))
                for v in range(n) if available & (1 << v)}
        g = 0
        while g in seen:
            g += 1
        return g
    return rec((1 << n) - 1)

def occupied_sg(a):
    n = len(a)
    @lru_cache(None)
    def rec(chosen):
        seen = {rec(chosen | (1 << v)) for v in range(n)
                if not (chosen & (1 << v)) and not (a[v] & chosen)}
        g = 0
        while g in seen:
            g += 1
        return g
    return rec(0)

def extend_by_leaf(trees):
    representatives = {}
    for a in trees:
        n = len(a)
        for v in range(n):
            b = list(a) + [1 << v]
            b[v] |= 1 << n
            b = tuple(b)
            representatives.setdefault(canonical(b), b)
    return list(representatives.values())

def main():
    trees = [(2, 1)]  # one edge
    possible = {}
    witness = None
    for e in range(1, 13):
        if e > 1:
            trees = extend_by_leaf(trees)
        histogram = Counter()
        for a in trees:
            x, y = available_sg(a), occupied_sg(a)
            assert x == y, (e, a, x, y)
            histogram[x] += 1
            if e == 12 and x == 7 and witness is None:
                witness = a
        actual = tuple(histogram.get(i, 0) for i in range(max(histogram) + 1))
        assert actual == EXPECTED[e], (e, actual)
        possible[e] = set(histogram)
        print("tree", e, len(trees), actual, flush=True)

    assert witness is not None
    edges = [(i, j) for i in range(len(witness))
             for j in range(i + 1, len(witness))
             if witness[i] & (1 << j)]
    print("tree_12_edge_grundy_7", edges)
    assert 7 not in possible[11] and 7 in possible[12]

    # Every forest is a disjoint union of nontrivial trees and isolated vertices.
    attainable = [{0}] + [set() for _ in range(12)]
    for e in range(1, 13):
        attainable[e] = {x ^ y for k in range(1, e + 1)
                         for x in possible[k] for y in attainable[e-k]}
        assert max(attainable[e]) <= 7
        print("forest", e, sorted(attainable[e]), flush=True)
    assert 7 not in attainable[9] and 7 in attainable[10]

if __name__ == "__main__":
    main()
