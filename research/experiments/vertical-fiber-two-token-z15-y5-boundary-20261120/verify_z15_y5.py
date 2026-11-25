#!/usr/bin/env python3
"""Independent audit for the proved z=15, y=5 two-token residual-game slice."""
from __future__ import annotations
from functools import lru_cache
import hashlib, json, random, sys
from pathlib import Path
sys.setrecursionlimit(500000)

def mex(values):
    values=set(values); m=0
    while m in values: m+=1
    return m

def odd(r,lo,hi): return r%2==1 and lo<=r<=hi
def even(r,lo,hi): return r%2==0 and lo<=r<=hi

@lru_cache(None)
def H_ordered(R,X,z):
    if R==0: return 0
    opts=set()
    for i,v in enumerate(X):
        child=X[:i]+(v-1,)+X[i+1:] if v>1 else X[:i]+X[i+1:]
        opts.add(H_ordered(R-1,child,z if v>1 else z+1))
    if z>=1: opts.add(1^H_ordered(R-1,X,z-1))
    return mex(opts)

@lru_cache(None)
def H_canonical(R,X,z):
    X=tuple(sorted(X,reverse=True))
    if R==0: return 0
    opts=set(); i=0
    while i<len(X):
        v=X[i]
        if v>1:
            child=tuple(sorted(X[:i]+(v-1,)+X[i+1:],reverse=True))
            opts.add(H_canonical(R-1,child,z))
        else:
            child=tuple(sorted(X[:i]+X[i+1:],reverse=True))
            opts.add(H_canonical(R-1,child,z+1))
        i+=1
        while i<len(X) and X[i]==v: i+=1
    if z>=1: opts.add(1^H_canonical(R-1,X,z-1))
    return mex(opts)

def clear_caches():
    H_ordered.cache_clear(); H_canonical.cache_clear()

# K1048: H(R;(x,4);15), x>=4.
def K1048_T(x,r):
    if x==4: return odd(r,1,7)
    if x in (5,6): return odd(r,1,9)
    if x in (7,8): return odd(r,1,11)
    if x in (9,10): return odd(r,1,13)
    if x==11: return odd(r,1,19)
    if x in (12,13,14,16,17,18): return odd(r,1,15)
    if x==15: return odd(r,1,15) or r==21
    if x==19: return odd(r,1,15) or r==23
    if x==20: return odd(r,1,15) or odd(r,23,39)
    return odd(r,1,15) or r==23

def K1048_P(x,r):
    if x in (5,7,9): return r>=x+5
    if x in (11,13): return r in (16,18,20) or r>=21
    if x==12: return r in (16,18)
    if x in (14,16): return r in (16,18,20)
    if x in (15,17): return r in (16,18,20,22) or r>=23
    if x==18: return r in (16,18,20,22)
    if x==19: return r in (16,18,20,22) or r>=24
    if x==20: return r in (16,18,20,22)
    if x>=21 and x%2: return r in (16,18,20,22) or odd(r,25,x+18) or r>=x+20
    if x>=22 and x%2==0: return r in (16,18,20,22) or odd(r,25,x+19)
    return False

def K1048(x,r):
    if r==0: return 0
    return 2 if K1048_T(x,r) else 1 if K1048_P(x,r) else 0

# K1047: H(R;(x,5);14), x>=5.
def K1047_T(x,r):
    if x==5: return odd(r,1,9)
    if x==6: return odd(r,1,11)
    if x==7: return odd(r,1,11)
    if x==8: return odd(r,1,13)
    if x==9: return odd(r,1,19)
    if x in (10,11,12): return odd(r,1,13)
    if x==13: return odd(r,1,13) or r==21
    if x in (14,15,16,18,19): return odd(r,1,13)
    if x==17: return odd(r,1,13) or r==23
    if x==20: return odd(r,1,13) or odd(r,25,39)
    return odd(r,1,13) or r==25

