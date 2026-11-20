#!/usr/bin/env python3
"""Universal verifier for the y=11 two-token residual family (PART 1).

Family: H(R; (x,11); z), all z >= 0, all x >= 11, all R >= 0.
Claim under test (K1143, currently status "observed"; this machine is the
promotion-stage part 1): the closed form cand11 (T/P row tables below)
equals H everywhere; with corollaries
  merge-below-diagonal (y=11 promotion of the y=10 line): x <= z-12
       =>  H == single_token(x+11, z, R)
  tail:                                 R >= x+z+12  =>  H == (x+11) % 2

STAGE: part 1 (machine construction). Checks implemented and run here:
C1, C1b, C2, C2b, C3, C4 (clip window 2y+2 = 24, sentinel 25), C4t (clip
tightness probe 23/24), C7, C8, C9, C11, C12. C1d (published fixed-z
slice anchors z = 8/9/10/15/16/17 specialised at y=11 -- the K0999/K1000/
K1001/K1011/K1065/K1077/K1087 uniform closed forms, whose scopes x>=y>=9
resp. x>=y>=6 all include y=11) and the census_rows.py duplication are
deferred to part 2, exactly as the y=10 machine deferred its C1d in
part 1. K1143 is promoted observed -> proved only after part 2 completes
and 3 byte-identical audit runs are recorded, per the procedure that
promoted y=5..y=10 (K1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/
K1138/K1141).

Run modes:
  python3 verify_y11_universal.py            # all checks except C11
  python3 verify_y11_universal.py C11        # census check only (slow)
  python3 verify_y11_universal.py C1 C2 ...  # explicit check list

  C1   raw order-preserving AND descending-canonical engines vs cand11,
       z=0..14, x=11..29, R=0..x+z+46
  C1b  single-token closed form (K0832) raw anchor; published y=10 closed
       form (K1141 transcription, the B-child of every y=11 point and the
       x=11 A-child) raw anchor; x=11 multiset merger (10,11)==(11,10)
       i.e. A==B child value raw anchor
  C2   closed-form identity grid z=0..48, x=11..56, R<=x+z+40 (+merge,tail)
  C2b  deep-tail identity rows z in {60,72,84,96,108,120,240,400},
       x in {11,16,...,61}, R <= x+z+30
  C3   option-decomposition raw anchor (child sets vs raw recursion)
  C4   type machine, clip window 2y+2 = 24 sentinel 25, free-coordinate
       box v0=x-z, v1=R-x, v3=R-x-z in +/-60: full sweep, per-type
       confluence of the (value, sorted-children) effect
  C4t  tightness probe: the same box at clip 23 counts confluence
       violations (informational, not part of the bad total) -- tests
       the 7-family continuation of the tight 2y+2 clip pattern
       (y=5..10: 12/14/16/18/20/22 all tight; 2y+2 for y=11 is 24)
  C7   fixed-seed far probes (seed 20261131): 200k points, z,x <= 3000,
       R <= 9000, tail window around x+z+12
  C8   boundary manifolds z in {0..5, 29..31, 59..61, 299..301, 999..1001,
       2999, 3000}, dx in [-24, 15], tail window [x+z+12, x+z+14]
  C9   v-space shell sweeps at radii [61,64], [89,92], [117,120]
  C11  raw census anchor z=0..79, x=11..70, R<=x+z+12 (both engines; cache
       cleared engine-to-engine), plus merge/tail corollaries
  C12  deep closed grid z=0..120, x=11..120, R<=x+z+16

Trust boundary (same machine as K1023/K1099/K1104/K1112/K1126/K1127/
K1131/K1135/K1138/K1141): option decomposition + closed-form mex identity
+ finite-type confluence over the free-coordinate box, anchored to raw
engines and to the published y=10 family (K1141, the B-child) and to the
x=11 multiset merger ((10,11)==(11,10)). The family law shifts carried
from y=10 to y=11 (S parity flip to the odd-y type: value-1 infinite
band and tail on x even rows; pin lattice d==3 mod 4 (z odd, 6 rows) /
d==1 mod 4 (z even, 5 rows); sweep row d=12; steady pins z+22/z+23;
band bottom 2y+2=24; tail x+z+12; merge x<=z-12; even-z diagonal without
value 1) are all inside the audited tables, not assumed separately.

Published transcriptions inside this file:
  engine + K0832 single_token: verbatim from the published
  verify_y10_universal.py (K1141 proof experiment, SHA-256
  f9169449309dcd25aaba8d6379d4289167f61eb3895b031e45ff9e80c46c05e4);
  cand10: verbatim from the same published verifier (its own cand10
  block: published K1141 fit tables; the block-local name Y is renamed
  to Y10 so the cand11 block can carry its own Y = 11; no other change);
  cand11: verbatim from the published cand11.py (K1143 fit experiment,
  SHA-256 8a083400d2b7690aee6fbaa75ace4d118b21f284e7f42af425a2c0f5fea7829b),
  fit driver omitted (its probe self-check is K1143's own evidence,
  re-runnable there);
  the re-defined q_odd/single_token_val copies inside the cand10/cand11
  blocks are semantically identical to the shared body (last definition
  wins at call time, as in the published y=10 verifier).
Their correctness is K0832/K1141/K1143's claim, not re-proven here; every
transcription is additionally re-anchored against the raw order-preserving
engine by this machine's C1/C1b, and cand10's y=11-scope usage is inside
its published proved domain (x >= 10, all z, all R).
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



# =====================================================================
# Published y=10 two-token closed form (K1141, proved). cand10 is the
# B-child of the y=11 identity (decrement of the 11-token -> (x,10)) and
# the x=11 merger child value ((10,11)==(11,10)). Verbatim from the
# published verify_y10_universal.py saver block; the block-local Y is
# renamed Y10 (the cand11 block below carries Y = 11).
# =====================================================================
Y10 = 10

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
    if x <= z - Y10 - 1:
        return R % 2 == 1 and R <= q_odd(x + Y10)
    d = x - z
    if d == -Y10:
        return R % 2 == 1 and R <= (z + Y10 if z % 2 == 1 else z + Y10 - 1)
    if z % 2 == 1:
        if d in (-7, -3, 1, 5, 9):
            # not a y=10 pin class; plain ladder (keep template explicit)
            return R % 2 == 1 and R <= z
        if d in (-6, -2, 2, 6, 10):
            pin = z + (d + 3 * Y10) // 2
            return (R % 2 == 1 and R <= z) or R == pin
        if d == Y10 + 1:
            return (R % 2 == 1 and R <= z) or ((R - z) % 2 == 0 and z + 2 * Y10 <= R <= x + z + Y10)
        if d >= Y10 + 2:
            return (R % 2 == 1 and R <= z) or R == z + 2 * Y10
        return R % 2 == 1 and R <= z
    else:
        if d in (-9, -7, -5, -3, -1, 1, 3, 5, 7, 9):
            return R % 2 == 1 and R <= z - 1
        if d in (-8, -4, 0, 4, 8):
            pin = z + (d + 3 * Y10) // 2
            return (R % 2 == 1 and R <= z - 1) or R == pin
        if d == -Y10:  # handled above
            return R % 2 == 1 and R <= z + Y10 - 1
        if d == 10:
            return R % 2 == 1 and R <= z - 1
        if d == Y10 + 1:
            return (R % 2 == 1 and R <= z - 1) or (R % 2 == 1 and z + 2 * Y10 + 1 <= R <= x + z + Y10)
        if d >= Y10 + 2:
            return (R % 2 == 1 and R <= z - 1) or R == z + 2 * Y10 + 1
        return R % 2 == 1 and R <= z - 1

def _bk(off, k):
    return 1 <= off <= 2 * k - 1 and off % 2 == 1

def in_P10(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y10 - 1:
        S = x + Y10
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    off = R - z
    base10 = _bk(off, 10)
    band = (2 * Y10 + 2 <= off <= x + Y10) and off % 2 == 0
    tail = x % 2 == 1 and R >= x + z + Y10 + 1
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



# =====================================================================
# Candidate under test: y=11 two-token closed form (K1143 published fit).
# cand11 tables verbatim from the published cand11.py (K1143 fit
# experiment); fit driver omitted.
# ===================================================================== 
Y = 11

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
        if d % 4 == 3 and -11 <= d <= 11:
            pin = z + (d + 33) // 2
            if R == pin:
                return True
        if d == Y + 1:
            return ladder or (o % 2 == 0 and 2 * Y <= o <= x + Y)
        if d >= Y + 2:
            return ladder or R == z + 2 * Y
        return ladder
    else:
        ladder = R % 2 == 1 and R <= z - 1
        if d % 4 == 1 and -7 <= d <= 9:
            pin = z + (d + 33) // 2
            if R == pin:
                return True
        if d == Y + 1:
            return ladder or (o % 2 == 1 and 2 * Y + 1 <= o <= x + Y)
        if d >= Y + 2:
            return ladder or R == z + 2 * Y + 1
        return ladder

def _bk(off, k):
    return 1 <= off <= 2 * k - 1 and off % 2 == 1

def in_P11(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y - 1:
        S = x + Y
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    off = R - z
    b11 = _bk(off, Y)
    band_base = off % 2 == 0 and 2 * Y + 2 <= off <= x + Y          # steady base rows
    band_int = off % 2 == 0 and 2 * Y + 2 <= off <= x + Y - 1       # steady I rows
    tail = x % 2 == 0 and R >= x + z + Y + 1                          # S odd rows (y=11: x even)
    if z % 2 == 1:
        if -11 <= d <= 11 and d % 2 == 1:
            k = (d + 34) // 4          # I rows: b_k U I[2k+1)  (diag d=-11 included, k=5)
            return _bk(off, k) or off >= 2 * k + 1
        if d == Y + 1:
            return b11                 # sweep row, base type: z odd x odd
        if d >= Y + 2:
            if d % 2 == 0:
                return b11 or band_base
            return b11 or band_int or tail
        return _bk(off, (d + 34) // 4)  # base rows d even in [-10,10]
    else:
        if d == -Y:
            return False                # even-z diagonal: no value-1 at all
        if d == Y + 1:
            return b11 or band_int or tail   # sweep row, I type: z even x even
        if d >= Y + 2:
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


# ------------------------------------------------------------------
# Closed-form identity (option decomposition, no raw recursion).
# ------------------------------------------------------------------


def opts11(z, x, R):
    """Closed-form option values of H(R; (x,11); z). R >= 1.

    x == 11: both token-decrement children coincide as multisets:
    (10,11) == (11,10), both are the y=10 family row x=11.
    """
    if x == 11:
        A = cand10(z, 11, R - 1)
    else:
        A = cand11(z, x - 1, R - 1)
    out = [A, cand10(z, x, R - 1)]
    if z >= 1:
        out.append(1 ^ cand11(z - 1, x, R - 1))
    return out


def identity_ok11(z, x, R):
    t = in_T11(z, x, R)
    pv = in_P11(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    got = mex(opts11(z, x, R))
    want = cand11(z, x, R)
    return got == want, got, want


# ------------------------------------------------------------------
# Type machine. y=10's clip window (+/-22 sentinel +/-23) folded y=10
# features; the y=11 features (pins up to z+22 odd-z / z+23 even-z,
# sweep band d=12 offsets up to x+11, band bottom R-z = 2y+2 = 24,
# tail offset R-x-z = 12, base span to z+21 and the d=11 row's
# I[2k+1) excursions) are tested with +/-24/25 (= 2y+2 for y=11),
# the 7-family-continuation candidate of the 2y+2 tight pattern
# (y=5:12, y=6:14, y=7:16, y=8:18, y=9:20, y=10:22 all tight).
# CLIP/SENT are re-checked for confluence by check_C4; the
# tightness probe (CLIP=23) is reported separately (check_C4t).
# ------------------------------------------------------------------
CLIP, SENT = 24, 25


def clipw(w):
    if w > CLIP:
        return SENT
    if w < -CLIP:
        return -SENT
    return w


def type_of11(z, x, R):
    return (1 if x == 11 else 0,
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
        for x in range(11, 30):
            for R in range(0, x + z + 47):
                n += 1
                c = cand11(z, x, R)
                if H_ordered(R, (x, 11), z) != c or H_canonical(R, (x, 11), z) != c:
                    bad += 1
    audit['C1'] = {'desc': 'raw both engines vs cand11 z=0..14 x=11..29 R<=x+z+46',
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
    # (ii) published y=10 closed form (K1141, the B-child) raw anchor
    for z in range(0, 25):
        for x in range(10, 26):
            for R in range(0, x + z + 30):
                n += 1
                if H_ordered(R, (x, 10), z) != cand10(z, x, R):
                    bad += 1
    # (iii) x=11 multiset merger: (10,11) == (11,10) raw, and == cand10(z,11,R-1)
    for z in range(0, 31):
        for R in range(1, z + 41):
            n += 1
            a = H_ordered(R - 1, (10, 11), z)
            b = H_ordered(R - 1, (11, 10), z)
            c = H_canonical(R - 1, (10, 11), z)
            if a != b or a != c or a != cand10(z, 11, R - 1):
                bad += 1
    audit['C1b'] = {'desc': 'single_token/y=10-child/x=11 merger raw anchors',
                    'points': n, 'bad': bad}


def check_C2(audit, corr):
    n = bad = 0
    for z in range(0, 49):
        for x in range(11, 57):
            for R in range(1, x + z + 41):
                n += 1
                ok, _, _ = identity_ok11(z, x, R)
                if not ok:
                    bad += 1
                corollary(z, x, R, corr)
    audit['C2'] = {'desc': 'closed identity grid z=0..48 x=11..56 R<=x+z+40 (+merge,tail)',
                   'points': n, 'bad': bad}


def check_C2b(audit):
    n = bad = 0
    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(11, 63, 5):
            for R in range(1, x + z + 31):
                n += 1
                ok, _, _ = identity_ok11(z, x, R)
                if not ok or (R >= x + z + 12 and cand11(z, x, R) != (x + 11) % 2):
                    bad += 1
    audit['C2b'] = {'desc': 'deep tail identity rows z in {60..400} x=11..61(step5) R<=x+z+30',
                    'points': n, 'bad': bad}


def check_C3(audit):
    n = bad = 0
    for z in range(0, 6):
        for x in range(11, 16):
            for R in range(1, x + z + 22):
                n += 1
                # raw option set by manual child enumeration on the raw engine
                raw_opts = set()
                if x > 11:
                    raw_opts.add(H_ordered(R - 1, (x - 1, 11), z))
                else:
                    raw_opts.add(H_ordered(R - 1, (10, 11), z))
                raw_opts.add(H_ordered(R - 1, (x, 10), z))
                if z >= 1:
                    raw_opts.add(1 ^ H_ordered(R - 1, (x, 11), z - 1))
                closed = set(opts11(z, x, R))
                if raw_opts != closed:
                    bad += 1
    audit['C3'] = {'desc': 'option decomposition vs raw child enumeration',
                   'points': n, 'bad': bad}


def conform(z, x, R, types):
    """Return True if this point's type conforms (registry update if new)."""
    t = type_of11(z, x, R)
    e = (cand11(z, x, R), tuple(sorted(opts11(z, x, R))))
    if t not in types:
        types[t] = e
        return True
    return types[t] == e


