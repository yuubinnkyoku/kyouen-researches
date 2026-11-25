#!/usr/bin/env python3
"""Independent generator (NetworkX) and residual induced-graph mex recurrence.
Requires networkx. Usage: python verify_tree_minima_networkx.py [max_n].
"""
import json, sys, pathlib
import networkx as nx
from functools import lru_cache
from collections import Counter

@lru_cache(None)
def grundy(adj):
    n = len(adj)
    if n == 0:
        return 0
    children = set()
    for v in range(n):
        kept = [u for u in range(n) if u != v and not (adj[v] & (1 << u))]
        index = {u:i for i,u in enumerate(kept)}
        sub = tuple(sum(1 << index[w] for w in kept if adj[u] & (1 << w)) for u in kept)
        children.add(grundy(sub))
    mex = 0
    while mex in children:
        mex += 1
    return mex

def main(max_n):
    stats, first = {}, {}
    for n in range(1, max_n+1):
        dist = Counter()
        count = 0
        for tree in [nx.empty_graph(1)] if n == 1 else nx.nonisomorphic_trees(n):
            adj = tuple(sum(1 << j for j in tree.neighbors(i)) for i in range(n))
            g = grundy(adj)
            count += 1
            dist[g] += 1
            first.setdefault(g, {'n':n, 'edges':[list(e) for e in tree.edges()]})
        stats[n] = {'total':count, 'nimbers':dict(sorted(dist.items()))}
        print(n, stats[n],flush=True)
    result = {'method':'NetworkX nonisomorphic_trees + residual induced-graph mex', 'stats':stats,'first':first}
    path = pathlib.Path(__file__).parent/'output/tree_minima_networkx.json'
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False))
    other = json.loads(path.with_name('tree_minima_independent.json').read_text())
    assert stats == {int(k):{'total':v['total'],'nimbers':{int(j):c for j,c in v['nimbers'].items()}} for k,v in other['stats'].items()}
    assert {k:v['n'] for k,v in first.items()} == {int(k):v['n'] for k,v in other['first'].items()}
    print('INDEPENDENT ENUMERATION AND SG DISTRIBUTIONS MATCH')

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv)>1 else 15)
