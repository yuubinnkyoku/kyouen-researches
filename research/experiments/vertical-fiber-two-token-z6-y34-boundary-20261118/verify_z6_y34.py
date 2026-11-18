#!/usr/bin/env python3
"""Independent finite audit for the proved z=6, y=34 two-token slice.

The universal proof is the x-induction and the explicit A/B/C signature table
in report.md. This script corroborates it with two direct recursions, a separate
A/B/C recursion, signature/mex checks, and the K0832 tail.
"""
from __future__ import annotations
import hashlib, json, sys
from functools import lru_cache
from pathlib import Path
sys.setrecursionlimit(10000)

def mex(values):
    s=set(values); n=0
    while n in s: n+=1
    return n

def O(r,a,b=None): return r>=a and (b is None or r<=b) and r%2==1
def E(r,a,b=None): return r>=a and (b is None or r<=b) and r%2==0

def h5(x,y,r):
    """K0873: exact z=5 two-token formula."""
    if r==0: return 0
    s,d=x+y,x-y
    twos={1,3,5}
    if d==1 and y>=2: twos.add(2*y+3)
    elif d==5: twos.add(2*y+5)
    elif d==6: twos.update({2*y+5,2*y+7,2*y+9,2*y+11})
    elif d>=7: twos.add(2*y+5)
    if r in twos: return 2
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

def T33(x):
    t={1,3,5}
    if x==33: t.add(69)
    elif x==37: t.add(71)
    elif x==40: t.update({73,75,77,79})
    elif x>=41: t.add(73)
    return t

def P33(x,r):
    if x==33: return O(r,7,67)
    if x==34: return O(r,7,73) or E(r,70,72) or r>=74
    if x==35: return O(r,7,69)
    if x==36: return O(r,7,75) or E(r,72,74) or r>=76
    if x==37: return O(r,7,69)
    if x==38: return O(r,7,77) or E(r,72,76) or r>=78
    if x==39: return O(r,7,71)
    if x%2==0: return O(r,7,71) or E(r,74,x+38) or r>=x+40
    return O(r,7,71) or E(r,74,x+39)

def h33(x,r):
    if r==0: return 0
    if r in T33(x): return 2
    return int(P33(x,r))

def T34(x):
    t={1,3,5}
    if x==34: t.add(71)
    elif x==38: t.add(73)
    elif x==41: t.update({75,77,79,81})
    elif x>=42: t.add(75)
    return t

def P34(x,r):
    if x==34: return O(r,7,69)
    if x==35: return O(r,7) or E(r,72)
    if x==36: return O(r,7,71)
    if x==37: return O(r,7) or E(r,74)
    if x==38: return O(r,7,71)
    if x==39: return O(r,7) or E(r,74)
    if x==40: return O(r,7,73)
    if x==41: return O(r,7,73) or E(r,76) or r>=82
    if x%2==0: return O(r,7,73) or E(r,76,x+40)
    return O(r,7,73) or E(r,76) or r>=x+41

def h34_closed(x,r):
    if r==0: return 0
    if r in T34(x): return 2
    return int(P34(x,r))

@lru_cache(None)
def h34_induction(x,r):
    if r==0: return 0
    a=h33(34,r-1) if x==34 else h34_induction(x-1,r-1)
    b=h33(x,r-1)
    c=1 ^ h5(x,34,r-1)
    return mex((a,b,c))

def expected_rows(x, parity):
    if parity:
        table={
          34:[(1,5,(0,1)),(7,69,(0,)),(71,71,(0,1)),(73,73,(1,))],
          35:[(1,5,(0,1)),(7,75,(0,))],
          36:[(1,5,(0,1)),(7,71,(0,)),(73,75,(1,))],
          37:[(1,5,(0,1)),(7,77,(0,))],
          38:[(1,5,(0,1)),(7,71,(0,)),(73,73,(0,1)),(75,77,(1,))],
          39:[(1,5,(0,1)),(7,79,(0,))],
          40:[(1,5,(0,1)),(7,73,(0,)),(75,79,(1,))],
          41:[(1,5,(0,1)),(7,73,(0,)),(75,81,(0,1))],
          42:[(1,5,(0,1)),(7,73,(0,)),(75,75,(0,1)),(77,81,(1,))],
        }
        return table.get(x,[(1,5,(0,1)),(7,73,(0,)),(75,75,(0,1)),(77,x+40,(1,))])
    table={
      34:[(2,6,(2,3)),(8,74,(1,))],
      35:[(2,6,(2,3)),(8,70,(1,)),(72,72,(0,2,3)),(74,74,(0,))],
      36:[(2,6,(2,3)),(8,76,(1,))],
      37:[(2,6,(2,3)),(8,70,(1,)),(72,72,(1,2)),(74,76,(0,))],
      38:[(2,6,(2,3)),(8,78,(1,))],
      39:[(2,6,(2,3)),(8,72,(1,)),(74,74,(0,2,3)),(76,78,(0,))],
      40:[(2,6,(2,3)),(8,72,(1,)),(74,80,(1,2,3))],
      41:[(2,6,(2,3)),(8,72,(1,)),(74,74,(1,2,3)),(76,80,(0,))],
      42:[(2,6,(2,3)),(8,72,(1,)),(74,74,(1,2,3)),(76,82,(0,2))],
    }
    if x in table: return table[x]
    end=x+(39 if x&1 else 40)
    return [(2,6,(2,3)),(8,72,(1,)),(74,74,(1,2,3)),(76,76,(0,2)),(78,end,(0,))]

