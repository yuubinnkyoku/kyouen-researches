#!/usr/bin/env python3
"""Independent audit for the proved z=6, y=32 two-token slice."""
from __future__ import annotations
import hashlib, json, sys
from functools import lru_cache
from pathlib import Path
sys.setrecursionlimit(10000)

def mex(v):
    s=set(v); n=0
    while n in s: n+=1
    return n

def O(r,a,b=None): return r>=a and (b is None or r<=b) and r%2==1
def E(r,a,b=None): return r>=a and (b is None or r<=b) and r%2==0

def h5(x,y,r):
    if r==0: return 0
    s,d=x+y,x-y; t={1,3,5}
    if d==1 and y>=2: t.add(2*y+3)
    elif d==5: t.add(2*y+5)
    elif d==6: t.update({2*y+5,2*y+7,2*y+9,2*y+11})
    elif d>=7: t.add(2*y+5)
    if r in t: return 2
    if d==0: one=E(r,6,s+2) if y>=3 else False
    elif d==1: one=(E(r,6,s+3) or r>=s+4) if y>=2 else r>=4
    elif d==2: one=E(r,6,s) if y>=2 else False
    elif d==3: one=E(r,6,s+1) or r>=s+2
    elif d==4: one=E(r,6,s)
    elif d==5: one=E(r,6,s-1) or r>=s+1
    elif d==6: one=E(r,6,s-2)
    elif d%2: one=E(r,6,2*y+4) or O(r,2*y+7,s+4) or r>=s+6
    else: one=E(r,6,2*y+4) or O(r,2*y+7,s+5)
    return int(one)

def h31(x,r):
    if r==0: return 0
    t={1,3,5}
    if x==31: t.add(65)
    elif x==35: t.add(67)
    elif x==38: t.update({69,71,73,75})
    elif x>=39: t.add(69)
    if r in t: return 2
    if x==31: one=O(r,7,63)
    elif x==32: one=O(r,7,69) or E(r,66,68) or r>=70
    elif x==33: one=O(r,7,65)
    elif x==34: one=O(r,7,71) or E(r,68,70) or r>=72
    elif x==35: one=O(r,7,65)
    elif x==36: one=O(r,7,73) or E(r,68,72) or r>=74
    elif x==37: one=O(r,7,67)
    elif x==38: one=O(r,7,67) or E(r,70,74) or r>=76
    elif x%2: one=O(r,7,67) or E(r,70,x+37)
    else: one=O(r,7,67) or E(r,70,x+36) or r>=x+38
    return int(one)

def T32(x):
    t={1,3,5}
    if x==32: t.add(67)
    elif x==36: t.add(69)
    elif x==39: t.update({71,73,75,77})
    elif x>=40: t.add(71)
    return t

def P32(x,r):
    if x==32: return O(r,7,65)
    if x==33: return O(r,7,71) or E(r,68,70) or r>=72
    if x==34: return O(r,7,67)
    if x==35: return O(r,7,73) or E(r,70,72) or r>=74
    if x==36: return O(r,7,67)
    if x==37: return O(r,7,75) or E(r,70,74) or r>=76
    if x==38: return O(r,7,69)
    if x==39: return O(r,7,69) or E(r,72,76) or r>=78
    if x%2==0: return O(r,7,69) or E(r,72,x+38)
    return O(r,7,69) or E(r,72,x+37) or r>=x+39

def h32_closed(x,r):
    if r==0: return 0
    if r in T32(x): return 2
    return int(P32(x,r))

@lru_cache(None)
def h32_rec(x,r):
    if r==0: return 0
    a=h31(32,r-1) if x==32 else h32_rec(x-1,r-1)
    b=h31(x,r-1); c=1^h5(x,32,r-1)
    return mex((a,b,c))

# Each interval is (first,last,signature); signatures are sorted tuples.
ODD={
 32:[(1,5,(0,1)),(7,65,(0,)),(67,67,(0,1)),(69,69,(1,))],
 33:[(1,5,(0,1)),(7,71,(0,))],
 34:[(1,5,(0,1)),(7,67,(0,)),(69,71,(1,))],
 35:[(1,5,(0,1)),(7,73,(0,))],
 36:[(1,5,(0,1)),(7,67,(0,)),(69,69,(0,1)),(71,73,(1,))],
 37:[(1,5,(0,1)),(7,75,(0,))],
 38:[(1,5,(0,1)),(7,69,(0,)),(71,75,(1,))],
 39:[(1,5,(0,1)),(7,69,(0,)),(71,77,(0,1))],
}
EVEN={
 32:[(2,6,(2,3)),(8,70,(1,))],
 33:[(2,6,(2,3)),(8,66,(1,)),(68,68,(0,2,3)),(70,70,(0,))],
 34:[(2,6,(2,3)),(8,72,(1,))],
 35:[(2,6,(2,3)),(8,66,(1,)),(68,68,(1,2)),(70,72,(0,))],
 36:[(2,6,(2,3)),(8,74,(1,))],
 37:[(2,6,(2,3)),(8,68,(1,)),(70,70,(0,2,3)),(72,74,(0,))],
 38:[(2,6,(2,3)),(8,68,(1,)),(70,76,(1,2,3))],
 39:[(2,6,(2,3)),(8,68,(1,)),(70,70,(1,2,3)),(72,76,(0,))],
 40:[(2,6,(2,3)),(8,68,(1,)),(70,70,(1,2,3)),(72,78,(0,2))],
}
def sig_expected(x,r):
    if r&1:
        rows=ODD.get(x)
        if rows is None:
            end=x+37 if x%2==0 else x+38
            rows=[(1,5,(0,1)),(7,69,(0,)),(71,71,(0,1)),(73,end,(1,))]
    else:
        rows=EVEN.get(x)
        if rows is None:
            end=x+38 if x%2==0 else x+37
            rows=[(2,6,(2,3)),(8,68,(1,)),(70,70,(1,2,3)),(72,72,(0,2)),(74,end,(0,))]
    for a,b,s in rows:
        if a<=r<=b and (r-a)%2==0: return s
    return None

