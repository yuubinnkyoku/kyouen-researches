#!/usr/bin/env python3
"""Independent checks for K0648: local leaf-core formula vs domination and hyperedges."""
from collections import Counter
from itertools import combinations


def local(n, edges, r):
    e = len(edges)
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    deg = [len(a) for a in adj]
    H = [v for v in range(n) if deg[v] >= 2]
    L = sum(deg[v] == 1 and deg[next(iter(adj[v]))] >= 2 for v in range(n))
    h = sum(deg[u] == deg[v] == 1 for u, v in edges)
    C = e - L - h
    out = Counter({e - 1: 1})  # unique center-free terminal
    for mask in range(1 << len(H)):
        B = {v for i, v in enumerate(H) if mask >> i & 1}
        if any(not (adj[v] - B) for v in B):
            continue
        d = sum(deg[v] - 1 for v in B) - sum(u in B and v in B for u, v in edges)
        assert len(B) <= 2 * d
        a = sum(deg[w] == 1 for v in B for w in adj[v])
        exponent = C + a - len(B) - d
        assert exponent >= 0
        out[d] += r ** exponent * (r + 1) ** (L - a) * (r + 2) ** h
    return +out, deg


def dominating(n, edges, r):
    e = len(edges)
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    out = Counter({e - 1: 1})
    for mask in range(1 << n):
        X = {v for v in range(n) if mask >> v & 1}
        if any(not (adj[v] - X) for v in X):
            continue
        remaining = sum(u not in X and v not in X for u, v in edges)
        out[e - len(X) - remaining] += r ** remaining
    return +out


def hyperedges(n, edges, r):
    """Enumerate all size-(s+1) subsets and test maximality directly."""
    e = len(edges)
    N = 1 + n + r * e
    target = N - e + 1
    forbidden = []
    for j, (u, v) in enumerate(edges):
        edge = 1 | (1 << (u + 1)) | (1 << (v + 1))
        for k in range(r):
            edge |= 1 << (1 + n + j * r + k)
        forbidden.append(edge)
    count = 0
    for positions in combinations(range(N), target):
        state = sum(1 << v for v in positions)
        if any(state & edge == edge for edge in forbidden):
            continue
        if all(any((state | (1 << j)) & edge == edge for edge in forbidden)
               for j in range(N) if not (state >> j & 1)):
            count += 1
    return count


def audit():
    full = direct = gaps = 0
    for n in range(2, 7):
        pairs = list(combinations(range(n), 2))
        masks = range(1 << len(pairs)) if n <= 5 else range(0, 1 << len(pairs), 37)
        for mask in masks:
            edges = [p for j, p in enumerate(pairs) if mask >> j & 1]
            if not edges:
                continue
            for r in (1, 2, 3):
                got, deg = local(n, edges, r)
                expected = dominating(n, edges, r)
                assert got == expected, (n, edges, r, got, expected)
                full += 1
                if len(edges) >= 3:
                    assert (got.get(1, 0) > 0) == (2 in deg)
                    gaps += 1
            if n <= 4 and len(edges) <= 4 and len(edges) >= 2:
                for r in (1, 2):
                    got, _ = local(n, edges, r)
                    assert hyperedges(n, edges, r) == got.get(1, 0)
                    direct += 1
    print(f"PASS full-spectrum={full}; gap-criterion={gaps}; forbidden-hyperedge={direct}")


if __name__ == "__main__":
    audit()
