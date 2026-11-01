#!/usr/bin/env python3
"""Independent checks for the three-state forest terminal-polynomial recurrence.

The Prüfer-code oracle directly enumerates admissible deleted vertex sets.
The hypergraph oracle directly tests all subsets for safety and maximality.
"""
from collections import Counter
from itertools import product


def add(*polys):
    out = Counter()
    for p in polys:
        out.update(p)
    return {k: v for k, v in out.items() if v}


def mul(a, b):
    out = Counter()
    for i, ai in a.items():
        for j, bj in b.items():
            out[i + j] += ai * bj
    return dict(out)


def shift(a, d=0, c=1):
    return {i + d: c * v for i, v in a.items()}


def subtract(a, b):
    return add(a, {k: -v for k, v in b.items()})


def forest_polynomial(n, edges, r):
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    seen = set()
    total = {0: 1}

    def visit(v, parent):
        outside = {0: 1}
        all_valid = {0: 1}
        all_selected = {0: 1}
        for child in graph[v]:
            if child == parent:
                continue
            a, b, c = visit(child, v)
            outside = mul(outside, add(shift(a, -1, r), b, c))
            all_valid = mul(all_valid, add(a, b))
            all_selected = mul(all_selected, b)
        return (outside, shift(subtract(all_valid, all_selected), -1),
                shift(all_selected, -1))

    for root in range(n):
        if root in seen:
            continue
        stack = [root]
        while stack:
            v = stack.pop()
            if v in seen:
                continue
            seen.add(v)
            stack.extend(graph[v])
        a, b, _ = visit(root, -1)
        total = mul(total, add(a, b))
    N = 1 + n + r * len(edges)
    return add({N - 1: 1}, shift(total, N))


def vertex_oracle(n, edges, r):
    N = 1 + n + r * len(edges)
    neighbors = [set() for _ in range(n)]
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    out = Counter({N - 1: 1})
    for mask in range(1 << n):
        deleted = {v for v in range(n) if mask >> v & 1}
        if any(not (neighbors[v] - deleted) for v in deleted):
            continue
        intact = sum(a not in deleted and b not in deleted for a, b in edges)
        out[N - len(deleted) - intact] += r ** intact
    return dict(out)


def prufer_edges(code):
    n = len(code) + 2
    degree = [1] * n
    for v in code:
        degree[v] += 1
    edges = []
    for v in code:
        leaf = next(i for i in range(n) if degree[i] == 1)
        edges.append((leaf, v))
        degree[leaf] -= 1
        degree[v] -= 1
    a, b = [i for i in range(n) if degree[i] == 1]
    return edges + [(a, b)]


def hypergraph_oracle(n, edges, r):
    N = 1 + n + r * len(edges)
    forbidden = []
    for index, (a, b) in enumerate(edges):
        f = (1 << 0) | (1 << (1 + a)) | (1 << (1 + b))
        for j in range(r):
            f |= 1 << (1 + n + r * index + j)
        forbidden.append(f)
    assert all(f.bit_count() == r + 3 for f in forbidden)
    out = Counter()
    for mask in range(1 << N):
        if any(mask & f == f for f in forbidden):
            continue
        if all(any((mask | (1 << i)) & f == f for f in forbidden)
               for i in range(N) if not (mask >> i) & 1):
            out[mask.bit_count()] += 1
    return dict(out)


def run():
    tree_checks = 0
    for n in range(2, 8):
        for code in product(range(n), repeat=n - 2):
            edges = prufer_edges(code)
            for r in (1, 2, 3):
                assert forest_polynomial(n, edges, r) == vertex_oracle(n, edges, r), (n, code, r)
                tree_checks += 1

    direct_checks = 0
    subsets = 0
    for n in range(2, 6):
        codes = list(product(range(n), repeat=n - 2))
        for code in codes[:4 if n > 3 else len(codes)]:
            edges = prufer_edges(code)
            for r in (1, 2):
                N = 1 + n + r * len(edges)
                assert forest_polynomial(n, edges, r) == hypergraph_oracle(n, edges, r), (n, code, r)
                direct_checks += 1
                subsets += 1 << N

    star_checks = 0
    for r in range(1, 5):
        for d in range(1, 13):
            edges = [(0, i) for i in range(1, d + 1)]
            N = 2 + (r + 1) * d
            expected = add({N - d: (r + 1) ** d}, {N - 1: 2})
            assert forest_polynomial(d + 1, edges, r) == expected
            star_checks += 1

    # Isolated vertices are allowed if at least one edge remains.
    for r in (1, 2, 3):
        edges = [(0, 1), (1, 2)]
        assert forest_polynomial(5, edges, r) == vertex_oracle(5, edges, r)

    print("PASS: %d Prüfer-tree checks; %d direct hypergraph checks (%d subsets); "
          "%d star checks; 3 isolated-vertex checks" %
          (tree_checks, direct_checks, subsets, star_checks))


if __name__ == "__main__":
    run()
