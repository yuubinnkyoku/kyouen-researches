#!/usr/bin/env python3
"""Independent verifier for the pure-fiber max-value theorem (t in {2,3}).

Audits, each by brute force independent of the closed forms where possible:
  V1  Decomposition: direct canonical-engine G == x ^ H(e,R) over full grids.
  V2  Closed form H = min(L,R) mod 2 (p=0), all states in range.
  V3  Closed form H = (L-n) mod 2 in regime R >= L-1 (p=1), all states in range.
  V4  Max-value theorem: engine max G == predicted max over (q,w,m) grids.
  V5  Witness constructions: for every cap <= 40 (all residues) build the
      periodic-family witness at boundary-tight width and check
      formula G and engine G both equal the predicted max.
  V6  H=3 absence scan for M=3 (sup H == 2 on the scanned box).

Usage: python3 verify_maxvalue.py [--fast]
Prints PASS/FAIL per section and writes audit_maxvalue.json.
"""
import json, sys, itertools
from functools import lru_cache

def mex(opts):
    n = 0
    while n in opts:
        n += 1
    return n

def make_H(M, p):
    @lru_cache(maxsize=None)
    def H(e, R):
        if R == 0:
            return 0
        opts = set()
        for i in range(M):
            if e[i] >= 1:
                child = list(e)
                child[i] -= 1
                if i + 1 < M:
                    child[i + 1] += 1
                    opts.add(H(tuple(child), R - 1))
                else:
                    opts.add(H(tuple(child), R - 1) ^ p)
        if not opts:
            return 0
        return mex(opts)
    return H

def canonical_engine(t, q, w, m):
    cap_max = q - 1
    @lru_cache(None)
    def grundy(state):
        opts = set()
        for i, v in enumerate(state):
            if v < m:
                cl = list(state)
                cl[i] += 1
                child = tuple(sorted(cl, reverse=True))
                if sum(min(x, t) for x in child) <= cap_max:
                    opts.add(grundy(child))
        if len(state) < w and sum(min(x, t) for x in state) + 1 <= cap_max:
            child = tuple(sorted(state + (1,), reverse=True))
            opts.add(grundy(child))
        return mex(opts)
    seen = {()}
    stack = [()]
    while stack:
        state = stack.pop()
        for i, v in enumerate(state):
            if v < m:
                cl = list(state)
                cl[i] += 1
                child = tuple(sorted(cl, reverse=True))
                if sum(min(x, t) for x in child) <= cap_max and child not in seen:
                    seen.add(child); stack.append(child)
        if len(state) < w and sum(min(x, t) for x in state) + 1 <= cap_max:
            child = tuple(sorted(state + (1,), reverse=True))
            if child not in seen:
                seen.add(child); stack.append(child)
    return {s: grundy(s) for s in seen}

def formula_value(t, q, w, m, state, Hcache):
    M = min(t, m)
    p = (m - M) % 2
    H = Hcache[M]
    x = 0
    e = [0] * M
    for c in state:
        if c >= M:
            x ^= (m - c) % 2
        else:
            e[c] += 1
    e[0] += w - len(state)
    R = (q - 1) - sum(min(c, t) for c in state)
    h = H(tuple(e), R) if any(e) or R > 0 else 0
    return x ^ h

