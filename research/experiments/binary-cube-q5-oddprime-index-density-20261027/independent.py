#!/usr/bin/env python3
"""Independent exact common-order computation, not a power-residue test."""
import math
import sys

limit = int(sys.argv[1]) if len(sys.argv)>1 else 1000000
if not 37 <= limit <= 1000000:
    raise SystemExit('37 <= limit <= 1000000 required')
spf = list(range(limit))
for x in range(2, math.isqrt(limit-1)+1):
    if spf[x] == x:
        for y in range(x*x,limit,x):
            if spf[y] == y:
                spf[y] = x
ell = (3,5,7,11,13,17,19)
counts = {(q,r):0 for q in ell for r in (1,2,3)}
first = {(q,r):0 for q in ell for r in (1,2,3)}
primes = 0
for p in range(37,limit,2):
    if spf[p] != p:
        continue
    primes += 1
    n = p-1
    fac=[]
    while n>1:
        q=spf[n]
        fac.append(q)
        while n%q==0:
            n//=q
    period = p-1
    for q in fac:
        while period%q==0 and all(pow(a,period//q,p)==1 for a in (2,3,5,7)):
            period//=q
    idx=(p-1)//period
    for q in ell:
        for r in (1,2,3):
            if idx%(q**r)==0:
                counts[q,r]+=1
                if first[q,r]==0:first[q,r]=p
print('limit=',limit,'primes=',primes)
for q in ell:
    for r in (1,2,3):
        print('ell=',q,'r=',r,'count=',counts[q,r],'first=',first[q,r])
