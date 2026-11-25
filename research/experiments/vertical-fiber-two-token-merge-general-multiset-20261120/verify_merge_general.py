#!/usr/bin/env python3
"""Verify the general-multiset boundary-Mex reduction (K1150 lane, 2026-11-20).

PROVED UNIVERSALLY (symbolic proofs in report.md; this machine double-checks
the engines and collects finite census evidence):

  R1 (far lemma):    for z >= S+2 every child of (X, z) lies in the merged
                     region (z' >= sum'+1), so MERGE at layer R-1 transfers
                     to layer R.
  R2 (collapse lem.): at z = S+1 every token child of X shares the value
                     a(m) = single_token(S-1, S, m) (m = R-1; z-independence of
                     the z>=x+1 case), hence
                     H(R; X; S+1) = mex({a(R-1), 1 ^ D_X(R-1)}),
                     where D_X(m) := H(m; X; S) is the diagonal band.
                     Likewise at the diagonal itself:
                     D_X(m) = mex({a(m-1), 1 ^ U1_X(m-1)}),
                     U1_X(m) := H(m; X; S-1)  (level-1 stripe; cascade step).
  R3 (mex lemma):    with b = 1^D, b' = 1^e:
                       mex({0, b})  = {2 if D==0 else 1}          (depends only on D==0)
                       mex({1, b})  = {2 if D==1 else 0}          (depends only on D==1)
                       mex({2, b})  = {1 if D==1 else 0}          (depends only on D==1)
                     so mex({a, 1^D}) == mex({a, 1^e}) iff
                       (a==0 and D==0 iff e==0) or (a in {1,2} and D==1 iff e==1).

  THEOREM (reduction).  MERGE(S) := "for all multisets X with sum S, all
  z >= S+1, all R >= 0: H(R; X; z) = single_token(S, z, R)".  BAND(S) := the
  explicit diagonal-band conditions, for all X with sum S:
     S even:   (D_X(m) != 1 for all m)  and  (D_X(m) == 0 for all even m <= S-1)
     S odd:    (D_X(m) == 0  iff  (m even and m <= S-1))
               and (D_X(m) != 1 for all odd m <= S-2).
  Then, given MERGE(S') for all S' < S:   MERGE(S)  iff  BAND(S).
  In particular, universally:  (MERGE for all S)  iff  (BAND for all S).
  The general merge observation is therefore REDUCED to the diagonal-band
  claims.  BAND itself remains finite-evidence only (frontier: the level-k
  stripe cascade L1/L2/... and the band table B(k,S)).

Raw engine semantics are copied verbatim from the published K1101 verifier
(H_canonical) and single_token is the published K0832 closed form (verbatim).

All checks are deterministic: fixed iteration order, sorted JSON keys, no
timestamps, stdlib only.
"""

import json
import os
import sys
from functools import lru_cache

sys.setrecursionlimit(1_000_000)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "audit.json")

S_CAP = 20            # partition universe cap (all multisets, sums 1..S_CAP)
ZTOP = S_CAP + 2      # highest queried z for boundary rows
ZMAX = ZTOP + S_CAP + 2   # DP closure pad (removal chains never reach here)
R_CAP = 200
S_CAP_BAND = 16       # band table cap (k <= S <= 16)
PART2 = 40            # 2-token wide DP part cap
ZMAX2 = 2 * PART2 + 4     # 2-token DP pad (z <= S+2 <= 82, +2 removal pad)


# ---------------------------------------------------------------- engines ---

def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m


