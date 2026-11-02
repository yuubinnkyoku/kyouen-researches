#!/usr/bin/env python3
"""Independent finite audit of graph-substitution terminal-polynomial recursion."""
from collections import Counter
from itertools import combinations
import random


def leaf():
    return ((), ())


def node(children, quotient_edges):
    return (tuple(children), tuple(sorted(tuple(sorted(e)) for e in quotient_edges)))


def graph_of(expr):
    children, qe = expr
    if not children:
        return 1, set()
    pieces = [graph_of(child) for child in children]
    offsets = []
    n = 0
    edges = set()
    for size, local_edges in pieces:
        offsets.append(n)
        edges.update((u+n, v+n) for u, v in local_edges)
        n += size
    for i, j in qe:
        for u in range(offsets[i], offsets[i] + pieces[i][0]):
            for v in range(offsets[j], offsets[j] + pieces[j][0]):
                edges.add((min(u, v), max(u, v)))
    return n, edges


def recurse(expr):
    children, qe = expr
    if not children:
        return {(0, 0): 1, (1, 0): 1}, {(1, 0): 1}
    data = [recurse(c) for c in children]
    k = len(children)
    edge_set = set(qe)

    def build(dominating):
        result = Counter()
        for mask in range(1 << k):
            if dominating and any(not (mask >> i & 1) and
                                  not any((mask >> j & 1) and
                                          (min(i, j), max(i, j)) in edge_set
                                          for j in range(k) if i != j)
                                  for i in range(k)):
                continue
            factors = []
            for i in range(k):
                if not (mask >> i & 1):
                    continue
                active_neighbor = any((mask >> j & 1) and
                                      (min(i, j), max(i, j)) in edge_set
                                      for j in range(k) if j != i)
                source = data[i][1] if dominating and not active_neighbor else data[i][0]
                factors.append((i, [(a, b, c) for (a, b), c in source.items() if a]))
            states = [((), 0, 0, 1)]
            for i, terms in factors:
                next_states = []
                for counts, a0, b0, weight in states:
                    for a, b, multiplicity in terms:
                        previous = sum(counts[pos] for pos, (j, _) in enumerate(factors[:len(counts)])
                                       if (min(i, j), max(i, j)) in edge_set)
                        next_states.append((counts + (a,), a0+a, b0+b+a*previous,
                                            weight*multiplicity))
                states = next_states
            for _, a, b, weight in states:
                result[(a, b)] += weight
        return dict(result)
    return build(False), build(True)


def direct_tables(n, edges):
    a, d = Counter(), Counter()
    adj = [0]*n
    for i, j in edges:
        adj[i] |= 1 << j
        adj[j] |= 1 << i
    for mask in range(1 << n):
        size = mask.bit_count()
        edge_count = sum(bool((mask >> i & 1) and (mask >> j & 1)) for i, j in edges)
        a[(size, edge_count)] += 1
        if all((mask >> v & 1) or (adj[v] & mask) for v in range(n)):
            d[(size, edge_count)] += 1
    return dict(a), dict(d)


def terminal(d, n, e, q):
    r = q-3
    N = 1+n+r*e
    p = Counter({N-1: 1})
    for (a, b), count in d.items():
        p[N-n+a-b] += count*r**b
    return dict(p)


def direct_star(n, edges, q):
    r = q-3
    hyperedges = []
    idx = n+1
    for i, j in sorted(edges):
        hyperedges.append((1 | (1 << (i+1)) | (1 << (j+1)) |
                           sum(1 << t for t in range(idx, idx+r))))
        idx += r
    N = idx
    out = Counter()
    for mask in range(1 << N):
        if any(mask & h == h for h in hyperedges):
            continue
        if all(any(((mask | (1 << p)) & h) == h for h in hyperedges)
               for p in range(N) if not (mask >> p & 1)):
            out[mask.bit_count()] += 1
    return dict(out)


def clique(m):
    return node([leaf() for _ in range(m)], combinations(range(m), 2))


def check(expr, q_values=(4, 5), star=False):
    n, edges = graph_of(expr)
    a, d = recurse(expr)
    aa, dd = direct_tables(n, edges)
    assert a == aa, ('A', n, edges, a, aa)
    assert d == dd, ('D', n, edges, d, dd)
    for q in q_values:
        p = terminal(d, n, len(edges), q)
        assert p == terminal(dd, n, len(edges), q)
        if star:
            assert p == direct_star(n, edges, q), ('star', n, edges, q)


def main():
    count = 0
    # All 64 labelled quotient graphs on four singleton modules.
    pairs = list(combinations(range(4), 2))
    for bits in range(64):
        expr = node([leaf() for _ in range(4)],
                    [e for i, e in enumerate(pairs) if bits >> i & 1])
        check(expr)
        count += 1
    rng = random.Random(20261102)
    for _ in range(360):
        pieces = [leaf() for _ in range(rng.randint(2, 8))]
        while len(pieces) > 1:
            k = rng.randint(2, min(4, len(pieces)))
            selected = [pieces.pop(rng.randrange(len(pieces))) for _ in range(k)]
            qe = [e for e in combinations(range(k), 2) if rng.randrange(2)]
            pieces.append(node(selected, qe))
        check(pieces[0])
        count += 1
    # Independent enumeration of the forbidden q-point hyperedges.
    star_cases = 0
    for bits in range(64):
        expr = node([leaf() for _ in range(4)],
                    [e for i, e in enumerate(pairs) if bits >> i & 1])
        if 1 <= bits.bit_count() <= 3:
            check(expr, q_values=(4, 5, 6) if bits.bit_count() <= 2 else (4, 5), star=True)
            star_cases += 1
    # P4 blown up by cliques: unbounded treewidth and not a cograph.
    p4 = [(0, 1), (1, 2), (2, 3)]
    for m in (1, 2, 3):
        expr = node([clique(m) for _ in range(4)], p4)
        n, edges = graph_of(expr)
        _, d = recurse(expr)
        _, dd = direct_tables(n, edges)
        assert d == dd
        t = 2**m-1
        assert terminal(d, n, len(edges), 4) and sum(d.values()) == t**4+4*t**3+4*t**2
    print(f'PASS: {count} substitution expressions (A,D, q=4,5), '
          f'{star_cases} direct q-point hyperedge graphs (103 q=4,5,6 cases), '
          'P4 clique blowups m=1..3; zero mismatches')


if __name__ == '__main__':
    main()
