#!/usr/bin/env python3
"""Exact q-point forbidden-overlap distribution from primitive integer curve equations."""
from collections import defaultdict,Counter
from itertools import combinations
from math import comb,gcd
from functools import reduce
import json,sys

def normalize(vals):
    g=reduce(gcd,(abs(x) for x in vals))
    if g==0: raise AssertionError(vals)
    v=tuple(x//g for x in vals)
    if next(x for x in v if x)!=abs(next(x for x in v if x)):
        v=tuple(-x for x in v)
    return v

def curve(a,b,c):
    x,y=a; dx,dy=b[0]-x,b[1]-y; ex,ey=c[0]-x,c[1]-y
    delta=dx*ey-ex*dy
    if not delta:
        return ('L',)+normalize((dy,-dx,dx*y-dy*x))
    u=-(b[0]**2+b[1]**2-x*x-y*y)
    v=-(c[0]**2+c[1]**2-x*x-y*y)
    A=u*ey-v*dy; B=dx*v-ex*u; C=-delta*(x*x+y*y)-A*x-B*y
    return ('C',)+normalize((delta,A,B,C))

def all_curves(n):
    pts=[(x,y) for y in range(n) for x in range(n)]
    masks={}
    for i,j,k in combinations(range(len(pts)),3):
        key=curve(pts[i],pts[j],pts[k]); masks[key]=masks.get(key,0)|(1<<i)|(1<<j)|(1<<k)
    return pts,masks

def calc(n,q):
    pts,curves=all_curves(n); N=len(pts)
    d1=[0]*N; d2=defaultdict(int)
    moments=[0]*q; total=0; hist_k=Counter()
    for key,mask in curves.items():
        k=mask.bit_count()
        if k<q: continue
        hist_k[(key[0],k)]+=1
        total+=comb(k,q)
        indices=[i for i in range(N) if mask>>i&1]
        weight1=comb(k-1,q-1);weight2=comb(k-2,q-2)
        for i in indices:d1[i]+=weight1
        for a,b in combinations(indices,2):d2[(a,b)]+=weight2
        for t in range(3,q):
            moments[t]+=comb(k,t)*comb(comb(k-t,q-t),2)
    moments[0]=comb(total,2)
    moments[1]=sum(comb(v,2) for v in d1)
    moments[2]=sum(comb(v,2) for v in d2.values())
    O=[sum((-1)**(t-j)*comb(t,j)*moments[t] for t in range(j,q)) for j in range(q)]
    assert min(O)>=0 and sum(O)==moments[0]
    return dict(n=n,q=q,forbidden=total,curve_length_counts={f'{t}{k}':v for (t,k),v in sorted(hist_k.items())},moments=moments,overlap=O,unique_support_curves=sum(hist_k.values()))

if __name__=='__main__':
    for n,q in [(3,4),(4,4),(5,4),(4,5),(5,5),(7,5),(11,5)]:
        r=calc(n,q);print(json.dumps(r,ensure_ascii=False),flush=True)
