#!/usr/bin/env python3
"""Universal verifier for the y=12 two-token residual family (PART 1).

Family: H(R; (x,12); z), all z >= 0, all x >= 12, all R >= 0.
Claim under test (K1152, currently status "observed"; this machine is the
promotion-stage part 1): the closed form cand12 (T/P row tables below)
equals H everywhere; with corollaries
  merge-below-diagonal (y=12 promotion of the y=11 line): x <= z-13
       =>  H == single_token(x+12, z, R)
  tail:                                 R >= x+z+13  =>  H == (x+12) % 2

STAGE: part 1 (machine construction). Checks implemented and run here:
C1, C1b, C2, C2b, C3, C4 (clip window 2y+2 = 26, sentinel 27), C4t (clip
tightness probe 25/26), C7, C8, C9, C11, C12. C1d (published fixed-z
slice anchors specialised at y=12) and the census_rows.py duplication are
deferred to part 2, exactly as the y=10 and y=11 machines deferred their
C1d in part 1. K1152 is promoted observed -> proved only after part 2
completes and 3 byte-identical audit runs are recorded, per the procedure
that promoted y=5..y=10 (K1023/K1099/K1104/K1112/K1126/K1127/K1131/
K1135/K1138/K1141) and is pending for y=11 (K1143).

Run modes:
  python3 verify_y12_universal.py                 # all checks except C11
  python3 verify_y12_universal.py C11ordered      # census part 1 (slow)
  python3 verify_y12_universal.py C11canonical   # census part 2 (slow)
  python3 verify_y12_universal.py C11            # merge census parts, run all
  python3 verify_y12_universal.py C1 C2 ...       # explicit check list

  C1   raw order-preserving AND descending-canonical engines vs cand12,
       z=0..14, x=12..30, R=0..x+z+47
  C1b  single-token closed form (K0832) raw anchor; published y=11 closed
       form (K1143 transcription, the B-child of every y=12 point and the
       x=12 A-child) raw anchor; x=12 multiset merger (11,12)==(12,11)
       i.e. A==B child value raw anchor
  C2   closed-form identity grid z=0..48, x=12..57, R<=x+z+42 (+merge,tail)
  C2b  deep-tail identity rows z in {60,72,84,96,108,120,240,400},
       x in {12,17,...,62}, R <= x+z+31
  C3   option-decomposition raw anchor (child sets vs raw recursion)
  C4   type machine, clip window 2y+2 = 26 sentinel 27, free-coordinate
       box v0=x-z, v1=R-x, v3=R-x-z in +/-60: full sweep, per-type
       confluence of the (value, sorted-children) effect
  C4t  tightness probe: the same box at clip 25 counts confluence
       violations (informational, not part of the bad total) -- tests
       the 8-family continuation of the tight 2y+2 clip pattern
       (y=5..11: 12/14/16/18/20/22/24; 2y+2 for y=12 is 26)
  C7   fixed-seed far probes (seed 20261132): 200k points, z,x <= 3000,
       R <= 9000, tail window around x+z+13
  C8   boundary manifolds z in {0..5, 29..31, 59..61, 299..301,
       999..1001, 2999, 3000}, dx in [-26, 16], tail window
       [x+z+13, x+z+15]
  C9   v-space shell sweeps at radii [61,64], [89,92], [117,120]
  C11  raw census anchor z=0..79, x=12..70, R<=x+z+13, both engines,
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
  C12  deep closed grid z=0..120, x=12..120, R<=x+z+16

Trust boundary (same machine class as K1023/K1099/K1104/K1112/K1126/
K1127/K1131/K1135/K1138/K1141/K1143-part1): option decomposition +
closed-form mex identity + finite-type confluence over the
free-coordinate box, anchored to raw engines and to the published y=11
family (K1143 published fit, the B-child) and to the x=12 multiset
merger ((11,12)==(12,11)). The family law shifts carried from y=11 to
y=12 (even-y type: value-1 infinite band and tail on x odd rows; pin
lattice d==0 mod 4 (z odd, 6 rows) / d==2 mod 4 (z even, 6 rows, up
from 5 at y=11); sweep row d=13; steady pins z+24/z+25; band bottom
2y+2=26; tail x+z+13; merge x<=z-13; even-z diagonal without value 1;
z-odd I-row th(d)=ceil((d+37)/2) continuous-integer sweep 13..25 with
the pin slot th-1 alternating mod 4) are all inside the audited tables,
not assumed separately.

Published transcriptions inside this file:
  engines + K0832 single_token (raw engines H_ordered/H_canonical, the
  K0832 single-token closed form and its helpers): verbatim from the
  published verify_y11_universal.py (K1143 part-1 proof machine,
  SHA-256 c57baf5c5270c47ef9f29cc390a2d2eb6b18de438f576aa8f5e94264e3fd8c6b),
  whose own provenance chain is the published verify_y10_universal.py
  (K1141) and verify_y09_universal.py (K1138);
  cand11 (the B-child of every y=12 point and the x=12 merger child):
  verbatim from the published verify_y11_universal.py's cand11 block
  (block-local Y renamed to Y11 so the cand12 block can carry Y = 12;
  that block is itself the published cand11.py transcription minus the
  fit driver);
  cand12: verbatim from the published cand12.py (K1152 fit experiment,
  SHA-256 79e588b3d44bada83355676d9da1db559c57167574ed58ce118ef3c897149131),
  fit driver omitted (its probe self-check is K1152's own evidence,
  re-runnable there);
  the re-defined q_odd/single_token_val copies inside the cand11/cand12
  blocks are semantically identical to the shared body (last definition
  wins at call time, as in the published y=10/y=11 verifiers).
Their correctness is K0832/K1143/K1152's claim, not re-proven here; every
transcription is additionally re-anchored against the raw
order-preserving engine by this machine's C1/C1b, and cand11's y=12-scope
usage is inside its published fit domain (x >= 11, all z, all R).
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
# Published y=11 two-token closed form (K1143 published fit). This is the
# B-child of every y=12 point and the x=12 merger child value. Code block
# verbatim from the published verify_y11_universal.py's cand11 block
# (block-local Y renamed to Y11 so the cand12 block can carry Y = 12;
# that block is itself the published cand11.py transcription minus the
# fit driver).
# =====================================================================

Y11 = 11

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

def in_T11(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y11 - 1:
        S = x + Y11
        return R % 2 == 1 and R <= q_odd(S)
    d = x - z
    o = R - z
    if d == -Y11:
        cap = (z + Y11 - 1) if z % 2 == 1 else (z + Y11)
        if R % 2 == 1 and R <= (z if z % 2 == 1 else z - 1):
            return True
        if z % 2 == 1:
            return o % 2 == 0 and 2 <= o <= cap - z
        else:
            return o % 2 == 1 and 1 <= o <= cap - z
    if z % 2 == 1:
        ladder = R % 2 == 1 and R <= z
        if d % 4 == 3 and -11 <= d <= 11:
            pin = z + (d + 33) // 2
            if R == pin:
                return True
        if d == Y11 + 1:
            return ladder or (o % 2 == 0 and 2 * Y11 <= o <= x + Y11)
        if d >= Y11 + 2:
            return ladder or R == z + 2 * Y11
        return ladder
    else:
        ladder = R % 2 == 1 and R <= z - 1
        if d % 4 == 1 and -7 <= d <= 9:
            pin = z + (d + 33) // 2
            if R == pin:
                return True
        if d == Y11 + 1:
            return ladder or (o % 2 == 1 and 2 * Y11 + 1 <= o <= x + Y11)
        if d >= Y11 + 2:
            return ladder or R == z + 2 * Y11 + 1
        return ladder

def _bk(off, k):
    return 1 <= off <= 2 * k - 1 and off % 2 == 1

def in_P11(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y11 - 1:
        S = x + Y11
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    off = R - z
    b11 = _bk(off, Y11)
    band_base = off % 2 == 0 and 2 * Y11 + 2 <= off <= x + Y11          # steady base rows
    band_int = off % 2 == 0 and 2 * Y11 + 2 <= off <= x + Y11 - 1       # steady I rows
    tail = x % 2 == 0 and R >= x + z + Y11 + 1                          # S odd rows (y=11: x even)
    if z % 2 == 1:
        if -11 <= d <= 11 and d % 2 == 1:
            k = (d + 34) // 4          # I rows: b_k U I[2k+1)  (diag d=-11 included, k=5)
            return _bk(off, k) or off >= 2 * k + 1
        if d == Y11 + 1:
            return b11                 # sweep row, base type: z odd x odd
        if d >= Y11 + 2:
            if d % 2 == 0:
                return b11 or band_base
            return b11 or band_int or tail
        return _bk(off, (d + 34) // 4)  # base rows d even in [-10,10]
    else:
        if d == -Y11:
            return False                # even-z diagonal: no value-1 at all
        if d == Y11 + 1:
            return b11 or band_int or tail   # sweep row, I type: z even x even
        if d >= Y11 + 2:
            if d % 2 == 1:
                return b11 or band_base
            return b11 or band_int or tail
        if d % 2 == 0:
            k = (d + 32) // 4          # I rows: b_k U I[2k+1)
            return _bk(off, k) or off >= 2 * k + 1
        return _bk(off, (d + 34) // 4)  # base rows d odd in [-9,11]

def cand11(z, x, R):
    if R <= 0:
        return 0
    if in_T11(z, x, R):
        return 2
    if in_P11(z, x, R):
        return 1
    return 0


# =====================================================================
# Candidate under test: y=12 two-token closed form (K1152 published fit).
# cand12 tables verbatim from the published cand12.py (K1152 fit
# experiment); fit driver omitted. The y=11 family (cand11 block above) is
# the B-child of this identity and the x=12 merger child value.
# =====================================================================

Y = 12

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
        if d % 4 == 0 and -Y + 4 <= d <= Y:
            if R == z + (d + 3 * Y) // 2:
                return True
        if d == Y + 1:
            return ladder or (o % 2 == 0 and 2 * Y <= o <= x + Y)
        if d >= Y + 2:
            return ladder or R == z + 2 * Y
        return ladder
    else:
        ladder = R % 2 == 1 and R <= z - 1
        if d % 4 == 2 and -Y + 2 <= d <= Y - 2:
            if R == z + (d + 3 * Y) // 2:
                return True
        if d == Y + 1:
            return ladder or (o % 2 == 1 and 2 * Y + 1 <= o <= x + Y)
        if d >= Y + 2:
            return ladder or R == z + 2 * Y + 1
        return ladder

def _bk(off, k):
    return 1 <= off <= 2 * k - 1 and off % 2 == 1

def in_P12(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y - 1:
        S = x + Y
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    off = R - z
    b12 = _bk(off, Y)
    band = off % 2 == 0 and 2 * Y + 2 <= off <= x + Y
    tail = x % 2 == 1 and R >= x + z + Y + 1
    if z % 2 == 1:
        if -Y <= d <= Y and d % 2 == 0:
            k = (d + 38) // 4           # I rows (diag d=-12 and last pin d=12 included)
            th = 2 * k + (1 if d % 4 == 0 else 0)
            return _bk(off, k) or off >= th
        if -Y + 1 <= d <= Y - 1 and d % 2 == 1:
            return _bk(off, (d + 37) // 4)   # base rows
        if d == Y + 1:
            return b12              # sweep row is base-type (x even): band belongs to T
        return b12 or band or tail  # d >= Y+2 steady rows
    else:
        if d == -Y:
            return False            # even-z diagonal: no value-1 at all
        if -Y + 1 <= d <= Y - 1 and d % 2 == 1:
            k = (d + 35) // 4       # I rows: b_k U I[2k+1)
            return _bk(off, k) or off >= 2 * k + 1
        if -Y + 2 <= d <= Y and d % 2 == 0:
            return _bk(off, (d + 37) // 4)   # base rows
        return b12 or band or tail  # d >= Y+1 (sweep 13 included: x odd -> tail active)

def cand12(z, x, R):
    if R <= 0:
        return 0
    if in_T12(z, x, R):
        return 2
    if in_P12(z, x, R):
        return 1
    return 0


# ------------------------------------------------------------------
# Closed-form identity (option decomposition, no raw recursion).
# ------------------------------------------------------------------


def opts12(z, x, R):
    """Closed-form option values of H(R; (x,12); z). R >= 1.

    x == 12: both token-decrement children coincide as multisets:
    (11,12) == (12,11), both are the y=11 family row x=12.
    """
    if x == 12:
        A = cand11(z, 12, R - 1)
    else:
        A = cand12(z, x - 1, R - 1)
    out = [A, cand11(z, x, R - 1)]
    if z >= 1:
        out.append(1 ^ cand12(z - 1, x, R - 1))
    return out


def identity_ok12(z, x, R):
    t = in_T12(z, x, R)
    pv = in_P12(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    got = mex(opts12(z, x, R))
    want = cand12(z, x, R)
    return got == want, got, want


# ------------------------------------------------------------------
# Type machine. y=11's clip window (+/-24 sentinel +/-25) folded y=11
# features; the y=12 features (pins up to z+24 odd-z / z+25 even-z,
# sweep band d=13 offsets up to x+12, band bottom R-z = 2y+2 = 26,
# tail offset R-x-z = 13, base span to z+23 and the I-row
# th(d)=ceil((d+37)/2) excursions) are tested with +/-26/27 (= 2y+2
# for y=12), the 8-family-continuation candidate of the 2y+2 tight
# pattern (y=5..11: 12/14/16/18/20/22/24). CLIP/SENT are re-checked
# for confluence by check_C4; the tightness probe (CLIP=25) is
# reported separately (check_C4t).
# ------------------------------------------------------------------
CLIP, SENT = 26, 27


def clipw(w):
    if w > CLIP:
        return SENT
    if w < -CLIP:
        return -SENT
    return w


def type_of12(z, x, R):
    return (1 if x == 12 else 0,
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
        for x in range(12, 31):
            for R in range(0, x + z + 48):
                n += 1
                c = cand12(z, x, R)
                if H_ordered(R, (x, 12), z) != c or H_canonical(R, (x, 12), z) != c:
                    bad += 1
    audit['C1'] = {'desc': 'raw both engines vs cand12 z=0..14 x=12..30 R<=x+z+47',
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
    # (ii) published y=11 closed form (K1143, the B-child) raw anchor
    for z in range(0, 25):
        for x in range(11, 26):
            for R in range(0, x + z + 30):
                n += 1
                if H_ordered(R, (x, 11), z) != cand11(z, x, R):
                    bad += 1
    # (iii) x=12 multiset merger: (11,12) == (12,11) raw, and == cand11(z,12,R-1)
    for z in range(0, 31):
        for R in range(1, z + 42):
            n += 1
            a = H_ordered(R - 1, (11, 12), z)
            b = H_ordered(R - 1, (12, 11), z)
            c = H_canonical(R - 1, (11, 12), z)
            if a != b or a != c or a != cand11(z, 12, R - 1):
                bad += 1
    audit['C1b'] = {'desc': 'single_token/y=11-child/x=12 merger raw anchors',
                    'points': n, 'bad': bad}


def check_C2(audit, corr):
    n = bad = 0
    for z in range(0, 49):
        for x in range(12, 58):
            for R in range(1, x + z + 42):
                n += 1
                ok, _, _ = identity_ok12(z, x, R)
                if not ok:
                    bad += 1
                corollary(z, x, R, corr)
    audit['C2'] = {'desc': 'closed identity grid z=0..48 x=12..57 R<=x+z+41 (+merge,tail)',
                   'points': n, 'bad': bad}


def check_C2b(audit):
    n = bad = 0
    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(12, 63, 5):
            for R in range(1, x + z + 32):
                n += 1
                ok, _, _ = identity_ok12(z, x, R)
                if not ok or (R >= x + z + 13 and cand12(z, x, R) != (x + 12) % 2):
                    bad += 1
    audit['C2b'] = {'desc': 'deep tail identity rows z in {60..400} x=12..62(step5) R<=x+z+31',
                    'points': n, 'bad': bad}


def check_C3(audit):
    n = bad = 0
    for z in range(0, 6):
        for x in range(12, 17):
            for R in range(1, x + z + 22):
                n += 1
                # raw option set by manual child enumeration on the raw engine
                raw_opts = set()
                if x > 12:
                    raw_opts.add(H_ordered(R - 1, (x - 1, 12), z))
                else:
                    raw_opts.add(H_ordered(R - 1, (11, 12), z))
                raw_opts.add(H_ordered(R - 1, (x, 11), z))
                if z >= 1:
                    raw_opts.add(1 ^ H_ordered(R - 1, (x, 12), z - 1))
                closed = set(opts12(z, x, R))
                if raw_opts != closed:
                    bad += 1
    audit['C3'] = {'desc': 'option decomposition vs raw child enumeration',
                   'points': n, 'bad': bad}


def conform(z, x, R, types):
    """Return True if this point's type conforms (registry update if new)."""
    t = type_of12(z, x, R)
    e = (cand12(z, x, R), tuple(sorted(opts12(z, x, R))))
    if t not in types:
        types[t] = e
        return True
    return types[t] == e