def K1047_P(x,r):
    if x==6: return r>=12
    if x==8: return r>=14
    if x==10: return r in (15,17,19) or r>=20
    if x==11: return r in (15,17,19)
    if x==12: return r in (15,17,19) or r>=21
    if x==13: return r in (15,17,19)
    if x==14: return r in (15,17,19) or r>=21
    if x==15: return r in (15,17,19,21)
    if x==16: return r in (15,17,19,21) or r>=23
    if x==17: return r in (15,17,19,21)
    if x==18: return r in (15,17,19,21) or r>=23
    if x==19: return r in (15,17,19,21,23)
    if x>=20 and x%2==0: return r in (15,17,19,21,23) or even(r,26,x+18) or r>=x+20
    if x>=21 and x%2: return r in (15,17,19,21,23) or even(r,26,x+19)
    return False

def K1047(x,r):
    if r==0: return 0
    return 2 if K1047_T(x,r) else 1 if K1047_P(x,r) else 0

# Candidate theorem H(R;(x,5);15), x>=5.
def T(x,r):
    if x==5: return odd(r,1,9)
    if x in (6,7): return odd(r,1,11)
    if x in (8,9): return odd(r,1,13)
    if x==10: return odd(r,1,19)
    if x==11: return odd(r,1,15)
    if x==12: return odd(r,1,15) or r==21
    if x in (13,14,15): return odd(r,1,15)
    if x==16: return odd(r,1,15) or r==23
    if x in (17,18,19): return odd(r,1,15)
    if x==20: return odd(r,1,15) or r==25
    if x==21: return odd(r,1,15) or odd(r,25,41)
    return odd(r,1,15) or r==25

def P(x,r):
    if x==5: return False
    if x==6: return r>=12
    if x==7: return False
    if x==8: return r>=14
    if x==9: return False
    if x==10: return r in (16,18,20) or r>=21
    if x==11: return r in (16,18,20)
    if x==12: return r in (16,18,20) or r>=22
    if x==13: return r in (16,18,20)
    if x==14: return r in (16,18,20,22) or r>=23
    if x==15: return r in (16,18,20,22)
    if x==16: return r in (16,18,20,22) or r>=24
    if x==17: return r in (16,18,20,22)
    if x==18: return r in (16,18,20,22,24) or r>=25
    if x==19: return r in (16,18,20,22,24)
    if x==20: return r in (16,18,20,22,24,26) or r>=27
    if x==21: return r in (16,18,20,22,24)
    if x>=22 and x%2==0: return r in (16,18,20,22,24) or odd(r,27,x+21) or r>=x+22
    if x>=23 and x%2: return r in (16,18,20,22,24) or odd(r,27,x+20)
    raise ValueError(x)

def candidate(x,r):
    if r==0: return 0
    return 2 if T(x,r) else 1 if P(x,r) else 0