def direct_engines():
    @lru_cache(None)
    def ordered(r,tokens,z):
        if r==0:return 0
        out=[]
        for i,v in enumerate(tokens):
            c=list(tokens); nz=z
            if v>=2:c[i]-=1
            else:c.pop(i); nz+=1
            out.append(ordered(r-1,tuple(c),nz))
        if z:out.append(1^ordered(r-1,tokens,z-1))
        return mex(out)
    @lru_cache(None)
    def canonical(r,tokens,z):
        if r==0:return 0
        out=[]
        for i,v in enumerate(tokens):
            c=list(tokens); nz=z
            if v>=2:c[i]-=1
            else:c.pop(i); nz+=1
            out.append(canonical(r-1,tuple(sorted(c,reverse=True)),nz))
        if z:out.append(1^canonical(r-1,tokens,z-1))
        return mex(out)
    return ordered,canonical

def audit_once():
    failures=[]; ordered,canonical=direct_engines(); direct=0
    for x in range(32,61):
        for r in range(x+51):
            for tag,tokens,z,value in (
                ("target",(x,32),6,h32_closed(x,r)),
                ("y31",(x,31),6,h31(x,r)),
                ("z5",(x,32),5,h5(x,32,r)),
            ):
                a=ordered(r,tokens,z); b=canonical(r,tuple(sorted(tokens,reverse=True)),z); direct+=2
                if a!=value or b!=value: failures.append(("direct",tag,x,r,a,b,value))
    sigs=mexclosed=mexrec=odd=even=0; params=0
    for x in range(32,2001):
        twos=set()
        for r in range(1,x+39):
            q=r-1; a=h31(32,q) if x==32 else h32_rec(x-1,q)
            b=h31(x,q); c=1^h5(x,32,q); actual=tuple(sorted({a,b,c}))
            want=sig_expected(x,r); sigs+=1
            if actual!=want: failures.append(("signature",x,r,actual,want)); continue
            v=mex(actual); mexclosed+=1
            if v!=h32_closed(x,r): failures.append(("closed",x,r,v,h32_closed(x,r)))
            if v!=h32_rec(x,r): failures.append(("recurrence",x,r,v,h32_rec(x,r)))
            mexrec+=1
            if r&1:
                odd+=1
                if not set(actual)<= {0,1}: failures.append(("odd-bound",x,r,actual))
            else:
                even+=1
                if v>1: failures.append(("even-bound",x,r,v,actual))
            if v==2: twos.add(r)
        params+=1
        if twos!=T32(x): failures.append(("T32",x,sorted(twos),sorted(T32(x))))
    tail=0
    for x in range(32,2001):
        for r in range(x+39,x+103):
            tail+=1; want=(x+32)&1
            if h32_closed(x,r)!=want: failures.append(("tail",x,r,h32_closed(x,r),want))
    return {
      "schema":"kyouen-z6-y32-audit-v1",
      "range":{"direct_x":[32,60],"direct_r":"0..x+50","signature_x":[32,2000],"signature_r":"1..x+38","tail_r":"x+39..x+102"},
      "checks":{"direct_ordered_and_canonical":direct,"explicit_ABC_signatures":sigs,"mex_equals_closed_formula":mexclosed,"mex_equals_independent_recurrence":mexrec,"odd_parent_child_bound":odd,"even_parent_value_bound":even,"tail_parity":tail,"x_parameters":params},
      "failures":failures[:20],"failure_count":len(failures),
      "cache":{"h32_recurrence_states":h32_rec.cache_info().currsize,"ordered_states":ordered.cache_info().currsize,"canonical_states":canonical.cache_info().currsize}
    }

def main():
    body=audit_once(); body["verifier_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    raw=json.dumps(body,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    body["audit_sha256"]=hashlib.sha256(raw.encode()).hexdigest()
    out=json.dumps(body,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    p=Path(__file__).with_name("output")/"audit.json"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(out,encoding="utf-8")
    print(out,end="")
    if body["failure_count"]: raise SystemExit(1)
if __name__=="__main__": main()
