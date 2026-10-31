#!/usr/bin/env python3
"""Independent set-based mex, all small graphs, unlabeled trees via leaf extension."""
from collections import Counter
from functools import lru_cache
from itertools import combinations

def values(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    @lru_cache(None)
    def solve(remaining):
        if not remaining:
            return (0, 1)
        gs, hs = set(), set()
        for v in remaining:
            g, h = solve(remaining.difference(adj[v] | {v}))
            gs.add(g)
            hs.add(h)
        g = h = 0
        while g in gs:
            g += 1
        while h in hs:
            h += 1
        return g, h
    return solve(frozenset(range(n)))

def connected(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    seen = {0}
    while True:
        nxt = seen | set().union(*(adj[v] for v in seen))
        if nxt == seen:
            return len(seen) == n
        seen = nxt

def tree_code(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    remaining = set(range(n))
    while len(remaining) > 2:
        leaves = {v for v in remaining if len(adj[v] & remaining) <= 1}
        remaining -= leaves
    def rooted(v, parent):
        return "(" + "".join(sorted(rooted(u, v) for u in adj[v]
                                   if u != parent)) + ")"
    if len(remaining) == 1:
        return rooted(next(iter(remaining)), -1)
    a, b = sorted(remaining)
    return "[" + "".join(sorted((rooted(a, b), rooted(b, a)))) + "]"

def audit_graphs():
    expected = [(1,1,0,0), (2,1,0,0), (8,4,0,0),
                (64,38,0,0), (1024,728,0,0),
                (32768,26704,150,60)]
    for n in range(1, 7):
        pairs = list(combinations(range(n), 2))
        total = con = bad = badcon = 0
        for bits in range(1 << len(pairs)):
            edges = [edge for i, edge in enumerate(pairs) if bits >> i & 1]
            g, h = values(n, edges)
            total += 1
            iscon = connected(n, edges)
            con += iscon
            if h != (1-g if g < 2 else g):
                bad += 1
                badcon += iscon
                assert n == 6 and (g,h) == (0,0)
                deg = Counter(v for e in edges for v in e)
                if iscon:
                    assert len(edges) == 6 and all(deg[v] == 2 for v in range(6))
                else:
                    assert len(edges) == 4 and sorted(deg.values()) == [1,1,1,1,2,2]
        assert (total,con,bad,badcon) == expected[n-1]
        print("graphs", n, total, con, bad, badcon)

def audit_trees():
    trees = {tree_code(1, []): []}
    expected = [1,1,1,2,3,6,11,23]
    for n in range(1, 9):
        if n > 1:
            new = {}
            for edges in trees.values():
                for v in range(n-1):
                    e = edges + [(v,n-1)]
                    new.setdefault(tree_code(n,e),e)
            trees = new
        assert len(trees) == expected[n-1]
        bad = []
        for edges in trees.values():
            g,h = values(n,edges)
            if h != (1-g if g < 2 else g):
                bad.append((edges,g,h))
        if n < 8:
            assert not bad
        else:
            assert len(bad) == 3
            assert Counter((g,h) for _,g,h in bad) == {(1,4):2,(4,1):1}
            for edges,g,h in bad:
                print("tree witness",edges,"g",g,"h",h)
        print("trees",n,len(trees),len(bad))

if __name__ == "__main__":
    audit_graphs()
    audit_trees()
    cycle = [(i, (i+1)%6) for i in range(6)]
    assert values(6, cycle) == (0,0)
    assert values(8, cycle + [(0,6),(0,7)]) == (0,0)
    print("connected infinite-family bases: C6 and C6+2 leaves verified")