FIXED={
5:[(1,1,9,"01"),(1,11,25,"1"),(0,2,10,"23"),(0,12,24,"1")],
6:[(1,1,11,"01"),(1,13,25,"0"),(0,2,10,"23"),(0,12,12,"03"),(0,14,26,"0")],
7:[(1,1,11,"01"),(1,13,27,"1"),(0,2,12,"23"),(0,14,26,"1")],
8:[(1,1,13,"01"),(1,15,27,"0"),(0,2,12,"23"),(0,14,14,"03"),(0,16,28,"0")],
9:[(1,1,13,"01"),(1,15,29,"1"),(0,2,14,"23"),(0,16,20,"13"),(0,22,28,"1")],
10:[(1,1,19,"01"),(1,21,29,"0"),(0,2,14,"23"),(0,16,30,"0")],
11:[(1,1,15,"01"),(1,17,31,"1"),(0,2,14,"23"),(0,16,20,"02"),(0,22,30,"1")],
12:[(1,1,15,"01"),(1,17,19,"1"),(1,21,21,"01"),(1,23,31,"0"),(0,2,14,"23"),(0,16,16,"02"),(0,18,32,"0")],
13:[(1,1,15,"01"),(1,17,33,"1"),(0,2,14,"23"),(0,16,16,"02"),(0,18,20,"0"),(0,22,22,"123"),(0,24,32,"1")],
14:[(1,1,15,"01"),(1,17,21,"1"),(1,23,33,"0"),(0,2,14,"23"),(0,16,16,"02"),(0,18,34,"0")],
15:[(1,1,15,"01"),(1,17,35,"1"),(0,2,14,"23"),(0,16,16,"02"),(0,18,20,"0"),(0,22,22,"02"),(0,24,34,"1")],
16:[(1,1,15,"01"),(1,17,21,"1"),(1,23,23,"01"),(1,25,35,"0"),(0,2,14,"23"),(0,16,16,"02"),(0,18,36,"0")],
17:[(1,1,15,"01"),(1,17,37,"1"),(0,2,14,"23"),(0,16,16,"02"),(0,18,22,"0"),(0,24,24,"123"),(0,26,36,"1")],
18:[(1,1,15,"01"),(1,17,23,"1"),(1,25,37,"0"),(0,2,14,"23"),(0,16,16,"02"),(0,18,38,"0")],
19:[(1,1,15,"01"),(1,17,39,"1"),(0,2,14,"23"),(0,16,16,"02"),(0,18,22,"0"),(0,24,24,"02"),(0,26,38,"1")],
20:[(1,1,15,"01"),(1,17,23,"1"),(1,25,25,"01"),(1,27,39,"0"),(0,2,14,"23"),(0,16,16,"02"),(0,18,22,"0"),(0,24,24,"02"),(0,26,40,"023")],
21:[(1,1,15,"01"),(1,17,23,"1"),(1,25,41,"01"),(0,2,14,"23"),(0,16,16,"02"),(0,18,22,"0"),(0,24,24,"02"),(0,26,26,"123"),(0,28,40,"1")],
22:[(1,1,15,"01"),(1,17,23,"1"),(1,25,25,"01"),(1,27,41,"0"),(0,2,14,"23"),(0,16,16,"02"),(0,18,22,"0"),(0,24,24,"02"),(0,26,26,"123"),(0,28,42,"12")]
}

def bands_for(x):
    if x in FIXED: return FIXED[x]
    if x>=24 and x%2==0:
        return [(1,1,15,"01"),(1,17,23,"1"),(1,25,25,"01"),(1,27,x+19,"0"),
                (0,2,14,"23"),(0,16,16,"02"),(0,18,22,"0"),(0,24,24,"02"),(0,26,26,"123"),(0,28,x+20,"1")]
    if x>=23 and x%2:
        return [(1,1,15,"01"),(1,17,23,"1"),(1,25,25,"01"),(1,27,x+20,"0"),
                (0,2,14,"23"),(0,16,16,"02"),(0,18,22,"0"),(0,24,24,"02"),(0,26,26,"123"),(0,28,x+19,"1")]
    raise ValueError(x)

def signature_from_children(x,R):
    r=R-1
    values={K1048(x,r),1^K1047(x,r)}
    values.add(candidate(x-1,r) if x>5 else K1048(x,r))
    return "".join(str(v) for v in sorted(values))

def single_token(n,z,R):
    if R==0 or n<=0: return 0
    if z==0: return min(R,n)%2
    if z==n:
        if R%2 and R<=2*n-1: return 2
        if R%2==0 and R<=n-1: return 0
        return n%2
    if 1<=z<=n-1:
        m=z if z%2 else z-1
        if R<=m: return 2 if R%2 else 0
        if m<R<n+z: return (R+z)%2
        return n%2
    if z>=n+1:
        m=n if n%2 else n-1
        if R<=m: return 2 if R%2 else 0
        return n%2
    raise ValueError((n,z,R))

