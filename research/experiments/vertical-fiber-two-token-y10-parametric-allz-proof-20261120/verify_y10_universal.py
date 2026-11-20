#!/usr/bin/env python3
"""Universal verifier for the y=10 two-token residual family (PART 1).

Family: H(R; (x,10); z), all z >= 0, all x >= 10, all R >= 0.
Claim under test (K1141, currently status "observed"; this machine is the
promotion stage): the closed form cand10 (T/P row tables below) equals
H everywhere; with corollaries
  merge-below-diagonal (y=10 promotion of the y=9 line): x <= z-11
       =>  H == single_token(x+10, z, R)
  tail:                                 R >= x+z+11  =>  H == (x+10) % 2

STAGE: part 2 (promotion stage). Checks implemented and run here: C1,
C1b, C1d (published fixed-z slice anchors z = 8/9/10/15/16/17 specialised
at y=10, transcribed from the published K1000/K1001/K1011 (z=8/9/10,
y>=9) and K1065/K1077/K1087 (z=15/16/17, y>=6) uniform closed forms --
the y>=9 lines specialise the K0999/K1002 uniform candidates; part 1
deferred C1d to part 2), C2, C2b, C3, C4, C4t (clip tightness probe), C7,
C8, C9, C11 (optional, see "run modes"), C12. The census rows file
(census_rows.py, double-recursion row extraction) is published alongside
this machine as part 2. K1141 is promoted observed -> proved once this
full machine passes and 3 byte-identical runs are recorded, per the same
procedure that promoted y=5..y=9 (K1023/K1099/K1104/K1112/K1126/K1127/
K1131/K1135/K1138).

Run modes:
  python3 verify_y10_universal.py            # all checks except C11 (C1d included)
  python3 verify_y10_universal.py C11        # census check only (slow)
  python3 verify_y10_universal.py C1 C2 ...  # explicit check list

Trust boundary (same machine as K1023/K1099/K1104/K1112/K1126/K1127/
K1131/K1135/K1138): option decomposition + closed-form mex identity +
finite-type confluence over the free-coordinate box, anchored to raw
engines and to the published y=9 family (K1138, the B-child), to the
x=10 multiset merger ((9,10)==(10,9)), and (here, part 2) to the published
fixed-z slices specialised at y=10.

  C1   raw order-preserving AND descending-canonical engines vs cand10,
       z=0..14, x=10..29, R=0..x+z+46
  C1b  single-token closed form (K0832) raw anchor; published y=9 closed
       form (K1138 transcription) raw anchor; x=10 multiset merger
       (9,10)==(10,9) i.e. A==B child value raw anchor
  C2   closed-form identity grid z=0..48, x=10..56, R<=x+z+40 (+merge,tail)
  C2b  deep-tail identity rows z in {60,72,84,96,108,120,240,400},
       x in {10,15,...,60}, R <= x+z+30
  C3   option-decomposition raw anchor (child sets vs raw recursion)
  C4   type machine, clip window 2y+2 = 22 sentinel 23, free-coordinate
       box v0=x-z, v1=R-x, v3=R-x-z in +/-60: full sweep, per-type
       confluence of the (value, sorted-children) effect
  C4t  tightness probe: the same box at clip 21 counts confluence
       violations (informational, not part of the bad total) -- supports
       the 6-family continuation of the tight 2y+2 clip pattern
       (y=5..9: 12/14/16/18/20 all tight)
  C7   fixed-seed far probes (seed 20261130): 200k points, z,x <= 3000,
       R <= 9000, tail window around x+z+11
  C8   boundary manifolds z in {0..5, 29..31, 59..61, 299..301, 999..1001,
       2999, 3000}, dx in [-23, 14], tail window [x+z+11, x+z+13]
  C9   v-space shell sweeps at radii [61,64], [89,92], [117,120]
  C11  raw census anchor z=0..79, x=10..70, R<=x+z+12 (both engines; cache
       cleared engine-to-engine), plus merge/tail corollaries
  C12  deep closed grid z=0..120, x=10..120, R<=x+z+16

Published transcriptions inside this file:
  engine + single_token + cand9: verbatim from the published
  verify_y9_universal.py (K1138 proof experiment, SHA-256
  299acb6a70b9625310a3397a10f809879ba4a10a97e965115615d83f46c9171b);
  cand9 (in_T9/in_P9/cand9 with the fail-closed T/P-overlap assert) is the
  published K1138 verifier's copy, which the published y=10 machine
  pre-flight (machine-preflight experiment) proved semantically identical
  to the published K1138 fit cand9.py copy on 308,484 points (C1c there);
  cand10: verbatim from the published cand10.py (K1141 fit experiment,
  SHA-256 7c08e065d1278e9e90e4f748a2f7a8a6406318618ac06d259659233387427163),
  tables Y/q_odd/single_token_val/in_T10/_bk/in_P10/cand10, fit driver
  omitted (its probe self-check is K1141's own evidence, re-runnable there);
  the two published q_odd definitions have identical semantics (the last
  definition, from the cand10 block, is in effect at call time).
Their correctness is K0832/K1138/K1141's claim, not re-proven here; every
transcription was additionally pre-validated against the raw
order-preserving engine (K1141 fit for cand10; K1138 for cand9; this
machine's C1/C1b re-anchor them against both raw engines anyway).
Determinism: fixed seed, no clock, sorted audit keys, stable hash seeds.
"""
import hashlib
import json
import random
import sys
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