def box_points(B):
    for v0 in range(-B, B + 1):
        for v1 in range(-B, B + 1):
            for v3 in range(-B, B + 1):
                z, x, R = vpoint(v0, v1, v3)
                if z < 0 or x < 12 or R < 1:
                    continue
                yield z, x, R


def check_C4(audit, types):
    n = bad = conf_bad = id_bad = 0
    for z, x, R in box_points(60):
        n += 1
        ok, _, _ = identity_ok12(z, x, R)
        if not ok:
            id_bad += 1
        if not conform(z, x, R, types):
            conf_bad += 1
    bad = id_bad + conf_bad
    audit['C4'] = {'desc': 'type machine box +/-60, clip 26/sentinel 27, confluence',
                   'points': n, 'bad': bad, 'types': len(types),
                   'identity_bad': id_bad, 'confluence_bad': conf_bad}


def check_C4t(audit):
    """Tightness probe: clip 25 / sentinel 26 over the same box.

    Counts type-confluence violations when the clip window is narrowed
    by one (2y+1 instead of the 8-family candidate 2y+2=26). Not part
    of the PASS/FAIL bad total; reported for the pattern claim.
    """
    global CLIP, SENT
    old_clip, old_sent = CLIP, SENT
    CLIP, SENT = 25, 26
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
    audit['C4t'] = {'desc': 'tightness probe clip 25/sentinel 26 (not in bad total)',
                    'points': n, 'violations_at_clip25': viol,
                    'first_violation': first}


