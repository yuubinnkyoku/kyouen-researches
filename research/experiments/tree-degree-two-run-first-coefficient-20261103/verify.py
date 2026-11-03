"""Independent audit of the corrected first-defect coefficient for trees."""
from itertools import product


def tree_from_prufer(code):
    n = len(code) + 2
    deg = [1] * n
    for x in code:
        deg[x] += 1
    edges = []
    for x in code:
        leaf = next(i for i in range(n) if deg[i] == 1)
        edges.append((leaf, x))
        deg[leaf] -= 1
        deg[x] -= 1
    a, b = (i for i in range(n) if deg[i] == 1)
    edges.append((a, b))
    return edges


def counts(n, edges, r):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    deg = list(map(len, adj))
    L = sum(x == 1 for x in deg)
    C = len(edges) - L
    core = [i for i in range(n) if deg[i] >= 2]
    direct = 0
    direct_kernels = 0
    for mask in range(1 << len(core)):
        B = {core[j] for j in range(len(core)) if mask >> j & 1}
        if any(not (adj[v] - B) for v in B):
            continue
        a = sum(deg[v] == 1 and bool(adj[v] & B) for v in range(n))
        eb = sum(bool(adj[v] & B) for v in B) // 2
        d = sum(deg[v] - 1 for v in B) - eb
        if d == 1:
            direct_kernels += 1
            direct += r ** (C + a - len(B) - 1) * (r + 1) ** (L - a)
    degree_two = {i for i in range(n) if deg[i] == 2}
    candidates = [{v} for v in degree_two]
    candidates += [{a, b} for a, b in edges if a in degree_two and b in degree_two]
    formula = 0
    for B in candidates:
        a = sum(deg[v] == 1 and bool(adj[v] & B) for v in range(n))
        formula += r ** (C + a - len(B) - 1) * (r + 1) ** (L - a)
    return direct, formula, direct_kernels, len(candidates)


def main():
    tested = 0
    for n in range(3, 8):
        for code in product(range(n), repeat=n - 2):
            edges = tree_from_prufer(code)
            for r in range(1, 5):
                actual, expected, kernels, candidate_count = counts(n, edges, r)
                assert (actual, kernels) == (expected, candidate_count), (n, code, r, actual, expected)
                tested += 1
    assert tested == 72988, tested
    print(f"PASS: {tested} labeled-tree/q cases; all coefficients and kernel counts agree")
    assert counts(5, [(0, 1), (1, 2), (2, 3), (3, 4)], 1) == (12, 12, 5, 5)
    print("PASS: P5 q=4 regression, coefficient=12 and admissible kernels=5")


if __name__ == "__main__":
    main()