# ------------------------------------------------------------------
# Published y=9 two-token closed form (K1138, verbatim). cand9 is the
# B-child of the y=10 identity (decrement of the 10-token) and the x=10
# merger child value ((9,10)==(10,9)).
# ------------------------------------------------------------------
Y9 = 9


def in_T9(z, x, R):
    if R <= 0: return False
    if x <= z - Y9 - 1:
        return R % 2 == 1 and R <= q_odd(x + Y9)
    d = x - z
    if z % 2 == 1:
        if d == -Y9: return R % 2 == 1 and R <= z + Y9 - 1
        if d in (-7, -3, 1, 5, 9):
            pin = z + 2*Y9 + (d - Y9) // 2
            return (R % 2 == 1 and R <= z) or R == pin
        if d == Y9 + 1:
            return (R % 2 == 1 and R <= z) or (R % 2 == 1 and z + 2*Y9 <= R <= x + z + Y9)
        if d >= Y9 + 2:
            return (R % 2 == 1 and R <= z) or R == z + 2*Y9
        return R % 2 == 1 and R <= z
    else:
        if d == -Y9: return R % 2 == 1 and R <= z + Y9
        if d in (-5, -1, 3, 7, 11):
            pin = z + (d + 3*Y9) // 2
            return (R % 2 == 1 and R <= z - 1) or R == pin
        if d == Y9 + 1:
            return (R % 2 == 1 and R <= z - 1) or (R % 2 == 1 and z + 2*Y9 + 1 <= R <= x + z + Y9)
        if d >= Y9 + 2:
            return (R % 2 == 1 and R <= z - 1) or R == z + 2*Y9 + 1
        return R % 2 == 1 and R <= z - 1


def in_P9(z, x, R):
    if R <= 0: return False
    if x <= z - Y9 - 1:
        S = x + Y9
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    b4 = 1 <= R - z <= 9 and (R - z) % 2 == 1
    b5 = b4 or (R - z == 11)
    b6 = b5 or (R - z == 13)
    b7 = b6 or (R - z == 15)
    base9 = b7 or (R - z == 17)
    if z % 2 == 1:
        if d == -9: return b4 or R >= z + 10
        if d == -8: return b4
        if d == -7: return b5 or R >= z + 11
        if d == -6: return b4
        if d == -5: return b6 or R >= z + 12
        if d == -4: return b5
        if d == -3: return b6 or R >= z + 14
        if d == -2: return b5
        if d == -1: return b6 or R >= z + 14
        if d == 0:  return b6
        if d == 1:  return b7 or R >= z + 16
        if d == 2:  return b6
        if d == 3:  return b7 or R >= z + 16
        if d == 4:  return b7
        if d == 5:  return base9 or R >= z + 18
        if d == 6:  return b7
        if d == 7:  return base9 or R >= z + 18
        if d == 8:  return base9
        if d == 9:  return base9 or R == z + 19 or R >= z + 20
        if d == 10: return base9
        band = (z + 18 <= R <= x + z + Y9) and R % 2 == z % 2 and R != z + 2*Y9
        tail = x % 2 == 0 and R >= x + z + Y9 + 1
        return base9 or band or tail
    else:
        if d == -9: return False
        if d == -8: return b4 or R >= z + 9
        if d == -7: return b4
        if d == -6: return b5 or R >= z + 12
        if d == -5: return b4
        if d == -4: return b5 or R >= z + 12
        if d == -3: return b5
        if d == -2: return b6 or R >= z + 14
        if d == -1: return b5
        if d == 0:  return b6 or R >= z + 14
        if d == 1:  return b6
        if d == 2:  return b7 or R >= z + 16
        if d == 3:  return b6
        if d == 4:  return b7 or R >= z + 16
        if d == 5:  return b7
        if d == 6:  return base9 or R >= z + 18
        if d == 7:  return b7
        if d == 8:  return base9 or R >= z + 18
        if d == 9:  return base9
        if d == 10:
            band = (z + 2*Y9 + 2 <= R <= x + z + Y9) and R % 2 == z % 2
            tail = x % 2 == 0 and R >= x + z + Y9 + 1
            return base9 or band or tail
        band = (z + 2*Y9 + 2 <= R <= x + z + Y9) and R % 2 == z % 2
        tail = x % 2 == 0 and R >= x + z + Y9 + 1
        return base9 or band or tail


