#!/usr/bin/env python3
"""Verifier for the single-unsaturated-fiber residual closed form (kappa=1).

Theorem (claimed, proven in report.md by strong induction on R; machine-checked here):
For x >= 1, z >= 0, R >= 0 with L = x + z + 1, the residual value v = H(R; (x); z) is:

  F(x, z, R) =
    case z == 0:                min(R, x) mod 2
    case x == z >= 1:           2 if R odd and R <= 2x-1;
                                0 if R even and R <= x-1;
                                x mod 2 otherwise
    case 1 <= z <= x-1:         m = oddround(z) = 2*ceil(z/2)-1;
                                2 if R odd and R <= m; 0 if R even and R <= m;
                                (R + z) mod 2 if m < R < L-1; x mod 2 if R >= L-1
    case z >= x+1:              m = oddround(x);
                                2 if R odd and R <= m; 0 if R even and R <= m;
                                x mod 2 if R > m

Checks:
  V0: two independent engines (memoized vs naive game tree) cross-check, R <= 12.
  V1: formula vs memoized engine, x<=60, z<=60, R<=130 (full grid),
      plus focused band 61<=x<=140, z<=80, x-2<=R<=min(130,L+2).
  V2: 200 random spot cells up to x,z<=250, R<=500.
  V3: mex-identity: F satisfies the defining recursion inside box x<=40,z<=40,R<=90
      (this verifies the induction step closes; combined with the written proof it
      pins the universal claim).
  V3b: same mex-identity inside box x<=150,z<=150,R<=320 (pure closed form, no engine).
  V4: token-cap lemma on general multisets: H(R;X;z) = H(R;cap(X,R+1);z).
  V5: structural consistency: even R => v<=1, odd R => v<=2, regime R>=L-1 => v=x mod 2.
Writes audit JSON to stdout.
"""
import sys, json, hashlib, random
from functools import lru_cache

sys.setrecursionlimit(3000000)

def oddround(k):
    return k if k % 2 == 1 else k - 1

def F(x, z, R):
    L = x + z + 1
    if z == 0:
        return min(R, x) % 2
    if x == z:
        if R % 2 == 1 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if z <= x - 1:
        m = oddround(z)
        if R <= m:
            return 2 if R % 2 == 1 else 0
        if R < L - 1:
            return (R + z) % 2
        return x % 2
    # z >= x + 1
    m = oddround(x)
    if R <= m:
        return 2 if R % 2 == 1 else 0
    return x % 2

# ---------- engine 1: memoized ----------
@lru_cache(maxsize=None)
def H(R, X, z):
    cands = set()
    if R >= 1:
        for x in set(X):
            nx = list(X)
            if x >= 2:
                nx.remove(x); nx.append(x - 1); nx.sort()
                cands.add(H(R - 1, tuple(nx), z))
            else:
                nx.remove(1); nx.sort()
                cands.add(H(R - 1, tuple(nx), z + 1))
        if z >= 1:
            cands.add(1 ^ H(R - 1, X, z - 1))
    g = 0
    while g in cands: g += 1
    return g

# ---------- engine 2: naive game tree, no memoization ----------
def Hnaive(R, X, z):
    if R == 0:
        return 0
    cands = set()
    seen = set()
    for i in range(len(X)):
        x = X[i]
        if x in seen: continue
        seen.add(x)
        rest = list(X[:i]) + list(X[i+1:])
        if x >= 2:
            cands.add(Hnaive(R - 1, tuple(sorted(rest + [x - 1], reverse=True)), z))
        else:
            cands.add(Hnaive(R - 1, tuple(sorted(rest, reverse=True)), z + 1))
    if z >= 1:
        cands.add(1 ^ Hnaive(R - 1, X, z - 1))
    g = 0
    while g in cands: g += 1
    return g

def mex(vals):
    g = 0
    s = set(vals)
    while g in s: g += 1
    return g

