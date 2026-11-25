#!/usr/bin/env python3
"""Independent finite audit of the graph-star top terminal gap.

Run: python3 verify.py. Python standard library only.
"""
from itertools import combinations
from collections import Counter


def graph_edges(n, code):
    pairs = list(combinations(range(n), 2))
    return [edge for i, edge in enumerate(pairs) if code >> i & 1]


def vertex_cover_number(n, edges):
    for k in range(n + 1):
        for verts in combinations(range(n), k):
            cover = set(verts)
            if all(a in cover or b in cover for a, b in edges):
                return k
    raise AssertionError


def center_terminals_by_graph(n, edges, r):
    """Independent weighted domination-subset enumerator, not used by direct audit."""
    N = 1 + n + r * len(edges)
    ans = Counter()
    for bits in range(1 << n):
        R = {v for v in range(n) if bits >> v & 1}
        if any(not any((a == v and b in R) or (b == v and a in R)
                       for a, b in edges) for v in range(n) if v not in R):
            continue
        inside = sum(a in R and b in R for a, b in edges)
        ans[N - (n - len(R)) - inside] += r ** inside
    return ans


def center_terminals_direct(n, edges, r):
    """Enumerate point sets and q-forbidden sets, checking every legal extension."""
    N = 1 + n + r * len(edges)
    forbidden = []
    for i, (a, b) in enumerate(edges):
        f = 1 | (1 << (1 + a)) | (1 << (1 + b))
        for j in range(r):
            f |= 1 << (1 + n + r * i + j)
        forbidden.append(f)
    counts = Counter()
    for s in range(1, 1 << N, 2):
        if any(s & f == f for f in forbidden):
            continue
        if all(any((s | (1 << j)) & f == f for f in forbidden)
               for j in range(1, N) if not s >> j & 1):
            counts[s.bit_count()] += 1
    return counts


def main():
    graphs = 0
    formula_cases = 0
    direct_cases = 0
    direct_subsets = 0
    for n in range(2, 7):
        for code in (range(1, 1 << (n * (n - 1) // 2))
                     if n <= 5 else range(1, 1001)):
            edges = graph_edges(n, code)
            tau = vertex_cover_number(n, edges)
            graphs += 1
            for r in (1, 2, 3):
                N = 1 + n + r * len(edges)
                predicted = center_terminals_by_graph(n, edges, r)
                assert max(predicted) == N - tau, (n, code, r, tau, predicted)
                assert all(k <= N - tau for k in predicted)
                assert predicted[N - tau] > 0
                if tau >= 2:
                    assert not any(k in predicted for k in range(N - tau + 1, N - 1))
                formula_cases += 1
                if N <= 12:
                    direct = center_terminals_direct(n, edges, r)
                    assert direct == predicted, (n, code, r, direct, predicted)
                    direct_cases += 1
                    direct_subsets += 1 << (N - 1)
    print(f'graph instances={graphs}; formula cases={formula_cases}; '
          f'direct forbidden-hyperedge cases={direct_cases}; '
          f'center-containing subsets inspected={direct_subsets}; mismatches=0')


if __name__ == '__main__':
    main()
