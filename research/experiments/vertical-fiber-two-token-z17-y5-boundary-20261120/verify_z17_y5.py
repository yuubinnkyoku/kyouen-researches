#!/usr/bin/env python3
"""Independent finite audit for the z=17, y=5 two-token slice.

Universal proof: x-outer induction with the multiset-merger base at x=5
plus the complete disjoint A/B/C signature bands for all 1<=R<=x+22 in
report.md, and the K0832 general tail for R>=x+23.

Checks:
- two independent raw recursion engines (order-preserving and
  descending-canonical) against the parent closed form
- child anchors: K1076 (z=17,y=4) and K1074 (z=16,y=5) transcriptions
  vs fresh raw recursion of the child positions
- complete parity signature band table (static rows x=5..24, sweep row
  x=23, exception row x=24, generic rows x>=25): disjoint coverage of
  1<=R<=x+22, band identity vs mechanically computed child signatures, mex
- the induction step mex{A,B,C} itself (closure base + closure sweep)
- set-based and predicate closed-form transcriptions of the parent
- height-only single-token reduction (K0832 proven R<=18; finite
  observation to R<=22 with the sharpness witness x=12, R=23)
- general tail R>=x+23 -> (x+5) mod 2, deep affine band endpoints and
  signature samples to x<=200000, fixed-seed scatter with raw engines.
"""
from __future__ import annotations
import hashlib, json, random, sys
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(100000)
import os
SMOKE = bool(os.environ.get('SMOKE'))
if SMOKE:
    LIM_PARENT, LIM_ANCHOR, LIM_PRED = 16, 24, 40
    LIM_BAND, LIM_SWEEP, LIM_TAILH = 32, 300, 16
    DEEP_MAX, DEEP_STEP = 4000, 71
    N_SCATTER = 3000
else:
    LIM_PARENT, LIM_ANCHOR, LIM_PRED = 61, 76, 301
    LIM_BAND, LIM_SWEEP, LIM_TAILH = 96, 5001, 96
    DEEP_MAX, DEEP_STEP = 200001, 71
    N_SCATTER = 8000

def mex(values):
    m = 0; values = set(values)
    while m in values: m += 1
    return m

@lru_cache(None)
def H_ordered(R, X, z):
    if R == 0: return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i+1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i+1:], z + 1))
    if z: opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)

@lru_cache(None)
def H_canonical(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0: return 0
    opts = set(); i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            Y = tuple(sorted(X[:i] + (v - 1,) + X[i+1:], reverse=True))
            opts.add(H_canonical(R - 1, Y, z))
        else:
            Y = tuple(sorted(X[:i] + X[i+1:], reverse=True))
            opts.add(H_canonical(R - 1, Y, z + 1))
        while i + 1 < len(X) and X[i+1] == v: i += 1
        i += 1
    if z: opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)

@lru_cache(None)
def single(x, z, r):
    if r == 0 or (x == 0 and z == 0): return 0
    opts = set()
    if x > 1: opts.add(single(x - 1, z, r - 1))
    elif x == 1: opts.add(single(0, z + 1, r - 1))
    if z: opts.add(1 ^ single(x, z - 1, r - 1))
    return mex(opts)

def odd(r, a, b): return r % 2 == 1 and a <= r <= b

# ---------- published K1076 child transcription (z=17, y=4; B child) ----------
def g17y4_T(x, r):
    if x == 4: return odd(r, 1, 7)
    if x in (5, 6): return odd(r, 1, 9)
    if x in (7, 8): return odd(r, 1, 11)
    if x in (9, 10): return odd(r, 1, 13)
    if x in (11, 12): return odd(r, 1, 15)
    if x == 13: return odd(r, 1, 21)
    if x in (14, 15, 16, 17, 18, 19, 20): return odd(r, 1, 17) or (x == 17 and r == 23)
    if x == 21: return odd(r, 1, 17) or r == 25
    if x == 22: return odd(r, 1, 17) or odd(r, 25, 43)
    if x >= 23: return odd(r, 1, 17) or r == 25
    return False

