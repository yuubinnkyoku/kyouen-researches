#!/usr/bin/env python3
"""Independent exact checks for graph-star bounded-degree/cycle terminal theorem.
No third-party packages; integer arithmetic only.
"""
from itertools import combinations
from fractions import Fraction
from math import comb


def graph_edges(t, mask):
    pairs = list(combinations(range(t), 2))
    return [edge for i, edge in enumerate(pairs) if mask & (1 << i)]


def polynomial_from_transversals(t, edges, r):
    """Enumerate all subsets of actual symbols and test minimal hitting sets."""
    e = len(edges)
    N = 1 + t + r * e
    forbidden = []
    for i, (a, b) in enumerate(edges):
        h = (1 << 0) | (1 << (1 + a)) | (1 << (1 + b))
        for j in range(r):
            h |= 1 << (1 + t + r * i + j)
        forbidden.append(h)
    out = {}
    for mask in range(1 << N):
        if any((mask & h) == 0 for h in forbidden):
            continue
        if any(all(((mask & ~(1 << v)) & h) != 0 for h in forbidden)
               for v in range(N) if mask & (1 << v)):
            continue  # Not inclusion-minimal
        length = N - mask.bit_count()
        out[length] = out.get(length, 0) + 1
    return out


def polynomial_from_graph(t, edges, r):
    e = len(edges)
    N = 1 + t + r * e
    out = {N - 1: 1}
    for mask in range(1 << t):
        X = {i for i in range(t) if mask & (1 << i)}
        if any(not any((a == v and b not in X) or (b == v and a not in X)
                           for a, b in edges) for v in X):
            continue
        untouched = sum(a not in X and b not in X for a, b in edges)
        length = N - len(X) - untouched
        out[length] = out.get(length, 0) + r ** untouched
    return out


def trace_matrix_power(r, t):
    M = ((r, 1, 0, 0), (0, 0, 1, 1), (r, 1, 0, 0), (0, 0, 1, 0))
    P = [[int(i == j) for j in range(4)] for i in range(4)]
    for _ in range(t):
        P = [[sum(P[i][k] * M[k][j] for k in range(4))
              for j in range(4)] for i in range(4)]
    return sum(P[i][i] for i in range(4))


def cycle_sum_direct(t, r):
    z = 0
    for mask in range(1 << t):
        x = [(mask >> i) & 1 for i in range(t)]
        if any(x[(i - 1) % t] and x[i] and x[(i + 1) % t]
               for i in range(t)):
            continue
        zero_edges = sum(x[i] == 0 and x[(i + 1) % t] == 0
                         for i in range(t))
        z += r ** zero_edges
    return z


def check_general_bound(t, edges, r):
    deg = [0] * t
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    if min(deg) < 2:
        return False
    e = len(edges)
    poly = polynomial_from_graph(t, edges, r)
    T = sum(poly.values())
    assert poly[1 + t + (r - 1) * e] == r ** e
    independent = []
    edge_set = {frozenset(pair) for pair in edges}
    for v in range(t):
        if all(frozenset((v, w)) not in edge_set for w in independent):
            independent.append(v)
    assert len(independent) >= (t + max(deg)) // (max(deg) + 1)
    product = Fraction(1)
    for v in independent:
        product *= Fraction(r ** deg[v] + 1, r ** deg[v])
    assert Fraction(T, r ** e) >= product
    assert Fraction(r ** e, T) <= Fraction(1, 1) / product
    return True


def main():
    cycles = 0
    for r in range(1, 5):
        for t in range(4, 13):
            z = cycle_sum_direct(t, r)
            assert z == trace_matrix_power(r, t)
            edges = [(i, (i + 1) % t) for i in range(t)]
            poly = polynomial_from_graph(t, edges, r)
            assert sum(poly.values()) == 1 + z
            assert poly[1 + t + (r - 1) * t] == r ** t
            if t >= 7:
                assert z == r * cycle_sum_direct(t - 1, r) + cycle_sum_direct(t - 2, r) + cycle_sum_direct(t - 3, r)
            cycles += 1
    direct = 0
    for t in range(3, 6):
        edges = [(i, (i + 1) % t) for i in range(t)]
        for r in (1, 2):
            assert polynomial_from_transversals(t, edges, r) == polynomial_from_graph(t, edges, r)
            direct += 1
    graphs = 0
    for t in range(3, 6):
        for mask in range(1 << comb(t, 2)):
            edges = graph_edges(t, mask)
            for r in (1, 2, 3):
                graphs += int(check_general_bound(t, edges, r))
    print(f"PASS: {cycles} cycle partition checks, {direct} direct transversal enumerations, {graphs} graph-degree-bound checks")
    for r in (1, 2, 3):
        print(f"r={r}: C4 T={1 + cycle_sum_direct(4, r)}, shortest={r ** 4}; C5 T={1 + cycle_sum_direct(5, r)}, shortest={r ** 5}")


if __name__ == '__main__':
    main()
