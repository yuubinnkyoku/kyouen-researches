#!/usr/bin/env python3
"""Independent verifier for the z=12, y=1 two-token residual-game slice.

Theorem (candidate, machine-derived from census, anchored on published child
theorems):
  * value-2 positions T(x):  x=1: {1}; x even <=10: O[1,x+1]; x odd <=9: O[1,x];
    x=11: O[1,13]; x=12,13: O[1,11]; x=14: O[1,11] u O[15,27]; x>=15: {1,3,5,7,9,11,15}.
  * value-1 positions P(x): x even <=10: I[x+2,inf); x odd <=11: empty;
    x=12: I[13,inf); x=13: {13}; x even >=14: {13} u E[16,x+12] u I[x+14,inf);
    x odd >=15: {13} u E[16,x+13].
  * tail: R >= x+14 => H = (x+1) mod 2.
Children: A = H(R-1;(x-1,1);12) (x-outer induction, same slice row x-1),
B = single_token(x, 13, R-1) (K0832 universal single-token closed form),
C = 1 xor K1012 (z=11, y=1 published slice). At x=1 both removal moves
coincide in the single-token child.
"""
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

# K1012, z=11, y=1 (published universal slice).
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
def h11_y1(x, r):
    if r == 0: return 0
    if T11(x, r): return 2
    if P11(x, r): return 1
    return 0

# z=12, y=1 candidate closed form.
def T12(x, r):
    if x == 1: return r == 1
    if x <= 10:
        top = x + 1 if x % 2 == 0 else x
        return 1 <= r <= top and r % 2 == 1
    if x == 11: return 1 <= r <= 13 and r % 2 == 1
    if x <= 13: return 1 <= r <= 11 and r % 2 == 1
    if x == 14:
        return (1 <= r <= 11 or 15 <= r <= 27) and r % 2 == 1
    return r in (1,3,5,7,9,11,15)
def P12(x, r):
    if x % 2 == 1:
        if x <= 11: return False
        if x == 13: return r == 13
        return r == 13 or (r % 2 == 0 and 16 <= r <= x + 13)
    if x <= 10: return r >= x + 2
    if x == 12: return r >= 13
    # x even, >= 14
    return r == 13 or (r % 2 == 0 and 16 <= r <= x + 12) or r >= x + 14
def candidate(x, R):
    if R == 0: return 0
    if T12(x, R): return 2
    if P12(x, R): return 1
    return 0

def band_signature(x, R):
    # head bands shared by most rows
    if x == 1:
        return "01" if R == 1 else "23" if R == 2 else "1"
    if x == 2:
        return {1:"01",2:"23",3:"01",4:"03"}.get(R, "0")
    if x == 3:
        return {1:"01",2:"23",3:"01",4:"23"}.get(R, "1")
    if x == 4:
        return {1:"01",2:"23",3:"01",4:"23",5:"01",6:"03"}.get(R, "0")
    if x in (5,7,9):
        if R % 2: return "01" if R <= x else "1"
        return "23" if R <= x + 1 else "1"
    if x in (6,8,10):
        if R % 2: return "01" if R <= x + 1 else "0"
        return "23" if R <= x else "03" if R == x + 2 else "0"
    if x == 11:
        if R % 2: return "01" if R <= 13 else "1"
        return "23" if R <= 12 else "1"
    if x == 12:
        if R % 2: return "01" if R <= 11 else "0"
        return "23" if R <= 12 else "023" if R == 14 else "0"
    if x == 13:
        if R == 13: return "0"
        if R % 2: return "01" if R <= 11 else "1"
        return "23" if R <= 12 else "123" if R <= 26 else "1"
    if x == 14:
        if R == 13: return "0"
        if R == 14: return "123"
        if R % 2: return "01" if R <= 27 else "0"
        return "23" if R <= 12 else "0"
    # x >= 15
    if x == 15:
        if R == 13: return "0"
        if R == 14: return "123"
        if R == 15: return "01"
        if R % 2: return "01" if R <= 11 else "1"
        return "23" if R <= 12 else "02" if R <= 28 else "1"
    # steady rows x >= 16
    if R % 2:
        if R <= 11: return "01"
        if R == 13: return "0"
        if R == 15: return "01"
        if x % 2 == 0:
            if R <= x + 13: return "1"
            return "0"
        if R <= x + 12: return "1"
        return "1"
    if R <= 12: return "23"
    if R == 14: return "123"
    if R == 16: return "02"
    if x % 2 == 0:
        if R <= x + 12: return "0"
        return "0"
    if R <= x + 13: return "0"
    return "1"

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
            a = H_ordered(R,(x,1),12)
            b = H_canonical(R,(x,1),12)
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
            opts.add(single_token(x,13,r))
            opts.add(1 ^ h11_y1(x,r))
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
            R = x+14+off
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
    check("V9_general_tail",bad_tail == 0,{"points":tail_points,"bad":bad_tail,"example":ex_tail,"claim":"R >= x+14 => H=(x+1) mod 2"})
    check("V10_theorem_T_parity_bound",parity_bad == 0,{"points":parity_points,"bad":parity_bad,"example":ex_parity})
    audit["n_points"] += tail_points + parity_points

    # V11: single-token z=13 anchor; V12: K1012 child anchor.
    bad_single = 0; ex_single = None; n = 0
    for x in range(1,81):
        for R in range(0,81):
            n += 1
            a = H_ordered(R,(x,),13); b = single_token(x,13,R)
            if a != b:
                bad_single += 1
                if ex_single is None: ex_single = (x,R,a,b)
    check("V11_single_token_z13_anchor",bad_single == 0,{"points":n,"bad":bad_single,"example":ex_single})
    audit["n_points"] += n

    bad_h11 = 0; ex_h11 = None; n = 0
    for x in range(1,81):
        for R in range(0,x+46):
            n += 1
            a = H_ordered(R,(x,1),11); b = h11_y1(x,R)
            if a != b:
                bad_h11 += 1
                if ex_h11 is None: ex_h11 = (x,R,a,b)
    check("V12_K1012_child_anchor",bad_h11 == 0,{"points":n,"bad":bad_h11,"example":ex_h11})
    audit["n_points"] += n

    # V13: fixed-seed broad scatter.
    rng = random.Random(20261120)
    bad_scatter = 0; ex_scatter = None; n = 20000
    for _ in range(n):
        x = rng.randint(1,1500); R = rng.randint(0,x+100)
        if R == 0:
            am = 0
        else:
            r = R-1; opts = set()
            if x >= 2: opts.add(candidate(x-1,r))
            opts.add(single_token(x,13,r))
            opts.add(1 ^ h11_y1(x,r))
            am = mex(opts)
        got = candidate(x,R)
        if am != got:
            bad_scatter += 1
            if ex_scatter is None: ex_scatter = (x,R,am,got)
    check("V13_fixed_seed_scatter",bad_scatter == 0,{"points":n,"bad":bad_scatter,"example":ex_scatter,"seed":20261120})
    audit["n_points"] += n

    # V14: height-only reduction for R <= 13 (kappa=1, S=x+1 single token).
    bad_ho = 0; ex_ho = None; n = 0
    for x in range(1,501):
        for R in range(0,14):
            n += 1
            a = H_ordered(R,(x,1),12); b = single_token(x+1,12,R)
            if a != b:
                bad_ho += 1
                if ex_ho is None: ex_ho = (x,R,a,b)
    check("V14_height_only_reduction_R_le_13",bad_ho == 0,{"points":n,"bad":bad_ho,"example":ex_ho})
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
    sys.exit(main())
