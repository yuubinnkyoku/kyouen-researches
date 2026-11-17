#!/usr/bin/env python3
"""Independent finite audit for the universally proved z=6, y=24 slice."""
from __future__ import annotations
import hashlib, json, random
from functools import lru_cache
from pathlib import Path

def mex(values):
    s=set(values); n=0
    while n in s: n+=1
    return n

def odd(r,a,b=None): return r>=a and (b is None or r<=b) and r%2==1
def even(r,a,b=None): return r>=a and (b is None or r<=b) and r%2==0

def h5(x,y,r):
    if r==0:return 0
    s,d=x+y,x-y; t={1,3,5}
    if d==1 and y>=2:t.add(2*y+3)
    elif d==5:t.add(2*y+5)
    elif d==6:t.update({2*y+5,2*y+7,2*y+9,2*y+11})
    elif d>=7:t.add(2*y+5)
    if r in t:return 2
    if d==0:o=even(r,6,s+2) if y>=3 else False
    elif d==1:o=(even(r,6,s+3) or r>=s+4) if y>=2 else r>=4
    elif d==2:o=even(r,6,s) if y>=2 else False
    elif d==3:o=even(r,6,s+1) or r>=s+2
    elif d==4:o=even(r,6,s)
    elif d==5:o=even(r,6,s-1) or r>=s+1
    elif d==6:o=even(r,6,s-2)
    elif d>=7 and d%2:o=even(r,6,2*y+4) or odd(r,2*y+7,s+4) or r>=s+6
    else:o=even(r,6,2*y+4) or odd(r,2*y+7,s+5)
    return int(o)

def h23(x,r):
    d=x-23
    if r==0:return 0
    t={1,3,5}
    if d==0:t.add(49)
    elif d==4:t.add(51)
    elif d==7:t.update({53,55,57,59})
    elif d>=8:t.add(53)
    if r in t:return 2
    if d==0:o=odd(r,7,47)
    elif d==1:o=odd(r,7) or even(r,50)
    elif d==2:o=odd(r,7,49)
    elif d==3:o=odd(r,7) or even(r,52)
    elif d==4:o=odd(r,7,49)
    elif d==5:o=odd(r,7) or even(r,52)
    elif d==6:o=odd(r,7,51)
    elif d==7:o=odd(r,7,51) or even(r,54) or odd(r,61)
    elif x%2:o=odd(r,7,51) or even(r,54,x+29)
    else:o=odd(r,7,51) or even(r,54) or odd(r,x+31)
    return int(o)

def twos24(x):
    d=x-24;t={1,3,5}
    if d==0:t.add(51)
    elif d==4:t.add(53)
    elif d==7:t.update({55,57,59,61})
    elif d>=8:t.add(55)
    return t

def ones24(x,r):
    d=x-24
    if d==0:return odd(r,7,49)
    if d==1:return odd(r,7) or even(r,52)
    if d==2:return odd(r,7,51)
    if d==3:return odd(r,7) or even(r,54)
    if d==4:return odd(r,7,51)
    if d==5:return odd(r,7) or even(r,54)
    if d==6:return odd(r,7,53)
    if d==7:return odd(r,7,53) or even(r,56) or odd(r,63)
    if x%2==0:return odd(r,7,53) or even(r,56,x+30)
    return odd(r,7,53) or even(r,56) or odd(r,x+32)

def h24(x,r):
    if r==0:return 0
    if r in twos24(x):return 2
    return int(ones24(x,r))

@lru_cache(None)
def ordered(r,toks,z):
    if r==0:return 0
    opts=[]
    for i,t in enumerate(toks):
        a=list(toks); zz=z
        if t>=2:a[i]-=1
        else:a.pop(i);zz+=1
        opts.append(ordered(r-1,tuple(a),zz))
    if z:opts.append(1^ordered(r-1,toks,z-1))
    return mex(opts)

@lru_cache(None)
def canonical(r,toks,z):
    if r==0:return 0
    opts=[]
    for i,t in enumerate(toks):
        a=list(toks); zz=z
        if t>=2:a[i]-=1
        else:a.pop(i);zz+=1
        opts.append(canonical(r-1,tuple(sorted(a,reverse=True)),zz))
    if z:opts.append(1^canonical(r-1,tuple(sorted(toks,reverse=True)),z-1))
    return mex(opts)

ROWS={
24:(
 [(1,5,(0,1)),(7,49,(0,)),(51,51,(0,1)),(53,53,(1,))],
 [(2,6,(2,3)),(8,54,(1,))]
),
25:(
 [(1,5,(0,1)),(7,55,(0,))],
 [(2,6,(2,3)),(8,50,(1,)),(52,52,(0,2,3)),(54,54,(0,))]
),
26:(
 [(1,5,(0,1)),(7,51,(0,)),(53,55,(1,))],
 [(2,6,(2,3)),(8,56,(1,))]
),
27:(
 [(1,5,(0,1)),(7,57,(0,))],
 [(2,6,(2,3)),(8,50,(1,)),(52,52,(1,2)),(54,56,(0,))]
),
28:(
 [(1,5,(0,1)),(7,51,(0,)),(53,53,(0,1)),(55,57,(1,))],
 [(2,6,(2,3)),(8,58,(1,))]
),
29:(
 [(1,5,(0,1)),(7,59,(0,))],
 [(2,6,(2,3)),(8,52,(1,)),(54,54,(0,2,3)),(56,58,(0,))]
),
30:(
 [(1,5,(0,1)),(7,53,(0,)),(55,59,(1,))],
 [(2,6,(2,3)),(8,52,(1,)),(54,60,(1,2,3))]
),
31:(
 [(1,5,(0,1)),(7,53,(0,)),(55,61,(0,1))],
 [(2,6,(2,3)),(8,52,(1,)),(54,54,(1,2,3)),(56,60,(0,))]
),
32:(
 [(1,5,(0,1)),(7,53,(0,)),(55,55,(0,1)),(57,61,(1,))],
 [(2,6,(2,3)),(8,52,(1,)),(54,54,(1,2,3)),(56,62,(0,2))]
)
}

