#!/usr/bin/env python3
"""Closed-box proof that H <= 2 for the t=3, p=1 residual game on all states
reachable from boards with cap <= 6 (i.e. q <= 7), m even >= 4.

Setting. For t=3, m even >= 4 the decomposition gives G = x xor H with the
residual recursion (M=3, spawn parity kappa=1):
    H(R; e0,e1,e2) = mex of
      { H(R-1; e0-1,e1+1,e2)  if e0>=1, R>=1        (climb 0->1)
        H(R-1; e0,e1-1,e2+1)  if e1>=1, R>=1        (climb 1->2)
        1 xor H(R-1; e0,e1,e2-1) if e2>=1, R>=1     (spawn 2->3) }
    H = 0 when R = 0 or no move is available.
D := R + e1 + 2*e2 is invariant under climbs and drops by 3 on spawn, so
board states with cap <= 6 only ever reach D = cap - 3s <= 6, R <= D <= 6.

Box B = {(R,e0,e1,e2): R,e1,e2 >= 0, e0 <= 9, R+e1+2*e2 <= 6}.
Closure: every move child of a box state is again in B (spawn requires
D >= 1+2 = 3, so D-3 >= 0). Saturation (t3-q7 lane, Lemma 5): e0 >= R
implies H(R,e0,...) = H(R,R,...), so e0 >= 10 > 6 >= R reduces into B.
Hence B + saturation covers every residual state of every board position
with cap <= 6, and a complete fixed-point enumeration of B proves H <= 2.

Checks (audit written to output/box_h2.json):
  B1  Closure of B under the residual recursion (explicit child scan).
  B2  Fixed point + value set: table computed entirely within B by
      increasing R (all children have R-1); explicit mex re-check on every
      state; values subset of {0,1,2}; sup achieved (=2).
  B3  Agreement with the unconstrained memoized recursion on all of B.
  B4  Saturation lemma re-verified empirically for e0 up to 30 on all
      D <= 6 states (paper proof: t3-q7 lane Lemma 5).
  B5  Cross-check against the published 64-row universal residual table E
      of the t3-q7 all-position classification lane (D in {0,3,6}).
  B6  Board-level: t=3, m in {4,6}, q in {4..7}, small w grids; every safe
      position satisfies G = x xor H_box(saturated e0) == engine G, and the
      engine max equals the max-value theorem prediction.

Usage: python3 verify_box_h2.py
"""
import json, itertools
from functools import lru_cache

DMAX = 6
E0MAX = 9


def mex(opts):
    n = 0
    s = set(opts)
    while n in s:
        n += 1
    return n


def children(R, e0, e1, e2):
    """Move children as (state, xor_parity). Empty when R == 0."""
    out = []
    if R >= 1:
        if e0 >= 1:
            out.append(((R - 1, e0 - 1, e1 + 1, e2), 0))
        if e1 >= 1:
            out.append(((R - 1, e0, e1 - 1, e2 + 1), 0))
        if e2 >= 1:
            out.append(((R - 1, e0, e1, e2 - 1), 1))
    return out


def in_box(st):
    R, e0, e1, e2 = st
    return 0 <= e0 <= E0MAX and R >= 0 and e1 >= 0 and e2 >= 0 and R + e1 + 2 * e2 <= DMAX


