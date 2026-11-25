#!/usr/bin/env python3
"""Independent determinant / binary-form / weighted-sum audit for 2+1+1 circles.
No floating-point arithmetic is used.  Run: python verify_three_line_211.py
"""
from itertools import combinations
from math import isqrt


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def circle_det(points):
    # Difference of the lifted coordinates against the fourth point.
    x0, y0 = points[3]
    rows = []
    for x, y in points[:3]:
        rows.append((x*x+y*y-x0*x0-y0*y0, x-x0, y-y0))
    return det3(*rows) == 0


def form(a, b, u, v, y_pair, y_u, y_v):
    d, s = b-a, a+b
    X, Y = 2*u-s, 2*v-s
    if (y_u-y_pair)*(y_v-y_pair) < 0:
        # u and v on opposite sides. p below, q above.
        if y_u < y_pair:
            p, q = y_pair-y_u, y_v-y_pair
            return q*X*X+p*Y*Y == (p+q)*(d*d-4*p*q)
        p, q = y_pair-y_v, y_u-y_pair
        return q*Y*Y+p*X*X == (p+q)*(d*d-4*p*q)
    # Pair on an extreme line: u and v in order near -> far.
    if abs(y_u-y_pair) < abs(y_v-y_pair):
        p, q = abs(y_u-y_pair), abs(y_v-y_pair)
        return q*X*X-p*Y*Y == (q-p)*(d*d+4*p*q)
    p, q = abs(y_v-y_pair), abs(y_u-y_pair)
    return q*Y*Y-p*X*X == (q-p)*(d*d+4*p*q)


def weighted_count(m, y_pair, y_u, y_v):
    count = 0
    # For a=0, other coordinates alpha,beta must be in a window of length m.
    # Each lies in [-(m-1),2*(m-1)] for any admissible translation.
    for d in range(1,m):
        for alpha in range(-(m-1),2*m-1):
            for beta in range(-(m-1),2*m-1):
                if not form(0,d,alpha,beta,y_pair,y_u,y_v):
                    continue
                xs = (0,d,alpha,beta)
                span = max(xs)-min(xs)
                count += max(0,m-span)
    return count


def main():
    comparisons = 0
    counts = 0
    for rows in combinations(range(8),3):
        for y_pair in rows:
            y_u,y_v = (y for y in rows if y!=y_pair)
            for m in range(2,9):
                observed = 0
                for a,b in combinations(range(m),2):
                    for u in range(m):
                        for v in range(m):
                            points=((a,y_pair),(b,y_pair),(u,y_u),(v,y_v))
                            truth=circle_det(points)
                            test=form(a,b,u,v,y_pair,y_u,y_v)
                            assert truth==test, (rows,y_pair,m,a,b,u,v)
                            observed+=truth
                            comparisons+=1
                counted=weighted_count(m,y_pair,y_u,y_v)
                assert counted==observed, (rows,y_pair,m,observed,counted)
                counts+=1
    # An infinite arithmetic obstruction for equally spaced rows.
    obstruction=0
    for h in range(1,20,2):
        for d in range(4,161,4):
            n=2*d*d-8*h*h
            if n>=0:
                assert not any(isqrt(n-X*X)**2==n-X*X for X in range(isqrt(n)+1))
                obstruction+=1
    print(f'PASS: {comparisons:,} integer-determinant vs binary-form instances')
    print(f'PASS: {counts} exact weighted-sum vs direct count instances')
    print(f'PASS: {obstruction} modular-obstruction instances (h odd, 4|d)')
    print('General claims are proved algebraically; these are finite independent checks.')

if __name__=='__main__':
    main()
