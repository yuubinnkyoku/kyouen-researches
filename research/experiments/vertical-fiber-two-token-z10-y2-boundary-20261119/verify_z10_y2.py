#!/usr/bin/env python3
"""Independent verifier for the z=10, y=2 boundary slice of the two-token
vertical-fiber residual game (K1004; mirror of verify_z10_y1.py for K1003).

Candidate closed form: cand(x, R) below.  Checks:

  V1  direct recursion vs candidate, dense grid      2<=x<=60, R<=x+40
  V2  direct recursion vs anchor-mex, dense grid     2<=x<=60, R<=x+40
  V3  band table: coverage, signature, mex vs anchor 2<=x<=2000, R<=x+26
  V4  B-child transfer (K1003 z=10,y=1) vs direct     2<=x<=60, R<=x+40
  V5  C-child transfer (K0988 z=9,y=2) vs direct     2<=x<=60, R<=x+40
  V6  tail parity ((x+2) mod 2 for R>=x+13)          x<=5000, R in [x+13,x+16]
  V7  wide-x low-R scan vs direct recursion          2<=x<=500, R<=12
  V8  fixed-seed scatter                              seed=20261120, 20000 pts
  V9  Theorem T parity identities on the band table  x<=2000
  V10 iterativeDP (second implementation) vs cand    2<=x<=30, R<=x+30
  V11 height-only reduction (K0832) R<=11            2<=x<=500, R<=11

All implementations are written from the primary sources (game rules,
K0832 single-token formula, K1003 z=10 y=1 closed form, K0988 z=9 y=2
closed form) independently of the exploration script.

Output: output/audit.json (deterministic; run twice, compare byte-wise).
"""

import sys, json, os, random
from functools import lru_cache

sys.setrecursionlimit(1000000)
AUDIT = {"checks": {}, "fail": [], "n_points": 0}

# ---------------------------------------------------------------- recursion
# Two-token vertical fiber: tokens X, residual credit z.  Moves:
# (i) token v>1 -> v-1; (ii) token 1 removed, z -> z+1;
# (iii) z>=1: z -> z-1, value 1 ^ child.
@lru_cache(maxsize=None)
def H(R, X, z):
    if R == 0:
        return 0
    opts = set()
    seen = set()
    for i, v in enumerate(X):
        if v in seen:
            continue
        seen.add(v)
        if v > 1:
            opts.add(H(R - 1, tuple(sorted(X[:i] + X[i + 1:] + (v - 1,))), z))
        else:
            opts.add(H(R - 1, tuple(sorted(X[:i] + X[i + 1:])), z + 1))
    if z >= 1:
        opts.add(1 ^ H(R - 1, X, z - 1))
    if not opts:
        return 0
    m = 0
    while m in opts:
        m += 1
    return m


def mex(s):
    m = 0
    while m in s:
        m += 1
    return m


def sig(s):
    return "".join(str(v) for v in sorted(s))


# ------------------------------------------- K0832 single-token formula
def qod(k):
    return k if k % 2 == 1 else k - 1


def v_single(x, z, R):
    """Single-token closed form (K0832): all x>=1, z>=0."""
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 == 1 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = qod(z)
        if R <= m:
            return 2 if R % 2 == 1 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = qod(x)
        if R <= m:
            return 2 if R % 2 == 1 else 0
        return x % 2
    raise ValueError((x, z, R))


# ------------------------------------------- K1003 (z=10, y=1, proved): B child
T10Y1 = {
    1: {1}, 2: {1, 3}, 3: {1, 3}, 4: {1, 3, 5}, 5: {1, 3, 5},
    6: {1, 3, 5, 7}, 7: {1, 3, 5, 7}, 8: {1, 3, 5, 7, 9},
    9: {1, 3, 5, 7, 9, 11}, 10: {1, 3, 5, 7, 9}, 11: {1, 3, 5, 7, 9},
}


def b_T(x, R):
    if x in T10Y1:
        return R in T10Y1[x]
    if x == 12:
        return R in (1, 3, 5, 7, 9) or (13 <= R <= 23 and R % 2 == 1)
    return R in (1, 3, 5, 7, 9, 13)


