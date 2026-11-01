"""Independent finite checks for q-point graph-star circle games (K0602).

No third-party dependencies: python verify.py
"""
from collections import Counter
from itertools import combinations
from math import comb


def polynomial(n, edges, q):
    r = q - 3
    e = len(edges)
    N = 1 + n + r * e
    neighbors = [set() for _ in range(n)]
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    safe = Counter({k: comb(N - 1, k) for k in range(N)})
    terminal = Counter({N - 1: 1})
    for bits in range(1 << n):
        X = {v for v in range(n) if bits & (1 << v)}
        factors = [Counter({0: 1})]
        for a, b in edges:
            inside = a in X and b in X
            factor = Counter({j: comb(r, j) for j in range(r + (not inside))})
            old = factors[-1]
            new = Counter()
            for i, ci in old.items():
                for j, cj in factor.items():
                    new[i + j] += ci * cj
            factors.append(new)
        for k, ways in factors[-1].items():
            safe[1 + len(X) + k] += ways
        if all(neighbors[v] - X for v in X):
            untouched = sum(a not in X and b not in X for a, b in edges)
            terminal[N - len(X) - untouched] += r ** untouched
    return +safe, +terminal


def brute(n, edges, q):
    r = q - 3
    N = 1 + n + r * len(edges)
    forbidden = []
    for i, (a, b) in enumerate(edges):
        f = 1 | (1 << (1 + a)) | (1 << (1 + b))
        for j in range(r):
            f |= 1 << (1 + n + i * r + j)
        forbidden.append(f)
    safe, terminal = Counter(), Counter()
    for bits in range(1 << N):
        if any(bits & f == f for f in forbidden):
            continue
        safe[bits.bit_count()] += 1
        if all(any((bits | (1 << p)) & f == f for f in forbidden)
               for p in range(N) if not bits & (1 << p)):
            terminal[bits.bit_count()] += 1
    return +safe, +terminal


def shortest_count(n, edges, q):
    r = q - 3
    e = len(edges)
    deg = [0] * n
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    isolated_edges = sum(deg[a] == deg[b] == 1 for a, b in edges)
    outer_leaves = sum(deg[v] == 1 and deg[next(b if a == v else a
                           for a, b in edges if a == v or b == v)] >= 2
                       for v in range(n))
    assert e >= outer_leaves + isolated_edges
    return r ** (e - outer_leaves - isolated_edges) * (r + 1) ** outer_leaves * (r + 2) ** isolated_edges + (e == 1)


def circle_or_line(points):
    """Exact 4x4 rank test of (x,y,x*x+y*y,1), including collinearity."""
    def det3(a, b, c):
        return (a[0] * (b[1] * c[2] - b[2] * c[1])
                - a[1] * (b[0] * c[2] - b[2] * c[0])
                + a[2] * (b[0] * c[1] - b[1] * c[0]))
    x0, y0 = points[0]
    rows = [(x - x0, y - y0, x*x + y*y - x0*x0 - y0*y0)
            for x, y in points[1:]]
    return all(det3(*three) == 0 for three in combinations(rows, 3))


def verify_geometry():
    pts = [(3, 1), (3, 5), (6, 4), (4, 4), (2, 2), (2, 4),
           (0, 2), (0, 4), (3, 3), (4, 0)]
    expected = [(0, 1, 2, 4, 5), (0, 1, 3, 6, 7), (0, 2, 3, 8, 9)]
    actual = [ids for ids in combinations(range(10), 5)
              if circle_or_line([pts[i] for i in ids])]
    assert actual == expected, (actual, expected)
    assert brute(3, [(0, 1), (0, 2), (1, 2)], 5) == polynomial(
        3, [(0, 1), (0, 2), (1, 2)], 5)
    assert polynomial(3, [(0, 1), (0, 2), (1, 2)], 5)[1] == Counter({7: 8, 8: 9, 9: 1})
    print('q=5 geometry: 10 points, 252 five-subsets, 1024 game subsets, 0 mismatches')


def main():
    total_graphs = total_subsets = 0
    for q, max_n in [(4, 5), (5, 4), (6, 3), (7, 3)]:
        for n in range(2, max_n + 1):
            pairs = list(combinations(range(n), 2))
            for bits in range(1, 1 << len(pairs)):
                edges = [pair for i, pair in enumerate(pairs) if bits >> i & 1]
                got = brute(n, edges, q)
                expected = polynomial(n, edges, q)
                assert got == expected, (q, n, bits, got, expected)
                N = 1 + n + (q - 3) * len(edges)
                assert min(got[1]) == N - len(edges)
                assert max(got[1]) == N - 1
                assert got[1][N - len(edges)] == shortest_count(n, edges, q), (q, n, edges, got[1])
                total_graphs += 1
                total_subsets += 1 << N
    print(f'q=4..7: {total_graphs} labeled graph games, {total_subsets} subsets, 0 mismatches')
    verify_geometry()


if __name__ == '__main__':
    main()
