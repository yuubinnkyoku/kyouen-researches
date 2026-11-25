#!/usr/bin/env python3
"""Independent finite audit for the proved two-token residual slice z=6,y=8."""
from __future__ import annotations
import hashlib, json, random, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANCHOR = runpy.run_path(str(HERE.parent / "vertical-fiber-two-token-z6-y7-boundary-20261117" / "verify_z6_y7.py"))
mex, even, odd = ANCHOR["mex"], ANCHOR["even"], ANCHOR["odd"]
exact_ordered, exact_canonical = ANCHOR["exact_ordered"], ANCHOR["exact_canonical"]
h5, h6_y7 = ANCHOR["h5"], ANCHOR["h6_y7"]

def h6_y8(x: int, r: int) -> int:
    if r == 0: return 0
    base = {1, 3, 5}
    if x == 8: t, p = base | {19}, odd(r, 7, 17)
    elif x == 9: t, p = base, odd(r, 7, 23) or r >= 20
    elif x == 10: t, p = base, odd(r, 7, 19)
    elif x == 11: t, p = base, odd(r, 7, 21) or r >= 22
    elif x == 12: t, p = base | {21}, odd(r, 7, 19)
    elif x == 13: t, p = base, odd(r, 7, 21) or r >= 22
    elif x == 14: t, p = base, odd(r, 7, 21)
    elif x == 15: t, p = base | {23,25,27,29}, odd(r,7,21) or even(r,24,28) or r >= 30
    elif x >= 16 and x % 2 == 0: t, p = base | {23}, odd(r,7,21) or even(r,24,x+14)
    else: t, p = base | {23}, odd(r,7,21) or even(r,24,x+13) or r >= x+15
    return 2 if r in t else int(p)

SMALL = {
8:{1:[(1,5,"01"),(7,17,"0"),(19,19,"01"),(21,21,"1")],0:[(2,6,"23"),(8,22,"1")]},
9:{1:[(1,5,"01"),(7,23,"0")],0:[(2,6,"23"),(8,18,"1"),(20,20,"023"),(22,22,"0")]},
10:{1:[(1,5,"01"),(7,19,"0"),(21,23,"1")],0:[(2,6,"23"),(8,24,"1")]},
11:{1:[(1,5,"01"),(7,25,"0")],0:[(2,6,"23"),(8,18,"1"),(20,20,"12"),(22,24,"0")]},
12:{1:[(1,5,"01"),(7,19,"0"),(21,21,"01"),(23,25,"1")],0:[(2,6,"23"),(8,26,"1")]},
13:{1:[(1,5,"01"),(7,27,"0")],0:[(2,6,"23"),(8,20,"1"),(22,22,"023"),(24,26,"0")]},
14:{1:[(1,5,"01"),(7,21,"0"),(23,27,"1")],0:[(2,6,"23"),(8,20,"1"),(22,28,"123")]},
15:{1:[(1,5,"01"),(7,21,"0"),(23,29,"01")],0:[(2,6,"23"),(8,20,"1"),(22,22,"123"),(24,28,"0")]},
16:{1:[(1,5,"01"),(7,21,"0"),(23,23,"01"),(25,29,"1")],0:[(2,6,"23"),(8,20,"1"),(22,22,"123"),(24,30,"02")]}
}

def expected_signature(x,r):
    if x in SMALL: rows=SMALL[x][r%2]
    else:
        u=x+14 if x%2 else x+13
        v=x+13 if x%2 else x+14
        rows=([(1,5,"01"),(7,21,"0"),(23,23,"01"),(25,u,"1")] if r%2 else
              [(2,6,"23"),(8,20,"1"),(22,22,"123"),(24,24,"02"),(26,v,"0")])
    for lo,hi,digits in rows:
        if lo<=r<=hi and (r-lo)%2==0: return {int(c) for c in digits}
    return set()

