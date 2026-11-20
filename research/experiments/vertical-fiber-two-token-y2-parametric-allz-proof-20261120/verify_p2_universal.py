#!/usr/bin/env python3
"""Universal verifier for the two-token y=2 parametric family, all z.

Claim under test (proposition K, "y=2 parametric all-z"):
  For all z >= 0, x >= 2, R >= 0:
      H(R; (x, 2); z) == cand2(z, x, R)
  where H is the common circular-fiber two-token residual game value
  (defined by the raw engines below), and cand2 is the closed form
  transcribed in this file.

Method (mirrors verify_p1_universal.py of K1023, adapted to y=2):

  C1   Raw engines (order-preserving and descending-canonical double
       recursion) vs cand2 on z=0..14, x=2..26, R<=x+z+45.
  C1b  Engine anchors for the closed-form children used downstream:
       single_token vs raw single-token engine; the y=1 child
       H(R-1,(x,1),z) vs the K1023 closed form cand_y1_allz; and the
       x==2 coincidence H(R,(1,2),z) == H(R,(2,1),z) == cand(2, R-1).
  C1d  Verbatim anchors against previously published per-z theorems:
       the z=16 and z=17, y=2 census candidates (K1042/K1051 family)
       must agree with cand2 pointwise on x=2..64, R<=x+50.
  C2   Closed-form-only identity grid: mex of the closed-form children
       == cand2, over z=0..48, x=2..56, R<=x+z+40, plus deep-tail z.
  C3   Option-decomposition anchor: the closed-form children chosen in
       the identity equal the raw option-value sets of the engine.
  C4   Type machine over the v-space box (v0,v1,v3 in [-60,60]):
       every point gets a type (x==2 bit, z==0 bit, parities, clipped
       differential family w=x-z, R-x, R-z, R-x-z, R-2x, R-2z within
       +-8, sentinel +-9); confluence of the effect vector
       (value, option values) within each realized type; per-type
       witness identity; and full-box identity as a cross-check.
  C7   Seeded far probes (deterministic RNG): 200k points with
       z,x <= 3000, R <= 9000, biased toward the boundary manifolds.
  C8   Boundary-manifold sweeps at z in {0..5, 29..31, 59..61, 299..301,
       999..1001, 2999, 3000}, x in z-12..z+6, R<=x+z+26.
  C9   Type-machine shell sweep in v-space bands [61,64], [89,92],
       [117,120] of max|v|: no new types, confluence, identity.
  C12  Deep grid sweep z=0..120, x=2..120, R<=x+z+16: identity.

Everything is deterministic. Two runs produce byte-identical
output/audit.json (no timestamps, seeded RNG, sorted JSON keys).
"""
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
# Raw engines (verbatim from the published z=16/z=17 census files).
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
# Published single-token closed form (engine-independent, K0832 line).
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
# Published y=1 two-token parametric closed form (K1023, verbatim).
# ------------------------------------------------------------------
def cand_y1(z, x, R):
    if R == 0:
        return 0
    if x < 1:
        return 0
    S = x + 1 + z
    if z % 2 == 0:
        if x % 2 == 0 and 2 <= x <= z - 2:
            T = (R % 2 == 1 and R <= x + 1)
        elif x % 2 == 1 and x <= z - 3:
            T = (R % 2 == 1 and R <= x)
        elif x == z - 1:
            T = (R % 2 == 1 and R <= z + 1)
        elif x in (z, z + 1):
            T = (R % 2 == 1 and R <= z - 1)
        elif x == z + 2:
            T = (R % 2 == 1 and (R <= z - 1 or z + 3 <= R <= 2 * z + 3))
        else:
            T = (R == z + 3 or (R % 2 == 1 and R <= z - 1))
        if x % 2 == 1 and x <= z - 1:
            P = False
        elif x % 2 == 0 and x <= z - 2:
            P = (R >= x + 2)
        elif x == z:
            P = (R >= z + 1)
        elif x == z + 1:
            P = (R == z + 1)
        elif x % 2 == 0:
            P = (R == z + 1 or (R % 2 == 0 and z + 4 <= R <= S - 1) or R >= S + 1)
        else:
            P = (R == z + 1 or (R % 2 == 0 and z + 4 <= R <= S))
    else:
        if x % 2 == 0 and x <= z - 1:
            T = (R % 2 == 1 and R <= x + 1)
        elif x % 2 == 1 and x <= z:
            T = (R % 2 == 1 and R <= x)
        elif x == z + 1:
            T = (R % 2 == 1 and R <= z + 2)
        elif x == z + 2:
            T = (R % 2 == 1 and R <= 2 * z + 3)
        else:
            T = (R == z + 2 or (R % 2 == 1 and R <= z))
        if x % 2 == 1 and x <= z - 2:
            P = False
        elif x % 2 == 0 and x <= z - 1:
            P = (R >= x + 2)
        elif x == z:
            P = (R == z + 1)
        elif x == z + 1:
            P = (R == z + 1 or R >= z + 3)
        elif x == z + 2:
            P = (R == z + 1)
        elif x % 2 == 1:
            P = (R == z + 1 or (R % 2 == 1 and z + 4 <= R <= S))
        else:
            P = (R == z + 1 or (R % 2 == 1 and z + 4 <= R <= S) or R >= S + 1)
    assert not (T and P), (z, x, R)
    return 2 if T else (1 if P else 0)


