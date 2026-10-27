#!/usr/bin/env python3
"""Independent NetworkX Atlas generation and set-recursion audit (optional)."""
from functools import lru_cache
from itertools import combinations

import networkx as nx


def grundy(g):
    @lru_cache(None)
    def recurse(remaining):
        options = set()
        for v in remaining:
            child = remaining - ({v} | set(g.neighbors(v)))
            options.add(recurse(frozenset(child)))
        answer = 0
        while answer in options:
            answer += 1
        return answer

    return recurse(frozenset(g.nodes))


def main():
    count = 0
    values = set()
    for graph in nx.graph_atlas_g():
        vertices = list(graph.nodes)
        if len(vertices) < 2:
            continue
        if not any(all(u in pair or v in pair for u, v in graph.edges)
                   for pair in combinations(vertices, 2)):
            continue
        result = grundy(graph)
        assert result <= 3, (vertices, list(graph.edges), result)
        count += 1
        values.add(result)
    assert count == 130, count
    assert values == {0, 1, 2, 3}, values
    print('NetworkX Atlas nonisomorphic graphs with 2<=n<=7, vertex cover<=2:', count)
    print('All independently generated values:', sorted(values))


if __name__ == '__main__':
    main()
