#!/usr/bin/env python3
"""Independent direct-factorization check of the 4-residue sieve weight."""
from fractions import Fraction
from math import isqrt
import json

def direct_weight(n):
    ans=Fraction(1)
    d=2
    while d*d<=n:
        if n%d==0:
            if n%(d*d)==0 or d<7 or d%4!=3:
                return Fraction(0)
            n//=d
            ans*=Fraction(4,d-4)
        d+=1
    if n>1:
        if n<7 or n%4!=3:
            return Fraction(0)
        ans*=Fraction(4,n-4)
    return ans

def dp_weights(limit):
    p=[True]*(limit+1)
    p[0]=p[1]=False
    for d in range(2,isqrt(limit)+1):
        if p[d]:
            for m in range(d*d,limit+1,d):p[m]=False
    f=[Fraction(0)]*(limit+1)
    f[1]=Fraction(1)
    for q in range(7,limit+1):
        if p[q] and q%4==3:
            for n in range(limit//q,0,-1):
                f[n*q]+=f[n]*Fraction(4,q-4)
    return f

limit=2000
f=dp_weights(limit)
assert all(f[n]==direct_weight(n) for n in range(1,limit+1))
for z in (100,200,500,1000,2000):
    g=sum(f[1:z+1])
    assert g==sum((direct_weight(n) for n in range(1,z+1)),Fraction(0))
    print(json.dumps({'z':z,'G_fraction':str(g),'G_float':float(g)}))
print('PASS: 2000 exact rational weights, five partial sums; direct trial factorization vs independent DP')