def b_P(x, R):
    if x in (1, 3, 5, 7, 9):
        return False
    if x == 2:
        return R >= 4
    if x == 4:
        return R >= 6
    if x == 6:
        return R >= 8
    if x == 8:
        return R >= 10
    if x == 10:
        return R >= 11
    if x == 11:
        return R == 11
    if x == 12:
        return R == 11 or (14 <= R <= 22 and R % 2 == 0) or R >= 24
    if x % 2 == 1:
        return R == 11 or (14 <= R <= x + 11 and R % 2 == 0)
    return R == 11 or (14 <= R <= x + 10 and R % 2 == 0) or R >= x + 12


def b_val(x, R):
    if R == 0:
        return 0
    if b_T(x, R):
        return 2
    if b_P(x, R):
        return 1
    return 0


# ------------------------------------------- K0988 (z=9, y=2, proved): C child
T9Y2 = {
    2: {1, 3}, 3: {1, 3, 5}, 4: {1, 3, 5}, 5: {1, 3, 5, 7},
    6: {1, 3, 5, 7}, 7: {1, 3, 5, 7, 9, 11}, 8: {1, 3, 5, 7, 9},
    9: {1, 3, 5, 7, 9}, 10: {1, 3, 5, 7, 9}, 11: {1, 3, 5, 7, 9, 13},
}


def c_T(x, R):
    if x in T9Y2:
        return R in T9Y2[x]
    if x == 12:
        return R in (1, 3, 5, 7, 9, 13) or (15 <= R <= 23 and R % 2 == 1)
    return R in (1, 3, 5, 7, 9, 13)


def c_P(x, R):
    if x in (2, 4, 6):
        return False
    if x == 3:
        return R >= 6
    if x == 5:
        return R >= 8
    if x == 7:
        return R == 10 or R >= 12
    if x == 8:
        return R == 10
    if x == 9:
        return R == 10 or R >= 12
    if x == 10:
        return R in (10, 12)
    if x == 11:
        return R in (10, 12) or R >= 14
    if x == 12:
        return R in (10, 12)
    if x % 2 == 1:
        return R in (10, 12) or (15 <= R <= x + 12 and R % 2 == 1) or R >= x + 13
    return R in (10, 12) or (15 <= R <= x + 11 and R % 2 == 1)


def c_val(x, R):
    if R == 0:
        return 0
    if c_T(x, R):
        return 2
    if c_P(x, R):
        return 1
    return 0


# ------------------------------------------- candidate: z=10, y=2 closed form
T_CAND = {
    2: {1, 3}, 3: {1, 3, 5}, 4: {1, 3, 5}, 5: {1, 3, 5, 7},
    6: {1, 3, 5, 7}, 7: {1, 3, 5, 7, 9}, 8: {1, 3, 5, 7, 9, 11},
    9: {1, 3, 5, 7, 9}, 10: {1, 3, 5, 7, 9, 13}, 11: {1, 3, 5, 7, 9},
    12: {1, 3, 5, 7, 9},
}


def cand_T(x, R):
    if x in T_CAND:
        return R in T_CAND[x]
    if x == 13:
        return R in (1, 3, 5, 7, 9) or (15 <= R <= 25 and R % 2 == 1)
    return R in (1, 3, 5, 7, 9, 15)


def cand_P(x, R):
    if x in (2, 4, 6, 8):
        return False
    if x == 3:
        return R >= 6
    if x == 5:
        return R >= 8
    if x == 7:
        return R >= 10
    if x in (9, 11):
        return R in (11, 13) or R >= 14
    if x == 10:
        return R == 11
    if x == 12:
        return R in (11, 13)
    if x % 2 == 1:
        return R in (11, 13) or (16 <= R <= x + 11 and R % 2 == 0) \
            or R >= x + 13
    return R in (11, 13) or (16 <= R <= x + 12 and R % 2 == 0)


def cand(x, R):
    if R == 0:
        return 0
    if cand_T(x, R):
        return 2
    if cand_P(x, R):
        return 1
    return 0


# ------------------------------------------------------------ anchor (proof)
def opts_anchor(x, R):
    """Option set {A, B, C} of the proof: A child = cand at (x-1, R-1)
    (x-outer induction), B child = z=10 y=1 fiber (K1003) at (x, R-1),
    C child = 1 xor z=9 y=2 fiber (K0988) at (x, R-1).  For x=2 the two
    token-decrement moves collapse to the same child (1,2);10 fiber."""
    s = set()
    if x >= 3:
        s.add(cand(x - 1, R - 1))
        s.add(b_val(x, R - 1))
    else:
        s.add(b_val(2, R - 1))
    s.add(1 ^ c_val(x, R - 1))
    return s


