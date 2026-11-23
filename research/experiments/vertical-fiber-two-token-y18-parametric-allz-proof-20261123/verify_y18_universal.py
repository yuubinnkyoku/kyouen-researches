#!/usr/bin/env python3
"""
Universal verifier for the y=18 two-token residual family (PART 1).

Family: H(R; (x,18); z), all z >= 0, all x >= 18, all R >= 0.
Claim under test (K1242, currently status "observed"); the closed form
cand18 equals H everywhere; with corollaries
  merge-below-diagonal (y=18 promotion of the y=12..17 lines):
       x <= z-19  =>  H == single_token(x+18, z, R)
  tail:                                 R >= x+z+19  =>  H == (x+18) % 2

STAGE: part 1 (the 12-check machine; the part 2 stage adds C1d published
fixed-z slice anchors at the y=18 rows and the independent census_rows.py
census.txt consumer C11r and, on overall PASS with 3 byte-identical audit
runs, promotes K1242 observed -> proved), per the procedure that proved
y=5..y=17 (K1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138/K1141/
K1143/K1152/K1231/K1233/K1235/K1237/K1240).

Checks implemented and run here: C1, C1b, C2, C2b, C3, C4 (clip window
2y+2 = 38, sentinel 39), C4t (clip tightness probe 37), C7, C8, C9, C11,
C12. part2 will add C1d and C11r in place with these bodies byte-invariant.

Run modes:
  python3 verify_y18_universal.py                 # all checks except C11
  python3 verify_y18_universal.py C11ordered      # census part 1 (slow)
  python3 verify_y18_universal.py C11canonical    # census part 2 (slow)
  python3 verify_y18_universal.py C11             # merge census parts, then
                                                  # run all checks incl. C11
  python3 verify_y18_universal.py C1 C2 ...      # explicit check list

  C1   raw order-preserving AND descending-canonical engines vs cand18,
       z=0..14, x=18..36, R=0..x+z+49
  C1b  single-token closed form (K0832) raw anchor; published y=17 closed
       form (K1240 transcription, the B-child of every y=18 point and the
       x=18 A-child) raw anchor; x=18 multiset merger (17,18)==(18,17)
       i.e. A==B child value raw anchor
  C2   closed-form identity grid z=0..48, x=18..60, R<=x+z+44 (+merge,tail)
  C2b  deep-tail identity rows z in {60,72,84,96,108,120,240,400},
       x in {18,23,...,68}, R <= x+z+31
  C3   option-decomposition raw anchor (child sets vs raw recursion)
  C4   type machine, clip window 2y+2 = 38 sentinel 39, free-coordinate
       box v0=x-z, v1=R-x, v3=R-x-z in +/-60: full sweep, per-type
       confluence of the (value, sorted-children) effect
  C4t  tightness probe: the same box at clip 37 (2y+1) counts confluence
       violations (informational, not part of the bad total) -- tests
       the 14-family continuation candidate of the tight 2y+2 clip
       pattern (y=5..17: 12/14/16/18/20/22/24/26/28/30/32/34/36; 2y+2 for
       y=18 is 38)
  C7   fixed-seed far probes (seed 20261182): 200k points, z,x <= 3000,
       R <= 9000, tail window around x+z+19
  C8   boundary manifolds z in {0..5, 29..31, 59..61, 299..301,
       999..1001, 2999, 3000}, dx in [-30, 19], tail window
       [x+z+19, x+z+21]. x=17 rows enter the identity as closed-form
       extension-consistency rows only (no raw claim below x=18),
       exactly as the x=16 rows did in the published y=17 machine;
       the deep-tail window check uses the published cand17 (K1240,
       proved) tail claim R>=x+z+18 => (x+17)%2 at x>=17
  C9   v-space shell sweeps at radii [61,64], [89,92], [117,120]
  C11  raw census anchor z=0..79, x=18..70, R<=x+z+19, both engines,
       plus merge/tail corollaries. Because this execution host is
       memory-capped (~1.0 GiB cgroup, the same class as the y=15/y=16/
       y=17 census hosts), the census runs each raw engine in its own command
       (C11ordered / C11canonical) through a BOUNDED-MEMOIZATION twin
       of the verbatim engine (identical recursive definition,
       existing LRU-capped cache; memoization of a deterministic pure
       function is transparent, and LRU eviction is deterministic under
       the fixed visit order). Each part writes output/census-<engine>.json;
       the C11 mode validates both parts (engine name, census geometry
       point counts, corollary counts recomputed from formulas, bad == 0
       fail-closed) and merges them. The unbounded verbatim engines
       still anchor C1, C1b, C3.
  C12  deep closed grid z=0..120, x=18..120, R<=x+z+20

Trust boundary (same machine class as the y=5..y=17 proof machines):
option decomposition + closed-form mex identity + finite-type confluence
over the free-coordinate box, anchored to raw engines, to the published
y=17 family (K1240 proved, the B-child), to the x=18 multiset merger
((17,18)==(18,17)). The family law shifts carried from y=17 to y=18
(even-y type, same row-type family as y=10/12/14/16: value-1 infinite band
and tail on x odd rows; pin lattice unified law pin = z+(d+54)/2 with
o_pin in [19,36], z-odd 9 pin rows d in {-14,-10,-6,-2,2,6,10,14,18} /
z-even 9 pin rows d in {-16,-12,-8,-4,0,4,8,12,16} -- the first
both-parity 9-pin-row family (y/2 row count law on both parities);
z-odd I rows k(d)=floor((d+3y+2)/4) with th sweeping the consecutive
integers 19..37 over the 19 d-even rows (the first 19-row sweep);
pin slot = th-1 (8th consecutive family); z-even I rows
k(d)=floor((d+3y-1)/4), th=2k+1, z-even pin slot = 2k+1; base rows
k(d)=floor((d+3y+1)/4) (9th consecutive candidate family), the z-even
d=18 base row at k=18 saturation; sweep row d=19; steady pins z+36/z+37;
single even band law (even-y contrast to y=15/y=17 band_base/band_int
separation); band bottom 2y+2=38; tail x+z+19 on x odd rows; merge x<=z-19;
even-z diagonal d=-18 without value 1 (11th consecutive candidate family);
the final pin row d=18=y reaching the upper endpoint in I[37) form) are
all inside the audited tables, not assumed separately.

Published transcriptions inside this file (each guarded by explicit
@@TRANSCRIPTION markers and machine-checked against the published bytes
by scripts/check_transcriptions_y18.py before this machine runs):
  engines + K0832 single_token (raw engines H_ordered/H_canonical, the
  K0832 single-token closed form and its helpers): verbatim from the
  published verify_y17_universal.py part2 (commit
  ab23d12014afaa57eb3da83b3ffd056e86df4949, SHA-256 4253cf29...), whose
  own provenance chain is the published verify_y13/verify_y14/
  verify_y15/verify_y16 machines (K1231/K1233/K1235/K1237 promotion
  machines), verify_y12_universal.py (K1152/K1162), verify_y11_
  universal.py (K1143 part 1), verify_y10_universal.py (K1141) and
  verify_y09_universal.py (K1138);
  cand17 (the B-child of every y=18 point and the x=18 merger child
  value): verbatim from the published verify_y17_universal.py cand17
  block (block-local Y renamed to Y17 so the cand18 block can carry
  Y = 18; that block is itself the published cand17.py transcription
  minus the fit driver; its universal proof is K1240, promoted by the
  K1241 part1/part2 machine); its y=18-scope usage (x >= 18 rows) is
  inside its published universal domain (x >= 17, all z, all R);
  cand18: verbatim from the published cand18.py (K1242 fit experiment
  vertical-fiber-two-token-y18-parametric-allz-fit-20261123, commit
  9e898f45; the fit driver is omitted); its correctness at universal
  scope is exactly the claim under test, not assumed;
Their correctness is K0832/K1240's claim (not re-proven here); every
transcription is additionally re-anchored against the raw
order-preserving engine by this machine's C1/C1b.
Determinism: fixed seed, no clock, sorted audit keys, census parts
deterministic under the fixed visit order and LRU cap.
"""


