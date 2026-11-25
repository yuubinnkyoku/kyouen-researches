#!/usr/bin/env python3
"""Exact witness construction for arbitrary vertical spacing in 3-column lattices.

No floating-point operations or third-party packages.
"""
from math import gcd
from itertools import combinations


def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a // b) * y)


def construct(a, b, d):
    """Return six distinct integer-grid points if divisibility condition holds."""
    assert min(a, b, d) >= 1
    g = gcd(a, b)
    abc = a * b * (a + b)
    if abc % (d*d*g):
        return None
    A, B = a//g, b//g
    h, u0, v0 = egcd(B, A)
    assert h == 1 and B*u0 + A*v0 == 1
    # Choose the unique residue of B^{-1} mod A in [2, A+1].
    # A=1 is included (u=2).  Then v=(1-B*u)/A < 0.
    u = 2 + (u0 - 2) % A
    v = (1 - B*u) // A
    assert B*u + A*v == 1 and u >= 2 and v <= -1
    N = -abc // (d*d*g)
    T1 = N - B*u*u - A*v*v
    T0, T2 = T1 + 2*u, T1 + 2*v
    assert T0 < 0 and T1 < 0 and T2 < 0
    S = (N-1) % 2
    assert all(T % 2 == S for T in (T0,T1,T2))
    points = []
    for x, T in zip((0, a, a+b), (T0,T1,T2)):
        points.extend(((x, d*((S+T)//2)), (x, d*((S-T)//2))))
    assert len(set(points)) == 6
    return points, (u, v, (T0,T1,T2), S)


def det3(p, q, r):
    return (p[0]*(q[1]*r[2]-q[2]*r[1])
            -p[1]*(q[0]*r[2]-q[2]*r[0])
            +p[2]*(q[0]*r[1]-q[1]*r[0]))


def circle_from_three(p, q, r):
    z = lambda p: p[0]**2 + p[1]**2
    D = det3((p[0],p[1],1), (q[0],q[1],1), (r[0],r[1],1))
    if not D:
        return None
    U = -det3((z(p),p[1],1), (z(q),q[1],1), (z(r),r[1],1))
    V = -det3((p[0],z(p),1), (q[0],z(q),1), (r[0],z(r),1))
    W = -det3((p[0],p[1],z(p)), (q[0],q[1],z(q)), (r[0],r[1],z(r)))
    if D < 0:
        D,U,V,W = -D,-U,-V,-W
    gg = gcd(gcd(D, abs(U)), gcd(abs(V), abs(W)))
    return D//gg, U//gg, V//gg, W//gg


def audit_witness(points):
    c = circle_from_three(points[0],points[2],points[4])
    assert c is not None
    D,U,V,W = c
    assert all(D*(x*x+y*y)+U*x+V*y+W == 0 for x,y in points)
    return c


def audit_finite(a,b,d,height=7):
    pts = [(x,d*j) for x in (0,a,a+b) for j in range(height)]
    circles = {c for p,q,r in combinations(pts,3)
               if (c:=circle_from_three(p,q,r)) is not None}
    maximum = 0
    for D,U,V,W in circles:
        count = sum(D*(x*x+y*y)+U*x+V*y+W == 0 for x,y in pts)
        maximum = max(maximum,count)
    return maximum


def main():
    total = positive = 0
    for d in range(1,31):
        for a in range(1,51):
            for b in range(1,51):
                total += 1
                result = construct(a,b,d)
                if result:
                    positive += 1
                    pts, extra = result
                    audit_witness(pts)
    print('arbitrary d construction:',total,'triples,',positive,'positive; every witness direct')
    count = negatives = positives = 0
    for d in (1,2,3,4,6,10,12):
        for a in range(1,7):
            for b in range(1,7):
                count += 1
                M = audit_finite(a,b,d)
                good = a*b*(a+b) % (d*d*gcd(a,b)) == 0
                if not good:
                    negatives += 1
                    assert M == 4, (a,b,d,M)
                else:
                    positives += 1
                    assert 4 <= M <= 6, (a,b,d,M)
    print('independent determinant exhaustive:',count,'3x7 boards,',negatives,'criterion-negative,',positives,'positive')
    a,b,d = 4,9,6
    pts, extra = construct(a,b,d)
    print('mixed-prime witness (a,b,d)=(4,9,6):',pts,'metadata:',extra,'circle:',audit_witness(pts))
    assert a*(a+b) % (d*d) != 0 and b*(a+b) % (d*d) != 0

if __name__ == '__main__':
    main()