def box_points(B):
    for v0 in range(-B, B + 1):
        for v1 in range(-B, B + 1):
            for v3 in range(-B, B + 1):
                z, x, R = vpoint(v0, v1, v3)
                if z < 0 or x < 11 or R < 1:
                    continue
                yield z, x, R


def check_C4(audit, types):
    n = bad = conf_bad = id_bad = 0
    for z, x, R in box_points(60):
        n += 1
        ok, _, _ = identity_ok11(z, x, R)
        if not ok:
            id_bad += 1
        if not conform(z, x, R, types):
            conf_bad += 1
    bad = id_bad + conf_bad
    audit['C4'] = {'desc': 'type machine box +/-60, clip 24/sentinel 25, confluence',
                   'points': n, 'bad': bad, 'types': len(types),
                   'identity_bad': id_bad, 'confluence_bad': conf_bad}


def check_C4t(audit):
    """Tightness probe: clip 23 / sentinel 24 over the same box.

    Counts type-confluence violations when the clip window is narrowed
    by one (2y+1 instead of the 7-family candidate 2y+2=24). Not part
    of the PASS/FAIL bad total; reported for the pattern claim.
    """
    global CLIP, SENT
    old_clip, old_sent = CLIP, SENT
    CLIP, SENT = 23, 24
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
    audit['C4t'] = {'desc': 'tightness probe clip 23/sentinel 24 (not in bad total)',
                    'points': n, 'violations_at_clip23': viol,
                    'first_violation': first}


