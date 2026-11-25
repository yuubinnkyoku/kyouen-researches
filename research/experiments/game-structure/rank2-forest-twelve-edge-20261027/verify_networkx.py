#!/usr/bin/env python3
"""Independent generation using networkx.nonisomorphic_trees (optional dependency)."""
from collections import Counter
from functools import lru_cache
import networkx as nx

EXPECTED = {
    1:(0,1), 2:(0,0,1), 3:(1,1), 4:(0,0,1,2),
    5:(2,4), 6:(1,2,5,3), 7:(11,11,0,0,1),
    8:(6,7,14,18,2), 9:(41,42,7,4,8,4),
    10:(35,36,72,66,11,14,1),
    11:(173,174,49,62,43,50),
    12:(195,209,336,340,122,85,5,9),
}

def nimber(graph):
    n = len(graph)
    adj = [sum(1 << v for v in graph.neighbors(i)) for i in range(n)]
    @lru_cache(None)
    def rec(mask):
        children = {rec(mask & ~(adj[v] | (1 << v)))
                    for v in range(n) if mask & (1 << v)}
        g = 0
        while g in children:
            g += 1
        return g
    return rec((1 << n) - 1)

def main():
    for e in range(1, 13):
        hist = Counter(nimber(g) for g in nx.nonisomorphic_trees(e + 1))
        got = tuple(hist.get(i, 0) for i in range(max(hist) + 1))
        assert got == EXPECTED[e], (e, got)
        print(e, got, flush=True)

if __name__ == "__main__":
    main()