def audit_once():
    clear_caches(); failures=[]; counts={}
    n=0
    for x in range(5,36):
        for R in range(x+23):
            a=H_ordered(R,(x,5),15); b=H_canonical(R,(x,5),15); c=candidate(x,R)
            n+=2
            if a!=b or a!=c: failures.append(("root-direct",x,R,a,b,c))
    counts["ordered_and_canonical_direct_vs_formula"]=n
    n=0
    for x in range(5,36):
        for R in range(x+23):
            for engine in (H_ordered,H_canonical):
                b=engine(R,(x,4),15); c=engine(R,(x,5),14); n+=2
                if b!=K1048(x,R): failures.append(("K1048-B-anchor",x,R,b,K1048(x,R)))
                if c!=K1047(x,R): failures.append(("K1047-C-anchor",x,R,c,K1047(x,R)))
    counts["K1048_and_K1047_child_anchor_checks"]=n
    n=0; parity=0
    for x in range(5,2001):
        bands=bands_for(x)
        for R in range(1,x+21):
            hits=[s for p,lo,hi,s in bands if R%2==p and lo<=R<=hi]
            if len(hits)!=1:
                failures.append(("band-coverage",x,R,hits)); continue
            actual=signature_from_children(x,R)
            if hits[0]!=actual:
                failures.append(("band-signature",x,R,hits[0],actual)); continue
            value=mex({int(ch) for ch in hits[0]}); expected=candidate(x,R); n+=1
            if value!=expected: failures.append(("band-mex",x,R,hits[0],value,expected))
            if (R%2==0 and value>1) or (R%2==1 and value>2):
                failures.append(("Theorem-T",x,R,hits[0],value))
            parity+=1
    counts["complete_signature_coverage_identity_mex"]=n
    counts["Theorem_T_parity_bound"]=parity
    n=0
    for x in range(5,2001):
        for R in range(17):
            a=candidate(x,R); b=single_token(x+5,15,R); n+=1
            if a!=b: failures.append(("height-only",x,R,a,b))
    counts["height_only_reduction_R_le_16"]=n
    n=0
    for x in range(5,5001):
        for offset in range(4):
            R=x+21+offset; a=candidate(x,R); b=(x+5)%2; n+=1
            if a!=b: failures.append(("general-tail",x,R,a,b))
    counts["general_tail"]=n
    rng=random.Random(20261120); n=0
    for _ in range(10000):
        x=rng.randint(5,100000); R=rng.randint(0,x+150); n+=1
        if R==0: actual=0
        else:
            r=R-1; A=candidate(x-1,r) if x>5 else K1048(x,r)
            actual=mex({A,K1048(x,r),1^K1047(x,r)})
        expected=candidate(x,R)
        if actual!=expected: failures.append(("scatter",x,R,actual,expected))
    counts["fixed_seed_child_mex_scatter"]=n
    return {"all_pass":not failures,
      "theorem":"H(R;(x,5);15), x>=5, all R>=0: complete Grundy classification",
      "classification":"universal proof by x-outer induction and complete A/B/C signature bands",
      "finite_audit_role":"two direct mex recurrences, published K1048/K1047 child anchors, signature coverage/identity/mex, low-R collapse, general tail, and fixed-seed scatter only",
      "scope":{"target":"H(R;(x,5);15), x>=5, R>=0","direct_x":[5,35],"direct_R":"0 <= R <= x+22",
        "anchor_x":[5,35],"anchor_R":"0 <= R <= x+22","signature_x":[5,2000],
        "signature_R":"1 <= R <= x+20","low_R":"0 <= R <= 16","low_x":[5,2000],
        "tail_R":"x+21 <= R <= x+24","tail_x":[5,5000],"scatter_points":10000,"scatter_seed":20261120},
      "counts":counts,"total_checks":sum(counts.values()),"failure_count":len(failures),"first_failures":failures[:20]}

def run():
    first=audit_once(); second=audit_once()
    a=json.dumps(first,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    b=json.dumps(second,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    same=a==b; verifier_sha=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result={**first,"repeat_runs":2,"repeat_byte_identical":same,
      "verifier_sha256":verifier_sha,"sha256_without_hash_field":hashlib.sha256(a).hexdigest()}
    payload=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    out=Path(__file__).with_name("output"); out.mkdir(parents=True,exist_ok=True)
    (out/"audit.json").write_text(payload,encoding="utf-8")
    print(payload,end="")
    return 0 if result["all_pass"] and same else 1

if __name__=="__main__": sys.exit(run())
