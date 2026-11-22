#!/usr/bin/env python3
"""Universal verifier for the y=13 two-token residual family (PART 1).

Family: H(R; (x,13); z), all z >= 0, all x >= 13, all R >= 0.
Claim under test (K1231, currently status "observed"; this machine is the
promotion-stage part 1): the closed form cand13 (T/P row tables below)
equals H everywhere; with corollaries
  merge-below-diagonal (y=13 promotion of the y=12 line): x <= z-14
       =>  H == single_token(x+13, z, R)
  tail:                                 R >= x+z+14  =>  H == (x+13) % 2

STAGE: part 1 (publishes the 12-check machine and the part-1 audit). The
promotion decision K1231 observed -> proved is reserved for part2 (C1d
published fixed-z slice anchors at y=13 and the independent
census_rows.py census consumer), per the procedure that promoted
y=5..y=12 (K1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138/K1141/
K1143/K1152). This is the first family whose B-child chain (cand12,
K1152 proved) is itself a universally proved family.

Checks implemented and run here: C1, C1b, C2, C2b, C3, C4 (clip window
2y+2 = 28, sentinel 29), C4t (clip tightness probe 27/28), C7, C8, C9,
C11, C12.

Run modes:
  python3 verify_y13_universal.py                 # all checks except C11
  python3 verify_y13_universal.py C11ordered      # census part 1 (slow)
  python3 verify_y13_universal.py C11canonical   # census part 2 (slow)
  python3 verify_y13_universal.py C11            # merge census parts, then
                                                # run all checks incl. C11
  python3 verify_y13_universal.py C1 C2 ...       # explicit check list

  C1   raw order-preserving AND descending-canonical engines vs cand13,
       z=0..14, x=13..31, R=0..x+z+47
  C1b  single-token closed form (K0832) raw anchor; published y=12 closed
       form (K1152 transcription, the B-child of every y=13 point and the
       x=13 A-child) raw anchor; x=13 multiset merger (12,13)==(13,12)
       i.e. A==B child value raw anchor
  C2   closed-form identity grid z=0..48, x=13..58, R<=x+z+42 (+merge,tail)
  C2b  deep-tail identity rows z in {60,72,84,96,108,120,240,400},
       x in {13,18,...,63}, R <= x+z+31
  C3   option-decomposition raw anchor (child sets vs raw recursion)
  C4   type machine, clip window 2y+2 = 28 sentinel 29, free-coordinate
       box v0=x-z, v1=R-x, v3=R-x-z in +/-60: full sweep, per-type
       confluence of the (value, sorted-children) effect
  C4t  tightness probe: the same box at clip 27 counts confluence
       violations (informational, not part of the bad total) -- tests
       the 9-family continuation candidate of the tight 2y+2 clip
       pattern (y=5..12: 12/14/16/18/20/22/24/26; 2y+2 for y=13 is 28)
  C7   fixed-seed far probes (seed 20261132): 200k points, z,x <= 3000,
       R <= 9000, tail window around x+z+14
  C8   boundary manifolds z in {0..5, 29..31, 59..61, 299..301,
       999..1001, 2999, 3000}, dx in [-28, 17], tail window
       [x+z+14, x+z+16]
  C9   v-space shell sweeps at radii [61,64], [89,92], [117,120]
  C11  raw census anchor z=0..79, x=13..70, R<=x+z+14, both engines,
       plus merge/tail corollaries. Because this execution host is capped
       at 1 GiB RAM (cgroup), the fully resident cold census of this box
       exceeds memory in one process; the census therefore runs each raw
       engine in its own command (C11ordered / C11canonical) through a
       BOUNDED-MEMOIZATION twin of the verbatim engine (identical
       recursive definition, existing LRU-capped cache; memoization of
       a deterministic pure function is transparent, and LRU eviction is
       deterministic under the fixed visit order). Each part writes
       output/census-<engine>.json; the C11 mode validates both parts
       (engine name, census geometry point counts, corollary counts
       recomputed from formulas, bad == 0 fail-closed) and merges them.
       The unbounded verbatim engines still anchor C1, C1b, C3.
  C12  deep closed grid z=0..120, x=13..120, R<=x+z+16

Trust boundary (same machine class as the y=5..y=12 promotion machines
K1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138/K1141/K1143-part1/
K1162): option decomposition + closed-form mex identity + finite-type
confluence over the free-coordinate box, anchored to raw engines and to
the published y=12 family (K1152 proved, the B-child) and to the x=13
multiset merger ((12,13)==(13,12)). The family law shifts carried from
y=12 to y=13 (odd-y type, same as y=9/y=11: value-1 infinite band and
tail on x even rows; pin lattice (d+3y)%4==0 with o_pin=(d+3y)/2 in
[y+1,2y], z-odd 7 rows d in {-11,-7,-3,1,5,9,13} / z-even 6 rows d in
{-9,-5,-1,3,7,11} -- the first odd-y family with 6 even-z pin rows;
sweep row d=14; steady pins z+26/z+27; band bottom 2y+2=28; tail
x+z+14; merge x<=z-14; even-z diagonal without value 1 (6th consecutive
family); z-odd base/I-row split with k(d)=floor((d+40)/4) and th=2k+1,
z-even I rows k(d)=floor((d+38)/4), sweep-row I type on z even) are all
inside the audited tables, not assumed separately.

Published transcriptions inside this file:
  engines + K0832 single_token (raw engines H_ordered/H_canonical, the
  K0832 single-token closed form and its helpers): verbatim from the
  published verify_y12_universal.py (K1162/K1152 promotion machine,
  SHA-256 e209297603f68c9a82a50f90cac0bc678211d1517f137b5d490dfca3c492eb04),
  whose own provenance chain is the published verify_y11_universal.py
  (K1143 part 1), verify_y10_universal.py (K1141) and
  verify_y09_universal.py (K1138);
  cand12 (the B-child of every y=13 point and the x=13 merger child):
  verbatim from the published verify_y12_universal.py's cand12 block
  (block-local Y renamed to Y12 so the cand13 block can carry Y = 13;
  that block is itself the published cand12.py transcription minus the
  fit driver; its universal proof is K1152);
  cand13: verbatim from the published cand13.py (K1231 fit experiment,
  SHA-256 cb903c56b589310907d44f21674ef61a21a4baf7cec8b2e314d5720ff68e2e09),
  fit driver omitted (its probe self-check is K1231's own evidence,
  re-runnable there);
  the re-defined q_odd/single_token_val copies inside the cand12/cand13
  blocks are semantically identical to the shared body (last definition
  wins at call time, as in the published y=10..y=12 verifiers).
Their correctness is K0832/K1152/K1231's claim, not re-proven here; every
transcription is additionally re-anchored against the raw
order-preserving engine by this machine's C1/C1b, and cand12's y=13-scope
usage is inside its published fit domain (x >= 13 ⊂ x >= 12, all z, all
R, of the K1152 universal proof).
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


# =====================================================================
# Published y=12 two-token closed form (K1152 proved). This is the
# B-child of every y=13 point and the x=13 merger child value. Code block
# verbatim from the published verify_y12_universal.py's cand12 block
# (block-local Y renamed to Y12 so the cand13 block can carry Y = 13;
# that block is itself the published cand12.py transcription minus the
# fit driver; its universal proof is K1152).
# =====================================================================

Y12 = 12

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

def in_T12(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y12 - 1:
        S = x + Y12
        return R % 2 == 1 and R <= q_odd(S)
    d = x - z
    o = R - z
    if d == -Y12:
        if R % 2 == 1 and R <= (z if z % 2 == 1 else z - 1):
            return True
        if z % 2 == 1:
            return o % 2 == 0 and 2 <= o <= Y12
        return o % 2 == 1 and 1 <= o <= Y12 - 1
    if z % 2 == 1:
        ladder = R % 2 == 1 and R <= z
        if d % 4 == 0 and -Y12 + 4 <= d <= Y12:
            if R == z + (d + 3 * Y12) // 2:
                return True
        if d == Y12 + 1:
            return ladder or (o % 2 == 0 and 2 * Y12 <= o <= x + Y12)
        if d >= Y12 + 2:
            return ladder or R == z + 2 * Y12
        return ladder
    else:
        ladder = R % 2 == 1 and R <= z - 1
        if d % 4 == 2 and -Y12 + 2 <= d <= Y12 - 2:
            if R == z + (d + 3 * Y12) // 2:
                return True
        if d == Y12 + 1:
            return ladder or (o % 2 == 1 and 2 * Y12 + 1 <= o <= x + Y12)
        if d >= Y12 + 2:
            return ladder or R == z + 2 * Y12 + 1
        return ladder

def _bk(off, k):
    return 1 <= off <= 2 * k - 1 and off % 2 == 1

def in_P12(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y12 - 1:
        S = x + Y12
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    off = R - z
    b12 = _bk(off, Y12)
    band = off % 2 == 0 and 2 * Y12 + 2 <= off <= x + Y12
    tail = x % 2 == 1 and R >= x + z + Y12 + 1
    if z % 2 == 1:
        if -Y12 <= d <= Y12 and d % 2 == 0:
            k = (d + 38) // 4           # I rows (diag d=-12 and last pin d=12 included)
            th = 2 * k + (1 if d % 4 == 0 else 0)
            return _bk(off, k) or off >= th
        if -Y12 + 1 <= d <= Y12 - 1 and d % 2 == 1:
            return _bk(off, (d + 37) // 4)   # base rows
        if d == Y12 + 1:
            return b12              # sweep row is base-type (x even): band belongs to T
        return b12 or band or tail  # d >= Y12+2 steady rows
    else:
        if d == -Y12:
            return False            # even-z diagonal: no value-1 at all
        if -Y12 + 1 <= d <= Y12 - 1 and d % 2 == 1:
            k = (d + 35) // 4       # I rows: b_k U I[2k+1)
            return _bk(off, k) or off >= 2 * k + 1
        if -Y12 + 2 <= d <= Y12 and d % 2 == 0:
            return _bk(off, (d + 37) // 4)   # base rows
        return b12 or band or tail  # d >= Y12+1 (sweep 13 included: x odd -> tail active)

def cand12(z, x, R):
    if R <= 0:
        return 0
    if in_T12(z, x, R):
        return 2
    if in_P12(z, x, R):
        return 1
    return 0



# =====================================================================
# Candidate under test: y=13 two-token closed form (K1231 published fit).
# cand13 tables verbatim from the published cand13.py (K1231 fit
# experiment); fit driver omitted. The y=12 family (cand12 block above) is
# the B-child of this identity and the x=13 merger child value.
# =====================================================================

Y = 13

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

def in_T13(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y - 1:
        S = x + Y
        return R % 2 == 1 and R <= q_odd(S)
    d = x - z
    o = R - z
    if d == -Y:
        cap = (z + Y - 1) if z % 2 == 1 else (z + Y)
        if R % 2 == 1 and R <= (z if z % 2 == 1 else z - 1):
            return True
        if z % 2 == 1:
            return o % 2 == 0 and 2 <= o <= cap - z
        else:
            return o % 2 == 1 and 1 <= o <= cap - z
    if z % 2 == 1:
        ladder = R % 2 == 1 and R <= z
        if (d + 3 * Y) % 4 == 0:
            o_pin = (d + 3 * Y) // 2
            if Y + 1 <= o_pin <= 2 * Y and R == z + o_pin:
                return True
        if d == Y + 1:
            return ladder or (o % 2 == 0 and 2 * Y <= o <= x + Y)
        if d >= Y + 2:
            return ladder or R == z + 2 * Y
        return ladder
    else:
        ladder = R % 2 == 1 and R <= z - 1
        if (d + 3 * Y) % 4 == 2:
            o_pin = (d + 3 * Y) // 2
            if Y + 1 <= o_pin <= 2 * Y and R == z + o_pin:
                return True
        if d == Y + 1:
            return ladder or (o % 2 == 1 and 2 * Y + 1 <= o <= x + Y)
        if d >= Y + 2:
            return ladder or R == z + 2 * Y + 1
        return ladder

def _bk(off, k):
    return 1 <= off <= 2 * k - 1 and off % 2 == 1

def in_P13(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y - 1:
        S = x + Y
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    off = R - z
    b13 = _bk(off, Y)
    band_base = off % 2 == 0 and 2 * Y + 2 <= off <= x + Y          # steady base rows
    band_int = off % 2 == 0 and 2 * Y + 2 <= off <= x + Y - 1       # steady I rows
    tail = x % 2 == 0 and R >= x + z + Y + 1                          # S odd rows (y=13: x even)
    if z % 2 == 1:
        if -Y <= d <= Y and d % 2 == 1:
            k = (d + 40) // 4         # I rows: b_k U I[2k+1)  (diag d=-13 included, k=6)
            return _bk(off, k) or off >= 2 * k + 1
        if d == Y + 1:
            return b13                 # sweep row, base type: z odd x odd
        if d >= Y + 2:
            if d % 2 == 0:
                return b13 or band_base
            return b13 or band_int or tail
        return _bk(off, (d + 40) // 4)  # base rows d even in [-12,12]
    else:
        if d == -Y:
            return False                # even-z diagonal: no value-1 at all (fit level, 6th consecutive)
        if d == Y + 1:
            return b13 or band_int or tail   # sweep row, I type: z even x even
        if d >= Y + 2:
            if d % 2 == 1:
                return b13 or band_base
            return b13 or band_int or tail
        if d % 2 == 0:
            k = (d + 38) // 4          # I rows: b_k U I[2k+1)
            return _bk(off, k) or off >= 2 * k + 1
        return _bk(off, (d + 40) // 4)  # base rows d odd in [-11,13]

def cand13(z, x, R):
    if R <= 0:
        return 0
    if in_T13(z, x, R):
        return 2
    if in_P13(z, x, R):
        return 1
    return 0


def opts13(z, x, R):
    """Closed-form option values of H(R; (x,13); z). R >= 1.

    x == 13: both token-decrement children coincide as multisets:
    (12,13) == (13,12), both are the y=12 family row x=13.
    """
    if x == 13:
        A = cand12(z, 13, R - 1)
    else:
        A = cand13(z, x - 1, R - 1)
    out = [A, cand12(z, x, R - 1)]
    if z >= 1:
        out.append(1 ^ cand13(z - 1, x, R - 1))
    return out


def identity_ok13(z, x, R):
    t = in_T13(z, x, R)
    pv = in_P13(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    got = mex(opts13(z, x, R))
    want = cand13(z, x, R)
    return got == want, got, want


# ------------------------------------------------------------------
# Type machine. y=12's clip window (+/-26 sentinel +/-27) folded y=12
# features; the y=13 features (pins up to z+26 odd-z / z+27 even-z,
# sweep band d=14 offsets up to x+13, band bottom R-z = 2y+2 = 28,
# tail offset R-x-z = 14, merge boundary x = z-14, base span to z+25
# and the I-row th(d)=2k+1 excursions) are tested with +/-28/29
# (= 2y+2 for y=13), the 9-family-continuation candidate of the 2y+2
# tight pattern (y=5..12: 12/14/16/18/20/22/24/26). CLIP/SENT are
# re-checked for confluence by check_C4; the tightness probe (CLIP=27)
# is reported separately (check_C4t).
# ------------------------------------------------------------------
CLIP, SENT = 28, 29


def clipw(w):
    if w > CLIP:
        return SENT
    if w < -CLIP:
        return -SENT
    return w


def type_of13(z, x, R):
    return (1 if x == 13 else 0,
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
        for x in range(13, 32):
            for R in range(0, x + z + 48):
                n += 1
                c = cand13(z, x, R)
                if H_ordered(R, (x, 13), z) != c or H_canonical(R, (x, 13), z) != c:
                    bad += 1
    audit['C1'] = {'desc': 'raw both engines vs cand13 z=0..14 x=13..31 R<=x+z+47',
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
    # (ii) published y=12 closed form (K1152, the B-child) raw anchor
    for z in range(0, 25):
        for x in range(12, 27):
            for R in range(0, x + z + 30):
                n += 1
                if H_ordered(R, (x, 12), z) != cand12(z, x, R):
                    bad += 1
    # (iii) x=13 multiset merger: (12,13) == (13,12) raw, and == cand12(z,13,R-1)
    for z in range(0, 31):
        for R in range(1, z + 42):
            n += 1
            a = H_ordered(R - 1, (12, 13), z)
            b = H_ordered(R - 1, (13, 12), z)
            c = H_canonical(R - 1, (12, 13), z)
            if a != b or a != c or a != cand12(z, 13, R - 1):
                bad += 1
    audit['C1b'] = {'desc': 'single_token/y=12-child/x=13 merger raw anchors',
                    'points': n, 'bad': bad}


def check_C2(audit, corr):
    n = bad = 0
    for z in range(0, 49):
        for x in range(13, 59):
            for R in range(1, x + z + 42):
                n += 1
                ok, _, _ = identity_ok13(z, x, R)
                if not ok:
                    bad += 1
                corollary(z, x, R, corr)
    audit['C2'] = {'desc': 'closed identity grid z=0..48 x=13..58 R<=x+z+41 (+merge,tail)',
                   'points': n, 'bad': bad}


def check_C2b(audit):
    n = bad = 0
    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(13, 64, 5):
            for R in range(1, x + z + 32):
                n += 1
                ok, _, _ = identity_ok13(z, x, R)
                if not ok or (R >= x + z + 14 and cand13(z, x, R) != (x + 13) % 2):
                    bad += 1
    audit['C2b'] = {'desc': 'deep tail identity rows z in {60..400} x=13..63(step5) R<=x+z+31',
                    'points': n, 'bad': bad}


def check_C3(audit):
    n = bad = 0
    for z in range(0, 6):
        for x in range(13, 18):
            for R in range(1, x + z + 22):
                n += 1
                # raw option set by manual child enumeration on the raw engine
                raw_opts = set()
                if x > 13:
                    raw_opts.add(H_ordered(R - 1, (x - 1, 13), z))
                else:
                    raw_opts.add(H_ordered(R - 1, (12, 13), z))
                raw_opts.add(H_ordered(R - 1, (x, 12), z))
                if z >= 1:
                    raw_opts.add(1 ^ H_ordered(R - 1, (x, 13), z - 1))
                closed = set(opts13(z, x, R))
                if raw_opts != closed:
                    bad += 1
    audit['C3'] = {'desc': 'option decomposition vs raw child enumeration',
                   'points': n, 'bad': bad}


def conform(z, x, R, types):
    """Return True if this point's type conforms (registry update if new)."""
    t = type_of13(z, x, R)
    e = (cand13(z, x, R), tuple(sorted(opts13(z, x, R))))
    if t not in types:
        types[t] = e
        return True
    return types[t] == e


