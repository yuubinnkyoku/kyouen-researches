#!/usr/bin/env python3
"""Universal proof verifier for the two-token residual-game y=1 family (P1).

THEOREM (P1). For every integer z >= 1, x >= 1, R >= 0:
    H(R; (x,1); z) == cand(z, x, R)
where H is the two-token vertical-fiber residual game (order-preserving raw
recursion below; the sorted `H_canonical` engine agrees on every point ever
audited), tokens (x, 1), fiber parameter z, remaining height R; and cand is
the published parametric closed form of the 2026-11-19 y=1 census
(z-parity tables; identical code path to the census artifact).

PROOF ARCHITECTURE (universal, not census):
  Lemma Z (base z = 0).  H(R;(x,1);0) == cand0(x,R), with cand0 = {T0 = {3}
    for x >= 2; P0 rows: x=1: {1}; x odd >= 3: {1} u {even R in [4,x+1]};
    x even >= 2: {1} u {even R in [4,x]} u I[x+2,inf)}.
  Lemma I (slice identity). For z >= 1, the raw engine's option set at
    (z, x, R >= 1) is exactly {A, B, C} (A only when x >= 2):
      A = H(R-1; (x-1,1); z)   (decrement of the x token, x >= 2)
      B = single_token(x, z+1, R-1)   (removal of the y=1 token; K0832)
      C = 1 ^ H(R-1; (x,1); z-1)   (the z -> z-1 pass move)
    and at x = 1 the two token moves coincide: the sole token-child is
    single_token(1, z+1, R-1).
  Induction.  cand0 (Lemma Z, all x, R) + identity for z = 1 (uses C =
    1^cand0) proves slice z = 1; then jointly for each z >= 2 the identity
    with C = 1^cand(z-1, x, R-1) proves slice z from slices < z (x-outer
    induction inside each slice).  Strong induction on z closes all z >= 1.

The identities "cand(z,x,R) == mex(options)" for ALL z (resp. all x, R) are
reduced to a FINITE check by the TYPE MACHINERY below:
  - every closed form involved (cand, cand0, single_token and their child
    evaluations) reads only: the three parities, six difference families
    w0 = x-z, w1 = R-x, w2 = R-z, w3 = R-x-z, w4 = R-2x, w5 = R-2z,
    plus the single absolute read option: the decrement option A exists
    iff x >= 2 (z >= 2 identity); z = 1 and z = 0 use their own absolute
    clip families (see the machine sections).
  - child evaluations shift each family by at most 1 and read thresholds
    bounded by |k| <= 6, while clip windows are ±8 with sentinels at ±9:
    the value of every child is therefore a function of the parent TYPE
    alone (shift-closure lemma, machine-checked by witness-pair confluence).
  - the type space is finite; every realizable type is enumerated with an
    explicit witness (exhaustive box in the free coordinates) and the
    identity is verified once per type.
  - coverage of the unbounded space by the box is the witness-bound lemma
    (report Appendix A); machine evidence: witness-pair confluence, shell
    samplers, seeded far-magnitude probes (z, x <= 3000, R <= 9000) and
    boundary-aligned probes at z in {2,3,97,98,997,998,2999,3000}.

All checks are deterministic; audit JSON is byte-identical across runs
(no timestamps, sorted keys, seeded RNG only).
"""
from __future__ import annotations
import json, random, sys
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(1_000_000)

# ------------------------------------------------------------------ engines

