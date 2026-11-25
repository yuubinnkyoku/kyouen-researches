#!/usr/bin/env python3
"""Independent checks for the 2q+1 two-carrier theorem; Python 3.10+."""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from math import comb


def types():
    return [(u, v, c, 1+c-u-v)
            for u in range(4) for v in range(u+1)
            for c in range(3) if 1+c-u-v >= 0]


def mex(values):
    values = set(values)
    k = 0
    while k in values:
        k += 1
    return k


def check_game(q, spec):
    u,v,c,z = spec
    x,y = q+u-c,q+v-c
    n = 2*q+1
    assert x+y+c+z == n
    aa = (1<<x)-1
    bb = ((1<<y)-1)<<x
    cc = ((1<<c)-1)<<(x+y)
    A,B = aa|cc,bb|cc

    @lru_cache(None)
    def counts(i,j,t,e):
        children = []
        if i<x and i+t<q-1: children.append(counts(i+1,j,t,e))
        if j<y and j+t<q-1: children.append(counts(i,j+1,t,e))
        if t<c and i+t<q-1 and j+t<q-1: children.append(counts(i,j,t+1,e))
        if e<z: children.append(counts(i,j,t,e+1))
        return (mex(v[0] for v in children),mex(v[1] for v in children)) if children else (0,1)

    @lru_cache(None)
    def direct(mask):
        children = []
        remaining = ((1<<n)-1)^mask
        while remaining:
            bit = remaining & -remaining
            remaining -= bit
            nxt = mask|bit
            if (nxt&A).bit_count()<q and (nxt&B).bit_count()<q:
                children.append(direct(nxt))
        return (mex(v[0] for v in children),mex(v[1] for v in children)) if children else (0,1)

    terminals = Counter()
    safe = 0
    for mask in range(1<<n):
        i,j,t,e = (mask&aa).bit_count(),(mask&bb).bit_count(),(mask&cc).bit_count(),(mask>>(x+y+c)).bit_count()
        if i+t>=q or j+t>=q: continue
        safe += 1
        assert direct(mask)==counts(i,j,t,e),(q,spec,mask)
        if not any(not (mask&(1<<k)) and
                   ((mask|(1<<k))&A).bit_count()<q and
                   ((mask|(1<<k))&B).bit_count()<q for k in range(n)):
            terminals[mask.bit_count()] += 1

    formula = Counter()
    for i in range(x+1):
        for j in range(y+1):
            for t in range(c+1):
                if i+t>=q or j+t>=q: continue
                if i<x and i+t<q-1: continue
                if j<y and j+t<q-1: continue
                if t<c and i+t<q-1 and j+t<q-1: continue
                formula[i+j+t+z] += comb(x,i)*comb(y,j)*comb(c,t)
    assert terminals==formula,(q,spec,terminals,formula)
    return safe,counts(0,0,0,0)


def enumerate_carriers(pts,q):
    def det(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    curves=set()
    for p,r,s in combinations(pts,3):
        if det(p,r,s)==0:
            A,B=r[1]-p[1],p[0]-r[0]
            C=-A*p[0]-B*p[1]
            d=A if A else B
            curves.add(('L',A/d,B/d,C/d))
        else:
            def norm(v): return v[0]*v[0]+v[1]*v[1]
            a,b=r[0]-p[0],r[1]-p[1]
            c,d=s[0]-p[0],s[1]-p[1]
            h=norm(p)-norm(r);k=norm(p)-norm(s)
            den=a*d-c*b
            D=(h*d-k*b)/den
            E=(a*k-c*h)/den
            G=-norm(p)-D*p[0]-E*p[1]
            curves.add(('C',D,E,G))
    result=[]
    for kind,A,B,C in curves:
        if kind=='L':
            members=frozenset(p for p in pts if A*p[0]+B*p[1]+C==0)
        else:
            members=frozenset(p for p in pts if p[0]**2+p[1]**2+A*p[0]+B*p[1]+C==0)
        if len(members)>=q: result.append(members)
    return set(result)


def check_geometry(q,spec):
    u,v,c,z=spec
    dx={0:12,1:10,2:6}[c]
    shared={0:[],1:[(F(5),F(0))],2:[(F(3),F(4)),(F(3),F(-4))]}[c]
    pts=list(shared)
    expected=[set(shared),set(shared)]
    for center,needed,target in ((0,q+u-c,expected[0]),(dx,q+v-c,expected[1])):
        t=1
        while needed:
            p=(F(center)+F(5*(1-t*t),1+t*t),F(10*t,1+t*t))
            if p not in pts:
                pts.append(p);target.add(p);needed-=1
            t+=1
    for k in range(z): pts.append((F(100+3*k),F(200+7*k)))
    assert len(pts)==2*q+1 and len(set(pts))==len(pts)
    assert enumerate_carriers(pts,q)=={frozenset(s) for s in expected}


def check_sharp(q=7):
    circles=[(F(0),F(0),F(5)),(F(6),F(0),F(5)),(F(2),F(-5),F(2))]
    pts=set([(F(3),F(4)),(F(3),F(-4)),(F(0),F(-5)),
             (F(100,29),F(-105,29)),(F(2),F(-3)),(F(162,41),F(-187,41))])
    def on(p,C):
        x,y,r=C
        return (p[0]-x)**2+(p[1]-y)**2==r*r
    for C in circles:
        needed=q-sum(on(p,C) for p in pts)
        assert needed==q-4
        t=1
        while needed:
            x,y,r=C
            p=(x+r*F(1-t*t,1+t*t),y+r*F(2*t,1+t*t))
            if p not in pts and not any(on(p,other) for other in circles if other is not C):
                pts.add(p);needed-=1
            t+=1
    assert len(pts)==3*q-6
    assert len(enumerate_carriers(pts,q))==3


def main():
    specs=types()
    assert len(specs)==12
    total=0
    for spec in specs:
        n,root=check_game(8,spec)
        check_geometry(8,spec)
        total+=n
        print('q=8',spec,'safe=',n,'root=',root)
    assert total==1510740
    check_sharp(7)
    print('PASS: 12 types, 1510740 safe states, exact geometry, sharp q=7 triple')


if __name__=='__main__':
    main()
