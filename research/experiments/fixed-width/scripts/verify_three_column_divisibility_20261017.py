#!/usr/bin/env python3
"""Independent finite audit of 3-column six-point circle divisibility theorem.

Method A: row-pair midpoint / exact chord-square equation.
Method B: enumerate circles through three noncollinear grid points by integer
          determinant; no chord formula is used in method B.
"""
from itertools import combinations
from math import gcd


def chord_six(h, d, m):
    # Return frozensets of 6 lattice coordinates in row indices, not scaled y.
    out = set()
    pairs = [(lo, hi, hi-lo, lo+hi) for lo in range(m) for hi in range(lo+1,m)]
    for p0 in pairs:
        for p1 in pairs:
            if p0[3] != p1[3]:
                continue
            for p2 in pairs:
                if p2[3] != p0[3]:
                    continue
                if d*d*(p0[2]**2 - 2*p1[2]**2 + p2[2]**2) == -8*h*h:
                    out.add(frozenset((i, y) for i,p in enumerate((p0,p1,p2)) for y in p[:2]))
    return out


def det3(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])


def triple_six(h,d,m):
    pts = [(i,j) for i in range(3) for j in range(m)]
    physical = [(h*i,d*j) for i,j in pts]
    circles = set()
    for ids in combinations(range(len(pts)),3):
        (x1,y1),(x2,y2),(x3,y3) = [physical[i] for i in ids]
        a = (x1,y1,1); b=(x2,y2,1); c=(x3,y3,1)
        D = det3(a,b,c)
        if D==0: continue
        z = [x*x+y*y for x,y in ((x1,y1),(x2,y2),(x3,y3))]
        A = -det3((z[0],y1,1),(z[1],y2,1),(z[2],y3,1))
        B = -det3((x1,z[0],1),(x2,z[1],1),(x3,z[2],1))
        C = -det3((x1,y1,z[0]),(x2,y2,z[1]),(x3,y3,z[2]))
        hit = frozenset(pts[i] for i,(x,y) in enumerate(physical) if D*(x*x+y*y)+A*x+B*y+C==0)
        if len(hit)==6: circles.add(hit)
        elif len(hit)>6: raise AssertionError((h,d,m,'seven or more points',hit))
    return circles


def explicit_witness(h,d):
    assert h%d==0
    a=h//d
    m=3*a+1
    return m, frozenset(((0,a),(0,2*a),(1,0),(1,3*a),(2,0),(2,3*a)))


def main():
    cases=0
    total=0
    # All h,d in [1,6], all 3<=m<=8; exhaustive and independent.
    for h in range(1,7):
        for d in range(1,7):
            for m in range(3,9):
                a=chord_six(h,d,m)
                b=triple_six(h,d,m)
                assert a==b, (h,d,m,a^b)
                if h%d: assert not a,(h,d,m,a)
                cases+=1
                total+=len(a)
    print(f'cross-check: {cases} grids, {total} six-point circles, exact set equality')
    for h in range(1,13):
        for d in range(1,13):
            if h%d==0:
                m,witness=explicit_witness(h,d)
                assert witness in chord_six(h,d,m)
    print('explicit existence: all divisible pairs h,d<=12 verified via independent chord equation')
    print('the theorem for unbounded h,d,m is mathematical; this finite audit is auxiliary')

if __name__=='__main__':main()
