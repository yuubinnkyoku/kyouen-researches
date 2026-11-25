#!/usr/bin/env python3
"""Exact, independent checks for hyperplane-forbidden minimal terminals."""
from itertools import combinations, product
from math import gcd
from fractions import Fraction

def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def det(a,b,c): return sum(x*y for x,y in zip(cross(a,b),c))

def direct_count(n):
    p=list(product(*(range(x) for x in n)))
    return sum(cross(sub(q,p0),sub(r,p0))==(0,0,0)
               for p0,q,r in combinations(p,3))

def endpoint_count(n):
    total=0
    ranges=[range(-((x-1)//2),(x-1)//2+1) for x in n]
    for v in product(*ranges):
        if not any(v) or next(x for x in v if x)<0: continue
        if gcd(gcd(abs(v[0]),abs(v[1])),abs(v[2]))!=1: continue
        for k in range(2,max(n)+1):
            ways=1
            for side,step in zip(n,v): ways*=max(0,side-k*abs(step))
            if not ways: break
            total+=(k-1)*ways
    return total

def exhaustive(n):
    pts=list(product(*(range(x) for x in n)))
    m=len(pts); assert m<=27
    triples=list(combinations(range(m),3))
    index={t:i for i,t in enumerate(triples)}
    blocked_by=[0]*len(triples)
    for quad in combinations(range(m),4):
        a,b,c,d=(pts[i] for i in quad)
        if det(sub(b,a),sub(c,a),sub(d,a))==0:
            for tri in combinations(quad,3):
                other=next(x for x in quad if x not in tri)
                blocked_by[index[tri]] |= 1<<other
    safe=0; maximal={}
    def visit(chosen,start):
        nonlocal safe
        safe+=1
        used=sum(1<<i for i in chosen)
        blocked=0
        for tri in combinations(chosen,3): blocked|=blocked_by[index[tri]]
        if used|blocked==(1<<m)-1:
            maximal[len(chosen)]=maximal.get(len(chosen),0)+1
        for i in range(start,m):
            if not (blocked>>i)&1: visit(chosen+[i],i+1)
    visit([],0)
    return safe,maximal

def rank(points):
    a=[[Fraction(x-y) for x,y in zip(p,points[0])] for p in points[1:]]
    r=0
    for col in range(len(points[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][col]),None)
        if pivot is None: continue
        a[r],a[pivot]=a[pivot],a[r]
        f=a[r][col]; a[r]=[x/f for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][col]:
                f=a[i][col]; a[i]=[x-f*y for x,y in zip(a[i],a[r])]
        r+=1
    return r

def main():
    expected={(2,2,2):(159,{4:24,5:8}),
              (2,2,3):(857,{3:4,5:172}),
              (2,3,3):(6456,{3:16,5:1064,6:368}),
              (3,3,3):(72204,{3:49,5:2644,6:14616,7:752,8:16})}
    for n in [(2,2,2),(2,2,3),(2,3,3),(3,3,3),
              (3,3,4),(3,4,5),(4,4,4)]:
        a,b=direct_count(n),endpoint_count(n)
        assert a==b,(n,a,b)
        if n in expected:
            safe,maximal=exhaustive(n)
            assert (safe,maximal)==expected[n]
            assert maximal.get(3,0)==a
            print(n,a,safe,maximal)
        else: print(n,a)
    for d in range(4,9):
        witness=[(0,0)+v for v in product((0,1),repeat=d-2)][:d]
        assert len(witness)==d and rank(witness)<=d-2
        print('cube dimension',d,'witness rank',rank(witness))
    print('PASS')

if __name__=='__main__': main()
