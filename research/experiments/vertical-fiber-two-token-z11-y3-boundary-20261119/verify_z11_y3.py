#!/usr/bin/env python3
"""Independent two-engine audit of K1014 (z=11, y=3)."""
from __future__ import annotations
import hashlib, json
from functools import lru_cache
from pathlib import Path


def mex(values):
    s = set(values); m = 0
    while m in s: m += 1
    return m


def odd(a, b, r): return a <= r <= b and r % 2 == 1


@lru_cache(None)
def H_ordered(R, X, z):
    if R == 0: return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1: opts.add(H_ordered(R-1, X[:i] + (v-1,) + X[i+1:], z))
        else: opts.add(H_ordered(R-1, X[:i] + X[i+1:], z+1))
    if z: opts.add(1 ^ H_ordered(R-1, X, z-1))
    return mex(opts)


@lru_cache(None)
def H_canonical(R, X, z):
    X = tuple(sorted(X))
    if R == 0: return 0
    opts = set()
    for v in sorted(set(X)):
        i = X.index(v)
        if v > 1:
            opts.add(H_canonical(R-1, tuple(sorted(X[:i] + (v-1,) + X[i+1:])), z))
        else:
            opts.add(H_canonical(R-1, X[:i] + X[i+1:], z+1))
    if z: opts.add(1 ^ H_canonical(R-1, X, z-1))
    return mex(opts)


def formula(x, r):
    if x == 3: T, p = {1,3,5}, False
    elif x == 4: T, p = {1,3,5,7}, r >= 8
    elif x == 5: T, p = {1,3,5,7}, False
    elif x == 6: T, p = {1,3,5,7,9}, r >= 10
    elif x == 7: T, p = {1,3,5,7,9}, False
    elif x == 8: T, p = {1,3,5,7,9,11,13}, r == 12 or r >= 14
    elif x == 9: T, p = {1,3,5,7,9,11}, r in {12,14}
    elif x == 10: T, p = {1,3,5,7,9,11,15}, r in {12,14} or r >= 16
    elif x == 11: T, p = {1,3,5,7,9,11}, r in {12,14}
    elif x == 12: T, p = {1,3,5,7,9,11}, r in {12,14} or r >= 16
    elif x == 13: T, p = {1,3,5,7,9,11}, r in {12,14,16}
    elif x == 14: T, p = {1,3,5,7,9,11,17}, r in {12,14,16} or r >= 18
    elif x == 15: T, p = {1,3,5,7,9,11} | set(range(17,30,2)), r in {12,14,16}
    else:
        T = {1,3,5,7,9,11,17}
        p = (r in {12,14,16} or odd(19, x+13, r) or r >= x+15) if x % 2 == 0 else (r in {12,14,16} or odd(19, x+14, r))
    return 2 if r in T else 1 if p else 0


def qodd(k): return k if k % 2 else k-1

def single(x, z, r):
    if r == 0 or x <= 0: return 0
    if z == 0: return min(r, x) % 2
    if z == x:
        if r % 2 and r <= 2*x-1: return 2
        if r % 2 == 0 and r <= x-1: return 0
        return x % 2
    if 1 <= z <= x-1:
        m = qodd(z)
        if r <= m: return 2 if r % 2 else 0
        if m < r < x+z: return (r+z) % 2
        return x % 2
    if z >= x+1:
        m = qodd(x)
        if r <= m: return 2 if r % 2 else 0
        return x % 2
    raise ValueError((x,z,r))


