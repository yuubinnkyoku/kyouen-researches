#!/usr/bin/env python3
"""Independent exact checks for the equal-arm spider terminal polynomial.

Only the standard library is needed. Branch words, graph-vertex deletion
sets and forbidden-hyperedge subsets are counted by separate routines.
"""
from collections import Counter
from itertools import product


def add_scaled(a, b, shift=0, factor=1):
    result = Counter(a)
    for degree, coefficient in b.items():
        result[degree + shift] += factor * coefficient
    return +result


def multiply(a, b):
    out = Counter()
    for i, x in a.items():
        for j, y in b.items():
            out[i + j] += x * y
    return +out


def power(a, n):
    result = Counter({0: 1})
    for _ in range(n):
        result = multiply(result, a)
    return result


def branch_polynomials(length, r):
    """F,G,J: direct binary-word enumeration, not a recurrence."""
    F, G, J = Counter(), Counter(), Counter()
    for word in product((0, 1), repeat=length):
        for center in (0, 1):
            chain = (center,) + word
            if any(chain[i] == 0 and chain[i-1] == 0 and
                   (i == length or chain[i+1] == 0)
                   for i in range(1, length+1)):
                continue
            deleted = word.count(0)
            kept_edges = sum(chain[i] and chain[i+1]
                             for i in range(length))
            coefficient = r ** kept_edges
            if center:
                F[length - deleted - kept_edges] += coefficient
            else:
                degree = length - 1 - deleted - kept_edges
                G[degree] += coefficient
                if word[0] == 0:
                    J[degree] += coefficient
    return +F, +G, +J


def predicted(length, d, r):
    F, G, J = branch_polynomials(length, r)
    s = 2 + r * length * d
    hist = Counter()
    hist = add_scaled(hist, power(F, d), s)
    hist = add_scaled(hist, power(G, d), s+d-1)
    hist = add_scaled(hist, power(J, d), s+d-1, -1)
    hist[s+length*d-1] += 1
    return +hist


def direct_graph(length, d, r):
    """Enumerate every graph-vertex deletion subset independently."""
    vertices = 1 + length*d
    edges = []
    for arm in range(d):
        prev = 0
        for depth in range(length):
            v = 1 + arm*length + depth
            edges.append((prev, v))
            prev = v
    neighbors = [0] * vertices
    for a, b in edges:
        neighbors[a] |= 1 << b
        neighbors[b] |= 1 << a
    N = 1 + vertices + r*len(edges)
    out = Counter({N-1: 1})
    full = (1 << vertices) - 1
    for deleted in range(1 << vertices):
        kept = full ^ deleted
        if any((deleted >> v) & 1 and not (neighbors[v] & kept)
               for v in range(vertices)):
            continue
        kept_edges = sum(bool((kept >> a) & 1) and bool((kept >> b) & 1)
                         for a, b in edges)
        stones = N - deleted.bit_count() - kept_edges
        out[stones] += r ** kept_edges
    return +out


def direct_hyperedges(length, d, r):
    """Enumerate all 2^N board subsets using forbidden hyperedges only."""
    vertices = 1 + length*d
    edges = []
    for arm in range(d):
        prev = 0
        for depth in range(length):
            v = 1 + arm*length + depth
            edges.append((prev, v))
            prev = v
    N = 1 + vertices + r*len(edges)
    forbidden = []
    for index, (a, b) in enumerate(edges):
        edge_points = ((1 << r) - 1) << (1 + vertices + r*index)
        forbidden.append((1 << 0) | (1 << (a+1)) |
                         (1 << (b+1)) | edge_points)
    full = (1 << N) - 1
    out = Counter()
    for occupied in range(1 << N):
        if any(occupied & f == f for f in forbidden):
            continue
        missing = full ^ occupied
        maximal = True
        while missing:
            bit = missing & -missing
            if not any((occupied | bit) & f == f for f in forbidden):
                maximal = False
                break
            missing ^= bit
        if maximal:
            out[occupied.bit_count()] += 1
    return +out, 1 << N


def main():
    ngraph = 0
    for length in range(1, 9):
        for d in range(1, 5):
            if length*d > 15:
                continue
            for r in range(1, 5):
                got = direct_graph(length, d, r)
                expected = predicted(length, d, r)
                assert got == expected, (length, d, r, got, expected)
                ngraph += 1
    nhyper, subsets = 0, 0
    cases = [(2, 2, 1), (3, 1, 1), (3, 2, 1),
             (4, 1, 1), (4, 2, 1), (5, 1, 1),
             (6, 1, 1), (4, 1, 2), (5, 1, 2), (3, 2, 2)]
    for length, d, r in cases:
        got, n = direct_hyperedges(length, d, r)
        expected = predicted(length, d, r)
        assert got == expected, (length, d, r, got, expected)
        nhyper += 1
        subsets += n
    for length in range(1, 20):
        for r in range(1, 10):
            F, G, J = branch_polynomials(length, r)
            A, B = sum(F.values()), sum(G.values())
            assert A >= B
            if length >= 3:
                assert A > B and A - B >= r ** (length - 3)
                assert F[0] > 0 and F[1] > 0
            if length == 2 and r == 1:
                assert A == B
    F, G, J = branch_polynomials(4, 1)
    assert F == {0: 2, 1: 8, 2: 1}, F
    assert G == {0: 4, 1: 5}, G
    assert J == {0: 2, 1: 1}, J
    print(f'PASS: graph-vertex deletion {ngraph} cases; forbidden-hyperedge {nhyper} cases / {subsets:,} subsets;')
    print('PASS: A>=B and strict lower bound 171 integer parameter cases; length-four coefficients.')
    print('L=4, r=1: F=2+8u+u^2, G=4+5u, J=2+u; B/A=9/11.')


if __name__ == '__main__':
    main()
