#!/usr/bin/env python3
"""Independent audit for the proved z=8, y=8 two-token residual slice."""
from __future__ import annotations
import hashlib
import json
from functools import lru_cache
from pathlib import Path

def mex(values):
    s=set(values); n=0
    while n in s:n+=1
    return n

def odd(r,a,b): return r%2==1 and a<=r<=b
def even(r,a,b): return r%2==0 and a<=r<=b
def ge(r,a): return r>=a

def z8_y7(x,r):
    if r==0:return 0
    t=(r in (1,3,5,7) or (x==9 and r==19) or
       (x==13 and r==21) or (x==16 and odd(r,23,31)) or
       (x>=17 and r==23))
    if x in (7,9):p=odd(r,9,17)
    elif x in (8,10):p=odd(r,9,17) or ge(r,19)
    elif x in (11,13):p=odd(r,9,19)
    elif x in (12,14):p=odd(r,9,19) or ge(r,21)
    elif x==15:p=odd(r,9,21)
    elif x==16:p=odd(r,9,21) or even(r,24,32) or ge(r,33)
    elif x%2:p=odd(r,9,21) or even(r,24,x+15)
    else:p=odd(r,9,21) or even(r,24,x+14) or ge(r,x+16)
    return 2 if t else 1 if p else 0

def z7_ge4(x,y,r):
    if r==0:return 0
    d=x-y;s=x+y
    t=(r in (1,3,5,7) or (d==3 and r==2*y+5) or
       (d==7 and r==2*y+7) or
       (d==8 and r in (2*y+7,2*y+9,2*y+11,2*y+13,2*y+15)) or
       (d>=9 and r==2*y+7))
    p=((d==0 and even(r,8,2*y+2)) or
       (d==1 and (even(r,8,2*y+8) or odd(r,2*y+5,2*y+7))) or
       (d==2 and even(r,8,2*y+4)) or
       (d==3 and (even(r,8,2*y+10) or odd(r,2*y+7,2*y+9))) or
       (d==4 and even(r,8,2*y+4)) or
       (d==5 and (even(r,8,2*y+12) or odd(r,2*y+7,2*y+11))) or
       (d==6 and even(r,8,2*y+6)) or
       (d==7 and (even(r,8,2*y+14) or odd(r,2*y+9,2*y+13))) or
       (d==8 and even(r,8,2*y+6)) or
       (d>=9 and (even(r,8,2*y+6) or odd(r,2*y+9,min(2*y+2*d-3,s+7)))))
    if t:return 2
    if p:return 1
    if r>=s+8:return s%2
    return 0

def candidate(x,r):
    if r==0:return 0
    t=(r in (1,3,5,7) or (x==10 and r==21) or
       (x==14 and r==23) or (x==17 and odd(r,25,33)) or
       (x>=18 and r==25))
    if x==8:p=odd(r,9,19)
    elif x in (9,11):p=odd(r,9,19) or ge(r,21)
    elif x==10:p=odd(r,9,19)
    elif x==12:p=odd(r,9,21)
    elif x in (13,15):p=odd(r,9,21) or ge(r,23)
    elif x==14:p=odd(r,9,21)
    elif x==16:p=odd(r,9,23)
    elif x==17:p=odd(r,9,23) or even(r,26,32) or ge(r,34)
    elif x==18:p=odd(r,9,23) or even(r,26,34)
    else:p=odd(r,9,23) or even(r,26,x+16) or (x%2==1 and ge(r,x+17))
    return 2 if t else 1 if p else 0

