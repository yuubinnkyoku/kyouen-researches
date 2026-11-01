"""Independent exhaustive checks for graph-star circle universality (K0601).
Run with Python 3, no third-party packages: python verify.py
"""
from collections import Counter
from itertools import combinations, permutations
from math import comb


def formulas(n, edges):
    e = len(edges)
    assert e > 0
    N = 1 + n + e
    neighbors = [set() for _ in range(n)]
    for v, w in edges:
        neighbors[v].add(w)
        neighbors[w].add(v)
    safe = Counter({k: comb(N - 1, k) for k in range(N)})
    terminal = Counter({N - 1: 1})
    for mask in range(1 << n):
        X = {v for v in range(n) if mask >> v & 1}
        inside = sum(v in X and w in X for v, w in edges)
        for j in range(e - inside + 1):
            safe[1 + len(X) + j] += comb(e - inside, j)
        if all(neighbors[v] - X for v in X):
            untouched = sum(v not in X and w not in X for v, w in edges)
            terminal[N - len(X) - untouched] += 1
    return +safe, +terminal


def brute(n, edges):
    e = len(edges)
    N = 1 + n + e
    forbidden = [1 | (1 << (v + 1)) | (1 << (w + 1)) | (1 << (n + 1 + i))
                 for i, (v, w) in enumerate(edges)]
    safe, terminal = Counter(), Counter()
    for mask in range(1 << N):
        if any(mask & f == f for f in forbidden):
            continue
        safe[mask.bit_count()] += 1
        if all(any((mask | (1 << p)) & f == f for f in forbidden)
               for p in range(N) if not (mask >> p & 1)):
            terminal[mask.bit_count()] += 1
    return +safe, +terminal


def det4(points):
    """Leibniz determinant: no reliance on a geometric-circle library."""
    rows = [(x, y, x*x + y*y, 1) for x, y in points]
    total = 0
    for p in permutations(range(4)):
        inv = sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4))
        term = -1 if inv & 1 else 1
        for i in range(4):
            term *= rows[i][p[i]]
        total += term
    return total


def verify_triangle():
    pts = [(10, 8), (3, 9), (10, 1), (4, 10), (3, 0), (5, 3), (0, 3)]
    observed = [tuple(q) for q in combinations(range(7), 4)
                if det4([pts[i] for i in q]) == 0]
    expected = [(0, 1, 2, 4), (0, 1, 3, 5), (0, 2, 3, 6)]
    assert observed == expected, (observed, expected)
    forbidden = [sum(1 << i for i in q) for q in observed]
    safe, terminal = Counter(), Counter()
    for mask in range(1 << 7):
        if any(mask & f == f for f in forbidden):
            continue
        safe[mask.bit_count()] += 1
        if all(any((mask | (1 << i)) & f == f for f in forbidden)
               for i in range(7) if not (mask >> i & 1)):
            terminal[mask.bit_count()] += 1
    assert (+safe, +terminal) == formulas(3, [(0, 1), (0, 2), (1, 2)])
    assert terminal == Counter({4: 1, 5: 6, 6: 1})
    print("triangle 11x11 witness: 35 quadruples, 128 subsets, 0 mismatches")


def main():
    graphs = 0
    subsets = 0
    for n in range(2, 6):
        pairs = list(combinations(range(n), 2))
        for bits in range(1, 1 << len(pairs)):
            edges = [pair for i, pair in enumerate(pairs) if bits >> i & 1]
            got = brute(n, edges)
            expected = formulas(n, edges)
            assert got == expected, (n, bits, got, expected)
            graphs += 1
            subsets += 1 << (1 + n + len(edges))
    print(f"all labeled graphs n=2..5: {graphs} graphs, {subsets} subsets, 0 mismatches")
    verify_triangle()
    for n in range(3, 6):
        edges = list(combinations(range(n), 2))
        _, p = formulas(n, edges)
        assert sum(p.values()) == 1 << n
        assert min(p) == n + 1
        assert max(p) == n + len(edges)
        assert p[n + 1] == p[max(p)] == 1
        print(f"K_{n}: N={1+n+len(edges)}, maximal polynomial={sorted(p.items())}")


if __name__ == "__main__":
    main()