# ------------------------------------------------------- band table (proof)
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
        return [(1, 5, "01", "odd"), (2, 6, "23", "even"), (7, None, "1", None)]
    if x == 5:
        return [(1, 7, "01", "odd"), (2, 6, "23", "even"),
                (8, 8, "03", None), (9, None, "0", None)]
    if x == 6:
        return [(1, 7, "01", "odd"), (2, 8, "23", "even"),
                (9, None, "1", None)]
    if x == 7:
        return [(1, 9, "01", "odd"), (2, 8, "23", "even"),
                (10, 10, "03", None), (11, 11, "0", None),
                (12, 12, "03", None), (13, None, "0", None)]
    if x == 8:
        return [(1, 9, "01", "odd"), (2, 10, "23", "even"),
                (11, 11, "01", None), (12, 12, "1", None),
                (13, None, "1", None)]
    if x == 9:
        return [(1, 9, "01", "odd"), (2, 10, "23", "even"),
                (11, 11, "0", None), (12, 12, "12", None),
                (13, None, "0", None)]
    if x == 10:
        return [(1, 9, "01", "odd"), (2, 10, "23", "even"),
                (11, 11, "0", None), (12, 12, "1", None),
                (13, 13, "01", None), (14, None, "1", None)]
    if x == 11:
        return [(1, 9, "01", "odd"), (2, 10, "23", "even"),
                (11, 11, "0", None), (12, 12, "1", None),
                (13, 13, "0", None), (14, 14, "023", None),
                (15, None, "0", None)]
    if x == 12:
        return [(1, 9, "01", "odd"), (2, 10, "23", "even"),
                (11, 11, "0", None), (12, 12, "1", None),
                (13, 13, "0", None), (14, 24, "123", "even"),
                (15, 23, "1", "odd"), (25, None, "1", None)]
    if x == 13:
        return [(1, 9, "01", "odd"), (2, 10, "23", "even"),
                (11, 11, "0", None), (12, 12, "1", None),
                (13, 13, "0", None), (14, 14, "123", None),
                (15, 25, "01", "odd"), (16, 24, "0", "even"),
                (26, None, "0", None)]
    if x == 14:
        return [(1, 9, "01", "odd"), (2, 10, "23", "even"),
                (11, 11, "0", None), (12, 12, "1", None),
                (13, 13, "0", None), (14, 14, "123", None),
                (15, 15, "01", None), (16, 26, "02", "even"),
                (17, 25, "1", "odd"), (27, None, "1", None)]
    if x % 2 == 0:   # even x >= 16
        return [(1, 9, "01", "odd"), (2, 10, "23", "even"),
                (11, 11, "0", None), (12, 12, "1", None),
                (13, 13, "0", None), (14, 14, "123", None),
                (15, 15, "01", None), (16, 16, "02", None),
                (17, x + 11, "1", "odd"), (18, x + 12, "0", "even"),
                (x + 13, None, "1", None)]
    # odd x >= 15
    return [(1, 9, "01", "odd"), (2, 10, "23", "even"),
            (11, 11, "0", None), (12, 12, "1", None),
            (13, 13, "0", None), (14, 14, "123", None),
            (15, 15, "01", None), (16, 16, "02", None),
            (17, x + 10, "1", "odd"), (18, x + 11, "0", "even"),
            (x + 12, x + 12, "1", None), (x + 13, None, "0", None)]


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


# ------------------------------------------------ iterative DP (2nd impl.)
def moves_iter(X, z):
    """Yield (child_X, child_z, flipped) - an enumeration written from the
    rules independently of H (state-level, no value dedup)."""
    out = []
    seen = set()
    for i, v in enumerate(X):
        if v in seen:
            continue
        seen.add(v)
        if v > 1:
            out.append((tuple(sorted(X[:i] + X[i + 1:] + (v - 1,))), z, False))
        else:
            out.append((tuple(sorted(X[:i] + X[i + 1:])), z + 1, False))
    if z >= 1:
        out.append((X, z - 1, True))
    return out


