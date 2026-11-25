#!/usr/bin/env python3
"""Independent finite checks for K0647; no external packages needed."""
from collections import Counter
from itertools import product


def edges_from_prufer(code, n):
    degree = [1] * n
    for x in code:
        degree[x] += 1
    edges = []
    for x in code:
        leaf = next(i for i in range(n) if degree[i] == 1)
        edges.append((leaf, x))
        degree[leaf] -= 1
        degree[x] -= 1
    a, b = (i for i in range(n) if degree[i] == 1)
    edges.append((a, b))
    return edges


def components_of_induced(n, edges, mask):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for a, b in edges:
        if (mask >> a & 1) and (mask >> b & 1):
            ra, rb = find(a), find(b)
            parent[ra] = rb
    return len({find(i) for i in range(n) if mask >> i & 1})


def direct_graph_polynomial(n, edges, r):
    """Directly enumerate dominating sets; no forest identity is used."""
    N = 1 + n + r * len(edges)
    ans = Counter({N - 1: 1})
    for R in range(1 << n):
        if any(not (R >> v & 1) and not any(
            (R >> (b if a == v else a) & 1)
            for a, b in edges if a == v or b == v
        ) for v in range(n)):
            continue
        eR = sum(bool(R >> a & 1) and bool(R >> b & 1) for a, b in edges)
        ans[N - (n - R.bit_count()) - eR] += r ** eR
    return +ans


def forest_component_polynomial(n, edges, r):
    """Independently enumerate dominating sets by component count."""
    N = 1 + n + r * len(edges)
    ans = Counter({N - 1: 1})
    for R in range(1 << n):
        if any(not (R >> v & 1) and not any(
            R >> (b if a == v else a) & 1
            for a, b in edges if a == v or b == v
        ) for v in range(n)):
            continue
        c = components_of_induced(n, edges, R)
        eR = sum((R >> a & 1) and (R >> b & 1) for a, b in edges)
        ans[N - n + c] += r ** eR
    return +ans


def star_forest_formula(ds, r):
    n = sum(d + 1 for d in ds)
    e = sum(ds)
    N = 1 + n + r * e
    s = N - e
    poly = Counter({0: 1})
    for d in ds:
        factor = Counter({0: (r + 1) ** d})
        factor[d - 1] += 1
        new = Counter()
        for a, va in poly.items():
            for b, vb in factor.items():
                new[a + b] += va * vb
        poly = new
    result = Counter({N - 1: 1})
    for shift, count in poly.items():
        result[s + shift] += count
    return +result


def direct_hyperedge_polynomial(n, edges, r):
    """Enumerate all point subsets, independently of dominating-set formula."""
    N = 1 + n + r * len(edges)
    hyperedges = []
    for j, (a, b) in enumerate(edges):
        h = (1 << 0) | (1 << (1 + a)) | (1 << (1 + b))
        for k in range(r):
            h |= 1 << (1 + n + j * r + k)
        hyperedges.append(h)
    out = Counter()
    for S in range(1 << N):
        if any(S & h == h for h in hyperedges):
            continue
        if any(not (S >> v & 1) and not any((S | (1 << v)) & h == h for h in hyperedges)
               for v in range(N)):
            continue
        out[S.bit_count()] += 1
    return +out


def star_edges(ds):
    n = 0
    edges = []
    for d in ds:
        edges.extend((n, n + j) for j in range(1, d + 1))
        n += d + 1
    return n, edges


def test():
    tree_count = 0
    for n in range(2, 7):
        for code in product(range(n), repeat=n - 2):
            edges = edges_from_prufer(code, n)
            alpha = max(R.bit_count() for R in range(1 << n)
                        if all(not ((R >> a & 1) and (R >> b & 1)) for a, b in edges))
            counts = set()
            for R in range(1 << n):
                if all((R >> v & 1) or any(R >> (b if a == v else a) & 1
                        for a, b in edges if a == v or b == v) for v in range(n)):
                    counts.add(components_of_induced(n, edges, R))
            assert min(counts) == 1 and max(counts) == alpha
            for r in (1, 2, 3):
                assert direct_graph_polynomial(n, edges, r) == forest_component_polynomial(n, edges, r)
            tree_count += 1
    forest_count = 0
    for ds in ((1,), (2,), (3,), (4,), (5,), (1, 1), (1, 2), (2, 2),
               (1, 3), (2, 3), (1, 1, 1), (1, 1, 2), (1, 2, 2), (3, 3)):
        n, edges = star_edges(ds)
        for r in (1, 2, 3, 4):
            assert direct_graph_polynomial(n, edges, r) == star_forest_formula(ds, r)
            forest_count += 1
    hyper_count = 0
    for ds in ((1,), (2,), (3,), (4,), (1, 1), (1, 2), (2, 2), (1, 3), (1, 1, 1)):
        n, edges = star_edges(ds)
        for r in (1, 2, 3):
            if 1 + n + r * len(edges) > 17:
                continue
            assert direct_hyperedge_polynomial(n, edges, r) == star_forest_formula(ds, r)
            hyper_count += 1
    path_count = 0
    for n in range(2, 10):
        edges = [(i, i + 1) for i in range(n - 1)]
        alpha = (n + 1) // 2
        for r in (1, 2, 3):
            N = 1 + n + r * (n - 1)
            s = N - (n - 1)
            actual = set(direct_graph_polynomial(n, edges, r)) - {N - 1}
            assert actual == set(range(s, s + alpha)) or (
                N - 1 == s + alpha - 1 and actual == set(range(s, s + alpha - 1))
            )
            path_count += 1
    print(f"PASS: {tree_count} labelled trees n<=6, {3*tree_count} forest-component polynomial checks; "
          f"{forest_count} star-forest formula checks; {hyper_count} full hyperedge checks; "
          f"{path_count} path spectra checks")


if __name__ == '__main__':
    test()