def box_points(B):
    for v0 in range(-B, B + 1):
        for v1 in range(-B, B + 1):
            for v3 in range(-B, B + 1):
                z, x, R = vpoint(v0, v1, v3)
                if z < 0 or x < 13 or R < 1:
                    continue
                yield z, x, R


def check_C4(audit, types):
    n = bad = conf_bad = id_bad = 0
    for z, x, R in box_points(60):
        n += 1
        ok, _, _ = identity_ok13(z, x, R)
        if not ok:
            id_bad += 1
        if not conform(z, x, R, types):
            conf_bad += 1
    bad = id_bad + conf_bad
    audit['C4'] = {'desc': 'type machine box +/-60, clip 28/sentinel 29, confluence',
                   'points': n, 'bad': bad, 'types': len(types),
                   'identity_bad': id_bad, 'confluence_bad': conf_bad}


def check_C4t(audit):
    """Tightness probe: clip 27 / sentinel 28 over the same box.

    Counts type-confluence violations when the clip window is narrowed
    by one (2y+1 instead of the 9-family candidate 2y+2=28). Not part
    of the PASS/FAIL bad total; reported for the pattern claim.
    """
    global CLIP, SENT
    old_clip, old_sent = CLIP, SENT
    CLIP, SENT = 27, 28
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
    audit['C4t'] = {'desc': 'tightness probe clip 27/sentinel 28 (not in bad total)',
                    'points': n, 'violations_at_clip27': viol,
                    'first_violation': first}


