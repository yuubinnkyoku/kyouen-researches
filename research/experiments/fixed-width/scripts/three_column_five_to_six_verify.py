#!/usr/bin/env python3
"""Independent exact arithmetic audit for 5 -> 6 circles on three vertical lattice columns.

Usage: python three_column_five_to_six_verify.py
No third-party packages required.
"""
from fractions import Fraction
from itertools import combinations


def q(a, b, t):
    return b*t[0]**2 - (a+b)*t[1]**2 + a*t[2]**2


def lift(a, b, t, n):
    c = a+b
    ell = b*t[0] - c*t[1] + a*t[2]
    mu = a*b*(t[0]-t[2])
    w = (a, 0, -b)
    lam = 2*n*mu + 2*n*n*a*b*c*ell
    return tuple(t[i]+2*n*ell*w[i]-lam for i in range(3))


def circle_coefficients(points):
    # Three noncollinear points define x²+y²+U*x+V*y+W=0.
    (x0,y0),(x1,y1),(x2,y2)=points
    A=x1-x0; B=y1-y0; C=x2-x0; D=y2-y0
    e=-(x1*x1+y1*y1-x0*x0-y0*y0)
    f=-(x2*x2+y2*y2-x0*x0-y0*y0)
    det=A*D-B*C
    assert det
    U=Fraction(e*D-B*f,det)
    V=Fraction(A*f-e*C,det)
    W=-x0*x0-y0*y0-U*x0-V*y0
    return U,V,W


def independent_circle_check(a,b,d,t):
    assert all(z!=0 for z in t)
    xs=(0,a,a+b)
    pts=[(x,y) for x,v in zip(xs,t) for y in (-d*v,d*v)]
    assert len(set(pts))==6
    co=circle_coefficients((pts[0],pts[2],pts[4]))
    assert all(x*x+y*y+co[0]*x+co[1]*y+co[2]==0 for x,y in pts)
    assert co[1]==0
    return co


def tangent_examples():
    for a in range(1,9):
        for b in range(1,9):
            for d in range(1,7):
                if a*b*(a+b)%(d*d):
                    continue
                N=a*b*(a+b)//(d*d)
                for zero in range(3):
                    inds=[i for i in range(3) if i!=zero]
                    for x in range(1,24):
                        for y in range(1,24):
                            t=[0,0,0];t[inds[0]]=x;t[inds[1]]=y
                            if q(a,b,t)==-N:
                                yield a,b,d,tuple(t)
                                break
                        else:continue
                        break


def run():
    # All small signed vectors: polynomial invariance independent of geometry.
    algebra=0
    for a in range(1,7):
        for b in range(1,7):
            for t in ((0,3,4),(1,2,3),(-3,4,1),(4,-2,0),(0,0,1)):
                for n in (-3,-2,-1,0,1,2,3):
                    assert q(a,b,lift(a,b,t,n))==q(a,b,t)
                    algebra+=1
    examples=list(tangent_examples())
    assert examples
    lifted=0; distinct=set(); max_n=0
    for a,b,d,t in examples:
        assert t.count(0)==1
        assert d*d*q(a,b,t)==-a*b*(a+b)
        for n in range(1,15):
            s=lift(a,b,t,n)
            if all(s):
                independent_circle_check(a,b,d,s)
                assert q(a,b,s)==q(a,b,t)
                distinct.add((a,b,d,t))
                max_n=max(max_n,n)
                lifted+=1
                break
        else:raise AssertionError((a,b,d,t))
    # Concrete tangent circle (0,0),(1,+/-3),(2,+/-4) lifts to six points.
    t=(0,3,4)
    assert lift(1,1,t,1)==(12,19,24)
    assert independent_circle_check(1,1,1,(12,19,24))
    print(f'algebraic Q-invariance tests: {algebra}')
    print(f'distinct tangent 5-point examples: {len(distinct)}')
    print(f'constructed and independently checked 6-point circles: {lifted}')
    print(f'maximum first-success parameter n: {max_n}')
    print('witness: a=b=d=1, tangent t=(0,3,4) -> six-point t=(12,19,24)')


if __name__=='__main__':
    run()
