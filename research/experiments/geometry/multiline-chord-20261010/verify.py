#!/usr/bin/env python3
"""Independent exhaustive small-window audit for sharp simultaneous 2+2 row-circle counts."""
from itertools import combinations, product
from collections import Counter


def U(r, t):
    return sum(min(2*r-4*i-3, 2*t-4*j-3)
               for i in range(r//2) for j in range(t//2))


def canonical(m, r):
    assert 0 <= r <= m
    if r < 2:
        return tuple(range(r))
    if r == 2:
        return (0, m-1 if m % 2 == 0 else m-2)
    lo = (m-r)//2
    return tuple(range(lo, lo+r))


def chord_energy(A, B):
    a = Counter(x+y for x, y in combinations(A, 2))
    b = Counter(x+y for x, y in combinations(B, 2))
    return sum(v*b[s] for s, v in a.items())


def circle_det4(pts):
    # Determinant of 4x4 lifted coordinates: x, y, x*x+y*y, 1.
    mat = [[x, y, x*x+y*y, 1] for x, y in pts]
    det = 0
    from itertools import permutations
    for p in permutations(range(4)):
        inv = sum(p[i] > p[j] for i in range(4) for j in range(i+1, 4))
        prod = 1
        for i in range(4):
            prod *= mat[i][p[i]]
        det += (-1 if inv % 2 else 1)*prod
    return det


def det_energy(A, B, y1, y2):
    assert y1 != y2
    return sum(circle_det4([(a, y1), (b, y1), (c, y2), (d, y2)]) == 0
               for a,b in combinations(A, 2) for c,d in combinations(B, 2))


def main():
    pair_tests = 0
    brute_tests = 0
    det_tests = 0
    for m in range(1, 15):
        cs = [canonical(m, r) for r in range(m+1)]
        for r in range(m+1):
            for t in range(m+1):
                assert chord_energy(cs[r], cs[t]) == U(r,t), (m,r,t)
                pair_tests += 1
                if m <= 8:
                    assert det_energy(cs[r], cs[t], 0, 3) == U(r,t), (m,r,t)
                    det_tests += 1
        if m <= 7:
            sets = [list(combinations(range(m), r)) for r in range(m+1)]
            for r in range(m+1):
                for t in range(m+1):
                    vals = [chord_energy(A,B) for A in sets[r] for B in sets[t]]
                    assert max(vals) == U(r,t), (m,r,t,max(vals),U(r,t))
                    brute_tests += len(vals)
    # Simultaneous multi-row example with uneven occupancy, and independent determinant.
    m = 8
    rs = [8,7,6,5,4,3,2,1,0]
    cs = [canonical(m,r) for r in rs]
    predicted = sum(U(rs[i],rs[j]) for i in range(len(rs)) for j in range(i+1,len(rs)))
    actual = sum(det_energy(cs[i],cs[j],i,j) for i in range(len(rs)) for j in range(i+1,len(rs)))
    assert actual == predicted
    print('PASS: %d constructed row-pair cases, %d exhaustive labeled subset pairs, %d independent determinant cases' % (pair_tests, brute_tests, det_tests))
    print('9-row witness m=8, occupancies=%s, total 2+2 circle quadruples=%d' % (rs,actual))
    print('Rows:', cs)


if __name__ == '__main__':
    main()
