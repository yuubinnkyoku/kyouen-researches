"""Independent finite audit of K0648 component multiplicativity.

Enumerates all nonempty-edge unlabeled simple graphs of order <=7 from
NetworkX graph atlas and q=4..9. No polynomial root approximations.
"""
import networkx as nx


def polynomial(g, r):
    e = g.number_of_edges()
    high = [v for v in g if g.degree(v) >= 2]
    leaves = [v for v in g if g.degree(v) == 1]
    L = sum(any(g.degree(w) >= 2 for w in g[v]) for v in leaves)
    h = sum(
        len(c) == 2 and g.subgraph(c).number_of_edges() == 1
        for c in nx.connected_components(g)
    )
    C = e - L - h
    out = {}
    for mask in range(1 << len(high)):
        B = {v for i, v in enumerate(high) if mask >> i & 1}
        if any(all(w in B for w in g[v]) for v in B):
            continue
        a = sum(any(w in B for w in g[v]) for v in leaves)
        d = sum(g.degree(v) - 1 for v in B) - g.subgraph(B).number_of_edges()
        exponent = C + a - len(B) - d
        assert exponent >= 0
        out[d] = out.get(d, 0) + (r + 2) ** h * r ** exponent * (r + 1) ** (L - a)
    return out


def multiply(a, b):
    result = {}
    for i, x in a.items():
        for j, y in b.items():
            result[i + j] = result.get(i + j, 0) + x * y
    return result


def main():
    checked = 0
    for g in nx.graph_atlas_g():
        if not 1 <= len(g) <= 7 or g.number_of_edges() == 0:
            continue
        components = [g.subgraph(c).copy() for c in nx.connected_components(g)]
        for r in range(1, 7):
            product = {0: 1}
            for component in components:
                product = multiply(product, polynomial(component, r))
            direct = polynomial(g, r)
            assert product == direct, (list(g.edges()), r, product, direct)
            checked += 1
    print("PASS", checked, "graph/q conditions")


if __name__ == "__main__":
    main()
