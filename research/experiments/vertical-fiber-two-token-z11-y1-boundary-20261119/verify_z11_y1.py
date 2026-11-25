#!/usr/bin/env python3
"""Independent verifier for the z=11, y=1 two-token residual-game slice."""
from __future__ import annotations
import json, random, sys
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(1_000_000)

def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

@lru_cache(None)
def H_ordered(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)

@lru_cache(None)
def H_canonical(R, X, z):
    X = tuple(sorted(X))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            opts.add(H_canonical(R - 1, tuple(sorted(X[:i] + (v - 1,) + X[i + 1:])), z))
        else:
            opts.add(H_canonical(R - 1, X[:i] + X[i + 1:], z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)

def q_odd(k):
    return k if k % 2 else k - 1

def single_token(x, z, R):
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))

# K1003, z=10 and y=1.
T10 = {
    1:{1}, 2:{1,3}, 3:{1,3}, 4:{1,3,5}, 5:{1,3,5},
    6:{1,3,5,7}, 7:{1,3,5,7}, 8:{1,3,5,7,9},
    9:{1,3,5,7,9,11}, 10:{1,3,5,7,9}, 11:{1,3,5,7,9}
}
def h10_T(x, r):
    if x in T10:
        return r in T10[x]
    if x == 12:
        return r in (1,3,5,7,9) or (13 <= r <= 23 and r % 2 == 1)
    return r in (1,3,5,7,9,13)
def h10_P(x, r):
    if x in (1,3,5,7,9): return False
    if x == 2: return r >= 4
    if x == 4: return r >= 6
    if x == 6: return r >= 8
    if x == 8: return r >= 10
    if x == 10: return r >= 11
    if x == 11: return r == 11
    if x == 12: return r == 11 or (14 <= r <= 22 and r % 2 == 0) or r >= 24
    if x % 2: return r == 11 or (14 <= r <= x + 11 and r % 2 == 0)
    return r == 11 or (14 <= r <= x + 10 and r % 2 == 0) or r >= x + 12
def h10_y1(x, r):
    if r == 0: return 0
    if h10_T(x, r): return 2
    if h10_P(x, r): return 1
    return 0

def T11(x, r):
    if x <= 12: return 1 <= r <= x + 1 and r % 2 == 1
    if x == 13: return 1 <= r <= 25 and r % 2 == 1
    return r in (1,3,5,7,9,11,13)
def P11(x, r):
    if x == 1: return False
    if x <= 10: return x % 2 == 0 and r >= x + 2
    if x == 11: return r == 12
    if x == 12: return r == 12 or r >= 14
    if x == 13: return r == 12
    if x % 2 == 0:
        return r == 12 or (r % 2 == 1 and 15 <= r <= x + 13) or r >= x + 14
    return r == 12 or (r % 2 == 1 and 15 <= r <= x + 12)
def candidate(x, R):
    if R == 0: return 0
    if T11(x, R): return 2
    if P11(x, R): return 1
    return 0

def band_signature(x, R):
    if x == 1: return "01" if R == 1 else "23" if R == 2 else "1"
    if x == 2: return {1:"01",2:"23",3:"01",4:"03"}.get(R,"0")
    if x == 3: return {1:"01",2:"23",3:"01",4:"23"}.get(R,"1")
    if x == 4: return {1:"01",2:"23",3:"01",4:"23",5:"01",6:"03"}.get(R,"0")
    if x == 5:
        return ("01" if R <= 5 else "1") if R % 2 else ("23" if R <= 6 else "1")
    if x == 6:
        if R % 2: return "01" if R <= 7 else "0"
        if R <= 6: return "23"
        return "03" if R == 8 else "0"
    if x == 7:
        return ("01" if R <= 7 else "1") if R % 2 else ("23" if R <= 8 else "1")
    if x == 8:
        if R % 2: return "01" if R <= 9 else "0"
        if R <= 8: return "23"
        return "03" if R == 10 else "0"
    if x == 9:
        if R % 2: return "01" if R <= 9 else "1"
        if R <= 10: return "23"
        return "13" if R == 12 else "1"
    if x == 10:
        if R % 2: return "01" if R <= 11 else "0"
        return "23" if R <= 10 else "0"
    if x == 11:
        if R % 2: return "01" if R <= 11 else "1"
        if R <= 10: return "23"
        return "02" if R == 12 else "1"
    if x == 12:
        if R % 2:
            return "01" if R <= 13 else "0"
        if R <= 10: return "23"
        if R == 12: return "02"
        return "023" if R <= 24 else "0"
    if x == 13:
        if R % 2: return "01" if R <= 25 else "1"
        if R <= 10: return "23"
        if R == 12: return "02"
        if R == 14: return "123"
        return "1"
    if x == 14:
        if R % 2:
            if R <= 11 or R == 13: return "01"
            return "0"
        if R <= 10: return "23"
        if R == 12: return "02"
        if R == 14: return "123"
        return "12" if 16 <= R <= 26 else "0"
    if R % 2:
        if R <= 11 or R == 13: return "01"
        if R <= x + 13: return "0"
        return "0" if x % 2 == 0 else "1"
    if R <= 10: return "23"
    if R == 12: return "02"
    if R == 14: return "123"
    if R <= x + 12: return "1"
    return "0" if x % 2 == 0 else "1"

def sig_values(s):
    return {int(ch) for ch in s}