def cand9(z, x, R):
    t = in_T9(z, x, R)
    pv = in_P9(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    if R == 0:
        return 0
    if t:
        return 2
    return 1 if pv else 0

# =====================================================================
# Candidate under test: y=10 two-token closed form (K1141 published fit).
# cand10 tables verbatim from the published cand10.py (K1141 fit
# experiment). NOTE: the published file also defines q_odd with identical
# semantics (last definition wins at call time; the shared body is
# semantically identical in both published sources).
# =====================================================================
Y = 10

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

def in_T10(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y - 1:
        return R % 2 == 1 and R <= q_odd(x + Y)
    d = x - z
    if d == -Y:
        return R % 2 == 1 and R <= (z + Y if z % 2 == 1 else z + Y - 1)
    if z % 2 == 1:
        if d in (-7, -3, 1, 5, 9):
            # not a y=10 pin class; plain ladder (keep template explicit)
            return R % 2 == 1 and R <= z
        if d in (-6, -2, 2, 6, 10):
            pin = z + (d + 3 * Y) // 2
            return (R % 2 == 1 and R <= z) or R == pin
        if d == Y + 1:
            return (R % 2 == 1 and R <= z) or ((R - z) % 2 == 0 and z + 2 * Y <= R <= x + z + Y)
        if d >= Y + 2:
            return (R % 2 == 1 and R <= z) or R == z + 2 * Y
        return R % 2 == 1 and R <= z
    else:
        if d in (-9, -7, -5, -3, -1, 1, 3, 5, 7, 9):
            return R % 2 == 1 and R <= z - 1
        if d in (-8, -4, 0, 4, 8):
            pin = z + (d + 3 * Y) // 2
            return (R % 2 == 1 and R <= z - 1) or R == pin
        if d == -Y:  # handled above
            return R % 2 == 1 and R <= z + Y - 1
        if d == 10:
            return R % 2 == 1 and R <= z - 1
        if d == Y + 1:
            return (R % 2 == 1 and R <= z - 1) or (R % 2 == 1 and z + 2 * Y + 1 <= R <= x + z + Y)
        if d >= Y + 2:
            return (R % 2 == 1 and R <= z - 1) or R == z + 2 * Y + 1
        return R % 2 == 1 and R <= z - 1

def _bk(off, k):
    return 1 <= off <= 2 * k - 1 and off % 2 == 1

def in_P10(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y - 1:
        S = x + Y
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    off = R - z
    base10 = _bk(off, 10)
    band = (2 * Y + 2 <= off <= x + Y) and off % 2 == 0
    tail = x % 2 == 1 and R >= x + z + Y + 1
    if z % 2 == 1:
        # interval rows: d even; base th(d) zigzag
        if d == -10: return _bk(off, 6) or R >= z + 12
        if d == -9: return _bk(off, 5)
        if d == -8: return _bk(off, 6) or R >= z + 12
        if d == -7: return _bk(off, 6)
        if d == -6: return _bk(off, 7) or R >= z + 14
        if d == -5: return _bk(off, 6)
        if d == -4: return _bk(off, 7) or R >= z + 14
        if d == -3: return _bk(off, 7)
        if d == -2: return _bk(off, 8) or R >= z + 16
        if d == -1: return _bk(off, 7)
        if d == 0: return _bk(off, 8) or R >= z + 16
        if d == 1: return _bk(off, 8)
        if d == 2: return _bk(off, 9) or R >= z + 18
        if d == 3: return _bk(off, 8)
        if d == 4: return _bk(off, 9) or R >= z + 18
        if d == 5: return _bk(off, 9)
        if d == 6: return _bk(off, 10) or R >= z + 20
        if d == 7: return _bk(off, 9)
        if d == 8: return _bk(off, 10) or R >= z + 20
        if d == 9: return _bk(off, 10)
        if d == 10: return _bk(off, 10) or R >= z + 21  # pin offset 20 is value 2
        if d == 11: return base10  # sweep row: no value-1 beyond base
        return base10 or band or tail
    else:
        if d == -10: return False  # even-z diagonal: no value-1 at all
        if d == -9: return _bk(off, 6) or R >= z + 12
        if d == -8: return _bk(off, 5)
        if d == -7: return _bk(off, 6) or R >= z + 12
        if d == -6: return _bk(off, 6)
        if d == -5: return _bk(off, 7) or R >= z + 14
        if d == -4: return _bk(off, 6)
        if d == -3: return _bk(off, 7) or R >= z + 14
        if d == -2: return _bk(off, 7)
        if d == -1: return _bk(off, 8) or R >= z + 16
        if d == 0: return _bk(off, 7)
        if d == 1: return _bk(off, 8) or R >= z + 16
        if d == 2: return _bk(off, 8)
        if d == 3: return _bk(off, 9) or R >= z + 18
        if d == 4: return _bk(off, 8)
        if d == 5: return _bk(off, 9) or R >= z + 18
        if d == 6: return _bk(off, 9)
        if d == 7: return _bk(off, 10) or R >= z + 20
        if d == 8: return _bk(off, 9)
        if d == 9: return _bk(off, 10) or R >= z + 20
        if d == 10: return _bk(off, 10)
        return base10 or band or tail  # d >= 11 (sweep included)

def cand10(z, x, R):
    if R <= 0:
        return 0
    if in_T10(z, x, R):
        return 2
    if in_P10(z, x, R):
        return 1
    return 0


# ------------------------------------------------------------------
# Closed-form identity (option decomposition, no raw recursion).
# ------------------------------------------------------------------


def opts10(z, x, R):
    """Closed-form option values of H(R; (x,10); z). R >= 1.

    x == 10: both token-decrement children coincide as multisets:
    (9,10) == (10,9), both are the y=9 family row x=10.
    """
    if x == 10:
        A = cand9(z, 10, R - 1)
    else:
        A = cand10(z, x - 1, R - 1)
    out = [A, cand9(z, x, R - 1)]
    if z >= 1:
        out.append(1 ^ cand10(z - 1, x, R - 1))
    return out


def identity_ok10(z, x, R):
    got = mex(opts10(z, x, R))
    want = cand10(z, x, R)
    return got == want, got, want


# ------------------------------------------------------------------
# Type machine. y=9's clip window (+/-20 sentinel +/-21) folds y=9
# features; the y=10 features (pins up to z+20 odd-z / z+21 even-z,
# sweep band d=11 offsets up to x+10, band bottom R-z = 2y+2 = 22,
# tail offset R-x-z = 11, base span to z+19 and the d=10 row's
# I[z+21) excursion) are tested with +/-22/23 (= 2y+2 for y=10),
# the 6-family-continuation candidate of the 2y+2 tight pattern
# (y=5:12, y=6:14, y=7:16, y=8:18, y=9:20 all tight).
# CLIP/SENT are re-checked for confluence by check_C4; the
# tightness probe (CLIP=21) is reported separately (check_C4t).
# ------------------------------------------------------------------
CLIP, SENT = 22, 23


def clipw(w):
    if w > CLIP:
        return SENT
    if w < -CLIP:
        return -SENT
    return w


def type_of10(z, x, R):
    return (1 if x == 10 else 0,
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
        for x in range(10, 30):
            for R in range(0, x + z + 47):
                n += 1
                c = cand10(z, x, R)
                if H_ordered(R, (x, 10), z) != c or H_canonical(R, (x, 10), z) != c:
                    bad += 1
    audit['C1'] = {'desc': 'raw both engines vs cand10 z=0..14 x=10..29 R<=x+z+46',
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
    # (ii) published y=9 closed form (K1138, the B-child) raw anchor
    for z in range(0, 25):
        for x in range(9, 25):
            for R in range(0, x + z + 30):
                n += 1
                if H_ordered(R, (x, 9), z) != cand9(z, x, R):
                    bad += 1
    # (iii) x=10 multiset merger: (9,10) == (10,9) raw, and == cand9(z,10,R-1)
    for z in range(0, 31):
        for R in range(1, z + 39):
            n += 1
            a = H_ordered(R - 1, (9, 10), z)
            b = H_ordered(R - 1, (10, 9), z)
            c = H_canonical(R - 1, (9, 10), z)
            if a != b or a != c or a != cand9(z, 10, R - 1):
                bad += 1
    audit['C1b'] = {'desc': 'single_token/y=9-child/x=10 merger raw anchors',
                    'points': n, 'bad': bad}



# ------------------------------------------------------------------
# Published fixed-z slice anchors specialised at y=10 (C1d).
# Independent of the cand10 tables above. Uniform closed forms kept in
# their published parametric (x,y,r) form and evaluated at the y=10 row:
#   z=8:  K0999/K1000 uniform candidate, scope x>=y>=9
#         (verify_z8_y_ge9_proof.py, SHA-256 e88e5ea7...)
#   z=9:  K1001 uniform candidate, scope x>=y>=9
#         (verify_z9_y_ge9_proof.py, SHA-256 db1d60c6...)
#   z=10: K1002 uniform candidate restricted to y>=9 = the K1011 proof
#         scope (verify_z10_y_ge9_proof.py, SHA-256 42db00b2...)
#   z=15: K1065 uniform y>=6 family (verify_z15_y_ge6.py,
#         SHA-256 131e1c64...); the small-y transitional cells
#         (y,d) in {(6,0),(6,1),(6,2),(7,0),(6,3),(7,1)} are unreachable
#         at y=10, so the published generic rows apply as-is
#   z=16: K1077 uniform y>=6 family (verify_z16_y_ge6.py,
#         SHA-256 d07c3b0e...); unreachable transitional (y,d) cells
#         at y=10 likewise
#   z=17: K1087 uniform y>=6 family (verify_z17_y_ge6.py,
#         SHA-256 e49d24d2...); the S<17 / S==17 transitional branches
#         are unreachable at y=10 (S=x+10>=20)
# Every anchor was pre-validated against both raw engines at the y=10
# rows before incorporation (pre-flight box: z fixed, x=10..45,
# R<=x+z+30: 15,336 points, mismatch 0, both engines).
# ------------------------------------------------------------------


def _od(r, a, b):
    return r % 2 == 1 and a <= r <= b


def _ev(r, a, b):
    return r % 2 == 0 and a <= r <= b


def A8u(x, y, r):
    """K0999/K1000 published uniform form: H(R;(x,y);8), x>=y>=9."""
    if r == 0:
        return 0
    if r >= x + y + 9:
        return (x + y) % 2
    d = x - y
    t = (r in (1, 3, 5, 7) or
         (d == 2 and r == 2 * y + 5) or
         (d == 6 and r == 2 * y + 7) or
         (d == 9 and _od(r, 2 * y + 9, 2 * y + 17)) or
         (d >= 10 and r == 2 * y + 9))
    if t:
        return 2
    if d == 0:
        p = _od(r, 9, 2 * y + 3)
    elif d == 1:
        p = _od(r, 9, 2 * y + 9) or _ev(r, 2 * y + 6, 2 * y + 9)
    elif d == 2:
        p = _od(r, 9, 2 * y + 3)
    elif d == 3:
        p = _od(r, 9, 2 * y + 11) or _ev(r, 2 * y + 6, 2 * y + 11)
    elif d == 4:
        p = _od(r, 9, 2 * y + 5)
    elif d == 5:
        p = _od(r, 9, 2 * y + 13) or _ev(r, 2 * y + 8, 2 * y + 13)
    elif d == 6:
        p = _od(r, 9, 2 * y + 5)
    elif d == 7:
        p = _od(r, 9, 2 * y + 15) or _ev(r, 2 * y + 8, 2 * y + 15)
    elif d == 8:
        p = _od(r, 9, 2 * y + 7)
    elif d == 9:
        p = _od(r, 9, 2 * y + 7) or _ev(r, 2 * y + 10, 2 * y + 16)
    else:
        p = _od(r, 9, 2 * y + 7) or _ev(r, 2 * y + 10, x + y + 8)
    return 1 if p else 0


def A9u(x, y, r):
    """K1001 published uniform form: H(R;(x,y);9), x>=y>=9."""
    if r == 0:
        return 0
    if r >= x + y + 10:
        return (x + y) % 2
    d = x - y
    top = x + y + 9
    t = (r in (1, 3, 5, 7, 9) or
         (d == 1 and r == 2 * y + 5) or
         (d == 5 and r == 2 * y + 7) or
         (d == 9 and r == 2 * y + 9) or
         (d == 10 and _od(r, 2 * y + 9, 2 * y + 19)) or
         (d >= 11 and r == 2 * y + 9))
    if t:
        return 2
    if d == 10:
        p = _ev(r, 10, 2 * y + 8)
    elif d % 2 == 1:
        if d <= 3:
            p = _ev(r, 10, 2 * y + 6) or r >= 2 * y + 7
        elif d <= 7:
            p = _ev(r, 10, 2 * y + 8) or r >= 2 * y + 9
        elif d == 9:
            p = _ev(r, 10, 2 * y + 8) or r >= 2 * y + 10
        else:
            p = _ev(r, 10, 2 * y + 8) or _od(r, 2 * y + 11, top)
    else:
        if d <= 2:
            ht = 2 * y + 4
        elif d <= 6:
            ht = 2 * y + 6
        else:
            ht = 2 * y + 8
        if d >= 12:
            p = _ev(r, 10, ht) or _od(r, 2 * y + 11, top)
        else:
            p = _ev(r, 10, ht)
    return 1 if p else 0


def A10u(x, y, r):
    """K1002 uniform form restricted to y>=9 (K1011 proof scope):
    H(R;(x,y);10), x>=y>=9."""
    if r == 0:
        return 0
    S = x + y
    if r >= S + 11:
        return S % 2
    d = x - y
    t = (r in (1, 3, 5, 7, 9) or
         (d in (0, 4, 8) and r == 2 * y + 5 + d // 2) or
         (d == 11 and _od(r, 2 * y + 11, S + 10)) or
         (d >= 12 and r == 2 * y + 11))
    if t:
        return 2
    if d % 2 == 0 and d <= 10:
        p = _od(r, 11, 2 * y + 3 + 2 * ((d + 3) // 4))
    elif d % 2 == 0:
        p = _od(r, 11, 2 * y + 9) or _ev(r, 2 * y + 12, S + 10)
    elif d <= 9:
        p = _od(r, 11, S + 10) or _ev(r, 2 * y + 6 + 2 * ((d + 1) // 4), S + 9)
    else:
        p = _od(r, 11, 2 * y + 9) or _ev(r, 2 * y + 12, S + 9)
    return 1 if p else 0


def A15u(x, y, r):
    """K1065 published uniform form: H(R;(x,y);15), x>=y>=6.
    The (y,d) transitional cells are unreachable at y=10."""
    d = x - y
    Y = 2 * y
    S = x + y
    if r == 0:
        return 0
    if r >= S + 16:
        return S % 2
    t = (_od(r, 1, 15) or
         (d in (3, 7, 11, 15) and r == Y + (d + 15) // 2) or
         (d == 16 and _od(r, Y + 15, S + 15)) or
         (d >= 17 and r == Y + 15))
    if t:
        return 2
    if d % 2 == 0 and d <= 14:
        p = _ev(r, 16, Y + 6 + 2 * ((d + 3) // 4))
    elif d % 2 == 1 and d <= 15:
        p = (_ev(r, 16, S + 15) or _od(r, Y + 7 + 2 * ((d + 5) // 4), S + 14)
             or r >= S + 16)
    elif d == 16:
        p = _ev(r, 16, Y + 14)
    else:
        hi = S + (15 if d % 2 == 0 else 14)
        p = (_ev(r, 16, Y + 14) or _od(r, Y + 17, hi)
             or (d % 2 == 1 and r >= S + 16))
    return 1 if p else 0


def A16u(x, y, r):
    """K1077 published uniform form: H(R;(x,y);16), x>=y>=6.
    The (y,d) transitional cells are unreachable at y=10."""
    d = x - y
    Y = 2 * y
    S = x + y
    if r == 0:
        return 0
    if r >= S + 17:
        return S % 2
    t = (_od(r, 1, 15) or
         (d in (2, 6, 10, 14) and r == Y + (d + 16) // 2) or
         (d == 17 and _od(r, Y + 17, S + 16)) or
         (d >= 18 and r == Y + 17))
    if t:
        return 2
    if d % 2 == 0 and d <= 14:
        p = _od(r, 17, Y + 7 + 2 * (d // 4))
    elif d % 2 == 1 and d <= 15:
        p = (_od(r, 17, S + 16) or _ev(r, Y + 10 + 2 * ((d - 1) // 4), S + 15)
             or r >= S + 17)
    elif d == 16:
        p = _od(r, 17, Y + 15)
    elif d % 2 == 1:
        p = (_od(r, 17, Y + 15) or _ev(r, Y + 18, S + 15) or r >= S + 17)
    else:
        p = _od(r, 17, Y + 15) or _ev(r, Y + 18, S + 16)
    return 1 if p else 0


def A17u(x, y, r):
    """K1087 published uniform form: H(R;(x,y);17), x>=y>=6.
    T fully evaluated before P (value17 order); the S<17 and S==17
    transitional branches are unreachable at y=10 (S=x+10>=20)."""
    d = x - y
    Y = 2 * y
    S = x + y
    if r == 0:
        return 0
    if r >= S + 18:
        return S % 2
    if _od(r, 1, 17):
        return 2
    if d == 18 and _od(r, Y + 17, S + 17):
        return 2
    if d >= 19 and r == Y + 17:
        return 2
    if d % 2 == 1 and d % 4 == 1 and d <= 17 and r == Y + (d + 17) // 2:
        return 2
    if d >= 19:
        if _ev(r, 18, Y + 16):
            return 1
        if _od(r, Y + 19, S + 17):
            return 1
        if S % 2 == 1 and r >= S + 18:
            return 1
        return 0
    if d == 18:
        return 1 if _ev(r, 18, Y + 16) else 0
    if d % 2 == 1:
        rt = Y + (d + 17) // 2
        if d % 4 == 1:
            p = _ev(r, 18, rt - 1) or r >= rt + 1
        else:
            p = _ev(r, 18, rt - 2) or r >= rt
        return 1 if p else 0
    U = Y + 8 + 2 * (d // 4)
    return 1 if _ev(r, 18, U) else 0


def check_C1d(audit):
    n = bad = 0
    anchors = (8, A8u), (9, A9u), (10, A10u), (15, A15u), (16, A16u), (17, A17u)
    for z0, fn in anchors:
        for x in range(10, 160):
            for r in range(1, x + 62):
                n += 1
                if fn(x, 10, r) != cand10(z0, x, r):
                    bad += 1
    # published low-R single-token reduction of the fixed-z y>=6 slices
    # (R<=z+6) checked directly on the y=10 rows
    n_low = bad_low = 0
    for z0 in (15, 16, 17):
        for x in range(10, 160):
            for R in range(1, z0 + 7):
                n_low += 1
                if cand10(z0, x, R) != single_token(x + 10, z0, R):
                    bad_low += 1
    audit['C1d'] = {'desc': 'published z=8/9/10/15/16/17 uniform slices (y=10) vs cand10, x=10..159 R<=x+61; + low-R single-token reduction R<=z+6 (z=15..17)',
                    'points': n + n_low, 'bad': bad + bad_low,
                    'anchor_bad': bad, 'lowR_bad': bad_low}


def check_C2(audit, corr):
    n = bad = 0
    for z in range(0, 49):
        for x in range(10, 57):
            for R in range(1, x + z + 41):
                n += 1
                ok, _, _ = identity_ok10(z, x, R)
                if not ok:
                    bad += 1
                corollary(z, x, R, corr)
    audit['C2'] = {'desc': 'closed identity grid z=0..48 x=10..56 R<=x+z+40 (+merge,tail)',
                   'points': n, 'bad': bad}


def check_C2b(audit):
    n = bad = 0
    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(10, 63, 5):
            for R in range(1, x + z + 31):
                n += 1
                ok, _, _ = identity_ok10(z, x, R)
                if not ok or (R >= x + z + 11 and cand10(z, x, R) != (x + 10) % 2):
                    bad += 1
    audit['C2b'] = {'desc': 'deep tail identity rows z in {60..400} x=10..60(step5) R<=x+z+30',
                    'points': n, 'bad': bad}


def check_C3(audit):
    n = bad = 0
    for z in range(0, 6):
        for x in range(10, 15):
            for R in range(1, x + z + 22):
                n += 1
                # raw option set by manual child enumeration on the raw engine
                raw_opts = set()
                if x > 10:
                    raw_opts.add(H_ordered(R - 1, (x - 1, 10), z))
                else:
                    raw_opts.add(H_ordered(R - 1, (9, 10), z))
                raw_opts.add(H_ordered(R - 1, (x, 9), z))
                if z >= 1:
                    raw_opts.add(1 ^ H_ordered(R - 1, (x, 10), z - 1))
                closed = set(opts10(z, x, R))
                if raw_opts != closed:
                    bad += 1
    audit['C3'] = {'desc': 'option decomposition vs raw child enumeration',
                   'points': n, 'bad': bad}


def conform(z, x, R, types):
    """Return True if this point's type conforms (registry update if new)."""
    t = type_of10(z, x, R)
    e = (cand10(z, x, R), tuple(sorted(opts10(z, x, R))))
    if t not in types:
        types[t] = e
        return True
    return types[t] == e


def box_points(B):
    for v0 in range(-B, B + 1):
        for v1 in range(-B, B + 1):
            for v3 in range(-B, B + 1):
                z, x, R = vpoint(v0, v1, v3)
                if z < 0 or x < 10 or R < 1:
                    continue
                yield z, x, R


def check_C4(audit, types):
    n = bad = conf_bad = id_bad = 0
    for z, x, R in box_points(60):
        n += 1
        ok, _, _ = identity_ok10(z, x, R)
        if not ok:
            id_bad += 1
        if not conform(z, x, R, types):
            conf_bad += 1
    bad = id_bad + conf_bad
    audit['C4'] = {'desc': 'type machine box +/-60, clip 22/sentinel 23, confluence',
                   'points': n, 'bad': bad, 'types': len(types),
                   'identity_bad': id_bad, 'confluence_bad': conf_bad}


def check_C4t(audit):
    """Tightness probe: clip 21 / sentinel 22 over the same box.

    Counts type-confluence violations when the clip window is narrowed
    by one (2y+1 instead of the 6-family candidate 2y+2=22). Not part
    of the PASS/FAIL bad total; reported for the pattern claim.
    """
    global CLIP, SENT
    old_clip, old_sent = CLIP, SENT
    CLIP, SENT = 21, 22
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
    audit['C4t'] = {'desc': 'tightness probe clip 21/sentinel 22 (not in bad total)',
                    'points': n, 'violations_at_clip21': viol,
                    'first_violation': first}


def check_C7(audit, types, corr):
    rng = random.Random(20261130)
    n = bad = 0
    for _ in range(200000):
        z = rng.randrange(0, 3001)
        x = rng.randrange(10, 3001)
        mode = rng.randrange(4)
        if mode == 0:
            R = rng.randrange(1, x + z + 11)
        elif mode == 1:
            R = x + z + 11 + rng.randrange(-3, 4)
        elif mode == 2:
            x = max(10, z + rng.randrange(-23, 16))
            R = rng.randrange(1, 9001)
        else:
            R = rng.randrange(1, 9001)
        if R < 1 or x < 10:
            continue
        n += 1
        ok, _, _ = identity_ok10(z, x, R)
        if not ok or not conform(z, x, R, types):
            bad += 1
        corollary(z, x, R, corr)
    audit['C7'] = {'desc': 'seeded far probes 200k, seed 20261130, z,x<=3000',
                   'points': n, 'bad': bad}


def check_C8(audit, types, corr):
    n = bad = 0
    zs = list(range(0, 6)) + list(range(29, 32)) + list(range(59, 62)) + \
        list(range(299, 302)) + list(range(999, 1002)) + [2999, 3000]
    for z in zs:
        for dx in range(-23, 15):
            x = z + dx
            if x < 10:
                continue
            for R in range(1, x + z + 29):
                n += 1
                ok, _, _ = identity_ok10(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
            for R in (x + z + 11, x + z + 12, x + z + 13):
                n += 1
                if cand10(z, x, R) != (x + 10) % 2:
                    bad += 1
    audit['C8'] = {'desc': 'boundary manifolds z<=3000, dx in [-23,14], tail window',
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
                    if z < 0 or x < 10 or R < 1:
                        continue
                    n += 1
                    ok, _, _ = identity_ok10(z, x, R)
                    if not ok or not conform(z, x, R, types):
                        bad += 1
    audit['C9'] = {'desc': 'v-space shell sweeps [61,64],[89,92],[117,120]',
                   'points': n, 'bad': bad}


def check_C11(audit, corr):
    n = bad = 0
    for engine in (H_ordered, H_canonical):
        for z in range(0, 80):
            for x in range(10, 71):
                for R in range(0, x + z + 13):
                    c = cand10(z, x, R)
                    if engine(R, (x, 10), z) != c:
                        bad += 1
                    corollary(z, x, R, corr)
                    n += 1
        engine.cache_clear()
    audit['C11'] = {'desc': 'raw census anchor z=0..79 x=10..70 R<=x+z+12, both engines',
                    'points': n, 'bad': bad}


def check_C12(audit, types, corr):
    n = bad = 0
    for z in range(0, 121):
        for x in range(10, 121):
            for R in range(1, x + z + 17):
                n += 1
                ok, _, _ = identity_ok10(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
    audit['C12'] = {'desc': 'deep closed grid z=0..120 x=10..120 R<=x+z+16',
                    'points': n, 'bad': bad}


def corollary(z, x, R, corr):
    if x <= z - 11:
        corr['merge']['points'] += 1
        if cand10(z, x, R) != single_token(x + 10, z, R):
            corr['merge']['bad'] += 1
    if R >= x + z + 11:
        corr['tail']['points'] += 1
        if cand10(z, x, R) != (x + 10) % 2:
            corr['tail']['bad'] += 1


def main():
    requested = set(sys.argv[1:])
    everything = {'C1', 'C1b', 'C1d', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C12'}
    todo = requested & everything if requested else (everything - {'C11'})
    audit = {'experiment': 'vertical-fiber-two-token-y10-parametric-allz-proof-20261120',
             'family': 'H(R;(x,10);z), z>=0, x>=10, R>=0',
             'stage': 'part2 (all check machines incl. C1d published-slice anchors and the C11 raw census anchor PASS; census_rows.py published alongside; promotion of K1141 observed->proved on this basis)',
             'checks_run': sorted(todo),
             'checks': {},
             'corollaries': {
                 'merge_below_diagonal': {'claim': 'x<=z-11 => H == single_token(x+10,z,R)'},
                 'tail': {'claim': 'R>=x+z+11 => H == (x+10)%2'}}}
    corr = {'merge': {'points': 0, 'bad': 0}, 'tail': {'points': 0, 'bad': 0}}
    types = {}

    for name in ('C1', 'C1b', 'C1d', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C12'):
        if name not in todo:
            continue
        if name == 'C1':
            check_C1(audit['checks'])
        elif name == 'C1b':
            check_C1b(audit['checks'])
        elif name == 'C1d':
            check_C1d(audit['checks'])
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
        print('  C4t:', t['violations_at_clip21'], 'violations at clip 21, first:', t['first_violation'])
    return audit


if __name__ == '__main__':
    sys.exit(0 if main()['overall'] == 'PASS' else 1)