def predicted_max(t, q, w, m):
    cap = q - 1
    M = min(t, m)
    p = (m - M) % 2
    if cap == 0:
        return 0
    if p == 0:
        return 1
    if q >= t * w:
        return 1
    return min(3, cap // t + 1)

FAST = "--fast" in sys.argv
audit = {}

_HPOOL = {}
def get_H(M, p):
    if (M, p) not in _HPOOL:
        _HPOOL[(M, p)] = make_H(M, p)
    return _HPOOL[(M, p)]

# ---------------- V1: decomposition ----------------
mism = 0; tot = 0
for t in (2, 3):
    qmax = 8 if FAST else (10 if t == 3 else 11)
    wmax = 4 if FAST else (4 if t == 3 else 5)
    mmax = 5 if FAST else (6 if t == 3 else 6)
    for q in range(2, qmax + 1):
        for w in range(1, wmax + 1):
            for m in range(1, mmax + 1):
                M = min(t, m); p = (m - M) % 2
                H = get_H(M, p)
                eng = canonical_engine(t, q, w, m)
                for s, g in eng.items():
                    tot += 1
                    if g != formula_value(t, q, w, m, s, {M: H}):
                        mism += 1
                        if mism < 5:
                            print("V1 MISMATCH", t, q, w, m, s, g)
audit["V1_decomposition"] = {"states_checked": tot, "mismatches": mism}
print(f"V1 decomposition: states={tot} mismatches={mism}")

# ---------------- V2/V3: closed forms ----------------
badA = 0; chkA = 0
for M in (2, 3):
    H = make_H(M, 0)
    rng = 4 if FAST else 5
    rR = 16 if FAST else 36
    for e in itertools.product(range(0, rng), repeat=M):
        if sum(e) == 0: continue
        L = sum((M - i) * e[i] for i in range(M))
        for R in range(1, rR):
            chkA += 1
            if H(e, R) != min(L, R) % 2:
                badA += 1
                if badA < 5: print("V2 VIOLATION", M, e, R)
audit["V2_p0_closed_form"] = {"checked": chkA, "violations": badA}
print(f"V2 p=0 closed form: checked={chkA} violations={badA}")

badB = 0; chkB = 0
for M in (2, 3, 4):
    H = make_H(M, 1)
    rng = 4 if FAST else 5
    for e in itertools.product(range(0, rng), repeat=M):
        if sum(e) == 0: continue
        L = sum((M - i) * e[i] for i in range(M))
        n = sum(e)
        for R in range(max(1, L - 1), L + (6 if FAST else 10)):
            chkB += 1
            if H(e, R) != (L - n) % 2:
                badB += 1
                if badB < 5: print("V3 VIOLATION", M, e, R)
audit["V3_regime_closed_form"] = {"checked": chkB, "violations": badB}
print(f"V3 p=1 regime closed form: checked={chkB} violations={badB}")

# ---------------- V4: max-value theorem ----------------
bad = 0; chk = 0; fails = []
for t in (2, 3):
    qmax = 8 if FAST else (10 if t == 3 else 11)
    wmax = 4 if FAST else (4 if t == 3 else 5)
    mmax = 5 if FAST else (6 if t == 3 else 6)
    for q in range(2, qmax + 1):
        for w in range(1, wmax + 1):
            for m in range(1, mmax + 1):
                eng = canonical_engine(t, q, w, m)
                mx = max(eng.values())
                pr = predicted_max(t, q, w, m)
                chk += 1
                if mx != pr:
                    bad += 1
                    if len(fails) < 10: fails.append((t, q, w, m, mx, pr))
audit["V4_max_value_grid"] = {"combos": chk, "mismatches": bad, "examples": fails}
print(f"V4 max-value grid: combos={chk} mismatches={bad} {fails[:4]}")

# ---------------- V4b: extended width for small caps ----------------
# The only non-proven piece of the t=3 theorem is exclusion of G=3 via
# (x,H)=(0,3) when cap <= 2t-1; small caps admit large widths, so audit
# the engine directly there.
bad = 0; chk = 0; fails = []
w_hi = 10 if FAST else 16
for t in (2, 3):
    cap_lo = t
    cap_hi = 2 * t - 1
    for cap in range(cap_lo, cap_hi + 1):
        for w in range((cap + 2) // t + 1, w_hi + 1):  # beyond the earlier grid
            for m in ((4, 6) if FAST else (4, 6, 8)) if t == 3 else ((3, 5) if FAST else (3, 5, 7)):
                if (m - min(t, m)) % 2 != 1:
                    continue
                q = cap + 1
                if q >= t * w:
                    continue
                eng = canonical_engine(t, q, w, m)
                mx = max(eng.values())
                pr = predicted_max(t, q, w, m)
                chk += 1
                if mx != pr:
                    bad += 1
                    if len(fails) < 10: fails.append((t, q, w, m, mx, pr))
audit["V4b_small_cap_wide"] = {"combos": chk, "mismatches": bad, "examples": fails}
print(f"V4b small-cap wide-width grid: combos={chk} mismatches={bad} {fails[:4]}")

# ---------------- V5: witness constructions ----------------
def witness_t3(cap, m):
    """t=3, m even >= 4, cap >= 6: returns (position_tuple, w_needed)."""
    assert cap >= 6 and m % 2 == 0 and m >= 4
    r0 = 6 + ((cap - 6) % 6)
    u = (cap - r0) // 6
    seeds = {6: ((1,0,1), 1), 7: ((1,1,0), 3), 8: ((0,2,1), 1),
            9: ((0,1,2), 1), 10: ((1,0,2), 3), 11: ((0,1,3), 1)}
    (e0, e1, e2), R = seeds[r0]
    chains = 2*u + 1
    pos = [3] * chains + [1] * e1 + [2] * e2
    w = chains + e0 + e1 + e2
    return tuple(sorted(pos, reverse=True)), w

def witness_t2(cap, m):
    """t=2, m odd >= 3, cap >= 4: returns (position_tuple, w_needed)."""
    assert cap >= 4 and m % 2 == 1 and m >= 3
    r0 = 4 + ((cap - 4) % 4)
    u = (cap - r0) // 4
    s0 = 2*u + (1 if r0 >= 6 else 0)
    if r0 in (4, 6):
        (e0, e1), R = (1, 1), 1
    else:
        (e0, e1), R = (1, 2), 1
    pos = [2] + [3] * s0 + [1] * e1
    w = 1 + s0 + e0 + e1
    return tuple(sorted(pos, reverse=True)), w

def witness_max2(t, cap):
    """returns (position_tuple, w_needed) for cap in the max=2 range."""
    if t == 3:
        tbl = {3: ((2,), 2), 4: ((2, 1), 2), 5: ((2, 1, 1), 3)}
        return tbl[cap]
    tbl = {2: ((1,), 2), 3: ((1, 1), 3)}
    return tbl[cap]

bad = 0; chk = 0; fails = []
cap_hi = 20 if FAST else 40
for t in (2, 3):
    for cap in range(t, cap_hi + 1):
        pred = min(3, cap // t + 1)
        for m in ((4, 6) if FAST else (4, 6, 8, 10)) if t == 3 else ((3, 5) if FAST else (3, 5, 7)):
            if (m - min(t, m)) % 2 != 1:
                continue  # only p=1 needs witnesses
            if pred <= 1:
                continue
            q = cap + 1
            if pred == 2:
                pos, w = witness_max2(t, cap)
            elif t == 3:
                pos, w = witness_t3(cap, m)
            else:
                pos, w = witness_t2(cap, m)
            # boundary-tight width must suffice
            w_tight = -(-(cap + 2) // t)  # ceil((cap+2)/t)
            if w > w_tight:
                bad += 1
                if len(fails) < 10: fails.append(("width", t, cap, m, w, w_tight))
                continue
            M = min(t, m); p = 1
            H = get_H(M, p)
            g_formula = formula_value(t, q, w, m, pos, {M: H})
            ok = (g_formula == pred)
            g_engine = None
            if cap <= 12 and w <= 5:
                # independent engine cross-check on small instances
                eng = canonical_engine(t, q, w, m)
                g_engine = eng.get(pos)
                ok = ok and (g_engine == pred)
            chk += 1
            if not ok:
                bad += 1
                if len(fails) < 10: fails.append(("value", t, cap, m, pos, g_formula, g_engine, pred))
audit["V5_witnesses"] = {"checked": chk, "failures": bad, "examples": fails}
print(f"V5 witnesses: checked={chk} failures={bad} {fails[:4]}")

# ---------------- V6: H=3 absence for M=3 ----------------
H = make_H(3, 1)
mx = 0; chk = 0
rng = 5 if FAST else 7
rR = 26 if FAST else 46
for e in itertools.product(range(0, rng), repeat=3):
    if sum(e) == 0: continue
    L = sum((3 - i) * e[i] for i in range(3))
    for R in range(1, min(rR, L + 12)):
        chk += 1
        mx = max(mx, H(e, R))
audit["V6_sup_H_M3"] = {"states_checked": chk, "max_H": mx}
print(f"V6 sup H (M=3, e_i<={rng-1}, R<={rR}): {mx} over {chk} states")

audit["fast_mode"] = FAST
ok = (mism == 0 and badA == 0 and badB == 0 and bad == 0 and mx <= 2 and audit["V4b_small_cap_wide"]["mismatches"] == 0)
audit["overall"] = "PASS" if ok else "FAIL"
import os
os.makedirs("output", exist_ok=True)
with open("output/audit.json", "w") as f:
    json.dump(audit, f, indent=1)
print("OVERALL:", audit["overall"])
