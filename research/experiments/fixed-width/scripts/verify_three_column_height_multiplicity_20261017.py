#!/usr/bin/env python3
"""Exact independent circle enumeration for first-appearance multiplicity.

Uses two points in one column and a third in another column to derive
integer circle coefficients; does NOT use the triple-determinant method.
"""
from itertools import combinations
from math import gcd
from functools import reduce


def normalize(v):
    g = reduce(gcd, v)
    assert g != 0
    v = tuple(x // g for x in v)
    return v if v[0] > 0 else tuple(-x for x in v)


def all_circles(a, b, d, m):
    xs = (0, a, a + b)
    pts = tuple((x, d * j) for x in xs for j in range(m))
    circles = set()
    for xi in xs:
        for yi, yj in combinations(range(0, d * m, d), 2):
            s = yi + yj
            for xk, yk in pts:
                if xk == xi:
                    continue
                den = 2 * (xk - xi)
                num = xk*xk - xi*xi + yk*yk - yi*yi - s*(yk - yi)
                const = -den*(xi*xi + yi*yi) + 2*num*xi + s*den*yi
                circles.add(normalize((den, -2*num, -s*den, const)))
    return pts, circles


def exact_counts(a, b, d, k):
    assert a*b == d*d*k*(k+1)
    h5, h6 = k+2, 2*k+2
    pts, cs = all_circles(a, b, d, h6)
    first5 = first6 = 0
    early5 = early6 = 0
    for D, A, B, C in cs:
        on = [(x, y) for x,y in pts if D*(x*x+y*y)+A*x+B*y+C == 0]
        if len(on) < 5:
            continue
        # Number of grid rows needed for a subset of q points of this circle.
        js = sorted(y // d for x,y in on)
        min5 = min(js[i+4] - js[i] + 1 for i in range(len(js)-4))
        if min5 < h5:
            early5 += 1
        if sum(y < d*h5 for x,y in on) >= 5:
            first5 += 1
        if len(on) >= 6:
            min6 = min(js[i+5] - js[i] + 1 for i in range(len(js)-5))
            if min6 < h6:
                early6 += 1
            first6 += 1
    assert (early5, early6, first5, first6) == (0,0,2,1), (a,b,d,k,early5,early6,first5,first6)
    return len(cs), first5, first6


if __name__ == '__main__':
    cases = [(1,k*(k+1),1,k) for k in range(1,11)]
    cases += [(2,3,1,2), (2,12,2,2), (3,8,2,2), (4,5,1,4),
              (4,20,2,4), (6,20,2,5), (9,20,3,4)]
    for a,b,d,k in cases:
        total, c5, c6 = exact_counts(a,b,d,k)
        print(f'a={a:3} b={b:3} d={d:2} k={k:2} circles={total:6} H5={k+2:2} first5={c5} H6={2*k+2:2} first6={c6} PASS')
