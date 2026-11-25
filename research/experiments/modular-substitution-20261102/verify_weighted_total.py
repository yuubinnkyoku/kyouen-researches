#!/usr/bin/env python3
"""Independent audit of the q-weighted total terminal count for substitution trees."""
from itertools import combinations
from random import Random


def leaf():
    return None


def node(children, edges):
    return (tuple(children), tuple(sorted(edges)))


def expand(expr):
    if expr is None:
        return 1, set()
    children, quotient = expr
    pieces = [expand(child) for child in children]
    offsets = []
    n = 0
    edges = set()
    for size, child_edges in pieces:
        offsets.append(n)
        edges.update((a+n, b+n) for a, b in child_edges)
        n += size
    for i, j in quotient:
        for a in range(offsets[i], offsets[i]+pieces[i][0]):
            for b in range(offsets[j], offsets[j]+pieces[j][0]):
                edges.add((a, b))
    return n, edges


def weighted_tables(expr, r):
    """Degree-only recursion: no induced-edge degree is stored."""
    if expr is None:
        return [1, 1], [0, 1]
    children, quotient = expr
    tables = [weighted_tables(child, r) for child in children]
    h = len(children)
    quotient = set(quotient)
    powers = [1]
    bound = sum(len(a)-1 for a, _ in tables)**2
    for _ in range(bound):
        powers.append(powers[-1]*r)

    def build(dominating):
        out = [0]*(1+sum(len(a)-1 for a, _ in tables))
        for mask in range(1 << h):
            active = [i for i in range(h) if mask & (1 << i)]
            if dominating and any(i not in active and
                not any((min(i,j),max(i,j)) in quotient for j in active)
                for i in range(h)):
                continue

            def visit(pos, sizes, coeff):
                if pos == len(active):
                    cross = sum(sizes[i]*sizes[j] for i,j in quotient
                                if i in sizes and j in sizes)
                    out[sum(sizes.values())] += coeff*powers[cross]
                    return
                i = active[pos]
                neighbor = any((min(i,j),max(i,j)) in quotient
                               for j in active if j != i)
                source = tables[i][0 if (not dominating or neighbor) else 1]
                for a in range(1, len(source)):
                    if source[a]:
                        sizes[i] = a
                        visit(pos+1, sizes, coeff*source[a])
                        del sizes[i]
            visit(0, {}, 1)
        return out
    return build(False), build(True)


def brute(n, edges, r):
    adj = [0]*n
    for a,b in edges:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    a = [0]*(n+1)
    d = [0]*(n+1)
    for mask in range(1 << n):
        size = mask.bit_count()
        e = sum(bool(mask >> u & 1 and mask >> v & 1) for u,v in edges)
        weight = r**e
        a[size] += weight
        if all(mask >> v & 1 or (adj[v] & mask) for v in range(n)):
            d[size] += weight
    return a,d


def check(expr, r):
    n, edges = expand(expr)
    expected = brute(n, edges, r)
    got = weighted_tables(expr, r)
    assert got == expected, (n, sorted(edges), r, got, expected)
    assert 1+sum(got[1]) == 1+sum(expected[1])


def main():
    cases = 0
    pairs = list(combinations(range(4),2))
    for mask in range(64):
        expr = node([leaf() for _ in range(4)],
                    [e for bit,e in enumerate(pairs) if mask >> bit & 1])
        for r in (1,2,3,6):
            check(expr,r)
            cases += 1
    rng = Random(20261102)
    for _ in range(360):
        pieces = [leaf() for _ in range(rng.randint(2,8))]
        while len(pieces) > 1:
            h = rng.randint(2,min(4,len(pieces)))
            children = [pieces.pop(rng.randrange(len(pieces))) for _ in range(h)]
            edges = [e for e in combinations(range(h),2) if rng.randrange(2)]
            pieces.append(node(children,edges))
        for r in (1,2,3,6):
            check(pieces[0],r)
            cases += 1
    p4 = [(0,1),(1,2),(2,3)]
    for m in (1,2,3):
        cliques = [node([leaf() for _ in range(m)],
                        list(combinations(range(m),2))) for _ in range(4)]
        expr = node(cliques,p4)
        for r in (1,2,3,6):
            check(expr,r)
            cases += 1
    print(f'PASS {cases} independent (A,D) weighted-degree comparisons, '
          'q=4,5,6,9, P4 clique blowups m<=3; mismatches 0')


if __name__ == '__main__':
    main()