def cand0_y1(x, R):
    """Published y=1 z=0 base closed form (K1023, cand0)."""
    if R == 0 or x < 1:
        return 0
    if x == 1:
        return 1 if R == 1 else 0
    if R == 3:
        return 2
    if x % 2 == 1:
        return 1 if (R == 1 or (R % 2 == 0 and 4 <= R <= x + 1)) else 0
    return 1 if (R == 1 or (R % 2 == 0 and 4 <= R <= x) or R >= x + 2) else 0


def cand_y1_allz(z, x, R):
    if R == 0:
        return 0
    if z == 0:
        return cand0_y1(x, R)
    return cand_y1(z, x, R)


# ------------------------------------------------------------------
# Candidate under test: y=2 two-token parametric closed form, all z.
# ------------------------------------------------------------------
def cand2_T(z, x):
    """Value-2 position data as (kind, lo, hi, extra)."""
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


def in_T(z, x, R):
    if R <= 0:
        return False
    kind, lo, hi, extra = cand2_T(z, x)
    if kind in ("ladder", "band"):
        return lo <= R <= hi and R % 2 == 1
    if kind == "pin":
        return (lo <= R <= hi and R % 2 == 1) or R == extra
    a, b = extra
    return (lo <= R <= hi and R % 2 == 1) or (a <= R <= b and R % 2 == 1)


