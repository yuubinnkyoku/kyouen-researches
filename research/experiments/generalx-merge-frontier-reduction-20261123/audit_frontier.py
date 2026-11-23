#!/usr/bin/env python3
"""general-X merge law (GX-M) and frontier reduction (FR-X) audit.
Experiment: research/experiments/generalx-merge-frontier-reduction-20261123/
Single-owner declaration: research/log/2026-11-23-generalx-merge-frontier-reduction-single-owner-note.md (commit efe21bd3, observed HEAD-before-push cf3fbe4a)

Provenance of the transcribed blocks (published bytes, @@TRANSCRIPTION
markers): the published y=18 universal verifier
vertical-fiber-two-token-y18-parametric-allz-proof-20261123/verify_y18_universal.py,
part2 edition, SHA-256 8ddd0c2f24213e658705a403ede55d185aab59e7b7d47bd68679d9b3b0b6072a
(51,925 bytes per its K1242 part2 publication), itself the published
transcription chain of the raw engines from the K1138 verifier and of the
closed forms cand17 (K1240 proved) and cand18 (K1242 proved). The engine
block carries H_ordered, H_canonical, mex, q_odd, single_token (published
single-token closed form) and (via the cand17 block) single_token_val
(published K0832 z-independent single-token merge-region profile).

Components (deterministic, fixed iteration orders, no clock):
  CX  engine cross-validation: new DP column engine vs published raw
      H_canonical, all cells, families (6,4),(9,7),(12,12),(20,20),(24,24),
      (28,26), z <= S+2, R <= 2S+6; plus H_ordered vs H_canonical spot
      battery on 3-token states.
  XB  published single-token closed-form raw anchor: x <= 24, all
      z <= x+3, R <= 2x+3, raw vs single_token.
  M2  fresh-family three-way battery (raw x DP x published closed forms):
      (x,y) in [{y,y+2} for y in {20,22,24,26,28,30}], columns z in
      {S,S+1,S+2}, R <= 2S+6: raw==DP, merge law z>=S+1, BSL parts on the
      boundary column z=S, F+-. Raw engine cache cleared per family.
  M2D DP comprehensive sweep: y=1..30, x=y..y+12: merge law (z=S+1,S+2,
      R<=2S+6), BSL (i) R<R*, (ii) tail from R*-1, (iii) first mismatch
      exactly at R* ((1,1) exempt: R*>2 sigma, empty divergence window),
      (iv) divergence confined to [R*,2 sigma], F+- (R<=2S+1).
      R* = x+2y+1+(x mod 2).
  G3  GX-M: 3-token sigma<=12, 4-token sigma<=10, 5-token sigma<=8 complete
      enumeration + stretch samples, z in {sigma+1,sigma+2}, R<=sigma+z+4,
      raw vs single_token_val.
  G4  F+-X: boundary rows z=sigma, R<=2 sigma+2, 3/4-token (sigma<=10) and
      5-token (sigma<=8) complete enumeration, raw.
  L4  low-R general-X reduction: R<=z+1, z<=sigma+3, raw vs single_token.
  E5  proved closed forms cand17/cand18 on their boundary rows z=S=x+Y,
      x=Y..Y+40, R<=2S+2: BSL + F+- with published single_token sides.
  C8  FR mex case table: all 27 (t,b,s) triples, machine-verified equality
      predicates (t=0: mex({0,1^b}) equal iff [b==0]==[s==0]; t!=0:
      mex({t,1^b}) equal iff [b==1]==[s==1]).

Status discipline: observed laws are finite machine audits only; the FR-X
lemma (report.md) is the proved structural content; nothing here promotes
a family to proved universal.

Fail-closed tamper battery: --tamper {1..6} applies a single corruption and
the run must report TAMPER-DETECTED (rc=1); TAMPER-MISSED (rc=2) is a
battery failure. T1 single_token_val flip (fires in M2D/G3), T2 R* shift,
T3 F zero-clause rewrite, T4 DP engine bit flip (fires in CX/M2D), T5
single_token R off-by-one (fires in L4/XB), T6 GX single-side sigma-1.

Output: --out JSON (sorted keys). overall_bad must be 0.
"""
from functools import lru_cache

