#!/usr/bin/env python3
"""All-real parameter classification for x=0..4, y=0..2."""
from fractions import Fraction
from itertools import combinations
from collections import Counter
import json

def det3(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
          - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
          + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))

def polynomial(pts):
    x0,y0=pts[0]
    a=[(x*x-x0*x0,x-x0,y-y0) for x,y in pts[1:]]
    b=[(y*y-y0*y0,x-x0,y-y0) for x,y in pts[1:]]
    return det3(a),det3(b)

def main():
    pts=[(x,y) for x in range(5) for y in range(3)]
    n=len(pts)
    quads=[]
    roots=set()
    always=0
    for ids in combinations(range(n),4):
        a,b=polynomial([pts[i] for i in ids])
        mask=sum(1<<i for i in ids)
        if a==b==0:always+=1
        elif b:roots.add(Fraction(-a,b))
        quads.append((mask,a,b))
    roots=sorted(roots)
    generic=next(Fraction(k) for k in range(100) if Fraction(k) not in roots)
    cases=[("generic",generic)]+[(str(v),v) for v in roots]
    full=(1<<n)-1
    result=[]
    for name,lam in cases:
        forb=[mask for mask,a,b in quads if a+b*lam==0]
        bad=bytearray(full+1)
        for mask in forb:bad[mask]=1
        for mask in range(1,full+1):
            if bad[mask]:continue
            t=mask
            while t:
                bit=t&-t
                if bad[mask^bit]:
                    bad[mask]=1
                    break
                t-=bit
        g=[-1]*(full+1)
        safe=Counter()
        maximal=Counter()
        for mask in range(full,-1,-1):
            if bad[mask]:continue
            safe[mask.bit_count()]+=1
            moves={g[mask|(1<<i)] for i in range(n)
                   if not (mask>>i&1) and not bad[mask|(1<<i)]}
            if not moves:maximal[mask.bit_count()]+=1
            v=0
            while v in moves:v+=1
            g[mask]=v
        result.append(dict(lambda_value=name,root_grundy=g[0],
                           safe_positions=sum(safe.values()),
                           forbidden_quadruples=len(forb),
                           winning_first_moves=[list(pts[i]) for i in range(n)
                                                if g[1<<i]==0],
                           safe_size_distribution=dict(sorted(safe.items())),
                           maximal_size_distribution=dict(sorted(maximal.items()))))
    print(json.dumps(dict(board="3 rows x 5 columns",points=pts,
                          always_forbidden=always,
                          exceptional_values=[str(v) for v in roots],
                          cases=result),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
