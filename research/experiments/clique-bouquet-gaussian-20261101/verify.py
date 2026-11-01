#!/usr/bin/env python3
"""Independent exact checks for clique-bouquet graph-star terminal polynomials.

All checks use integer masks and exact integer arithmetic. The direct hypergraph
route does not use the dominating-set characterization.
"""
from collections import Counter
from math import comb


def multiply(a, b):
    c = Counter()
    for i, ai in a.items():
        for j, bj in b.items():
            c[i + j] += ai * bj
    return c


def power(a, n):
    c = {0: 1}
    for _ in range(n):
        c = multiply(c, a)
    return c


def predicted(k, L, r):
    E = k * (k + 1) // 2
    N = 2 + (k + r * E) * L
    s = N - E * L
    A, B = Counter(), Counter()
    for j in range(k + 1):
        A[E - k - j * (j - 1) // 2] += comb(k, j) * r ** (j * (j + 1) // 2)
        if j:
            B[E - k + j - j * (j - 1) // 2] += comb(k, j) * r ** (j * (j - 1) // 2)
    out = Counter({N - 1: 1})
    for d, count in power(A, L).items():
        out[s + d] += count
    for d, count in power(B, L).items():
        out[s - 1 + d] += count
    return dict(sorted(out.items()))


def graph(k, L):
    t = 1 + k * L
    edges = []
    for i in range(L):
        petal = [1 + i * k + j for j in range(k)]
        for a in petal:
            edges.append((0, a))
        for ai, a in enumerate(petal):
            for b in petal[ai + 1:]:
                edges.append((a, b))
    return t, edges


def enumerate_dominating(k, L, r):
    t, edges = graph(k, L)
    N = 1 + t + r * len(edges)
    out = Counter({N - 1: 1})
    neighbors = [0] * t
    for a, b in edges:
        neighbors[a] |= 1 << b
        neighbors[b] |= 1 << a
    for D in range(1 << t):
        kept = ((1 << t) - 1) ^ D
        if any((D >> v) & 1 and not (neighbors[v] & kept) for v in range(t)):
            continue
        intact = sum(not ((D >> a) & 1 or (D >> b) & 1) for a, b in edges)
        out[N - D.bit_count() - intact] += r ** intact
    return dict(sorted(out.items()))


def enumerate_hypergraph(k, L, r):
    t, edges = graph(k, L)
    N = 1 + t + r * len(edges)
    forb = []
    for i, (a, b) in enumerate(edges):
        m = (1 << 0) | (1 << (1 + a)) | (1 << (1 + b))
        for j in range(r):
            m |= 1 << (1 + t + r * i + j)
        forb.append(m)
    assert all(x.bit_count() == r + 3 for x in forb)
    out = Counter()
    for mask in range(1 << N):
        if any(mask & f == f for f in forb):
            continue
        if all(any((mask | (1 << p)) & f == f for f in forb)
               for p in range(N) if not (mask >> p) & 1):
            out[mask.bit_count()] += 1
    return dict(sorted(out.items()))


def run():
    checks = 0
    for k, max_L in [(2, 6), (3, 4), (4, 3)]:
        for L in range(1, max_L + 1):
            for r in range(1, 5):
                assert predicted(k, L, r) == enumerate_dominating(k, L, r), (k, L, r)
                checks += 1
    cases = [(2, 1, 1), (2, 1, 2), (2, 1, 3), (2, 2, 1),
             (2, 2, 2), (2, 3, 1), (3, 1, 1), (3, 1, 2), (4, 1, 1)]
    masks = 0
    for k, L, r in cases:
        t, edges = graph(k, L)
        N = 1 + t + r * len(edges)
        assert predicted(k, L, r) == enumerate_hypergraph(k, L, r), (k, L, r)
        checks += 1
        masks += 1 << N
    print(f"PASS: {checks} exact independent comparisons; {masks} direct hypergraph subsets")
    print("k=2, L=2, q=4:", predicted(2, 2, 1))
    print("k=2, L=2, q=5:", predicted(2, 2, 2))
    print("k=2, L=1, q=5:", predicted(2, 1, 2))
    print("k=3, L=2, q=4:", predicted(3, 2, 1))


if __name__ == "__main__":
    run()