BOX = [(R, e0, e1, e2)
       for R in range(DMAX + 1)
       for e0 in range(E0MAX + 1)
       for e1 in range(DMAX - R + 1)
       for e2 in range((DMAX - R - e1) // 2 + 1)]

audit = {}

# ---------------- B1: closure ----------------
bad = 0
for st in BOX:
    for ch, _ in children(*st):
        if not in_box(ch):
            bad += 1
            print("B1 CLOSURE VIOLATION", st, "->", ch)
audit["B1_closure"] = {"box_states": len(BOX), "violations": bad}
print(f"B1 closure: box_states={len(BOX)} violations={bad}")

# ---------------- B2: fixed point within B ----------------
table = {}
for R in range(DMAX + 1):
    for st in BOX:
        if st[0] != R:
            continue
        opts = set()
        for ch, par in children(*st):
            opts.add(table[ch] ^ par)
        table[st] = mex(opts) if opts else 0

# explicit mex re-check (independent second pass)
bad = 0
vals = set()
for st in BOX:
    opts = [table[ch] ^ par for ch, par in children(*st)]
    v = mex(opts) if opts else 0
    if v != table[st]:
        bad += 1
        if bad < 5:
            print("B2 FIXED POINT VIOLATION", st, table[st], v)
    vals.add(table[st])
sup = max(table.values())
n2 = sum(1 for v in table.values() if v == 2)
audit["B2_fixed_point"] = {
    "states": len(BOX),
    "violations": bad,
    "value_set": sorted(vals),
    "sup_H": sup,
    "count_H_equal_2": n2,
    "count_H_equal_3": sum(1 for v in table.values() if v == 3),
}
print(f"B2 fixed point: states={len(BOX)} violations={bad} value_set={sorted(vals)} sup_H={sup}")

# ---------------- B3: agreement with unconstrained recursion ----------------
@lru_cache(maxsize=None)
def H_unc(R, e0, e1, e2):
    if R == 0:
        return 0
    opts = set()
    for ch, par in children(R, e0, e1, e2):
        opts.add(H_unc(*ch) ^ par)
    return mex(opts) if opts else 0

bad = 0
for st in BOX:
    if H_unc(*st) != table[st]:
        bad += 1
        if bad < 5:
            print("B3 AGREEMENT VIOLATION", st, H_unc(*st), table[st])
audit["B3_unconstrained_agreement"] = {"states": len(BOX), "violations": bad}
print(f"B3 unconstrained agreement: states={len(BOX)} violations={bad}")

# ---------------- B4: saturation lemma on D<=6, e0<=30 ----------------
bad = 0
chk = 0
for R in range(DMAX + 1):
    for e1 in range(DMAX - R + 1):
        for e2 in range((DMAX - R - e1) // 2 + 1):
            for e0 in range(R, 31):
                chk += 1
                if H_unc(R, e0, e1, e2) != H_unc(R, R, e1, e2):
                    bad += 1
                    if bad < 5:
                        print("B4 SATURATION VIOLATION", (R, e0, e1, e2))
audit["B4_saturation"] = {"checked": chk, "violations": bad}
print(f"B4 saturation (e0 in [R,30], D<=6): checked={chk} violations={bad}")

# ---------------- B5: cross-check vs published t3-q7 E table ----------------
# Rows (R,e0,e1,e2,E) from research/experiments/
#   vertical-fiber-t3-q7-full-classification-20261115/report.md appendix
# (universal residual table for m even >= 4, cap = 6, i.e. D in {0,3,6}).
E_TAB = [
    (0, 0, 0, 0, 0), (0, 0, 0, 3, 0), (0, 0, 1, 1, 0), (0, 0, 2, 2, 0),
    (0, 0, 3, 0, 0), (0, 0, 4, 1, 0), (0, 0, 6, 0, 0),
    (1, 0, 0, 1, 0), (1, 0, 1, 2, 2), (1, 0, 2, 0, 1), (1, 0, 3, 1, 2),
    (1, 0, 5, 0, 1), (1, 1, 0, 1, 2), (1, 1, 1, 2, 2), (1, 1, 2, 0, 1),
    (1, 1, 3, 1, 2), (1, 1, 5, 0, 1),
    (2, 0, 0, 2, 0), (2, 0, 1, 0, 1), (2, 0, 2, 1, 1), (2, 0, 4, 0, 0),
    (2, 1, 0, 2, 0), (2, 1, 1, 0, 0), (2, 1, 2, 1, 1), (2, 1, 4, 0, 0),
    (2, 2, 0, 2, 0), (2, 2, 1, 0, 0), (2, 2, 2, 1, 1), (2, 2, 4, 0, 0),
    (3, 0, 0, 0, 0), (3, 0, 1, 1, 1), (3, 0, 3, 0, 0), (3, 1, 0, 0, 0),
    (3, 1, 1, 1, 2), (3, 1, 3, 0, 2), (3, 2, 0, 0, 1), (3, 2, 1, 1, 2),
    (3, 2, 3, 0, 2), (3, 3, 0, 0, 1), (3, 3, 1, 1, 2), (3, 3, 3, 0, 2),
    (4, 0, 0, 1, 0), (4, 0, 2, 0, 0), (4, 1, 0, 1, 0), (4, 1, 2, 0, 1),
    (4, 2, 0, 1, 1), (4, 2, 2, 0, 0), (4, 3, 0, 1, 1), (4, 3, 2, 0, 0),
    (4, 4, 0, 1, 1), (4, 4, 2, 0, 0),
    (5, 0, 1, 0, 1), (5, 1, 1, 0, 1), (5, 2, 1, 0, 0), (5, 3, 1, 0, 2),
    (5, 4, 1, 0, 2), (5, 5, 1, 0, 2),
    (6, 0, 0, 0, 0), (6, 1, 0, 0, 0), (6, 2, 0, 0, 0), (6, 3, 0, 0, 1),
    (6, 4, 0, 0, 0), (6, 5, 0, 0, 0), (6, 6, 0, 0, 0),
]
bad = 0
for R, e0, e1, e2, E in E_TAB:
    st = (R, e0, e1, e2)
    if not in_box(st):
        bad += 1
        print("B5 ROW OUTSIDE BOX", st)
        continue
    if table[st] != E:
        bad += 1
        if bad < 8:
            print("B5 TABLE MISMATCH", st, "box=", table[st], "published=", E)
# also: for saturated representative rows (e0 == R), lookups with e0x > e0
# must reproduce the same row value (published table's reading rule).
chk2 = 0
for R, e0, e1, e2, E in E_TAB:
    if e0 != R:
        continue  # not a saturated representative; no extension guaranteed
    for e0x in range(e0 + 1, E0MAX + 1):
        chk2 += 1
        if table[(R, e0x, e1, e2)] != E:
            bad += 1
            if bad < 8:
                print("B5 SATURATION MISMATCH", (R, e0x, e1, e2), table[(R, e0x, e1, e2)], E)
audit["B5_published_table_crosscheck"] = {"rows": len(E_TAB), "extra_saturated_lookups": chk2, "mismatches": bad}
print(f"B5 published E-table cross-check: rows={len(E_TAB)} saturated_lookups={chk2} mismatches={bad}")

# ---------------- B6: board-level grids via box table ----------------
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
                    seen.add(child)
                    stack.append(child)
        if len(state) < w and sum(min(x, t) for x in state) + 1 <= cap_max:
            child = tuple(sorted(state + (1,), reverse=True))
            if child not in seen:
                seen.add(child)
                stack.append(child)
    return {s: grundy(s) for s in seen}


def box_value(t, q, w, m, state):
    """Decomposed value using ONLY the box table (+ saturation)."""
    x = 0
    e = [0, 0, 0]
    for c in state:
        if c >= 3:
            x ^= (m - c) % 2
        else:
            e[c] += 1
    e[0] += w - len(state)
    R = (q - 1) - sum(min(c, t) for c in state)
    if R == 0 and not any(e):
        return x
    e0 = min(e[0], R) if e[0] > E0MAX else e[0]
    # universality: D = R + e1 + 2*e2 = cap - 3s <= 6 for cap <= 6
    D = R + e[1] + 2 * e[2]
    assert D <= DMAX, (t, q, w, m, state, D)
    assert e0 <= E0MAX
    return x ^ table[(R, e0, e[1], e[2])]


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


bad = 0
chk = 0
tot = 0
fail_combos = []
for q in (4, 5, 6, 7):
    wmax = 4 if q == 7 else 6
    for w in range(1, wmax + 1):
        for m in (4, 6):
            t = 3
            eng = canonical_engine(t, q, w, m)
            mx = max(eng.values())
            pr = predicted_max(t, q, w, m)
            chk += 1
            if mx != pr:
                bad += 1
                fail_combos.append(("max", q, w, m, mx, pr))
            for s, g in eng.items():
                tot += 1
                if g != box_value(t, q, w, m, s):
                    bad += 1
                    if bad < 8:
                        print("B6 BOARD MISMATCH", q, w, m, s, g, box_value(t, q, w, m, s))
audit["B6_board_grids"] = {"combos": chk, "states": tot, "mismatches": bad, "examples": fail_combos[:6]}
print(f"B6 board grids (t=3, q in 4..7): combos={chk} states={tot} mismatches={bad}")

audit["overall"] = "PASS" if (
    audit["B1_closure"]["violations"] == 0
    and audit["B2_fixed_point"]["violations"] == 0
    and sup <= 2
    and audit["B3_unconstrained_agreement"]["violations"] == 0
    and audit["B4_saturation"]["violations"] == 0
    and audit["B5_published_table_crosscheck"]["mismatches"] == 0
    and audit["B6_board_grids"]["mismatches"] == 0
) else "FAIL"

import os
os.makedirs("output", exist_ok=True)
with open("output/box_h2.json", "w") as f:
    json.dump(audit, f, indent=1)
print("OVERALL:", audit["overall"])
