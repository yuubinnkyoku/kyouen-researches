#!/usr/bin/env python3
"""Two independent exact audits of H5=3, H6=2t+1 for (a,b,d)=(1,t*t-1,t).

No floating point, no third-party dependencies. Run from repository root.
"""
from collections import defaultdict
from math import gcd, isqrt


def canonical_circle(p, q, r):
    """Exact integer coefficients (A,B,C,D) for A(x^2+y^2)+Bx+Cy+D=0."""
    x1,y1=p; x2,y2=q; x3,y3=r
    z1=x1*x1+y1*y1; z2=x2*x2+y2*y2; z3=x3*x3+y3*y3
    A=x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2)
    if A==0: return None
    B=-(z1*(y2-y3)+z2*(y3-y1)+z3*(y1-y2))
    C=-(x1*(z2-z3)+x2*(z3-z1)+x3*(z1-z2))
    D=-(x1*(y2*z3-y3*z2)+x2*(y3*z1-y1*z3)+x3*(y1*z2-y2*z1))
    h=0
    for v in (A,B,C,D): h=gcd(h,v)
    A//=h; B//=h; C//=h; D//=h
    if A<0: A,B,C,D=-A,-B,-C,-D
    return A,B,C,D


def triple_audit(t):
    m=2*t+1
    pts=[(x,t*j,j) for x in (0,1,t*t) for j in range(m)]
    circles=set()
    n=len(pts)
    for i in range(n):
        for j in range(i+1,n):
            for k in range(j+1,n):
                c=canonical_circle(pts[i][:2],pts[j][:2],pts[k][:2])
                if c is not None: circles.add(c)
    h5=h6=10**9
    count6=0
    for A,B,C,D in circles:
        rows=sorted(j for x,y,j in pts if A*(x*x+y*y)+B*x+C*y+D==0)
        if len(rows)>=5:
            h5=min(h5,min(rows[i+4]-rows[i]+1 for i in range(len(rows)-4)))
        if len(rows)>=6:
            h6=min(h6,min(rows[i+5]-rows[i]+1 for i in range(len(rows)-5)))
            count6+=1
    assert (h5,h6)==(3,2*t+1),(t,h5,h6)
    return len(circles),count6


def chord_audit(t):
    # Any six-point circle with height <=2t+1 has all D_i in [1,2t].
    # Equation: t^2*(D1^2-D0^2-4)=D2^2-D0^2-4.
    witnesses=[]
    for D0 in range(1,2*t+1):
        for D2 in range(1,2*t+1):
            numer=(t*t-1)*(D0*D0+4)+D2*D2
            if numer%(t*t): continue
            D1=isqrt(numer//(t*t))
            if D1*D1*t*t!=numer: continue
            if D1==0 or (D0-D1)%2 or (D0-D2)%2: continue
            if max(D0,D1,D2)<=2*t:
                witnesses.append((D0,D1,D2))
    assert witnesses, t
    assert min(max(v)+1 for v in witnesses)==2*t+1,(t,witnesses)
    return len(witnesses)


def main():
    print('exact chord audit: t=2..50')
    for t in range(2,51):
        n=chord_audit(t)
        if t in (2,3,4,5,10,20,30,40,50):print(f'  t={t:2} H5=3 H6={2*t+1:3} six-chord-solutions={n}')
    print('independent determinant/triple audit: t=2..9')
    for t in range(2,10):
        n,c=triple_audit(t)
        print(f'  t={t:2} H5=3 H6={2*t+1:2} distinct-circles={n} six-circles={c}')
    print('PASS: all exact assertions')

if __name__=='__main__':main()
