"""Independent cross-check using NetworkX graph atlas and Node Kayles recurrence.

Atlas is a catalog of unlabeled graphs through 7 vertices.  For each
unlabeled graph, independently calculate the Grundy value on the remaining
available vertices; weight it by n!/|Aut(G)| to reconstruct labeled totals.
"""
import collections
import functools
import itertools
import json
import math
import networkx as nx


def grundy_from_available(adj):
    n = len(adj)
    @functools.lru_cache(None)
    def rec(available):
        child_values = set()
        for v in range(n):
            if available & (1 << v):
                child_values.add(rec(available & ~(adj[v] | (1 << v))))
        g = 0
        while g in child_values:
            g += 1
        return g
    return rec((1 << n) - 1), rec


def aut_count(adj):
    n = len(adj)
    count = 0
    for perm in itertools.permutations(range(n)):
        if all(bool(adj[i] & (1 << j)) == bool(adj[perm[i]] & (1 << perm[j]))
               for i in range(n) for j in range(i + 1, n)):
            count += 1
    return count


def main():
    hist = {n: collections.Counter() for n in range(8)}
    unlabeled = {n: collections.Counter() for n in range(8)}
    witnesses = []
    for G in nx.graph_atlas_g():
        n = len(G)
        adj = [0] * n
        for a, b in G.edges():
            adj[a] |= 1 << b
            adj[b] |= 1 << a
        g, rec = grundy_from_available(adj)
        weight = math.factorial(n) // aut_count(adj)
        hist[n][g] += weight
        unlabeled[n][g] += 1
        if n == 7 and g == 4:
            witnesses.append({'edges': [list(e) for e in sorted(G.edges())], 'aut': math.factorial(n) // weight})
    result = {'labeled_hist': {str(n): dict(sorted(hist[n].items())) for n in hist},
              'unlabeled_hist': {str(n): dict(sorted(unlabeled[n].items())) for n in unlabeled},
              'seven_g4_unlabeled': len(witnesses), 'seven_g4_witnesses': witnesses}
    for n in range(8):
        assert sum(hist[n].values()) == 1 << (n * (n - 1) // 2)
    assert len(witnesses) == 26
    assert all(len(x['edges']) >= 7 for x in witnesses)
    assert all(len(x['edges']) <= 12 for x in witnesses)
    assert all(nx.is_connected(nx.Graph([(v, v) for v in range(7)] + [tuple(e) for e in x['edges']])) for x in witnesses)
    print(json.dumps({'labeled_hist': result['labeled_hist'],
                      'unlabeled_hist': result['unlabeled_hist'],
                      'seven_g4_unlabeled': len(witnesses)}, indent=2))

if __name__ == '__main__':
    main()