def iterative_dp_values(x, Rmax):
    """Bottom-up DP over all reachable states from ((2,x);10), filling
    val[(X,z)][R] for R=0..Rmax ascending.  Returns dict state->list."""
    states = set()
    frontier = [(tuple(sorted((2, x))), 10)]
    states.add(frontier[0])
    stack = list(frontier)
    while stack:
        X, z = stack.pop()
        for (cX, cz, _) in moves_iter(X, z):
            st = (cX, cz)
            if st not in states:
                states.add(st)
                stack.append(st)
    val = {st: [0] * (Rmax + 1) for st in states}
    for R in range(1, Rmax + 1):
        for st in states:
            X, z = st
            opts = set()
            for (cX, cz, flipped) in moves_iter(X, z):
                cv = val[(cX, cz)][R - 1]
                opts.add(1 ^ cv if flipped else cv)
            m = 0
            while m in opts:
                m += 1
            val[st][R] = m
    return val


# ------------------------------------------------------------------ checks
def check(name, ok, detail):
    AUDIT["checks"][name] = {"ok": bool(ok), **detail}
    if not ok:
        AUDIT["fail"].append(name)


def V1_V2():
    bad1 = bad2 = n = 0
    ex1 = ex2 = None
    for x in range(2, 61):
        for R in range(1, x + 41):
            n += 1
            c = cand(x, R)
            d = H(R, (2, x), 10)
            a = mex(opts_anchor(x, R))
            if c != d:
                bad1 += 1
                if ex1 is None:
                    ex1 = (x, R, c, d)
            if a != d:
                bad2 += 1
                if ex2 is None:
                    ex2 = (x, R, a, d)
    check("V1_direct_vs_cand", bad1 == 0,
          {"points": n, "bad": bad1, "example": ex1})
    check("V2_direct_vs_anchor_mex", bad2 == 0,
          {"points": n, "bad": bad2, "example": ex2})
    AUDIT["n_points"] += n


def V3():
    bad_cov = bad_sig = bad_mex = bad_val = n = 0
    ex_c = ex_s = ex_m = ex_v = None
    for x in range(2, 2001):
        for R in range(1, x + 27):
            n += 1
            s = band_sig_at(x, R)
            if s is None:
                bad_cov += 1
                if ex_c is None:
                    ex_c = (x, R)
                continue
            sa = sig(opts_anchor(x, R))
            if s != sa:
                bad_sig += 1
                if ex_s is None:
                    ex_s = (x, R, s, sa)
                continue
            if mex(band_sigset(s)) != mex(opts_anchor(x, R)):
                bad_mex += 1
                if ex_m is None:
                    ex_m = (x, R)
            if mex(band_sigset(s)) != cand(x, R):
                bad_val += 1
                if ex_v is None:
                    ex_v = (x, R)
    check("V3_band_table",
          bad_cov == 0 and bad_sig == 0 and bad_mex == 0 and bad_val == 0,
          {"points": n, "bad_coverage": bad_cov, "bad_sig": bad_sig,
           "bad_mex": bad_mex, "bad_val": bad_val, "ex_cov": ex_c,
           "ex_sig": ex_s, "ex_mex": ex_m, "ex_val": ex_v})
    AUDIT["n_points"] += n


def V4():
    bad = n = 0
    ex = None
    for x in range(2, 61):
        for R in range(1, x + 41):
            n += 1
            a = H(R, (1, x), 10)
            c = b_val(x, R)
            if a != c:
                bad += 1
                if ex is None:
                    ex = (x, R, a, c)
    check("V4_k1003_transfer", bad == 0,
          {"points": n, "bad": bad, "example": ex})
    AUDIT["n_points"] += n


def V5():
    bad = n = 0
    ex = None
    for x in range(2, 61):
        for R in range(1, x + 41):
            n += 1
            a = H(R, (2, x), 9)
            c = c_val(x, R)
            if a != c:
                bad += 1
                if ex is None:
                    ex = (x, R, a, c)
    check("V5_k0988_transfer", bad == 0,
          {"points": n, "bad": bad, "example": ex})
    AUDIT["n_points"] += n


def V6():
    bad = n = 0
    ex = None
    for x in range(2, 5001):
        for k in range(0, 4):
            R = x + 13 + k
            n += 1
            c = cand(x, R)
            t = (x + 2) % 2
            if c != t:
                bad += 1
                if ex is None:
                    ex = (x, R, c, t)
    check("V6_tail_parity", bad == 0,
          {"points": n, "bad": bad, "example": ex,
           "tail": "cand(x,R) == (x+2) mod 2 for R >= x+13"})
    AUDIT["n_points"] += n


