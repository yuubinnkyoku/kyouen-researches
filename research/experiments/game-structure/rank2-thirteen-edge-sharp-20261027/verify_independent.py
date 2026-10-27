"""Independent NetworkX generators for two disjoint 13-edge graph families.

Graph Atlas supplies all connected 13-edge graphs on 6 or 7 vertices.
nonisomorphic_trees supplies all connected 13-edge graphs on 14 vertices.
The Grundy recursion is independently implemented over available vertices.
Requires NetworkX (not a project runtime dependency).
"""
from collections import Counter
from functools import cache
import networkx as nx


def nimber(graph):
    nodes = list(graph)
    index = {v: i for i, v in enumerate(nodes)}
    adj = [sum(1 << index[w] for w in graph.neighbors(v)) for v in nodes]

    @cache
    def rec(available):
        seen = set()
        rest = available
        while rest:
            bit = rest & -rest
            rest ^= bit
            v = bit.bit_length() - 1
            seen.add(rec(available & ~(bit | adj[v])))
        ans = 0
        while ans in seen:
            ans += 1
        return ans

    return rec((1 << len(nodes)) - 1)


atlas = Counter((len(g), nimber(g)) for g in nx.graph_atlas_g()
                if g.number_of_edges() == 13 and nx.is_connected(g))
assert {z: c for (n, z), c in atlas.items() if n == 6} == {2: 2}
assert {z: c for (n, z), c in atlas.items() if n == 7} == {0: 23, 1: 5, 2: 8, 3: 59}
print("Graph Atlas:", dict(sorted(atlas.items())))

trees = Counter(nimber(g) for g in nx.nonisomorphic_trees(14))
assert trees == {0: 850, 1: 859, 2: 434, 3: 370, 4: 321, 5: 293, 6: 15, 7: 17}
print("14-vertex trees:", dict(sorted(trees.items())))
