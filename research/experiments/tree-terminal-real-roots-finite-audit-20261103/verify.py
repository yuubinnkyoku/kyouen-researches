"""Finite exact audit: branching trees of order <=8, q=4..8."""
import networkx as nx
import sympy as sp

u = sp.symbols("u")
counts = {}
for n in range(4, 9):
    trees = list(nx.generators.nonisomorphic_trees(n))
    branching = [g for g in trees if max(dict(g.degree()).values()) >= 3]
    counts[n] = len(branching)
    for r in range(1, 6):
        for g in branching:
            e = g.number_of_edges()
            leaves = [v for v in g if g.degree(v) == 1]
            L = len(leaves)
            C = e - L
            H = [v for v in g if g.degree(v) >= 2]
            p = 0
            for mask in range(1 << len(H)):
                B = {v for i, v in enumerate(H) if mask >> i & 1}
                if any(all(w in B for w in g[v]) for v in B):
                    continue
                a = sum(any(w in B for w in g[v]) for v in leaves)
                d = sum(g.degree(v) - 1 for v in B) - g.subgraph(B).number_of_edges()
                p += r ** (C + a - len(B) - d) * (r + 1) ** (L - a) * u ** d
            p = sp.Poly(p, u)
            assert p.degree() >= 2
            assert p.count_roots(-sp.oo, 0) < p.degree(), (n, r, p)
print(counts, "total checks", sum(counts.values()) * 5)