import hashlib
import json
import random
import sys
import types
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(1_000_000)


# @@TRANSCRIPTION-ENGINE-START@@
def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m



# ------------------------------------------------------------------
# Raw engines (verbatim from the published K1138 verifier).
# ------------------------------------------------------------------
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
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z + 1))
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

# @@TRANSCRIPTION-ENGINE-END@@


# =====================================================================
# Published y=17 two-token closed form (K1240 proved). This is the
# B-child of every y=18 point and the x=18 merger child value. Code
# block verbatim from the published verify_y17_universal.py cand17
# block (block-local Y renamed to Y17 so the cand18 block can carry
# Y = 18; that block is itself the published cand17.py transcription
# minus the fit driver; machine-checked against the published bytes by
# scripts/check_transcriptions_y18.py); its y=18-scope usage (x >= 18
# rows) is inside its published universal domain (x >= 17, all z, all R).
# =====================================================================
# @@TRANSCRIPTION-CAND17-START@@
Y17 = 17

def q_odd(k):
    return k if k % 2 == 1 else k - 1

def single_token_val(S, R):
    # K0832 published single-token closed form, z-independent rows (merge region)
    if R == 0:
        return 0
    if R % 2 == 1 and R <= q_odd(S):
        return 2
    if S % 2 == 1 and R >= q_odd(S) + 1:
        return 1
    return 0

