#!/usr/bin/env python3
"""Exact independent audits of the disjoint-clique graph-star theorem."""
from collections import Counter
from itertools import combinations
from math import comb


def formula(h, ell, r):
    t, e = ell * h, ell * comb(h, 2)
    n = 1 + t + r * e
    part = Counter({0: 1})
    for _ in range(ell):
        nxt = Counter()
        for degree, coefficient in part.items():
            for j in range(1, h + 1):
                nxt[degree + j - comb(j, 2)] += (
                    coefficient * comb(h, j) * r ** comb(j, 2)
                )
        part = nxt
    out = Counter({n - 1: 1})
    for degree, coefficient in part.items():
        out[n - t + degree] += coefficient
    return +out


def direct_graph(h, ell, r):
    """Enumerate all vertex subsets without decomposing components."""
    t, e = ell * h, ell * comb(h, 2)
    n = 1 + t + r * e
    neighbors = [0] * t
    edges = []
    for base in range(0, t, h):
        for i, j in combinations(range(base, base + h), 2):
            edges.append((i, j))
            neighbors[i] |= 1 << j
            neighbors[j] |= 1 << i
    out = Counter({n - 1: 1})
    for u in range(1 << t):
        if any(not (u & (1 << v)) and not (u & neighbors[v])
               for v in range(t)):
            continue
        inside = sum(bool(u & (1 << i)) and bool(u & (1 << j))
                     for i, j in edges)
        out[n - t + u.bit_count() - inside] += r ** inside
    return +out


def direct_hypergraph(h, ell, r):
    """Enumerate all safe and maximal placements on the actual q-point game."""
    t, e = ell * h, ell * comb(h, 2)
    n = 1 + t + r * e
    assert n <= 19
    forbidden = []
    point = 1 + t
    for base in range(0, t, h):
        for i, j in combinations(range(base, base + h), 2):
            mask = 1 | (1 << (1 + i)) | (1 << (1 + j))
            for _ in range(r):
                mask |= 1 << point
                point += 1
            forbidden.append(mask)
    assert point == n
    safe = bytearray(1 << n)
    safe[0] = 1
    for s in range(1, 1 << n):
        parent = s ^ (s & -s)
        if safe[parent] and not any((s & edge) == edge for edge in forbidden):
            safe[s] = 1
    out = Counter()
    board = (1 << n) - 1
    for s in range(1 << n):
        if not safe[s]:
            continue
        missing = board ^ s
        maximal = True
        while missing:
            bit = missing & -missing
            missing ^= bit
            if safe[s | bit]:
                maximal = False
                break
        if maximal:
            out[s.bit_count()] += 1
    return +out


def main():
    count = 0
    for h in range(3, 7):
        for ell in range(1, 4):
            if h * ell > 12:
                continue
            for r in (1, 2, 3, 4):
                assert formula(h, ell, r) == direct_graph(h, ell, r)
                count += 1
    assert count == 40, count
    count = 0
    for h, ell, r in [(3, 1, 1), (3, 1, 2), (3, 2, 1),
                      (3, 2, 2), (4, 1, 1), (4, 1, 2)]:
        assert formula(h, ell, r) == direct_hypergraph(h, ell, r)
        count += 1
    assert count == 6
    count = 0
    for h in range(3, 18):
        for r in (1, 2, 3, 4):
            w = sum(comb(h, j) * r ** comb(j, 2)
                    for j in range(1, h + 1))
            assert sum(formula(h, 1, r).values()) == 1 + w
            count += 1
    assert count == 60
    assert formula(3, 2, 2) == Counter({13: 64, 14: 144, 15: 81, 18: 1})
    print("40 direct graph, 6 full hypergraph, 60 component checks: PASS")


if __name__ == "__main__":
    main()