def actual_sig(x,r):
    rr=r-1
    a=h23(24,rr) if x==24 else h24(x-1,rr)
    b=h23(x,rr); c=1^h5(x,24,rr)
    return tuple(sorted({a,b,c}))

def expected_sig(x,r):
    if x in ROWS:segs=ROWS[x][0 if r%2 else 1]
    elif r%2:
        u=x+30 if x%2 else x+29
        segs=[(1,5,(0,1)),(7,53,(0,)),(55,55,(0,1)),(57,u,(1,))]
    else:
        u=x+29 if x%2 else x+30
        segs=[(2,6,(2,3)),(8,52,(1,)),(54,54,(1,2,3)),(56,56,(0,2)),(58,u,(0,))]
    for a,b,s in segs:
        if a<=r<=b and (r-a)%2==0:return s
    return None

def family(x):
    y,z=24,6; d=x-y
    out={r for r in range(1,min(x+y,z)+1,2)}
    if d%2==z%2 and d<=z:
        ys=(z-d)//2
        if ys>=1 and y==ys:
            lo=d+1 if (d+1)%2 else d+2
            hi=2*((z+d+3)//4)-1
            out.update(2*y+v for v in range(lo,hi+1,2))
        if (z+d)%4==2 and y>=ys:out.add(2*y+(z+d)//2)
    da=z if z%2 else z+1
    if d==z+1:out.update(2*y+v for v in range(da,2*z+2,2))
    elif d>=z+2:out.add(2*y+da)
    return out

def audit_once():
    failures=[]; direct=0
    ordered.cache_clear();canonical.cache_clear()
    for x in range(24,61):
        for r in range(x+51):
            for toks,z,exp in (((x,24),6,h24(x,r)),((x,23),6,h23(x,r)),((x,24),5,h5(x,24,r))):
                a=ordered(r,toks,z);b=canonical(r,tuple(sorted(toks,reverse=True)),z);direct+=1
                if a!=b or a!=exp:failures.append(("direct",x,r,toks,z,a,b,exp))
    sigs=mexes=ob=eb=v2=fam=0
    for x in range(24,2001):
        seen=set()
        for r in range(1,x+31):
            a=actual_sig(x,r);e=expected_sig(x,r);sigs+=1
            if a!=e:failures.append(("signature",x,r,a,e));continue
            v=mex(a);mexes+=1
            if v!=h24(x,r):failures.append(("mex",x,r,v,h24(x,r)))
            if r%2:
                ob+=1
                if not set(a)<={0,1}:failures.append(("odd-bound",x,r,a))
            else:
                eb+=1
                if v>1:failures.append(("even-bound",x,r,v))
            if v==2:seen.add(r)
        if seen!=twos24(x):failures.append(("value2",x,sorted(seen),sorted(twos24(x))))
        v2+=1
        if seen!=family(x):failures.append(("family",x,sorted(seen),sorted(family(x))))
        fam+=1
    tail=0
    for x in range(24,2001):
        for off in range(65):
            r=x+31+off;tail+=1
            if h24(x,r)!=(x+24)%2:failures.append(("tail",x,r,h24(x,r)))
    rng=random.Random(20261117);far=0
    for _ in range(2000):
        x=rng.randint(24,100000);r=x+31+rng.randint(0,100000);far+=1
        if h24(x,r)!=(x+24)%2:failures.append(("far-tail",x,r,h24(x,r)))
    counts={
      "choice_signatures":sigs,"direct_ordered_canonical_formula_anchors":direct,
      "even_parent_upper_bound":eb,"fixed_seed_far_tail":far,"mex_identities":mexes,
      "odd_parent_upper_bound":ob,"tail":tail,"three_family_specialization":fam,"value2_locus":v2
    }
    return {"all_pass":not failures,
      "audit_scope":{"direct_R":"0 <= R < x+51","direct_x":[24,60],"far_tail_samples":far,
        "far_tail_seed":20261117,"signature_R":"1 <= R <= x+30","signature_x":[24,2000],
        "tail_offsets":[0,64],"tail_x":[24,2000]},
      "classification":"universal proof by explicit A/B/C signature table, K0832 Theorem T, general tail theorem, and strong induction on R",
      "counts":counts,"failures":failures,"target":"H(R;(x,24);6), x>=24, R>=0","total_checks":sum(counts.values())}

def run():
    first=audit_once();second=audit_once()
    same=json.dumps(first,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()==json.dumps(second,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    p=dict(first);p["repeat_byte_identical"]=same;p["repeat_runs"]=2
    raw=json.dumps(p,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    p["sha256_without_hash_field"]=hashlib.sha256(raw).hexdigest()
    out=Path(__file__).with_name("output");out.mkdir(parents=True,exist_ok=True)
    (out/"audit.json").write_text(json.dumps(p,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"all_pass":p["all_pass"],"total_checks":p["total_checks"],"counts":p["counts"],
      "failures":len(p["failures"]),"repeat_byte_identical":same,"sha256_without_hash_field":p["sha256_without_hash_field"]},
      ensure_ascii=False,sort_keys=True))
    if not p["all_pass"] or not same:raise SystemExit(1)

if __name__=="__main__":run()
