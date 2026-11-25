"""Finite independent audit of the degree-two first coefficient (requires networkx).

Run: python verify.py
Enumerates all admissible kernels directly, without assuming their shape.
"""
import networkx as nx


def verify(g, q):
    e = g.number_of_edges()
    if not e:
        return
    r = q - 3
    deg = dict(g.degree())
    h = sum(len(c) == 2 and g.subgraph(c).number_of_edges() == 1
            for c in nx.connected_components(g))
    leaves = [v for v in g if deg[v] == 1 and
              any(deg[w] >= 2 for w in g.neighbors(v))]
    L = len(leaves)
    C = e - L - h
    H = [v for v in g if deg[v] >= 2]
    D = {v for v in H if deg[v] == 2}
    edges = list(g.edges())

    def weight(B):
        a = sum(any(w in B for w in g.neighbors(v)) for v in leaves)
        return (r + 2)**h * r**(C + a - len(B) - 1) * (r + 1)**(L - a)

    direct = count = 0
    for mask in range(1 << len(H)):
        B = {H[i] for i in range(len(H)) if mask >> i & 1}
        if any(all(w in B for w in g.neighbors(v)) for v in B):
            continue
        d = sum(deg[v] - 1 for v in B) - sum(
            u in B and v in B for u, v in edges)
        if d == 1:
            direct += weight(B)
            count += 1

    candidates = [{v} for v in D] + [
        {u, v} for u, v in edges if u in D and v in D]
    expected = sum(map(weight, candidates))
    assert (direct, count) == (expected, len(candidates)), (
        list(edges), q, direct, expected, count, len(candidates))


if __name__ == "__main__":
    graphs = [g for g in nx.graph_atlas_g() if g.number_of_edges()]
    for g in graphs:
        for q in range(4, 10):
            verify(g, q)
    print(f"PASS: {len(graphs)} graphs, {len(graphs)*6} conditions, q=4..9")
