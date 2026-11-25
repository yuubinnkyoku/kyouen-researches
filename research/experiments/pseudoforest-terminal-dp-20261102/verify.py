#!/usr/bin/env python3
"""Independent exact checks for the pseudoforest terminal polynomial."""
from collections import defaultdict
from itertools import combinations, product


def add(*polys):
    out = defaultdict(int)
    for poly in polys:
        for k, v in poly.items():
            out[k] += v
    return {k: v for k, v in out.items() if v}


def neg(poly):
    return {k: -v for k, v in poly.items()}


def mul(a, b):
    out = defaultdict(int)
    for i, x in a.items():
        for j, y in b.items():
            out[i + j] += x * y
    return {k: v for k, v in out.items() if v}


def prod(polys):
    ans = {0: 1}
    for p in polys:
        ans = mul(ans, p)
    return ans


def shift(poly, exponent, coefficient=1):
    return {k + exponent: coefficient * v for k, v in poly.items()}


def component_nodes(adj):
    seen = set()
    for start in range(len(adj)):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        part = []
        while stack:
            v = stack.pop()
            part.append(v)
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        yield part


def terminal_dp(n, edges, r):
    """K0602 P_G(u), for any pseudoforest; returns {stone_count: count}."""
    adj = [set() for _ in range(n)]
    for v, w in edges:
        assert v != w and w not in adj[v]
        adj[v].add(w)
        adj[w].add(v)
    z = {-1: r}
    inv = {-1: 1}

    def rooted(v, parent, cycle):
        children = [rooted(w, v, cycle) for w in adj[v]
                    if w != parent and w not in cycle]
        a = prod([add(mul(z, x), y, h) for x, y, h in children])
        all_ab = prod([add(x, y) for x, y, _ in children])
        all_b = prod([y for _, y, _ in children])
        b = mul(inv, add(all_ab, neg(all_b)))
        c = mul(inv, all_b)
        return a, b, c

    def cyclic_order(cycle):
        first = min(cycle)
        order = [first]
        prev = -1
        while len(order) < len(cycle):
            v = order[-1]
            candidates = [w for w in adj[v] if w in cycle and w != prev]
            nxt = min(candidates)
            assert nxt not in order
            order.append(nxt)
            prev = v
        assert first in adj[order[-1]]
        return order

    def cycle_poly(cycle):
        order = cyclic_order(cycle)
        k = len(order)
        abc = [rooted(v, -1, cycle) for v in order]

        def factor(i, left, mid, right):
            a, b, c = abc[i]
            if mid == 0:
                return mul(a, z) if right == 0 else a
            return add(b, c) if left == 0 or right == 0 else b

        total = {}
        for x0, x1 in product((0, 1), repeat=2):
            dp = {(x0, x1): {0: 1}}
            for i in range(1, k - 1):
                nxt_dp = {}
                for (left, mid), weight in dp.items():
                    for right in (0, 1):
                        pair = (mid, right)
                        term = mul(weight, factor(i, left, mid, right))
                        nxt_dp[pair] = add(nxt_dp.get(pair, {}), term)
                dp = nxt_dp
            for (left, mid), weight in dp.items():
                term = mul(weight, factor(k - 1, left, mid, x0))
                term = mul(term, factor(0, mid, x0, x1))
                total = add(total, term)
        return total

    total = {0: 1}
    for part in component_nodes(adj):
        edges_in_part = sum(len(adj[v]) for v in part) // 2
        if edges_in_part == len(part) - 1:
            a, b, _ = rooted(part[0], -1, set())
            local = add(a, b)
        else:
            assert edges_in_part == len(part), "not a pseudoforest"
            degree = {v: len(adj[v]) for v in part}
            leaves = [v for v in part if degree[v] == 1]
            while leaves:
                v = leaves.pop()
                degree[v] = 0
                for w in adj[v]:
                    if degree[w] > 0:
                        degree[w] -= 1
                        if degree[w] == 1:
                            leaves.append(w)
            cycle = {v for v in part if degree[v] > 0}
            assert len(cycle) >= 3
            local = cycle_poly(cycle)
        total = mul(total, local)
    N = 1 + n + r * len(edges)
    return add({N - 1: 1}, shift(total, N))


def direct_graph(n, edges, r):
    nbr = [0] * n
    for a, b in edges:
        nbr[a] |= 1 << b
        nbr[b] |= 1 << a
    N = 1 + n + r * len(edges)
    out = defaultdict(int)
    out[N - 1] += 1
    allbits = (1 << n) - 1
    for X in range(1 << n):
        kept = allbits ^ X
        if any(not (nbr[v] & kept) for v in range(n) if X >> v & 1):
            continue
        e0 = sum(not (X >> a & 1) and not (X >> b & 1) for a, b in edges)
        out[N - X.bit_count() - e0] += r ** e0
    return dict(out)


def direct_hyperedges(n, edges, r):
    N = 1 + n + r * len(edges)
    assert N <= 18
    forb = []
    for i, (a, b) in enumerate(edges):
        mask = 1 | (1 << (1 + a)) | (1 << (1 + b))
        for j in range(r):
            mask |= 1 << (1 + n + r * i + j)
        forb.append(mask)
    counts = defaultdict(int)
    for s in range(1 << N):
        if any(s & h == h for h in forb):
            continue
        maximal = True
        for i in range(N):
            if not (s >> i & 1) and all(((s | (1 << i)) & h) != h for h in forb):
                maximal = False
                break
        if maximal:
            counts[s.bit_count()] += 1
    return dict(counts)


def is_pseudoforest(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return all(sum(len(adj[v]) for v in part) // 2 <= len(part)
               for part in component_nodes(adj))


def main():
    checked = 0
    hyperchecked = 0
    hypermasks = 0
    for n in range(2, 7):
        pairs = list(combinations(range(n), 2))
        for edge_mask in range(1 << len(pairs)):
            edges = [p for i, p in enumerate(pairs) if edge_mask >> i & 1]
            if not edges or (n == 6 and edge_mask % 11 != 0) or not is_pseudoforest(n, edges):
                continue
            for r in (1, 2, 3):
                got = terminal_dp(n, edges, r)
                expect = direct_graph(n, edges, r)
                assert got == expect, (n, edges, r, got, expect)
                checked += 1
                N = 1 + n + r * len(edges)
                if n <= 5 and N <= 15 and hyperchecked < 90:
                    hyp = direct_hyperedges(n, edges, r)
                    assert got == hyp, (n, edges, r, got, hyp)
                    hyperchecked += 1
                    hypermasks += 1 << N
    for r in (1, 2, 3):
        edges = [(0, 1), (1, 2), (2, 0), (2, 3), (4, 5)]
        assert terminal_dp(7, edges, r) == direct_graph(7, edges, r)
    for r in (1, 2):
        example = terminal_dp(4, [(0, 1), (1, 2), (2, 0), (0, 3)], r)
        print(f"triangle + leaf, q={r+3}: {sorted(example.items())}")
    print(f"PASS graph cases={checked}, hypergraph cases={hyperchecked}, hypergraph masks={hypermasks}")


if __name__ == '__main__':
    main()
