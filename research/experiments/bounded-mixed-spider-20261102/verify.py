#!/usr/bin/env python3
"""Independent exact checks for bounded heterogeneous-arm graph-star terminal laws.

Uses only the standard library. Branch-word polynomial and two independent
full enumerators are compared, including leaves and q=5 edge multiplicities.
"""
from collections import Counter
from itertools import product


def multiply(a, b):
    out = Counter()
    for i, x in a.items():
        for j, y in b.items():
            out[i + j] += x * y
    return +out


def branch(length, r):
    f, g, j = Counter(), Counter(), Counter()
    for word in product((0, 1), repeat=length):
        for center in (0, 1):
            bits = (center,) + word + (0,)
            if any(bits[i] == 0 and bits[i - 1] == 0 and bits[i + 1] == 0
                   for i in range(1, length + 1)):
                continue
            missing = word.count(0)
            kept_edges = sum(bits[i] * bits[i + 1]
                             for i in range(length))
            coefficient = r ** kept_edges
            if center:
                f[length - missing - kept_edges] += coefficient
            else:
                degree = length - 1 - missing - kept_edges
                g[degree] += coefficient
                if word[0] == 0:
                    j[degree] += coefficient
    return +f, +g, +j


def predicted(lengths, r):
    e, d = sum(lengths), len(lengths)
    s = 2 + r * e
    f, g, j = Counter({0: 1}), Counter({0: 1}), Counter({0: 1})
    for length in lengths:
        ff, gg, jj = branch(length, r)
        f, g, j = multiply(f, ff), multiply(g, gg), multiply(j, jj)
    out = Counter()
    for degree, count in f.items():
        out[s + degree] += count
    for degree, count in g.items():
        out[s + d - 1 + degree] += count
    for degree, count in j.items():
        out[s + d - 1 + degree] -= count
    out[s + e - 1] += 1
    return +out


def graph(lengths):
    edges = []
    vertices = 1
    for length in lengths:
        prev = 0
        for _ in range(length):
            edges.append((prev, vertices))
            prev = vertices
            vertices += 1
    return vertices, edges


def direct_graph(lengths, r):
    vertices, edges = graph(lengths)
    N = 1 + vertices + r * len(edges)
    neighbors = [0] * vertices
    for a, b in edges:
        neighbors[a] |= 1 << b
        neighbors[b] |= 1 << a
    full = (1 << vertices) - 1
    out = Counter({N - 1: 1})
    for deleted in range(1 << vertices):
        kept = full ^ deleted
        if any((deleted >> v) & 1 and not (neighbors[v] & kept)
               for v in range(vertices)):
            continue
        kept_edges = sum(bool((kept >> a) & 1) and bool((kept >> b) & 1)
                         for a, b in edges)
        out[N - deleted.bit_count() - kept_edges] += r ** kept_edges
    return +out


def direct_forbidden(lengths, r):
    vertices, edges = graph(lengths)
    N = 1 + vertices + r * len(edges)
    forbidden = []
    for index, (a, b) in enumerate(edges):
        edge_bits = ((1 << r) - 1) << (1 + vertices + r * index)
        forbidden.append(1 | (1 << (a + 1)) | (1 << (b + 1)) | edge_bits)
    full = (1 << N) - 1
    out = Counter()
    for occupied in range(1 << N):
        if any(occupied & h == h for h in forbidden):
            continue
        missing = full ^ occupied
        while missing:
            bit = missing & -missing
            if not any((occupied | bit) & h == h for h in forbidden):
                break
            missing ^= bit
        else:
            out[occupied.bit_count()] += 1
    return +out, 1 << N


def main():
    ngraph = 0
    for n1 in range(4):
        for n2 in range(5):
            for n3 in range(3):
                for n4 in range(2):
                    lengths = [1] * n1 + [2] * n2 + [3] * n3 + [4] * n4
                    if not lengths or sum(lengths) > 10:
                        continue
                    for r in (1, 2, 3):
                        expected = predicted(lengths, r)
                        got = direct_graph(lengths, r)
                        assert got == expected, (lengths, r, got, expected)
                        ngraph += 1
    cases = [
        ([1], 1), ([2], 1), ([1, 2], 1), ([1, 3], 1),
        ([2, 3], 1), ([2, 4], 1), ([1, 2, 3], 1),
        ([1, 1, 2], 1), ([2, 2, 1], 1), ([1, 4], 1),
        ([1, 2], 2), ([1, 3], 2), ([2, 2], 2),
        ([1, 1], 3), ([2], 3),
    ]
    subsets = 0
    for lengths, r in cases:
        got, count = direct_forbidden(lengths, r)
        expected = predicted(lengths, r)
        assert got == expected, (lengths, r, got, expected)
        subsets += count
    for r in range(1, 6):
        for length in range(1, 13):
            f, g, j = branch(length, r)
            a, b = sum(f.values()), sum(g.values())
            assert a >= b, (length, r)
            if length == 1:
                assert (a, b, j) == (r + 1, 1, Counter())
            elif length == 2:
                assert a == r*r + r + 1 and b == r + 2
                assert (a == b) == (r == 1)
            else:
                assert a - b >= r ** (length - 3)
    print(f'PASS graph-deletion independent enumeration: {ngraph} cases')
    print(f'PASS forbidden-hyperedge complete enumeration: {len(cases)} cases / {subsets:,} subsets')
    print('PASS center-sector inequalities: 60 exact parameter cases')
    print('q=4, one leaf and n length-2 arms: limiting sector weights 2/3 and 1/3')
    print('example [1,2,3], q=4:', sorted(predicted([1,2,3], 1).items()))


if __name__ == '__main__':
    main()
