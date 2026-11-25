#!/usr/bin/env python3
"""Independent verifier for the z=11, y=2 two-token residual-game slice (K1013)."""
from __future__ import annotations
import json, random, sys
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(1_000_000)

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

# K0832 single-token closed form (transcribed from the published proof).
def v_single(x, z, R):
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

# ---------------------------------------------------------------- B child: K1012 (z=11, y=1, proved)
def b_T(x, r):
    if x <= 12:
        return 1 <= r <= x + 1 and r % 2 == 1
    if x == 13:
        return 1 <= r <= 25 and r % 2 == 1
    return r in (1, 3, 5, 7, 9, 11, 13)

def b_P(x, r):
    if x == 1:
        return False
    if x <= 10:
        return x % 2 == 0 and r >= x + 2
    if x == 11:
        return r == 12
    if x == 12:
        return r == 12 or r >= 14
    if x == 13:
        return r == 12
    if x % 2 == 0:
        return r == 12 or (r % 2 == 1 and 15 <= r <= x + 13) or r >= x + 14
    return r == 12 or (r % 2 == 1 and 15 <= r <= x + 12)

def b_val(x, r):
    if r == 0:
        return 0
    if b_T(x, r):
        return 2
    if b_P(x, r):
        return 1
    return 0

# ---------------------------------------------------------------- C child: K1004 (z=10, y=2, proved)
T_CAND = {
    2: {1, 3}, 3: {1, 3, 5}, 4: {1, 3, 5}, 5: {1, 3, 5, 7},
    6: {1, 3, 5, 7}, 7: {1, 3, 5, 7, 9}, 8: {1, 3, 5, 7, 9, 11},
    9: {1, 3, 5, 7, 9}, 10: {1, 3, 5, 7, 9, 13}, 11: {1, 3, 5, 7, 9},
    12: {1, 3, 5, 7, 9},
}

def c_T(x, r):
    if x in T_CAND:
        return r in T_CAND[x]
    if x == 13:
        return r in (1, 3, 5, 7, 9) or (15 <= r <= 25 and r % 2 == 1)
    return r in (1, 3, 5, 7, 9, 15)

def c_P(x, r):
    if x in (2, 4, 6, 8):
        return False
    if x == 3:
        return r >= 6
    if x == 5:
        return r >= 8
    if x == 7:
        return r >= 10
    if x in (9, 11):
        return r in (11, 13) or r >= 14
    if x == 10:
        return r == 11
    if x == 12:
        return r in (11, 13)
    if x % 2 == 1:
        return r in (11, 13) or (16 <= r <= x + 11 and r % 2 == 0) or r >= x + 13
    return r in (11, 13) or (16 <= r <= x + 12 and r % 2 == 0)

def c_val(x, r):
    if r == 0:
        return 0
    if c_T(x, r):
        return 2
    if c_P(x, r):
        return 1
    return 0

# ------------------------------------------------- candidate: z=11, y=2 closed form (K1013)
def cand_T(x, r):
    if x == 2:
        return r in (1, 3)
    if x in (3, 4):
        return r in (1, 3, 5)
    if x in (5, 6):
        return r in (1, 3, 5, 7)
    if x in (7, 8):
        return r in (1, 3, 5, 7, 9)
    if x == 9:
        return r in (1, 3, 5, 7, 9, 11, 13)
    if x in (10, 11, 12):
        return r in (1, 3, 5, 7, 9, 11)
    if x == 13:
        return r in (1, 3, 5, 7, 9, 11, 15)
    if x == 14:
        return r in (1, 3, 5, 7, 9, 11) or (15 <= r <= 27 and r % 2 == 1)
    return r in (1, 3, 5, 7, 9, 11, 15)

