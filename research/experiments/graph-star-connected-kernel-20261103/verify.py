#!/usr/bin/env python3
"""Independent finite check for connected-component enumeration of fixed defect d.

No dependencies. Run: python verify.py
"""
from itertools import combinations
from random import Random


def neighbors(n, edges):
    a = [0] * n
    for u, v in edges:
        a[u] |= 1 << v
        a[v] |= 1 << u
    return a


def direct_coefficient(n, edges, q, defect):
    a = neighbors(n, edges)
    e = len(edges)
    r = q - 3
    N = 1 + n + r * e
    s = N - e
    ans = int(N - 1 == s + defect)
    for X in range(1 << n):
        if any(not (a[v] & ~X) for v in range(n) if X >> v & 1):
            continue
        remaining_edges = sum(not (X >> u & 1 or X >> v & 1) for u, v in edges)
        if N - X.bit_count() - remaining_edges == s + defect:
            ans += r ** remaining_edges
    return ans


def connected_component_coefficient(n, edges, q, defect):
    a = neighbors(n, edges)
    deg = [x.bit_count() for x in a]
    e = len(edges)
    r = q - 3
    N = 1 + n + r * e
    s = N - e
    if defect < 0:
        return 0
    h = sum(deg[u] == deg[v] == 1 for u, v in edges)
    L = sum(
        deg[(a[v] & -a[v]).bit_length() - 1] >= 2
        for v in range(n) if deg[v] == 1
    )
    C = e - L - h
    low = {v for v in range(n) if 2 <= deg[v] <= defect + 1}

    # Enumerate connected subsets by adding an adjacent low-degree vertex.
    seen = set()
    todo = [1 << v for v in low]
    components = []
    while todo:
        mask = todo.pop()
        if mask in seen:
            continue
        seen.add(mask)
        vs = [v for v in range(n) if mask >> v & 1]
        if len(vs) > 2 * defect:
            continue
        inside_edges = sum(bool(mask >> u & 1 and mask >> v & 1) for u, v in edges)
        cost = sum(deg[v] - 1 for v in vs) - inside_edges
        admissible = all(a[v] & ~mask for v in vs)
        if 1 <= cost <= defect and admissible:
            leaf_neighbors = sum(
                deg[w] == 1
                for v in vs for w in range(n) if a[v] >> w & 1
            )
            boundary = mask
            for v in vs:
                boundary |= a[v]
            components.append((mask, boundary, cost, len(vs), leaf_neighbors))
        if len(vs) < 2 * defect:
            nxt = set()
            for v in vs:
                nxt.update(
                    w for w in low
                    if a[v] >> w & 1 and not (mask >> w & 1)
                )
            todo.extend(mask | (1 << w) for w in nxt)

    # Select nonadjacent connected components; every union is counted once.
    ans = int(N - 1 == s + defect)

    def rec(start, forbidden, cost, size, leaves):
        nonlocal ans
        if cost == defect:
            exp = C + leaves - size - cost
            assert exp >= 0
            ans += (r + 2) ** h * r ** exp * (r + 1) ** (L - leaves)
            return
        for i in range(start, len(components)):
            cm, cb, cd, cs, cl = components[i]
            if cost + cd <= defect and not (cm & forbidden):
                rec(i + 1, forbidden | cb, cost + cd, size + cs, leaves + cl)

    rec(0, 0, 0, 0, 0)
    return ans


def main():
    checks = 0
    for n in range(1, 6):
        pairs = list(combinations(range(n), 2))
        for emask in range(1 << len(pairs)):
            edges = [p for i, p in enumerate(pairs) if emask >> i & 1]
            if not edges:
                continue
            for q in (4, 5, 8):
                for d in range(4):
                    lhs = connected_component_coefficient(n, edges, q, d)
                    rhs = direct_coefficient(n, edges, q, d)
                    assert lhs == rhs, (n, edges, q, d, lhs, rhs)
                    checks += 1
    rng = Random(20261103)
    for n in (6, 7, 8):
        pairs = list(combinations(range(n), 2))
        for _ in range(150):
            edges = [p for p in pairs if rng.randrange(4) == 0]
            if not edges:
                continue
            for q in (4, 6):
                for d in range(4):
                    lhs = connected_component_coefficient(n, edges, q, d)
                    rhs = direct_coefficient(n, edges, q, d)
                    assert lhs == rhs, (n, edges, q, d, lhs, rhs)
                    checks += 1
    print(f"PASS: {checks} coefficient comparisons, direct vs connected-kernel")


if __name__ == "__main__":
    main()
