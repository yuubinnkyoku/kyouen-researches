#!/usr/bin/env python3
"""Independent direction-normalization/bitmask census for 2×k×m coplanar q=4."""
from itertools import combinations
from math import gcd

CASES = {(3,3):(1332,532),(3,4):(7528,592),(3,5):(26340,332),
         (3,6):(71826,18),(3,7):(164556,0),(4,4):(40368,304),
         (4,5):(139380,44),(4,6):(377096,0),(4,7):(857168,0)}

def direction(a,b):
    dy,dz=b[0]-a[0],b[1]-a[1]
    g=gcd(abs(dy),abs(dz))
    dy,dz=dy//g,dz//g
    if dy<0 or (dy==0 and dz<0): dy,dz=-dy,-dz
    return dy,dz

def census(k,m):
    points=[(y,z) for y in range(k) for z in range(m)]
    n=len(points)
    full=(1<<n)-1
    dirs={direction(points[u],points[v]) for u,v in combinations(range(n),2)}
    lines={}
    for u,(ay,az) in enumerate(points):
        for d in dirs:
            dy,dz=d
            lines[u,d]=sum(1<<v for v,(by,bz) in enumerate(points)
                           if (by-ay)*dz==(bz-az)*dy)
    pairs=[(u,v,direction(points[u],points[v]))
           for u,v in combinations(range(n),2)]
    safe=maximal=0
    witness=None
    for a,b,c in combinations(range(n),3):
        sides={direction(points[a],points[b]),
               direction(points[a],points[c]),
               direction(points[b],points[c])}
        if len(sides)!=3: continue
        d1,d2,d3=sides
        for u,v,db in pairs:
            if db in sides: continue
            safe+=1
            blocked=(lines[u,db]|lines[u,d1]|lines[v,d1]|
                     lines[u,d2]|lines[v,d2]|lines[u,d3]|lines[v,d3])
            if blocked==full:
                maximal+=1
                if witness is None:
                    witness=([points[i] for i in (a,b,c)],
                             [points[i] for i in (u,v)])
    return safe,maximal,witness

if __name__=="__main__":
    for (k,m),expected in CASES.items():
        safe,maximal,witness=census(k,m)
        assert (safe,maximal)==expected, ((k,m),(safe,maximal),expected)
        print(f"{k}x{m} safe={safe} maximal={maximal} witness={witness}")
