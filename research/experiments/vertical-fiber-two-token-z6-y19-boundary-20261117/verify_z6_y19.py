#!/usr/bin/env python3
"""Independent finite audit for the universally proved z=6, y=19 slice."""
from __future__ import annotations
import hashlib, json, random
from functools import lru_cache

def mex(v):
    s=set(v); n=0
    while n in s: n+=1
    return n
def O(r,a,b=None): return r>=a and (b is None or r<=b) and r%2==1
def E(r,a,b=None): return r>=a and (b is None or r<=b) and r%2==0

def h5(x,y,r):
    if r==0:return 0
    s,d=x+y,x-y; t={1,3,5}
    if d==1:t.add(2*y+3)
    elif d==5:t.add(2*y+5)
    elif d==6:t.update({2*y+5,2*y+7,2*y+9,2*y+11})
    elif d>=7:t.add(2*y+5)
    if r in t:return 2
    if d==0:v=E(r,6,s+2)
    elif d==1:v=E(r,6,s+3) or r>=s+4
    elif d==2:v=E(r,6,s)
    elif d==3:v=E(r,6,s+1) or r>=s+2
    elif d==4:v=E(r,6,s)
    elif d==5:v=E(r,6,s-1) or r>=s+1
    elif d==6:v=E(r,6,s-2)
    elif d>=7 and d%2:v=E(r,6,2*y+4) or O(r,2*y+7,s+4) or r>=s+6
    else:v=E(r,6,2*y+4) or O(r,2*y+7,s+5)
    return int(v)

def h18(x,r):
    if r==0:return 0
    t={1,3,5}
    if x==18:t.add(39)
    elif x==22:t.add(41)
    elif x==25:t.update({43,45,47,49})
    elif x>=26:t.add(43)
    if r in t:return 2
    if x==18:v=O(r,7,37)
    elif x==19:v=O(r,7) or E(r,40)
    elif x==20:v=O(r,7,39)
    elif x in (21,23):v=O(r,7) or E(r,42)
    elif x==22:v=O(r,7,39)
    elif x==24:v=O(r,7,41)
    elif x%2==0:v=O(r,7,41) or E(r,44,x+24)
    else:v=O(r,7,41) or E(r,44) or O(r,x+26)
    return int(v)

def h19(x,r):
    if r==0:return 0
    t={1,3,5}
    if x==19:t.add(41)
    elif x==23:t.add(43)
    elif x==26:t.update({45,47,49,51})
    elif x>=27:t.add(45)
    if r in t:return 2
    if x==19:v=O(r,7,39)
    elif x==20:v=O(r,7) or E(r,42)
    elif x==21:v=O(r,7,41)
    elif x==22:v=O(r,7) or E(r,44)
    elif x==23:v=O(r,7,41)
    elif x==24:v=O(r,7) or E(r,44)
    elif x==25:v=O(r,7,43)
    elif x%2==0:v=O(r,7,43) or E(r,46,x+24) or r>=x+26
    else:v=O(r,7,43) or E(r,46,x+25)
    return int(v)