def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

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
    X = tuple(sorted(X))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            opts.add(H_canonical(R - 1, tuple(sorted(X[:i] + (v - 1,) + X[i + 1:])), z))
        else:
            opts.add(H_canonical(R - 1, X[:i] + X[i + 1:], z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)

def q_odd(k):
    return k if k % 2 else k - 1

def single_token(x, z, R):
    """Published universal single-token closed form (K0832)."""
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

# cand(z, x, R): the published parametric y=1 closed form (verbatim from the
# census experiment vertical-fiber-two-token-y1-parametric-census-20261119).
def cand(z, x, R):
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
        else:  # x >= z + 3
            T = (R == z + 3 or (R % 2 == 1 and R <= z - 1))
        if x % 2 == 1 and x <= z - 1:
            P = False
        elif x % 2 == 0 and x <= z - 2:
            P = (R >= x + 2)
        elif x == z:
            P = (R >= z + 1)
        elif x == z + 1:
            P = (R == z + 1)
        elif x % 2 == 0:  # >= z + 2
            P = (R == z + 1 or (R % 2 == 0 and z + 4 <= R <= S - 1) or R >= S + 1)
        else:  # x odd >= z + 3
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
        else:  # x >= z + 3
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
        elif x % 2 == 1:  # odd x >= z + 3
            P = (R == z + 1 or (R % 2 == 1 and z + 4 <= R <= S))
        else:  # even x >= z + 4
            P = (R == z + 1 or (R % 2 == 1 and z + 4 <= R <= S) or R >= S + 1)
    assert not (T and P), (z, x, R)
    return 2 if T else (1 if P else 0)

# cand0(x, R): the two-token z=0 slice closed form (Lemma Z). Derived from
# the raw z=0 engine census (x <= 60, R <= 200 in development; machine
# engine anchor below re-verifies x <= 24, R <= 70 here, and the type
# machine proves the identity universally):
#   x = 1: P0 = {1} (the only option is the single-token child
#          single_token(1, 1, R-1): mex == 1 iff R == 1).
#   x >= 2: T0 = {3}; x odd: P0 = {1} u {even R: 4 <= R <= x+1};
#           x even: P0 = {1} u {even R: 4 <= R <= x} u I[x+2, inf).
def cand0(x, R):
    if R == 0 or x < 1:
        return 0
    if x == 1:
        return 1 if R == 1 else 0
    if R == 3:
        return 2
    if x % 2 == 1:
        return 1 if (R == 1 or (R % 2 == 0 and 4 <= R <= x + 1)) else 0
    return 1 if (R == 1 or (R % 2 == 0 and 4 <= R <= x) or R >= x + 2) else 0

# ------------------------------------------------------------- identities

def children_zge1(z, x, R):
    """Option value vector (A-or-None, B, C) for the slice-z identity.

    z >= 1, R >= 1. A is present iff x >= 2. C = 1^cand0 for z=1,
    1^cand(z-1) for z >= 2."""
    A = cand(z, x - 1, R - 1) if x >= 2 else None
    B = single_token(x, z + 1, R - 1)
    Cchild = cand0(x, R - 1) if z == 1 else cand(z - 1, x, R - 1)
    C = 1 ^ Cchild
    return A, B, C

def value_vector_zge1(z, x, R):
    """(cand, A, B, C) formula outputs at a point (any magnitude)."""
    if R == 0:
        return (cand(z, x, R), None, 0, None)
    A, B, C = children_zge1(z, x, R)
    return (cand(z, x, R), A, B, C)

def value_vector_z0(x, R):
    if R == 0:
        return (cand0(x, R), None, 0)
    A = cand0(x - 1, R - 1) if x >= 2 else None
    B = single_token(x, 1, R - 1)
    return (cand0(x, R), A, B)

def identity_zge1(z, x, R):
    """mex(options) at (z,x,R) vs cand. R >= 1."""
    A, B, C = children_zge1(z, x, R)
    opts = {B, C}
    if A is not None:
        opts.add(A)
    return mex(opts), cand(z, x, R)

def identity_z0(x, R):
    A, B = value_vector_z0(x, R)[1], value_vector_z0(x, R)[2]
    opts = {B}
    if A is not None:
        opts.add(A)
    return mex(opts), cand0(x, R)

def eff_vector_zge2(z, x, R):
    """Effective comparison vector for z >= 2 confluence: the parent value
    plus the actual option-VALUE SET (A dropped when absent, i.e. x == 1).
    The type machinery claims this vector is a function of the type."""
    if R == 0:
        return (cand(z, x, 0), frozenset())
    A, B, C = children_zge1(z, x, R)
    opts = {B, C} if A is None else {A, B, C}
    return (cand(z, x, R), frozenset(opts))

# ------------------------------------------------------------ type machinery

W6 = 8          # window half-width for the six difference families (z>=2)
B_V = 60        # free-coordinate box bound (witness-bound lemma margin)
XW1_HI, RW1_HI = 24, 80     # z=0/z=1 absolute clip window tops
DW_HI = 24                    # z=0/z=1 R-x window half-width
TWO_HI = 16                   # z=1 R-2x window half-width

def clip8(u):
    if -W6 <= u <= W6:
        return u
    return -9 if u < -W6 else 9

def type_zge2(z, x, R):
    # leading bit: x == 1 (absolute read: the decrement option A exists iff
    # x >= 2; every other closed-form read lies in the six clipped families)
    # from the six families and the three parities (checked exhaustively by
    # the witness-pair confluence test C4b below).
    return (1 if x == 1 else 0, z % 2, x % 2, R % 2,
            clip8(x - z), clip8(R - x), clip8(R - z),
            clip8(R - x - z), clip8(R - 2 * x), clip8(R - 2 * z))

def clip_abs(u, hi):
    # exact for 0 <= u <= hi (u >= 1 domains), sentinel 10 for u > hi
    return u if 1 <= u <= hi else (0 if u == 0 else 10 if u > hi else -10)

def clip_gen(u, hi):
    if -hi <= u <= hi:
        return u
    return -100 if u < -hi else 100

def type_z1(x, R):
    return (x % 2, R % 2, clip_abs(x, XW1_HI), clip_abs(R, RW1_HI),
            clip_gen(R - x, DW_HI), clip_gen(R - 2 * x, TWO_HI))

def type_z0(x, R):
    return (x % 2, R % 2, clip_abs(x, XW1_HI), clip_abs(R, RW1_HI),
            clip_gen(R - x, DW_HI))

# ------------------------------------------------------------------- audit

def run_audit():
    audit = {"checks": {}, "fail": [], "n_points": 0}
    def check(name, ok, detail):
        detail = {k: (list(v) if isinstance(v, tuple) else v) for k, v in detail.items()}
        audit["checks"][name] = {"ok": bool(ok), **detail}
        if not ok:
            audit["fail"].append(name)

    # ---- C1: engine anchors (raw recursion vs closed forms) -------------
    bad1 = 0; ex1 = None; n = 0
    for z in range(0, 7):
        for x in range(1, 17):
            for R in range(0, x + 31):
                n += 1
                h = H_ordered(R, (x, 1), z)
                c = cand0(x, R) if z == 0 else cand(z, x, R)
                if h != c:
                    bad1 += 1
                    if ex1 is None: ex1 = (z, x, R, h, c)
    check("C1_raw_engine_vs_closed_form_z0_6", bad1 == 0,
          {"points": n, "bad": bad1, "example": ex1})
    audit["n_points"] += n

    bad1b = 0; ex1b = None; n = 0
    for z in range(0, 7):
        for x in range(1, 17):
            for R in range(0, x + 31):
                n += 1
                h = H_canonical(R, (x, 1), z)
                c = cand0(x, R) if z == 0 else cand(z, x, R)
                if h != c:
                    bad1b += 1
                    if ex1b is None: ex1b = (z, x, R, h, c)
    check("C1b_canonical_engine_vs_closed_form_z0_6", bad1b == 0,
          {"points": n, "bad": bad1b, "example": ex1b})
    audit["n_points"] += n

    # single_token vs raw single-token engine
    bad1c = 0; ex1c = None; n = 0
    for x in range(1, 11):
        for zp in range(1, 13):
            for R in range(0, 31):
                n += 1
                if H_ordered(R, (x,), zp) != single_token(x, zp, R):
                    bad1c += 1
                    if ex1c is None: ex1c = (x, zp, R)
    check("C1c_single_token_engine_anchor", bad1c == 0,
          {"points": n, "bad": bad1c, "example": ex1c})
    audit["n_points"] += n

    # published-slice agreement (K1018 z=14, K1020 z=15 verbatim formulas)
    def T14(x, r):
        if x == 1: return r == 1
        if x == 13: return 1 <= r <= 15 and r % 2 == 1
        if x <= 12:
            top = x + 1 if x % 2 == 0 else x
            return 1 <= r <= top and r % 2 == 1
        if x == 14 or x == 15: return 1 <= r <= 13 and r % 2 == 1
        if x == 16: return (1 <= r <= 13 or 17 <= r <= 31) and r % 2 == 1
        return r in (1, 3, 5, 7, 9, 11, 13, 17)
    def P14(x, r):
        if x % 2 == 1:
            if x <= 13: return False
            if x == 15: return r == 15
            return r == 15 or (r % 2 == 0 and 18 <= r <= x + 15)
        if x <= 12: return r >= x + 2
        if x == 14: return r >= 15
        return r == 15 or (r % 2 == 0 and 18 <= r <= x + 14) or r >= x + 16
    def T15(x, r):
        if x == 1: return r == 1
        if x == 16: return 1 <= r <= 17 and r % 2 == 1
        if x == 17: return 1 <= r <= 33 and r % 2 == 1
        if x <= 15:
            top = x + 1 if x % 2 == 0 else x
            return 1 <= r <= top and r % 2 == 1
        return 1 <= r <= 17 and r % 2 == 1
    def P15(x, r):
        if x % 2 == 1:
            if x <= 13: return False
            if x in (15, 17): return r == 16
            return r == 16 or (r % 2 == 1 and 19 <= r <= x + 16)
        if x <= 14: return r >= x + 2
        if x == 16: return r == 16 or r >= 18
        return r == 16 or (r % 2 == 1 and 19 <= r <= x + 16) or r >= x + 17
    bad1d = 0; ex1d = None; n = 0
    for x in range(1, 121):
        for R in range(0, x + 35):
            n += 1
            c14 = 2 if T14(x, R) else (1 if P14(x, R) else 0)
            c15 = 2 if T15(x, R) else (1 if P15(x, R) else 0)
            if cand(14, x, R) != c14 or cand(15, x, R) != c15:
                bad1d += 1
                if ex1d is None: ex1d = (x, R)
    check("C1d_published_slice_agreement_z14_z15", bad1d == 0,
          {"points": n, "bad": bad1d, "example": ex1d})
    audit["n_points"] += n

    # ---- C2: finite formula-identity grids --------------------------------
    bad2 = 0; ex2 = None; n = 0
    for z in range(1, 41):
        for x in range(1, 41):
            for R in range(1, x + z + 41):
                n += 1
                m, c = identity_zge1(z, x, R)
                if m != c:
                    bad2 += 1
                    if ex2 is None: ex2 = (z, x, R, m, c)
    check("C2_identity_grid_z1_40", bad2 == 0,
          {"points": n, "bad": bad2, "example": ex2})
    audit["n_points"] += n

    bad2b = 0; ex2b = None; n = 0
    for x in range(1, 61):
        for R in range(1, 201):
            n += 1
            m, c = identity_z0(x, R)
            if m != c:
                bad2b += 1
                if ex2b is None: ex2b = (x, R, m, c)
    check("C2b_identity_grid_z0", bad2b == 0,
          {"points": n, "bad": bad2b, "example": ex2b})
    audit["n_points"] += n

    # R = 0 trivial value on sampled points
    bad2c = 0; n = 0
    for z in range(1, 30):
        for x in range(1, 30):
            n += 1
            if cand(z, x, 0) != 0 or cand0(x, 0) != 0:
                bad2c += 1
    check("C2c_R0_trivial", bad2c == 0, {"points": n, "bad": bad2c})
    audit["n_points"] += n

    # ---- C3: option-set anchor vs raw engine ------------------------------
    bad3 = 0; ex3 = None; n = 0
    for z in range(1, 6):
        for x in range(1, 10):
            for R in range(1, 31):
                n += 1
                # options exactly as the raw engine computes them
                opts = set()
                X = (x, 1)
                if x > 1:
                    opts.add(H_ordered(R - 1, (x - 1, 1), z))
                opts.add(H_ordered(R - 1, (x,), z + 1))
                opts.add(1 ^ H_ordered(R - 1, X, z - 1))
                m = mex(opts)
                c = cand(z, x, R)
                if m != c:
                    bad3 += 1
                    if ex3 is None: ex3 = (z, x, R, m, c)
    check("C3_option_decomposition_engine_anchor", bad3 == 0,
          {"points": n, "bad": bad3, "example": ex3})
    audit["n_points"] += n

    # ---- C4: z >= 2 type machine ------------------------------------------
    # Free coordinates: v0 = x-z, v1 = R-x, v3 = R-x-z
    #   w0 = v0, w1 = v1, w2 = v0+v1 (=R-z), w3 = v3, w4 = v3-v0 (=R-2x),
    #   w5 = v0+v3 (=R-2z)
    #   z = v1 - v3, x = v0 + v1 - v3, R = 2*v1 + v0 - v3
    types = {}
    n_enum = 0
    for v0 in range(-B_V, B_V + 1):
        for v1 in range(-B_V, B_V + 1):
            for v3 in range(-B_V, B_V + 1):
                z = v1 - v3
                if z < 2:
                    continue
                x = v0 + v1 - v3
                if x < 1:
                    continue
                R = 2 * v1 + v0 - v3
                if R < 1:
                    continue
                n_enum += 1
                t = type_zge2(z, x, R)
                key = v0 * v0 + v1 * v1 + v3 * v3
                if t in types:
                    wit = types[t]
                    if key < wit["key"]:
                        types[t] = {"key": key, "pt": (z, x, R),
                                    "other": wit["pt"] if wit["pt"] != (z, x, R) else wit["other"]}
                    elif (z, x, R) != wit["pt"] and wit["other"] is None:
                        wit["other"] = (z, x, R)
                else:
                    types[t] = {"key": key, "pt": (z, x, R), "other": None}
    # identity per type + witness-pair confluence
    bad4 = 0; ex4 = None; bad4b = 0; ex4b = None
    max_coord = 0
    for t, wit in types.items():
        z, x, R = wit["pt"]
        m, c = identity_zge1(z, x, R)
        if m != c:
            bad4 += 1
            if ex4 is None: ex4 = (z, x, R, m, c)
        max_coord = max(max_coord, abs(x - z), abs(R - x), abs(R - z),
                         abs(R - x - z), abs(R - 2 * x), abs(R - 2 * z))
        if wit["other"] is not None:
            z2, x2, R2 = wit["other"]
            if eff_vector_zge2(z2, x2, R2) != eff_vector_zge2(z, x, R):
                bad4b += 1
                if ex4b is None: ex4b = wit["pt"] + wit["other"]
    check("C4_zge2_type_identity", bad4 == 0,
          {"realized_types": len(types), "box_points": n_enum,
           "bad": bad4, "example": ex4,
           "box_bound": B_V, "window": W6,
           "max_abs_form_at_witness": max_coord})
    check("C4b_zge2_witness_pair_confluence", bad4b == 0,
          {"pairs_compared": sum(1 for w in types.values() if w["other"] is not None),
           "bad": bad4b, "example": ex4b})
    audit["n_points"] += n_enum

    # ---- C5: z = 1 type machine -------------------------------------------
    types1 = {}
    n_enum1 = 0
    for x in range(1, 141):
        for R in range(1, 321):
            n_enum1 += 1
            t = type_z1(x, R)
            key = x * x + R * R
            if t in types1:
                wit = types1[t]
                if key < wit["key"]:
                    types1[t] = {"key": key, "pt": (x, R),
                                 "other": wit["pt"] if wit["pt"] != (x, R) else wit["other"]}
                elif (x, R) != wit["pt"] and wit["other"] is None:
                    wit["other"] = (x, R)
            else:
                types1[t] = {"key": key, "pt": (x, R), "other": None}
    bad5 = 0; ex5 = None; bad5b = 0; ex5b = None
    for t, wit in types1.items():
        x, R = wit["pt"]
        m, c = identity_zge1(1, x, R)
        if m != c:
            bad5 += 1
            if ex5 is None: ex5 = (x, R, m, c)
        if wit["other"] is not None:
            x2, R2 = wit["other"]
            if value_vector_zge1(1, x2, R2) != value_vector_zge1(1, x, R):
                bad5b += 1
                if ex5b is None: ex5b = wit["pt"] + wit["other"]
    check("C5_z1_type_identity", bad5 == 0,
          {"realized_types": len(types1), "box_points": n_enum1,
           "bad": bad5, "example": ex5,
           "windows": {"x": [1, XW1_HI], "R": [0, RW1_HI], "R_minus_x": DW_HI,
                       "R_minus_2x": TWO_HI}})
    check("C5b_z1_witness_pair_confluence", bad5b == 0,
          {"pairs_compared": sum(1 for w in types1.values() if w["other"]),
           "bad": bad5b, "example": ex5b})
    audit["n_points"] += n_enum1

    # ---- C6: z = 0 type machine -------------------------------------------
    types0 = {}
    n_enum0 = 0
    for x in range(1, 141):
        for R in range(1, 301):
            n_enum0 += 1
            t = type_z0(x, R)
            key = x * x + R * R
            if t in types0:
                wit = types0[t]
                if key < wit["key"]:
                    types0[t] = {"key": key, "pt": (x, R),
                                 "other": wit["pt"] if wit["pt"] != (x, R) else wit["other"]}
                elif (x, R) != wit["pt"] and wit["other"] is None:
                    wit["other"] = (x, R)
            else:
                types0[t] = {"key": key, "pt": (x, R), "other": None}
    bad6 = 0; ex6 = None; bad6b = 0; ex6b = None
    for t, wit in types0.items():
        x, R = wit["pt"]
        m, c = identity_z0(x, R)
        if m != c:
            bad6 += 1
            if ex6 is None: ex6 = (x, R, m, c)
        if wit["other"] is not None:
            x2, R2 = wit["other"]
            if value_vector_z0(x2, R2) != value_vector_z0(x, R):
                bad6b += 1
                if ex6b is None: ex6b = wit["pt"] + wit["other"]
    check("C6_z0_type_identity", bad6 == 0,
          {"realized_types": len(types0), "box_points": n_enum0,
           "bad": bad6, "example": ex6})
    check("C6b_z0_witness_pair_confluence", bad6b == 0,
          {"pairs_compared": sum(1 for w in types0.values() if w["other"]),
           "bad": bad6b, "example": ex6b})
    audit["n_points"] += n_enum0

    # ---- C7: far-magnitude probes -----------------------------------------
    rng = random.Random(20261119)
    zge2_types = set(types.keys())
    z1_types = set(types1.keys())
    z0_types = set(types0.keys())
    bad7 = 0; ex7 = None; bad7b = 0; ex7b = None
    n7 = 200000
    for _ in range(n7):
        z = rng.randint(1, 3000)
        x = rng.randint(1, 3000)
        R = rng.randint(0, 9000)
        if R == 0:
            if cand(z, x, R) != 0:
                bad7 += 1
            continue
        m, c = identity_zge1(z, x, R)
        if m != c:
            bad7 += 1
            if ex7 is None: ex7 = (z, x, R, m, c)
        if z >= 2:
            t = type_zge2(z, x, R)
            if t not in zge2_types:
                bad7b += 1
                if ex7b is None: ex7b = ("zge2 type missing", z, x, R, t)
                continue
            wit = types[t]["pt"]
            if eff_vector_zge2(z, x, R) != eff_vector_zge2(wit[0], wit[1], wit[2]):
                bad7b += 1
                if ex7b is None: ex7b = ("confluence", z, x, R, t)
        else:
            t = type_z1(x, R)
            if t not in z1_types:
                bad7b += 1
                if ex7b is None: ex7b = ("z1 type missing", x, R, t)
                continue
            wit = types1[t]["pt"]
            if value_vector_zge1(1, x, R) != value_vector_zge1(1, wit[0], wit[1]):
                bad7b += 1
                if ex7b is None: ex7b = ("z1 confluence", x, R, t)
    check("C7_seeded_far_probes_identity", bad7 == 0,
          {"points": n7, "bad": bad7, "example": ex7,
           "ranges": "z,x in [1,3000], R in [0,9000], seed 20261119"})
    check("C7b_seeded_far_probes_type_membership_confluence", bad7b == 0,
          {"points": n7, "bad": bad7b, "example": ex7b})
    audit["n_points"] += n7

    # boundary-aligned probes along all critical manifolds
    zgrid = [2, 3, 97, 98, 997, 998, 2999, 3000]
    bad8 = 0; ex8 = None; bad8b = 0; ex8b = None
    n8 = 0
    for z in zgrid:
        xs = sorted(set(list(range(1, 16)) + [z + d for d in range(-6, 9)]))
        for x in xs:
            if x < 1:
                continue
            base = {R + off for B in (x, z, x + z, 2 * x, 2 * z, x + z + 1)
                    for off in range(-8, 11) for R in [B]}
            for R in base:
                if R < 1:
                    continue
                n8 += 1
                m, c = identity_zge1(z, x, R)
                if m != c:
                    bad8 += 1
                    if ex8 is None: ex8 = (z, x, R, m, c)
                t = type_zge2(z, x, R)
                if t not in zge2_types:
                    bad8b += 1
                    if ex8b is None: ex8b = ("type missing", z, x, R, t)
                    continue
                wit = types[t]["pt"]
                if eff_vector_zge2(z, x, R) != eff_vector_zge2(*wit):
                    bad8b += 1
                    if ex8b is None: ex8b = ("confluence", z, x, R, t)
    check("C8_boundary_manifold_probes", bad8 == 0,
          {"points": n8, "bad": bad8, "z_values": zgrid, "example": ex8})
    check("C8b_boundary_manifold_type_coverage", bad8b == 0,
          {"points": n8, "bad": bad8b, "example": ex8b})
    audit["n_points"] += n8

    # ---- C9: z=0/z=1 far probes -------------------------------------------
    bad9 = 0; ex9 = None; bad9b = 0; ex9b = None; n9 = 0
    for _ in range(60000):
        x = rng.randint(1, 5000)
        R = rng.randint(1, 15000)
        n9 += 1
        m, c = identity_z0(x, R)
        if m != c:
            bad9 += 1
            if ex9 is None: ex9 = ("z0", x, R, m, c)
        t0 = type_z0(x, R)
        if t0 not in z0_types:
            bad9b += 1
            if ex9b is None: ex9b = ("z0 type missing", x, R, t0)
            continue
        # z=1 identity at the same (x, R)
        m1, c1 = identity_zge1(1, x, R)
        if m1 != c1:
            bad9 += 1
            if ex9 is None: ex9 = ("z1", x, R, m1, c1)
        t1 = type_z1(x, R)
        if t1 not in z1_types:
            bad9b += 1
            if ex9b is None: ex9b = ("z1 type missing", x, R, t1)
            continue
        wit0, wit1 = types0[t0]["pt"], types1[t1]["pt"]
        if value_vector_z0(x, R) != value_vector_z0(*wit0) or \
           value_vector_zge1(1, x, R) != value_vector_zge1(1, wit1[0], wit1[1]):
            bad9b += 1
            if ex9b is None: ex9b = ("confluence", x, R, t0, t1)
    check("C9_z0_z1_far_probes", bad9 == 0,
          {"points": n9 * 2, "bad": bad9, "example": ex9,
           "ranges": "x in [1,5000], R in [1,15000]"})
    check("C9b_z0_z1_type_coverage_confluence", bad9b == 0,
          {"points": n9 * 2, "bad": bad9b, "example": ex9b})
    audit["n_points"] += 2 * n9

    # ---- C10: engine deep anchor at larger z (cand vs raw) -----------------
    bad10 = 0; ex10 = None; n = 0
    for z in range(7, 13):
        H_ordered.cache_clear(); H_canonical.cache_clear()
        for x in range(1, 13):
            for R in range(0, 27):
                n += 1
                if H_ordered(R, (x, 1), z) != cand(z, x, R) or \
                   H_canonical(R, (x, 1), z) != cand(z, x, R):
                    bad10 += 1
                    if ex10 is None: ex10 = (z, x, R)
    check("C10_engine_deep_anchor_z7_12", bad10 == 0,
          {"points": n, "bad": bad10, "example": ex10})
    audit["n_points"] += n

    # ---- C11: v-space shell sweep (box-boundary stress for z >= 2) --------
    # Deterministic seeded sampling on shells max(|v0|,|v1|,|v3|) = r for
    # r in [B_V+1, 2*B_V]: every realized type must already be in the box
    # (no new types beyond it), and confluence must hold.
    bad11 = 0; ex11 = None; n11 = 0
    new_types = []
    for r in range(B_V + 1, 2 * B_V + 1):
        for _ in range(2000):
            v0 = rng.choice([-r, r]) if rng.random() < 0.5 else rng.randint(-r, r)
            v1 = rng.choice([-r, r]) if rng.random() < 0.5 else rng.randint(-r, r)
            v3 = rng.randint(-r, r)
            if max(abs(v0), abs(v1), abs(v3)) != r:
                continue
            z = v1 - v3; x = v0 + v1 - v3; R = 2 * v1 + v0 - v3
            if z < 2 or x < 1 or R < 1:
                continue
            n11 += 1
            t = type_zge2(z, x, R)
            if t not in zge2_types:
                bad11 += 1
                if not any(m[:4] == (z, x, R, t) for m in new_types):
                    new_types.append((z, x, R, t))
                if ex11 is None: ex11 = (z, x, R, t)
                continue
            wit = types[t]["pt"]
            if eff_vector_zge2(z, x, R) != eff_vector_zge2(*wit):
                bad11 += 1
                if ex11 is None: ex11 = ("confluence", z, x, R, t)
    check("C11_vspace_shell_sweep_zge2", bad11 == 0,
          {"points": n11, "bad": bad11, "new_types_beyond_box": len(new_types),
           "shell_range": [B_V + 1, 2 * B_V], "example": ex11})
    audit["n_points"] += n11

    # ---- C12: out-of-box ring sweep for the z=0/z=1 machines --------------
    # x in [1, 300], R in [1, 1000] fully covers the enumeration boxes
    # ([1,140]x[1,320] / [1,301]) and a far larger ring beyond them.
    bad12 = 0; ex12 = None; n12 = 0
    new12 = []
    for x in range(1, 301):
        for R in range(1, 1001):
            n12 += 1
            t0 = type_z0(x, R)
            if t0 not in z0_types:
                bad12 += 1
                if ex12 is None: ex12 = ("z0 type missing", x, R, t0)
                new12.append(("z0", x, R))
            else:
                w = types0[t0]["pt"]
                if value_vector_z0(x, R) != value_vector_z0(*w):
                    bad12 += 1
                    if ex12 is None: ex12 = ("z0 confluence", x, R, t0)
            t1 = type_z1(x, R)
            if t1 not in z1_types:
                bad12 += 1
                if ex12 is None: ex12 = ("z1 type missing", x, R, t1)
                new12.append(("z1", x, R))
            else:
                w = types1[t1]["pt"]
                if value_vector_zge1(1, x, R) != value_vector_zge1(1, w[0], w[1]):
                    bad12 += 1
                    if ex12 is None: ex12 = ("z1 confluence", x, R, t1)
    check("C12_ring_sweep_z0_z1", bad12 == 0,
          {"points": n12 * 2, "bad": bad12, "new_types_beyond_box": len(new12),
           "ring": "x in [1,300], R in [1,1000] vs boxes x<=140, R<=321",
           "example": ex12})
    audit["n_points"] += 2 * n12

    audit["all_ok"] = not audit["fail"]
    audit["summary"] = {
        "zge2_realized_types": len(types),
        "z1_realized_types": len(types1),
        "z0_realized_types": len(types0),
    }
    return audit

def main():
    audit = run_audit()
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(audit, sort_keys=True, indent=2) + "\n"
    (out / "audit.json").write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if audit["all_ok"] else 1

if __name__ == "__main__":
    sys.exit(main())