@lru_cache(None)
def H_canonical(R, X, z):
    """Verbatim raw recursion (K1101 verifier)."""
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            opts.add(H_canonical(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
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
    """Published single-token closed form (K0832, verbatim from K1101)."""
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


def gen_partitions(n, maxpart=None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield ()
        return
    for first in range(min(n, maxpart), 0, -1):
        for rest in gen_partitions(n - first, first):
            yield (first,) + rest


def all_universe(scap):
    parts = [()]
    for s in range(1, scap + 1):
        parts.extend(sorted(gen_partitions(s)))
    return parts


def build_dp(uni, zmax, r_cap):
    """Layer DP over the universe. Returns (L, IX, W):
    val(X, z, r) == L[r][IX[X] * W + z]."""
    IX = {X: i for i, X in enumerate(uni)}
    N = len(uni)
    W = zmax + 1
    kids = []
    for X in uni:
        ks = []
        seen = set()
        for i, v in enumerate(X):
            if v in seen:
                continue
            seen.add(v)
            if v > 1:
                child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
                ks.append((0, IX[child]))
            else:
                child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
                ks.append((1, IX[child]))
        kids.append(ks)
    prev = [0] * (N * W)
    L = [prev]
    for r in range(1, r_cap + 1):
        cur = [0] * (N * W)
        for ix in range(N):
            base = ix * W
            ks = kids[ix]
            for z in range(W):
                opts = set()
                for kind, cix in ks:
                    opts.add(prev[cix * W + (z if kind == 0 else z + 1)])
                if z >= 1:
                    opts.add(1 ^ prev[base + z - 1])
                m = 0
                while m in opts:
                    m += 1
                cur[base + z] = m
        prev = cur
        L.append(cur)
    return L, IX, W


# ------------------------------------------------------------- audit frame ---

results = {}
POINTS = 0


def check(name, fn):
    global POINTS
    ok, detail, n = fn()
    POINTS += n
    results[name] = {"pass": bool(ok), "points": n, "detail": detail}


def band_pair(a, D, e):
    """mex({a,1^D}) == mex({a,1^e}) and its reduction to bit conditions."""
    return mex({a, 1 ^ D}) == mex({a, 1 ^ e})


# ------------------------------------------------------------------ checks ---

def C1_dp_vs_topdown():
    """Layer DP vs verbatim top-down recursion on a small grid."""
    bad = []
    n = 0
    for X in UNI:
        S = sum(X)
        if S > 6 or len(X) > 3:
            continue
        for z in range(0, min(S + 3, ZTOP) + 1):
            for r in (1, 2, 3, 5, 9, 17, 40, 119):
                n += 1
                if VAL(X, z, r) != H_canonical(r, X, z):
                    bad.append((X, z, r, VAL(X, z, r), H_canonical(r, X, z)))
                    if len(bad) >= 20:
                        return False, bad, n
    return (len(bad) == 0), bad[:20], n


def C2_singleton_closed_form():
    """Singleton rows vs published closed form, z <= ZTOP, r <= R_CAP."""
    bad = []
    n = 0
    for X in UNI:
        if len(X) != 1:
            continue
        x = X[0]
        for z in range(0, ZTOP + 1):
            for r in range(0, R_CAP + 1):
                n += 1
                if VAL(X, z, r) != single_token(x, z, r):
                    bad.append((x, z, r, VAL(X, z, r), single_token(x, z, r)))
                    if len(bad) >= 20:
                        return False, bad, n
    return (len(bad) == 0), bad[:20], n


def C3_counterexample_and_sharpness():
    """Canonical S=z counterexample + published 828-divergence reproduction
    (verbatim top-down, same band as K1101 C8)."""
    a = H_canonical(5, (2, 1), 3)
    b = H_canonical(5, (3,), 3)
    if not (a == 1 and b == 2):
        return False, {"canonical": [a, b], "want": [1, 2]}, 2
    n = 2
    div = 0
    for z in range(3, 25):
        for y in range(1, z // 2 + 1):
            x = z - y
            if x < y:
                continue
            top = min(2 * z + 20, 80)
            for R in range(0, top + 1):
                n += 1
                if H_canonical(R, (x, y), z) != H_canonical(R, (z,), z):
                    div += 1
    ok = div == 828
    return ok, {"canonical": [3, (2, 1), 5, a, b],
                "S_eq_z_divergences_within_band": div, "published_value": 828}, n


def C4_merge_rows():
    """Merge rows z=S+1, S+2 for ALL multisets (z=S+3 extra far evidence for
    S <= 18), all r <= R_CAP, vs single_token."""
    bad = []
    n = 0
    for X in UNI:
        S = sum(X)
        if S < 1:
            continue
        zs = [S + 1, S + 2]
        if S <= 18:
            zs.append(S + 3)
        for z in zs:
            if z > ZTOP:
                continue
            for r in range(0, R_CAP + 1):
                n += 1
                if VAL(X, z, r) != single_token(S, z, r):
                    bad.append((X, z, r, VAL(X, z, r), single_token(S, z, r)))
                    if len(bad) >= 20:
                        return False, bad, n
    return (len(bad) == 0), bad[:20], n


def C5_collapse_identities():
    """(A) boundary z=S+1 raw value == mex({a, 1^D});
    (B) diagonal cascade identity D(m) == mex({a(m-1), 1^U1(m-1)}).
    Domain: non-singleton X, S >= 2 (A: r >= 1, B: m >= 1)."""
    bad = []
    n = 0
    for X in UNI:
        S = sum(X)
        if S < 2 or len(X) == 1:
            continue
        for r in range(1, R_CAP + 1):
            m = r - 1
            a = single_token(S - 1, S, m)
            Dm = VAL(X, S, m)
            rawb = VAL(X, S + 1, r)
            n += 1
            if rawb != mex({a, 1 ^ Dm}):
                bad.append(("A", X, r, rawb, mex({a, 1 ^ Dm})))
            if len(bad) >= 20:
                return False, bad[:20], n
        for m in range(1, R_CAP + 1):
            a_prev = single_token(S - 1, S, m - 1)
            Dm = VAL(X, S, m)
            U1_prev = VAL(X, S - 1, m - 1)
            n += 1
            if Dm != mex({a_prev, 1 ^ U1_prev}):
                bad.append(("B", X, m, Dm, mex({a_prev, 1 ^ U1_prev})))
            if len(bad) >= 20:
                return False, bad[:20], n
    return (len(bad) == 0), bad[:20], n


def C6_compat():
    """mex({a, 1^D}) == mex({a, 1^e}) for all non-singleton X, r <= R_CAP
    (merge at the boundary, single-token side)."""
    bad = []
    n = 0
    for X in UNI:
        S = sum(X)
        if S < 2 or len(X) == 1:
            continue
        for r in range(1, R_CAP + 1):
            m = r - 1
            a = single_token(S - 1, S, m)
            D = VAL(X, S, m)
            e = single_token(S, S, m)
            n += 1
            if not band_pair(a, D, e):
                bad.append((X, r, a, D, e))
                if len(bad) >= 20:
                    return False, bad, n
    return (len(bad) == 0), bad[:20], n


def C7_band_evenS():
    """BAND(S even): D != 1 for all m; D == 0 for all even m <= S-1.
    Non-singleton X, m <= R_CAP."""
    bad = []
    n = 0
    for X in UNI:
        S = sum(X)
        if S < 2 or S % 2 != 0 or len(X) == 1:
            continue
        for m in range(0, R_CAP + 1):
            D = VAL(X, S, m)
            n += 1
            if D == 1:
                bad.append(("no1", X, m, D))
            if m % 2 == 0 and m <= S - 1 and D != 0:
                bad.append(("even0", X, m, D))
            if len(bad) >= 20:
                return False, bad[:20], n
    return (len(bad) == 0), bad[:20], n


def C8_band_oddS():
    """BAND(S odd): D == 0 iff (m even and m <= S-1); D != 1 for odd m <= S-2.
    Non-singleton X, m <= R_CAP."""
    bad = []
    n = 0
    for X in UNI:
        S = sum(X)
        if S < 3 or S % 2 != 1 or len(X) == 1:
            continue
        for m in range(0, R_CAP + 1):
            D = VAL(X, S, m)
            n += 1
            if (D == 0) != (m % 2 == 0 and m <= S - 1):
                bad.append(("iff0", X, m, D))
            if m % 2 == 1 and m <= S - 2 and D == 1:
                bad.append(("no1", X, m, D))
            if len(bad) >= 20:
                return False, bad[:20], n
    return (len(bad) == 0), bad[:20], n


def C9_L1_stripes():
    """Level-1 stripe claims (non-singleton X, m <= R_CAP):
       L1-A: S even: odd m <= S-1 -> U1 != 1;  S odd: odd m <= S-2 -> U1 != 1
       L1-B: S odd: even m <= S-3 -> U1 == 0."""
    bad = []
    n = 0
    for X in UNI:
        S = sum(X)
        if S < 2 or len(X) == 1:
            continue
        for m in range(0, R_CAP + 1):
            U1 = VAL(X, S - 1, m)
            n += 1
            if S % 2 == 0:
                if m % 2 == 1 and m <= S - 1 and U1 == 1:
                    bad.append(("A_evenS", X, m, U1))
            else:
                if m % 2 == 1 and m <= S - 2 and U1 == 1:
                    bad.append(("A_oddS", X, m, U1))
                if m % 2 == 0 and m <= S - 3 and U1 != 0:
                    bad.append(("B_oddS", X, m, U1))
            if len(bad) >= 20:
                return False, bad[:20], n
    return (len(bad) == 0), bad[:20], n


def C10_mex_case_lemma():
    """Exhaustive table: value forms and equality criterion (a in {0,1,2},
    D, e in 0..15)."""
    bad = []
    n = 0
    for a in (0, 1, 2):
        for D in range(0, 16):
            v = mex({a, 1 ^ D})
            n += 1
            want = None
            if a == 0:
                want = 2 if D == 0 else 1
            elif a == 1:
                want = 2 if D == 1 else 0
            else:
                want = 1 if D == 1 else 0
            if v != want:
                bad.append(("value", a, D, v, want))
    for a in (0, 1, 2):
        for D in range(0, 16):
            for e in range(0, 16):
                n += 1
                eq = band_pair(a, D, e)
                if a == 0:
                    want = (D == 0) == (e == 0)
                else:
                    want = (D == 1) == (e == 1)
                if eq != want:
                    bad.append(("criterion", a, D, e, eq, want))
                    if len(bad) >= 20:
                        return False, bad[:20], n
    return (len(bad) == 0), bad[:20], n


def C11_level2_and_zero_law():
    """Level-2 cascade claims + one-directional even-S diagonal zero law +
    L1-A extension. Non-singleton X, S >= 3, m <= R_CAP.
       Z2: S even: even j <= S-2 -> U2 == 0;  S odd: even j <= S-3 -> U2 == 0
       N2: S even: odd j <= S-2 -> U2 != 1;   S odd: odd j <= S-4 -> U2 != 1
       zero law (one-directional, S even): m even or m >= 2S -> D == 0
       L1-A extension: (S even: all odd m -> U1 != 1), (S odd: odd m <= S-2
                        -> U1 != 1; same band as C9, listed for completeness)"""
    bad = []
    n = 0
    for X in UNI:
        S = sum(X)
        if S < 3 or len(X) == 1:
            continue
        for m in range(0, R_CAP + 1):
            D = VAL(X, S, m)
            U1 = VAL(X, S - 1, m)
            U2 = VAL(X, S - 2, m)
            n += 3
            if S % 2 == 0:
                if m % 2 == 0 and m <= S - 2 and U2 != 0:
                    bad.append(("Z2_evenS", X, m, U2))
                if m % 2 == 1 and m <= S - 2 and U2 == 1:
                    bad.append(("N2_evenS", X, m, U2))
                if (m % 2 == 0 or m >= 2 * S) and D != 0:
                    bad.append(("zero_law", X, m, D))
                if m % 2 == 1 and U1 == 1:
                    bad.append(("L1A_ext_evenS", X, m, U1))
            else:
                if m % 2 == 0 and m <= S - 3 and U2 != 0:
                    bad.append(("Z2_oddS", X, m, U2))
                if m % 2 == 1 and m <= S - 4 and U2 == 1:
                    bad.append(("N2_oddS", X, m, U2))
            if len(bad) >= 20:
                return False, bad[:20], n
    return (len(bad) == 0), bad[:20], n


def C12_two_token_wide():
    """Pairs (parts <= 40, S <= 80), layer DP, r <= R_CAP:
    merge rows z=S+1,S+2; BAND claims; L1 stripes; Z2/N2 level-2."""
    uni = [()]
    for a in range(1, PART2 + 1):
        uni.append((a,))
    for a in range(1, PART2 + 1):
        for b in range(1, a + 1):
            uni.append((a, b))
    L, IX, W = build_dp(uni, ZMAX2, R_CAP)

    def val(X, z, r):
        return L[r][IX[X] * W + z]

    bad = []
    n = 0
    n_pairs = 0
    for X in uni:
        if len(X) != 2:
            continue
        n_pairs += 1
        S = sum(X)
        for z in (S + 1, S + 2):
            for r in range(0, R_CAP + 1):
                n += 1
                if val(X, z, r) != single_token(S, z, r):
                    bad.append(("merge", X, z, r, val(X, z, r), single_token(S, z, r)))
        for m in range(0, R_CAP + 1):
            D = val(X, S, m)
            U1 = val(X, S - 1, m)
            U2 = val(X, S - 2, m)
            n += 3
            if S % 2 == 0:
                if D == 1:
                    bad.append(("band_evenS_no1", X, m, D))
                if m % 2 == 0 and m <= S - 1 and D != 0:
                    bad.append(("band_evenS_even0", X, m, D))
                if m % 2 == 1 and m <= S - 1 and U1 == 1:
                    bad.append(("L1A_evenS", X, m, U1))
                if m % 2 == 0 and m <= S - 2 and U2 != 0:
                    bad.append(("Z2_evenS", X, m, U2))
                if m % 2 == 1 and m <= S - 2 and U2 == 1:
                    bad.append(("N2_evenS", X, m, U2))
            else:
                if (D == 0) != (m % 2 == 0 and m <= S - 1):
                    bad.append(("band_oddS_iff0", X, m, D))
                if m % 2 == 1 and m <= S - 2 and D == 1:
                    bad.append(("band_oddS_no1", X, m, D))
                if m % 2 == 1 and m <= S - 2 and U1 == 1:
                    bad.append(("L1A_oddS", X, m, U1))
                if m % 2 == 0 and m <= S - 3 and U1 != 0:
                    bad.append(("L1B_oddS", X, m, U1))
                if m % 2 == 0 and m <= S - 3 and U2 != 0:
                    bad.append(("Z2_oddS", X, m, U2))
                if m % 2 == 1 and m <= S - 4 and U2 == 1:
                    bad.append(("N2_oddS", X, m, U2))
            if len(bad) >= 20:
                return False, bad[:20], n
    ok = len(bad) == 0
    return ok, {"pairs": n_pairs, "violations": bad[:20]}, n


def sub_universe(X):
    """All sub-multisets of X closed under removals and v -> v-1."""
    subs = {(), X}
    frontier = {X}
    while frontier:
        newf = set()
        for Y in frontier:
            seen = set()
            for i, v in enumerate(Y):
                if v in seen:
                    continue
                seen.add(v)
                Z = Y[:i] + Y[i + 1:]
                if Z not in subs:
                    subs.add(Z)
                    newf.add(Z)
        frontier = newf
    changed = True
    while changed:
        changed = False
        for Y in list(subs):
            if not Y:
                continue
            seen = set()
            for i, v in enumerate(Y):
                if v in seen:
                    continue
                seen.add(v)
                if v > 1:
                    Z = tuple(sorted(Y[:i] + (v - 1,) + Y[i + 1:], reverse=True))
                    if Z not in subs:
                        subs.add(Z)
                        changed = True
    return sorted(subs)


def C13_deep_probes():
    """Deep probes (per-probe layer DP over the sub-universe closure):
    merge rows z=S+1,S+2; BAND; L1 stripes; Z2/N2; collapse identities.
    Finite evidence at deeper R than the grids."""
    baskets = [
        ((1,) * 25, 600),
        ((25, 5), 600),
        ((24, 12), 600),
        ((10, 8, 6), 400),
        ((20, 7, 7), 300),
        ((17, 16), 300),
        ((5, 4, 3, 2, 1), 300),
        ((13, 11, 9), 250),
    ]
    bad = []
    per_probe = []
    n = 0
    for X0, rmax in baskets:
        X = tuple(sorted(X0, reverse=True))
        S = sum(X)
        uni = sub_universe(X)
        zmax = S + 2 + len(X) + 2
        L, IX, W = build_dp(uni, zmax, rmax)

        def val(Y, z, r):
            return L[r][IX[Y] * W + z]

        probe_bad = 0
        for z in (S + 1, S + 2):
            for r in range(0, rmax + 1):
                n += 1
                if val(X, z, r) != single_token(S, z, r):
                    bad.append(("merge", X, z, r))
                    probe_bad += 1
        for m in range(0, rmax + 1):
            D = val(X, S, m)
            U1 = val(X, S - 1, m)
            U2 = val(X, S - 2, m)
            n += 3
            if S % 2 == 0:
                if D == 1:
                    bad.append(("band_evenS_no1", X, m, D))
                    probe_bad += 1
                if m % 2 == 0 and m <= S - 1 and D != 0:
                    bad.append(("band_evenS_even0", X, m, D))
                    probe_bad += 1
                if m % 2 == 1 and m <= S - 1 and U1 == 1:
                    bad.append(("L1A_evenS", X, m, U1))
                    probe_bad += 1
                if m % 2 == 0 and m <= S - 2 and U2 != 0:
                    bad.append(("Z2_evenS", X, m, U2))
                    probe_bad += 1
                if m % 2 == 1 and m <= S - 2 and U2 == 1:
                    bad.append(("N2_evenS", X, m, U2))
                    probe_bad += 1
            else:
                if (D == 0) != (m % 2 == 0 and m <= S - 1):
                    bad.append(("band_oddS_iff0", X, m, D))
                    probe_bad += 1
                if m % 2 == 1 and m <= S - 2 and D == 1:
                    bad.append(("band_oddS_no1", X, m, D))
                    probe_bad += 1
                if m % 2 == 1 and m <= S - 2 and U1 == 1:
                    bad.append(("L1A_oddS", X, m, U1))
                    probe_bad += 1
                if m % 2 == 0 and m <= S - 3 and U1 != 0:
                    bad.append(("L1B_oddS", X, m, U1))
                    probe_bad += 1
                if m % 2 == 0 and m <= S - 3 and U2 != 0:
                    bad.append(("Z2_oddS", X, m, U2))
                    probe_bad += 1
                if m % 2 == 1 and m <= S - 4 and U2 == 1:
                    bad.append(("N2_oddS", X, m, U2))
                    probe_bad += 1
            if m >= 1:
                n += 2
                a = single_token(S - 1, S, m - 1)
                if D != mex({a, 1 ^ val(X, S - 1, m - 1)}):
                    bad.append(("diag_collapse", X, m, D))
                    probe_bad += 1
                if m + 1 <= rmax:
                    ar = single_token(S - 1, S, m)
                    if val(X, S + 1, m + 1) != mex({ar, 1 ^ D}):
                        bad.append(("boundary_collapse", X, m + 1))
                        probe_bad += 1
        per_probe.append({"X": list(X), "S": S, "rmax": rmax, "universe": len(uni),
                          "violations": probe_bad})
    ok = len(bad) == 0
    return ok, {"probes": per_probe, "violations": bad[:20]}, n


def C14_band_table():
    """Band table B(k, S) for k <= S <= S_CAP_BAND (all multisets of sum S):
    the maximal prefix r <= R_CAP such that for ALL X with sum S,
    H(r; X; S-k) == single_token(S, S-k, r') for all r' <= r; and the start of
    the next band after the first failure. Observation only."""
    rows = []
    n = 0
    for S in range(1, S_CAP_BAND + 1):
        ixs = [IX[X] for X in UNI if sum(X) == S]
        for k in range(0, S + 1):
            z = S - k
            B = None
            r = 0
            while r <= R_CAP:
                ok = True
                for ix in ixs:
                    n += 1
                    if L[r][ix * W + z] != single_token(S, z, r):
                        ok = False
                        break
                if not ok:
                    B = r - 1
                    break
                r += 1
            else:
                B = R_CAP
            second = None
            r2 = B + 1
            while r2 <= R_CAP:
                ok = True
                for ix in ixs:
                    n += 1
                    if L[r2][ix * W + z] != single_token(S, z, r2):
                        ok = False
                        break
                if ok:
                    second = r2
                    break
                r2 += 1
            rows.append([k, S, z, B, second, "ALL" if B >= R_CAP else ""])
    return True, {"rows": rows}, n


# -------------------------------------------------------------------- main ---

UNI = None
L = None
IX = None
W = None


def VAL(X, z, r):
    return L[r][IX[X] * W + z]


def main():
    global UNI, L, IX, W
    os.makedirs(os.path.dirname(OUT), exist_ok=True)

    UNI = all_universe(S_CAP)
    L, IX, W = build_dp(UNI, ZMAX, R_CAP)

    check("C1_layer_dp_vs_verbatim_topdown", C1_dp_vs_topdown)
    check("C2_singleton_closed_form_grid", C2_singleton_closed_form)
    check("C3_sharpness_S_eq_z_counterexample_and_828", C3_counterexample_and_sharpness)
    check("C4_merge_rows_z_Sp1_Sp2_all_multisets", C4_merge_rows)
    check("C5_boundary_and_diagonal_collapse_identities", C5_collapse_identities)
    check("C6_boundary_compat_mex_identity", C6_compat)
    check("C7_band_S_even", C7_band_evenS)
    check("C8_band_S_odd", C8_band_oddS)
    check("C9_L1_stripe_claims", C9_L1_stripes)
    check("C10_mex_case_lemma_exhaustive", C10_mex_case_lemma)
    check("C11_level2_Z2_N2_zero_law_L1A_ext", C11_level2_and_zero_law)
    check("C12_two_token_wide_parts40", C12_two_token_wide)
    check("C13_deep_probes", C13_deep_probes)
    check("C14_band_table_BkS", C14_band_table)

    ok = all(v["pass"] for k, v in results.items())
    doc = {
        "pass": ok,
        "theorems_proved_symbolically": [
            "R1 far lemma: for z >= S+2 every child of (X, z) stays in the "
            "merged region, so MERGE at layer R-1 transfers to layer R",
            "R2 collapse lemma: H(R; X; S+1) = mex({single_token(S-1,S,R-1), "
            "1^D_X(R-1)}); likewise D_X(m) = mex({a(m-1), 1^U1_X(m-1)})",
            "R3 mex case lemma: mex({a,1^D}) == mex({a,1^e}) iff "
            "(a==0: D==0 iff e==0) or (a in {1,2}: D==1 iff e==1)",
            "reduction theorem: given MERGE(S') for S' < S, "
            "MERGE(S) iff BAND(S); hence universally "
            "(MERGE for all S) iff (BAND for all S)",
        ],
        "band_definition": {
            "S_even": "D_X(m) != 1 for all m; and D_X(m) == 0 for all even m <= S-1",
            "S_odd": "D_X(m) == 0 iff (m even and m <= S-1); and D_X(m) != 1 for odd m <= S-2",
            "note": "D_X(m) := H(m; X; S), quantified over all multisets X with sum S",
        },
        "census_only_no_universal_claim": [
            "BAND(S) itself within S <= 20 partitions (C7/C8), 2-token parts <= 40 "
            "(C12), deep probes to R <= 600 (C13)",
            "L1/L2 stripe cascade claims (C9/C11/C12/C13)",
            "one-directional even-S diagonal zero law: D == 0 if m even or m >= 2S (C11)",
            "band table B(k,S) and second-band structure (C14)",
        ],
        "open_frontier": [
            "BAND(S) universal (hence the general multiset merge universal)",
            "level-k cascade closure for k >= 3 (bands shrink ~1 per level; "
            "expected termination near k ~ S)",
        ],
        "trust_boundary": (
            "The universal claims are the symbolic proofs listed above "
            "(engines: verbatim K1101 recursion, K0832 closed form; not "
            "Lean-formalized). C1-C14 are finite deterministic double-checks: "
            "C1 anchor the DP to the verbatim recursion, C2 anchors the closed "
            "form, C3 fixes the sharpness boundary, C4-C13 are censuses in the "
            "stated finite domains, C14 is band extraction. No finite census is "
            "a universal statement; BAND and the cascade remain conjectures."
        ),
        "total_points": POINTS,
        "checks": results,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    print("pass" if ok else "FAIL", POINTS)
    for k in sorted(results):
        r = results[k]
        print(f"  {k}: pass={r['pass']} points={r['points']}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