BANDS={
8:[(1,1,7,"01"),(1,9,19,"0"),(1,21,23,"1"),(0,2,8,"23"),(0,10,24,"1")],
9:[(1,1,7,"01"),(1,9,25,"0"),(0,2,8,"23"),(0,10,18,"1"),(0,20,20,"12"),(0,22,24,"0")],
10:[(1,1,7,"01"),(1,9,19,"0"),(1,21,21,"01"),(1,23,25,"1"),(0,2,8,"23"),(0,10,26,"1")],
11:[(1,1,7,"01"),(1,9,27,"0"),(0,2,8,"23"),(0,10,20,"1"),(0,22,22,"023"),(0,24,26,"0")],
12:[(1,1,7,"01"),(1,9,21,"0"),(1,23,27,"1"),(0,2,8,"23"),(0,10,28,"1")],
13:[(1,1,7,"01"),(1,9,29,"0"),(0,2,8,"23"),(0,10,20,"1"),(0,22,22,"12"),(0,24,28,"0")],
14:[(1,1,7,"01"),(1,9,21,"0"),(1,23,23,"01"),(1,25,29,"1"),(0,2,8,"23"),(0,10,30,"1")],
15:[(1,1,7,"01"),(1,9,31,"0"),(0,2,8,"23"),(0,10,22,"1"),(0,24,24,"023"),(0,26,30,"0")],
16:[(1,1,7,"01"),(1,9,23,"0"),(1,25,31,"1"),(0,2,8,"23"),(0,10,22,"1"),(0,24,32,"123")],
17:[(1,1,7,"01"),(1,9,23,"0"),(1,25,33,"01"),(0,2,8,"23"),(0,10,22,"1"),(0,24,24,"123"),(0,26,32,"0")],
18:[(1,1,7,"01"),(1,9,23,"0"),(1,25,25,"01"),(1,27,33,"1"),(0,2,8,"23"),(0,10,22,"1"),(0,24,24,"123"),(0,26,34,"02")],
}
def bands_for(x):
    if x in BANDS:return BANDS[x]
    return [(1,1,7,"01"),(1,9,23,"0"),(1,25,25,"01"),(1,27,x+16,"1"),
            (0,2,8,"23"),(0,10,22,"1"),(0,24,24,"123"),
            (0,26,26,"02"),(0,28,x+16,"0")]

def make_engines():
    @lru_cache(None)
    def ordered(r,tokens,z):
        if r==0:return 0
        opts=set()
        for i,v in enumerate(tokens):
            if v>1:opts.add(ordered(r-1,tokens[:i]+(v-1,)+tokens[i+1:],z))
            else:opts.add(ordered(r-1,tokens[:i]+tokens[i+1:],z+1))
        if z:opts.add(1^ordered(r-1,tokens,z-1))
        return mex(opts)
    @lru_cache(None)
    def canonical(r,tokens,z):
        if r==0:return 0
        opts=set();seen=set()
        for i,v in enumerate(tokens):
            if v in seen:continue
            seen.add(v)
            if v>1:child=tuple(sorted(tokens[:i]+(v-1,)+tokens[i+1:],reverse=True));opts.add(canonical(r-1,child,z))
            else:child=tuple(sorted(tokens[:i]+tokens[i+1:],reverse=True));opts.add(canonical(r-1,child,z+1))
        if z:opts.add(1^canonical(r-1,tokens,z-1))
        return mex(opts)
    return ordered,canonical