def V7():
    bad = n = 0
    ex = None
    for x in range(2, 501):
        for R in range(1, 13):
            n += 1
            c = cand(x, R)
            d = H(R, (2, x), 10)
            if c != d:
                bad += 1
                if ex is None:
                    ex = (x, R, c, d)
    check("V7_wide_x_low_R_scan", bad == 0,
          {"points": n, "bad": bad, "example": ex})
    AUDIT["n_points"] += n


def V8():
    random.seed(20261120)
    bad = n = 0
    ex = None
    for _ in range(20000):
        x = random.randint(2, 400)
        R = random.randint(1, 460)
        n += 1
        c = cand(x, R)
        a = mex(opts_anchor(x, R))
        if c != a:
            bad += 1
            if ex is None:
                ex = (x, R, c, a)
    check("V8_scatter_seed20261120", bad == 0,
          {"points": n, "bad": bad, "example": ex})
    AUDIT["n_points"] += n


def V9():
    """Theorem T identities on the closed form and band table.

    (a) Theorem T value bound: even R -> candidate value <= 1,
        odd R -> candidate value <= 2, over the full V3 grid;
    (b) tail value: for R = x+13 the candidate value is (x+2) mod 2
        and the band signature's mex agrees;
    (c) bracket: band-table value at R = x+11 equals cand there."""
    bad = n = 0
    ex = None
    for x in range(2, 2001):
        for R in range(1, x + 27):
            n += 1
            c = cand(x, R)
            hi = 1 if R % 2 == 0 else 2
            if c > hi:
                bad += 1
                if ex is None:
                    ex = ("Tbound", x, R, c)
        R = x + 13
        n += 1
        s = band_sig_at(x, R)
        if s is None or mex(band_sigset(s)) != (x + 2) % 2 \
                or cand(x, R) != (x + 2) % 2:
            bad += 1
            if ex is None:
                ex = ("tail", x, R, s)
        Rb = x + 11
        n += 1
        s2 = band_sig_at(x, Rb)
        if s2 is None or mex(band_sigset(s2)) != cand(x, Rb):
            bad += 1
            if ex is None:
                ex = ("band", x, Rb, s2)
    check("V9_theorem_T_parity", bad == 0,
          {"points": n, "bad": bad, "example": ex})
    AUDIT["n_points"] += n


def V11():
    """Height-only reduction (K0832): for R <= 11 the two-token value
    at z=10 equals the single-token value of the summed height:
    cand(x, R) == v_single(x + 2, 10, R)."""
    bad = n = 0
    ex = None
    for x in range(2, 501):
        for R in range(1, 12):
            n += 1
            c = cand(x, R)
            m = v_single(x + 2, 10, R)
            if c != m:
                bad += 1
                if ex is None:
                    ex = (x, R, c, m)
    check("V11_height_only_reduction", bad == 0,
          {"points": n, "bad": bad, "example": ex,
           "note": "R in [1,11]: cand(x,R) == v_single(x+2, 10, R)"})
    AUDIT["n_points"] += n


def V10():
    bad = n = 0
    ex = None
    for x in range(2, 31):
        Rmax = x + 30
        val = iterative_dp_values(x, Rmax)
        col = val[(tuple(sorted((2, x))), 10)]
        for R in range(1, Rmax + 1):
            n += 1
            c = cand(x, R)
            d = col[R]
            if c != d:
                bad += 1
                if ex is None:
                    ex = (x, R, c, d)
    check("V10_iterative_dp_vs_cand", bad == 0,
          {"points": n, "bad": bad, "example": ex})
    AUDIT["n_points"] += n


def main():
    V1_V2()
    V3()
    V4()
    V5()
    V6()
    V7()
    V8()
    V9()
    V10()
    V11()
    AUDIT["all_ok"] = len(AUDIT["fail"]) == 0
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "audit.json"), "w") as f:
        json.dump(AUDIT, f, sort_keys=True, indent=2)
        f.write("\n")
    print(json.dumps(AUDIT, sort_keys=True, indent=2))
    return 0 if AUDIT["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