def cand_P(x, r):
    if x in (2, 4, 6, 8):
        return False
    if x == 3:
        return r >= 6
    if x == 5:
        return r >= 8
    if x == 7:
        return r >= 10
    if x in (9, 11):
        return r in (12, 14) or r >= 15
    if x == 10:
        return r == 12
    if x == 12:
        return r in (12, 14)
    if x == 13:
        return r in (12, 14) or r >= 16
    if x == 14:
        return r in (12, 14)
    if x % 2 == 0:
        return r in (12, 14) or (17 <= r <= x + 13 and r % 2 == 1)
    return r in (12, 14) or (17 <= r <= x + 12 and r % 2 == 1) or r >= x + 14

def cand(x, R):
    if R == 0:
        return 0
    if cand_T(x, R):
        return 2
    if cand_P(x, R):
        return 1
    return 0

# ------------------------------------------------------------- proof: A/B/C option sets
def opts_ABC(x, R):
    """Options of H(R;(x,2);11): A = slice at (x-1, R-1) for x>=3
    (x-outer induction), B = K1012 (z=11,y=1) at (x, R-1),
    C = 1 xor K1004 (z=10,y=2) at (x, R-1). For x=2 the two
    token-decrement moves collapse onto the same (2,1);11 child."""
    r = R - 1
    s = set()
    if x >= 3:
        s.add(cand(x - 1, r))
        s.add(b_val(x, r))
    else:
        s.add(b_val(2, r))
    s.add(1 ^ c_val(x, r))
    return s

# ------------------------------------------------------- band table (proof) for z=11,y=2
PRE = [(1, 11, "01", "odd"), (2, 10, "23", "even"),
       (12, 12, "02", None), (13, 13, "1", None), (14, 14, "02", None),
       (15, 15, "01", None), (16, 16, "123", None), (17, 17, "0", None)]

def bands_for(x):
    """List of (lo, hi, signature, parity); hi None = open-ended, parity
    None = every R, "odd"/"even" = only odd/even R in [lo, hi]."""
    if x == 2:
        return [(1, 1, "01", None), (2, 2, "23", None), (3, 3, "01", None),
                (4, 4, "23", None), (5, None, "1", None)]
    if x == 3:
        return [(1, 1, "01", None), (2, 2, "23", None), (3, 3, "01", None),
                (4, 4, "23", None), (5, 5, "01", None), (6, 6, "03", None),
                (7, None, "0", None)]
    if x == 4:
        return [(1, 1, "01", None), (2, 2, "23", None), (3, 3, "01", None),
                (4, 4, "23", None), (5, 5, "01", None), (6, 6, "23", None),
                (7, None, "1", None)]
    if x == 5:
        return [(1, 1, "01", None), (2, 2, "23", None), (3, 3, "01", None),
                (4, 4, "23", None), (5, 5, "01", None), (6, 6, "23", None),
                (7, 7, "01", None), (8, 8, "03", None), (9, None, "0", None)]
    if x == 6:
        return [(1, 1, "01", None), (2, 2, "23", None), (3, 3, "01", None),
                (4, 4, "23", None), (5, 5, "01", None), (6, 6, "23", None),
                (7, 7, "01", None), (8, 8, "23", None), (9, None, "1", None)]
    if x == 7:
        return [(1, 1, "01", None), (2, 2, "23", None), (3, 3, "01", None),
                (4, 4, "23", None), (5, 5, "01", None), (6, 6, "23", None),
                (7, 7, "01", None), (8, 8, "23", None), (9, 9, "01", None),
                (10, 10, "03", None), (11, None, "0", None)]
    if x == 8:
        return [(1, 1, "01", None), (2, 2, "23", None), (3, 3, "01", None),
                (4, 4, "23", None), (5, 5, "01", None), (6, 6, "23", None),
                (7, 7, "01", None), (8, 8, "23", None), (9, 9, "01", None),
                (10, 10, "23", None), (11, 11, "1", None), (12, 12, "13", None),
                (13, None, "1", None)]
    if x == 9:
        return PRE[:2] + [(12, 12, "0", None), (13, 13, "01", None),
                          (14, None, "0", None)]
    if x == 10:
        return PRE[:2] + [(12, 12, "02", None), (13, 13, "1", None),
                          (14, 14, "123", None), (15, None, "1", None)]
    if x == 11:
        return PRE[:2] + [(12, 12, "02", None), (13, 13, "1", None),
                          (14, None, "0", None)]
    if x == 12:
        return PRE[:2] + [(12, 12, "02", None), (13, 13, "1", None),
                          (14, 14, "02", None), (15, None, "1", None)]
    if x == 13:
        return PRE[:2] + [(12, 12, "02", None), (13, 13, "1", None),
                          (14, 14, "02", None), (15, 15, "01", None),
                          (16, 26, "023", "even"), (17, 25, "0", "odd"),
                          (27, None, "0", None)]
    if x == 14:
        return PRE[:2] + [(12, 12, "02", None), (13, 13, "1", None),
                          (14, 14, "02", None), (15, 15, "01", None),
                          (16, 16, "123", None), (17, 27, "01", "odd"),
                          (18, 26, "1", "even"), (28, None, "1", None)]
    if x == 15:
        return PRE + [(18, 28, "12", "even"), (19, 28, "0", "odd"),
                      (29, None, "0", None)]
    if x % 2 == 0:   # even x >= 16
        return PRE + [(18, x + 13, "1", "even"), (19, x + 13, "0", "odd"),
                      (x + 14, None, "1", None)]
    # odd x >= 17
    return PRE + [(18, x + 13, "1", "even"), (19, x + 13, "0", "odd"),
                  (x + 14, None, "0", None)]