def in_P(z, x, R):
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
    t = in_T(z, x, R)
    pv = in_P(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    if R == 0:
        return 0
    if t:
        return 2
    return 1 if pv else 0


# ------------------------------------------------------------------
# Verbatim published per-z candidates (z=16 and z=17, y=2), used as
# independent anchors (transcribed unchanged from the census files).
# ------------------------------------------------------------------
def z16_candidate_T(x, r):
    if x == 2:
        return r in (1, 3)
    if x in (3, 4):
        return 1 <= r <= 5 and r % 2 == 1
    if x in (5, 6):
        return 1 <= r <= 7 and r % 2 == 1
    if x in (7, 8):
        return 1 <= r <= 9 and r % 2 == 1
    if x in (9, 10):
        return 1 <= r <= 11 and r % 2 == 1
    if x in (11, 12):
        return 1 <= r <= 13 and r % 2 == 1
    if x == 14:
        return 1 <= r <= 17 and r % 2 == 1
    if x == 16:
        return (1 <= r <= 15 and r % 2 == 1) or r == 19
    if x == 19:
        return r % 2 == 1 and (1 <= r <= 15 or 21 <= r <= 37)
    if x >= 20:
        return r in (1, 3, 5, 7, 9, 11, 13, 15, 21)
    return 1 <= r <= 15 and r % 2 == 1


def z16_candidate_P(x, r):
    if x % 2 == 0 and x <= 14:
        return False
    if x % 2 == 1 and x <= 13:
        return r >= x + 3
    if x in (15, 17):
        return r in (17, 19) or r >= 20
    if x == 16:
        return r == 17
    if x == 18:
        return r in (17, 19)
    if x % 2 == 1:
        return r in (17, 19) or (r % 2 == 0 and 22 <= r <= x + 19) or r >= x + 20
    return r in (17, 19) or (r % 2 == 0 and 22 <= r <= x + 18)


def z16_candidate(x, R):
    if R == 0:
        return 0
    if z16_candidate_T(x, R):
        return 2
    return 1 if z16_candidate_P(x, R) else 0


def z17_candidate_T(x, r):
    if x == 2:
        return r in (1, 3)
    if x in (3, 4):
        return 1 <= r <= 5 and r % 2 == 1
    if x in (5, 6):
        return 1 <= r <= 7 and r % 2 == 1
    if x in (7, 8):
        return 1 <= r <= 9 and r % 2 == 1
    if x in (9, 10):
        return 1 <= r <= 11 and r % 2 == 1
    if x in (11, 12):
        return 1 <= r <= 13 and r % 2 == 1
    if x in (13, 14):
        return 1 <= r <= 15 and r % 2 == 1
    if x == 15:
        return 1 <= r <= 19 and r % 2 == 1
    if x == 19:
        return (1 <= r <= 17 and r % 2 == 1) or r == 21
    if x == 20:
        return (r % 2 == 1 and (1 <= r <= 17 or 21 <= r <= 39))
    if x >= 21:
        return (1 <= r <= 17 and r % 2 == 1) or r == 21
    return 1 <= r <= 17 and r % 2 == 1


def z17_candidate_P(x, r):
    if x % 2 == 0 and x <= 14:
        return False
    if x % 2 == 1 and x <= 13:
        return r >= x + 3
    if x == 15:
        return r in (18, 20) or r >= 21
    if x == 16:
        return r == 18
    if x == 17:
        return r in (18, 20) or r >= 21
    if x == 18:
        return r in (18, 20)
    if x == 19:
        return r in (18, 20) or r >= 22
    if x == 20:
        return r in (18, 20)
    if x % 2 == 1:
        return (r in (18, 20)
                or (r % 2 == 1 and 23 <= r <= x + 20)
                or r >= x + 21)
    return r in (18, 20) or (r % 2 == 1 and 23 <= r <= x + 19)


def z17_candidate(x, R):
    assert not (z17_candidate_T(x, R) and z17_candidate_P(x, R)), (x, R)
    if R == 0:
        return 0
    if z17_candidate_T(x, R):
        return 2
    return 1 if z17_candidate_P(x, R) else 0


# ------------------------------------------------------------------
# Closed-form identity (option decomposition, no raw recursion).
# ------------------------------------------------------------------
def opts_closed(z, x, R):
    """Closed-form option values of H(R, (x,2), z). R >= 1."""
    if x == 2:
        A = cand_y1_allz(z, 2, R - 1)   # both token moves coincide at (2,2)
    else:
        A = cand2(z, x - 1, R - 1)
    B = cand_y1_allz(z, x, R - 1)
    out = [A, B]
    if z >= 1:
        out.append(1 ^ cand2(z - 1, x, R - 1))
    return out


def identity_ok(z, x, R):
    """cand2(z,x,R) == mex of closed-form children. R >= 1."""
    got = mex(opts_closed(z, x, R))
    return got == cand2(z, x, R), got, cand2(z, x, R)


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
    return (1 if x == 2 else 0,
            1 if z == 0 else 0,
            z % 2, x % 2, R % 2,
            clip(x - z), clip(R - x), clip(R - z),
            clip(R - x - z), clip(R - 2 * x), clip(R - 2 * z))


def eff(z, x, R):
    """Effect vector: the value plus the closed-form option values."""
    return (cand2(z, x, R), tuple(sorted(opts_closed(z, x, R))))


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
        for x in range(2, 27):
            for R in range(0, x + z + 46):
                a = H_ordered(R, (x, 2), z)
                b = H_canonical(R, (x, 2), z)
                c = cand2(z, x, R)
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
                a = H_ordered(R - 1, (x, 1), z)
                if a != cand_y1_allz(z, x, R - 1):
                    b_bad += 1
                b_pts += 1
    # x==2 coincidence: (1,2) and (2,1) are the same multiset.
    co_pts = co_bad = 0
    for z in range(0, 25):
        for R in range(1, z + 33):
            a = H_ordered(R, (1, 2), z)
            b = H_ordered(R, (2, 1), z)
            c = cand_y1_allz(z, 2, R)
            if a != b or a != c:
                co_bad += 1
            co_pts += 1
    return {"single_token_points": st_pts, "single_token_mismatches": st_bad,
            "y1_child_points": b_pts, "y1_child_mismatches": b_bad,
            "x2_coincidence_points": co_pts, "x2_coincidence_mismatches": co_bad}


def check_c1d():
    out = {}
    for name, zz, pub in (("z16", 16, z16_candidate), ("z17", 17, z17_candidate)):
        pts = 0
        bad = []
        for x in range(2, 65):
            for R in range(0, x + 51):
                if cand2(zz, x, R) != pub(x, R):
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
    for z in range(0, 49):
        for x in range(2, 57):
            for R in range(1, x + z + 41):
                ok, got, want = identity_ok(z, x, R)
                pts += 1
                if not ok:
                    bad.append((z, x, R, got, want))
                    if len(bad) >= 10:
                        return pts, bad
    return pts, bad


def check_c2b():
    pts = 0
    bad = []
    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(2, 41, 3):
            for R in range(1, x + z + 31, 2):
                ok, got, want = identity_ok(z, x, R)
                pts += 1
                if not ok:
                    bad.append((z, x, R, got, want))
                    if len(bad) >= 10:
                        return pts, bad
    return pts, bad


def check_c3():
    """Raw engine option values vs the closed-form child identification."""
    pts = 0
    bad = []
    for z in range(0, 7):
        for x in range(2, 11):
            for R in range(1, x + z + 21):
                engine_opts = set()
                X = (x, 2)
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
    """Box sweep: full identity, type collection, confluence, witness."""
    types = {}
    points = 0
    ident_bad = []
    conf_bad = []
    new_shell_types = 0
    for v0 in range(-B_V, B_V + 1):
        for v1 in range(-B_V, B_V + 1):
            for v3 in range(-B_V, B_V + 1):
                z, x, R = vpoint(v0, v1, v3)
                if z < 0 or x < 2 or R < 1:
                    continue
                points += 1
                ok, got, want = identity_ok(z, x, R)
                if not ok:
                    ident_bad.append((z, x, R, got, want))
                    if len(ident_bad) >= 10:
                        return (points, len(types), ident_bad, conf_bad, new_shell_types)
                t = type_of(z, x, R)
                e = eff(z, x, R)
                if t not in types:
                    types[t] = (z, x, R, e)
                elif types[t][3] != e:
                    conf_bad.append((types[t][0], types[t][1], types[t][2],
                                     z, x, R, types[t][3], e))
                    if len(conf_bad) >= 10:
                        return (points, len(types), ident_bad, conf_bad, new_shell_types)
    # witness identity per type (full box identity already checked; this
    # records the per-type witness used by the confluence argument).
    return points, len(types), ident_bad, conf_bad, new_shell_types


def check_c7(types):
    rng = random.Random(20261120)
    pts = 0
    ident_bad = []
    conf_bad = []
    new_types = []
    for i in range(200000):
        z = rng.randint(0, 3000)
        x = rng.randint(2, 3000)
        m = i % 4
        if m == 1:
            R = x + z + rng.randint(-4, 6)
        elif m == 2:
            x = max(2, z + rng.randint(-12, 5))
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
        t = type_of(z, x, R)
        if t not in types:
            new_types.append((z, x, R))
            if len(new_types) >= 10:
                break
        elif types[t][3] != eff(z, x, R):
            conf_bad.append((z, x, R))
            if len(conf_bad) >= 10:
                break
    return pts, ident_bad, new_types, conf_bad


def check_c8(types):
    pts = 0
    ident_bad = []
    new_types = []
    conf_bad = []
    tail_bad = []
    zset = (0, 1, 2, 3, 4, 5, 29, 30, 31, 59, 60, 61, 299, 300, 301,
            999, 1000, 1001, 2999, 3000)
    for z in zset:
        for dx in range(-12, 7):
            x = z + dx
            if x < 2:
                continue
            for R in range(1, x + z + 27):
                pts += 1
                ok, got, want = identity_ok(z, x, R)
                if not ok:
                    ident_bad.append((z, x, R, got, want))
                    if len(ident_bad) >= 10:
                        return pts, ident_bad, new_types, conf_bad, tail_bad
                t = type_of(z, x, R)
                if t not in types:
                    new_types.append((z, x, R))
                    if len(new_types) >= 10:
                        return pts, ident_bad, new_types, conf_bad, tail_bad
                elif types[t][3] != eff(z, x, R):
                    conf_bad.append((z, x, R))
                    if len(conf_bad) >= 10:
                        return pts, ident_bad, new_types, conf_bad, tail_bad
                if R >= x + z + 3 and R <= x + z + 5:
                    if cand2(z, x, R) != (x + 2) % 2:
                        tail_bad.append((z, x, R))
    # tail claim plus deep-manifold value probe without identity grid
    return pts, ident_bad, new_types, conf_bad, tail_bad


def check_c9(types):
    pts = 0
    bad = []
    new_types = []
    conf_bad = []
    bands = ((61, 64), (89, 92), (117, 120))
    for lo, hi in bands:
        for v0 in range(-hi, hi + 1):
            for v1 in range(-hi, hi + 1):
                for v3 in range(-hi, hi + 1):
                    m = max(abs(v0), abs(v1), abs(v3))
                    if m < lo or m > hi:
                        continue
                    z, x, R = vpoint(v0, v1, v3)
                    if z < 0 or x < 2 or R < 1:
                        continue
                    pts += 1
                    ok, got, want = identity_ok(z, x, R)
                    if not ok:
                        bad.append((z, x, R, got, want))
                        if len(bad) >= 10:
                            return pts, bad, new_types, conf_bad
                    t = type_of(z, x, R)
                    if t not in types:
                        new_types.append((z, x, R))
                        if len(new_types) >= 10:
                            return pts, bad, new_types, conf_bad
                    elif types[t][3] != eff(z, x, R):
                        conf_bad.append((z, x, R))
                        if len(conf_bad) >= 10:
                            return pts, bad, new_types, conf_bad
    return pts, bad, new_types, conf_bad


def check_c12():
    pts = 0
    bad = []
    for z in range(0, 121):
        for x in range(2, 121):
            for R in range(1, x + z + 17):
                ok, got, want = identity_ok(z, x, R)
                pts += 1
                if not ok:
                    bad.append((z, x, R, got, want))
                    if len(bad) >= 10:
                        return pts, bad
    return pts, bad


def main():
    audit = {
        "verifier": "verify_p2_universal",
        "family": "two-token y=2 residual, parametric in z (all z >= 0)",
        "claim": "for all z>=0, x>=2, R>=0: H(R,(x,2),z) == cand2(z,x,R)",
    }
    checks = {}

    m, pts = check_c1()
    checks["c1_engine_vs_cand2"] = {
        "grid": "z=0..14, x=2..26, R<=x+z+45",
        "points": pts, "mismatches": m,
    }

    checks["c1b_child_anchors"] = check_c1b()

    checks["c1d_published_z16_z17"] = check_c1d()

    pts, bad = check_c2()
    checks["c2_identity_grid"] = {
        "grid": "z=0..48, x=2..56, R<=x+z+40",
        "points": pts, "mismatches": bad,
    }

    pts, bad = check_c2b()
    checks["c2b_deep_tail"] = {
        "z_values": [60, 72, 84, 96, 108, 120, 240, 400],
        "points": pts, "mismatches": bad,
    }

    pts, bad = check_c3()
    checks["c3_option_decomposition_anchor"] = {
        "points": pts, "mismatches": bad,
    }

    points, ntypes, ident_bad, conf_bad, _ = check_c4()
    # rebuild the type table for later checks
    types = {}
    for v0 in range(-B_V, B_V + 1):
        for v1 in range(-B_V, B_V + 1):
            for v3 in range(-B_V, B_V + 1):
                z, x, R = vpoint(v0, v1, v3)
                if z < 0 or x < 2 or R < 1:
                    continue
                t = type_of(z, x, R)
                if t not in types:
                    types[t] = (z, x, R, eff(z, x, R))
    checks["c4_type_machine_box"] = {
        "box_bound": B_V, "clip": CLIP, "sentinel": SENT,
        "type_fields": "x==2, z==0, z%2, x%2, R%2, clipped w0..w5",
        "valid_points": points, "realized_types": ntypes,
        "witness_identity_mismatches": ident_bad,
        "confluence_mismatches": conf_bad,
    }

    pts, ident_bad, new_types, conf_bad = check_c7(types)
    checks["c7_seeded_far_probes"] = {
        "seed": 20261120, "n": 200000,
        "z_max": 3000, "x_max": 3000, "R_max": 9000,
        "points": pts, "identity_mismatches": ident_bad,
        "new_types": new_types, "confluence_mismatches": conf_bad,
    }

    pts, ident_bad, new_types, conf_bad, tail_bad = check_c8(types)
    checks["c8_boundary_manifolds"] = {
        "points": pts, "identity_mismatches": ident_bad,
        "new_types": new_types, "confluence_mismatches": conf_bad,
        "tail_value_mismatches": tail_bad,
    }

    pts, bad, new_types, conf_bad = check_c9(types)
    checks["c9_shell_sweep"] = {
        "bands": [[61, 64], [89, 92], [117, 120]],
        "points": pts, "identity_mismatches": bad,
        "new_types": new_types, "confluence_mismatches": conf_bad,
    }

    pts, bad = check_c12()
    checks["c12_deep_grid_sweep"] = {
        "grid": "z=0..120, x=2..120, R<=x+z+16",
        "points": pts, "mismatches": bad,
    }

    ok = True
    for name, c in checks.items():
        for k, v in c.items():
            if k.endswith(("mismatches", "mismatches_total_prefix", "bad")) and v:
                ok = False
            if k in ("new_types",) and v:
                ok = False
            if k == "c1d_published_z16_z17":
                pass
    # explicit pass/fail over every mismatch field
    def is_fail(c):
        if isinstance(c, dict):
            return any(is_fail(v) for v in c.values())
        if isinstance(c, list):
            return len(c) > 0
        return False
    for name, c in checks.items():
        if name == "c1d_published_z16_z17":
            for zz, d in c.items():
                if d["mismatches_total_prefix"]:
                    ok = False
        else:
            for k, v in c.items():
                if "mismatch" in k or k in ("new_types", "tail_value_mismatches"):
                    if is_fail(v):
                        ok = False
    audit["checks"] = checks
    audit["overall"] = "PASS" if ok else "FAIL"

    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(audit, indent=2, sort_keys=True, ensure_ascii=False)
    (out / "audit.json").write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