def in_T17(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y17 - 1:
        S = x + Y17
        return R % 2 == 1 and R <= q_odd(S)
    d = x - z
    o = R - z
    if d == -Y17:
        cap = (z + Y17 - 1) if z % 2 == 1 else (z + Y17)
        if R % 2 == 1 and R <= (z if z % 2 == 1 else z - 1):
            return True
        if z % 2 == 1:
            return o % 2 == 0 and 2 <= o <= cap - z
        else:
            return o % 2 == 1 and 1 <= o <= cap - z
    if z % 2 == 1:
        ladder = R % 2 == 1 and R <= z
        if (d + 3 * Y17) % 4 == 0:
            o_pin = (d + 3 * Y17) // 2
            if Y17 + 1 <= o_pin <= 2 * Y17 and R == z + o_pin:
                return True
        if d == Y17 + 1:
            return ladder or (o % 2 == 0 and 2 * Y17 <= o <= x + Y17)
        if d >= Y17 + 2:
            return ladder or R == z + 2 * Y17
        return ladder
    else:
        ladder = R % 2 == 1 and R <= z - 1
        if (d + 3 * Y17) % 4 == 2:
            o_pin = (d + 3 * Y17) // 2
            if Y17 + 1 <= o_pin <= 2 * Y17 and R == z + o_pin:
                return True
        if d == Y17 + 1:
            return ladder or (o % 2 == 1 and 2 * Y17 + 1 <= o <= x + Y17)
        if d >= Y17 + 2:
            return ladder or R == z + 2 * Y17 + 1
        return ladder

def _bk(off, k):
    return 1 <= off <= 2 * k - 1 and off % 2 == 1

def in_P17(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y17 - 1:
        S = x + Y17
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    off = R - z
    b17 = _bk(off, Y17)
    band_base = off % 2 == 0 and 2 * Y17 + 2 <= off <= x + Y17          # steady base rows
    band_int = off % 2 == 0 and 2 * Y17 + 2 <= off <= x + Y17 - 1       # steady I rows
    tail = x % 2 == 0 and R >= x + z + Y17 + 1                         # S odd rows (y=17: x even)
    if z % 2 == 1:
        if -Y17 <= d <= Y17 and d % 2 == 1:
            k = (d + 3 * Y17 + 1) // 4      # I rows: b_k U I[2k+1)  (diag d=-17 included, k=8)
            return _bk(off, k) or off >= 2 * k + 1
        if d == Y17 + 1:
            return b17                     # sweep row, base type: z odd x odd
        if d >= Y17 + 2:
            if d % 2 == 0:
                return b17 or band_base
            return b17 or band_int or tail
        return _bk(off, (d + 3 * Y17 + 1) // 4)  # base rows d even in [-16,16]
    else:
        if d == -Y17:
            return False                   # even-z diagonal: no value-1 at all (10th consecutive candidate)
        if d == Y17 + 1:
            return b17 or band_int or tail     # sweep row, I type: z even x even
        if d >= Y17 + 2:
            if d % 2 == 1:
                return b17 or band_base
            return b17 or band_int or tail
        if d % 2 == 0:
            k = (d + 3 * Y17 - 1) // 4       # I rows: b_k U I[2k+1)
            return _bk(off, k) or off >= 2 * k + 1
        return _bk(off, (d + 3 * Y17 + 1) // 4)  # base rows d odd in [-15,17]

def cand17(z, x, R):
    if R <= 0:
        return 0
    if in_T17(z, x, R):
        return 2
    if in_P17(z, x, R):
        return 1
    return 0
# @@TRANSCRIPTION-CAND17-END@@


# =====================================================================
# Published y=18 closed form cand18 (K1242, status observed at the time
# of this machine's construction; fit-driver omitted). cand18 tables
# verbatim from the published cand18.py (K1242 fit experiment, commit
# 9e898f45; machine-checked against the published bytes by
# scripts/check_transcriptions_y18.py); the published bytes are
# re-anchored against the raw engines by this machine's C1 and against
# the y=17 family B-child by C1b/C3.
# =====================================================================
# @@TRANSCRIPTION-CAND18-START@@
Y = 18

def q_odd(k):
    return k if k % 2 == 1 else k - 1

def single_token_val(S, R):
    # K0832 published single-token closed form, z-independent rows (merge region)
    if R == 0:
        return 0
    if R % 2 == 1 and R <= q_odd(S):
        return 2
    if S % 2 == 1 and R >= q_odd(S) + 1:
        return 1
    return 0

def in_T18(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y - 1:
        S = x + Y
        return R % 2 == 1 and R <= q_odd(S)
    d = x - z
    o = R - z
    if d == -Y:
        if R % 2 == 1 and R <= (z if z % 2 == 1 else z - 1):
            return True
        if z % 2 == 1:
            return o % 2 == 0 and 2 <= o <= Y
        return o % 2 == 1 and 1 <= o <= Y - 1
    if z % 2 == 1:
        ladder = R % 2 == 1 and R <= z
        if (d + 3 * Y) % 4 == 0 and -Y + 4 <= d <= Y:
            if R == z + (d + 3 * Y) // 2:
                return True
        if d == Y + 1:
            return ladder or (o % 2 == 0 and 2 * Y <= o <= x + Y)
        if d >= Y + 2:
            return ladder or R == z + 2 * Y
        return ladder
    else:
        ladder = R % 2 == 1 and R <= z - 1
        if (d + 3 * Y) % 4 == 2 and -Y + 2 <= d <= Y - 2:
            if R == z + (d + 3 * Y) // 2:
                return True
        if d == Y + 1:
            return ladder or (o % 2 == 1 and 2 * Y + 1 <= o <= x + Y)
        if d >= Y + 2:
            return ladder or R == z + 2 * Y + 1
        return ladder

def _bk(off, k):
    return 1 <= off <= 2 * k - 1 and off % 2 == 1

def in_P18(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y - 1:
        S = x + Y
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    off = R - z
    b18 = _bk(off, Y)
    band = off % 2 == 0 and 2 * Y + 2 <= off <= x + Y          # steady/sweep even band
    tail = x % 2 == 1 and R >= x + z + Y + 1                    # S odd rows (y=18: x odd)
    if z % 2 == 1:
        if -Y <= d <= Y and d % 2 == 0:
            k = (d + 3 * Y + 2) // 4          # I rows: b_k U I[th) (diag d=-18 incl., k=9)
            th = 2 * k + (1 if (d + 3 * Y) % 4 == 0 else 0)   # pin rows (d==y mod4): 2k+1; skew: 2k
            return _bk(off, k) or off >= th
        if -Y + 1 <= d <= Y - 1 and d % 2 == 1:
            return _bk(off, (d + 3 * Y + 1) // 4)  # base rows d odd in [-17,17]
        if d == Y + 1:
            return b18                          # sweep row, base type: z odd x even
        return b18 or band or tail              # d >= Y+2 steady rows
    else:
        if d == -Y:
            return False                        # even-z diagonal: no value-1 (11th consecutive candidate family y=8..18)
        if -Y + 1 <= d <= Y - 1 and d % 2 == 1:
            k = (d + 3 * Y - 1) // 4           # I rows: b_k U I[2k+1)
            return _bk(off, k) or off >= 2 * k + 1
        if -Y + 2 <= d <= Y and d % 2 == 0:
            return _bk(off, (d + 3 * Y + 1) // 4)  # base rows d even in [-16,18] (d=18 saturates k=Y=18)
        return b18 or band or tail              # d >= Y+1 (sweep 19 incl.: x odd -> tail active)

def cand18(z, x, R):
    if R <= 0:
        return 0
    if in_T18(z, x, R):
        return 2
    if in_P18(z, x, R):
        return 1
    return 0
# @@TRANSCRIPTION-CAND18-END@@


def opts18(z, x, R):
    """Closed-form option values of H(R; (x,18); z). R >= 1.

    x == 18: both token-decrement children coincide as multisets:
    (17,18) == (18,17), both are the y=17 family row x=18.
    """
    if x == 18:
        A = cand17(z, 18, R - 1)
    else:
        A = cand18(z, x - 1, R - 1)
    out = [A, cand17(z, x, R - 1)]
    if z >= 1:
        out.append(1 ^ cand18(z - 1, x, R - 1))
    return out


def identity_ok18(z, x, R):
    t = in_T17(z, x, R)
    pv = in_P17(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    got = mex(opts18(z, x, R))
    want = cand18(z, x, R)
    return got == want, got, want


# ------------------------------------------------------------------
# Type machine. y=17's clip window (+/-36 sentinel +/-37) folded the
# y=17 features; the y=18 features (pins up to z+36 odd-z / z+37 even-z
# for the final-pin row, steady pins z+36/z+37, sweep band d=19 offsets
# up to x+18, band bottom R-z = 2y+2 = 38, tail offset R-x-z = 19,
# merge boundary x = z-19, base span to z+37 and the I-row th(d)
# excursions up to 37) are tested with +/-38/39 (= 2y+2 for y=18),
# the 14-family-continuation candidate of the 2y+2 tight pattern
# (y=5..17: 12/14/16/18/20/22/24/26/28/30/32/34/36). CLIP/SENT are
# re-checked for confluence by check_C4; the tightness probe (CLIP=37)
# is reported separately (check_C4t).
# ------------------------------------------------------------------
CLIP, SENT = 38, 39


def clipw(w):
    if w > CLIP:
        return SENT
    if w < -CLIP:
        return -SENT
    return w


def type_of18(z, x, R):
    return (1 if x == 18 else 0,
            1 if z == 0 else 0,
            z % 2, x % 2, R % 2,
            clipw(x - z), clipw(R - x), clipw(R - z),
            clipw(R - x - z), clipw(R - 2 * x), clipw(R - 2 * z))


def vpoint(v0, v1, v3):
    z = v1 - v3
    x = v0 + v1 - v3
    R = v0 + 2 * v1 - v3
    return z, x, R


# ------------------------------------------------------------------
# Checks.
# ------------------------------------------------------------------
def check_C1(audit):
    n = bad = 0
    for z in range(0, 15):
        for x in range(18, 37):
            for R in range(0, x + z + 50):
                n += 1
                c = cand18(z, x, R)
                if H_ordered(R, (x, 18), z) != c or H_canonical(R, (x, 18), z) != c:
                    bad += 1
    audit['C1'] = {'desc': 'raw both engines vs cand18 z=0..14 x=18..36 R<=x+z+49',
                   'points': n, 'bad': bad}


def check_C1b(audit):
    n = bad = 0
    # (i) single-token closed form (K0832) vs raw ordered engine
    for z in range(0, 21):
        for x in range(1, 21):
            for R in range(0, x + z + 21):
                n += 1
                if H_ordered(R, (x,), z) != single_token(x, z, R):
                    bad += 1
    # (ii) published y=17 closed form (K1240, the B-child) raw anchor
    for z in range(0, 25):
        for x in range(17, 31):
            for R in range(0, x + z + 33):
                n += 1
                if H_ordered(R, (x, 17), z) != cand17(z, x, R):
                    bad += 1
    # (iii) x=18 multiset merger: (17,18) == (18,17) raw, and == cand17(z,18,R-1)
    for z in range(0, 31):
        for R in range(1, z + 47):
            n += 1
            a = H_ordered(R - 1, (17, 18), z)
            b = H_ordered(R - 1, (18, 17), z)
            c = H_canonical(R - 1, (17, 18), z)
            if a != b or a != c or a != cand17(z, 18, R - 1):
                bad += 1
    audit['C1b'] = {'desc': 'single_token/y=17-child/x=18 merger raw anchors',
                    'points': n, 'bad': bad}


def check_C2(audit, corr):
    n = bad = 0
    for z in range(0, 49):
        for x in range(18, 61):
            for R in range(1, x + z + 45):
                n += 1
                ok, _, _ = identity_ok18(z, x, R)
                if not ok:
                    bad += 1
                corollary(z, x, R, corr)
    audit['C2'] = {'desc': 'closed identity grid z=0..48 x=18..60 R<=x+z+44 (+merge,tail)',
                   'points': n, 'bad': bad}


def check_C2b(audit):
    n = bad = 0
    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(18, 73, 5):
            for R in range(1, x + z + 32):
                n += 1
                ok, _, _ = identity_ok18(z, x, R)
                if not ok or (R >= x + z + 19 and cand18(z, x, R) != (x + 18) % 2):
                    bad += 1
    audit['C2b'] = {'desc': 'deep tail identity rows z in {60..400} x=18..68(step5) R<=x+z+31',
                    'points': n, 'bad': bad}


def check_C3(audit):
    n = bad = 0
    for z in range(0, 6):
        for x in range(18, 23):
            for R in range(1, x + z + 22):
                n += 1
                # raw option set by manual child enumeration on the raw engine
                raw_opts = set()
                if x > 18:
                    raw_opts.add(H_ordered(R - 1, (x - 1, 18), z))
                else:
                    raw_opts.add(H_ordered(R - 1, (17, 18), z))
                raw_opts.add(H_ordered(R - 1, (x, 17), z))
                if z >= 1:
                    raw_opts.add(1 ^ H_ordered(R - 1, (x, 18), z - 1))
                closed = set(opts18(z, x, R))
                if raw_opts != closed:
                    bad += 1
    audit['C3'] = {'desc': 'option decomposition vs raw child enumeration',
                   'points': n, 'bad': bad}


def conform(z, x, R, types):
    """Return True if this point's type conforms (registry update if new)."""
    t = type_of18(z, x, R)
    e = (cand18(z, x, R), tuple(sorted(opts18(z, x, R))))
    if t not in types:
        types[t] = e
        return True
    return types[t] == e


def box_points(B):
    for v0 in range(-B, B + 1):
        for v1 in range(-B, B + 1):
            for v3 in range(-B, B + 1):
                z, x, R = vpoint(v0, v1, v3)
                if z < 0 or x < 18 or R < 1:
                    continue
                yield z, x, R


def check_C4(audit, types):
    n = bad = conf_bad = id_bad = 0
    for z, x, R in box_points(60):
        n += 1
        ok, _, _ = identity_ok18(z, x, R)
        if not ok:
            id_bad += 1
        if not conform(z, x, R, types):
            conf_bad += 1
    bad = id_bad + conf_bad
    audit['C4'] = {'desc': 'type machine box +/-60, clip 38/sentinel 39, confluence',
                   'points': n, 'bad': bad, 'types': len(types),
                   'identity_bad': id_bad, 'confluence_bad': conf_bad}


def check_C4t(audit):
    """Tightness probe: clip 37 / sentinel 38 over the same box.

    Counts type-confluence violations when the clip window is narrowed
    by one (2y+1 instead of the 14-family candidate 2y+2=38). Not part
    of the PASS/FAIL bad total; reported for the pattern claim.
    """
    global CLIP, SENT
    old_clip, old_sent = CLIP, SENT
    CLIP, SENT = 37, 38
    n = viol = 0
    first = None
    probe_types = {}
    for z, x, R in box_points(60):
        n += 1
        if not conform(z, x, R, probe_types):
            viol += 1
            if first is None:
                first = (z, x, R)
    CLIP, SENT = old_clip, old_sent
    audit['C4t'] = {'desc': 'tightness probe clip 37/sentinel 38 (not in bad total)',
                    'points': n, 'violations_at_clip37': viol,
                    'first_violation': first}


def check_C7(audit, types, corr):
    rng = random.Random(20261182)
    n = bad = 0
    for _ in range(200000):
        z = rng.randrange(0, 3001)
        x = rng.randrange(18, 3001)
        mode = rng.randrange(4)
        if mode == 0:
            R = rng.randrange(1, x + z + 19)
        elif mode == 1:
            R = x + z + 19 + rng.randrange(-3, 4)
        elif mode == 2:
            x = max(18, z + rng.randrange(-30, 21))
            R = rng.randrange(1, 9001)
        else:
            R = rng.randrange(1, 9001)
        if R < 1 or x < 18:
            continue
        n += 1
        ok, _, _ = identity_ok18(z, x, R)
        if not ok or not conform(z, x, R, types):
            bad += 1
        corollary(z, x, R, corr)
    audit['C7'] = {'desc': 'seeded far probes 200k, seed 20261182, z,x<=3000',
                   'points': n, 'bad': bad}


def check_C8(audit, types, corr):
    n = bad = 0
    zs = list(range(0, 6)) + list(range(29, 32)) + list(range(59, 62)) + \
        list(range(299, 302)) + list(range(999, 1002)) + [2999, 3000]
    for z in zs:
        for dx in range(-30, 20):
            x = z + dx
            if x < 17:
                continue
            for R in range(1, x + z + 33):
                n += 1
                ok, _, _ = identity_ok18(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
            for R in (x + z + 19, x + z + 20, x + z + 21):
                n += 1
                if cand17(z, x, R) != (x + 17) % 2:
                    bad += 1
    audit['C8'] = {'desc': 'boundary manifolds z<=3000, dx in [-30,19], tail window',
                   'points': n, 'bad': bad}


def check_C9(audit, types):
    n = bad = 0
    for band in ((61, 64), (89, 92), (117, 120)):
        lo, hi = band
        for v0 in range(-hi, hi + 1):
            for v1 in range(-hi, hi + 1):
                for v3 in range(-hi, hi + 1):
                    m = max(abs(v0), abs(v1), abs(v3))
                    if m < lo:
                        continue
                    z, x, R = vpoint(v0, v1, v3)
                    if z < 0 or x < 18 or R < 1:
                        continue
                    n += 1
                    ok, _, _ = identity_ok18(z, x, R)
                    if not ok or not conform(z, x, R, types):
                        bad += 1
    audit['C9'] = {'desc': 'v-space shell sweeps [61,64],[89,92],[117,120]',
                   'points': n, 'bad': bad}


# ------------------------------------------------------------------
# C11 census: bounded-memoization twins + separate-command parts.
# ------------------------------------------------------------------
CENSUS_CACHE_MAXSIZE = 1_600_000


def _bounded_twin(raw_engine, name):
    """LRU-capped twin of a published raw engine.

    The recursive definition is byte-identical (the published function's
    own code object re-bound into a shallow copy of the module globals,
    with the recursive name resolving to the capped wrapper instead of the
    unbounded cache). Memoization of a deterministic pure function is
    transparent, and LRU eviction is deterministic under the fixed
    census visit order, so the twin returns exactly the published engine's
    values; the cap only bounds residency on this memory-capped host
    (~1.0 GiB cgroup, the same class as the y=15/y=16/y=17 census hosts).
    """
    impl = raw_engine.__wrapped__
    g = dict(impl.__globals__)
    twin = types.FunctionType(impl.__code__, g, impl.__name__)
    capped = lru_cache(CENSUS_CACHE_MAXSIZE)(twin)
    g[name] = capped
    return capped


def _census_part_file(engine_name):
    return f"census-{engine_name}.json"


def _census_expected_counts():
    points = merge = tail = 0
    for z in range(0, 80):
        for x in range(18, 71):
            points += x + z + 20
            if x <= z - 19:
                merge += x + z + 20
            tail += 1  # exactly one R (= x+z+19) is >= x+z+19 within the box
    return points, merge, tail


def run_census(engine_name):
    if engine_name not in ("ordered", "canonical"):
        raise SystemExit(f"FAIL-CLOSED: unknown census engine {engine_name}")
    raw = H_ordered if engine_name == "ordered" else H_canonical
    twin = _bounded_twin(raw, "H_ordered" if engine_name == "ordered" else "H_canonical")
    n = bad = 0
    corr = {'merge': {'points': 0, 'bad': 0}, 'tail': {'points': 0, 'bad': 0}}
    for z in range(0, 80):
        for x in range(18, 71):
            for R in range(0, x + z + 20):
                c = cand18(z, x, R)
                if twin(R, (x, 18), z) != c:
                    bad += 1
                corollary(z, x, R, corr)
                n += 1
    payload = {
        'engine': engine_name,
        'box': 'z=0..79, x=18..70, R=0..x+z+19',
        'cache_type': 'bounded-memoization twin of the verbatim raw engine (published code object, LRU-capped cache)',
        'cache_maxsize': CENSUS_CACHE_MAXSIZE,
        'points': n,
        'bad': bad,
        'corollaries': {
            'merge': {'points': corr['merge']['points'], 'bad': corr['merge']['bad'],
                      'claim': 'x<=z-19 => H == single_token(x+18,z,R)'},
            'tail': {'points': corr['tail']['points'], 'bad': corr['tail']['bad'],
                     'claim': 'R>=x+z+19 => H == (x+18)%2'},
        },
    }
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    (out / _census_part_file(engine_name)).write_text(text, encoding="utf-8")
    print(f"census[{engine_name}]: points={n} bad={bad} "
          f"merge={corr['merge']} tail={corr['tail']}", flush=True)
    return 0 if bad == 0 and corr['merge']['bad'] == 0 and corr['tail']['bad'] == 0 else 1


def check_C11(audit, corr):
    out = Path(__file__).with_name("output")
    parts = {}
    for engine_name in ("ordered", "canonical"):
        p = out / _census_part_file(engine_name)
        if not p.is_file():
            raise SystemExit(
                f"FAIL-CLOSED: census part file for engine '{engine_name}' is "
                f"missing ({p.name}); run mode C11{engine_name} first")
        parts[engine_name] = json.loads(p.read_text(encoding="utf-8"))
    exp_points, exp_merge, exp_tail = _census_expected_counts()
    for engine_name, part in parts.items():
        if part.get('engine') != engine_name:
            raise SystemExit("FAIL-CLOSED: census part engine field mismatch")
        if part.get('box') != 'z=0..79, x=18..70, R=0..x+z+19':
            raise SystemExit("FAIL-CLOSED: census part box mismatch")
        if part.get('cache_maxsize') != CENSUS_CACHE_MAXSIZE:
            raise SystemExit("FAIL-CLOSED: census cache cap mismatch")
        if part.get('points') != exp_points:
            raise SystemExit(f"FAIL-CLOSED: census points {part.get('points')} != {exp_points}")
        if part.get('bad') != 0:
            raise SystemExit("FAIL-CLOSED: census part reported bad != 0")
        cm, ct = part['corollaries']['merge'], part['corollaries']['tail']
        if cm['points'] != exp_merge or cm['bad'] != 0:
            raise SystemExit("FAIL-CLOSED: census merge corollary mismatch")
        if ct['points'] != exp_tail or ct['bad'] != 0:
            raise SystemExit("FAIL-CLOSED: census tail corollary mismatch")
    ordered, canonical = parts['ordered'], parts['canonical']
    n = ordered['points'] + canonical['points']
    bad = ordered['bad'] + canonical['bad']
    for k in ('merge', 'tail'):
        corr[k]['points'] += ordered['corollaries'][k]['points'] + canonical['corollaries'][k]['points']
        corr[k]['bad'] += ordered['corollaries'][k]['bad'] + canonical['corollaries'][k]['bad']
    audit['C11'] = {'desc': 'raw census anchor z=0..79 x=18..70 R<=x+z+19, both engines '
                            '(bounded-memoization twins, LRU cap 1600000, separate commands '
                            'C11ordered/C11canonical on this memory-capped host), parts validated '
                            'and merged here with recomputed expected counts',
                    'points': n, 'bad': bad,
                    'ordered_points': ordered['points'],
                    'canonical_points': canonical['points'],
                    'census_cache_maxsize': CENSUS_CACHE_MAXSIZE,
                    'census_part_files': ['census-ordered.json', 'census-canonical.json']}


def check_C12(audit, types, corr):
    n = bad = 0
    for z in range(0, 121):
        for x in range(18, 121):
            for R in range(1, x + z + 21):
                n += 1
                ok, _, _ = identity_ok18(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
    audit['C12'] = {'desc': 'deep closed grid z=0..120 x=18..120 R<=x+z+20',
                   'points': n, 'bad': bad}


def corollary(z, x, R, corr):
    if x <= z - 19:
        corr['merge']['points'] += 1
        if cand18(z, x, R) != single_token(x + 18, z, R):
            corr['merge']['bad'] += 1
    if R >= x + z + 19:
        corr['tail']['points'] += 1
        if cand18(z, x, R) != (x + 18) % 2:
            corr['tail']['bad'] += 1


def main():
    args = sys.argv[1:]
    if args and args[0] in ("C11ordered", "C11canonical"):
        rc = run_census(args[0][3:].lower())
        return {'overall': 'PASS' if rc == 0 else 'FAIL'}
    requested = set(args)
    everything = {'C1', 'C1b', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C12'}
    todo = requested & everything if requested else (everything - {'C11'})
    audit = {'experiment': 'vertical-fiber-two-token-y18-parametric-allz-proof-20261123',
             'family': 'H(R;(x,18);z), z>=0, x>=18, R>=0',
             'stage': 'part1 (the 12-check canonical machine; the part2 stage '
                      'adds C1d published-slice anchors at the y=18 rows and the '
                      'independent census.txt consumer C11r; census parts '
                      'anchored via bounded-memoization twins on a memory-capped '
                      'host)',
             'checks_run': sorted(todo),
             'checks': {},
             'corollaries': {
                 'merge_below_diagonal': {'claim': 'x<=z-19 => H == single_token(x+18,z,R)'},
                 'tail': {'claim': 'R>=x+z+19 => H == (x+18)%2'}}}
    corr = {'merge': {'points': 0, 'bad': 0}, 'tail': {'points': 0, 'bad': 0}}
    types = {}

    for name in ('C1', 'C1b', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C12'):
        if name not in todo:
            continue
        if name == 'C1':
            check_C1(audit['checks'])
        elif name == 'C1b':
            check_C1b(audit['checks'])
        elif name == 'C2':
            check_C2(audit['checks'], corr)
        elif name == 'C2b':
            check_C2b(audit['checks'])
        elif name == 'C3':
            check_C3(audit['checks'])
        elif name == 'C4':
            check_C4(audit['checks'], types)
        elif name == 'C4t':
            check_C4t(audit['checks'])
        elif name == 'C7':
            check_C7(audit['checks'], types, corr)
        elif name == 'C8':
            check_C8(audit['checks'], types, corr)
        elif name == 'C9':
            check_C9(audit['checks'], types)
        elif name == 'C11':
            check_C11(audit['checks'], corr)
        elif name == 'C12':
            check_C12(audit['checks'], types, corr)
        c = audit['checks'].get(name)
        if c:
            print(f"  {name}: pts={c.get('points')} bad={c.get('bad', 0)}", flush=True)

    audit['corollaries']['merge_below_diagonal'].update(corr['merge'])
    audit['corollaries']['tail'].update(corr['tail'])
    total = sum(c['points'] for c in audit['checks'].values() if 'points' in c)
    allbad = sum(c['bad'] for c in audit['checks'].values() if 'bad' in c)
    audit['total_points'] = total
    audit['total_bad'] = allbad + corr['merge']['bad'] + corr['tail']['bad']
    audit['type_count'] = len(types)
    audit['overall'] = 'PASS' if audit['total_bad'] == 0 else 'FAIL'
    audit['verifier_sha256'] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(audit, sort_keys=True, ensure_ascii=False, indent=2)
    (out / "audit.json").write_text(payload + "\n", encoding="utf-8")
    print('overall:', audit['overall'], 'total_points:', total,
          'types:', len(types), flush=True)
    for k in sorted(audit['checks']):
        c = audit['checks'][k]
        print(f"  {k}: pts={c.get('points')} bad={c.get('bad')}", flush=True)
    print('  merge:', corr['merge'])
    print('  tail:', corr['tail'])
    if 'C4t' in audit['checks']:
        t = audit['checks']['C4t']
        print('  C4t:', t['violations_at_clip37'], 'violations at clip 37, first:', t['first_violation'])
    return audit


if __name__ == '__main__':
    sys.exit(0 if main()['overall'] == 'PASS' else 1)
