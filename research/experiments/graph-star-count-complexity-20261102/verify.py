"""Independent finite audits for the split-incidence counting reduction.

Run: python verify.py
The complexity proof is mathematical, not a finite-experiment extrapolation.
"""
from itertools import combinations


def edges_of(n, bits):
    return [e for j, e in enumerate(combinations(range(n), 2)) if bits >> j & 1]


def split_graph(n, edges, t):
    N = n + t * len(edges)
    adj = [0] * N
    for a, b in combinations(range(n), 2):
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    for j, (a, b) in enumerate(edges):
        for z in range(t):
            v = n + t * j + z
            for w in (a, b):
                adj[v] |= 1 << w
                adj[w] |= 1 << v
    return adj


def direct_dominating(adj):
    N = len(adj)
    closed = [(1 << i) | adj[i] for i in range(N)]
    full = (1 << N) - 1
    coverage = [0] * (1 << N)
    total = 0
    for mask in range(1, 1 << N):
        bit = mask & -mask
        coverage[mask] = coverage[mask ^ bit] | closed[bit.bit_length() - 1]
        total += coverage[mask] == full
    return total


def weighted(n, edges, t):
    B = 1 << t
    total = 1  # empty original selection: all clones forced
    for S in range(1, 1 << n):
        covered = sum(bool(S & (1 << a) or S & (1 << b)) for a, b in edges)
        total += B ** covered
    return total


def direct_vertex_covers(n, edges):
    return sum(all(S >> a & 1 or S >> b & 1 for a, b in edges)
               for S in range(1 << n))


def direct_hypergraph_terminal(adj):
    h = len(adj)
    edges = [(a, b) for a in range(h) for b in range(a + 1, h) if adj[a] >> b & 1]
    N = 1 + h + len(edges)
    forbidden = [(1 << 0) | (1 << (1 + a)) | (1 << (1 + b)) |
                 (1 << (1 + h + j)) for j, (a, b) in enumerate(edges)]
    total = 0
    for mask in range(1 << N):
        if any(mask & e == e for e in forbidden):
            continue
        if all(any((mask | (1 << v)) & e == e for e in forbidden)
               for v in range(N) if not (mask >> v & 1)):
            total += 1
    return total


def run():
    base_checks = direct_checks = hyper_checks = 0
    max_h = 0
    for n in range(2, 6):
        for bits in range(1 << (n * (n - 1) // 2)):
            edges = edges_of(n, bits)
            if not edges or any(not any(v in e for e in edges) for v in range(n)):
                continue
            t = n + 1
            B = 1 << t
            covers = direct_vertex_covers(n, edges)
            assert (weighted(n, edges, t) - 1) // B ** len(edges) == covers
            base_checks += 1
            for small_t in (1, 2, t):
                H = split_graph(n, edges, small_t)
                if len(H) <= 16:
                    assert direct_dominating(H) == weighted(n, edges, small_t)
                    direct_checks += 1
                    max_h = max(max_h, len(H))
                if 1 + len(H) + sum(a.bit_count() for a in H) // 2 <= 17:
                    assert direct_hypergraph_terminal(H) == 1 + weighted(n, edges, small_t)
                    hyper_checks += 1
    assert (base_checks, direct_checks, hyper_checks, max_h) == (814, 1255, 10, 16)
    print(f"PASS {base_checks} base, {direct_checks} direct domination, "
          f"{hyper_checks} direct forbidden-hyperedge checks; max H={max_h}")


if __name__ == "__main__":
    run()
