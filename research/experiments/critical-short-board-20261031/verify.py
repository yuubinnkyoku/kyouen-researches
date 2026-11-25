#!/usr/bin/env python3
"""Independent exact lattice audit for N=2q-2 planar carrier classification."""
from collections import Counter
from itertools import combinations, product


def det4(p):
    x0, y0 = p[0]
    rows = [(x-x0, y-y0, x*x+y*y-x0*x0-y0*y0) for x,y in p[1:]]
    (a,b,c),(d,e,f),(g,h,i) = rows
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)


def forbidden(points, q):
    return [frozenset(edge) for edge in combinations(range(len(points)),q)
            if all(det4([points[i] for i in quad]) == 0
                   for quad in combinations(edge,4))]


def mex(values):
    s = set(values)
    k = 0
    while k in s:
        k += 1
    return k


def audit_game(n, edges):
    full = (1 << n) - 1
    forbidden_masks = [sum(1 << x for x in e) for e in edges]
    g, h = {}, {}
    for mask in range(full, -1, -1):
        if any((mask & e) == e for e in forbidden_masks):
            continue
        children = [mask | (1 << i) for i in range(n)
                    if not (mask >> i & 1) and
                    all(((mask | (1 << i)) & e) != e for e in forbidden_masks)]
        g[mask] = mex(g[c] for c in children) if children else 0
        h[mask] = mex(h[c] for c in children) if children else 1
        if len(edges) <= 2:
            assert h[mask] == (1-g[mask] if g[mask] < 2 else g[mask])
        if len(edges) == 3:
            assert n == 6
            assert g[mask] == ((4-mask.bit_count()) % 2)
            assert h[mask] == 1-g[mask]
    return g[0], h[0]


def check_board(points, q, sample_game=False):
    n = len(points)
    edges = forbidden(points,q)
    f = len(edges)
    assert f in ({0,1,2,3,5,15} if q == 4 else {0,2,1,6,21,56}), (q,points,f)
    if f == 2:
        assert len(edges[0] & edges[1]) == 2
        expected = (2,2) if q == 4 else (0,1)
    elif f == 3:
        assert q == 4
        complements = [set(range(n))-set(e) for e in edges]
        assert all(not a & b for a,b in combinations(complements,2))
        expected = (0,1)
    elif f == 0:
        expected = (0,1)
    else:
        M = set().union(*edges)
        m = len(M)
        assert set(edges) == set(map(frozenset, combinations(M,q)))
        L = n-m+q-1
        expected = (L%2,1-L%2)
    if sample_game:
        assert audit_game(n,edges) == expected, (q,points,expected)
    return f


def main():
    grid = list(product(range(4),repeat=2))
    for q,n in [(4,6),(5,8)]:
        counts = Counter()
        samples = Counter()
        for ids in combinations(range(len(grid)),n):
            pts = [grid[i] for i in ids]
            f = check_board(pts,q)
            counts[f] += 1
            if samples[f] < 8:
                check_board(pts,q,True)
                samples[f] += 1
        print(f'q={q}, N={n}, exhaustive boards={sum(counts.values())}, forbidden-edge counts={dict(sorted(counts.items()))}, direct mex={sum(samples.values())}')
    q4triple = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,3)]
    q5double = [(1,-2),(1,2),(-2,-1),(-2,1),(-1,-2),(3,-2),(3,2),(4,-1)]
    assert check_board(q4triple,4,True) == 3
    assert check_board(q5double,5,True) == 2
    print('PASS: integer triple-carrier and q=5 double-carrier witnesses; all checks')


if __name__ == '__main__':
    main()
