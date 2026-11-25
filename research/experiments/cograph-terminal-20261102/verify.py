#!/usr/bin/env python3
"""Independent exact audit of cotree terminal polynomial for K0602 graph-star games.

Only Python standard library; run `python verify.py`.
"""
from collections import Counter
from itertools import combinations
from random import Random


def add(a, b, sign=1):
    out = Counter(a)
    for key, value in b.items():
        out[key] += sign * value
    return +out


def combine(a, b, join=False):
    out = Counter()
    for (s, e), x in a.items():
        for (t, f), y in b.items():
            out[s+t, e+f+(s*t if join else 0)] += x*y
    return +out


def cotree_tables(adj):
    """Return (all-subset table, dominating-subset table), or None for noncograph."""
    n = len(adj)

    def components(mask, complement):
        unseen = mask
        groups = []
        while unseen:
            start = unseen & -unseen
            frontier = start
            group = start
            unseen ^= start
            while frontier:
                bit = frontier & -frontier
                frontier ^= bit
                v = bit.bit_length()-1
                near = ((mask & ~(1 << v) & ~adj[v]) if complement
                        else (mask & adj[v])) & unseen
                unseen ^= near
                frontier |= near
                group |= near
            groups.append(group)
        return groups

    def solve(mask):
        if mask.bit_count() == 1:
            return Counter({(0, 0): 1, (1, 0): 1}), Counter({(1, 0): 1})
        groups = components(mask, False)
        joined = False
        if len(groups) == 1:
            groups = components(mask, True)
            if len(groups) == 1:
                return None
            joined = True
        first = solve(groups[0])
        if first is None:
            return None
        a, d = first
        for group in groups[1:]:
            other = solve(group)
            if other is None:
                return None
            b, f = other
            if joined:
                # Nonempty choices from both sides dominate the entire join.
                cross = combine(add(a, {(0, 0): 1}, -1),
                                add(b, {(0, 0): 1}, -1), True)
                a, d = add(add(add(a, b), cross), {(0, 0): 1}, -1), add(add(d, f), cross)
            else:
                a, d = combine(a, b), combine(d, f)
        return a, d

    return solve((1 << n)-1)


def from_tables(adj, tables, r):
    n = len(adj)
    e = sum(x.bit_count() for x in adj)//2
    N = 1+n+r*e
    out = Counter({N-1: 1})
    for (a, er), multiplicity in tables[1].items():
        out[N-n+a-er] += multiplicity * r**er
    return +out


def brute_deleted_sets(adj, r):
    n = len(adj)
    E = [(a, b) for a in range(n) for b in range(a+1, n) if adj[a] >> b & 1]
    N = 1+n+r*len(E)
    out = Counter({N-1: 1})
    for R in range(1 << n):
        if any(not (adj[v] & R) for v in range(n) if not (R >> v & 1)):
            continue
        er = sum((R >> a & 1) and (R >> b & 1) for a,b in E)
        out[N-n+R.bit_count()-er] += r**er
    return +out


def brute_forbidden_hyperedges(adj, r):
    n = len(adj)
    E = [(a, b) for a in range(n) for b in range(a+1, n) if adj[a] >> b & 1]
    N = 1+n+r*len(E)
    F = [(1 << 0) | (1 << (a+1)) | (1 << (b+1)) |
         sum(1 << (1+n+r*j+h) for h in range(r))
         for j,(a,b) in enumerate(E)]
    out = Counter()
    for s in range(1 << N):
        if any(s & f == f for f in F):
            continue
        if all(any((s | (1 << p)) & f == f for f in F)
               for p in range(N) if not (s >> p & 1)):
            out[s.bit_count()] += 1
    return +out, 1 << N


def adjacency(n, edge_mask):
    adj = [0]*n
    for j, (a,b) in enumerate(combinations(range(n),2)):
        if edge_mask >> j & 1:
            adj[a] |= 1 << b
            adj[b] |= 1 << a
    return adj


def random_cograph(n, rng):
    # Independently generate a binary union/join construction, then relabel.
    def rec(vertices):
        if len(vertices) == 1:
            return set()
        rng.shuffle(vertices)
        split = rng.randrange(1, len(vertices))
        L, R = vertices[:split], vertices[split:]
        out = rec(L) | rec(R)
        if rng.randrange(2):
            out.update((min(a,b), max(a,b)) for a in L for b in R)
        return out
    edges = rec(list(range(n)))
    adj = [0]*n
    for a,b in edges:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    return adj


def join_adj(a, b):
    n = len(a)
    return [x | (((1 << len(b))-1) << n) for x in a] + \
           [x << n | ((1 << n)-1) for x in b]


def union_adj(a, b):
    return a + [x << len(a) for x in b]


def biclique(m):
    return [sum(1 << j for j in range(m,2*m)) for _ in range(m)] + \
           [sum(1 << j for j in range(m)) for _ in range(m)]


def run():
    checked = 0
    cographs = 0
    for n in range(1,7):
        for bits in range(1 << (n*(n-1)//2)):
            adj = adjacency(n,bits)
            tables = cotree_tables(adj)
            if tables is None:
                continue
            cographs += 1
            assert sum(tables[0].values()) == (1 << n)
            assert tables[0][(0,0)] == 1
            if bits == 0:
                continue # K0602 requires at least one edge.
            for r in (1,2):
                fast = from_tables(adj,tables,r)
                direct = brute_deleted_sets(adj,r)
                assert fast == direct, (n,bits,r,fast,direct)
                checked += 1
    print(f"All labeled graphs n<=6: {cographs} cographs, {checked} q4/q5 comparisons; zero mismatches")

    rng = Random(20261102)
    sampled = 0
    for n, repetitions in ((7, 75), (8, 75), (9, 50), (10, 30), (12, 15), (16, 4)):
        for _ in range(repetitions):
            adj = random_cograph(n,rng)
            if not any(adj):
                continue
            tables = cotree_tables(adj)
            assert tables is not None
            for r in (1,2,3):
                assert from_tables(adj,tables,r) == brute_deleted_sets(adj,r)
                sampled += 1
    print(f"Seeded larger cotrees: {sampled} direct deleted-set comparisons; zero mismatches")

    hcases = subsets = 0
    for n in range(2,7):
        for bits in range(1 << (n*(n-1)//2)):
            adj = adjacency(n,bits)
            if not any(adj):
                continue
            tables = cotree_tables(adj)
            if tables is None:
                continue
            for r in (1,2):
                N = 1+n+r*sum(x.bit_count() for x in adj)//2
                if N > 12 or (n >= 5 and (bits * 97 + r * 17 + n) % (11 if n == 5 else 75)):
                    continue
                a = from_tables(adj,tables,r)
                b, count = brute_forbidden_hyperedges(adj,r)
                assert a == b, (n,bits,r,a,b)
                hcases += 1
                subsets += count
    print(f"Direct forbidden-hyperedge audits: {hcases} conditions, {subsets} point subsets; zero mismatches")

    for m in (1,2,3):
        a = union_adj(biclique(m), biclique(m))
        g = join_adj(a,a)
        tables = cotree_tables(g)
        assert tables is not None
        if m <= 2:
            assert from_tables(g,tables,1) == brute_deleted_sets(g,1)
        p = from_tables(g,tables,1)
        print(f"G_m=(2K_{{m,m}}) join (2K_{{m,m}}), m={m}: vertices={len(g)}, edges={sum(x.bit_count() for x in g)//2}, terminal-count={sum(p.values())}, distinct-sizes={len(p)}")


if __name__ == "__main__":
    run()
