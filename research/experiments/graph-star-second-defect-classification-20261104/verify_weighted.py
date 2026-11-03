"""Weighted defect-two coefficient audit against direct kernel enumeration.

Run: python verify_weighted.py (requires networkx).
Both sides use K0648's weight; this does NOT independently prove K0648.
"""
from itertools import combinations
import networkx as nx

def weight(G, B, q):
    r = q - 3
    e = G.number_of_edges()
    leaves = {v for v in G if G.degree(v) == 1 and any(G.degree(w) >= 2 for w in G[v])}
    L = len(leaves)
    h = sum(len(comp) == 2 for comp in nx.connected_components(G))
    C = e - L - h
    a = sum(any(w in B for w in G[v]) for v in leaves)
    return (r + 2)**h * r**(C + a - len(B) - 2) * (r + 1)**(L - a)

def direct(G):
    vertices = list(G)
    out = []
    for mask in range(1 << len(vertices)):
        B = frozenset(vertices[i] for i in range(len(vertices)) if mask & (1 << i))
        if any(G.degree(v) < 2 or not (set(G[v]) - B) for v in B):
            continue
        defect = sum(G.degree(v) - 1 for v in B) - G.subgraph(B).number_of_edges()
        if defect == 2:
            out.append(B)
    return out

def classified(G):
    D = {v for v in G if G.degree(v) == 2}
    T = {v for v in G if G.degree(v) == 3}
    result = [frozenset((v,)) for v in T]
    result += [frozenset((v, w)) for v, w in G.edges if {G.degree(v), G.degree(w)} == {2, 3}]
    for v in T:
        for a, b in combinations(set(G[v]) & D, 2):
            if not G.has_edge(a, b):
                result.append(frozenset((a, v, b)))
    A = [frozenset((v,)) for v in D] + [frozenset((v, w)) for v, w in G.edges if v in D and w in D]
    for I, J in combinations(A, 2):
        if I.isdisjoint(J) and all(not G.has_edge(v, w) for v in I for w in J):
            result.append(I | J)
    assert len(result) == len(set(result))
    return result

def main():
    checks = 0
    for i, G in enumerate(nx.graph_atlas_g()):
        expected, actual = direct(G), classified(G)
        for q in range(4, 10):
            x = sum(weight(G, B, q) for B in expected)
            y = sum(weight(G, B, q) for B in actual)
            if x != y:
                raise AssertionError((i, q, x, y))
            checks += 1
    print(f"PASS: {checks} graph/q pairs, exact weighted defect-two coefficients")

if __name__ == "__main__":
    main()
