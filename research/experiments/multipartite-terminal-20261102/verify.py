#!/usr/bin/env python3
"""Independent exact checks for complete multipartite graph-star q-point terminal polynomial.

Standard library only. Run: python3 verify.py
"""
from collections import Counter
from itertools import combinations, product
from math import comb


def edges_for_parts(parts):
    labels = [i for i, n in enumerate(parts) for _ in range(n)]
    return [(a, b) for a in range(len(labels)) for b in range(a + 1, len(labels))
            if labels[a] != labels[b]]


def terminal_dp(parts, r):
    """New polynomial-time formula; counts retained vertices and squared counts."""
    n = sum(parts)
    e = sum(a*b for a, b in combinations(parts, 2))
    N = 1+n+r*e
    states = {(0, 0, 0): 1}
    for size in parts:
        nxt = Counter()
        for (A, Q, support), count in states.items():
            for a in range(size + 1):
                nxt[(A+a, Q+a*a, min(2, support+(a > 0)))] += count*comb(size, a)
        states = nxt
    out = Counter({N-1: 1})
    for size in parts:
        out[N-n+size] += 1
    for (A, Q, support), count in states.items():
        if support == 2:
            assert (A*A-Q) % 2 == 0
            retained_edges = (A*A-Q)//2
            out[N-n+A-retained_edges] += count * r**retained_edges
    return +out


def direct_deleted_sets(parts, r):
    """Independent enumeration of all deleted vertex subsets from K0602."""
    n = sum(parts)
    edges = edges_for_parts(parts)
    N = 1+n+r*len(edges)
    neighbors = [set() for _ in range(n)]
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    out = Counter({N-1: 1})
    for mask in range(1 << n):
        deleted = {v for v in range(n) if mask & (1 << v)}
        kept = set(range(n))-deleted
        if any(not (neighbors[v] & kept) for v in deleted):
            continue
        e_keep = sum(a in kept and b in kept for a, b in edges)
        out[N-len(deleted)-e_keep] += r**e_keep
    return +out


def direct_hyperedge_game(parts, r):
    """Independently enumerate all point subsets and forbidden hyperedges."""
    n = sum(parts)
    edges = edges_for_parts(parts)
    N = 1+n+r*len(edges)
    forbidden = []
    for i, (a, b) in enumerate(edges):
        points = [0, 1+a, 1+b] + list(range(1+n+r*i, 1+n+r*(i+1)))
        forbidden.append(sum(1 << p for p in points))
    out = Counter()
    for mask in range(1 << N):
        if any((mask & f) == f for f in forbidden):
            continue
        maximal = True
        for p in range(N):
            if not (mask & (1 << p)):
                trial = mask | (1 << p)
                if not any((trial & f) == f for f in forbidden):
                    maximal = False
                    break
        if maximal:
            out[mask.bit_count()] += 1
    return +out, 1 << N


def compositions(n):
    if n == 0:
        yield ()
    else:
        for first in range(1, n+1):
            for rest in compositions(n-first):
                yield (first,)+rest


def run():
    tested = 0
    for n in range(2, 10):
        for parts in compositions(n):
            if len(parts) < 2:
                continue
            for r in (1, 2, 3):
                a = terminal_dp(parts, r)
                b = direct_deleted_sets(parts, r)
                assert a == b, (parts, r, a, b)
                tested += 1
    print(f"DP vs independent deleted-set enumeration: {tested} cases, zero mismatches")
    tested_hyper, total_subsets = 0, 0
    for n in range(2, 7):
        for parts in compositions(n):
            if len(parts) < 2:
                continue
            for r in (1, 2, 3):
                e = len(edges_for_parts(parts))
                N = 1+n+r*e
                if N > 15:
                    continue
                a = terminal_dp(parts, r)
                b, checked = direct_hyperedge_game(parts, r)
                assert a == b, (parts, r, a, b)
                tested_hyper += 1
                total_subsets += checked
    print(f"DP vs direct forbidden-hyperedge enumeration: {tested_hyper} cases, {total_subsets} point subsets, zero mismatches")
    # Specializations to K0602's complete-graph and K0604's complete-bipartite formulas.
    special = 0
    for r in (1, 2, 3):
        for k in range(2, 15):
            parts = (1,)*k
            n, e = k, k*(k-1)//2
            N = 1+n+r*e
            expected = Counter({N-1: 1})
            for j in range(1, k+1):
                expected[N-k+j-j*(j-1)//2] += comb(k, j)*r**(j*(j-1)//2)
            assert terminal_dp(parts, r) == +expected
            special += 1
        for a in range(1, 8):
            for b in range(1, 8):
                N = 1+a+b+r*a*b
                expected = Counter({N-1: 1, N-a: 1, N-b: 1})
                # Counter literal loses coinciding exponents; rebuild correctly.
                expected = Counter()
                for exp in (N-1, N-a, N-b):
                    expected[exp] += 1
                for i in range(1, a+1):
                    for j in range(1, b+1):
                        expected[N-a-b+i+j-i*j] += comb(a, i)*comb(b, j)*r**(i*j)
                assert terminal_dp((a,b), r) == +expected
                special += 1
    print(f"Complete-graph / complete-bipartite formula regressions: {special} cases, zero mismatches")
    # q=4 closed total count, with arbitrary number of parts.
    for n in range(2, 11):
        for parts in compositions(n):
            if len(parts) >= 2:
                expected = 2**n-sum(2**v for v in parts)+2*len(parts)
                assert sum(terminal_dp(parts, 1).values()) == expected
    print("q=4 total-count closed formula: all compositions n<=10, zero mismatches")
    print("EXAMPLE K_(2,2,2), q=4:", sorted(terminal_dp((2,2,2), 1).items()))
    print("EXAMPLE K_(2,2,2), q=5:", sorted(terminal_dp((2,2,2), 2).items()))


if __name__ == '__main__':
    run()
