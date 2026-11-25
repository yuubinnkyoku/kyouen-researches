#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent audit for the full z=7, y>=4 two-token theorem (K0976).

The universal proof is the S=x+y strong induction and the finite d=x-y
A/B/C signature table in report.md. This verifier independently checks:
  * the K0976 closed form against direct canonical-multiset mex recursion;
  * the A/B/C reconstruction from K0979 and K0974;
  * signature-table coverage, exact signatures and mex;
  * K0979 and K0974 anchor transcriptions;
  * the K0832 tail, height-only reduction and Theorem-T parity bounds.
"""
from functools import lru_cache
import json
import random

def O(a,b,r): return a <= r <= b and r % 2 == 1
def E(a,b,r): return a <= r <= b and r % 2 == 0
def I(a,r): return r >= a

@lru_cache(maxsize=None)
def direct(R, X, z):
    if R == 0:
        return 0
    opts=set()
    seen=set()
    for i,v in enumerate(X):
        if v in seen:
            continue
        seen.add(v)
        if v>1:
            child=tuple(sorted(X[:i]+X[i+1:]+(v-1,)))
            opts.add(direct(R-1,child,z))
        else:
            child=tuple(sorted(X[:i]+X[i+1:]))
            opts.add(direct(R-1,child,z+1))
    if z>=1:
        opts.add(1 ^ direct(R-1,X,z-1))
    m=0
    while m in opts:
        m+=1
    return m

def single(x,z,R):
    if R==0 or x<=0:
        return 0
    if z==0:
        return min(R,x)%2
    if z==x:
        if R%2 and R<=2*x-1:
            return 2
        if R%2==0 and R<=x-1:
            return 0
        return x%2
    if 1<=z<=x-1:
        q=z if z%2 else z-1
        if R<=q:
            return 2 if R%2 else 0
        if q<R<x+z:
            return (R+z)%2
        return x%2
    if z>=x+1:
        q=x if x%2 else x-1
        if R<=q:
            return 2 if R%2 else 0
        return x%2
    raise ValueError((x,z,R))

def z7_y3(x,R):
    if R==0:
        return 0
    T=(
        (x==3 and R in (1,3,5)) or
        (x==4 and R in (1,3,5,7,9)) or
        (x in (5,7,8,9) and R in (1,3,5,7)) or
        (x==6 and R in (1,3,5,7,11)) or
        (x==10 and R in (1,3,5,7,13)) or
        (x==11 and (R in (1,3,5,7,13) or O(15,21,R))) or
        (x>=12 and R in (1,3,5,7,13))
    )
    P=(
        (x==4 and (R in (8,10) or I(11,R))) or
        (x==5 and R in (8,10)) or
        (x==6 and (R in (8,10) or I(12,R))) or
        (x==7 and R in (8,10)) or
        (x==8 and (R in (8,10) or I(12,R))) or
        (x==9 and R in (8,10,12)) or
        (x==10 and (R in (8,10,12) or I(14,R))) or
        (x==11 and R in (8,10,12)) or
        (x>=12 and x%2==0 and (R in (8,10,12) or O(15,x+9,R) or I(x+11,R))) or
        (x>=13 and x%2==1 and (R in (8,10,12) or O(15,x+10,R)))
    )
    return 2 if T else 1 if P else 0

def z6_y_ge4(x,y,R):
    if R==0:
        return 0
    d=x-y
    S=x+y
    T=(
        (R in (1,3,5)) or
        (d==0 and R==2*y+3) or
        (d==4 and R==2*y+5) or
        (d==7 and R in (2*y+7,2*y+9,2*y+11,2*y+13)) or
        (d>=8 and R==2*y+7)
    )
    P=(
        (d==0 and O(7,2*y+1,R)) or
        (d==1 and (O(7,10**9,R) or E(2*y+4,10**9,R))) or
        (d==2 and O(7,2*y+3,R)) or
        (d==3 and (O(7,10**9,R) or E(2*y+6,10**9,R))) or
        (d==4 and O(7,2*y+3,R)) or
        (d==5 and (O(7,10**9,R) or E(2*y+6,10**9,R))) or
        (d==6 and O(7,2*y+5,R)) or
        (d>=7 and d%2==1 and (O(7,2*y+5,R) or E(2*y+8,10**9,R) or O(S+8,10**9,R))) or
        (d>=8 and d%2==0 and (O(7,2*y+5,R) or E(2*y+8,S+6,R)))
    )
    return 2 if T else 1 if P else 0

def candidate(x,y,R):
    if R==0:
        return 0
    d=x-y
    S=x+y
    T=(
        R in (1,3,5,7) or
        (d==3 and R==2*y+5) or
        (d==7 and R==2*y+7) or
        (d==8 and R in (2*y+7,2*y+9,2*y+11,2*y+13,2*y+15)) or
        (d>=9 and R==2*y+7)
    )
    P=(
        (d==0 and E(8,2*y+2,R)) or
        (d==1 and (E(8,2*y+8,R) or O(2*y+5,2*y+7,R))) or
        (d==2 and E(8,2*y+4,R)) or
        (d==3 and (E(8,2*y+10,R) or O(2*y+7,2*y+9,R))) or
        (d==4 and E(8,2*y+4,R)) or
        (d==5 and (E(8,2*y+12,R) or O(2*y+7,2*y+11,R))) or
        (d==6 and E(8,2*y+6,R)) or
        (d==7 and (E(8,2*y+14,R) or O(2*y+9,2*y+13,R))) or
        (d==8 and E(8,2*y+6,R)) or
        (d>=9 and (E(8,2*y+6,R) or O(2*y+9,min(2*y+2*d-3,S+7),R)))
    )
    if T:
        return 2
    if P:
        return 1
    if R>=S+8:
        return S%2
    return 0

def options_from_anchors(x,y,R):
    if R==0:
        return set()
    r=R-1
    d=x-y
    opts=set()
    if d==0:
        if y==4:
            opts.add(z7_y3(y,r))
        else:
            opts.add(candidate(y,y-1,r))
    else:
        opts.add(candidate(x-1,y,r))
        if y==4:
            opts.add(z7_y3(x,r))
        else:
            opts.add(candidate(x,y-1,r))
    opts.add(1 ^ z6_y_ge4(x,y,r))
    return opts

def mex(opts):
    m=0
    while m in opts:
        m+=1
    return m

def signature(opts):
    return "".join(str(v) for v in sorted(opts))

def bands(y,d):
    if d==0 and y==4:
        return [(1,1,7,"01"),(1,9,15,"1"),
                (0,2,6,"23"),(0,8,10,"02"),(0,12,12,"13"),(0,14,14,"1")]
    if d==0:
        return [(1,1,7,"01"),(1,9,2*y+7,"1"),
                (0,2,6,"23"),(0,8,8,"02"),(0,10,2*y+2,"0"),
                (0,2*y+4,2*y+4,"13"),(0,2*y+6,2*y+6,"1")]
    if d==1:
        return [(1,1,7,"01"),(1,9,2*y+3,"1"),(1,2*y+5,2*y+7,"0"),
                (0,2,6,"23"),(0,8,8,"02"),(0,10,2*y+8,"0")]
    if d==2:
        return [(1,1,7,"01"),(1,9,2*y+9,"1"),
                (0,2,6,"23"),(0,8,8,"02"),(0,10,2*y+2,"0"),
                (0,2*y+4,2*y+4,"02"),(0,2*y+6,2*y+8,"1")]
    if d==3:
        return [(1,1,7,"01"),(1,9,2*y+3,"1"),(1,2*y+5,2*y+5,"01"),
                (1,2*y+7,2*y+9,"0"),
                (0,2,6,"23"),(0,8,8,"02"),(0,10,2*y+10,"0")]
    if d==4:
        return [(1,1,7,"01"),(1,9,2*y+11,"1"),
                (0,2,6,"23"),(0,8,8,"02"),(0,10,2*y+4,"0"),
                (0,2*y+6,2*y+6,"123"),(0,2*y+8,2*y+10,"1")]
    if d==5:
        return [(1,1,7,"01"),(1,9,2*y+5,"1"),(1,2*y+7,2*y+11,"0"),
                (0,2,6,"23"),(0,8,8,"02"),(0,10,2*y+12,"0")]
    if d==6:
        return [(1,1,7,"01"),(1,9,2*y+13,"1"),
                (0,2,6,"23"),(0,8,8,"02"),(0,10,2*y+4,"0"),
                (0,2*y+6,2*y+6,"02"),(0,2*y+8,2*y+12,"1")]
    if d==7:
        return [(1,1,7,"01"),(1,9,2*y+5,"1"),(1,2*y+7,2*y+7,"01"),
                (1,2*y+9,2*y+13,"0"),
                (0,2,6,"23"),(0,8,8,"02"),(0,10,2*y+4,"0"),
                (0,2*y+6,2*y+6,"02"),(0,2*y+8,2*y+14,"023")]
    if d==8:
        return [(1,1,7,"01"),(1,9,2*y+5,"1"),(1,2*y+7,2*y+15,"01"),
                (0,2,6,"23"),(0,8,8,"02"),(0,10,2*y+4,"0"),
                (0,2*y+6,2*y+6,"02"),(0,2*y+8,2*y+8,"123"),
                (0,2*y+10,2*y+14,"1")]
    if d>=9:
        S=2*y+d
        return [(1,1,7,"01"),(1,9,2*y+5,"1"),(1,2*y+7,2*y+7,"01"),
                (1,2*y+9,min(2*y+2*d-3,S+7),"0"),
                (0,2,6,"23"),(0,8,8,"02"),(0,10,2*y+4,"0"),
                (0,2*y+6,2*y+6,"02"),(0,2*y+8,2*y+8,"123"),
                (0,2*y+10,S+7,"12" if d==9 else "1")]
    raise ValueError((y,d))

def main():
    audit={"verifier":"verify_z7_y_ge4_proof.py","target":"H(R;(x,y);7), x>=y>=4, R>=0","checks":{}}
    ok=True
    n=bad=0
    for y in range(4,11):
        for d in range(16):
            x=y+d; S=x+y
            for R in range(S+31):
                n+=1
                if direct(R,(y,x),7)!=candidate(x,y,R): bad+=1
    audit["checks"]["direct_vs_closed_form"]={"range":"4<=y<=10, 0<=d<=15, 0<=R<=S+30","points":n,"mismatches":bad}
    ok &= bad==0
    n=bad=0
    for y in range(4,11):
        for d in range(16):
            x=y+d; S=x+y
            for R in range(S+31):
                n+=1
                if direct(R,(y,x),7)!=mex(options_from_anchors(x,y,R)): bad+=1
    audit["checks"]["direct_vs_ABC_mex"]={"range":"4<=y<=10, 0<=d<=15, 0<=R<=S+30","points":n,"mismatches":bad}
    ok &= bad==0
    n=bad=0
    for x in range(3,61):
        for R in range(x+41):
            n+=1
            if direct(R,(3,x),7)!=z7_y3(x,R): bad+=1
    audit["checks"]["K0979_anchor_vs_direct"]={"range":"3<=x<=60, 0<=R<=x+40","points":n,"mismatches":bad}
    ok &= bad==0
    n=bad=0
    for y in range(4,11):
        for d in range(16):
            x=y+d; S=x+y
            for R in range(S+31):
                n+=1
                if direct(R,(y,x),6)!=z6_y_ge4(x,y,R): bad+=1
    audit["checks"]["K0974_anchor_vs_direct"]={"range":"4<=y<=10, 0<=d<=15, 0<=R<=S+30","points":n,"mismatches":bad}
    ok &= bad==0
    n=bc=bs=bm=0
    for y in range(4,101):
        for d in range(41):
            x=y+d; S=x+y
            for R in range(1,S+8):
                n+=1
                matches=[sig for p,a,b,sig in bands(y,d) if R%2==p and a<=R<=b]
                if len(matches)!=1: bc+=1; continue
                opts=options_from_anchors(x,y,R)
                if signature(opts)!=matches[0]: bs+=1; continue
                if mex(opts)!=candidate(x,y,R): bm+=1
    audit["checks"]["symbolic_band_cover_signature_mex"]={"range":"4<=y<=100, 0<=d<=40, 1<=R<=S+7","points":n,"coverage_errors":bc,"signature_errors":bs,"mex_errors":bm}
    ok &= bc==bs==bm==0
    n=bad=0
    for y in range(4,501):
        for d in (0,1,2,3,4,5,6,7,8,9,10,11,20,50,100):
            S=2*y+d
            for R in (S+8,S+9,S+10,S+11):
                n+=1
                if candidate(y+d,y,R)!=S%2: bad+=1
    audit["checks"]["tail"]={"range":"4<=y<=500, d in {0..11,20,50,100}, R=S+8..S+11","points":n,"mismatches":bad}
    ok &= bad==0
    n=bad=0
    for y in range(4,201):
        for d in range(31):
            S=2*y+d
            for R in range(9):
                n+=1
                if candidate(y+d,y,R)!=single(S,7,R): bad+=1
    audit["checks"]["height_only_reduction"]={"range":"4<=y<=200, 0<=d<=30, 0<=R<=8","points":n,"mismatches":bad}
    ok &= bad==0
    n=be=bo=0
    for y in range(4,101):
        for d in range(31):
            x=y+d; S=x+y
            for R in range(S+21):
                n+=1; g=candidate(x,y,R)
                if R%2==0 and g>1: be+=1
                if R%2==1 and g>2: bo+=1
    audit["checks"]["theorem_T_parity"]={"range":"4<=y<=100, 0<=d<=30, 0<=R<=S+20","points":n,"even_parent_gt1":be,"odd_parent_gt2":bo}
    ok &= be==bo==0
    rng=random.Random(20261119); pts=set()
    while len(pts)<2500:
        y=rng.randrange(4,31); d=rng.randrange(41); S=2*y+d; R=rng.randrange(S+31); pts.add((y,d,R))
    bad=0
    for y,d,R in sorted(pts):
        if direct(R,(y,y+d),7)!=candidate(y+d,y,R): bad+=1
    audit["checks"]["seeded_direct_samples"]={"range":"4<=y<=30, d<=40, R<=S+30, seed=20261119","points":len(pts),"mismatches":bad}
    ok &= bad==0
    audit["all_passed"]=bool(ok)
    audit["direct_cache"]={"hits":direct.cache_info().hits,"misses":direct.cache_info().misses}
    audit["total_points"]=sum(v.get("points",0) for v in audit["checks"].values())
    print(json.dumps(audit,ensure_ascii=False,sort_keys=True,indent=2))
    if not ok: raise SystemExit(1)

if __name__=="__main__": main()
