#!/usr/bin/env python3
"""Independent finite audits for K0612; standard library only."""
from collections import Counter
from math import comb


def formula(d, r):
    n = 2 + 2 * (r + 1) * d
    s = n - 2 * d
    out = Counter({s + k: comb(d, k) * (r * (r + 1)) ** (d - k)
                   for k in range(d + 1)})
    out[n - d - 1] += (r + 2) ** d - 1
    out[n - 1] += 1
    return +out


def graph_enumeration(d, r):
    """Directly enumerate all vertex subsets and test domination."""
    n = 2 * d + 1
    edges = [(0, 1 + i) for i in range(d)] + [
        (1 + i, 1 + d + i) for i in range(d)]
    allmask = (1 << n) - 1
    nsites = 1 + n + r * len(edges)
    counts = Counter()
    for deleted in range(1 << n):
        kept = allmask ^ deleted
        if any(not any((kept >> w) & 1 for a, b in edges
                       for w in ([b] if a == v else [a] if b == v else []))
               for v in range(n) if (deleted >> v) & 1):
            continue
        internal = sum(bool((kept >> a) & 1) and bool((kept >> b) & 1)
                       for a, b in edges)
        counts[nsites - deleted.bit_count() - internal] += r ** internal
    counts[nsites - 1] += 1  # Unique maximal set omitting O.
    return +counts


def hyperedge_enumeration(d, r):
    """Enumerate every point subset; independently check safety/maximality."""
    nv = 2 * d + 1
    o = nv
    edges = [(0, 1 + i) for i in range(d)] + [
        (1 + i, 1 + d + i) for i in range(d)]
    hyperedges = []
    for j, (a, b) in enumerate(edges):
        h = (1 << o) | (1 << a) | (1 << b)
        for k in range(r):
            h |= 1 << (o + 1 + r * j + k)
        hyperedges.append(h)
    n = o + 1 + r * len(edges)
    allmask = (1 << n) - 1
    counts = Counter()
    for mask in range(1 << n):
        if any((mask & h) == h for h in hyperedges):
            continue
        absent = allmask ^ mask
        maximal = True
        while absent:
            bit = absent & -absent
            absent -= bit
            if not any(((mask | bit) & h) == h for h in hyperedges):
                maximal = False
                break
        if maximal:
            counts[mask.bit_count()] += 1
    return +counts


def main():
    tests_graph = 0
    for r in range(1, 5):
        for d in range(1, 8):
            actual = graph_enumeration(d, r)
            expected = formula(d, r)
            assert actual == expected, (d, r, actual, expected)
            assert sum(actual.values()) == (r * (r + 1) + 1) ** d + (r + 2) ** d
            tests_graph += 1
    tests_hyper = 0
    subsets = 0
    for r, dmax in [(1, 4), (2, 3), (3, 2)]:
        for d in range(1, dmax + 1):
            actual = hyperedge_enumeration(d, r)
            expected = formula(d, r)
            assert actual == expected, (d, r, actual, expected)
            tests_hyper += 1
            subsets += 1 << (2 + 2 * (r + 1) * d)
    print(f"PASS graph-subset conditions={tests_graph}, forbidden-hyperedge conditions={tests_hyper},"
          f" point subsets={subsets}, mismatches=0")
    for d, r in [(3, 1), (3, 2), (4, 1)]:
        print(f"d={d},r={r},P={dict(sorted(formula(d,r).items()))}")


if __name__ == '__main__':
    main()
