#!/usr/bin/env python3
"""Independent finite audit for the proved z=6, y=25 two-token slice."""
from __future__ import annotations
import hashlib, json, random
from functools import lru_cache
from pathlib import Path

def mex(v):
    s=set(v); n=0
    while n in s: n+=1
    return n

def O(r,a,b=None): return r>=a and (b is None or r<=b) and r%2==1
def E(r,a,b=None): return r>=a and (b is None or r<=b) and r%2==0

def h5(x,y,r):
    if r==0:return 0
    s,d=x+y,x-y; t={1,3,5}
    if d==1 and y>=2:t.add(2*y+3)
    elif d==5:t.add(2*y+5)
    elif d==6:t.update({2*y+5,2*y+7,2*y+9,2*y+11})
    elif d>=7:t.add(2*y+5)
    if r in t:return 2
    if d==0:v=E(r,6,s+2) if y>=3 else False
    elif d==1:v=(E(r,6,s+3) or r>=s+4) if y>=2 else r>=4
    elif d==2:v=E(r,6,s) if y>=2 else False
    elif d==3:v=E(r,6,s+1) or r>=s+2
    elif d==4:v=E(r,6,s)
    elif d==5:v=E(r,6,s-1) or r>=s+1
    elif d==6:v=E(r,6,s-2)
    elif d%2:v=E(r,6,2*y+4) or O(r,2*y+7,s+4) or r>=s+6
    else:v=E(r,6,2*y+4) or O(r,2*y+7,s+5)
    return int(v)

def h24(x,r):
    if r==0:return 0
    d=x-24; t={1,3,5}
    if d==0:t.add(51)
    elif d==4:t.add(53)
    elif d==7:t.update({55,57,59,61})
    elif d>=8:t.add(55)
    if r in t:return 2
    if d==0:v=O(r,7,49)
    elif d==1:v=O(r,7) or E(r,52)
    elif d==2:v=O(r,7,51)
    elif d==3:v=O(r,7) or E(r,54)
    elif d==4:v=O(r,7,51)
    elif d==5:v=O(r,7) or E(r,54)
    elif d==6:v=O(r,7,53)
    elif d==7:v=O(r,7,53) or E(r,56) or O(r,63)
    elif x%2==0:v=O(r,7,53) or E(r,56,x+30)
    else:v=O(r,7,53) or E(r,56) or O(r,x+32)
    return int(v)

def T25(x):
    t={1,3,5}
    if x==25:t.add(53)
    elif x==29:t.add(55)
    elif x==32:t.update({57,59,61,63})
    elif x>=33:t.add(57)
    return t

def P25(x,r):
    if x==25:return O(r,7,51)
    if x==26:return O(r,7,57) or E(r,54,56) or r>=58
    if x==27:return O(r,7,53)
    if x==28:return O(r,7,59) or E(r,56,58) or r>=60
    if x==29:return O(r,7,53)
    if x==30:return O(r,7,61) or E(r,56,60) or r>=62
    if x==31:return O(r,7,55)
    if x==32:return O(r,7,55) or E(r,58,62) or r>=64
    if x==33:return O(r,7,55) or E(r,58,64)
    if x%2==0:return O(r,7,55) or E(r,58,x+30) or r>=x+32
    return O(r,7,55) or E(r,58,x+31)

def h25(x,r):
    if r==0:return 0
    if r in T25(x):return 2
    return int(P25(x,r))

# Each interval contains only R of the row's stated parity; signatures are
# sorted sets of the A/B/C child Grundy values.
ROWS={
25: ([(1,5,(0,1)),(7,51,(0,)),(53,53,(0,1)),(55,57,(1,))],[(2,6,(2,3)),(8,56,(1,))]),
26: ([(1,5,(0,1)),(7,57,(0,))],[(2,6,(2,3)),(8,52,(1,)),(54,54,(0,2,3)),(56,58,(0,))]),
27: ([(1,5,(0,1)),(7,53,(0,)),(55,59,(1,))],[(2,6,(2,3)),(8,58,(1,))]),
28: ([(1,5,(0,1)),(7,59,(0,))],[(2,6,(2,3)),(8,52,(1,)),(54,54,(1,2)),(56,60,(0,))]),
29: ([(1,5,(0,1)),(7,53,(0,)),(55,55,(0,1)),(57,61,(1,))],[(2,6,(2,3)),(8,60,(1,))]),
30: ([(1,5,(0,1)),(7,61,(0,))],[(2,6,(2,3)),(8,54,(1,)),(56,56,(0,2,3)),(58,62,(0,))]),
31: ([(1,5,(0,1)),(7,55,(0,)),(57,63,(1,))],[(2,6,(2,3)),(8,54,(1,)),(56,62,(1,2,3))]),
32: ([(1,5,(0,1)),(7,55,(0,)),(57,63,(0,1))],[(2,6,(2,3)),(8,54,(1,)),(56,56,(1,2,3)),(58,64,(0,))]),
33: ([(1,5,(0,1)),(7,55,(0,)),(57,57,(0,1)),(59,65,(1,))],[(2,6,(2,3)),(8,54,(1,)),(56,56,(1,2,3)),(58,64,(0,2))]),
}
def expected_sig(x,r):
    if x in ROWS: rows=ROWS[x]
    else:
        uo=x+32 if x%2 else x+31; ue=x+32 if x%2==0 else x+31
        rows=([(1,5,(0,1)),(7,55,(0,)),(57,57,(0,1)),(59,uo,(1,))],
              [(2,6,(2,3)),(8,54,(1,)),(56,56,(1,2,3)),(58,58,(0,2)),(60,ue,(0,))])
    for a,b,v in rows[r%2==0]:
        if a<=r<=b and (r-a)%2==0:return v
    return None

