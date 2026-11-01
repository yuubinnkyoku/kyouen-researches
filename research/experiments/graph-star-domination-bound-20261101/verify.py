#!/usr/bin/env python3
"""Independent checks for graph-star domination bounds (K0605)."""
from fractions import Fraction
from itertools import combinations
from math import prod


def graphs(n):
    pairs = list(combinations(range(n), 2))
    for bits in range(1 << len(pairs)):
        edges = [p for i, p in enumerate(pairs) if bits & (1 << i)]
        degrees = [0] * n
        for u, v in edges:
            degrees[u] += 1
            degrees[v] += 1
        if min(degrees) >= 2:
            yield edges, degrees


def partition(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    color = [-1] * n
    for start in range(n):
        if color[start] >= 0:
            continue
        color[start] = 0
        queue = [start]
        for v in queue:
            for w in adj[v]:
                if color[w] < 0:
                    color[w] = 1 - color[v]
                    queue.append(w)
    a = [v for v in range(n) if color[v] == 0]
    b = [v for v in range(n) if color[v] == 1]
    assert all(any(color[w] != color[v] for w in adj[v]) for v in range(n))
    return a, b


def weighted_total(n, edges, r):
    neighbors = [0] * n
    for u, v in edges:
        neighbors[u] |= 1 << v
        neighbors[v] |= 1 << u
    z = 0
    for x in range(1 << n):
        if all(not (x & (1 << v)) or (neighbors[v] & ~x) for v in range(n)):
            u = ((1 << n) - 1) ^ x
            eu = sum(bool(u & (1 << v)) and bool(u & (1 << w))
                     for v, w in edges)
            z += r ** eu
    other = 0
    for u in range(1 << n):
        if all((u & (1 << v)) or (neighbors[v] & u) for v in range(n)):
            eu = sum(bool(u & (1 << v)) and bool(u & (1 << w))
                     for v, w in edges)
            other += r ** eu
    assert z == other
    return 1 + z


def direct_hypergraph_total(n, edges, r):
    count = 1 + n + r * len(edges)
    hyperedges = []
    for i, (u, v) in enumerate(edges):
        hyperedges.append(
            1 | (1 << (u + 1)) | (1 << (v + 1)) |
            sum(1 << (n + 1 + r * i + j) for j in range(r)))
    total = 0
    shortest_count = 0
    shortest_size = count - len(edges)
    for mask in range(1 << count):
        if any((mask & h) == h for h in hyperedges):
            continue
        if any(not (mask & (1 << p)) and
               all(((mask | (1 << p)) & h) != h for h in hyperedges)
               for p in range(count)):
            continue
        total += 1
        shortest_count += mask.bit_count() == shortest_size
    return total, shortest_count


def run():
    checks = 0
    direct = 0
    for n in (3, 4, 5):
        for edges, degrees in graphs(n):
            a, b = partition(n, edges)
            e = len(edges)
            for r in (1, 2, 3):
                t = weighted_total(n, edges, r)
                norm = Fraction(t, r ** e)
                lower = (prod(1 + Fraction(1, r ** degrees[v]) for v in a)
                         + prod(1 + Fraction(1, r ** degrees[v]) for v in b)
                         - 1 + Fraction(1, r ** e))
                assert norm >= lower, (n, edges, r, norm, lower)
                delta = max(degrees)
                x = 1 + Fraction(1, r ** delta)
                assert norm >= x ** ((n + 1) // 2) + x ** (n // 2) - 1 + Fraction(1, r ** e)
                if r == 1:
                    assert t >= 2 ** ((n + 1) // 2) + 2 ** (n // 2)
                checks += 1
    for n in (3, 4):
        selected = list(graphs(n))
        for edges, _ in selected[:5]:
            for r in (1, 2):
                if 1 + n + r * len(edges) > 17:
                    continue
                total, shortest_count = direct_hypergraph_total(n, edges, r)
                assert total == weighted_total(n, edges, r)
                assert shortest_count == r ** len(edges)
                direct += 1
    print(f"PASS: {checks} exact graph/partition/weighted-domination checks; "
          f"{direct} full hypergraph subset enumerations")


if __name__ == "__main__":
    run()