def main():
    rng = random.Random(20261116)
    out = {"V0": {"checks": 0, "mismatches": 0},
           "V1": {"checks": 0, "mismatches": 0, "first": []},
           "V2": {"checks": 0, "mismatches": 0, "first": []},
           "V3": {"checks": 0, "mismatches": 0, "first": []},
           "V4": {"checks": 0, "mismatches": 0, "first": []},
           "V5": {"checks": 0, "violations": 0}}

    # ---- V0: engine cross-check ----
    for x in range(1, 15):
        for z in range(0, 15):
            for R in range(0, 13):
                out["V0"]["checks"] += 1
                if H(R, (x,), z) != Hnaive(R, (x,), z):
                    out["V0"]["mismatches"] += 1

    # ---- V1: formula vs engine, full grid ----
    for x in range(1, 61):
        for z in range(0, 61):
            L = x + z + 1
            for R in range(0, 131):
                out["V1"]["checks"] += 1
                f = F(x, z, R)
                h = H(R, (x,), z)
                if f != h:
                    out["V1"]["mismatches"] += 1
                    if len(out["V1"]["first"]) < 5:
                        out["V1"]["first"].append([x, z, R, f, h])
    # a few larger x,z with focused R (cap-lemma-backed completeness: x capped at R+1)
    for x in range(61, 141):
        for z in range(0, 80):
            L = x + z + 1
            for R in range(max(0, x - 2), min(131, L + 3)):
                out["V1"]["checks"] += 1
                f = F(x, z, R)
                h = H(R, (x,), z)
                if f != h:
                    out["V1"]["mismatches"] += 1
                    if len(out["V1"]["first"]) < 5:
                        out["V1"]["first"].append([x, z, R, f, h])

    # ---- V2: random spot cells ----
    for _ in range(200):
        x = rng.randint(1, 250)
        z = rng.randint(0, 250)
        R = rng.randint(0, 500)
        out["V2"]["checks"] += 1
        f = F(x, z, R)
        h = H(R, (x,), z)
        if f != h:
            out["V2"]["mismatches"] += 1
            if len(out["V2"]["first"]) < 5:
                out["V2"]["first"].append([x, z, R, f, h])

    # ---- V3: mex-identity inside box ----
    for x in range(0, 41):
        for z in range(0, 41):
            for R in range(1, 91):
                out["V3"]["checks"] += 1
                if x == 0:
                    opts = []
                    if z >= 1:
                        opts.append(1 ^ F(0, z - 1, R - 1))
                    pred = mex(opts)
                elif x == 1:
                    opts = [F(0, z + 1, R - 1)]
                    if z >= 1:
                        opts.append(1 ^ F(1, z - 1, R - 1))
                    pred = mex(opts)
                else:
                    opts = [F(x - 1, z, R - 1)]
                    if z >= 1:
                        opts.append(1 ^ F(x, z - 1, R - 1))
                    pred = mex(opts)
                if pred != F(x, z, R):
                    out["V3"]["mismatches"] += 1
                    if len(out["V3"]["first"]) < 5:
                        out["V3"]["first"].append([x, z, R, pred, F(x, z, R)])

    # ---- V3b: wide-box mex-identity (pure closed form) ----
    def mex_pred(x, z, R):
        # options mirror the engine exactly:
        #  A (x>=2): (x-1, z, R-1); B (x==1): (empty, z+1, R-1) [value 0];
        #  C (z>=1): 1 ^ (x, z-1, R-1)
        if x == 0:
            opts = []
            if z >= 1:
                opts.append(1 ^ F(0, z - 1, R - 1))
            return mex(opts)
        if x == 1:
            opts = [F(0, z + 1, R - 1)]
            if z >= 1:
                opts.append(1 ^ F(1, z - 1, R - 1))
            return mex(opts)
        opts = [F(x - 1, z, R - 1)]
        if z >= 1:
            opts.append(1 ^ F(x, z - 1, R - 1))
        return mex(opts)
    out["V3b"] = {"checks": 0, "mismatches": 0, "first": []}
    for x in range(0, 151):
        for z in range(0, 151):
            for R in range(1, 321):
                out["V3b"]["checks"] += 1
                pred = mex_pred(x, z, R)
                if pred != F(x, z, R):
                    out["V3b"]["mismatches"] += 1
                    if len(out["V3b"]["first"]) < 5:
                        out["V3b"]["first"].append([x, z, R, pred, F(x, z, R)])

    # ---- V4: token-cap lemma on general multisets ----
    def capms(X, c):
        return tuple(sorted((min(v, c) for v in X), reverse=True))
    def gen_multisets(maxpart, maxsize):
        results = {()}
        frontier = [()]
        while frontier:
            nf = []
            for ms in frontier:
                lo = ms[-1] if ms else maxpart
                if len(ms) < maxsize:
                    for p in range(1, lo + 1):
                        nm = tuple(sorted(ms + (p,), reverse=True))
                        if nm not in results:
                            results.add(nm); nf.append(nm)
            frontier = nf
        return sorted(results)
    for X in gen_multisets(8, 4):
        for z in range(0, 7):
            for R in range(0, 15):
                out["V4"]["checks"] += 1
                if H(R, X, z) != H(R, capms(X, R + 1), z):
                    out["V4"]["mismatches"] += 1
                    if len(out["V4"]["first"]) < 5:
                        out["V4"]["first"].append([list(X), z, R])

    # ---- V5: structural consistency of the formula itself ----
    for x in range(1, 61):
        for z in range(0, 61):
            L = x + z + 1
            for R in range(0, 131):
                out["V5"]["checks"] += 1
                f = F(x, z, R)
                if R % 2 == 0 and f > 1: out["V5"]["violations"] += 1
                if R % 2 == 1 and f > 2: out["V5"]["violations"] += 1
                if R >= L - 1 and f != x % 2: out["V5"]["violations"] += 1
                if R == 0 and f != 0: out["V5"]["violations"] += 1

    print(json.dumps(out, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__":
    main()