def sig(x, r):
    alt = {i: ("01" if i%2 else "23") for i in range(1,12)}
    if x == 3: return {1:"01",2:"23",3:"01",4:"23",5:"01",6:"23"}.get(r,"1")
    if x == 4: return {**{i:("01" if i%2 else "23") for i in range(1,8)},8:"03"}.get(r,"0")
    if x == 5: return {**{i:("01" if i%2 else "23") for i in range(1,9)}}.get(r,"1")
    if x == 6: return {**{i:("01" if i%2 else "23") for i in range(1,10)},10:"03"}.get(r,"0")
    if x == 7: return {**{i:("01" if i%2 else "23") for i in range(1,11)},11:"1",12:"13",13:"1",14:"13"}.get(r,"1")
    if x == 8: return {**alt,12:"0",13:"01"}.get(r,"0")
    if x == 9: return {**alt,12:"02",13:"1",14:"02"}.get(r,"1")
    if x == 10: return {**alt,12:"02",13:"1",14:"0",15:"01"}.get(r,"0")
    if x == 11: return {**alt,12:"02",13:"1",14:"0",15:"1",16:"123"}.get(r,"1")
    if x == 12: return {**alt,12:"02",13:"1",14:"0",15:"1"}.get(r,"0")
    if x == 13: return {**alt,12:"02",13:"1",14:"0",15:"1",16:"02"}.get(r,"1")
    if x == 14:
        d = {**alt,12:"02",13:"1",14:"0",15:"1",16:"02",17:"01"}
        if r in d: return d[r]
        if 18 <= r <= 28: return "023" if r%2 == 0 else "0"
        return "0"
    if x == 15:
        d = {**alt,12:"02",13:"1",14:"0",15:"1",16:"02",17:"01",18:"123"}
        if r in d: return d[r]
        if 19 <= r <= 29: return "01" if r%2 else "1"
        return "1"
    if x == 16:
        d = {**alt,12:"02",13:"1",14:"0",15:"1",16:"02",17:"01",18:"123"}
        if r in d: return d[r]
        if 19 <= r <= 31: return "0" if r%2 else "12"
        return "0"
    d = {**alt,12:"02",13:"1",14:"0",15:"1",16:"02",17:"01",18:"123"}
    if r in d: return d[r]
    if 19 <= r <= x+14: return "0" if r%2 else "1"
    return str(x%2)


def main():
    max_x = 300
    grid = signatures = mex_checks = parity = low = tail = extra = 0
    for x in range(3, max_x+1):
        for r in range(0, x+16):
            a = H_ordered(r, (3,x), 11)
            b = H_canonical(r, (3,x), 11)
            f = formula(x,r)
            assert a == b == f, ("grid",x,r,a,b,f)
            grid += 1
            if r <= 12:
                assert a == single(x+3,11,r), ("height-only",x,r)
                low += 1
            if r >= 1:
                opts = []
                if x >= 4: opts.append(H_ordered(r-1,(3,x-1),11))
                opts.append(H_ordered(r-1,(2,x),11))
                opts.append(1 ^ H_ordered(r-1,(3,x),10))
                actual = "".join(map(str, sorted(set(opts))))
                expected = sig(x,r)
                assert actual == expected, ("signature",x,r,actual,expected)
                assert mex(int(c) for c in expected) == f, ("mex",x,r,expected,f)
                signatures += 1; mex_checks += 1
                assert f <= (2 if r%2 else 1), ("Theorem-T",x,r,f)
                parity += 1
            if r >= x+15:
                assert f == (x+3)%2, ("tail",x,r,f)
                tail += 1
        for r in range(0,x+16,3):
            assert H_canonical(r,(3,x),11) == formula(x,r)
            extra += 1
    audit = {
      "theorem":"K1014 z=11 y=3 two-token full Grundy slice",
      "classification":"proved by x-induction and complete A/B/C signature bands",
      "finite_audit_only_supports_transcription_and_independent_recurrence_checks":True,
      "x_range":[3,max_x],"r_range_per_x":"0..x+15 inclusive",
      "checks":{"ordered_vs_canonical_vs_formula":grid,"A_B_C_signature_bands":signatures,
        "signature_mex_vs_closed_form":mex_checks,"Theorem_T_parity":parity,
        "height_only_reduction_R_le_12":low,"general_tail":tail,
        "extra_canonical_spot_checks":extra},
      "mismatches":0,
      "verifier_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      "cache":{"ordered_states":H_ordered.cache_info().currsize,"canonical_states":H_canonical.cache_info().currsize}
    }
    payload = json.dumps(audit,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    out=Path(__file__).parent/"output"/"audit.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(payload,encoding="utf-8")
    print(payload,end=""); print("AUDIT_SHA256="+hashlib.sha256(payload.encode()).hexdigest())

if __name__ == "__main__": main()