def g17y4_P(x, r):
    if x == 5: return r >= 10
    if x == 7: return r >= 12
    if x == 9: return r >= 14
    if x == 11: return r >= 16
    if x == 13: return r in (18, 20, 22) or r >= 23
    if x == 14: return r in (18, 20)
    if x == 15: return r in (18, 20, 22) or r >= 23
    if x == 16: return r in (18, 20, 22)
    if x == 17: return r in (18, 20, 22, 24) or r >= 25
    if x == 18: return r in (18, 20, 22)
    if x == 19: return r in (18, 20, 22, 24) or r >= 25
    if x == 20: return r in (18, 20, 22, 24)
    if x == 21: return r in (18, 20, 22, 24) or r >= 26
    if x == 22: return r in (18, 20, 22, 24)
    if x >= 23:
        base = r in (18, 20, 22, 24)
        if x & 1: return base or odd(r, 27, x + 20) or r >= x + 22
        return base or odd(r, 27, x + 21)
    return False

def g17y4(x, r):
    if r == 0: return 0
    if g17y4_T(x, r): return 2
    if g17y4_P(x, r): return 1
    return 0

# ---------- published K1074 child transcription (z=16, y=5; C child) ----------
BASE5C = {17, 19, 21, 23, 25}
def g16y5(x, r):
    if r == 0: return 0
    if x == 5: t = (r % 2 == 1 and r <= 9)
    elif x in (6, 7): t = (r % 2 == 1 and r <= 11)
    elif x in (8, 9): t = (r % 2 == 1 and r <= 13)
    elif x == 10: t = (r % 2 == 1 and r <= 15)
    elif x == 11: t = (r % 2 == 1 and r <= 21)
    elif x == 15: t = (r % 2 == 1 and r <= 15) or r == 23
    elif x == 19: t = (r % 2 == 1 and r <= 15) or r == 25
    elif x == 22: t = (r % 2 == 1 and r <= 15) or (r % 2 == 1 and 27 <= r <= 43)
    elif x >= 23: t = (r % 2 == 1 and r <= 15) or r == 27
    else: t = (r % 2 == 1 and r <= 15)
    if t: return 2
    if x in (5, 7, 9, 11): return 0
    if x == 6: return 1 if r >= 12 else 0
    if x == 8: return 1 if r >= 14 else 0
    if x == 10: return 1 if r >= 16 else 0
    if x == 12: return 1 if (r in (17, 19, 21) or r >= 22) else 0
    if x in (13, 15): return 1 if r in (17, 19, 21) else 0
    if x == 19: return 1 if r in (17, 19, 21, 23) else 0
    if x in (14, 16): return 1 if (r in (17, 19, 21, 23) or r >= 24) else 0
    if x == 17: return 1 if r in (17, 19, 21, 23) else 0
    if x in (18, 20): return 1 if (r in BASE5C or r >= 26) else 0
    if x == 21: return 1 if r in BASE5C else 0
    if x % 2: return 1 if (r in BASE5C or (r % 2 == 0 and 28 <= r <= x + 21)) else 0
    return 1 if (r in BASE5C or (r % 2 == 0 and 28 <= r <= x + 22) or r >= x + 23) else 0

# ---------- parent closed form (z=17, y=5): set-based ----------
def O(a, b): return set(range(a + (a % 2 == 0), b + 1, 2))
def E(a, b): return set(range(a + (a % 2 == 1), b + 1, 2))
def I(a): return set(range(a, 20000))

BASEP = {18, 20, 22, 24, 26}
def Tset(x):
    if x == 5: return O(1, 9)
    if x in (6, 7): return O(1, 11)
    if x in (8, 9): return O(1, 13)
    if x in (10, 11): return O(1, 15)
    if x == 12: return O(1, 21)          # x+y=z row, d+z=24==0 mod 4, top 21
    if x == 14: return O(1, 17) | {23}   # advance point, d+z=26==2 mod 4
    if x == 18: return O(1, 17) | {25}   # advance point, d+z=30==2 mod 4
    if x == 22: return O(1, 17) | {27}   # pin row x=z+y, pin 27=2y+z
    if x == 23: return O(1, 17) | O(27, 45)  # sweep row x=z+y+1
    if x >= 24: return O(1, 17) | {27}
    return O(1, 17)

