#!/usr/bin/env python3
"""Independent exact checks of the length-three spider maximal-size polynomial.

No dependencies beyond the Python standard library.  In particular, neither
K0613's closed formula nor the graph-deletion enumerator is used to construct
the forbidden-hyperedge enumerator.
"""
from collections import Counter
from math import comb


def graph(d):
    t = 1 + 3 * d
    edges = []
    for i in range(d):
        a, b, c = 1 + 3 * i, 2 + 3 * i, 3 + 3 * i
        edges.extend(((0, a), (a, b), (b, c)))
    return t, edges


def predicted(d, r):
    n = 2 + 3 * (r + 1) * d
    s = n - 3 * d
    result = Counter()
    for k in range(d + 1):
        result[s + k] += comb(d, k) * (r + 1) ** d * r ** (2 * (d - k)) * 2 ** k
        result[s + d - 1 + k] += comb(d, k) * (r + 1) ** (2 * (d - k))
    result[s + d - 1] -= (r + 1) ** d
    result[n - 1] += 1
    return +result


def direct_graph(d, r):
    t, edges = graph(d)
    n = 1 + t + r * len(edges)
    adjacency = [0] * t
    for a, b in edges:
        adjacency[a] |= 1 << b
        adjacency[b] |= 1 << a
    full = (1 << t) - 1
    result = Counter({n - 1: 1})
    for deleted in range(1 << t):
        remaining = full ^ deleted
        if any((deleted >> v) & 1 and not (adjacency[v] & remaining)
               for v in range(t)):
            continue
        kept_edges = sum(bool((remaining >> a) & 1 and (remaining >> b) & 1)
                         for a, b in edges)
        result[n - deleted.bit_count() - kept_edges] += r ** kept_edges
    return +result


def direct_hyperedges(d, r):
    t, edges = graph(d)
    q = r + 3
    n = 1 + t + r * len(edges)
    hyperedges = []
    next_point = t + 1
    for a, b in edges:
        sites = (0, 1 + a, 1 + b, *range(next_point, next_point + r))
        assert len(sites) == q
        hyperedges.append(sum(1 << v for v in sites))
        next_point += r
    assert next_point == n
    result = Counter()
    for subset in range(1 << n):
        if any((subset & h) == h for h in hyperedges):
            continue
        if all(any(((subset | (1 << v)) & h) == h for h in hyperedges)
               for v in range(n) if not (subset >> v) & 1):
            result[subset.bit_count()] += 1
    return +result


def main():
    graph_cases = 0
    for d in range(1, 6):
        for r in range(1, 5):
            expected = predicted(d, r)
            actual = direct_graph(d, r)
            assert expected == actual, (d, r, expected, actual)
            graph_cases += 1
    hyper_cases = [(1, 1), (1, 2), (1, 3), (1, 4),
                   (2, 1), (2, 2), (3, 1)]
    subsets = 0
    for d, r in hyper_cases:
        n = 2 + 3 * (r + 1) * d
        actual = direct_hyperedges(d, r)
        expected = predicted(d, r)
        assert actual == expected, (d, r, expected, actual)
        subsets += 1 << n
    # Strict inequality proving the one-phase normal limit, checked in a
    # separate finite sample but proved symbolically in proof.md.
    for r in range(1, 100):
        A = (r + 1) * (r * r + 2)
        B = (r + 1) ** 2 + 1
        assert A - B == r ** 3 and 0 < B < A
    print(f'PASS: {graph_cases} deletion-enumeration cases; '
          f'{len(hyper_cases)} direct-hyperedge cases; '
          f'{subsets:,} complete subsets; 99 arithmetic checks')
    print('Example q=4, d=2:', sorted(predicted(2, 1).items()))


if __name__ == '__main__':
    main()
