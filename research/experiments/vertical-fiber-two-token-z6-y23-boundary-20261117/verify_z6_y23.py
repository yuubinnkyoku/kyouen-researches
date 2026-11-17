#!/usr/bin/env python3
"""Independent finite audit for the universally proved z=6, y=23 slice."""
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
    if d==1:t.add(2*y+3)
    elif d==5:t.add(2*y+5)
    elif d==6:t.update({2*y+5,2*y+7,2*y+9,2*y+11})
    elif d>=7:t.add(2*y+5)
    if r in t:return 2
    if d==0:o=even(r,6,s+2)
    elif d==1:o=even(r,6,s+3) or r>=s+4
    elif d==2:o=even(r,6,s)
    elif d==3:o=even(r,6,s+1) or r>=s+2
    elif d==4:o=even(r,6,s)
    elif d==5:o=even(r,6,s-1) or r>=s+1
    elif d==6:o=even(r,6,s-2)
    elif d>=7 and d%2:o=even(r,6,2*y+4) or odd(r,2*y+7,s+4) or r>=s+6
    else:o=even(r,6,2*y+4) or odd(r,2*y+7,s+5)
    return int(o)

def twos22(x):
    t={1,3,5}
    if x==22:t.add(47)
    elif x==26:t.add(49)
    elif x==29:t.update({51,53,55,57})
    elif x>=30:t.add(51)
    return t

def ones22(x,r):
    if x==22:return odd(r,7,45)
    if x==23:return odd(r,7) or even(r,48)
    if x==24:return odd(r,7,47)
    if x==25:return odd(r,7) or even(r,50)
    if x==26:return odd(r,7,47)
    if x==27:return odd(r,7) or even(r,50)
    if x==28:return odd(r,7,49)
    if x%2:return odd(r,7,49) or even(r,52) or odd(r,x+30)
    return odd(r,7,49) or even(r,52,x+28)

def h22(x,r): return 2 if r in twos22(x) else int(ones22(x,r))