def actual_sig(x,r):
    q=r-1; a=h24(25,q) if x==25 else h25(x-1,q)
    return tuple(sorted({a,h24(x,q),1^h5(x,25,q)}))

@lru_cache(None)
def ordered(r,t,z):
    if r==0:return 0
    v=[]
    for i,a in enumerate(t):
        u=list(t); zz=z
        if a>=2:u[i]-=1
        else:u.pop(i); zz+=1
        v.append(ordered(r-1,tuple(u),zz))
    if z:v.append(1^ordered(r-1,t,z-1))
    return mex(v)

@lru_cache(None)
def canonical(r,t,z):
    if r==0:return 0
    v=[]
    for i,a in enumerate(t):
        u=list(t); zz=z
        if a>=2:u[i]-=1
        else:u.pop(i); zz+=1
        v.append(canonical(r-1,tuple(sorted(u,reverse=True)),zz))
    if z:v.append(1^canonical(r-1,tuple(sorted(t,reverse=True)),z-1))
    return mex(v)

def audit_once():
    bad=[]; direct=0; ordered.cache_clear(); canonical.cache_clear()
    for x in range(25,41):
        for r in range(x+36):
            v=h25(x,r); a=ordered(r,(x,25),6); b=canonical(r,(x,25),6); direct+=2
            if (a,b)!=(v,v):bad.append(("direct-y25",x,r,a,b,v))
            if r<=x+35:
                for z,tok,formula,tag in ((6,(x,24),h24(x,r),"y24"),(5,(x,25),h5(x,25,r),"z5")):
                    a=ordered(r,tok,z); b=canonical(r,tok,z); direct+=2
                    if a!=formula or b!=formula:bad.append((tag,x,r,a,b,formula))
    sigs=mexes=odd_bound=even_bound=value2=0
    for x in range(25,2001):
        seen=set()
        for r in range(1,x+33):
            a=actual_sig(x,r); e=expected_sig(x,r); sigs+=1
            if a!=e:bad.append(("signature",x,r,a,e)); continue
            v=mex(a); mexes+=1
            if v!=h25(x,r):bad.append(("mex",x,r,v,h25(x,r),a))
            if r%2:
                odd_bound+=1
                if not set(a)<={0,1}:bad.append(("odd-bound",x,r,a))
            else:
                even_bound+=1
                if v>1:bad.append(("even-bound",x,r,v,a))
            if v==2:seen.add(r)
        value2+=1
        if seen!=T25(x):bad.append(("value2",x,sorted(seen),sorted(T25(x))))
    tail=0
    for x in range(25,2001):
        for j in range(65):
            r=x+32+j; tail+=1
            if h25(x,r)!=(x+25)%2:bad.append(("tail",x,r,h25(x,r)))
    rng=random.Random(20261118); far=0
    for _ in range(5000):
        x=rng.randint(25,1_000_000); r=x+32+rng.randint(0,1_000_000); far+=1
        if h25(x,r)!=(x+25)%2:bad.append(("far-tail",x,r))
    counts={"direct_formula_and_two_engine_checks":direct,"even_parent_upper_bound":even_bound,
      "far_tail_seeded_checks":far,"mex_identities":mexes,"odd_parent_option_bound":odd_bound,
      "signature_points":sigs,"tail_checks":tail,"value2_locus_parameters":value2}
    return {"all_pass":not bad,"classification":"universal proof by explicit A/B/C signatures, Theorem T, the general tail theorem, and strong induction on R; finite checks are independent audits only",
      "counts":counts,"failures":bad,"scope":{"direct_x":[25,40],"direct_R":"0 <= R <= x+35 (z=5 and y=24 anchors also checked)",
      "signature_x":[25,2000],"signature_R":"1 <= R <= x+32","tail_x":[25,2000],"tail_offsets":[0,64],
      "far_tail_seed":20261118,"far_tail_samples":far},"target":"H(R;(x,25);6), x>=25, R>=0","total_checks":sum(counts.values())}

def run():
    a,b=audit_once(),audit_once()
    same=json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(",",":"))==json.dumps(b,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    out=dict(a,repeat_runs=2,repeat_byte_identical=same)
    raw=json.dumps(out,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    out["sha256_without_hash_field"]=hashlib.sha256(raw).hexdigest()
    p=Path(__file__).with_name("output"); p.mkdir(exist_ok=True)
    (p/"audit.json").write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"all_pass":out["all_pass"],"counts":out["counts"],"failures":len(out["failures"]),"repeat_byte_identical":same,
      "sha256_without_hash_field":out["sha256_without_hash_field"],"total_checks":out["total_checks"]},sort_keys=True))
    if not out["all_pass"] or not same:raise SystemExit(1)

if __name__=="__main__":run()