def Pset(x):
    if x in (5, 7, 9, 11): return set()
    if x == 6: return I(12)
    if x == 8: return I(14)
    if x == 10: return I(16)
    if x == 12: return {18, 20, 22} | I(23)
    if x in (13, 15): return {18, 20, 22}
    if x in (14, 16): return {18, 20, 22} | I(24)
    if x in (17, 19): return {18, 20, 22, 24}
    if x in (18, 20): return {18, 20, 22, 24} | I(26)
    if x == 21: return set(BASEP)
    if x == 22: return set(BASEP) | I(28)
    if x == 23: return set(BASEP)
    if x % 2: return set(BASEP) | O(29, x + 22)
    return set(BASEP) | O(29, x + 23) | I(x + 24)

def cand(x, r):
    if r == 0: return 0
    if r in Tset(x): return 2
    return 1 if r in Pset(x) else 0

# ---------- parent closed form: O(1) predicates ----------
def z17y5_T(x, r):
    if x == 5: return r % 2 == 1 and r <= 9
    if x in (6, 7): return r % 2 == 1 and r <= 11
    if x in (8, 9): return r % 2 == 1 and r <= 13
    if x in (10, 11): return r % 2 == 1 and r <= 15
    if x == 12: return r % 2 == 1 and r <= 21
    if x == 14: return (r % 2 == 1 and r <= 17) or r == 23
    if x == 18: return (r % 2 == 1 and r <= 17) or r == 25
    if x == 22: return (r % 2 == 1 and r <= 17) or r == 27
    if x == 23: return (r % 2 == 1 and r <= 17) or (r % 2 == 1 and 27 <= r <= 45)
    if x >= 24: return (r % 2 == 1 and r <= 17) or r == 27
    return r % 2 == 1 and r <= 17

def z17y5_P(x, r):
    if x in (5, 7, 9, 11): return False
    if x == 6: return r >= 12
    if x == 8: return r >= 14
    if x == 10: return r >= 16
    if x == 12: return r in (18, 20, 22) or r >= 23
    if x in (13, 15): return r in (18, 20, 22)
    if x in (14, 16): return r in (18, 20, 22) or r >= 24
    if x in (17, 19): return r in (18, 20, 22, 24)
    if x in (18, 20): return r in (18, 20, 22, 24) or r >= 26
    if x == 21: return r in BASEP
    if x == 22: return r in BASEP or r >= 28
    if x == 23: return r in BASEP
    if x % 2: return r in BASEP or (r % 2 == 1 and 29 <= r <= x + 22)
    return r in BASEP or (r % 2 == 1 and 29 <= r <= x + 23) or r >= x + 24

def z17y5(x, r):
    if r == 0: return 0
    if r >= x + 23: return (x + 5) % 2
    if z17y5_T(x, r): return 2
    if z17y5_P(x, r): return 1
    return 0

# ---------- signature bands ----------
# STATIC rows x=5..24 were generated mechanically from the two raw engines
# and the published child closed forms (no hand transcription of endpoints).
STATIC = {
5: (((1,9,'01'), (11,27,'1')), [(2,10,'23'), (12,26,'1')]),
6: (((1,11,'01'), (13,27,'0')), [(2,10,'23'), (12,12,'03'), (14,28,'0')]),
7: (((1,11,'01'), (13,29,'1')), [(2,12,'23'), (14,28,'1')]),
8: (((1,13,'01'), (15,29,'0')), [(2,12,'23'), (14,14,'03'), (16,30,'0')]),
9: (((1,13,'01'), (15,31,'1')), [(2,14,'23'), (16,30,'1')]),
10: (((1,15,'01'), (17,31,'0')), [(2,14,'23'), (16,16,'03'), (18,32,'0')]),
11: (((1,15,'01'), (17,33,'1')), [(2,16,'23'), (18,22,'13'), (24,32,'1')]),
12: (((1,21,'01'), (23,33,'0')), [(2,16,'23'), (18,34,'0')]),
13: (((1,17,'01'), (19,35,'1')), [(2,16,'23'), (18,22,'02'), (24,34,'1')]),
14: (((1,17,'01'), (19,21,'1'), (23,23,'01'), (25,35,'0')), [(2,16,'23'), (18,18,'02'), (20,36,'0')]),
15: (((1,17,'01'), (19,37,'1')), [(2,16,'23'), (18,18,'02'), (20,22,'0'), (24,24,'123'), (26,36,'1')]),
16: (((1,17,'01'), (19,23,'1'), (25,37,'0')), [(2,16,'23'), (18,18,'02'), (20,38,'0')]),
17: (((1,17,'01'), (19,39,'1')), [(2,16,'23'), (18,18,'02'), (20,22,'0'), (24,24,'02'), (26,38,'1')]),
18: (((1,17,'01'), (19,23,'1'), (25,25,'01'), (27,39,'0')), [(2,16,'23'), (18,18,'02'), (20,40,'0')]),
19: (((1,17,'01'), (19,41,'1')), [(2,16,'23'), (18,18,'02'), (20,24,'0'), (26,26,'123'), (28,40,'1')]),
20: (((1,17,'01'), (19,25,'1'), (27,41,'0')), [(2,16,'23'), (18,18,'02'), (20,42,'0')]),
21: (((1,17,'01'), (19,43,'1')), [(2,16,'23'), (18,18,'02'), (20,24,'0'), (26,26,'02'), (28,42,'1')]),
22: (((1,17,'01'), (19,25,'1'), (27,27,'01'), (29,43,'0')), [(2,16,'23'), (18,18,'02'), (20,24,'0'), (26,26,'02'), (28,44,'023')]),
23: (((1,17,'01'), (19,25,'1'), (27,45,'01')), [(2,16,'23'), (18,18,'02'), (20,24,'0'), (26,26,'02'), (28,28,'123'), (30,44,'1')]),
24: (((1,17,'01'), (19,25,'1'), (27,27,'01'), (29,45,'0')), [(2,16,'23'), (18,18,'02'), (20,24,'0'), (26,26,'02'), (28,28,'123'), (30,46,'12')]),
}

