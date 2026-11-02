#!/usr/bin/env python3
"""Independent finite checks for K0643: q-invariant terminal offsets and parity."""
from collections import Counter
from itertools import combinations


def graph_polynomial(n, edges, r):
    """K0602 domination-side expression, with exponent shifted by s_q."""
    e = len(edges)
    adj = [0] * n
    for a, b in edges:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    out = Counter({e - 1: 1})  # center-free maximal placement
    for mask in range(1 << n):
        if any(not ((mask >> v) & 1) and not (mask & adj[v]) for v in range(n)):
            continue
        inside = sum(bool(mask & (1 << a) and mask & (1 << b)) for a, b in edges)
        offset = e - inside - (n - mask.bit_count())
        assert offset >= 0
        out[offset] += r ** inside
    return out


def hypergraph_polynomial(n, edges, r):
    """Unrelated exhaustive maximality test on actual abstract forbidden q-tuples."""
    e = len(edges)
    N = 1 + n + r * e
    s = N - e
    forbidden = []
    for i, (a, b) in enumerate(edges):
        h = (1 << 0) | (1 << (a + 1)) | (1 << (b + 1))
        for k in range(r):
            h |= 1 << (1 + n + r * i + k)
        forbidden.append(h)
    out = Counter()
    for mask in range(1 << N):
        if any(mask & h == h for h in forbidden):
            continue
        if any(
            not any(((mask | (1 << v)) & h) == h for h in forbidden)
            for v in range(N) if not (mask & (1 << v))
        ):
            continue
        out[mask.bit_count() - s] += 1
    return out


def main():
    tested_graphs = tested_direct = tested_interpolation = 0
    for n in range(2, 6):
        pairs = list(combinations(range(n), 2))
        for bits in range(1, 1 << len(pairs)):
            edges = [edge for i, edge in enumerate(pairs) if bits & (1 << i)]
            e = len(edges)
            polynomials = [graph_polynomial(n, edges, r) for r in range(1, max(7, e + 3))]
            support = set(polynomials[0])
            assert all(set(p) == support for p in polynomials)
            assert all(sum(polynomials[i].values()) % 2 == 0 for i in (0, 2, 4))
            for i in range(5):
                assert all(polynomials[i][k] <= polynomials[i + 1][k] for k in support)
            # Coefficients in r are integers, of degree at most e.
            # Verify (e+1)-st forward difference vanishes, independently
            # of the explicit coefficient formula, for all offsets.
            for offset in support:
                vals = [polynomials[r - 1][offset] for r in range(1, e + 3)]
                for _ in range(e + 1):
                    vals = [b - a for a, b in zip(vals, vals[1:])]
                assert vals == [0]
            tested_interpolation += 1
            for r in range(1, 5):
                if 1 + n + r * e <= 15:
                    direct = hypergraph_polynomial(n, edges, r)
                    assert direct == polynomials[r - 1], (n, edges, r, direct, polynomials[r - 1])
                    tested_direct += 1
            tested_graphs += 1
    k2 = [(0, 1)]
    k3 = list(combinations(range(3), 2))
    assert sum(graph_polynomial(2, k2, 2).values()) == 5
    assert sum(graph_polynomial(3, k3, 2).values()) == 18
    print(f"PASS graphs={tested_graphs} direct-hypergraphs={tested_direct} "
          f"finite-differences={tested_interpolation}; no discrepancies")


if __name__ == "__main__":
    main()
