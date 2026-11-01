#!/usr/bin/env python3
"""Independent exact checks of K_{a,b} graph-star terminal polynomials."""
from collections import Counter
from fractions import Fraction
from math import comb


def formula(a, b, r):
    n = 1 + a + b + r*a*b
    p = Counter({n-1: 1})
    p[n-a] += 1
    p[n-b] += 1
    for i in range(1, a+1):
        for j in range(1, b+1):
            p[n-a-b+i+j-i*j] += comb(a,i)*comb(b,j)*r**(i*j)
    return p


def enumerate_hypergraph(a, b, r):
    n = 1 + a + b + r*a*b
    edges = []
    k = 1+a+b
    for i in range(a):
        for j in range(b):
            h = (1<<0) | (1<<(1+i)) | (1<<(1+a+j))
            for t in range(r):
                h |= 1<<(k+t)
            edges.append(h)
            k += r
    p = Counter()
    full = (1<<n)-1
    for mask in range(1<<n):
        if any((mask & h)==h for h in edges):
            continue
        outside = full ^ mask
        maximal = True
        while outside:
            bit = outside & -outside
            outside -= bit
            if not any(((mask | bit)&h)==h for h in edges):
                maximal = False
                break
        if maximal:
            p[mask.bit_count()] += 1
    return p


def enumerate_D(a,b,r):
    n=1+a+b+r*a*b
    p=Counter({n-1:1})
    for x in range(1<<a):
        for y in range(1<<b):
            xa=x.bit_count()
            yb=y.bit_count()
            if x and yb==b:
                continue
            if y and xa==a:
                continue
            e0=(a-xa)*(b-yb)
            p[n-xa-yb-e0] += r**e0
    return p


def exact_error(a,b,r):
    t=sum(formula(a,b,r).values())
    return Fraction(t,r**(a*b)) - (1+Fraction(1,r**a))**b


def main():
    cases=0
    masks=0
    for a in range(2,4):
        for b in range(a,5):
            for r in (1,2):
                n=1+a+b+r*a*b
                if n>18:
                    continue
                expected=formula(a,b,r)
                actual=enumerate_hypergraph(a,b,r)
                assert expected==actual,(a,b,r,expected,actual)
                cases+=1
                masks+=2**n
    print(f'direct hypergraph exhaustive: {cases} cases, {masks:,} masks; exact match')
    cases=0
    for a in range(2,7):
        for b in range(a,9):
            for r in (1,2,3,4):
                assert enumerate_D(a,b,r)==formula(a,b,r),(a,b,r)
                cases+=1
    print(f'independent vertex-mask D(G) enumeration: {cases} cases; exact match')
    cases=0
    for a in range(2,8):
        for b in range(a,22):
            for r in (2,3,4):
                err=abs(exact_error(a,b,r))
                bound=Fraction(b+2,1)*Fraction(3,4)**b
                assert err<=bound,(a,b,r,err,bound)
                cases+=1
    print(f'uniform exponential error inequality: {cases} exact-rational cases; all hold')
    for a,b,r in ((2,3,1),(2,3,2),(3,3,2),(4,8,2),(7,128,2)):
        if b<=8:
            print(f'K_{{{a},{b}}}, r={r}: T={sum(formula(a,b,r).values())}, M={r**(a*b)}')
        else:
            z=Fraction(b,r**a)
            ratio=Fraction(r**(a*b),sum(formula(a,b,r).values()))
            print(f'K_{{{a},{b}}}, r={r}: b/r^a={float(z):.6f}, M/T={float(ratio):.6f}')


if __name__=='__main__':
    main()
