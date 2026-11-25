#!/usr/bin/env python3
"""K1262 (provisional) audit: H(R;(x,y);20), all x>=y>=6, R>=0 - full Grundy
value classification.

Single-owner note: research/log/2026-11-23-z20-y-ge6-single-owner-note.md
(commit 3ff687c7e2..., declared 2026-11-23T16:25Z at HEAD 5c9ee6b3; B=K1126
z=20 row, C=1 xor K1261, as nominated by K1261). The pre-declaration census
(364 rows, y=6..16, d=0..32, R<=S+21) is disclosed in the note; the whole
verifier battery below was executed after the declaration.

Verifier pattern: K1259/K1261 (dual raw recursion engines + closed form +
parametric signature-band coverage/identity/mex + anchors K1126 (y=5
parametric all-z family, the B child at y=6 rows evaluated at z=20) and
K1261 (z=19, y>=6 uniform family, the C child) + direct closure sweep +
low-R single-token collapse with the sharpness witness (16,6)@27 + tail +
set/predicate cross-transcription + fixed-seed scatter with deep
band-identity samples).

Two-level induction: y-outer (B child: row y-1, y=6 anchored by the
published K1126 cand5 slice at z=20), d-inner (A child: same row, d-1; d=0
by the A==B multiset merge). C child: 1 XOR value19 (published K1261).

Identity: z=20 is even, so this is the z=18 (K1259) pattern shifted by 2:
ladder O[1,19]=O[1,z-1], active lattice rows d+z≡2 (mod 4) i.e. d≡2 (mod 4)
with points r=Y+(d+20)/2 (odd) for d<=18, pin=2y+z+1=Y+21 for d>=22, sweep
row d=z+1=21 with band O[Y+21,S+20], value-1 base band O[21,..] (odd
points), A1(d)=Y+13+2*floor((d-8)/4) for d<=20, single-gap odd rows
P=O[21,A1]∪I[A1+2,∞), diagonal S=20 rows with extended ladder top
Y+(d+20)/2-(0 if d≡2 (mod 4) else 1) and empty P, tail R>=S+21 -> S mod 2.
No z=19-style U+1 edit appears (census 364 rows zero mismatch against raw;
the even-z pattern of z=18 carries over to z=20 unedited).

Published coordinate chapters: y=1..5 slices K1023/K1099/K1104/K1112/K1126
(K1126 is parametric in z, so the z=20, y=5 row needs no separate slice);
rows y=6..22 already covered all-z by the published y-family proofs
K1127/K1131/K1135/K1138/K1141/.../K1257; the NEW content of this item is
the infinite tail of rows y>=23 at z=20 and the unified z=20 closed form,
completing the z=20 column as the fourth fully-closed z (after z=17, z=18,
z=19).

Finite audit is not the universal proof: universality rests on the
two-level induction and the complete symbolic band table below.
Standard 11x11 empty board, two-stone roots, S2, class 1/2/4 remain
UNKNOWN.
"""
import hashlib, json, random, sys
from functools import lru_cache
from pathlib import Path
import os

sys.setrecursionlimit(100000)
SMOKE = bool(os.environ.get('SMOKE'))
if SMOKE:
    Y_PARENT, D_PARENT = 10, 12
    X_B, YC_DC, XS = 30, (9, 10), 40
    YB_DB, YD, SWEEP, BAND_N, LOW_N = (9, 10), 12, 60, 40, 40
    SCATTER, DEEP = 800, 60
else:
    Y_PARENT, D_PARENT = 20, 30       # raw parent box: 6<=y<=20, 0<=d<=30
    X_B, YC_DC, XS = 150, (16, 16), 300   # B anchor x<=150; C anchor box; set-check x<=300
    YB_DB, YD, SWEEP, BAND_N, LOW_N = (18, 25), 18, 150, 80, 80
    SCATTER, DEEP = 5000, 1500

def mex(values):
    m = 0; values = set(values)
    while m in values:
        m += 1
    return m

@lru_cache(None)
def g_ordered(R, xs, z):
    if R == 0:
        return 0
    opts = set()
    for i, a in enumerate(xs):
        if a > 1:
            child = xs[:i] + (a - 1,) + xs[i + 1:]
            zz = z
        else:
            child = xs[:i] + xs[i + 1:]
            zz = z + 1
        opts.add(g_ordered(R - 1, child, zz))
    if z:
        opts.add(1 ^ g_ordered(R - 1, xs, z - 1))
    return mex(opts)

