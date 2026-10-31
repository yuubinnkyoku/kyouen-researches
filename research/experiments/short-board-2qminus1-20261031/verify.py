#!/usr/bin/env python3
"""Independent checks for N=2q-1 short-board classification, no dependencies."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import comb, lcm

def mex(values):
    s=set(values); k=0
    while k in s: k+=1
    return k

def predicted(q,a,b,c):
    u=q-1-a-c; v=q-1-b-c
    assert min(u,v)>=0 and 0<=c<=2
    if c==2: g=(u+v)%2
    elif c==1:
        t=min(u,v)
        g=(u+v)%2 if t==0 else (2+(u+v)%2 if t==1 else (u+v+1)%2)
    else:
        t=min(u,v)
        g=(u+v+1)%2 if t<=2 else (2+(u+v)%2 if t==3 else (u+v)%2)
    return g, (1-g if g<=1 else g)

def count_solver(q):
    A,B=q-1,q-2
    @lru_cache(None)
    def rec(a,b,c):
        children=[]
        for da,db,dc,available in ((1,0,0,a<A),(0,1,0,b<B),(0,0,1,c<2)):
            aa,bb,cc=a+da,b+db,c+dc
            if available and aa+cc<q and bb+cc<q:
                children.append(rec(aa,bb,cc))
        return (mex(v[0] for v in children),mex(v[1] for v in children)) if children else (0,1)
    for c in range(3):
        for a in range(A+1):
            for b in range(B+1):
                if a+c<q and b+c<q:
                    assert rec(a,b,c)==predicted(q,a,b,c),(q,a,b,c,rec(a,b,c))
    return rec(0,0,0),rec.cache_info().currsize

def integer_witness(q):
    # Two radius-5 rational circles, centers (0,0),(6,0), intersections (3,+/-4).
    def pt(t,shift):
        t=Fraction(t)
        return (Fraction(shift)+5*(1-t*t)/(1+t*t),10*t/(1+t*t))
    common=[(Fraction(3),Fraction(4)),(Fraction(3),Fraction(-4))]
    pts=[pt(t,0) for t in range(q-1)]
    pts += [pt(t,6) for t in [0,1,*range(3,q+1)][:q-2]]
    pts += common
    assert len(set(pts))==2*q-1
    scale=lcm(*(v.denominator for p in pts for v in p))
    return [(int(x*scale),int(y*scale)) for x,y in pts]

def collinear(p,a,b):
    return (a[0]-p[0])*(b[1]-p[1])==(a[1]-p[1])*(b[0]-p[0])

def concyclic(p,a,b,c):
    def row(v):
        return (v[0]*v[0]+v[1]*v[1]-p[0]*p[0]-p[1]*p[1],
                v[0]-p[0],v[1]-p[1])
    r,s,t=row(a),row(b),row(c)
    return (r[0]*(s[1]*t[2]-s[2]*t[1])
            -r[1]*(s[0]*t[2]-s[2]*t[0])
            +r[2]*(s[0]*t[1]-s[1]*t[0]))==0

def forbidden_q(points,q):
    edges=[]
    for ids in combinations(range(len(points)),q):
        pts=[points[i] for i in ids]
        p,a=pts[:2]
        if all(collinear(p,a,x) for x in pts[2:]):
            edges.append(ids);continue
        k=next(i for i in range(2,q) if not collinear(p,a,pts[i]))
        if all(concyclic(p,a,pts[k],x) for x in pts):
            edges.append(ids)
    return edges

def mask_solver(q,points,edges):
    n=len(points)
    forbidden=[sum(1<<i for i in e) for e in edges]
    safe=[not any((m&f)==f for f in forbidden) for m in range(1<<n)]
    g=[None]*(1<<n);h=[None]*(1<<n)
    states=sorted((m for m in range(1<<n) if safe[m]),key=int.bit_count,reverse=True)
    for m in states:
        children=[m|(1<<i) for i in range(n) if not (m>>i)&1 and safe[m|(1<<i)]]
        g[m],h[m]=(mex(g[x] for x in children),mex(h[x] for x in children)) if children else (0,1)
        a=(m&((1<<(q-1))-1)).bit_count()
        b=(m>>(q-1)&((1<<(q-2))-1)).bit_count()
        c=(m>>(2*q-3)).bit_count()
        assert (g[m],h[m])==predicted(q,a,b,c),(q,m,(g[m],h[m]),(a,b,c))
    return len(states),(g[0],h[0])

def main():
    for q in range(4,51):
        root,num=count_solver(q)
        assert root==((2,2) if q==4 else (0,1))
        if q in (4,5,6,7,8,10,20,50):
            print('count-recurrence',q,'states',num,'root',root)
    for q in range(4,9):
        points=integer_witness(q)
        edges=forbidden_q(points,q)
        c0,c1=2*q-3,2*q-2
        first=[*range(q-1),c0,c1]
        second=[*range(q-1,2*q-3),c0,c1]
        expected=set(combinations(first,q))|{tuple(second)}
        assert set(edges)==expected,(q,edges,expected)
        count,root=mask_solver(q,points,edges)
        print('integer-geometric-mask',q,'points',len(points),
              'forbidden',len(edges),'safe',count,'root',root)
    # Complete enumeration of subboards, using integer geometry on the full grid.
    for q,w,h in ((6,5,3),(7,4,4)):
        grid=[(x,y) for x in range(w) for y in range(h)]
        n=2*q-1
        full=forbidden_q(grid,q)
        masks=[sum(1<<i for i in e) for e in full]
        allowed={0,2,q+2}|{comb(m,q) for m in range(q,n+1)}
        counts=Counter()
        for ids in combinations(range(len(grid)),n):
            board=sum(1<<i for i in ids)
            f=sum((board&m)==m for m in masks)
            assert f in allowed,(q,ids,f)
            counts[f]+=1
        print('all-grid-subboards',q,f'{w}x{h}','boards',sum(counts.values()),
              'forbidden-count-frequency',sorted(counts.items()))
    # Two q-point forbidden edges, with one common vertex, or two and one free.
    for q in range(6,10):
        n=2*q-1
        e1=tuple(range(q))
        for label,e2 in (('overlap-one',tuple([q-1,*range(q,n)])),
                         ('overlap-two-exterior-one',tuple([0,1,*range(q,n-1)]))):
            forbidden=[sum(1<<i for i in e) for e in (e1,e2)]
            @lru_cache(None)
            def rec(mask):
                ch=[rec(mask|(1<<i)) for i in range(n)
                    if not (mask>>i)&1 and
                    all(((mask|(1<<i))&f)!=f for f in forbidden)]
                return (mex(x[0] for x in ch),mex(x[1] for x in ch)) if ch else (0,1)
            assert rec(0)==(1,0),(q,label,rec(0))
            print('two-q-carriers',q,label,'root',rec(0),
                  'states',rec.cache_info().currsize)
    print('PASS: all tests')

if __name__=='__main__':
    main()