def expected_signature(x,r):
    for a,b,sig in expected_rows(x,r&1):
        if a<=r<=b and (r-a)%2==0: return sig
    return None

def direct_engines():
    @lru_cache(None)
    def ordered(r,tokens,z):
        if r==0: return 0
        out=[]
        for i,v in enumerate(tokens):
            c=list(tokens); nz=z
            if v>=2: c[i]-=1
            else: c.pop(i); nz+=1
            out.append(ordered(r-1,tuple(c),nz))
        if z: out.append(1^ordered(r-1,tokens,z-1))
        return mex(out)
    @lru_cache(None)
    def canonical(r,tokens,z):
        if r==0: return 0
        out=[]
        for i,v in enumerate(tokens):
            c=list(tokens); nz=z
            if v>=2: c[i]-=1
            else: c.pop(i); nz+=1
            out.append(canonical(r-1,tuple(sorted(c,reverse=True)),nz))
        if z: out.append(1^canonical(r-1,tokens,z-1))
        return mex(out)
    return ordered,canonical

def audit_once():
    failures=[]; ordered,canonical=direct_engines(); direct_calls=0
    for x in range(34,58):
        for r in range(x+56):
            want=h34_closed(x,r)
            a=ordered(r,(x,34),6); b=canonical(r,(x,34),6)
            direct_calls+=2
            if a!=want or b!=want: failures.append(("direct",x,r,a,b,want))
    recurrence_count=0
    for x in range(34,81):
        for r in range(x+56):
            got=h34_induction(x,r); want=h34_closed(x,r)
            recurrence_count+=1
            if got!=want: failures.append(("induction",x,r,got,want))
    signature_count=mex_count=odd_count=even_count=0
    for x in range(34,2001):
        twos=set()
        for r in range(1,x+41):
            q=r-1
            a=h33(34,q) if x==34 else h34_closed(x-1,q)
            b=h33(x,q)
            c=1^h5(x,34,q)
            actual=tuple(sorted({a,b,c}))
            expected=expected_signature(x,r)
            signature_count+=1
            if actual!=expected:
                failures.append(("signature",x,r,actual,expected)); continue
            v=mex(actual); mex_count+=1
            if v!=h34_closed(x,r): failures.append(("mex",x,r,v,h34_closed(x,r)))
            if r&1:
                odd_count+=1
                if not set(actual)<={0,1}: failures.append(("odd-bound",x,r,actual))
            else:
                even_count+=1
                if v>1: failures.append(("even-bound",x,r,v,actual))
            if v==2: twos.add(r)
        if twos!=T34(x): failures.append(("T34",x,sorted(twos),sorted(T34(x))))
    tail_count=0
    for x in range(34,2001):
        val=(x+34)&1
        for r in range(x+41,x+105):
            tail_count+=1
            if h34_closed(x,r)!=val: failures.append(("tail",x,r,h34_closed(x,r),val))
    return {
      "schema":"kyouen-z6-y34-audit-v1",
      "range":{"direct_x":[34,57],"direct_r":"0..x+55","induction_x":[34,80],"induction_r":"0..x+55","signature_x":[34,2000],"signature_r":"1..x+40","tail_r":"x+41..x+104"},
      "checks":{"ordered_and_canonical_direct_calls":direct_calls,"independent_A_B_C_recurrence":recurrence_count,"ABC_signatures":signature_count,"mex_equals_closed_formula":mex_count,"odd_parent_child_bound":odd_count,"even_parent_value_bound":even_count,"tail_parity":tail_count,"x_parameters":1967},
      "failures":failures[:30],"failure_count":len(failures),
      "cache":{"induction_states":h34_induction.cache_info().currsize,"ordered_states":ordered.cache_info().currsize,"canonical_states":canonical.cache_info().currsize}}

def main():
    body=audit_once()
    body["verifier_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    canonical=json.dumps(body,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    body["audit_sha256"]=hashlib.sha256(canonical.encode()).hexdigest()
    out=json.dumps(body,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    output=Path(__file__).with_name("output"); output.mkdir(parents=True,exist_ok=True)
    (output/"audit.json").write_text(out,encoding="utf-8")
    print(out,end="")
    if body["failure_count"]: raise SystemExit(1)
if __name__=="__main__": main()
