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



def dense_count_independent(n, edges, r):
    """Count minimal transversals directly from their vertex masks."""
    adj = [0] * n
    for a, b in edges:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    total = 1  # the transversal {O}
    for x in range(1 << n):
        if any((x >> v & 1) and not (adj[v] & ~x) for v in range(n)):
            continue
        uncovered = sum(not (x >> a & 1) and not (x >> b & 1)
                        for a, b in edges)
        total += r ** uncovered
    return total


def verify_dense_concentration():
    """Exact graph bound, complete-graph spectrum, and q=4/q>=5 contrast."""
    checked_dense = 0
    for n in range(3, 6):
        pairs = list(combinations(range(n), 2))
        for mask in range(1, 1 << len(pairs)):
            edges = [edge for i, edge in enumerate(pairs) if mask >> i & 1]
            deg = [sum(v in edge for edge in edges) for v in range(n)]
            delta = min(deg)
            if delta < 2:
                continue
            e = len(edges)
            for r in range(2, 5):
                N = 1 + n + r * e
                T = dense_count_independent(n, edges, r)
                poly = polynomial(n, edges, r + 3)[1]
                assert T == sum(poly.values()), (n, mask, r)
                assert poly[N - e] == r ** e, (n, mask, r)
                # Exact integer bound: no floating point or rounding.
                upper = r ** e + 1 + sum(
                    comb(n, k) * r ** (e - (delta * k + 1) // 2)
                    for k in range(1, n + 1))
                assert r ** e <= T <= upper, (n, mask, r, T, upper)
                checked_dense += 1
    checked_complete = 0
    for t in range(3, 13):
        edges = list(combinations(range(t), 2))
        e = len(edges)
        for r in range(1, 5):
            N = 1 + t + r * e
            spectrum = Counter({N - 1: 1})
            for j in range(1, t + 1):
                spectrum[N - t + j - comb(j, 2)] += (
                    comb(t, j) * r ** comb(j, 2))
            assert len(spectrum) == t, (t, r, spectrum)
            assert min(spectrum) == N - e and max(spectrum) == N - 1
            assert (max(spectrum) - min(spectrum) + 1 - len(spectrum)
                    == e - t), (t, r)
            assert spectrum[N - e] == r ** e, (t, r)
            assert sum(spectrum.values()) == (
                1 + sum(comb(t, j) * r ** comb(j, 2)
                        for j in range(1, t + 1)))
            if r == 1:
                assert sum(spectrum.values()) == 2 ** t
            if t <= 7:
                assert spectrum == polynomial(t, edges, r + 3)[1], (t, r)
            checked_complete += 1
    print(f'density corollary: {checked_dense} exact min-degree graphs, '
          f'{checked_complete} complete-graph spectra, 0 mismatches')


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
    verify_dense_concentration()


if __name__ == '__main__':
    main()
