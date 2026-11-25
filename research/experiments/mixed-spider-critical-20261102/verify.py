#!/usr/bin/env python3
"""Independent exact checks for q=4 mixed arm lengths 2 and 3.

Formula uses per-arm polynomials. Independent enumerators use (i) graph
vertex deletion subsets and (ii) forbidden 4-subsets of the abstract board.
"""
from collections import Counter


def mul(a, b):
    out = Counter()
    for i, ai in a.items():
        for j, bj in b.items():
            out[i + j] += ai * bj
    return +out


def power(a, k):
    out = Counter({0: 1})
    for _ in range(k):
        out = mul(out, a)
    return out


def add(out, poly, shift, sign=1):
    for i, x in poly.items():
        out[i + shift] += sign * x


def formula(n, k):
    assert n + k >= 1
    s = 2 + 2*n + 3*k
    out = Counter()
    add(out, mul(power({0: 2, 1: 1}, n), power({0: 2, 1: 4}, k)), s)
    add(out, mul(power({0: 3}, n), power({0: 4, 1: 1}, k)), s+n+k-1)
    out[s+n+k-1] -= 2**k
    out[s+2*n+3*k-1] += 1
    return +out


def graph(n, k):
    lengths = [2]*n + [3]*k
    edges = []
    v = 1
    for length in lengths:
        parent = 0
        for _ in range(length):
            edges.append((parent, v))
            parent = v
            v += 1
    return v, edges


def direct_graph(n, k):
    v, edges = graph(n, k)
    N = 1 + v + len(edges)
    neighbors = [0]*v
    for a, b in edges:
        neighbors[a] |= 1 << b
        neighbors[b] |= 1 << a
    out = Counter({N-1: 1})
    full = (1 << v)-1
    for deleted in range(1 << v):
        kept = full ^ deleted
        if any(deleted & (1 << i) and not (neighbors[i] & kept)
               for i in range(v)):
            continue
        kept_edges = sum(bool(kept & (1 << a)) and bool(kept & (1 << b))
                         for a, b in edges)
        out[N - deleted.bit_count() - kept_edges] += 1
    return +out


def direct_hyperedges(n, k):
    v, edges = graph(n, k)
    N = 1 + v + len(edges)
    forbidden = [(1 << 0) | (1 << (a+1)) | (1 << (b+1)) |
                 (1 << (1+v+i)) for i, (a,b) in enumerate(edges)]
    full = (1 << N)-1
    out = Counter()
    for occupied in range(1 << N):
        if any(occupied & f == f for f in forbidden):
            continue
        missing = full ^ occupied
        while missing:
            bit = missing & -missing
            if not any((occupied | bit) & f == f for f in forbidden):
                break
            missing ^= bit
        else:
            out[occupied.bit_count()] += 1
    return +out, 1 << N


def main():
    graph_count = 0
    for n in range(7):
        for k in range(5):
            if not n+k or 2*n+3*k > 15:
                continue
            assert formula(n,k) == direct_graph(n,k), (n,k)
            graph_count += 1
    hyper_cases = [(1,0),(0,1),(2,0),(0,2),(1,1),
                   (3,0),(2,1),(1,2),(4,0)]
    total = 0
    for n,k in hyper_cases:
        actual, subsets = direct_hyperedges(n,k)
        assert actual == formula(n,k), (n,k,actual,formula(n,k))
        total += subsets
    for n in range(1, 8):
        for k in range(7):
            p = mul(power({0:2,1:1},n),power({0:2,1:4},k))
            assert sum(p.values()) == 3**n*6**k
            assert sum(formula(n,k).values()) == 3**n*(6**k+5**k)-2**k+1
    print(f'PASS graph deletion: {graph_count} cases')
    print(f'PASS direct forbidden hyperedges: {len(hyper_cases)} cases / {total:,} subsets')
    print('PASS exact total count: 49 cases')
    print('Example n=1,k=1:', sorted(formula(1,1).items()))


if __name__ == '__main__':
    main()