# @@TRANSCRIPTION-ENGINE-START@@
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

# @@TRANSCRIPTION-ENGINE-END@@
# @@TRANSCRIPTION-CAND17-START@@
Y17 = 17

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

def in_T17(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y17 - 1:
        S = x + Y17
        return R % 2 == 1 and R <= q_odd(S)
    d = x - z
    o = R - z
    if d == -Y17:
        cap = (z + Y17 - 1) if z % 2 == 1 else (z + Y17)
        if R % 2 == 1 and R <= (z if z % 2 == 1 else z - 1):
            return True
        if z % 2 == 1:
            return o % 2 == 0 and 2 <= o <= cap - z
        else:
            return o % 2 == 1 and 1 <= o <= cap - z
    if z % 2 == 1:
        ladder = R % 2 == 1 and R <= z
        if (d + 3 * Y17) % 4 == 0:
            o_pin = (d + 3 * Y17) // 2
            if Y17 + 1 <= o_pin <= 2 * Y17 and R == z + o_pin:
                return True
        if d == Y17 + 1:
            return ladder or (o % 2 == 0 and 2 * Y17 <= o <= x + Y17)
        if d >= Y17 + 2:
            return ladder or R == z + 2 * Y17
        return ladder
    else:
        ladder = R % 2 == 1 and R <= z - 1
        if (d + 3 * Y17) % 4 == 2:
            o_pin = (d + 3 * Y17) // 2
            if Y17 + 1 <= o_pin <= 2 * Y17 and R == z + o_pin:
                return True
        if d == Y17 + 1:
            return ladder or (o % 2 == 1 and 2 * Y17 + 1 <= o <= x + Y17)
        if d >= Y17 + 2:
            return ladder or R == z + 2 * Y17 + 1
        return ladder

def _bk(off, k):
    return 1 <= off <= 2 * k - 1 and off % 2 == 1

def in_P17(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y17 - 1:
        S = x + Y17
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    off = R - z
    b17 = _bk(off, Y17)
    band_base = off % 2 == 0 and 2 * Y17 + 2 <= off <= x + Y17          # steady base rows
    band_int = off % 2 == 0 and 2 * Y17 + 2 <= off <= x + Y17 - 1       # steady I rows
    tail = x % 2 == 0 and R >= x + z + Y17 + 1                         # S odd rows (y=17: x even)
    if z % 2 == 1:
        if -Y17 <= d <= Y17 and d % 2 == 1:
            k = (d + 3 * Y17 + 1) // 4      # I rows: b_k U I[2k+1)  (diag d=-17 included, k=8)
            return _bk(off, k) or off >= 2 * k + 1
        if d == Y17 + 1:
            return b17                     # sweep row, base type: z odd x odd
        if d >= Y17 + 2:
            if d % 2 == 0:
                return b17 or band_base
            return b17 or band_int or tail
        return _bk(off, (d + 3 * Y17 + 1) // 4)  # base rows d even in [-16,16]
    else:
        if d == -Y17:
            return False                   # even-z diagonal: no value-1 at all (10th consecutive candidate)
        if d == Y17 + 1:
            return b17 or band_int or tail     # sweep row, I type: z even x even
        if d >= Y17 + 2:
            if d % 2 == 1:
                return b17 or band_base
            return b17 or band_int or tail
        if d % 2 == 0:
            k = (d + 3 * Y17 - 1) // 4       # I rows: b_k U I[2k+1)
            return _bk(off, k) or off >= 2 * k + 1
        return _bk(off, (d + 3 * Y17 + 1) // 4)  # base rows d odd in [-15,17]

def cand17(z, x, R):
    if R <= 0:
        return 0
    if in_T17(z, x, R):
        return 2
    if in_P17(z, x, R):
        return 1
    return 0
# @@TRANSCRIPTION-CAND17-END@@
# @@TRANSCRIPTION-CAND18-START@@
Y = 18

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

def in_T18(z, x, R):
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
        if (d + 3 * Y) % 4 == 0 and -Y + 4 <= d <= Y:
            if R == z + (d + 3 * Y) // 2:
                return True
        if d == Y + 1:
            return ladder or (o % 2 == 0 and 2 * Y <= o <= x + Y)
        if d >= Y + 2:
            return ladder or R == z + 2 * Y
        return ladder
    else:
        ladder = R % 2 == 1 and R <= z - 1
        if (d + 3 * Y) % 4 == 2 and -Y + 2 <= d <= Y - 2:
            if R == z + (d + 3 * Y) // 2:
                return True
        if d == Y + 1:
            return ladder or (o % 2 == 1 and 2 * Y + 1 <= o <= x + Y)
        if d >= Y + 2:
            return ladder or R == z + 2 * Y + 1
        return ladder

def _bk(off, k):
    return 1 <= off <= 2 * k - 1 and off % 2 == 1

def in_P18(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y - 1:
        S = x + Y
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    off = R - z
    b18 = _bk(off, Y)
    band = off % 2 == 0 and 2 * Y + 2 <= off <= x + Y          # steady/sweep even band
    tail = x % 2 == 1 and R >= x + z + Y + 1                    # S odd rows (y=18: x odd)
    if z % 2 == 1:
        if -Y <= d <= Y and d % 2 == 0:
            k = (d + 3 * Y + 2) // 4          # I rows: b_k U I[th) (diag d=-18 incl., k=9)
            th = 2 * k + (1 if (d + 3 * Y) % 4 == 0 else 0)   # pin rows (d==y mod4): 2k+1; skew: 2k
            return _bk(off, k) or off >= th
        if -Y + 1 <= d <= Y - 1 and d % 2 == 1:
            return _bk(off, (d + 3 * Y + 1) // 4)  # base rows d odd in [-17,17]
        if d == Y + 1:
            return b18                          # sweep row, base type: z odd x even
        return b18 or band or tail              # d >= Y+2 steady rows
    else:
        if d == -Y:
            return False                        # even-z diagonal: no value-1 (11th consecutive candidate family y=8..18)
        if -Y + 1 <= d <= Y - 1 and d % 2 == 1:
            k = (d + 3 * Y - 1) // 4           # I rows: b_k U I[2k+1)
            return _bk(off, k) or off >= 2 * k + 1
        if -Y + 2 <= d <= Y and d % 2 == 0:
            return _bk(off, (d + 3 * Y + 1) // 4)  # base rows d even in [-16,18] (d=18 saturates k=Y=18)
        return b18 or band or tail              # d >= Y+1 (sweep 19 incl.: x odd -> tail active)

def cand18(z, x, R):
    if R <= 0:
        return 0
    if in_T18(z, x, R):
        return 2
    if in_P18(z, x, R):
        return 1
    return 0
# @@TRANSCRIPTION-CAND18-END@@

# =====================================================================
# Audit components (new code for this experiment, 2026-11-23).
# Deterministic: fixed iteration orders, sorted JSON keys, no clock.
# =====================================================================
import argparse

GX_VARG = 0  # tamper hook: expected single-side sum = sigma - GX_VARG


def mex_new(opts):
    s = set(opts)
    m = 0
    while m in s:
        m += 1
    return m


# ----- DP column engine (validated against the published raw engines by CX) -----
def empty_table(Zmax, Rmax):
    # H(r, (), z): options = {1 ^ H(r-1, (), z-1)} if z>=1 else {}.
    # Values live in {0,1}: mex({v}) = 0 if v == 1 else 1 (v in {0,1}),
    # mex({}) = 0. With H(0,*,*) = 0 both induction steps give 0, so
    # H(r, (), z) == 0 for all r, z (inline lemma; CX verifies vs raw).
    return [[0] * (Rmax + 1) for _ in range(Zmax + 1)]


def singles_tables(x, Zmax, Rmax, empt):
    tabs = []
    for z in range(Zmax + 1):
        layer = [None]
        prev = tabs[z - 1] if z >= 1 else None
        for a in range(1, x + 1):
            col = [0] * (Rmax + 1)
            if a > 1:
                tok = layer[a - 1]
                if z >= 1:
                    zch = prev[a]
                    for r in range(1, Rmax + 1):
                        col[r] = mex_new((tok[r - 1], 1 ^ zch[r - 1]))
                else:
                    for r in range(1, Rmax + 1):
                        col[r] = mex_new((tok[r - 1],))
            else:
                tok = empt[z + 1]
                if z >= 1:
                    zch = prev[1]
                    for r in range(1, Rmax + 1):
                        col[r] = mex_new((tok[r - 1], 1 ^ zch[r - 1]))
                else:
                    for r in range(1, Rmax + 1):
                        col[r] = mex_new((tok[r - 1],))
            layer.append(col)
        tabs.append(layer)
    return tabs


def pair_col(z, a, b, Rmax, singles, prev, layer):
    col = [0] * (Rmax + 1)
    opts_cols = []
    if a > 1:
        if a - 1 >= b:
            opts_cols.append(layer[(a - 1, b)])
        elif a - 1 >= 1:
            opts_cols.append(layer[(b, a - 1)])
    else:
        opts_cols.append(singles[z + 1][1])
    if b > 1:
        opts_cols.append(layer[(a, b - 1)])
    else:
        if a >= 2:
            opts_cols.append(singles[z + 1][a])
    nz = len(opts_cols)
    if z >= 1:
        zch = prev[(a, b)]
        if nz == 2:
            c0, c1 = opts_cols
            for r in range(1, Rmax + 1):
                col[r] = mex_new((c0[r - 1], c1[r - 1], 1 ^ zch[r - 1]))
        else:
            c0 = opts_cols[0]
            for r in range(1, Rmax + 1):
                col[r] = mex_new((c0[r - 1], 1 ^ zch[r - 1]))
    else:
        if nz == 2:
            c0, c1 = opts_cols
            for r in range(1, Rmax + 1):
                col[r] = mex_new((c0[r - 1], c1[r - 1]))
        else:
            c0 = opts_cols[0]
            for r in range(1, Rmax + 1):
                col[r] = mex_new((c0[r - 1],))
    return col


def family_dp(x, y, Zmax, Rmax):
    """Two-token family (x, y), x >= y >= 1. Returns pair_tabs, singles with
    pair_tabs[z][(a,b)] = value column over r=0..Rmax for desc pairs (a,b),
    singles[z][a] likewise. Layers z = 0..Zmax+2 (consumption margin)."""
    Ztot = Zmax + 2
    empt = empty_table(Ztot + 2, Rmax)
    singles = singles_tables(x, Ztot + 1, Rmax, empt)
    pairs_by_sum = {}
    for a in range(1, x + 1):
        for b in range(1, min(a, y) + 1):
            pairs_by_sum.setdefault(a + b, []).append((a, b))
    sums = sorted(pairs_by_sum)
    pair_tabs = []
    for z in range(Ztot + 1):
        layer = {}
        prev = pair_tabs[z - 1] if z >= 1 else None
        for s in sums:
            for (a, b) in pairs_by_sum[s]:
                layer[(a, b)] = pair_col(z, a, b, Rmax, singles, prev, layer)
        pair_tabs.append(layer)
    return pair_tabs, singles


# ----- law predicates -----
def Rstar(x, y):
    return x + 2 * y + 1 + (x % 2)


def check_F(S, R, v, res):
    """F+- frontier conditions on a boundary value v = b_X(R).
    Every clause that fires is a violation; res["bad"] accumulates."""
    if S % 2 == 0:
        if R <= S - 1 and R % 2 == 1 and v == 1:
            res["bad"] += 1; res["first"].append(("F+1", R, v))
        if R <= S and R % 2 == 0 and v != 0:
            res["bad"] += 1; res["first"].append(("F+2", R, v))
        if S + 1 <= R <= 2 * S and v == 1:
            res["bad"] += 1; res["first"].append(("F+3", R, v))
    else:
        if R <= S - 2 and R % 2 == 1 and v == 1:
            res["bad"] += 1; res["first"].append(("F-1", R, v))
        if R <= S - 1 and R % 2 == 0 and v != 0:
            res["bad"] += 1; res["first"].append(("F-2", R, v))
        if S <= R <= 2 * S and v == 0:
            res["bad"] += 1; res["first"].append(("F-3", R, v))


def new_res():
    return {"n": 0, "bad": 0, "first": []}


def dp_audit_family(x, y, out):
    """Comprehensive DP audit of one two-token family: merge law,
    BSL parts (i)-(iv), F+- conditions."""
    S = x + y
    Rcap = 2 * S + 6
    pair_tabs, singles = family_dp(x, y, S + 2, Rcap)
    Rst = Rstar(x, y)
    b = pair_tabs[S][(x, y)]
    # merge law
    nm = nbad = 0
    for z in (S + 1, S + 2):
        col = pair_tabs[z][(x, y)]
        for R in range(0, Rcap + 1):
            nm += 1
            if col[R] != single_token_val(S, R):
                nbad += 1
                if len(out.setdefault("merge_first", [])) < 6:
                    out["merge_first"].append((x, y, z, R))
    # BSL parts
    b1 = b2 = wf = 0
    for R in range(0, Rcap + 1):
        s = single_token(S, S, R)
        if R < Rst:
            b1 += b[R] != s
        if Rst - 1 <= R <= 2 * S + 4:
            b2 += b[R] != (S % 2)
        if R >= 2 * S + 1:
            wf += b[R] != s
    first_mis = None
    for R in range(0, Rcap + 1):
        if b[R] != single_token(S, S, R):
            first_mis = R
            break
    rstop_bad = 0 if ((first_mis is None and (x, y) == (1, 1)) or first_mis == Rst) else 1
    # F conditions (per cell)
    fn = fb = 0
    for R in range(0, 2 * S + 2):
        r = {"bad": 0, "first": []}
        check_F(S, R, b[R], r)
        fn += 1
        if r["bad"]:
            fb += r["bad"]
            if len(out.setdefault("F_first", [])) < 6:
                out["F_first"].append((x, y, r["first"][:3]))
    out["merge"] = {"n": out["merge"]["n"] + nm, "bad": out["merge"]["bad"] + nbad}
    out["bsl1"] = {"n": out["bsl1"]["n"] + Rst, "bad": out["bsl1"]["bad"] + b1}
    out["bsl2"] = {"n": out["bsl2"]["n"] + (2 * S + 6 - Rst), "bad": out["bsl2"]["bad"] + b2}
    out["rstop"] = {"n": out["rstop"]["n"] + 1, "bad": out["rstop"]["bad"] + rstop_bad}
    out["window"] = {"n": out["window"]["n"] + 1, "bad": out["window"]["bad"] + (1 if wf else 0)}
    out["F"] = {"n": out["F"]["n"] + fn, "bad": out["F"]["bad"] + fb}


# ----- CX: engine cross-validation -----
def comp_cx():
    out = {"families": [], "n": 0, "bad": 0, "first": []}
    fams = [(6, 4), (9, 7), (12, 12), (20, 20), (24, 24), (28, 26)]
    for (x, y) in fams:
        S = x + y
        Rcap = 2 * S + 6
        pair_tabs, singles = family_dp(x, y, S + 2, Rcap)
        fb = 0
        for z in range(0, S + 3):
            for a in range(1, x + 1):
                for R in range(0, Rcap + 1):
                    out["n"] += 1
                    if singles[z][a][R] != H_canonical(R, (a,), z):
                        fb += 1
                        if len(out["first"]) < 5:
                            out["first"].append(("sing", a, z, R))
            for (a, b), col in sorted(pair_tabs[z].items()):
                for R in range(0, Rcap + 1):
                    out["n"] += 1
                    if col[R] != H_canonical(R, (a, b), z):
                        fb += 1
                        if len(out["first"]) < 5:
                            out["first"].append(("pair", (a, b), z, R))
        out["families"].append({"x": x, "y": y, "bad": fb})
        out["bad"] += fb
    spot = spot_bad = 0
    for X in [(3, 2, 1), (4, 4, 1), (7, 5, 3)]:
        sig = sum(X)
        for z in range(0, sig + 3):
            for R in range(0, 2 * sig + 7):
                spot += 1
                if H_ordered(R, X, z) != H_canonical(R, X, z):
                    spot_bad += 1
                    if len(out["first"]) < 5:
                        out["first"].append(("ordlrcan", X, z, R))
    out["ord_can_n"] = spot; out["ord_can_bad"] = spot_bad
    out["bad"] += spot_bad
    if out["bad"] == 0:
        out["first"] = []
    return out


# ----- XB: published single-token closed-form raw anchor -----
def comp_xb():
    out = new_res()
    for x in range(1, 25):
        for z in range(0, x + 4):
            for R in range(0, 2 * x + 4):
                out["n"] += 1
                v = single_token(x, z, R)
                if H_canonical(R, (x,), z) != v:
                    out["bad"] += 1
                    if len(out["first"]) < 5:
                        out["first"].append((x, z, R))
    if out["bad"] == 0:
        out["first"] = []
    return out


# ----- M2: fresh-family three-way battery (raw x DP x closed forms) -----
def comp_m2():
    out = {"families": [], "n": 0, "bad": 0, "first": []}
    for y in (20, 22, 24, 26, 28, 30):
        for x in (y, y + 2):
            S = x + y
            Rcap = 2 * S + 6
            pair_tabs, singles = family_dp(x, y, S + 2, Rcap)
            Rst = Rstar(x, y)
            fam = {"x": x, "y": y, "raw_dp": 0, "merge": 0, "bsl1": 0,
                   "bsl2": 0, "rstop": 0, "window": 0, "F": 0}
            for z in (S, S + 1, S + 2):
                col = pair_tabs[z][(x, y)]
                for R in range(0, Rcap + 1):
                    out["n"] += 1
                    raw = H_canonical(R, (x, y), z)
                    if raw != col[R]:
                        fam["raw_dp"] += 1
                        if len(out["first"]) < 5:
                            out["first"].append(("rawdp", x, y, z, R))
            for z in (S + 1, S + 2):
                for R in range(0, Rcap + 1):
                    out["n"] += 1
                    if H_canonical(R, (x, y), z) != single_token_val(S, R):
                        fam["merge"] += 1
                        if len(out["first"]) < 5:
                            out["first"].append(("merge", x, y, z, R))
            first_mis = None
            bsl1 = bsl2 = wf = 0
            for R in range(0, Rcap + 1):
                raw = H_canonical(R, (x, y), S)
                s = single_token(S, S, R)
                out["n"] += 1
                if R < Rst:
                    if raw != s:
                        bsl1 += 1
                        if len(out["first"]) < 5:
                            out["first"].append(("bsl1", x, y, R, raw, s))
                if Rst - 1 <= R <= 2 * S + 4:
                    if raw != (S % 2):
                        bsl2 += 1
                        if len(out["first"]) < 5:
                            out["first"].append(("bsl2", x, y, R, raw))
                if R >= 2 * S + 1 and raw != s:
                    wf += 1
                    if len(out["first"]) < 5:
                        out["first"].append(("win", x, y, R, raw, s))
                if first_mis is None and raw != s:
                    first_mis = R
            fam["bsl1"] = bsl1; fam["bsl2"] = bsl2
            fam["window"] = 1 if wf else 0
            fam["rstop"] = 0 if first_mis == Rst else 1
            fb = 0
            for R in range(0, 2 * S + 2):
                out["n"] += 1
                r = {"bad": 0, "first": []}
                check_F(S, R, H_canonical(R, (x, y), S), r)
                fb += r["bad"]
                if r["bad"] and len(out["first"]) < 5:
                    out["first"].append(("F", x, y, r["first"][:2]))
            fam["F"] = fb
            out["families"].append(fam)
            out["bad"] += sum(fam[k] for k in ("raw_dp", "merge", "bsl1", "bsl2", "rstop", "window", "F"))
            H_canonical.cache_clear()
    if out["bad"] == 0:
        out["first"] = []
    return out


# ----- M2D: DP comprehensive sweep -----
def comp_m2d():
    out = {"merge": {"n": 0, "bad": 0}, "bsl1": {"n": 0, "bad": 0},
           "bsl2": {"n": 0, "bad": 0}, "rstop": {"n": 0, "bad": 0},
           "window": {"n": 0, "bad": 0}, "F": {"n": 0, "bad": 0}}
    for y in range(1, 31):
        for x in range(y, y + 13):
            dp_audit_family(x, y, out)
    out["bad"] = sum(out[k]["bad"] for k in ("merge", "bsl1", "bsl2", "rstop", "window", "F"))
    return out


# ----- multiset enumeration -----
def gen_multisets(sigma_max, k):
    out = []
    def rec(prefix, maxv, k_left, s_left):
        if k_left == 0:
            out.append(tuple(prefix))
            return
        for v in range(min(maxv, s_left - (k_left - 1)), 0, -1):
            rec(prefix + [v], v, k_left - 1, s_left - v)
    rec([], sigma_max, k, sigma_max)
    return out


GX_STRETCH = [(7, 5, 3), (8, 4, 2), (10, 7, 5), (12, 9, 3), (9, 8, 7),
              (6, 5, 4, 3), (8, 6, 4, 2), (5, 4, 3, 2, 1), (7, 7, 7, 7, 3)]

L4_STRETCH = [(7, 5, 3), (6, 5, 4, 3), (5, 4, 3, 2, 1), (7, 7, 7, 7, 3)]


# ----- G3: general-X merge law (raw) -----
def comp_g3():
    out = new_res()
    fams = list(gen_multisets(12, 3)) + list(gen_multisets(10, 4)) + list(gen_multisets(8, 5)) + GX_STRETCH
    out["families"] = len(fams)
    for X in fams:
        sig = sum(X)
        for z in (sig + 1, sig + 2):
            for R in range(0, sig + z + 5):
                out["n"] += 1
                v = single_token_val(sig - GX_VARG, R)
                if H_canonical(R, X, z) != v:
                    out["bad"] += 1
                    if len(out["first"]) < 6:
                        out["first"].append((X, z, R, v))
    if out["bad"] == 0:
        out["first"] = []
    return out


# ----- G4: F+-X on 3/4/5-token boundary rows (raw) -----
def comp_g4():
    out = new_res()
    fams = list(gen_multisets(10, 3)) + list(gen_multisets(10, 4)) + list(gen_multisets(8, 5))
    out["families"] = len(fams)
    for X in fams:
        sig = sum(X)
        for R in range(0, 2 * sig + 3):
            out["n"] += 1
            r = {"bad": 0, "first": []}
            check_F(sig, R, H_canonical(R, X, sig), r)
            if r["bad"]:
                out["bad"] += r["bad"]
                if len(out["first"]) < 6:
                    out["first"].append((X, R, r["first"][:2]))
    if out["bad"] == 0:
        out["first"] = []
    return out


# ----- L4: low-R reduction for general X (raw) -----
def comp_l4():
    out = new_res()
    fams = list(gen_multisets(10, 3)) + list(gen_multisets(9, 4)) + list(gen_multisets(7, 5)) + L4_STRETCH
    out["families"] = len(fams)
    for X in fams:
        sig = sum(X)
        for z in range(0, sig + 4):
            for R in range(0, z + 2):
                out["n"] += 1
                v = single_token(sig, z, R)
                if H_canonical(R, X, z) != v:
                    out["bad"] += 1
                    if len(out["first"]) < 6:
                        out["first"].append((X, z, R, v))
    if out["bad"] == 0:
        out["first"] = []
    return out


# ----- E5: proved closed forms cand17/cand18 on their boundary rows -----
def comp_e5():
    out = new_res()
    out["checks"] = 0
    for Y, cand in ((17, cand17), (18, cand18)):
        for x in range(Y, Y + 41):
            S = x + Y
            Rst = Rstar(x, Y)
            for R in range(0, 2 * S + 3):
                out["n"] += 1
                b = cand(S, x, R)
                s = single_token(S, S, R)
                if R < Rst and b != s:
                    out["bad"] += 1
                    if len(out["first"]) < 6: out["first"].append(("bsl1", Y, x, R, b, s))
                if Rst - 1 <= R <= 2 * S + 2 and b != (S % 2):
                    out["bad"] += 1
                    if len(out["first"]) < 6: out["first"].append(("bsl2", Y, x, R, b))
                if R >= 2 * S + 1 and b != s:
                    out["bad"] += 1
                    if len(out["first"]) < 6: out["first"].append(("win", Y, x, R))
                r = {"bad": 0, "first": []}
                check_F(S, R, b, r)
                out["checks"] += 1
                if r["bad"]:
                    out["bad"] += r["bad"]
                    if len(out["first"]) < 6: out["first"].append(("F", Y, x, r["first"][:2]))
    if out["bad"] == 0:
        out["first"] = []
    return out


# ----- C8: FR mex case table -----
def comp_c8():
    out = {"cases": [], "n": 0, "bad": 0}
    for t in (0, 1, 2):
        for b in (0, 1, 2):
            for s in (0, 1, 2):
                lhs = mex_new((t, 1 ^ b))
                rhs = mex_new((t, 1 ^ s))
                if t == 0:
                    pred_eq = (b == 0) == (s == 0)
                else:
                    pred_eq = (b == 1) == (s == 1)
                actual_eq = (lhs == rhs)
                out["n"] += 1
                out["cases"].append({"t": t, "b": b, "s": s, "mex_lhs": lhs,
                                     "mex_rhs": rhs, "predicted_equal": pred_eq,
                                     "actually_equal": actual_eq})
                if pred_eq != actual_eq:
                    out["bad"] += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--components", default="CX,XB,M2,M2D,G3,G4,L4,E5,C8")
    ap.add_argument("--out", default="output/audit.json")
    ap.add_argument("--tamper", default="0")
    args = ap.parse_args()
    tam = int(args.tamper)

    # fail-closed tamper battery (each variant must produce bad > 0)
    if tam == 1:
        _orig = single_token_val
        globals()["single_token_val"] = lambda S, R: 0 if (S == 7 and R == 1) else _orig(S, R)
    if tam == 2:
        globals()["Rstar"] = lambda x, y: x + 2 * y + 2 + (x % 2)
    if tam == 3:
        _cf = check_F
        def flipped(S, R, v, res):
            if S % 2 == 0:
                if R <= S and R % 2 == 0 and v != 1:
                    res["bad"] += 1; res["first"].append(("F+2x", R, v))
            if S % 2 == 1:
                if R <= S - 1 and R % 2 == 0 and v != 1:
                    res["bad"] += 1; res["first"].append(("F-2x", R, v))
            _cf(S, R, v, res)
        globals()["check_F"] = flipped
    if tam == 4:
        _fd = family_dp
        def fd_bug(x, y, Zmax, Rmax):
            pt, sg = _fd(x, y, Zmax, Rmax)
            pt[0][(x, y)][1] ^= 2
            return pt, sg
        globals()["family_dp"] = fd_bug
    if tam == 5:
        _st = single_token
        globals()["single_token"] = lambda x, z, R: _st(x, z, R + 1)
    if tam == 6:
        globals()["GX_VARG"] = 1

    comps = {c: globals()["comp_" + c.lower()] for c in args.components.split(",")}
    audit = {"components": {}, "overall_bad": 0}
    for name, fn in comps.items():
        res = fn()
        audit["components"][name] = res
        audit["overall_bad"] += res.get("bad", 0)
    import json
    with open(args.out, "w") as f:
        json.dump(audit, f, sort_keys=True, separators=(",", ":"))

    if tam != 0:
        if audit["overall_bad"] > 0:
            print("TAMPER-DETECTED bad=", audit["overall_bad"])
            raise SystemExit(1)
        else:
            print("TAMPER-MISSED")
            raise SystemExit(2)
    print("overall_bad =", audit["overall_bad"])
    raise SystemExit(0 if audit["overall_bad"] == 0 else 1)


if __name__ == "__main__":
    main()