def family22(x):
    d=x-22; t={1,3,5}
    if d<=6 and d%2==0 and (6+d)%4==2:t.add(44+(6+d)//2)
    elif d==7:t.update({51,53,55,57})
    elif d>=8:t.add(51)
    return t


def twos23(x):
    t={1,3,5}
    if x==23:t.add(49)
    elif x==27:t.add(51)
    elif x==30:t.update({53,55,57,59})
    elif x>=31:t.add(53)
    return t

def ones23(x,r):
    if x==23:return odd(r,7,47)
    if x==24:return odd(r,7,53) or even(r,50,52) or r>=54
    if x==25:return odd(r,7,49)
    if x==26:return odd(r,7,55) or even(r,52,54) or r>=56
    if x==27:return odd(r,7,49)
    if x==28:return odd(r,7,57) or even(r,52,56) or r>=58
    if x==29:return odd(r,7,51)
    if x==30:return odd(r,7,51) or even(r,54,58) or r>=60
    if x%2:return odd(r,7,51) or even(r,54,x+29)
    return odd(r,7,51) or even(r,54) or odd(r,x+31)

def h23_formula(x,r):
    if r==0:return 0
    if r in twos23(x):return 2
    return int(ones23(x,r))

def family23(x):
    d=x-23
    t={1,3,5}
    if d==0:t.add(49)
    elif d==4:t.add(51)
    elif d==7:t.update({53,55,57,59})
    elif d>=8:t.add(53)
    return t

ROWS23={
23: (
    [(1,5,(0,1)),(7,47,(0,)),(49,49,(0,1)),(51,51,(1,))],
    [(2,6,(2,3)),(8,52,(1,))]
),
24: (
    [(1,5,(0,1)),(7,53,(0,))],
    [(2,6,(2,3)),(8,48,(1,)),(50,50,(0,2,3)),(52,52,(0,))]
),
25: (
    [(1,5,(0,1)),(7,49,(0,)),(51,53,(1,))],
    [(2,6,(2,3)),(8,54,(1,))]
),
26: (
    [(1,5,(0,1)),(7,55,(0,))],
    [(2,6,(2,3)),(8,48,(1,)),(50,50,(1,2)),(52,54,(0,))]
),
27: (
    [(1,5,(0,1)),(7,49,(0,)),(51,51,(0,1)),(53,55,(1,))],
    [(2,6,(2,3)),(8,56,(1,))]
),
28: (
    [(1,5,(0,1)),(7,57,(0,))],
    [(2,6,(2,3)),(8,50,(1,)),(52,52,(0,2,3)),(54,56,(0,))]
),
29: (
    [(1,5,(0,1)),(7,51,(0,)),(53,57,(1,))],
    [(2,6,(2,3)),(8,50,(1,)),(52,58,(1,2,3))]
),
30: (
    [(1,5,(0,1)),(7,51,(0,)),(53,59,(0,1))],
    [(2,6,(2,3)),(8,50,(1,)),(52,52,(1,2,3)),(54,58,(0,))]
),
31: (
    [(1,5,(0,1)),(7,51,(0,)),(53,53,(0,1)),(55,59,(1,))],
    [(2,6,(2,3)),(8,50,(1,)),(52,52,(1,2,3)),(54,60,(0,2))]
)
}

def expected_sig23(x,R):
    if x in ROWS23:
        segs=ROWS23[x][0 if R%2 else 1]
    elif R%2:
        u=x+28 if x%2 else x+29
        segs=[(1,5,(0,1)),(7,51,(0,)),(53,53,(0,1)),(55,u,(1,))]
    else:
        u=x+29 if x%2 else x+28
        segs=[(2,6,(2,3)),(8,50,(1,)),(52,52,(1,2,3)),(54,54,(0,2)),(56,u,(0,))]
    for a,b,s in segs:
        if a<=R<=b and (R-a)%2==0:return s
    return None

def actual_sig23(x,R):
    r=R-1
    a=h22(23,r) if x==23 else h23_formula(x-1,r)
    b=h22(x,r)
    c=1^h5(x,23,r)
    return tuple(sorted({a,b,c}))

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


def audit_once():
    failures=[]
    direct=0
    ordered.cache_clear()
    canonical.cache_clear()
    for x in range(23,61):
        for r in range(x+51):
            for toks,z,expected in (
                ((x,23),6,h23_formula(x,r)),
                ((x,22),6,h22(x,r)),
                ((x,23),5,h5(x,23,r))
            ):
                a=ordered(r,toks,z)
                b=canonical(r,tuple(sorted(toks,reverse=True)),z)
                direct+=1
                if a!=b or a!=expected:
                    failures.append(("direct",x,r,toks,z,a,b,expected))
    sigs=mexes=ob=eb=v2=family=0
    for x in range(23,2001):
        seen=set()
        for r in range(1,x+30):
            a=actual_sig23(x,r)
            e=expected_sig23(x,r)
            sigs+=1
            if a!=e:
                failures.append(("signature",x,r,a,e))
                continue
            v=mex(a)
            mexes+=1
            if v!=h23_formula(x,r):
                failures.append(("mex",x,r,v,h23_formula(x,r)))
            if r%2:
                ob+=1
                if not set(a)<={0,1}:
                    failures.append(("odd-bound",x,r,a))
            else:
                eb+=1
                if v>1:
                    failures.append(("even-bound",x,r,v))
            if v==2:seen.add(r)
        if seen!=twos23(x):
            failures.append(("value2",x,sorted(seen),sorted(twos23(x))))
        v2+=1
        if seen!=family23(x):
            failures.append(("family",x,sorted(seen),sorted(family23(x))))
        family+=1
    tail=0
    for x in range(23,2001):
        for off in range(65):
            r=x+30+off
            tail+=1
            if h23_formula(x,r)!=(x+23)%2:
                failures.append(("tail",x,r,h23_formula(x,r)))
    rng=random.Random(20261118)
    far=0
    for _ in range(2000):
        x=rng.randint(23,100000)
        r=x+30+rng.randint(0,100000)
        far+=1
        if h23_formula(x,r)!=(x+23)%2:
            failures.append(("far-tail",x,r,h23_formula(x,r)))
    counts={
        "choice_signatures":sigs,
        "direct_ordered_canonical_formula_anchors":direct,
        "even_parent_upper_bound":eb,
        "fixed_seed_far_tail":far,
        "mex_identities":mexes,
        "odd_parent_upper_bound":ob,
        "tail":tail,
        "three_family_specialization":family,
        "value2_locus":v2
    }
    payload={
        "all_pass":not failures,
        "audit_scope":{
            "direct_R":"0 <= R < x+51",
            "direct_x":[23,60],
            "far_tail_samples":far,
            "far_tail_seed":20261118,
            "signature_R":"1 <= R <= x+29",
            "signature_x":[23,2000],
            "tail_offsets":[0,64],
            "tail_x":[23,2000]
        },
        "classification":"universal proof by explicit A/B/C signature table, Theorem T, general tail theorem, and strong induction on R",
        "counts":counts,
        "failures":failures,
        "target":"H(R;(x,23);6), x>=23, R>=0",
        "total_checks":sum(counts.values())
    }
    return payload

def run():
    first=audit_once()
    second=audit_once()
    first_bytes=json.dumps(first,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    second_bytes=json.dumps(second,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    repeat=first_bytes==second_bytes
    payload=dict(first)
    payload["repeat_byte_identical"]=repeat
    payload["repeat_runs"]=2
    raw=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    payload["sha256_without_hash_field"]=hashlib.sha256(raw).hexdigest()
    out=Path(__file__).with_name("output")
    out.mkdir(parents=True,exist_ok=True)
    rendered=json.dumps(payload,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    (out/"audit.json").write_text(rendered,encoding="utf-8")
    print(json.dumps({
        "all_pass":payload["all_pass"],
        "total_checks":payload["total_checks"],
        "counts":payload["counts"],
        "failures":len(payload["failures"]),
        "repeat_byte_identical":repeat,
        "sha256_without_hash_field":payload["sha256_without_hash_field"]
    },ensure_ascii=False,sort_keys=True))
    if not payload["all_pass"] or not repeat:
        raise SystemExit(1)

if __name__=="__main__":
    run()