def band_sig_at(x, R):
    for lo, hi, s, p in bands_for(x):
        if R >= lo and (hi is None or R <= hi):
            if p == "odd" and R % 2 == 0:
                continue
            if p == "even" and R % 2 == 1:
                continue
            return s
    return None

def band_sigset(s):
    return {int(c) for c in s}

# --------------------------------------------------------------------------- audit
def run_audit():
    audit = {"checks": {}, "fail": [], "n_points": 0}
    def check(name, ok, detail):
        audit["checks"][name] = {"ok": bool(ok), **detail}
        if not ok:
            audit["fail"].append(name)

    # V1-V3: two direct engines vs the closed form.
    bad = [0, 0, 0]; ex = [None, None, None]; n = 0
    for x in range(2, 81):
        for R in range(0, x + 47):
            n += 1
            a = H_ordered(R, (x, 2), 11)
            b = H_canonical(R, (x, 2), 11)
            c = cand(x, R)
            for j, ok in enumerate((a == c, b == c, a == b)):
                if not ok:
                    bad[j] += 1
                    if ex[j] is None: ex[j] = (x, R, a, b, c)
    for j, name in enumerate(("V1_ordered_direct_vs_formula",
                              "V2_canonical_direct_vs_formula",
                              "V3_two_direct_engines_agree")):
        check(name, bad[j] == 0, {"points": n, "bad": bad[j], "example": ex[j]})
    audit["n_points"] += 3 * n

    # V4-V8: A/B/C anchor mex, signature-band coverage, band vs ABC,
    # band mex, band mex vs formula.
    names = ("V4_ABC_anchor_mex_matches_formula", "V5_signature_band_coverage",
             "V6_signature_band_matches_ABC", "V7_signature_mex_matches_ABC",
             "V8_signature_mex_matches_formula")
    bad = [0] * 5; ex = [None] * 5; n = 0
    for x in range(2, 3001):
        for R in range(1, x + 32):
            n += 1
            opts = opts_ABC(x, R)
            am = mex(opts)
            actual = "".join(map(str, sorted(opts)))
            expected = band_sig_at(x, R)
            if am != cand(x, R):
                bad[0] += 1
                if ex[0] is None: ex[0] = (x, R, am, cand(x, R), actual)
            if expected is None:
                bad[1] += 1
                if ex[1] is None: ex[1] = (x, R)
            elif expected != actual:
                bad[2] += 1
                if ex[2] is None: ex[2] = (x, R, expected, actual)
            else:
                tm = mex(band_sigset(expected))
                if tm != am:
                    bad[3] += 1
                    if ex[3] is None: ex[3] = (x, R, expected, tm, am)
                if tm != cand(x, R):
                    bad[4] += 1
                    if ex[4] is None: ex[4] = (x, R, expected, tm, cand(x, R))
    for j, name in enumerate(names):
        check(name, bad[j] == 0, {"points": n, "bad": bad[j], "example": ex[j]})
    audit["n_points"] += 5 * n

    # V9: general tail R >= x+14 => H = (x+2) mod 2 (K0832 general tail).
    bad_tail = 0; ex_tail = None; tail_points = 0
    for x in range(2, 10001):
        for off in range(5):
            R = x + 14 + off
            tail_points += 1
            got = cand(x, R); want = (x + 2) % 2
            if got != want:
                bad_tail += 1
                if ex_tail is None: ex_tail = (x, R, got, want)
    check("V9_general_tail", bad_tail == 0,
          {"points": tail_points, "bad": bad_tail, "example": ex_tail,
           "claim": "R >= x+14 => H=(x+2) mod 2"})
    audit["n_points"] += tail_points

    # V10: Theorem T parity bound (odd R <= 2, even R <= 1).
    parity_bad = 0; ex_parity = None; parity_points = 0
    for x in range(2, 3001):
        for R in range(1, x + 32):
            parity_points += 1
            got = cand(x, R); bound = 2 if R % 2 else 1
            if got > bound:
                parity_bad += 1
                if ex_parity is None: ex_parity = (x, R, got, bound)
    check("V10_theorem_T_parity_bound", parity_bad == 0,
          {"points": parity_points, "bad": parity_bad, "example": ex_parity})
    audit["n_points"] += parity_points

    # V11: B-child anchor: direct recursion vs published K1012 transcription.
    bad_b = 0; ex_b = None; n = 0
    for x in range(1, 81):
        for R in range(0, x + 47):
            n += 1
            a = H_ordered(R, (x, 1), 11); b = b_val(x, R)
            if a != b:
                bad_b += 1
                if ex_b is None: ex_b = (x, R, a, b)
    check("V11_K1012_child_anchor", bad_b == 0,
          {"points": n, "bad": bad_b, "example": ex_b})
    audit["n_points"] += n

    # V12: C-child anchor: direct recursion vs published K1004 transcription.
    bad_c = 0; ex_c = None; n = 0
    for x in range(2, 81):
        for R in range(0, x + 47):
            n += 1
            a = H_ordered(R, (x, 2), 10); b = c_val(x, R)
            if a != b:
                bad_c += 1
                if ex_c is None: ex_c = (x, R, a, b)
    check("V12_K1004_child_anchor", bad_c == 0,
          {"points": n, "bad": bad_c, "example": ex_c})
    audit["n_points"] += n

    # V13: height-only reduction for R <= z+1 = 12 vs v_single(x+2, 11, R).
    bad_h = 0; ex_h = None; n = 0
    for x in range(2, 81):
        for R in range(0, 13):
            n += 1
            a = H_ordered(R, (x, 2), 11); b = v_single(x + 2, 11, R)
            if a != b:
                bad_h += 1
                if ex_h is None: ex_h = (x, R, a, b)
    check("V13_height_only_reduction_low_R", bad_h == 0,
          {"points": n, "bad": bad_h, "example": ex_h,
           "claim": "R<=12: H((x,2);11) = v_single(x+2,11,R)"})
    audit["n_points"] += n

    # V14: fixed-seed broad scatter via A/B/C mex.
    rng = random.Random(20261119)
    bad_scatter = 0; ex_scatter = None; n = 20000
    for _ in range(n):
        x = rng.randint(2, 5000); R = rng.randint(0, x + 100)
        am = mex(opts_ABC(x, R)) if R >= 1 else 0
        got = cand(x, R)
        if am != got:
            bad_scatter += 1
            if ex_scatter is None: ex_scatter = (x, R, am, got)
    check("V14_fixed_seed_scatter", bad_scatter == 0,
          {"points": n, "bad": bad_scatter, "example": ex_scatter,
           "seed": 20261119})
    audit["n_points"] += n

    audit["all_ok"] = not audit["fail"]
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
    raise SystemExit(main())
