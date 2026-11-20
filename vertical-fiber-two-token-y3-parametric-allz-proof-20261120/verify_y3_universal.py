#!/usr/bin/env python3
"""Universal verifier for the two-token y=3 parametric family, all z.

Claim under test (proposition P3, "y=3 parametric all-z"):
  For all z >= 0, x >= 3, R >= 0:
      H(R; (x, 3); z) == cand3(z, x, R)
  where H is the common circular-fiber two-token residual game value
  (defined by the raw engines below), and cand3 is the closed form
  transcribed in this file.

Corollaries folded into the audit:
  (merge-below-diagonal, y=3)  for all x <= z-4 (so S = x+3 < z):
      H(R;(x,3);z) == single_token(x+3, z, R)   (asserted on every grid
      point and every probe with x <= z-4);
  (tail)  R >= x+z+4  =>  H == (x+3) % 2;
  (published slice anchors)  z=18 (K1078) and z=19 (K1098) are special
      cases; their published predicates are transcribed verbatim.

Method (mirrors verify_p2_universal.py of K1099, adapted to y=3):

  C1   Raw engines (order-preserving and descending-canonical double
       recursion) vs cand3 on z=0..14, x=3..26, R<=x+z+45.
  C1b  Engine anchors for the closed-form children used downstream:
       single_token vs raw single-token engine; the y=2 child
       H(R-1,(x,2),z) vs the K1099 closed form cand2; and the x==3
       coincidence H(R,(2,3),z) == H(R,(3,2),z) == cand2(z,3,R).
  C1d  Verbatim anchors against previously published per-z theorems:
       the z=18 and z=19, y=3 boundary slices (K1078 / K1098) must agree
       with cand3 pointwise on x=3..64, R<=x+50.
  C2   Closed-form-only identity grid: mex of the closed-form children
       == cand3 over z=0..48, x=3..56, R<=x+z+40, plus the merge
       corollary on the same grid, plus deep-tail z (C2b).
  C3   Option-decomposition anchor: the closed-form children chosen in
       the identity equal the raw option-value sets of the engine.
  C4   Type machine over the v-space box (v0,v1,v3 in [-60,60]):
       type = (x==3 bit, z==0 bit, parities, clipped differential
       family); confluence of the effect vector within each realized
       type; full-box identity.
  C7   Seeded far probes (deterministic RNG): 200k points with
       z,x <= 3000, R <= 9000, biased toward the boundary manifolds,
       including the merge corollary on x<=z-4 samples.
  C8   Boundary-manifold sweeps at z in {0..5, 29..31, 59..61,
       299..301, 999..1001, 2999, 3000}, x in z-12..z+6, R<=x+z+26,
       with the tail claim on R in [x+z+4, x+z+6].
  C9   Type-machine shell sweep in v-space bands [61,64], [89,92],
       [117,120] of max|v|: no new types, confluence, identity.
  C12  Deep grid sweep z=0..120, x=3..120, R<=x+z+16: identity and
       merge corollary.

Everything is deterministic. Two runs produce byte-identical
output/audit.json (no timestamps, seeded RNG, sorted JSON keys).
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
# Raw engines (verbatim from the published census line).
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


# ------------------------------------------------------------------
# Published single-token closed form (K0832 line).
# ------------------------------------------------------------------
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
# Published y=2 two-token parametric closed form (K1099, verbatim).
# ------------------------------------------------------------------
def cand2_T(z, x):
    if z % 2 == 1:
        if x <= z - 3:
            top = 2 * ((x + 1) // 2) + 1
            return ("ladder", 1, top, None)
        if x == z - 2:
            return ("band", 1, z + 2, None)
        if x in (z - 1, z, z + 1):
            return ("band", 1, z, None)
        if x == z + 2:
            return ("pin", 1, z, z + 4)
        if x == z + 3:
            return ("sweep", 1, z, (z + 4, 2 * z + 5))
        return ("pin", 1, z, z + 4)
    else:
        if x <= z - 3:
            top = 2 * ((x + 1) // 2) + 1
            return ("ladder", 1, top, None)
        if x == z - 2:
            return ("band", 1, z + 1, None)
        if x in (z - 1, z + 1, z + 2):
            return ("band", 1, z - 1, None)
        if x == z:
            return ("pin", 1, z - 1, z + 3)
        if x == z + 3:
            return ("sweep", 1, z - 1, (z + 5, 2 * z + 5))
        return ("pin", 1, z - 1, z + 5)


def in_T2(z, x, R):
    if R <= 0:
        return False
    kind, lo, hi, extra = cand2_T(z, x)
    if kind in ("ladder", "band"):
        return lo <= R <= hi and R % 2 == 1
    if kind == "pin":
        return (lo <= R <= hi and R % 2 == 1) or R == extra
    a, b = extra
    return (lo <= R <= hi and R % 2 == 1) or (a <= R <= b and R % 2 == 1)


def in_P2(z, x, R):
    if R <= 0:
        return False
    p = z % 2
    if z % 2 == 1:
        if x % 2 == 0 and x <= z - 3:
            return False
        if x % 2 == 1 and x <= z - 3:
            return R >= x + 3
        if x in (z - 2, z):
            return R in (z + 1, z + 3) or R >= z + 4
        if x == z - 1:
            return R == z + 1
        if x == z + 1:
            return R in (z + 1, z + 3)
        if x == z + 2:
            return R in (z + 1, z + 3) or R >= z + 5
        if x == z + 3:
            return R in (z + 1, z + 3)
        if x % 2 == 1:
            return (R in (z + 1, z + 3)
                    or (z + 6 <= R <= x + z + 3 and R % 2 == 1)
                    or R >= x + z + 4)
        return (R in (z + 1, z + 3)
                or (z + 6 <= R <= x + z + 2 and R % 2 == 1))
    else:
        if x % 2 == 0 and x <= z - 2:
            return False
        if x % 2 == 1 and x <= z - 3:
            return R >= x + 3
        if x in (z - 1, z + 1):
            return R in (z + 1, z + 3) or R >= z + 4
        if x == z:
            return R == z + 1
        if x == z + 2:
            return R in (z + 1, z + 3)
        if x % 2 == 1:
            return (R in (z + 1, z + 3)
                    or (z + 6 <= R <= x + z + 3 and R % 2 == p)
                    or R >= x + z + 4)
        return (R in (z + 1, z + 3)
                or (z + 6 <= R <= x + z + 2 and R % 2 == p))


def cand2(z, x, R):
    t = in_T2(z, x, R)
    pv = in_P2(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    if R == 0:
        return 0
    if t:
        return 2
    return 1 if pv else 0


# ------------------------------------------------------------------
# Candidate under test: y=3 two-token parametric closed form, all z.
# Row classes: merge x<=z-4 (single-token merge, S=x+3<z),
# transients x=z-3..z+3, sweep row x=z+4, steady rows x>=z+5.
# Value-2 base: O[1,z] (z odd) / O[1,z-1] (z even); isolated pins
# z+4 and z+6 (z odd, rows z-1 and z+3) / z+5, z+7 (z even, rows
# z+1, and steady); sweep band O[z+6, 2z+7] (z odd) /
# O[z+7, 2z+7] (z even); value-1 base points {z+1, z+3, z+5};
# intermediate band O_z[z+8, x+z+3]; tail I[x+z+4, inf) for x even.
# ------------------------------------------------------------------
def in_T3(z, x, R):
    if R <= 0:
        return False
    S = x + 3
    if z % 2 == 1:
        if x <= z - 4:
            return R % 2 == 1 and R <= q_odd(S)
        if x == z - 3:
            return R % 2 == 1 and R <= z + 2
        if x == z - 2:
            return R % 2 == 1 and R <= z
        if x == z - 1:
            return (R % 2 == 1 and R <= z) or R == z + 4
        if x == z:
            return R % 2 == 1 and R <= z
        if x == z + 1:
            return R % 2 == 1 and R <= z
        if x == z + 2:
            return R % 2 == 1 and R <= z
        if x == z + 3:
            return (R % 2 == 1 and R <= z) or R == z + 6
        if x == z + 4:
            return (R % 2 == 1 and R <= z) or (R % 2 == 1 and z + 6 <= R <= 2 * z + 7)
        return (R % 2 == 1 and R <= z) or R == z + 6
    else:
        if x <= z - 4:
            return R % 2 == 1 and R <= q_odd(S)
        if x == z - 3:
            return R % 2 == 1 and R <= z + 3
        if x == z - 2:
            return R % 2 == 1 and R <= z - 1
        if x == z - 1:
            return R % 2 == 1 and R <= z - 1
        if x == z:
            return R % 2 == 1 and R <= z - 1
        if x == z + 1:
            return (R % 2 == 1 and R <= z - 1) or R == z + 5
        if x == z + 2:
            return R % 2 == 1 and R <= z - 1
        if x == z + 3:
            return R % 2 == 1 and R <= z - 1
        if x == z + 4:
            return (R % 2 == 1 and R <= z - 1) or (R % 2 == 1 and z + 7 <= R <= 2 * z + 7)
        return (R % 2 == 1 and R <= z - 1) or R == z + 7


def in_P3(z, x, R):
    if R <= 0:
        return False
    S = x + 3
    zn = z % 2
    if zn == 1:
        if x <= z - 4:
            return S % 2 == 1 and R >= q_odd(S) + 1
        if x == z - 3:
            return R == z + 1 or R >= z + 3
        if x == z - 2:
            return R in (z + 1, z + 3)
        if x == z - 1:
            return R in (z + 1, z + 3) or R >= z + 5
        if x == z:
            return R in (z + 1, z + 3)
        if x == z + 1:
            return R in (z + 1, z + 3) or R >= z + 5
        if x == z + 2:
            return R in (z + 1, z + 3, z + 5)
        if x == z + 3:
            return R in (z + 1, z + 3, z + 5) or R >= z + 7
        if x == z + 4:
            return R in (z + 1, z + 3, z + 5)
        base = R in (z + 1, z + 3, z + 5)
        band = z + 8 <= R <= x + z + 3 and R % 2 == 1
        tail = x % 2 == 0 and R >= x + z + 4
        return base or band or tail
    else:
        if x <= z - 4:
            return S % 2 == 1 and R >= q_odd(S) + 1
        if x == z - 3:
            return False
        if x == z - 2:
            return R == z + 1 or R >= z + 3
        if x == z - 1:
            return R in (z + 1, z + 3)
        if x == z:
            return R in (z + 1, z + 3) or R >= z + 5
        if x == z + 1:
            return R in (z + 1, z + 3)
        if x == z + 2:
            return R in (z + 1, z + 3) or R >= z + 5
        if x == z + 3:
            return R in (z + 1, z + 3, z + 5)
        base = R in (z + 1, z + 3, z + 5)
        band = z + 8 <= R <= x + z + 3 and R % 2 == 0
        tail = x % 2 == 0 and R >= x + z + 4
        return base or band or tail


def cand3(z, x, R):
    t = in_T3(z, x, R)
    pv = in_P3(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    if R == 0:
        return 0
    if t:
        return 2
    return 1 if pv else 0


# ------------------------------------------------------------------
# Verbatim published per-z candidates (z=18 and z=19, y=3), used as
# independent anchors (transcribed unchanged from the published
# verifiers of K1078 and K1098).
# ------------------------------------------------------------------
def z18_candidate_T(x, r):
    if r % 2 == 0:
        return False
    if x <= 14:
        return r <= 2 * (x // 2) + 3
    if x == 15:
        return r <= 21
    if 16 <= x <= 18:
        return r <= 17
    if x == 19:
        return r <= 17 or r == 23
    if x in (20, 21):
        return r <= 17
    if x == 22:
        return r <= 17 or 25 <= r <= 43
    return r <= 17 or r == 25


def z18_candidate_P(x, r):
    if x <= 15:
        return x >= 4 and x % 2 == 0 and r >= x + 4
    if x == 16:
        return r in (19, 21) or r >= 22
    if x == 17:
        return r in (19, 21)
    if x in (18, 20):
        return r in (19, 21) or r >= 23
    if x == 19:
        return r in (19, 21)
    if x == 21:
        return r in (19, 21, 23)
    if x == 22:
        return (r in (19, 21, 23) or (r % 2 == 0 and 26 <= r <= 42) or r >= 44)
    upper = x + 20 if x % 2 == 0 else x + 21
    return (r in (19, 21, 23) or (r % 2 == 0 and 26 <= r <= upper)
            or (x % 2 == 0 and r >= x + 22))


def z18_candidate(x, R):
    if R == 0:
        return 0
    if R >= x + 22:
        return (x + 3) % 2
    if z18_candidate_T(x, R):
        return 2
    if z18_candidate_P(x, R):
        return 1
    return 0


def z19_candidate_T(x, R):
    if x <= 15:
        return R % 2 == 1 and R <= 2 * (x // 2) + 3
    if x == 16:
        return R % 2 == 1 and R <= 21
    if x in (17, 19, 20, 21):
        return R % 2 == 1 and R <= 19
    if x == 18:
        return (R % 2 == 1 and R <= 19) or R == 23
    if x == 22:
        return (R % 2 == 1 and R <= 19) or R == 25
    if x == 23:
        return (R % 2 == 1 and R <= 19) or (R % 2 == 1 and 25 <= R <= 45)
    return (R % 2 == 1 and R <= 19) or R == 25


def z19_candidate_P(x, R):
    if x % 2 == 1 and x <= 15:
        return False
    if x % 2 == 0 and x <= 14:
        return R >= x + 4
    if x == 16:
        return R == 20 or R >= 22
    if x == 17:
        return R in (20, 22)
    if x == 18:
        return R in (20, 22) or R >= 24
    if x == 19:
        return R in (20, 22)
    if x == 20:
        return R in (20, 22) or R >= 24
    if x == 21:
        return R in (20, 22, 24)
    if x == 22:
        return R in (20, 22, 24) or R >= 26
    if x == 23:
        return R in (20, 22, 24)
    band = R % 2 == 1 and 27 <= R <= q_odd(x + 22)
    tail = x % 2 == 0 and R >= x + 23
    return R in (20, 22, 24) or band or tail


def z19_candidate(x, R):
    t = z19_candidate_T(x, R)
    p = z19_candidate_P(x, R)
    assert not (t and p), ("z19 anchor overlap", x, R)
    if R == 0:
        return 0
    if t:
        return 2
    return 1 if p else 0


# ------------------------------------------------------------------
# Closed-form identity (option decomposition, no raw recursion).
# ------------------------------------------------------------------
def opts_closed(z, x, R):
    """Closed-form option values of H(R, (x,3), z). R >= 1."""
    if x == 3:
        A = cand2(z, 3, R - 1)   # both token moves coincide at (3,3)
    else:
        A = cand3(z, x - 1, R - 1)
    B = cand2(z, x, R - 1)
    out = [A, B]
    if z >= 1:
        out.append(1 ^ cand3(z - 1, x, R - 1))
    return out


def identity_ok(z, x, R):
    """cand3(z,x,R) == mex of closed-form children. R >= 1."""
    got = mex(opts_closed(z, x, R))
    want = cand3(z, x, R)
    return got == want, got, want


def merge_ok(z, x, R):
    """Merge-below-diagonal corollary: x <= z-4 => single token."""
    if x > z - 4:
        return True
    return cand3(z, x, R) == single_token(x + 3, z, R)


# ------------------------------------------------------------------
# Type machine.
# ------------------------------------------------------------------
CLIP = 8
SENT = 9
B_V = 60


def clip(w):
    if w > CLIP:
        return SENT
    if w < -CLIP:
        return -SENT
    return w


def type_of(z, x, R):
    return (1 if x == 3 else 0,
            1 if z == 0 else 0,
            z % 2, x % 2, R % 2,
            clip(x - z), clip(R - x), clip(R - z),
            clip(R - x - z), clip(R - 2 * x), clip(R - 2 * z))


def eff(z, x, R):
    """Effect vector: the value plus the closed-form option values."""
    return (cand3(z, x, R), tuple(sorted(opts_closed(z, x, R))))


def vpoint(v0, v1, v3):
    z = v1 - v3
    x = v0 + v1 - v3
    R = v0 + 2 * v1 - v3
    return z, x, R


# ------------------------------------------------------------------
# Checks.
# ------------------------------------------------------------------
def check_c1():
    pts = 0
    mismatch = []
    for z in range(0, 15):
        for x in range(3, 27):
            for R in range(0, x + z + 46):
                a = H_ordered(R, (x, 3), z)
                b = H_canonical(R, (x, 3), z)
                c = cand3(z, x, R)
                if a != b or a != c:
                    mismatch.append((z, x, R, a, b, c))
                    if len(mismatch) >= 10:
                        return mismatch, pts
                pts += 1
    return mismatch, pts


def check_c1b():
    st_pts = st_bad = 0
    for z in range(0, 31):
        for x in range(1, 31):
            for R in range(0, 2 * x + z + 11):
                a = H_ordered(R, (x,), z)
                if a != single_token(x, z, R):
                    st_bad += 1
                st_pts += 1
    b_pts = b_bad = 0
    for z in range(0, 31):
        for x in range(2, 31):
            for R in range(1, x + z + 31):
                a = H_ordered(R - 1, (x, 2), z)
                if a != cand2(z, x, R - 1):
                    b_bad += 1
                b_pts += 1
    # x==3 coincidence: (2,3) and (3,2) are the same multiset.
    co_pts = co_bad = 0
    for z in range(0, 25):
        for R in range(1, z + 33):
            a = H_ordered(R, (2, 3), z)
            b = H_ordered(R, (3, 2), z)
            c = cand2(z, 3, R)
            if a != b or a != c:
                co_bad += 1
            co_pts += 1
    return {"single_token_points": st_pts, "single_token_mismatches": st_bad,
            "y2_child_points": b_pts, "y2_child_mismatches": b_bad,
            "x3_coincidence_points": co_pts, "x3_coincidence_mismatches": co_bad}


def check_c1d():
    out = {}
    for name, zz, pub in (("z18_k1078", 18, z18_candidate),
                          ("z19_k1098", 19, z19_candidate)):
        pts = 0
        bad = []
        for x in range(3, 65):
            for R in range(0, x + 51):
                if cand3(zz, x, R) != pub(x, R):
                    bad.append((x, R))
                    if len(bad) >= 10:
                        break
                pts += 1
            if len(bad) >= 10:
                break
        out[name] = {"points": pts, "mismatches_total_prefix": bad[:10]}
    return out


def check_c2():
    pts = 0
    bad = []
    mpts = mbad = 0
    for z in range(0, 49):
        for x in range(3, 57):
            for R in range(1, x + z + 41):
                ok, got, want = identity_ok(z, x, R)
                pts += 1
                if not ok:
                    bad.append((z, x, R, got, want))
                    if len(bad) >= 10:
                        return pts, bad, mpts, mbad
                if x <= z - 4:
                    mpts += 1
                    if not merge_ok(z, x, R):
                        mbad += 1
    return pts, bad, mpts, mbad


def check_c2b():
    pts = 0
    bad = []
    mpts = mbad = 0
    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(3, 41, 3):
            for R in range(1, x + z + 31, 2):
                ok, got, want = identity_ok(z, x, R)
                pts += 1
                if not ok:
                    bad.append((z, x, R, got, want))
                    if len(bad) >= 10:
                        return pts, bad, mpts, mbad
                if x <= z - 4:
                    mpts += 1
                    if not merge_ok(z, x, R):
                        mbad += 1
    return pts, bad, mpts, mbad


def check_c3():
    """Raw engine option values vs the closed-form child identification."""
    pts = 0
    bad = []
    for z in range(0, 7):
        for x in range(3, 11):
            for R in range(1, x + z + 21):
                engine_opts = set()
                X = (x, 3)
                for i, v in enumerate(X):
                    if v > 1:
                        engine_opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
                    else:
                        engine_opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
                if z >= 1:
                    engine_opts.add(1 ^ H_ordered(R - 1, X, z - 1))
                closed = set(opts_closed(z, x, R))
                pts += 1
                if engine_opts != closed:
                    bad.append((z, x, R, sorted(engine_opts), sorted(closed)))
                    if len(bad) >= 10:
                        return pts, bad
    return pts, bad


def check_c4():
    """Box sweep: full identity, type collection, confluence."""
    types = {}
    points = 0
    ident_bad = []
    conf_bad = []
    m_bad = []
    m_pts = 0
    for v0 in range(-B_V, B_V + 1):
        for v1 in range(-B_V, B_V + 1):
            for v3 in range(-B_V, B_V + 1):
                z, x, R = vpoint(v0, v1, v3)
                if z < 0 or x < 3 or R < 1:
                    continue
                points += 1
                ok, got, want = identity_ok(z, x, R)
                if not ok:
                    ident_bad.append((z, x, R, got, want))
                    if len(ident_bad) >= 10:
                        return (points, len(types), ident_bad, conf_bad, m_pts, m_bad)
                if x <= z - 4:
                    m_pts += 1
                    if not merge_ok(z, x, R):
                        m_bad.append((z, x, R))
                        if len(m_bad) >= 10:
                            return (points, len(types), ident_bad, conf_bad, m_pts, m_bad)
                t = type_of(z, x, R)
                e = eff(z, x, R)
                if t not in types:
                    types[t] = (z, x, R, e)
                elif types[t][3] != e:
                    conf_bad.append((types[t][0], types[t][1], types[t][2],
                                     z, x, R, types[t][3], e))
                    if len(conf_bad) >= 10:
                        return (points, len(types), ident_bad, conf_bad, m_pts, m_bad)
    return points, len(types), ident_bad, conf_bad, m_pts, m_bad


def check_c7(types):
    rng = random.Random(20261120)
    pts = 0
    ident_bad = []
    conf_bad = []
    new_types = []
    m_pts = m_bad = 0
    for i in range(200000):
        z = rng.randint(0, 3000)
        x = rng.randint(3, 3000)
        m = i % 4
        if m == 1:
            R = x + z + rng.randint(-4, 6)
        elif m == 2:
            x = max(3, z + rng.randint(-12, 5))
            R = rng.randint(1, x + z + 3)
        elif m == 3:
            R = rng.randint(1, 4)
        else:
            R = rng.randint(1, 9000)
        if R < 1:
            continue
        pts += 1
        ok, got, want = identity_ok(z, x, R)
        if not ok:
            ident_bad.append((z, x, R, got, want))
            if len(ident_bad) >= 10:
                break
        if x <= z - 4:
            m_pts += 1
            if not merge_ok(z, x, R):
                m_bad += 1
        t = type_of(z, x, R)
        if t not in types:
            new_types.append((z, x, R))
            if len(new_types) >= 10:
                break
        elif types[t][3] != eff(z, x, R):
            conf_bad.append((z, x, R))
            if len(conf_bad) >= 10:
                break
    return pts, ident_bad, new_types, conf_bad, m_pts, m_bad


def check_c8(types):
    pts = 0
    ident_bad = []
    new_types = []
    conf_bad = []
    tail_bad = []
    m_pts = m_bad = 0
    zset = (0, 1, 2, 3, 4, 5, 29, 30, 31, 59, 60, 61, 299, 300, 301,
            999, 1000, 1001, 2999, 3000)
    for z in zset:
        for dx in range(-12, 7):
            x = z + dx
            if x < 3:
                continue
            for R in range(1, x + z + 27):
                pts += 1
                ok, got, want = identity_ok(z, x, R)
                if not ok:
                    ident_bad.append((z, x, R, got, want))
                    if len(ident_bad) >= 10:
                        return pts, ident_bad, new_types, conf_bad, tail_bad, m_pts, m_bad
                if x <= z - 4:
                    m_pts += 1
                    if not merge_ok(z, x, R):
                        m_bad += 1
                t = type_of(z, x, R)
                if t not in types:
                    new_types.append((z, x, R))
                    if len(new_types) >= 10:
                        return pts, ident_bad, new_types, conf_bad, tail_bad, m_pts, m_bad
                elif types[t][3] != eff(z, x, R):
                    conf_bad.append((z, x, R))
                    if len(conf_bad) >= 10:
                        return pts, ident_bad, new_types, conf_bad, tail_bad, m_pts, m_bad
                if x + z + 4 <= R <= x + z + 6:
                    if cand3(z, x, R) != (x + 3) % 2:
                        tail_bad.append((z, x, R))
    return pts, ident_bad, new_types, conf_bad, tail_bad, m_pts, m_bad


def check_c9(types):
    pts = 0
    bad = []
    new_types = []
    conf_bad = []
    m_pts = m_bad = 0
    bands = ((61, 64), (89, 92), (117, 120))
    for lo, hi in bands:
        for v0 in range(-hi, hi + 1):
            for v1 in range(-hi, hi + 1):
                for v3 in range(-hi, hi + 1):
                    m = max(abs(v0), abs(v1), abs(v3))
                    if m < lo or m > hi:
                        continue
                    z, x, R = vpoint(v0, v1, v3)
                    if z < 0 or x < 3 or R < 1:
                        continue
                    pts += 1
                    ok, got, want = identity_ok(z, x, R)
                    if not ok:
                        bad.append((z, x, R, got, want))
                        if len(bad) >= 10:
                            return pts, bad, new_types, conf_bad, m_pts, m_bad
                    if x <= z - 4:
                        m_pts += 1
                        if not merge_ok(z, x, R):
                            m_bad += 1
                    t = type_of(z, x, R)
                    if t not in types:
                        new_types.append((z, x, R))
                        if len(new_types) >= 10:
                            return pts, bad, new_types, conf_bad, m_pts, m_bad
                    elif types[t][3] != eff(z, x, R):
                        conf_bad.append((z, x, R))
                        if len(conf_bad) >= 10:
                            return pts, bad, new_types, conf_bad, m_pts, m_bad
    return pts, bad, new_types, conf_bad, m_pts, m_bad


def check_c12():
    pts = 0
    bad = []
    m_pts = m_bad = 0
    badm = []
    for z in range(0, 121):
        for x in range(3, 121):
            for R in range(1, x + z + 17):
                ok, got, want = identity_ok(z, x, R)
                pts += 1
                if not ok:
                    bad.append((z, x, R, got, want))
                    if len(bad) >= 10:
                        return pts, bad, m_pts, m_bad, badm
                if x <= z - 4:
                    m_pts += 1
                    if not merge_ok(z, x, R):
                        m_bad += 1
                        badm.append((z, x, R))
                        if len(badm) >= 10:
                            return pts, bad, m_pts, m_bad, badm
    return pts, bad, m_pts, m_bad, badm


def main():
    audit = {
        "verifier": "verify_y3_universal",
        "family": "two-token y=3 residual, parametric in z (all z >= 0)",
        "claim": "for all z>=0, x>=3, R>=0: H(R,(x,3),z) == cand3(z,x,R)",
        "corollaries": {
            "merge_below_diagonal_y3": "x<=z-4 (S=x+3<z) implies "
                                       "H(R,(x,3),z) == single_token(x+3,z,R)",
            "tail": "R>=x+z+4 implies H == (x+3) % 2",
        },
    }
    checks = {}

    m, pts = check_c1()
    checks["c1_engine_vs_cand3"] = {
        "grid": "z=0..14, x=3..26, R<=x+z+45",
        "points": pts, "mismatches": m,
    }

    checks["c1b_child_anchors"] = check_c1b()

    checks["c1d_published_z18_z19"] = check_c1d()

    pts, bad, mpts, mbad = check_c2()
    checks["c2_identity_grid"] = {
        "grid": "z=0..48, x=3..56, R<=x+z+40",
        "points": pts, "mismatches": bad,
        "merge_points": mpts, "merge_mismatches": mbad,
    }

    pts, bad, mpts, mbad = check_c2b()
    checks["c2b_deep_tail"] = {
        "z_values": [60, 72, 84, 96, 108, 120, 240, 400],
        "points": pts, "mismatches": bad,
        "merge_points": mpts, "merge_mismatches": mbad,
    }

    pts, bad = check_c3()
    checks["c3_option_decomposition_anchor"] = {
        "points": pts, "mismatches": bad,
    }

    points, ntypes, ident_bad, conf_bad, mpts, m_bad = check_c4()
    checks["c4_type_machine_box"] = {
        "box_bound": B_V, "clip": CLIP, "sentinel": SENT,
        "type_fields": "x==3, z==0, z%2, x%2, R%2, clipped w0..w5",
        "valid_points": points, "realized_types": ntypes,
        "witness_identity_mismatches": ident_bad,
        "confluence_mismatches": conf_bad,
        "merge_points": mpts, "merge_mismatches": m_bad,
    }

    # rebuild the type table for later checks
    types = {}
    for v0 in range(-B_V, B_V + 1):
        for v1 in range(-B_V, B_V + 1):
            for v3 in range(-B_V, B_V + 1):
                z, x, R = vpoint(v0, v1, v3)
                if z < 0 or x < 3 or R < 1:
                    continue
                t = type_of(z, x, R)
                if t not in types:
                    types[t] = (z, x, R, eff(z, x, R))

    pts, ident_bad, new_types, conf_bad, mpts, m_bad = check_c7(types)
    checks["c7_seeded_far_probes"] = {
        "seed": 20261120, "n": 200000,
        "z_max": 3000, "x_max": 3000, "R_max": 9000,
        "points": pts, "identity_mismatches": ident_bad,
        "new_types": new_types, "confluence_mismatches": conf_bad,
        "merge_points": mpts, "merge_mismatches": m_bad,
    }

    pts, ident_bad, new_types, conf_bad, tail_bad, mpts, m_bad = check_c8(types)
    checks["c8_boundary_manifolds"] = {
        "points": pts, "identity_mismatches": ident_bad,
        "new_types": new_types, "confluence_mismatches": conf_bad,
        "tail_value_mismatches": tail_bad,
        "merge_points": mpts, "merge_mismatches": m_bad,
    }

    pts, bad, new_types, conf_bad, mpts, m_bad = check_c9(types)
    checks["c9_shell_sweep"] = {
        "bands": [[61, 64], [89, 92], [117, 120]],
        "points": pts, "identity_mismatches": bad,
        "new_types": new_types, "confluence_mismatches": conf_bad,
        "merge_points": mpts, "merge_mismatches": m_bad,
    }

    pts, bad, mpts, mbad, badm = check_c12()
    checks["c12_deep_grid_sweep"] = {
        "grid": "z=0..120, x=3..120, R<=x+z+16",
        "points": pts, "mismatches": bad,
        "merge_points": mpts, "merge_mismatches": mbad,
        "merge_mismatches_prefix": badm,
    }

    def is_fail(c):
        if isinstance(c, dict):
            return any(is_fail(v) for v in c.values())
        if isinstance(c, list):
            return len(c) > 0
        return False

    ok = True
    for name, c in checks.items():
        if name == "c1d_published_z18_z19":
            for zz, d in c.items():
                if d["mismatches_total_prefix"]:
                    ok = False
        else:
            for k, v in c.items():
                if "mismatch" in k or k in ("new_types", "tail_bad"):
                    if is_fail(v):
                        ok = False
    audit["checks"] = checks
    audit["total_points"] = sum(
        c.get("points", 0) for c in checks.values()
        if isinstance(c, dict) and isinstance(c.get("points", None), int))
    audit["total_merge_points"] = sum(
        c.get("merge_points", 0) for c in checks.values()
        if isinstance(c, dict) and isinstance(c.get("merge_points", 0), int))
    audit["overall"] = "PASS" if ok else "FAIL"
    audit["verifier_sha256"] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()

    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(audit, indent=2, sort_keys=True, ensure_ascii=False)
    (out / "audit.json").write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