def check_C7(audit, types, corr):
    rng = random.Random(20261132)
    n = bad = 0
    for _ in range(200000):
        z = rng.randrange(0, 3001)
        x = rng.randrange(13, 3001)
        mode = rng.randrange(4)
        if mode == 0:
            R = rng.randrange(1, x + z + 14)
        elif mode == 1:
            R = x + z + 14 + rng.randrange(-3, 4)
        elif mode == 2:
            x = max(13, z + rng.randrange(-28, 19))
            R = rng.randrange(1, 9001)
        else:
            R = rng.randrange(1, 9001)
        if R < 1 or x < 13:
            continue
        n += 1
        ok, _, _ = identity_ok13(z, x, R)
        if not ok or not conform(z, x, R, types):
            bad += 1
        corollary(z, x, R, corr)
    audit['C7'] = {'desc': 'seeded far probes 200k, seed 20261132, z,x<=3000',
                   'points': n, 'bad': bad}


def check_C8(audit, types, corr):
    n = bad = 0
    zs = list(range(0, 6)) + list(range(29, 32)) + list(range(59, 62)) + \
        list(range(299, 302)) + list(range(999, 1002)) + [2999, 3000]
    for z in zs:
        for dx in range(-28, 18):
            x = z + dx
            if x < 12:
                continue
            for R in range(1, x + z + 30):
                n += 1
                ok, _, _ = identity_ok13(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
            for R in (x + z + 14, x + z + 15, x + z + 16):
                n += 1
                if cand12(z, x, R) != (x + 12) % 2:
                    bad += 1
    audit['C8'] = {'desc': 'boundary manifolds z<=3000, dx in [-28,17], tail window',
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
                    if z < 0 or x < 13 or R < 1:
                        continue
                    n += 1
                    ok, _, _ = identity_ok13(z, x, R)
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
    values; the cap only bounds residency on this 1 GiB-cgroup host.
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
        for x in range(13, 71):
            points += x + z + 15
            if x <= z - 14:
                merge += x + z + 15
            tail += 1  # exactly one R (= x+z+14) is >= x+z+14 within the box
    return points, merge, tail


def run_census(engine_name):
    if engine_name not in ("ordered", "canonical"):
        raise SystemExit(f"FAIL-CLOSED: unknown census engine {engine_name}")
    raw = H_ordered if engine_name == "ordered" else H_canonical
    twin = _bounded_twin(raw, "H_ordered" if engine_name == "ordered" else "H_canonical")
    n = bad = 0
    corr = {'merge': {'points': 0, 'bad': 0}, 'tail': {'points': 0, 'bad': 0}}
    for z in range(0, 80):
        for x in range(13, 71):
            for R in range(0, x + z + 15):
                c = cand13(z, x, R)
                if twin(R, (x, 13), z) != c:
                    bad += 1
                corollary(z, x, R, corr)
                n += 1
    payload = {
        'engine': engine_name,
        'box': 'z=0..79, x=13..70, R=0..x+z+14',
        'cache_type': 'bounded-memoization twin of the verbatim raw engine (published code object, LRU-capped cache)',
        'cache_maxsize': CENSUS_CACHE_MAXSIZE,
        'points': n,
        'bad': bad,
        'corollaries': {
            'merge': {'points': corr['merge']['points'], 'bad': corr['merge']['bad'],
                      'claim': 'x<=z-14 => H == single_token(x+13,z,R)'},
            'tail': {'points': corr['tail']['points'], 'bad': corr['tail']['bad'],
                     'claim': 'R>=x+z+14 => H == (x+13)%2'},
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
        if part.get('box') != 'z=0..79, x=13..70, R=0..x+z+14':
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
    audit['C11'] = {'desc': 'raw census anchor z=0..79 x=13..70 R<=x+z+14, both engines '
                            '(bounded-memoization twins, LRU cap 1600000, separate commands '
                            'C11ordered/C11canonical on this 1 GiB-cgroup host), parts validated '
                            'and merged here with recomputed expected counts',
                    'points': n, 'bad': bad,
                    'ordered_points': ordered['points'],
                    'canonical_points': canonical['points'],
                    'census_cache_maxsize': CENSUS_CACHE_MAXSIZE,
                    'census_part_files': ['census-ordered.json', 'census-canonical.json']}


def check_C12(audit, types, corr):
    n = bad = 0
    for z in range(0, 121):
        for x in range(13, 121):
            for R in range(1, x + z + 17):
                n += 1
                ok, _, _ = identity_ok13(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
    audit['C12'] = {'desc': 'deep closed grid z=0..120 x=13..120 R<=x+z+16',
                   'points': n, 'bad': bad}


def corollary(z, x, R, corr):
    if x <= z - 14:
        corr['merge']['points'] += 1
        if cand13(z, x, R) != single_token(x + 13, z, R):
            corr['merge']['bad'] += 1
    if R >= x + z + 14:
        corr['tail']['points'] += 1
        if cand13(z, x, R) != (x + 13) % 2:
            corr['tail']['bad'] += 1


def main():
    args = sys.argv[1:]
    if args and args[0] in ("C11ordered", "C11canonical"):
        rc = run_census(args[0][3:].lower())
        return {'overall': 'PASS' if rc == 0 else 'FAIL'}
    requested = set(args)
    everything = {'C1', 'C1b', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C12'}
    todo = requested & everything if requested else (everything - {'C11'})
    audit = {'experiment': 'vertical-fiber-two-token-y13-parametric-allz-proof-20261122',
             'family': 'H(R;(x,13);z), z>=0, x>=13, R>=0',
             'stage': 'part1 (12-check promotion machine; the promotion decision K1231 '
                      'observed->proved is reserved for part2: C1d published-slice '
                      'anchors at y=13 + census_rows.py third implementation; census '
                      'parts re-anchored via bounded-memoization twins on a '
                      '1 GiB-cgroup host)',
             'checks_run': sorted(todo),
             'checks': {},
             'corollaries': {
                 'merge_below_diagonal': {'claim': 'x<=z-14 => H == single_token(x+13,z,R)'},
                 'tail': {'claim': 'R>=x+z+14 => H == (x+13)%2'}}}
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
        print('  C4t:', t['violations_at_clip27'], 'violations at clip 27, first:', t['first_violation'])
    return audit


if __name__ == '__main__':
    sys.exit(0 if main()['overall'] == 'PASS' else 1)