def audit_once():
    failures=[];ordered,canonical=make_engines();direct=0
    for x in range(8,61):
        for r in range(x+41):
            exp=candidate(x,r);a=ordered(r,(x,8),8);b=canonical(r,(x,8),8);direct+=2
            if a!=exp or b!=exp:failures.append(("target",x,r,a,b,exp))
    anchor=0
    for x in range(8,61):
        for r in range(x+41):
            b=canonical(r,(x,7),8);c=canonical(r,(x,8),7);anchor+=2
            if b!=z8_y7(x,r):failures.append(("B-anchor",x,r,b,z8_y7(x,r)))
            if c!=z7_ge4(x,8,r):failures.append(("C-anchor",x,r,c,z7_ge4(x,8,r)))
    sig=mexn=oddn=evenn=0
    for x in range(8,2001):
        for r in range(1,x+17):
            sig+=1
            hits=[s for p,lo,hi,s in bands_for(x) if r%2==p and lo<=r<=hi]
            if len(hits)!=1:failures.append(("coverage",x,r,hits));continue
            cr=r-1;a=z8_y7(8,cr) if x==8 else candidate(x-1,cr)
            b=z8_y7(x,cr);c=1^z7_ge4(x,8,cr)
            actual="".join(map(str,sorted({a,b,c})))
            if actual!=hits[0]:failures.append(("signature",x,r,hits[0],actual))
            v=mex({a,b,c});mexn+=1
            if v!=candidate(x,r):failures.append(("mex",x,r,v,candidate(x,r)))
            if r%2:oddn+=1
            else:evenn+=1
            if r%2 and v>2:failures.append(("odd-bound",x,r,v))
            if r%2==0 and v>1:failures.append(("even-bound",x,r,v))
    tail=0
    for x in range(8,5001):
        for off in range(4):
            r=x+17+off;tail+=1
            if candidate(x,r)!=(x+8)%2:failures.append(("tail",x,r,candidate(x,r),(x+8)%2))
    tailsig=0
    for x in range(8,2001):
        expected=str((x+7)%2)
        for off in range(4):
            r=x+17+off;tailsig+=1;cr=r-1
            a=z8_y7(8,cr) if x==8 else candidate(x-1,cr)
            b=z8_y7(x,cr);c=1^z7_ge4(x,8,cr)
            actual="".join(map(str,sorted({a,b,c})))
            if actual!=expected:failures.append(("tail-signature",x,r,actual,expected))
    theorem=0
    for x in range(8,2001):
        for r in range(x+29):
            theorem+=1;v=candidate(x,r)
            if v not in (0,1,2):failures.append(("range",x,r,v))
            if r%2==0 and v>1:failures.append(("even-Theorem-T",x,r,v))
            if r%2 and v>2:failures.append(("odd-Theorem-T",x,r,v))
    counts={"direct_formula_two_engines":direct,"independent_BC_anchor_direct":anchor,
      "signature_coverage_and_identity":sig,"mex_identity":mexn,
      "odd_parent_bound":oddn,"even_parent_bound":evenn,
      "tail_formula":tail,"tail_signature":tailsig,"Theorem_T_formula_grid":theorem}
    return {"all_pass":not failures,
      "classification":"universal proof by induction on x using explicit A/B/C signature bands, K0995, K0976, K0832 Theorem T and its high-R tail; finite checks are independent audits only",
      "counts":counts,"failures":failures,
      "scope":{"direct_x":[8,60],"direct_R":"0 <= R <= x+40",
        "anchor_x":[8,60],"anchor_R":"0 <= R <= x+40",
        "signature_R":"1 <= R <= x+16","signature_x":[8,2000],
        "tail_offsets":[0,3],"tail_signature_x":[8,2000],
        "tail_x":[8,5000],"theorem_R":"0 <= R <= x+28",
        "theorem_x":[8,2000]},
      "target":"H(R;(x,8);8), x>=8, R>=0","total_checks":sum(counts.values())}

def run():
    first=audit_once();second=audit_once()
    same=(json.dumps(first,ensure_ascii=False,sort_keys=True,separators=(",",":"))==
          json.dumps(second,ensure_ascii=False,sort_keys=True,separators=(",",":")))
    base=dict(first,repeat_runs=2,repeat_byte_identical=same)
    raw=json.dumps(base,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    result=dict(base,sha256_without_hash_field=hashlib.sha256(raw).hexdigest())
    out=Path(__file__).with_name("output");out.mkdir(exist_ok=True)
    (out/"audit.json").write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"all_pass":result["all_pass"],"counts":result["counts"],
      "failures":len(result["failures"]),"repeat_byte_identical":same,
      "sha256_without_hash_field":result["sha256_without_hash_field"],
      "total_checks":result["total_checks"]},sort_keys=True))
    if not result["all_pass"] or not same:raise SystemExit(1)
if __name__=="__main__":run()
