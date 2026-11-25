"""Independent exhaustive check of the defect-two admissible-kernel classification.

Requires networkx; run: python verify.py
"""
from itertools import combinations
import networkx as nx


def direct(G):
    vertices = list(G)
    result = set()
    for mask in range(1, 1 << len(vertices)):
        B = frozenset(vertices[i] for i in range(len(vertices)) if mask >> i & 1)
        # K0648 kernels use only degree >= 2 vertices.
        if any(G.degree(v) < 2 for v in B):
            continue
        if any(not (set(G[v]) - B) for v in B):
            continue
        defect = 0
        for comp in nx.connected_components(G.subgraph(B)):
            H = G.subgraph(comp)
            boundary = sum(w not in B for v in comp for w in G[v])
            beta = H.number_of_edges() - len(comp) + 1
            defect += boundary - 1 + beta
        if defect == 2:
            result.add(B)
    return result


def classified(G):
    D = {v for v in G if G.degree(v) == 2}
    T = {v for v in G if G.degree(v) == 3}
    ans = {frozenset([v]) for v in T}
    ans |= {frozenset([v, w]) for v, w in G.edges
            if {G.degree(v), G.degree(w)} == {2, 3}}
    for center in T:
        for a, b in combinations(set(G[center]) & D, 2):
            if not G.has_edge(a, b):
                ans.add(frozenset((a, center, b)))
    A = [frozenset([v]) for v in D]
    A += [frozenset((v, w)) for v, w in G.edges if v in D and w in D]
    for I, J in combinations(A, 2):
        if I.isdisjoint(J) and not any(G.has_edge(v, w) for v in I for w in J):
            ans.add(I | J)
    return ans


def main():
    atlas = nx.graph_atlas_g()
    for i, G in enumerate(atlas):
        expected, actual = direct(G), classified(G)
        if expected != actual:
            raise AssertionError((i, expected - actual, actual - expected))
    print(f"PASS: {len(atlas)} nonisomorphic graphs, order <= 7; exact kernel-set equality")


if __name__ == "__main__":
    main()
