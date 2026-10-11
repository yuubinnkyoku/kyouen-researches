#!/usr/bin/env python3
"""Independent pair-line enumeration against the d-dimensional run identity."""
from itertools import product, combinations
from math import comb, gcd
from collections import defaultdict


def directions(shape, q):
    bounds = [(n-1)//(q-1) for n in shape]
    for v in product(*(range(-b,b+1) for b in bounds)):
        if not any(v):
            continue
        if next(z for z in v if z) < 0:
            continue
        g=0
        for z in v:
            g=gcd(g,abs(z))
        if g==1:
            yield v


def A(shape,v,k):
    result=1
    for n,z in zip(shape,v):
        result*=max(0,n-(k-1)*abs(z))
    return result


def formula(shape,q):
    total=0
    histogram=defaultdict(int)
    for v in directions(shape,2):
        for k in range(2,max(shape)+1):
            e=A(shape,v,k)-2*A(shape,v,k+1)+A(shape,v,k+2)
            assert e>=0,(shape,v,k,e)
            histogram[k]+=e
            if k>=q:total+=e*comb(k,q)
    return total,{k:v for k,v in histogram.items() if v}


def brute(shape,q):
    pts=list(product(*(range(n) for n in shape)))
    lines=defaultdict(set)
    for i,j in combinations(range(len(pts)),2):
        a,b=pts[i],pts[j]
        delta=tuple(y-x for x,y in zip(a,b))
        g=0
        for z in delta:g=gcd(g,abs(z))
        v=tuple(z//g for z in delta)
        if next(z for z in v if z)<0:v=tuple(-z for z in v)
        start=a
        while all(0<=x-z<n for x,z,n in zip(start,v,shape)):
            start=tuple(x-z for x,z in zip(start,v))
        lines[v,start].update((i,j))
    histogram=defaultdict(int)
    for ids in lines.values():histogram[len(ids)]+=1
    return sum(comb(len(ids),q) for ids in lines.values() if len(ids)>=q),dict(histogram)


def main():
    cases=0
    for d in (2,3,4):
        max_n=4 if d==2 else 3 if d==3 else 2
        for shape in product(range(1,max_n+1),repeat=d):
            if __import__('math').prod(shape)>40:continue
            for q in range(2,max(shape)+2):
                got=formula(shape,q)
                expected=brute(shape,q)
                assert got==expected,(shape,q,got,expected)
                cases+=1
    print('independent box/q comparisons',cases)
    for shape in [(3,3,3),(2,3,4),(2,2,2,2),(3,3,3,2),(4,4)]:
        for q in (2,3,4):
            if __import__('math').prod(shape)>40:continue
            print(shape,'q=',q,'H=',formula(shape,q)[0])

if __name__=='__main__':main()
