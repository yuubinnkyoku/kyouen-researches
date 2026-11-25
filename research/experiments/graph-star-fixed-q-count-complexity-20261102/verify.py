"""Independent finite audits for fixed-q>=5 graph-star #P-hardness.

Run: python verify.py
The reduction is a mathematical theorem; these are implementation checks.
"""
from fractions import Fraction
from itertools import combinations


def edges_of(n, bits):
    return [e for j, e in enumerate(combinations(range(n), 2)) if bits >> j & 1]


def clone_graph(n, edges, t):
    N = n + t * len(edges)
    adj = [0] * N
    for a, b in edges:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    for j, (a, b) in enumerate(edges):
        for z in range(t):
            v = n + t*j + z
            for w in (a, b):
                adj[v] |= 1 << w
                adj[w] |= 1 << v
    return adj


def direct_weighted_domination(adj, r):
    N = len(adj)
    full = (1 << N) - 1
    closed = [adj[v] | (1 << v) for v in range(N)]
    covered = [0] * (1 << N)
    total = 0
    for S in range(1, 1 << N):
        bit = S & -S
        v = bit.bit_length() - 1
        covered[S] = covered[S ^ bit] | closed[v]
        if covered[S] == full:
            e = sum((adj[v] & S).bit_count() for v in range(N)
                    if S >> v & 1) // 2
            total += r ** e
    return total


def original_coefficients(n, edges):
    counts = {}
    for S in range(1 << n):
        a = b = 0
        for u, v in edges:
            selected = ((S >> u) & 1) + ((S >> v) & 1)
            a += selected == 1
            b += selected == 2
        counts[a, b] = counts.get((a, b), 0) + 1
    return counts


def evaluate_closed_form(counts, r, t):
    A, B = r + 1, r*r + 1
    return sum(count * r**b * (A**a * B**b)**t
               for (a, b), count in counts.items())


def recover_by_interpolation(m, r, values):
    """Exact rational Vandermonde elimination; no original subsets used."""
    pairs = [(a, b) for a in range(m+1) for b in range(m+1-a)]
    bases = [(r+1)**a * (r*r+1)**b for a, b in pairs]
    assert len(set(bases)) == len(bases)
    L = len(pairs)
    assert len(values) == L
    mat = [[Fraction(pow(base, t)) for base in bases]
           + [Fraction(values[t-1])] for t in range(1, L+1)]
    for col in range(L):
        pivot = next(row for row in range(col, L) if mat[row][col])
        mat[col], mat[pivot] = mat[pivot], mat[col]
        scale = mat[col][col]
        for j in range(col, L+1):
            mat[col][j] /= scale
        for row in range(col+1, L):
            factor = mat[row][col]
            if factor:
                for j in range(col, L+1):
                    mat[row][j] -= factor * mat[col][j]
    result = [Fraction(0)] * L
    for col in range(L-1, -1, -1):
        result[col] = mat[col][L] - sum(
            mat[col][j]*result[j] for j in range(col+1, L))
    return {pair: result[j]/r**pair[1] for j, pair in enumerate(pairs)}


def direct_terminal_hypergraph(adj, q):
    """Enumerate all safe subsets, independently of domination identities."""
    n = len(adj)
    edges = [(i, j) for i in range(n) for j in range(i+1, n)
             if adj[i] >> j & 1]
    r = q-3
    N = 1+n+r*len(edges)
    assert N <= 18
    forbidden = []
    for k, (u, v) in enumerate(edges):
        mask = 1 | (1 << (1+u)) | (1 << (1+v))
        for z in range(r):
            mask |= 1 << (1+n+r*k+z)
        forbidden.append(mask)
    total = 0
    for S in range(1 << N):
        if any(S & h == h for h in forbidden):
            continue
        if all(any((S | (1 << v)) & h == h for h in forbidden)
               for v in range(N) if not (S >> v & 1)):
            total += 1
    return total


def run():
    direct_checks = interpolation_checks = hyper_checks = 0
    for n in range(2, 5):
        for bits in range(1 << (n*(n-1)//2)):
            edges = edges_of(n, bits)
            m = len(edges)
            if not edges or m > 3 or any(
                    not any(v in e for e in edges) for v in range(n)):
                continue
            counts = original_coefficients(n, edges)
            L = (m+1)*(m+2)//2
            covers = sum(all((S >> a & 1) or (S >> b & 1)
                             for a, b in edges) for S in range(1 << n))
            for r in (2, 3, 4):
                values = [evaluate_closed_form(counts, r, t)
                          for t in range(1, L+1)]
                recovered = recover_by_interpolation(m, r, values)
                assert recovered == {
                    pair: Fraction(counts.get(pair, 0)) for pair in recovered}
                assert sum(v for (a, b), v in recovered.items()
                           if a+b == m) == covers
                interpolation_checks += 1
                for t in (1, 2):
                    adj = clone_graph(n, edges, t)
                    if len(adj) <= 15:
                        assert direct_weighted_domination(
                            adj, r) == evaluate_closed_form(counts, r, t)
                        direct_checks += 1
                    if ((n == 2 and t == 1 and r in (2, 3, 4))
                            or (n == 2 and t == 2 and r == 2)
                            or (n == 3 and m == 2 and t == 1 and r == 2)):
                        assert direct_terminal_hypergraph(
                            adj, r+3) == 1+evaluate_closed_form(counts, r, t)
                        hyper_checks += 1
    # The reduction strips isolates and restores the factor 2^k.
    edges = [(0, 1)]
    assert sum(all((S >> a & 1) or (S >> b & 1) for a, b in edges)
               for S in range(1 << 3)) == 6
    assert sum(all((S >> a & 1) or (S >> b & 1) for a, b in edges)
               for S in range(1 << 2)) * 2 == 6
    # Larger nontrivial Vandermonde systems (15, 21 and 28 bases).
    stress_checks = 0
    stress_graphs = [
        (5, [(0, 1), (1, 2), (2, 3), (3, 4)]),
        (5, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]),
        (4, list(combinations(range(4), 2))),
    ]
    for n, edges in stress_graphs:
        m = len(edges)
        counts = original_coefficients(n, edges)
        L = (m+1)*(m+2)//2
        for r in (2, 3):
            values = [evaluate_closed_form(counts, r, t)
                      for t in range(1, L+1)]
            recovered = recover_by_interpolation(m, r, values)
            assert recovered == {
                pair: Fraction(counts.get(pair, 0)) for pair in recovered}
            stress_checks += 1
    assert stress_checks == 6
    assert (interpolation_checks, direct_checks, hyper_checks) == (72, 144, 7)
    print(f"PASS {interpolation_checks} exact interpolations; "
          f"{direct_checks} direct domination checks; "
          f"{hyper_checks} direct q-uniform terminal checks; "
          f"{stress_checks} larger interpolations; isolated-vertex correction")


if __name__ == "__main__":
    run()
