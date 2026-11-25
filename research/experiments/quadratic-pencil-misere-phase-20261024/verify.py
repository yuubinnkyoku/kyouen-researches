#!/usr/bin/env python3
"""Exact small-board normal/misere audit for quadratic-pencil placement games."""
from functools import lru_cache
from fractions import Fraction
from itertools import combinations
from math import comb
import json

def det3(a,b,c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
           -a[1]*(b[0]*c[2]-b[2]*c[0])
           +a[2]*(b[0]*c[1]-b[1]*c[0]))

def rank2(pts,ids,lam):
    p,q=lam.numerator,lam.denominator
    a,b,c=[(q*pts[i][0]**2+p*pts[i][1]**2,q*pts[i][0],q*pts[i][1]) for i in ids]
    u=[b[j]-a[j] for j in range(3)]
    v=[c[j]-a[j] for j in range(3)]
    return all(u[i]*v[j]==u[j]*v[i] for i in range(3) for j in range(i+1,3))

def run(w,m,lam):
    pts=[(x,y) for x in range(m) for y in range(w)]
    n=len(pts)
    p,q=lam.numerator,lam.denominator
    v=[(q*x*x+p*y*y,q*x,q*y) for x,y in pts]
    forbidden=[]
    for ids in combinations(range(n),4):
        a,b,c,d=[v[i] for i in ids]
        diff=[tuple(z[k]-a[k] for k in range(3)) for z in (b,c,d)]
        if det3(*diff)==0:
            forbidden.append(sum(1<<i for i in ids))
    bypoint=[[] for _ in pts]
    for mask in forbidden:
        for i in range(n):
            if mask>>i&1:
                bypoint[i].append(mask^(1<<i))

    @lru_cache(None)
    def solve(s):
        children=[]
        for i in range(n):
            if not s>>i&1 and not any((s&t)==t for t in bypoint[i]):
                children.append(solve(s|(1<<i)))
        if not children:
            return 0,1
        gs={g for g,h in children}
        hs={h for g,h in children}
        g=h=0
        while g in gs: g+=1
        while h in hs: h+=1
        return g,h

    solve(0)
    T=3+2*(comb(3*w-2,3)-(w-1)) if w>=2 else 3
    seen={0}
    todo=[0]
    wrong=swapwrong=same=g2=terminal3=0
    while todo:
        s=todo.pop()
        k=s.bit_count()
        g,h=solve(s)
        swapwrong+=(h!=(1-g if g<2 else g))
        same+=(bool(g)==bool(h))
        g2+=(w%2==0 and k==2 and g==2)
        if k==3:
            ids=tuple(i for i in range(n) if s>>i&1)
            terminal3+=rank2(pts,ids,lam)
        if m>=T:
            predicted=((3*w-k)%2==0) or (
                w%2==0 and k==3 and rank2(pts,tuple(i for i in range(n) if s>>i&1),lam))
            wrong+=(bool(h)!=predicted)
        for i in range(n):
            if not s>>i&1 and not any((s&t)==t for t in bypoint[i]):
                nxt=s|(1<<i)
                if nxt not in seen:
                    seen.add(nxt)
                    todo.append(nxt)
    result=dict(w=w,m=m,lambda_=str(lam),threshold=T,states=len(seen),
        forbidden4=len(forbidden),normal_empty=solve(0)[0],misere_empty_h=solve(0)[1],
        misere_empty_win=solve(0)[1]!=0,same_outcome=same,swap_mismatches=swapwrong,
        normal_nimber2_pairs=g2,rank2_triples=terminal3,
        misere_formula_mismatches=wrong if m>=T else None)
    if m>=T:
        assert wrong==0 and swapwrong==0 and same==g2, result
    return result

if __name__=="__main__":
    cases=[(1,3,Fraction(0)),(1,4,Fraction(1)),(2,9,Fraction(0)),
           (2,9,Fraction(-1)),(2,9,Fraction(1,2)),(2,10,Fraction(1)),
           (3,4,Fraction(-1)),(3,5,Fraction(0)),(4,4,Fraction(-1))]
    print(json.dumps([run(*x) for x in cases],ensure_ascii=False,indent=2))