def row_bands(x, par):
    """odd-parity (par=1) / even-parity (par=0) band list for row x>=5."""
    if x <= 24:
        return STATIC[x][0] if par else STATIC[x][1]
    if par == 1:
        up = x + 22 if x % 2 else x + 21
        return [(1,17,'01'), (19,25,'1'), (27,27,'01'), (29, up, '0')]
    up = x + 21 if x % 2 else x + 22
    return [(2,16,'23'), (18,18,'02'), (20,24,'0'), (26,26,'02'),
            (28,28,'123'), (30, up, '1')]

def expected_sig(x, r):
    for lo, hi, s in row_bands(x, 1 if r % 2 else 0):
        if lo <= r <= hi and (r - lo) % 2 == 0: return s
    return None

MEX = {'01': 2, '23': 0, '03': 1, '0': 1, '1': 0, '12': 0, '13': 0,
       '02': 1, '023': 1, '123': 0}

def sig_of(vals):
    return ''.join(str(v) for v in sorted(set(vals)))

def signature(x, r):
    """child signature of (x,5);17 at budget r>=1, from closed forms."""
    rr = r - 1
    if x == 5:
        b = g17y4(5, rr)          # A==B: multiset merge at the d=0 column edge
        return sig_of((b, 1 ^ g16y5(5, rr)))
    a = z17y5(x - 1, rr)
    b = g17y4(x, rr)
    c = 1 ^ g16y5(x, rr)
    return sig_of((a, b, c))

def signature_raw(x, r):
    rr = r - 1
    if x == 5:
        b = H_ordered(rr, (5, 4), 17)
        return sig_of((b, 1 ^ H_ordered(rr, (5, 5), 16)))
    a = H_ordered(rr, (x - 1, 5), 17)
    b = H_ordered(rr, (x, 4), 17)
    c = 1 ^ H_ordered(rr, (x, 5), 16)
    return sig_of((a, b, c))