def run_audit():
    audit = {"checks": {}, "fail": [], "n_points": 0}
    def check(name, ok, detail):
        audit["checks"][name] = {"ok": bool(ok), **detail}
        if not ok: audit["fail"].append(name)

    # V1-V3: two direct engines.
    bad = [0,0,0]; ex = [None,None,None]; n = 0
    for x in range(1,81):
        for R in range(0,x+46):
            n += 1
            a = H_ordered(R,(x,1),11)
            b = H_canonical(R,(x,1),11)
            c = candidate(x,R)
            for j, ok in enumerate((a == c, b == c, a == b)):
                if not ok:
                    bad[j] += 1
                    if ex[j] is None: ex[j] = (x,R,a,b,c)
    for j,name in enumerate(("V1_ordered_direct_vs_formula","V2_canonical_direct_vs_formula","V3_two_direct_engines_agree")):
        check(name,bad[j] == 0,{"points":n,"bad":bad[j],"example":ex[j]})
    audit["n_points"] += 3*n

    # V4-V8: anchor and full signature-band table.
    names = ("V4_ABC_anchor_mex","V5_signature_band_coverage","V6_signature_band_matches_ABC","V7_signature_mex_matches","V8_signature_mex_vs_formula")
    bad = [0]*5; ex = [None]*5; n = 0
    for x in range(1,3001):
        for R in range(1,x+31):
            n += 1
            r = R-1
            opts = set()
            if x >= 2: opts.add(candidate(x-1,r))
            opts.add(single_token(x,12,r))
            opts.add(1 ^ h10_y1(x,r))
            am = mex(opts)
            actual = "".join(map(str,sorted(opts)))
            expected = band_signature(x,R)
            if am != candidate(x,R):
                bad[0] += 1
                if ex[0] is None: ex[0] = (x,R,am,candidate(x,R),actual)
            if expected is None:
                bad[1] += 1
                if ex[1] is None: ex[1] = (x,R)
            elif expected != actual:
                bad[2] += 1
                if ex[2] is None: ex[2] = (x,R,expected,actual)
            else:
                tm = mex(sig_values(expected))
                if tm != am:
                    bad[3] += 1
                    if ex[3] is None: ex[3] = (x,R,expected,tm,am)
                if tm != candidate(x,R):
                    bad[4] += 1
                    if ex[4] is None: ex[4] = (x,R,expected,tm,candidate(x,R))
    for j,name in enumerate(names):
        check(name,bad[j] == 0,{"points":n,"bad":bad[j],"example":ex[j]})
    audit["n_points"] += 5*n

    # V9-V10: tail and parity.
    bad_tail = 0; ex_tail = None
    for x in range(1,10001):
        for off in range(5):
            R = x+13+off
            got = candidate(x,R); want = (x+1)%2
            if got != want:
                bad_tail += 1
                if ex_tail is None: ex_tail = (x,R,got,want)
    parity_bad = 0; ex_parity = None
    for x in range(1,3001):
        for R in range(1,x+31):
            got = candidate(x,R); bound = 2 if R%2 else 1
            if got > bound:
                parity_bad += 1
                if ex_parity is None: ex_parity = (x,R,got,bound)
    tail_points = 50000
    parity_points = sum(x+30 for x in range(1,3001))
    check("V9_general_tail",bad_tail == 0,{"points":tail_points,"bad":bad_tail,"example":ex_tail,"claim":"R >= x+13 => H=(x+1) mod 2"})
    check("V10_theorem_T_parity_bound",parity_bad == 0,{"points":parity_points,"bad":parity_bad,"example":ex_parity})
    audit["n_points"] += tail_points + parity_points

    # V11: single-token z=12; V12: K1003 child.
    bad_single = 0; ex_single = None; n = 0
    for x in range(1,81):
        for R in range(0,81):
            n += 1
            a = H_ordered(R,(x,),12); b = single_token(x,12,R)
            if a != b:
                bad_single += 1
                if ex_single is None: ex_single = (x,R,a,b)
    check("V11_single_token_z12_anchor",bad_single == 0,{"points":n,"bad":bad_single,"example":ex_single})
    audit["n_points"] += n

    bad_h10 = 0; ex_h10 = None; n = 0
    for x in range(1,81):
        for R in range(0,x+46):
            n += 1
            a = H_ordered(R,(x,1),10); b = h10_y1(x,R)
            if a != b:
                bad_h10 += 1
                if ex_h10 is None: ex_h10 = (x,R,a,b)
    check("V12_K1003_child_anchor",bad_h10 == 0,{"points":n,"bad":bad_h10,"example":ex_h10})
    audit["n_points"] += n

    # V13: fixed-seed broad scatter.
    rng = random.Random(20261119)
    bad_scatter = 0; ex_scatter = None; n = 20000
    for _ in range(n):
        x = rng.randint(1,1500); R = rng.randint(0,x+100)
        if R == 0:
            am = 0
        else:
            r = R-1; opts = set()
            if x >= 2: opts.add(candidate(x-1,r))
            opts.add(single_token(x,12,r))
            opts.add(1 ^ h10_y1(x,r))
            am = mex(opts)
        got = candidate(x,R)
        if am != got:
            bad_scatter += 1
            if ex_scatter is None: ex_scatter = (x,R,am,got)
    check("V13_fixed_seed_scatter",bad_scatter == 0,{"points":n,"bad":bad_scatter,"example":ex_scatter,"seed":20261119})
    audit["n_points"] += n
    audit["all_ok"] = not audit["fail"]
    return audit

def main():
    audit = run_audit()
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True,exist_ok=True)
    payload = json.dumps(audit,sort_keys=True,indent=2) + "\n"
    (out / "audit.json").write_text(payload,encoding="utf-8")
    print(payload,end="")
    return 0 if audit["all_ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