def check_C7(audit, types, corr):
    rng = random.Random(20261132)
    n = bad = 0
    for _ in range(200000):
        z = rng.randrange(0, 3001)
        x = rng.randrange(12, 3001)
        mode = rng.randrange(4)
        if mode == 0:
            R = rng.randrange(1, x + z + 13)
        elif mode == 1:
            R = x + z + 13 + rng.randrange(-3, 4)
        elif mode == 2:
            x = max(12, z + rng.randrange(-26, 17))
            R = rng.randrange(1, 9001)
        else:
            R = rng.randrange(1, 9001)
        if R < 1 or x < 12:
            continue
        n += 1
        ok, _, _ = identity_ok12(z, x, R)
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
        for dx in range(-26, 17):
            x = z + dx
            if x < 12:
                continue
            for R in range(1, x + z + 29):
                n += 1
                ok, _, _ = identity_ok12(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
            for R in (x + z + 13, x + z + 14, x + z + 15):
                n += 1
                if cand12(z, x, R) != (x + 12) % 2:
                    bad += 1
    audit['C8'] = {'desc': 'boundary manifolds z<=3000, dx in [-26,16], tail window',
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
                    if z < 0 or x < 12 or R < 1:
                        continue
                    n += 1
                    ok, _, _ = identity_ok12(z, x, R)
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
        for x in range(12, 71):
            points += x + z + 14
            if x <= z - 13:
                merge += x + z + 14
            tail += 1  # exactly one R (= x+z+13) is >= x+z+13 within the box
    return points, merge, tail


def run_census(engine_name):
    if engine_name not in ("ordered", "canonical"):
        raise SystemExit(f"FAIL-CLOSED: unknown census engine {engine_name}")
    raw = H_ordered if engine_name == "ordered" else H_canonical
    twin = _bounded_twin(raw, "H_ordered" if engine_name == "ordered" else "H_canonical")
    n = bad = 0
    corr = {'merge': {'points': 0, 'bad': 0}, 'tail': {'points': 0, 'bad': 0}}
    for z in range(0, 80):
        for x in range(12, 71):
            for R in range(0, x + z + 14):
                c = cand12(z, x, R)
                if twin(R, (x, 12), z) != c:
                    bad += 1
                corollary(z, x, R, corr)
                n += 1
    payload = {
        'engine': engine_name,
        'box': 'z=0..79, x=12..70, R=0..x+z+13',
        'cache_type': 'bounded-memoization twin of the verbatim raw engine (published code object, LRU-capped cache)',
        'cache_maxsize': CENSUS_CACHE_MAXSIZE,
        'points': n,
        'bad': bad,
        'corollaries': {
            'merge': {'points': corr['merge']['points'], 'bad': corr['merge']['bad'],
                      'claim': 'x<=z-13 => H == single_token(x+12,z,R)'},
            'tail': {'points': corr['tail']['points'], 'bad': corr['tail']['bad'],
                     'claim': 'R>=x+z+13 => H == (x+12)%2'},
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
        if part.get('box') != 'z=0..79, x=12..70, R=0..x+z+13':
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
    audit['C11'] = {'desc': 'raw census anchor z=0..79 x=12..70 R<=x+z+13, both engines '
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
        for x in range(12, 121):
            for R in range(1, x + z + 17):
                n += 1
                ok, _, _ = identity_ok12(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
    audit['C12'] = {'desc': 'deep closed grid z=0..120 x=12..120 R<=x+z+16',
                   'points': n, 'bad': bad}


def corollary(z, x, R, corr):
    if x <= z - 13:
        corr['merge']['points'] += 1
        if cand12(z, x, R) != single_token(x + 12, z, R):
            corr['merge']['bad'] += 1
    if R >= x + z + 13:
        corr['tail']['points'] += 1
        if cand12(z, x, R) != (x + 12) % 2:
            corr['tail']['bad'] += 1


def main():
    args = sys.argv[1:]
    if args and args[0] in ("C11ordered", "C11canonical"):
        rc = run_census(args[0][3:].lower())
        return {'overall': 'PASS' if rc == 0 else 'FAIL'}
    requested = set(args)
    everything = {'C1', 'C1b', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C12'}
    todo = requested & everything if requested else (everything - {'C11'})
    audit = {'experiment': 'vertical-fiber-two-token-y12-parametric-allz-proof-20261120',
             'family': 'H(R;(x,12);z), z>=0, x>=12, R>=0',
             'stage': 'part1 (12-check machine constructed; census parts re-anchored via '
                      'bounded-memoization twins on a 1 GiB-cgroup host; C1d published-slice '
                      'anchors at y=12 and the census_rows.py duplication deferred to part 2; '
                      'K1152 stays observed until the full two-part procedure with 3 '
                      'byte-identical audit runs)',
             'checks_run': sorted(todo),
             'checks': {},
             'corollaries': {
                 'merge_below_diagonal': {'claim': 'x<=z-13 => H == single_token(x+12,z,R)'},
                 'tail': {'claim': 'R>=x+z+13 => H == (x+12)%2'}}}
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
        print('  C4t:', t['violations_at_clip25'], 'violations at clip 25, first:', t['first_violation'])
    return audit


if __name__ == '__main__':
    sys.exit(0 if main()['overall'] == 'PASS' else 1)