def check_C7(audit, types, corr):
    rng = random.Random(20261131)
    n = bad = 0
    for _ in range(200000):
        z = rng.randrange(0, 3001)
        x = rng.randrange(11, 3001)
        mode = rng.randrange(4)
        if mode == 0:
            R = rng.randrange(1, x + z + 12)
        elif mode == 1:
            R = x + z + 12 + rng.randrange(-3, 4)
        elif mode == 2:
            x = max(11, z + rng.randrange(-24, 16))
            R = rng.randrange(1, 9001)
        else:
            R = rng.randrange(1, 9001)
        if R < 1 or x < 11:
            continue
        n += 1
        ok, _, _ = identity_ok11(z, x, R)
        if not ok or not conform(z, x, R, types):
            bad += 1
        corollary(z, x, R, corr)
    audit['C7'] = {'desc': 'seeded far probes 200k, seed 20261131, z,x<=3000',
                   'points': n, 'bad': bad}


def check_C8(audit, types, corr):
    n = bad = 0
    zs = list(range(0, 6)) + list(range(29, 32)) + list(range(59, 62)) + \
        list(range(299, 302)) + list(range(999, 1002)) + [2999, 3000]
    for z in zs:
        for dx in range(-24, 16):
            x = z + dx
            if x < 11:
                continue
            for R in range(1, x + z + 29):
                n += 1
                ok, _, _ = identity_ok11(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
            for R in (x + z + 12, x + z + 13, x + z + 14):
                n += 1
                if cand11(z, x, R) != (x + 11) % 2:
                    bad += 1
    audit['C8'] = {'desc': 'boundary manifolds z<=3000, dx in [-24,15], tail window',
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
                    if z < 0 or x < 11 or R < 1:
                        continue
                    n += 1
                    ok, _, _ = identity_ok11(z, x, R)
                    if not ok or not conform(z, x, R, types):
                        bad += 1
    audit['C9'] = {'desc': 'v-space shell sweeps [61,64],[89,92],[117,120]',
                   'points': n, 'bad': bad}


def check_C11(audit, corr):
    n = bad = 0
    # bound the resident state: caches from C1/C1b/C3 are dead here and the
    # census itself is anchored cold, exactly like a standalone run
    H_ordered.cache_clear()
    H_canonical.cache_clear()
    for engine in (H_ordered, H_canonical):
        for z in range(0, 80):
            for x in range(11, 71):
                for R in range(0, x + z + 13):
                    c = cand11(z, x, R)
                    if engine(R, (x, 11), z) != c:
                        bad += 1
                    corollary(z, x, R, corr)
                    n += 1
        engine.cache_clear()
    audit['C11'] = {'desc': 'raw census anchor z=0..79 x=11..70 R<=x+z+12, both engines, caches cleared before and between engines',
                    'points': n, 'bad': bad}


def check_C12(audit, types, corr):
    n = bad = 0
    for z in range(0, 121):
        for x in range(11, 121):
            for R in range(1, x + z + 17):
                n += 1
                ok, _, _ = identity_ok11(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
    audit['C12'] = {'desc': 'deep closed grid z=0..120 x=11..120 R<=x+z+16',
                    'points': n, 'bad': bad}


def corollary(z, x, R, corr):
    if x <= z - 12:
        corr['merge']['points'] += 1
        if cand11(z, x, R) != single_token(x + 11, z, R):
            corr['merge']['bad'] += 1
    if R >= x + z + 12:
        corr['tail']['points'] += 1
        if cand11(z, x, R) != (x + 11) % 2:
            corr['tail']['bad'] += 1


def main():
    requested = set(sys.argv[1:])
    everything = {'C1', 'C1b', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C12'}
    todo = requested & everything if requested else (everything - {'C11'})
    audit = {'experiment': 'vertical-fiber-two-token-y11-parametric-allz-proof-20261120',
             'family': 'H(R;(x,11);z), z>=0, x>=11, R>=0',
             'stage': 'part1 (12-check machine constructed; C1d published-slice anchors at y=11 and the census_rows.py duplication deferred to part 2; K1143 stays observed until the full two-part procedure with 3 byte-identical audit runs)',
             'checks_run': sorted(todo),
             'checks': {},
             'corollaries': {
                 'merge_below_diagonal': {'claim': 'x<=z-12 => H == single_token(x+11,z,R)'},
                 'tail': {'claim': 'R>=x+z+12 => H == (x+11)%2'}}}
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
        print('  C4t:', t['violations_at_clip23'], 'violations at clip 23, first:', t['first_violation'])
    return audit


if __name__ == '__main__':
    sys.exit(0 if main()['overall'] == 'PASS' else 1)
