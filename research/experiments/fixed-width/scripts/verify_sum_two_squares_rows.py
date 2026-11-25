#!/usr/bin/env python3
"""Independent Gaussian-product and integer-square checks for circle row witnesses."""
from itertools import product
from math import isqrt, prod

primes = {5:(1,2), 13:(2,3), 17:(1,4), 29:(2,5)}
cases = [(55250,{5:3,13:1,17:1},32,235),
         (143650,{5:2,13:2,17:1},36,379),
         (320450,{5:2,13:1,17:1,29:1},48,565)]

def mul(z,w):
    a,b=z; c,d=w
    return a*c-b*d,a*d+b*c

def power(z,n):
    v=(1,0)
    for _ in range(n): v=mul(v,z)
    return v

def gaussian(factors):
    opts=[]
    for p,e in factors.items():
        a,b=primes[p]
        opts.append([mul(power((a,b),j),power((a,-b),e-j))
                     for j in range(e+1)])
    out=set()
    for choice in product(*opts):
        z=(1,1)
        for factor in choice: z=mul(z,factor)
        for u in [(1,0),(-1,0),(0,1),(0,-1)]:
            out.add(mul(z,u))
    return out

def direct(n):
    out=set()
    for b in range(-isqrt(n),isqrt(n)+1):
        a=isqrt(n-b*b)
        if a*a+b*b==n:
            out.add((a,b)); out.add((-a,b))
    return out

for n,f,k,m in cases:
    assert n==2*prod(p**e for p,e in f.items())
    a,b=gaussian(f),direct(n)
    assert a==b and len(a)==4*prod(e+1 for e in f.values())
    ys=[]
    d=(1+m*m-n)//4
    assert 4*d==1+m*m-n
    for v in sorted({y for x,y in a if x>0}):
        assert v%2 and abs(v)<=m
        x=isqrt(n-v*v)
        y=(v+m)//2
        for xx in [(-1+x)//2,(-1-x)//2]:
            assert xx*xx+y*y+xx-m*y+d==0
        ys.append(y)
    assert len(ys)==k and ys[0]==0 and ys[-1]==m
    if n==55250: assert sum(y<=210 for y in ys)==25
    print(n,'rows',k,'width',m+1,'D',d,'ys',ys)
print('PASS independent exact methods')
