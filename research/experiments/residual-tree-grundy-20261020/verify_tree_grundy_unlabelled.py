#!/usr/bin/env python3
"""Independent check via unlabelled trees and occupied-subset Grundy DP."""
from functools import lru_cache
import networkx as nx

for n in range(1,9):
    hist = {}
    labelled_hist = {}
    g4 = []
    for graph in nx.generators.nonisomorphic_trees(n):
        g = nx.convert_node_labels_to_integers(graph)
        adjacency = [set(g.neighbors(v)) for v in range(n)]
        @lru_cache(None)
        def grundy(occupied):
            moves = set()
            for v in range(n):
                if (occupied >> v) & 1:
                    continue
                if any((occupied >> u) & 1 for u in adjacency[v]):
                    continue
                moves.add(grundy(occupied | (1 << v)))
            x = 0
            while x in moves:
                x += 1
            return x
        nim = grundy(0)
        hist[nim] = hist.get(nim, 0) + 1
        # Automorphism count gives the exact number of labelled copies.
        aut = sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(g,g).isomorphisms_iter())
        multiplicity = __import__('math').factorial(n) // aut
        labelled_hist[nim] = labelled_hist.get(nim, 0) + multiplicity
        if nim == 4:
            g4.append((list(g.edges()), aut, multiplicity))
    print(f'n={n} unlabelled={sum(hist.values())} histogram={dict(sorted(hist.items()))}')
    print(f'    labelled={sum(labelled_hist.values())} histogram={dict(sorted(labelled_hist.items()))}')
    if g4:
        print(f'    g4_tree_types={len(g4)} witnesses={g4}')