# ============ audit ============
def run():
    c = {'parent_ordered_vs_formula': 0, 'parent_canonical_vs_formula': 0,
         'ordered_vs_canonical': 0,
         'child_anchor_K1076': 0, 'child_anchor_K1074': 0,
         'set_vs_predicate': 0,
         'band_coverage_rows': 0, 'band_identity_raw': 0,
         'band_identity_formula': 0, 'band_mex': 0,
         'closure_base': 0, 'closure_sweep': 0,
         'tail_raw': 0,
         'height_only_proven_R_le_18': 0, 'height_only_observed_R19_22': 0,
         'height_only_witness': 0,
         'deep_affine_formula': 0, 'band_endpoints_up_to_200k': 0,
         'scatter': 0}

    # 1) parent: two raw engines vs the closed form, finite box
    for x in range(5, LIM_PARENT):
        for r in range(0, x + 47):
            f = z17y5(x, r)
            a = H_ordered(r, (x, 5), 17)
            b = H_canonical(r, (x, 5), 17)
            assert a == f and b == f and a == b, ("parent", x, r, a, b, f)
            c['parent_ordered_vs_formula'] += 1
            c['parent_canonical_vs_formula'] += 1
            c['ordered_vs_canonical'] += 1

    # 2) child anchor transcriptions vs fresh raw recursion
    for x in range(4, LIM_ANCHOR):
        for r in range(0, x + 36):
            v = g17y4(x, r)
            assert H_ordered(r, (x, 4), 17) == v, ("K1076", x, r)
            assert H_canonical(r, (x, 4), 17) == v, ("K1076c", x, r)
            c['child_anchor_K1076'] += 2
    for x in range(5, LIM_ANCHOR):
        for r in range(0, x + 36):
            v = g16y5(x, r)
            assert H_ordered(r, (x, 5), 16) == v, ("K1074", x, r)
            assert H_canonical(r, (x, 5), 16) == v, ("K1074c", x, r)
            c['child_anchor_K1074'] += 2

    # 3) set-based vs predicate transcription of the parent
    for x in range(5, LIM_PRED):
        for r in range(0, x + 47):
            assert cand(x, r) == z17y5(x, r), ("pred", x, r)
            c['set_vs_predicate'] += 1

    # 4) band table: structural disjoint coverage of 1..x+22 per parity
    for x in range(5, LIM_BAND):
        for par in (1, 0):
            bands = row_bands(x, par)
            assert bands[0][0] == (1 if par else 2), ("first", x, par)
            prev = None
            for lo, hi, s in bands:
                assert lo % 2 == par and hi % 2 == par and lo <= hi, ("shape", x, par)
                assert s in MEX, ("sig", s)
                if prev is not None:
                    assert lo == prev + 2, ("gap", x, par, prev, lo)
                prev = hi
            top = x + 22
            want = top if (top % 2 == par) else top - 1
            assert prev == want, ("top", x, par, prev, want)
            c['band_coverage_rows'] += 1
        # band signature: raw engines vs formula-driven children, all R<=x+22
        for r in range(1, x + 23):
            s = expected_sig(x, r)
            assert s is not None, ("coverage", x, r)
            assert signature_raw(x, r) == s, ("band raw", x, r)
            assert signature(x, r) == s, ("band formula", x, r)
            v = MEX[s]
            assert v == z17y5(x, r), ("band mex", x, r, s, v, z17y5(x, r))
            if r % 2 == 0: assert v <= 1, ("even T", x, r)
            c['band_identity_raw'] += 1
            c['band_identity_formula'] += 1
            c['band_mex'] += 1

    # 5) closure: the induction step itself on the parameterized forms
    for r in range(1, 31):
        b = g17y4(5, r - 1)
        assert z17y5(5, r) == mex((b, b, 1 ^ g16y5(5, r - 1))), ("base", r)
        c['closure_base'] += 1
    for x in range(6, LIM_SWEEP):
        for r in range(1, x + 23):
            a = z17y5(x - 1, r - 1)
            b = g17y4(x, r - 1)
            cc = 1 ^ g16y5(x, r - 1)
            assert z17y5(x, r) == mex((a, b, cc)), ("closure", x, r)
            c['closure_sweep'] += 1

    # 6) tail: raw engines match the claim
    for x in range(5, LIM_TAILH):
        for r in range(x + 23, x + 68):
            v = (x + 5) % 2
            assert H_ordered(r, (x, 5), 17) == v, ("tail", x, r)
            assert H_canonical(r, (x, 5), 17) == v, ("tailc", x, r)
            assert z17y5(x, r) == v, ("tailf", x, r)
            c['tail_raw'] += 1

    # 7) height-only reduction: proven to R<=18 (K0832), observed to R<=22
    for x in range(5, LIM_TAILH):
        for r in range(0, 19):
            assert z17y5(x, r) == single(x + 5, 17, r), ("ho", x, r)
            c['height_only_proven_R_le_18'] += 1
        for r in range(19, 23):
            assert z17y5(x, r) == single(x + 5, 17, r), ("hoo", x, r)
            c['height_only_observed_R19_22'] += 1
    # sharpness witness of the uniform observation: first failure x=12, R=23
    assert z17y5(12, 23) == 1 and single(17, 17, 23) == 2
    c['height_only_witness'] = 1

    # 8) deep affine structure: pin, base, band edges, tail for x<=200000
    for x in range(25, DEEP_MAX):
        for r in (15, 16, 17, 18, 26, 27, 28, 29):
            f = z17y5(x, r)
            w = {15: 2, 16: 0, 17: 2, 18: 1, 26: 1, 27: 2, 28: 0, 29: 1}[r]
            assert f == w, ("deep", x, r, f, w)
            c['deep_affine_formula'] += 1
        for r in (x + 20, x + 21, x + 22, x + 23, x + 24, x + 30):
            v = z17y5(x, r)
            if r >= x + 23:
                assert v == (x + 5) % 2, ("deep tail", x, r, v)
            else:
                s = expected_sig(x, r)
                assert s is not None and v == MEX[s], ("deep band", x, r, v, s)
            c['deep_affine_formula'] += 1
        # band edge preceding the tail: odd x tops at P (value 1), even x at 0
        if x % 2:
            assert z17y5(x, x + 22) == 1, ("do", x)
            assert z17y5(x, x + 21) == 0, ("do0", x)
            assert z17y5(x, x + 20) == 1, ("do1", x)
        else:
            assert z17y5(x, x + 22) == 0, ("de2", x)
            assert z17y5(x, x + 21) == 1, ("de1", x)
            assert z17y5(x, x + 20) == 0, ("de0", x)
        assert z17y5(x, x + 23) == (x + 5) % 2, ("tail entry", x)
        c['deep_affine_formula'] += 4

    # 9) band endpoints and signature samples deep: x up to 200000, step 71
    for x in range(25, DEEP_MAX, DEEP_STEP):
        for par in (1, 0):
            bands = row_bands(x, par)
            n = len(bands)
            for k, (lo, hi, s) in enumerate(bands):
                for r in {lo, hi, lo + (hi - lo) // 4 * 2, lo + (hi - lo) // 2, lo + (hi - lo) // 4 * 3}:
                    if lo <= r <= hi and (r - lo) % 2 == 0:
                        assert signature(x, r) == s, ("dbs", x, par, r, s)
                        c['band_endpoints_up_to_200k'] += 1
            assert bands[-1][2] == ('0' if par else '1'), ("lastband", x, par)

    # 10) fixed-seed scatter with both raw engines
    rng = random.Random(20261126)
    for _ in range(N_SCATTER):
        x = rng.randint(5, 90)
        r = rng.randint(0, x + 55)
        a = H_ordered(r, (x, 5), 17)
        b = H_canonical(r, (x, 5), 17)
        f = z17y5(x, r)
        assert a == b == f, ("scatter", x, r)
        c['scatter'] += 1

    return c

if __name__ == '__main__':
    counts = run()
    counts['total_comparisons'] = sum(counts.values())
    counts['claim'] = 'H(R;(x,5);17), all x>=5 and R>=0'
    counts['proof_status'] = 'proved_by_x_outer_induction_and_complete_signature_bands'
    counts['finite_audit_scope'] = {
        'parent_direct': '5<=x<=60, 0<=R<=x+46',
        'K1076_B_anchor': '4<=x<=75, 0<=R<=x+35',
        'K1074_C_anchor': '5<=x<=75, 0<=R<=x+35',
        'set_vs_predicate': '5<=x<=300, 0<=R<=x+46',
        'signature_bands': '5<=x<=95, all 1<=R<=x+22',
        'closure_sweep': '6<=x<=5000, 1<=R<=x+22',
        'tail_direct': '5<=x<=95, x+23<=R<=x+67',
        'height_only': 'proven R<=18; observed R<=22 (witness x=12,R=23)',
        'deep_affine': '25<=x<=200000, pin/base/band-edge/tail points',
        'band_endpoints': 'x in 25..200000 step 71',
        'scatter_seed': 20261126,
    }
    counts['ordered_states'] = H_ordered.cache_info().currsize
    counts['canonical_states'] = H_canonical.cache_info().currsize
    counts['single_token_states'] = single.cache_info().currsize
    counts['verifier_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    counts['mode'] = 'smoke' if SMOKE else 'full'
    out = Path(__file__).resolve().parent / 'output' / 'audit.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(counts, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    out.write_text(payload, encoding='utf-8')
    print(payload, end='')
