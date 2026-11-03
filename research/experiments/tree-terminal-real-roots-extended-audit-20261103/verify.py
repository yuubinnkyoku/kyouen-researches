"""Exact finite audit of branching trees with 9 or 10 vertices (not an all-n theorem)."""
import networkx as nx
import sympy as sp

u = sp.symbols("u")
counts = {}
for n in (9, 10):
    trees = [g for g in nx.generators.nonisomorphic_trees(n)
             if max(dict(g.degree()).values()) >= 3]
    counts[n] = len(trees)
    for gi, g in enumerate(trees):
        leaves = [v for v in g if g.degree(v) == 1]
        L = len(leaves)
        C = g.number_of_edges() - L
        H = [v for v in g if g.degree(v) >= 2]
        terms = []
        for mask in range(1 << len(H)):
            B = {v for i, v in enumerate(H) if (mask >> i) & 1}
            if any(all(w in B for w in g[v]) for v in B):
                continue
            a = sum(any(w in B for w in g[v]) for v in leaves)
            d = sum(g.degree(v) - 1 for v in B) - g.subgraph(B).number_of_edges()
            terms.append((C + a - len(B) - d, L - a, d))
        for r in range(1, 6):
            p = sp.Poly(sum(r**x * (r+1)**y * u**d for x, y, d in terms), u)
            assert p.degree() >= 2
            assert p.count_roots(-sp.oo, 0) < p.degree(), (n, gi, r, p)
    print(n, len(trees))
print("Total exact checks:", sum(counts.values()) * 5)