@lru_cache(None)
def g_canon(R, xs, z):
    xs = tuple(sorted(xs, reverse=True))
    if R == 0:
        return 0
    opts = set()
    for i, a in enumerate(xs):
        if a > 1:
            child = tuple(sorted(xs[:i] + (a - 1,) + xs[i + 1:], reverse=True))
            zz = z
        else:
            child = tuple(sorted(xs[:i] + xs[i + 1:], reverse=True))
            zz = z + 1
        opts.add(g_canon(R - 1, child, zz))
    if z:
        opts.add(1 ^ g_canon(R - 1, xs, z - 1))
    return mex(opts)

def odd(r, a, b): return r % 2 == 1 and a <= r <= b
def even(r, a, b): return r % 2 == 0 and a <= r <= b

# ---------------- parent closed form (z=20, y>=6 uniform family) ----------
def z20_T(x, y, r):
    d, Y, S = x - y, 2 * y, x + y
    if S < 21:
        if S == 20:
            return odd(r, 1, Y + (d + 20) // 2 - (0 if d % 4 == 2 else 1))
        return odd(r, 1, S if S % 2 else S - 1)
    if odd(r, 1, 19):
        return True
    if d == 21:
        return odd(r, Y + 21, S + 20)
    if d >= 22:
        return r == Y + 21
    if d % 4 == 2:
        return r == Y + (d + 20) // 2
    return False

def A1d20(Y, d):
    return (Y + 13 + 2 * ((d - 8) // 4)) if d <= 20 else Y + 19

def z20_P(x, y, r):
    d, Y, S = x - y, 2 * y, x + y
    if S < 21:
        return S % 2 == 1 and r >= S + 1
    if d >= 22:
        if d % 2 == 0:
            return odd(r, 21, Y + 19) or even(r, Y + 22, S + 20)
        return odd(r, 21, Y + 19) or even(r, Y + 22, S + 19) or r >= S + 21
    if d == 21:
        return odd(r, 21, Y + 19) or even(r, Y + 22, S + 21)
    A1 = A1d20(Y, d)
    if d % 2 == 0:
        return odd(r, 21, A1)
    return odd(r, 21, A1) or r >= A1 + 2

def value20(x, y, r):
    if r == 0:
        return 0
    S = x + y
    if r >= S + 21:
        return S % 2
    if z20_T(x, y, r):
        return 2
    if z20_P(x, y, r):
        return 1
    return 0

# set-based transcription (independent encoding, cross-checked)
def Oset(a, b): return set(range(a + (a % 2 == 0), b + 1, 2))
def Eset(a, b): return set(range(a + (a % 2 == 1), b + 1, 2))

def Tset20(x, y, L):
    d, Y, S = x - y, 2 * y, x + y
    if S < 21:
        if S == 20:
            return Oset(1, min(L, Y + (d + 20) // 2 - (0 if d % 4 == 2 else 1)))
        return Oset(1, min(L, S if S % 2 else S - 1))
    base = Oset(1, 19)
    if d == 21:
        return base | Oset(Y + 21, min(L, S + 20))
    if d >= 22:
        return base | {Y + 21}
    if d % 4 == 2:
        return base | {Y + (d + 20) // 2}
    return base

def Pset20(x, y, L):
    d, Y, S = x - y, 2 * y, x + y
    if S < 21:
        return set(range(S + 1, L + 1)) if S % 2 == 1 else set()
    if d >= 22:
        p = Oset(21, min(L, Y + 19)) | Eset(Y + 22, min(L, S + 20 if d % 2 == 0 else S + 19))
        if d % 2 == 1:
            p |= set(range(S + 21, L + 1))
        return p
    if d == 21:
        p = Oset(21, min(L, Y + 19)) | Eset(Y + 22, min(L, S + 21))
        p |= set(range(S + 22, L + 1))
        return p
    A1 = A1d20(Y, d)
    if d % 2 == 0:
        return Oset(21, min(L, A1))
    return Oset(21, min(L, A1)) | set(range(A1 + 2, L + 1))

def cand20(x, y, r):
    if r == 0:
        return 0
    if r in Tset20(x, y, r):
        return 2
    if r in Pset20(x, y, r):
        return 1
    return 0

# ---------------- C child: K1261 (z=19, y>=6 uniform family) -------------
def z19_T(x, y, r):
    d, Y, S = x - y, 2 * y, x + y
    if S < 19:
        return odd(r, 1, S if S % 2 else S - 1)
    if S == 19:  # the four diagonal rows (y,d) in {(6,7),(7,5),(8,3),(9,1)}
        top = Y + (d + 19) // 2 - (0 if d % 4 == 3 else 1)
        return odd(r, 1, top)
    if odd(r, 1, 19):
        return True
    if d == 20:  # sweep row d=z+1
        return odd(r, Y + 19, S + 19)
    if d >= 21:
        return r == Y + 19
    if d % 2 == 1 and d % 4 == 3:  # active lattice rows d in {3,7,11,15,19}
        return r == Y + (d + 19) // 2
    return False

def z19_P(x, y, r):
    d, Y, S = x - y, 2 * y, x + y
    if S < 19:
        return S % 2 == 1 and r >= S + 1
    if d >= 21:
        if even(r, 20, Y + 18):
            return True
        if odd(r, Y + 21, S + 19):
            return True
        return S % 2 == 1 and r >= S + 20
    if d == 20:
        return even(r, 20, Y + 18)
    if d % 2 == 1:  # odd d, 1 <= d <= 19
        rt = Y + (d + 19) // 2
        if d % 4 == 3:   # lattice rows (incl. pin d=19): T point at rt (odd)
            return even(r, 20, rt - 1) or r >= rt + 1
        return even(r, 20, rt - 2) or r >= rt      # inactive rows (rt even)
    U = Y + 9 + 2 * (d // 4)
    if even(r, 20, U):
        return True
    if d % 4 == 2:
        return r == U + 1
    return False

def value19(x, y, r):
    if r == 0:
        return 0
    S = x + y
    if r >= S + 20:
        return S % 2
    if z19_T(x, y, r):
        return 2
    if z19_P(x, y, r):
        return 1
    return 0


# ---------------- B child at y=6: K1126 (y=5 family, parametric all-z; --
# z=20 row of cand5(z,x,R), verbatim transcription of the published form) --
def q_odd(k):
    return k if k % 2 else k - 1
def in_T5(z, x, R):
    if R <= 0:
        return False
    if x <= z - 6:
        return R % 2 == 1 and R <= q_odd(x + 5)
    d = x - z
    if z % 2 == 1:
        if d <= -5:            # diagonal x=z-5, S=z (may be vacuous for small z via x>=5)
            return R % 2 == 1 and R <= z + 4
        inband = R % 2 == 1 and R <= z
        if d == -3:
            return inband or R == z + 6
        if d == 1:
            return inband or R == z + 8
        if d == 5:
            return inband or R == z + 10
        if d == 6:
            return inband or (R % 2 == 1 and z + 10 <= R <= 2 * z + 11)
        if d >= 7:
            return inband or R == z + 10
        return inband
    else:
        if d <= -5:
            return R % 2 == 1 and R <= z + 5
        inband = R % 2 == 1 and R <= z - 1
        if d == -1:
            return inband or R == z + 7
        if d == 3:
            return inband or R == z + 9
        if d == 6:
            return inband or (R % 2 == 1 and z + 11 <= R <= 2 * z + 11)
        if d >= 7:
            return inband or R == z + 11
        return inband

def band5(z, x, R):
    return z + 12 <= R <= x + z + 5 and R % 2 == z % 2

def in_P5(z, x, R):
    if R <= 0:
        return False
    if x <= z - 6:
        S = x + 5
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    base5 = R in (z+1, z+3, z+5, z+7, z+9)
    b3 = R in (z+1, z+3, z+5)
    b4 = R in (z+1, z+3, z+5, z+7)
    if z % 2 == 1:
        if d == -5:
            return b3 or R >= z + 6
        if d == -4:
            return b3
        if d == -3:
            return b4 or R >= z + 8
        if d == -2:
            return b3
        if d == -1:
            return b4 or R >= z + 8
        if d == 0:
            return b4
        if d == 1:
            return base5 or R >= z + 10
        if d == 2:
            return b4
        if d == 3:
            return base5 or R >= z + 10
        if d == 4:
            return base5
        if d == 5:
            return base5 or R == z + 11 or R >= z + 12
        if d == 6:
            return base5
        tail = x % 2 == 0 and R >= x + z + 6
        return base5 or band5(z, x, R) or tail
    else:
        if d == -5:
            return False
        if d == -4:
            return b3 or R >= z + 6
        if d == -3:
            return b3
        if d == -2:
            return b4 or R >= z + 8
        if d == -1:
            return b3
        if d == 0:
            return b4 or R >= z + 8
        if d == 1:
            return b4
        if d == 2:
            return base5 or R >= z + 10
        if d == 3:
            return b4
        if d == 4:
            return base5 or R >= z + 10
        if d == 5:
            return base5
        tail = x % 2 == 0 and R >= x + z + 6
        return base5 or band5(z, x, R) or tail

def cand5(z, x, R):
    t = in_T5(z, x, R)
    pv = in_P5(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    if R == 0:
        return 0
    if t:
        return 2
    return 1 if pv else 0




# ---------------- parametric signature bands ------------------------------
TRANSIENT = {
    (6, 0): ([(1, 11, '01'), (13, 31, '1')], [(2, 12, '23'), (14, 32, '1')]),
    (6, 1): ([(1, 13, '01'), (15, 33, '0')], [(2, 12, '23'), (14, 14, '03'), (16, 32, '0')]),
    (6, 2): ([(1, 13, '01'), (15, 33, '1')], [(2, 14, '23'), (16, 34, '1')]),
    (6, 3): ([(1, 15, '01'), (17, 35, '0')], [(2, 14, '23'), (16, 16, '03'), (18, 34, '0')]),
    (6, 4): ([(1, 15, '01'), (17, 35, '1')], [(2, 16, '23'), (18, 36, '1')]),
    (6, 5): ([(1, 17, '01'), (19, 37, '0')], [(2, 16, '23'), (18, 18, '03'), (20, 36, '0')]),
    (6, 6): ([(1, 17, '01'), (19, 37, '1')], [(2, 18, '23'), (20, 38, '1')]),
    (6, 7): ([(1, 19, '01'), (21, 39, '0')], [(2, 18, '23'), (20, 26, '03'), (28, 38, '0')]),
    (6, 8): ([(1, 25, '01'), (27, 39, '1')], [(2, 20, '23'), (22, 40, '1')]),
    (7, 0): ([(1, 13, '01'), (15, 33, '1')], [(2, 14, '23'), (16, 34, '1')]),
    (7, 1): ([(1, 15, '01'), (17, 35, '0')], [(2, 14, '23'), (16, 16, '03'), (18, 34, '0')]),
    (7, 2): ([(1, 15, '01'), (17, 35, '1')], [(2, 16, '23'), (18, 36, '1')]),
    (7, 3): ([(1, 17, '01'), (19, 37, '0')], [(2, 16, '23'), (18, 18, '03'), (20, 36, '0')]),
    (7, 4): ([(1, 17, '01'), (19, 37, '1')], [(2, 18, '23'), (20, 38, '1')]),
    (7, 5): ([(1, 19, '01'), (21, 39, '0')], [(2, 18, '23'), (20, 26, '03'), (28, 38, '0')]),
    (7, 6): ([(1, 27, '01'), (29, 39, '1')], [(2, 20, '23'), (22, 40, '1')]),
    (8, 0): ([(1, 15, '01'), (17, 35, '1')], [(2, 16, '23'), (18, 36, '1')]),
    (8, 1): ([(1, 17, '01'), (19, 37, '0')], [(2, 16, '23'), (18, 18, '03'), (20, 36, '0')]),
    (8, 2): ([(1, 17, '01'), (19, 37, '1')], [(2, 18, '23'), (20, 38, '1')]),
    (8, 3): ([(1, 19, '01'), (21, 39, '0')], [(2, 18, '23'), (20, 28, '03'), (30, 38, '0')]),
    (8, 4): ([(1, 27, '01'), (29, 39, '1')], [(2, 20, '23'), (22, 40, '1')]),
    (9, 0): ([(1, 17, '01'), (19, 37, '1')], [(2, 18, '23'), (20, 38, '1')]),
    (9, 1): ([(1, 19, '01'), (21, 39, '0')], [(2, 18, '23'), (20, 28, '03'), (30, 38, '0')]),
    (9, 2): ([(1, 29, '01'), (31, 39, '1')], [(2, 20, '23'), (22, 40, '1')]),
    (10, 0): ([(1, 29, '01'), (31, 39, '1')], [(2, 20, '23'), (22, 40, '1')]),
}

def z20_bands(y, d):
    Y = 2 * y
    S = 2 * y + d
    if (y, d) in TRANSIENT:
        return TRANSIENT[(y, d)]
    ot = S + 20 if S % 2 == 1 else S + 19
    et = S + 20 if S % 2 == 0 else S + 19
    A1 = A1d20(Y, d)
    O = [(1, 19, '01')]
    E = [(2, 20, '23')]
    if d == 21:  # sweep row d=z+1
        O += [(21, Y + 19, '0'), (Y + 21, ot, '01')]
        E += [(22, Y + 18, '1'), (Y + 20, Y + 20, '123'), (Y + 22, et, '0')]
    elif d >= 22:
        O += [(21, Y + 19, '0'), (Y + 21, Y + 21, '01'), (Y + 23, ot, '1')]
        E += [(22, Y + 18, '1'), (Y + 20, Y + 20, '123')]
        if d == 22:  # d=z+2 row: uniform '02' even band
            E += [(Y + 22, et, '02')]
        else:
            E += [(Y + 22, Y + 22, '02'), (Y + 24, et, '0')]
    elif d % 4 == 2:  # active lattice rows d in {2,6,10,14,18}
        L = Y + (d + 20) // 2
        O += [(21, L - 2, '0'), (L, L, '01'), (L + 2, ot, '1')]
        E += [(22, et, '1')]
    elif d % 2 == 0:  # inactive even rows d≡0 (mod 4), d<=20
        O += [(21, A1, '0'), (A1 + 2, ot, '1')]
        if d == 20:  # d=z row
            E += [(22, Y + 18, '1'), (Y + 20, et, '123')]
        else:
            E += [(22, et, '1')]
    else:  # odd d, 1 <= d <= 19: single-gap rows
        O += [(21, ot, '0')]
        if S == 21:
            if d % 4 == 3:
                E += [(22, A1 + 1, '12'), (A1 + 3, A1 + 3, '023'), (A1 + 5, et, '0')]
            else:
                E += [(22, A1 + 1, '12'), (A1 + 3, et, '0')]
        else:
            if d % 4 == 3:
                E += [(22, A1 + 1, '1'), (A1 + 3, A1 + 3, '023'), (A1 + 5, et, '0')]
            else:
                E += [(22, A1 - 1, '1'), (A1 + 1, A1 + 1, '12'), (A1 + 3, et, '0')]
    return O, E

MEX = {'01': 2, '0': 1, '1': 0, '23': 0, '03': 1, '12': 0, '13': 0,
       '02': 1, '023': 1, '123': 0}

def signature(y, d, R):
    """mechanical child signature at budget R from the closed forms"""
    x = y + d
    rr = R - 1
    vals = set()
    if d == 0:
        vals.add(cand5(20, y, rr) if y == 6 else value20(y, y - 1, rr))
    else:
        vals.add(value20(x - 1, y, rr))
        vals.add(cand5(20, x, rr) if y == 6 else value20(x, y - 1, rr))
    vals.add(1 ^ value19(x, y, rr))
    return ''.join(str(v) for v in sorted(vals))

counts = {}

# 1) parent: dual recursion engines vs closed form, z=20
parent_checks = 0
for y in range(6, Y_PARENT + 1):
    for d in range(0, D_PARENT + 1):
        x = y + d
        S = x + y
        for R in range(S + 21):
            a = g_ordered(R, (x, y), 20)
            b = g_canon(R, (x, y), 20)
            c = value20(x, y, R)
            assert a == b == c, ("parent", x, y, d, R, a, b, c)
            parent_checks += 1
counts["parent_two_recursions"] = parent_checks

# 2) B anchor: K1126 cand5 z=20 row vs recursion, z=20 y=5 (x>=6 needed)
b_checks = 0
for x in range(6, X_B + 1):
    for R in range(x + 30):
        a = g_ordered(R, (x, 5), 20)
        b = g_canon(R, (x, 5), 20)
        c = cand5(20, x, R)
        assert a == b == c, ("B/K1126-z20-row", x, R, a, b, c)
        b_checks += 1
counts["K1126_B_anchor_z20_row"] = b_checks

# 3) C anchor re-validation: K1261 transcription vs recursion
c_checks = 0
for y in range(6, YC_DC[0] + 1):
    for d in range(0, YC_DC[1] + 1):
        x = y + d
        S = x + y
        for R in range(S + 19):
            a = g_ordered(R, (x, y), 19)
            b = g_canon(R, (x, y), 19)
            c = value19(x, y, R)
            assert a == b == c, ("C/K1261", x, y, d, R, a, b, c)
            c_checks += 1
counts["K1261_C_anchor"] = c_checks

# 4) signature bands: shape, coverage, identity, mex, parity, tops
sig_checks = 0
for y in range(6, BAND_N + 1):
    for d in range(0, BAND_N + 1):
        S = 2 * y + d
        ot = S + 20 if S % 2 == 1 else S + 19
        et = S + 20 if S % 2 == 0 else S + 19
        for par, want in ((1, ot), (0, et)):
            bands = z20_bands(y, d)[0 if par else 1]
            prev = None
            for lo, hi, s in bands:
                assert lo % 2 == par and hi % 2 == par and lo <= hi and s in MEX, ("band shape", y, d, par, bands)
                if prev is not None:
                    assert lo == prev + 2, ("band gap", y, d, par, bands)
                prev = hi
            assert prev == want, ("band top", y, d, par, bands, want)
        for R in range(1, S + 21):
            bo, be = z20_bands(y, d)
            bands = bo if R % 2 else be
            hits = [s for lo, hi, s in bands if lo <= R <= hi]
            assert len(hits) == 1, ("band coverage", y, d, R, hits)
            got = signature(y, d, R)
            assert hits[0] == got, ("band signature", y, d, R, hits[0], got)
            assert MEX[hits[0]] == value20(y + d, y, R), ("band mex", y, d, R, hits[0])
            v = value20(y + d, y, R)
            assert not (R % 2 == 0 and v == 2), ("parity T", y, d, R)
            assert 0 <= v <= 2, ("range", y, d, R)
            sig_checks += 1
counts["signature_coverage_identity_mex"] = sig_checks

# 5) direct closure sweep: parent == mex of closed-form children, wide
closure_checks = 0
for y in range(6, SWEEP + 1):
    for d in range(0, SWEEP + 1):
        S = 2 * y + d
        x = y + d
        for R in range(1, S + 21):
            rr = R - 1
            vals = set()
            if d == 0:
                vals.add(cand5(20, y, rr) if y == 6 else value20(y, y - 1, rr))
            else:
                vals.add(value20(x - 1, y, rr))
                vals.add(cand5(20, x, rr) if y == 6 else value20(x, y - 1, rr))
            vals.add(1 ^ value19(x, y, rr))
            assert mex(vals) == value20(x, y, R), ("closure", y, d, R)
            closure_checks += 1
counts["closure_sweep"] = closure_checks

# 6) low-R single-token collapse: R <= 26 = z+6, witness (16,6)@27
low_checks = 0
for y in range(6, LOW_N + 1):
    for d in range(0, LOW_N + 1):
        x = y + d
        S = x + y
        for R in range(27):
            a = value20(x, y, R)
            b = g_ordered(R, (S,), 20)
            assert a == b, ("low-R collapse", x, y, R, a, b)
            low_checks += 1
counts["low_R_single_token_collapse"] = low_checks
assert value20(16, 6, 27) == 2 and g_ordered(27, (22,), 20) == 1, ("low-R witness", 16, 6, 27)
counts["low_R_witness_16_6_R27"] = 1

# 7) tail: R >= S+21 gives S%2, raw
tail_checks = 0
for y in range(6, YB_DB[0] + 1):
    for d in range(0, YB_DB[1] + 1):
        x = y + d
        S = x + y
        for R in range(S + 21, S + 26):
            a = g_ordered(R, (x, y), 20)
            b = g_canon(R, (x, y), 20)
            assert a == b == S % 2, ("tail", x, y, R, a, b, S % 2)
            tail_checks += 1
counts["tail_direct"] = tail_checks

# 8) set-based vs predicate transcription
sp_checks = 0
for y in range(6, 31):
    for d in range(0, min(XS - y, 60) + 1):
        x = y + d
        S = x + y
        for R in range(S + 23):
            assert cand20(x, y, R) == value20(x, y, R), ("set vs predicate", x, y, R)
            sp_checks += 1
counts["set_vs_predicate"] = sp_checks

# 9) fixed-seed scatter: raw engines shallow + formula consistency deep
rng = random.Random(20261123)
scatter_checks = 0
for _ in range(SCATTER):
    y = rng.randint(6, 25)
    d = rng.randint(0, 25)
    x = y + d
    S = x + y
    R = rng.randint(0, S + 20)
    a = g_ordered(R, (x, y), 20)
    b = g_canon(R, (x, y), 20)
    f = value20(x, y, R)
    assert a == b == f, ("scatter raw", x, y, R, a, b, f)
    scatter_checks += 1
for _ in range(SCATTER):
    y = rng.randint(6, 4000)
    d = rng.randint(0, 4000)
    x = y + d
    S = x + y
    R = rng.randint(1, S + 20)
    v = value20(x, y, R)
    assert v in (0, 1, 2)
    assert not (z20_T(x, y, R) and z20_P(x, y, R))
    if R >= S + 21:
        assert v == S % 2
    bo, be = z20_bands(y, d)
    bands = bo if R % 2 else be
    hits = [s for lo, hi, s in bands if lo <= R <= hi]
    assert len(hits) == 1 and hits[0] == signature(y, d, R), ("deep band identity", y, d, R)
    assert MEX[hits[0]] == v, ("deep band mex", y, d, R)
    scatter_checks += 1
for _ in range(1000):
    y = rng.randint(6, DEEP)
    d = rng.randint(0, DEEP)
    x = y + d
    S = x + y
    R = rng.randint(S + 21, S + 31)
    assert value20(x, y, R) == S % 2, ("deep tail", x, y, R)
    scatter_checks += 1
counts["fixed_seed_scatter"] = scatter_checks

counts["total"] = sum(counts.values())
counts["bad"] = []
counts["claim"] = "H(R;(x,y);20), all x>=y>=6 and R>=0"
counts["proof_status"] = "proved_by_two_level_induction_and_symbolic_signature_bands"
counts["finite_audit_scope"] = {
    "parent_direct": "6<=y<=%d, 0<=d<=%d, 0<=R<=x+y+20" % (Y_PARENT, D_PARENT),
    "K1126_B_anchor": "6<=x<=%d, 0<=R<=x+29 (z=20 row of the parametric y=5 family)" % X_B,
    "K1261_C_anchor": "6<=y<=%d, 0<=d<=%d, 0<=R<=x+y+18" % YC_DC,
    "signature_bands": "6<=y<=%d, 0<=d<=%d, all 1<=R<=x+y+20" % (BAND_N, BAND_N),
    "closure_sweep": "6<=y<=%d, 0<=d<=%d, all 1<=R<=x+y+20 (direct mex of closed-form children)" % (SWEEP, SWEEP),
    "low_R_collapse": "6<=y<=%d, 0<=d<=%d, 0<=R<=26 (=z+6); sharpness witness (16,6)@R=27: value20=2 vs single token 1" % (LOW_N, LOW_N),
    "tail_direct": "6<=y<=%d, 0<=d<=%d, x+y+21<=R<=x+y+25" % YB_DB,
    "set_vs_predicate": "independent set-based transcription vs predicates, x<=300",
    "scatter_seed": 20261123,
    "scatter_raw": "y,d<=25, R<=x+y+20 (dual engines vs closed form)",
    "deep_scatter": "band identity + mex at y,d<=4000; tail consistency at y,d<=%d" % DEEP,
}
counts["verifier_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
raw = json.dumps(counts, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
out = Path(__file__).resolve().parent / "output" / "audit.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(raw, encoding="utf-8")
print(raw, end="")
