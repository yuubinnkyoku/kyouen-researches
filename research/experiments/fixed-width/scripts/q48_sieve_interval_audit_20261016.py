#!/usr/bin/env python3
"""Independent exact-integer interval audit of the refined slope sieve constant."""
from fractions import Fraction
from math import isqrt
import json

def primes(limit):
    return [p for p in range(7,limit+1) if p%4==3 and all(p%d for d in range(2,isqrt(p)+1))]

def G(z,B):
    w=[Fraction(0)]*(z+1)
    w[1]=Fraction(1)
    for p in primes(z):
        if B%p==0:continue
        for j in range(z//p,0,-1):
            w[j*p]+=w[j]*Fraction(4,p-4)
    return sum(w)

def above_gap(A,B):
    return A>3*B and A**4-18*A*A*B*B+9*B**4>0

rows=[]
for H in (80,160,320,640):
    z=isqrt(H)
    tested=0
    total=0
    for B in range(1,H+1):
        first=next((A for A in range(1,H+1) if above_gap(A,B)),H+1)
        if first>H:continue
        length=H-first+1
        ps=[p for p in primes(z) if B%p]
        count=sum(all(A%p not in {(c*B)%p for c in (-3,-1,1,3)} for p in ps)
                  for A in range(first,H+1))
        assert count*G(z,B)<=length+z*z,(H,B)
        total+=count
        tested+=1
    rows.append({'H':H,'z':z,'denominators_with_A_above_gap':tested,'local_survivors_in_gap_region':total})
print(json.dumps({'status':'PASS','interval_large_sieve':rows},indent=2))
