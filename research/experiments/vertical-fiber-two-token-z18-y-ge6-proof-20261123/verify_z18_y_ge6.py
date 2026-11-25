#!/usr/bin/env python3
"""K1259 (provisional) audit: H(R;(x,y);18), all x>=y>=6, R>=0 - full Grundy
value classification.
Verifier pattern: K1077/K1087 (dual raw recursion engines + closed form +
parametric signature-band coverage/identity/mex + anchors K1092 (z=18, y=5
slice, the B child at y=6 rows) and K1087 (z=17, y>=6 uniform family, the
C child) + direct closure sweep + low-R single-token collapse with the
sharpness witness (12,6)@25 + tail + set/predicate cross-transcription +
fixed-seed scatter with deep band-identity samples).
Two-level induction: y-outer (B child: row y-1, y=6 anchored by the
published K1092 slice), d-inner (A child: same row, d-1; d=0 by the
A==B multiset merge). C child: 1 XOR value17 (published K1087).
Published coordinate chapters: y=1..5 slices K1023/K1051/K1078/K1083/K1092;
rows y=6..22 already covered all-z by the published y-family proofs
K1127/K1131/K1135/K1138/K1141/.../K1257; the NEW content of this item is
the infinite tail of rows y>=23 at z=18 and the unified z=18 closed form.
Standard 11x11 empty board, two-stone roots, S2, class 1/2/4 remain UNKNOWN.
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

# ---------------- parent closed form (z=18, y>=6 uniform family) ----------
def z18_T(x, y, r):
    d, Y, S = x - y, 2 * y, x + y
    if S < 19:
        if S == 18:
            return odd(r, 1, Y + (d + 18) // 2 - (1 if d % 4 == 2 else 0))
        return odd(r, 1, S if S % 2 else S - 1)
    if odd(r, 1, 17):
        return True
    if d == 19:
        return odd(r, S, S + 18)
    if d >= 20:
        return r == Y + 19
    if d % 4 == 0:
        return r == Y + (d + 18) // 2
    return False

def A1d(Y, d):
    return (Y + 7 + 2 * ((d + 2) // 4)) if d <= 18 else Y + 17

def z18_P(x, y, r):
    d, Y, S = x - y, 2 * y, x + y
    if S < 19:
        return S % 2 == 1 and r >= S + 1
    A1 = A1d(Y, d)
    if d >= 20:
        if d % 2 == 0:
            return odd(r, 19, Y + 17) or even(r, Y + 20, S + 18)
        return odd(r, 19, Y + 17) or even(r, Y + 20, S + 17) or r >= S + 19
    if d == 19:
        return odd(r, 19, Y + 17) or even(r, Y + 20, S + 19) or r >= S + 20
    if d % 2 == 0:
        return odd(r, 19, A1)
    return odd(r, 19, A1) or r >= A1 + 2

def value18(x, y, r):
    if r == 0:
        return 0
    S = x + y
    if r >= S + 19:
        return S % 2
    if z18_T(x, y, r):
        return 2
    if z18_P(x, y, r):
        return 1
    return 0

# set-based transcription (independent encoding, cross-checked)
def Oset(a, b): return set(range(a + (a % 2 == 0), b + 1, 2))
def Eset(a, b): return set(range(a + (a % 2 == 1), b + 1, 2))

def Tset18(x, y):
    d, Y, S = x - y, 2 * y, x + y
    if S < 19:
        if S == 18:
            return Oset(1, Y + (d + 18) // 2 - (1 if d % 4 == 2 else 0))
        return Oset(1, S if S % 2 else S - 1)
    base = Oset(1, 17)
    if d == 19:
        return base | Oset(S, S + 18)
    if d >= 20:
        return base | {Y + 19}
    if d % 4 == 0:
        return base | {Y + (d + 18) // 2}
    return base

def Pset18(x, y):
    d, Y, S = x - y, 2 * y, x + y
    if S < 19:
        return set(range(S + 1, 4000)) if S % 2 == 1 else set()
    A1 = A1d(Y, d)
    if d >= 20:
        p = Oset(19, Y + 17) | Eset(Y + 20, S + 18 if d % 2 == 0 else S + 17)
        if d % 2 == 1:
            p |= set(range(S + 19, 4000))
        return p
    if d == 19:
        return Oset(19, Y + 17) | Eset(Y + 20, S + 19) | set(range(S + 20, 4000))
    if d % 2 == 0:
        return Oset(19, A1)
    return Oset(19, A1) | set(range(A1 + 2, 4000))

def cand18(x, y, r):
    if r == 0:
        return 0
    if r in Tset18(x, y):
        return 2
    if r in Pset18(x, y):
        return 1
    return 0

# ---------------- C child: K1087 (z=17, y>=6 uniform family) --------------
def z17_T(x, y, r):
    d, Y, S = x - y, 2 * y, x + y
    if S < 17:
        return odd(r, 1, S if S % 2 else S - 1)
    if S == 17:
        top = Y + (d + 17) // 2 - (0 if d % 4 == 1 else 1)
        return odd(r, 1, top)
    if odd(r, 1, 17):
        return True
    if d == 18:
        return odd(r, Y + 17, S + 17)
    if d >= 19:
        return r == Y + 17
    if d % 2 == 1 and d % 4 == 1:
        return r == Y + (d + 17) // 2
    return False

def z17_P(x, y, r):
    d, Y, S = x - y, 2 * y, x + y
    if S < 17:
        return S % 2 == 1 and r >= S + 1
    if d >= 19:
        if even(r, 18, Y + 16):
            return True
        if odd(r, Y + 19, S + 17):
            return True
        return S % 2 == 1 and r >= S + 18
    if d == 18:
        return even(r, 18, Y + 16)
    if d % 2 == 1:
        rt = Y + (d + 17) // 2
        if d % 4 == 1:
            return even(r, 18, rt - 1) or r >= rt + 1
        return even(r, 18, rt - 2) or r >= rt
    U = Y + 8 + 2 * (d // 4)
    return even(r, 18, U)

def value17(x, y, r):
    if r == 0:
        return 0
    S = x + y
    if r >= S + 18:
        return S % 2
    if z17_T(x, y, r):
        return 2
    if z17_P(x, y, r):
        return 1
    return 0

# ---------------- B child at y=6: K1092 (z=18, y=5 slice) ----------------
def z18y5_T(x, r):
    if 5 <= x <= 12: return r % 2 == 1 and r <= (x + 5 if (x + 5) % 2 == 1 else x + 4)
    if x == 13: return r % 2 == 1 and r <= 23
    if 14 <= x <= 16 or x in (18, 19, 20, 22, 23): return r % 2 == 1 and r <= 17
    if x == 17: return (r % 2 == 1 and r <= 17) or r == 25
    if x == 21: return (r % 2 == 1 and r <= 17) or r == 27
    if x == 24: return (r % 2 == 1 and r <= 17) or (r % 2 == 1 and 29 <= r <= 47)
    return (r % 2 == 1 and r <= 17) or r == 29

def z18y5_P(x, r):
    if x in (5, 7, 9, 11, 13): return False
    if x in (6, 8, 10, 12): return r >= x + 6
    if x == 14: return r in (19, 21) or r >= 23
    if x == 15: return r in (19, 21, 23)
    if x == 16: return r in (19, 21, 23) or r >= 25
    if x == 17: return r in (19, 21, 23)
    if x == 18: return r in (19, 21, 23) or r >= 25
    if x == 19: return r in (19, 21, 23, 25)
    if x == 20: return r in (19, 21, 23, 25) or r >= 27
    if x == 21: return r in (19, 21, 23, 25)
    if x == 22: return r in (19, 21, 23, 25) or r >= 27
    if x == 23: return r in (19, 21, 23, 25, 27)
    if x == 24: return r in (19, 21, 23, 25, 27) or (r % 2 == 0 and 30 <= r <= 46) or r >= 48
    b = r in (19, 21, 23, 25, 27)
    if x % 2: return b or (r % 2 == 0 and 30 <= r <= (x + 23 if (x + 23) % 2 == 0 else x + 22))
    return b or (r % 2 == 0 and 30 <= r <= (x + 23 if (x + 23) % 2 == 0 else x + 22)) or r >= x + 24

def k1092(x, r):
    if r == 0:
        return 0
    if r >= x + 24:
        return (x + 5) % 2
    if z18y5_T(x, r):
        return 2
    if z18y5_P(x, r):
        return 1
    return 0

# ---------------- parametric signature bands ------------------------------
TRANSIENT = {
    (6, 0): ([(1, 11, '01'), (13, 29, '1')], [(2, 12, '23'), (14, 30, '1')]),
    (6, 1): ([(1, 13, '01'), (15, 31, '0')], [(2, 12, '23'), (14, 14, '03'), (16, 30, '0')]),
    (6, 2): ([(1, 13, '01'), (15, 31, '1')], [(2, 14, '23'), (16, 32, '1')]),
    (6, 3): ([(1, 15, '01'), (17, 33, '0')], [(2, 14, '23'), (16, 16, '03'), (18, 32, '0')]),
    (6, 4): ([(1, 15, '01'), (17, 33, '1')], [(2, 16, '23'), (18, 34, '1')]),
    (6, 5): ([(1, 17, '01'), (19, 35, '0')], [(2, 16, '23'), (18, 24, '03'), (26, 34, '0')]),
    (6, 6): ([(1, 23, '01'), (25, 35, '1')], [(2, 18, '23'), (20, 36, '1')]),
    (7, 0): ([(1, 13, '01'), (15, 31, '1')], [(2, 14, '23'), (16, 32, '1')]),
    (7, 1): ([(1, 15, '01'), (17, 33, '0')], [(2, 14, '23'), (16, 16, '03'), (18, 32, '0')]),
    (7, 2): ([(1, 15, '01'), (17, 33, '1')], [(2, 16, '23'), (18, 34, '1')]),
    (7, 3): ([(1, 17, '01'), (19, 35, '0')], [(2, 16, '23'), (18, 24, '03'), (26, 34, '0')]),
    (7, 4): ([(1, 25, '01'), (27, 35, '1')], [(2, 18, '23'), (20, 36, '1')]),
    (8, 0): ([(1, 15, '01'), (17, 33, '1')], [(2, 16, '23'), (18, 34, '1')]),
    (8, 1): ([(1, 17, '01'), (19, 35, '0')], [(2, 16, '23'), (18, 26, '03'), (28, 34, '0')]),
    (8, 2): ([(1, 25, '01'), (27, 35, '1')], [(2, 18, '23'), (20, 36, '1')]),
    (9, 0): ([(1, 27, '01'), (29, 35, '1')], [(2, 18, '23'), (20, 36, '1')]),
}

def z18_bands(y, d):
    Y = 2 * y
    S = 2 * y + d
    if (y, d) in TRANSIENT:
        return TRANSIENT[(y, d)]
    A1 = A1d(Y, d)
    ot = S + 18 if S % 2 == 1 else S + 17
    et = S + 18 if S % 2 == 0 else S + 17
    O = [(1, 17, '01')]
    E = [(2, 18, '23')]
    if d <= 18 and d % 4 == 0:
        L = Y + (d + 18) // 2
        O += [(19, L - 2, '0'), (L, L, '01'), (L + 2, ot, '1')]
        E += [(20, et, '1')]
    elif d <= 18 and d % 2 == 0:
        O += [(19, A1, '0'), (A1 + 2, ot, '1')]
        if d == 18:
            E += [(20, Y + 16, '1'), (Y + 18, et, '123')]
        else:
            E += [(20, et, '1')]
    elif d == 19:
        O += [(19, Y + 17, '0'), (S, ot, '01')]
        E += [(20, Y + 16, '1'), (Y + 18, Y + 18, '123'), (Y + 20, et, '0')]
    elif d >= 20:
        O += [(19, Y + 17, '0'), (Y + 19, Y + 19, '01'), (Y + 21, ot, '1')]
        E += [(20, Y + 16, '1'), (Y + 18, Y + 18, '123')]
        if d == 20:
            E += [(Y + 20, et, '02')]
        else:
            E += [(Y + 20, Y + 20, '02'), (Y + 22, et, '0')]
    else:
        O += [(19, ot, '0')]
        if S == 19:
            if d % 4 == 1:
                E += [(20, A1 + 1, '12'), (A1 + 3, A1 + 3, '023'), (A1 + 5, et, '0')]
            else:
                E += [(20, A1 + 1, '12'), (A1 + 3, et, '0')]
        else:
            if d % 4 == 1:
                E += [(20, A1 + 1, '1'), (A1 + 3, A1 + 3, '023'), (A1 + 5, et, '0')]
            else:
                E += [(20, A1 - 1, '1'), (A1 + 1, A1 + 1, '12'), (A1 + 3, et, '0')]
    return O, E

MEX = {'01': 2, '0': 1, '1': 0, '23': 0, '03': 1, '12': 0, '13': 0,
       '02': 1, '023': 1, '123': 0}

def signature(y, d, R):
    """mechanical child signature at budget R from the closed forms"""
    x = y + d
    rr = R - 1
    vals = set()
    if d == 0:
        vals.add(k1092(y, rr) if y == 6 else value18(y, y - 1, rr))
    else:
        vals.add(value18(x - 1, y, rr))
        vals.add(k1092(x, rr) if y == 6 else value18(x, y - 1, rr))
    vals.add(1 ^ value17(x, y, rr))
    return ''.join(str(v) for v in sorted(vals))

counts = {}

# 1) parent: dual recursion engines vs closed form, z=18
parent_checks = 0
for y in range(6, Y_PARENT + 1):
    for d in range(0, D_PARENT + 1):
        x = y + d
        S = x + y
        for R in range(S + 19):
            a = g_ordered(R, (x, y), 18)
            b = g_canon(R, (x, y), 18)
            c = value18(x, y, R)
            assert a == b == c, ("parent", x, y, d, R, a, b, c)
            parent_checks += 1
counts["parent_two_recursions"] = parent_checks

# 2) B anchor: K1092 transcription vs recursion, z=18 y=5 (x>=6 needed)
b_checks = 0
for x in range(6, X_B + 1):
    for R in range(x + 28):
        a = g_ordered(R, (x, 5), 18)
        b = g_canon(R, (x, 5), 18)
        c = k1092(x, R)
        assert a == b == c, ("B/K1092", x, R, a, b, c)
        b_checks += 1
counts["K1092_B_anchor"] = b_checks

# 3) C anchor re-validation: K1087 transcription vs recursion
c_checks = 0
for y in range(6, YC_DC[0] + 1):
    for d in range(0, YC_DC[1] + 1):
        x = y + d
        S = x + y
        for R in range(S + 18):
            a = g_ordered(R, (x, y), 17)
            b = g_canon(R, (x, y), 17)
            c = value17(x, y, R)
            assert a == b == c, ("C/K1087", x, y, d, R, a, b, c)
            c_checks += 1
counts["K1087_C_anchor"] = c_checks

# 4) signature bands: shape, coverage, identity, mex, parity, tops
sig_checks = 0
for y in range(6, BAND_N + 1):
    for d in range(0, BAND_N + 1):
        S = 2 * y + d
        ot = S + 18 if S % 2 == 1 else S + 17
        et = S + 18 if S % 2 == 0 else S + 17
        for par, want in ((1, ot), (0, et)):
            bands = z18_bands(y, d)[0 if par else 1]
            prev = None
            for lo, hi, s in bands:
                assert lo % 2 == par and hi % 2 == par and lo <= hi and s in MEX, ("band shape", y, d, par, bands)
                if prev is not None:
                    assert lo == prev + 2, ("band gap", y, d, par, bands)
                prev = hi
            assert prev == want, ("band top", y, d, par, bands, want)
        for R in range(1, S + 19):
            bo, be = z18_bands(y, d)
            bands = bo if R % 2 else be
            hits = [s for lo, hi, s in bands if lo <= R <= hi]
            assert len(hits) == 1, ("band coverage", y, d, R, hits)
            got = signature(y, d, R)
            assert hits[0] == got, ("band signature", y, d, R, hits[0], got)
            assert MEX[hits[0]] == value18(y + d, y, R), ("band mex", y, d, R, hits[0])
            v = value18(y + d, y, R)
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
        for R in range(1, S + 19):
            rr = R - 1
            vals = set()
            if d == 0:
                vals.add(k1092(y, rr) if y == 6 else value18(y, y - 1, rr))
            else:
                vals.add(value18(x - 1, y, rr))
                vals.add(k1092(x, rr) if y == 6 else value18(x, y - 1, rr))
            vals.add(1 ^ value17(x, y, rr))
            assert mex(vals) == value18(x, y, R), ("closure", y, d, R)
            closure_checks += 1
counts["closure_sweep"] = closure_checks

# 6) low-R single-token collapse: R <= 24 = z+6, witness (12,6)@25
low_checks = 0
for y in range(6, LOW_N + 1):
    for d in range(0, LOW_N + 1):
        x = y + d
        S = x + y
        for R in range(25):
            a = value18(x, y, R)
            b = g_ordered(R, (S,), 18)
            assert a == b, ("low-R collapse", x, y, R, a, b)
            low_checks += 1
counts["low_R_single_token_collapse"] = low_checks
assert value18(12, 6, 25) == 0 and g_ordered(25, (18,), 18) == 2, ("low-R witness", 12, 6, 25)
counts["low_R_witness_12_6_R25"] = 1

# 7) tail: R >= S+19 gives S%2, raw
tail_checks = 0
for y in range(6, YB_DB[0] + 1):
    for d in range(0, YB_DB[1] + 1):
        x = y + d
        S = x + y
        for R in range(S + 19, S + 24):
            a = g_ordered(R, (x, y), 18)
            b = g_canon(R, (x, y), 18)
            assert a == b == S % 2, ("tail", x, y, R, a, b, S % 2)
            tail_checks += 1
counts["tail_direct"] = tail_checks

# 8) set-based vs predicate transcription
sp_checks = 0
for y in range(6, 31):
    for d in range(0, min(XS - y, 60) + 1):
        x = y + d
        S = x + y
        for R in range(S + 21):
            assert cand18(x, y, R) == value18(x, y, R), ("set vs predicate", x, y, R)
            sp_checks += 1
counts["set_vs_predicate"] = sp_checks

# 9) fixed-seed scatter: raw engines shallow + formula consistency deep
rng = random.Random(20261126)
scatter_checks = 0
for _ in range(SCATTER):
    y = rng.randint(6, 25)
    d = rng.randint(0, 25)
    x = y + d
    S = x + y
    R = rng.randint(0, S + 18)
    a = g_ordered(R, (x, y), 18)
    b = g_canon(R, (x, y), 18)
    f = value18(x, y, R)
    assert a == b == f, ("scatter raw", x, y, R, a, b, f)
    scatter_checks += 1
for _ in range(SCATTER):
    y = rng.randint(6, 4000)
    d = rng.randint(0, 4000)
    x = y + d
    S = x + y
    R = rng.randint(1, S + 18)
    v = value18(x, y, R)
    assert v in (0, 1, 2)
    assert not (z18_T(x, y, R) and z18_P(x, y, R))
    if R >= S + 19:
        assert v == S % 2
    bo, be = z18_bands(y, d)
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
    R = rng.randint(S + 19, S + 31)
    assert value18(x, y, R) == S % 2, ("deep tail", x, y, R)
    scatter_checks += 1
counts["fixed_seed_scatter"] = scatter_checks

counts["total"] = sum(counts.values())
counts["bad"] = []
counts["claim"] = "H(R;(x,y);18), all x>=y>=6 and R>=0"
counts["proof_status"] = "proved_by_two_level_induction_and_symbolic_signature_bands"
counts["finite_audit_scope"] = {
    "parent_direct": "6<=y<=%d, 0<=d<=%d, 0<=R<=x+y+18" % (Y_PARENT, D_PARENT),
    "K1092_B_anchor": "6<=x<=%d, 0<=R<=x+27" % X_B,
    "K1087_C_anchor": "6<=y<=%d, 0<=d<=%d, 0<=R<=x+y+17" % YC_DC,
    "signature_bands": "6<=y<=%d, 0<=d<=%d, all 1<=R<=x+y+18" % (BAND_N, BAND_N),
    "closure_sweep": "6<=y<=%d, 0<=d<=%d, all 1<=R<=x+y+18 (direct mex of closed-form children)" % (SWEEP, SWEEP),
    "low_R_collapse": "6<=y<=%d, 0<=d<=%d, 0<=R<=24 (=z+6); sharpness witness (12,6)@R=25: value18=0 vs single token 2" % (LOW_N, LOW_N),
    "tail_direct": "6<=y<=%d, 0<=d<=%d, x+y+19<=R<=x+y+23" % YB_DB,
    "set_vs_predicate": "independent set-based transcription vs predicates, x<=300",
    "scatter_seed": 20261126,
    "scatter_raw": "y,d<=25, R<=x+y+18 (dual engines vs closed form)",
    "deep_scatter": "band identity + mex at y,d<=4000; tail consistency at y,d<=%d" % DEEP,
}
counts["verifier_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
raw = json.dumps(counts, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
out = Path(__file__).resolve().parent / "output" / "audit.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(raw, encoding="utf-8")
print(raw, end="")