def actual_signature(x,r):
    a=h6_y7(8,r-1) if x==8 else h6_y8(x-1,r-1)
    return {a,h6_y7(x,r-1),1^h5(x,8,r-1)}

def predicted_t(x):
    d=x-8
    extra=({19} if d==0 else {21} if d==4 else {23,25,27,29} if d==7 else {23} if d>=8 else set())
    return {1,3,5}|extra

def run_audit():
    failures=[]; direct=0
    for x in range(8,51):
        for r in range(x+41):
            for z,tokens,formula in ((6,(x,8),h6_y8(x,r)),(6,(x,7),h6_y7(x,r)),(5,(x,8),h5(x,8,r))):
                a=exact_ordered(r,tokens,z)
                b=exact_canonical(r,tuple(sorted(tokens,reverse=True)),z)
                direct+=1
                if a!=b or a!=formula: failures.append({"kind":"direct","x":x,"r":r,"z":z,"tokens":tokens,"ordered":a,"canonical":b,"formula":formula})
    sig=mexn=oddn=evenn=famn=0
    for x in range(8,2001):
        tactual=set()
        for r in range(1,x+15):
            opts=actual_signature(x,r); exp=expected_signature(x,r); sig+=1
            if opts!=exp: failures.append({"kind":"signature","x":x,"r":r,"actual":sorted(opts),"expected":sorted(exp)})
            val=mex(opts); mexn+=1
            if val!=h6_y8(x,r): failures.append({"kind":"mex","x":x,"r":r,"options":sorted(opts),"actual":val,"formula":h6_y8(x,r)})
            if val==2: tactual.add(r)
            if r%2:
                oddn+=1
                if not opts<={0,1}: failures.append({"kind":"odd-bound","x":x,"r":r,"options":sorted(opts)})
            else:
                evenn+=1
                if val>1: failures.append({"kind":"even-bound","x":x,"r":r,"value":val})
        famn+=1
        if tactual!=predicted_t(x): failures.append({"kind":"three-family","x":x,"actual":sorted(tactual),"predicted":sorted(predicted_t(x))})
    tail=0
    for x in range(8,2001):
        for off in range(65):
            r=x+15+off; tail+=1
            if h6_y8(x,r)!=(x+8)%2: failures.append({"kind":"tail","x":x,"r":r,"actual":h6_y8(x,r),"expected":(x+8)%2})
    rng=random.Random(20261117); rand=0
    for _ in range(2000):
        x=rng.randint(8,100000); r=x+15+rng.randint(0,100000); rand+=1
        if h6_y8(x,r)!=(x+8)%2: failures.append({"kind":"random-tail","x":x,"r":r,"actual":h6_y8(x,r),"expected":(x+8)%2})
    counts={"direct_two_engine_formula_anchor_checks":direct,"option_signature_checks":sig,"mex_identity_checks":mexn,"odd_parent_option_bound_checks":oddn,"even_parent_value_bound_checks":evenn,"three_family_value2_specialization_checks":famn,"tail_checks":tail,"fixed_seed_random_tail_checks":rand}
    audit={"schema":"two-token-z6-y8-audit-v1","claim":"H(R;(x,8);6) is given by the complete formula for all x>=8,R>=0","classification":"finite-independent-audit-not-proof","counts":counts,"total_checks":sum(counts.values()),"seed":20261117,"failures":failures,"pass":not failures}
    encoded=json.dumps(audit,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    audit["sha256_without_hash_field"]=hashlib.sha256(encoded.encode("utf-8")).hexdigest()
    return audit

def main():
    audit=run_audit(); output=HERE/"output"/"audit.json"; output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(audit,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"pass":audit["pass"],"total_checks":audit["total_checks"],"failures":len(audit["failures"]),"sha256_without_hash_field":audit["sha256_without_hash_field"],"output":str(output)},ensure_ascii=False,sort_keys=True))
    if not audit["pass"]: raise SystemExit(1)

if __name__=="__main__": main()