def family(x):
    d=x-19; t={1,3,5}
    if d<=6 and d%2==0 and (6+d)%4==2:t.add(38+(6+d)//2)
    elif d==7:t.update({45,47,49,51})
    elif d>=8:t.add(45)
    return t

def sig_expected(x,r):
    odd=r%2==1
    rows={
    19: ([(1,5,"01"),(7,39,"0"),(41,41,"01"),(43,43,"1")],[(2,6,"23"),(8,44,"1")]),
    20: ([(1,5,"01"),(7,45,"0")],[(2,6,"23"),(8,40,"1"),(42,42,"023"),(44,44,"0")]),
    21: ([(1,5,"01"),(7,41,"0"),(43,45,"1")],[(2,6,"23"),(8,46,"1")]),
    22: ([(1,5,"01"),(7,47,"0")],[(2,6,"23"),(8,40,"1"),(42,42,"12"),(44,46,"0")]),
    23: ([(1,5,"01"),(7,41,"0"),(43,43,"01"),(45,47,"1")],[(2,6,"23"),(8,48,"1")]),
    24: ([(1,5,"01"),(7,49,"0")],[(2,6,"23"),(8,42,"1"),(44,44,"023"),(46,48,"0")]),
    25: ([(1,5,"01"),(7,43,"0"),(45,49,"1")],[(2,6,"23"),(8,42,"1"),(44,50,"123")]),
    26: ([(1,5,"01"),(7,43,"0"),(45,51,"01")],[(2,6,"23"),(8,42,"1"),(44,44,"123"),(46,50,"0")]),
    27: ([(1,5,"01"),(7,43,"0"),(45,45,"01"),(47,51,"1")],[(2,6,"23"),(8,42,"1"),(44,44,"123"),(46,52,"02")])}
    if x in rows: rr=rows[x][0 if odd else 1]
    elif odd:
        u=x+24 if x%2 else x+25
        rr=[(1,5,"01"),(7,43,"0"),(45,45,"01"),(47,u,"1")]
    else:
        u=x+25 if x%2 else x+24
        rr=[(2,6,"23"),(8,42,"1"),(44,44,"123"),(46,46,"02"),(48,u,"0")]
    for a,b,d in rr:
        if a<=r<=b and (r-a)%2==0:return tuple(map(int,d))
    return None

def actual_sig(x,R):
    r=R-1
    if x==19:a=b=h18(19,r)
    else:a,b=h19(x-1,r),h18(x,r)
    c=1^h5(x,19,r)
    return tuple(sorted({a,b,c}))

@lru_cache(None)
def ordered(r,X,z):
    if not r:return 0
    q=[]
    for i,t in enumerate(X):
        Y=list(X); zz=z
        if t>=2:Y[i]-=1
        else:Y.pop(i); zz+=1
        q.append(ordered(r-1,tuple(Y),zz))
    if z:q.append(1^ordered(r-1,X,z-1))
    return mex(q)
@lru_cache(None)
def canonical(r,X,z):
    if not r:return 0
    q=[]
    for i,t in enumerate(X):
        Y=list(X); zz=z
        if t>=2:Y[i]-=1
        else:Y.pop(i); zz+=1
        q.append(canonical(r-1,tuple(sorted(Y,reverse=True)),zz))
    if z:q.append(1^canonical(r-1,tuple(sorted(X,reverse=True)),z-1))
    return mex(q)

def run():
    ordered.cache_clear(); canonical.cache_clear(); bad=[]; direct=0
    for x in range(19,81):
        for r in range(x+51):
            for X,z,v in (((x,19),6,h19(x,r)),((x,18),6,h18(x,r)),((x,19),5,h5(x,19,r))):
                a=ordered(r,X,z); b=canonical(r,tuple(sorted(X,reverse=True)),z); direct+=1
                if a!=b or a!=v:bad.append(("direct",x,r,X,z,a,b,v))
    sig=mexn=odd=even=0
    for x in range(19,2001):
        got=set()
        for r in range(1,x+26):
            a=actual_sig(x,r); e=sig_expected(x,r); sig+=1
            if a!=e:bad.append(("signature",x,r,a,e))
            v=mex(a); mexn+=1
            if v!=h19(x,r):bad.append(("mex",x,r,v,h19(x,r)))
            if r%2:
                odd+=1
                if not set(a)<= {0,1}:bad.append(("odd",x,r,a))
            else:
                even+=1
                if v>1:bad.append(("even",x,r,v))
            if v==2:got.add(r)
        if got!=family(x):bad.append(("family",x,sorted(got),sorted(family(x))))
    tail=0
    for x in range(19,2001):
        for j in range(65):
            r=x+26+j; tail+=1
            if h19(x,r)!=(x+19)%2:bad.append(("tail",x,r))
    rng=random.Random(20261117); far=0
    for _ in range(2000):
        x=rng.randint(19,100000); r=x+26+rng.randint(0,100000); far+=1
        if h19(x,r)!=(x+19)%2:bad.append(("far",x,r))
    counts={"direct_ordered_canonical_formula_anchors":direct,"option_signatures":sig,
    "mex_identity":mexn,"odd_parent_bounds":odd,"even_parent_bounds":even,
    "three_family_specialization":1982,"tail":tail,"fixed_seed_far_tail":far}
    payload={"schema":"two-token-z6-y19-audit-v1",
    "claim":"H(R;(x,19);6) is given by the complete formula for all x>=19,R>=0",
    "classification":"universal proof by option-signature cases, Theorem T, tail theorem, and strong induction on R; finite checks are independent audits only",
    "counts":counts,"total_checks":sum(counts.values()),"mismatches":len(bad),"first_failures":bad[:20],
    "cache":{"ordered":ordered.cache_info()._asdict(),"canonical":canonical.cache_info()._asdict()}}
    raw=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    payload["sha256_without_hash_field"]=hashlib.sha256(raw).hexdigest()
    return payload

if __name__=="__main__":
    out=run(); print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))
    raise SystemExit(0 if out["mismatches"]==0 else 1)
