#!/usr/bin/env python3
"""Independent exhaustive audit of the first positive graph-star terminal offset."""
from collections import Counter
from itertools import combinations
from random import Random


def direct_spectrum(n, edges, r):
    """Independent domination-set enumeration (not the leaf-core polynomial)."""
    e = len(edges)
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    result = Counter({e - 1: 1})  # center-free terminal
    for x in range(1 << n):
        if any(x >> v & 1 and not (adj[v] & ~x) for v in range(n)):
            continue
        remaining_edges = sum(not (x >> u & 1) and not (x >> v & 1) for u, v in edges)
        d = e - x.bit_count() - remaining_edges
        assert d >= 0
        result[d] += r ** remaining_edges
    return +result


def theorem_prediction(n, edges, r):
    """Predict first nonzero offset and its coefficient using local degrees only."""
    e = len(edges)
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    deg = [len(a) for a in adj]
    H = [v for v in range(n) if deg[v] >= 2]
    if e == 1:
        return None, None  # unique terminal length, center-free coincides
    if not H:
        return e - 1, 1  # matching, no positive kernel
    delta = min(deg[v] for v in H)
    offset = delta - 1
    if delta == 2:
        return offset, None  # K0648's degree-two edge terms also contribute
    leaves = sum(deg[v] == 1 and deg[next(iter(adj[v]))] >= 2 for v in range(n))
    isolated_edges = sum(deg[u] == deg[v] == 1 for u, v in edges)
    C = e - leaves - isolated_edges
    coefficient = int(e == delta)
    for v in H:
        if deg[v] != delta:
            continue
        a = sum(deg[w] == 1 for w in adj[v])
        exponent = C + a - delta
        assert exponent >= 0, (n, edges, v, exponent)
        coefficient += (r + 2) ** isolated_edges * r ** exponent * (r + 1) ** (leaves - a)
    return offset, coefficient


def audit():
    cases = checked_coefficients = matching = 0
    rng = Random(20261103)
    for n in range(2, 8):
        pairs = list(combinations(range(n), 2))
        if n <= 5:
            masks = range(1, 1 << len(pairs))
        elif n == 6:
            masks = list(range(1, 1 << len(pairs), 41))
        else:
            masks = [rng.randrange(1, 1 << len(pairs)) for _ in range(300)]
        for mask in masks:
            edges = [p for j, p in enumerate(pairs) if mask >> j & 1]
            for r in (1, 2, 5, 17):
                spectrum = direct_spectrum(n, edges, r)
                predicted, coefficient = theorem_prediction(n, edges, r)
                actual = min((d for d, c in spectrum.items() if d > 0 and c), default=None)
                assert predicted == actual, (n, edges, r, predicted, actual)
                if coefficient is not None:
                    assert spectrum.get(predicted, 0) == coefficient, (n, edges, r, coefficient, spectrum)
                    checked_coefficients += 1
                if all(sum(v in edge for edge in edges) <= 1 for v in range(n)):
                    matching += 1
                    if len(edges) >= 2:
                        assert spectrum == Counter({0: (r + 2) ** len(edges), len(edges) - 1: 1})
                cases += 1
    print(f"PASS cases={cases}, coefficient_checks={checked_coefficients}, matching_cases={matching}")


if __name__ == "__main__":
    audit()
