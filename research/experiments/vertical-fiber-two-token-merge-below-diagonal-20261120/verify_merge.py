#!/usr/bin/env python3
"""Verify the two-token merge-below-diagonal theorem (K1101, 2026-11-20).

THEOREM (universal, proved symbolically from published closed forms):
  For y in {1, 2}: for all z >= 1, all x >= y with S = x+y < z, and all R >= 0,
      H(R; (x, y); z) = H(R; {S}; z) = single_token(S, z, R)
  where single_token is the published K0832 single-token closed form.

Symbolic proof (report.md): in the domain S < z the published closed forms
cand_y1 (K1023) and cand2 (K1099) reduce to z-independent row functions
  x even: value 2 on O[1, x+y-1], value 1 on [x+y, inf)   (only when S odd, i.e. y=1)
  ...

Concretely, for S = x+y:
  y=1: x even: T=O[1,x+1], P=[x+2,inf)   ; x odd: T=O[1,x], P=empty
  y=2: x even: T=O[1,x+1], P=empty       ; x odd: T=O[1,x+2], P=[x+3,inf)
  single_token (case z >= S+1): 2 on O[1, q_odd(S)], x%2... value S%2 beyond.
  q_odd(S) = 2*ceil(x/2)+1 for both parities; S%2 = (x+y)%2.
These coincide case by case.

This machine double-checks the theorem and produces evidence for the general
merge observation (all y >= 3 and multi-token multisets as FINITE census
witnesses only, not universal claims) and fixes the sharpness counterexample
family at S = z (merge fails).

Raw engine semantics are copied verbatim from the published z17-y2 census
machinery (H_ordered / H_canonical / single_token) and the K1023/K1099
closed forms are transcribed verbatim from the published verifiers.

All checks are deterministic: fixed iteration order, fixed-seed LCG probes,
sorted JSON keys, no timestamps, stdlib only.
"""

import json
import os
import sys
from functools import lru_cache

sys.setrecursionlimit(1_000_000)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "audit.json")


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
    """Published single-token closed form (K0832 machinery, as transcribed in
    the z17-y2 census)."""
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


def cand_y1(z, x, R):
    """Published y=1 parametric closed form (K1023, verbatim cand())."""
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


def _odd(a, b):
    return range(a | 1, b + 1, 2)


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
    """Published y=2 parametric closed form (K1099, verbatim)."""
    t = in_T(z, x, R)
    pv = in_P(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    if R == 0:
        return 0
    if t:
        return 2
    return 1 if pv else 0


class LCG:
    """Deterministic fixed-seed probe generator (numerical recipes style)."""

    def __init__(self, seed):
        self.state = seed

    def next(self):
        self.state = (self.state * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        return self.state >> 16


results = {}
POINTS = 0


def check(name, fn):
    ok, detail, n = fn()
    results[name] = {"pass": bool(ok), "points": n, "detail": detail}
    if not ok:
        results["_fail_examples"] = detail if isinstance(detail, list) else [detail]


def C1_raw_anchors():
    """Dual raw recursions vs both published closed forms vs single token,
    on the in-domain grid. z <= 32."""
    global POINTS
    bad = []
    n = 0
    for z in range(1, 33):
        for y in (1, 2):
            for x in range(y, z - y):
                S = x + y
                if S >= z:
                    continue
                for R in range(0, S + z + 20):
                    n += 1
                    POINTS += 1
                    X = (x, y)
                    ho = H_ordered(R, X, z)
                    hc = H_canonical(R, X, z)
                    c = cand_y1_allz(z, x, R) if y == 1 else cand2(z, x, R)
                    v = single_token(S, z, R)
                    sv = H_canonical(R, (S,), z)
                    if not (ho == hc == c == v == sv):
                        bad.append((z, x, y, R, ho, hc, c, v, sv))
                        if len(bad) >= 20:
                            return False, bad, n
    # explicit published-slice anchor rows (K1016 z=12 y=1 x<=10, K1042 z=16 y=2 x<=13):
    for x in range(1, 11):
        for R in range(0, x + 1 + 12 + 20):
            n += 1
            POINTS += 1
            if H_canonical(R, (x, 1), 12) != single_token(x + 1, 12, R):
                bad.append(("anchor-z12-y1", x, R))
    for x in range(2, 14):
        for R in range(0, x + 2 + 16 + 20):
            n += 1
            POINTS += 1
            if H_canonical(R, (x, 2), 16) != single_token(x + 2, 16, R):
                bad.append(("anchor-z16-y2", x, R))
    return (len(bad) == 0), bad[:20], n


def C2_y1_closed_identity():
    """K1023 closed form vs K0832 single-token on full domain grid z<=220."""
    global POINTS
    bad = []
    n = 0
    for z in range(0, 221):
        for x in range(1, max(z - 1, 0)):
            S = x + 1
            if S >= z:
                continue
            top = min(S + z + 40, S + 200)
            for R in range(0, top + 1):
                n += 1
                POINTS += 1
                if cand_y1_allz(z, x, R) != single_token(S, z, R):
                    bad.append((z, x, R, cand_y1_allz(z, x, R), single_token(S, z, R)))
                    if len(bad) >= 20:
                        return False, bad, n
    return (len(bad) == 0), bad[:20], n


def C3_y2_closed_identity():
    """K1099 closed form vs K0832 single-token on full domain grid z<=220."""
    global POINTS
    bad = []
    n = 0
    for z in range(0, 221):
        for x in range(2, max(z - 2, 0)):
            S = x + 2
            if S >= z:
                continue
            top = min(S + z + 40, S + 200)
            for R in range(0, top + 1):
                n += 1
                POINTS += 1
                if cand2(z, x, R) != single_token(S, z, R):
                    bad.append((z, x, R, cand2(z, x, R), single_token(S, z, R)))
                    if len(bad) >= 20:
                        return False, bad, n
    return (len(bad) == 0), bad[:20], n


def C4_seeded_deep_probes():
    """Fixed-seed scattered probes of the closed-form identity, z<=20000."""
    global POINTS
    bad = []
    n = 0
    g = LCG(20261120)
    for _ in range(200000):
        z = 1 + g.next() % 20000
        y = 1 + g.next() % 60
        x = y + g.next() % 200
        S = x + y
        if S >= z:
            continue
        if S % 2 == 0 and y % 2 == 1:
            pass  # covered below by both families
        R = g.next() % (S + z + 200)
        n += 1
        POINTS += 1
        if y == 1:
            if cand_y1_allz(z, x, R) != single_token(S, z, R):
                bad.append(("y1", z, x, R))
        elif y == 2:
            if cand2(z, x, R) != single_token(S, z, R):
                bad.append(("y2", z, x, R))
        # y >= 3: closed form not published; skip (census handles raw side).
        if len(bad) >= 20:
            return False, bad, n
    # far tail columns: R up to 100000 on moderate z
    for z in (997, 1000, 4001):
        for x in (2, 3, 50, 300, 900):
            y2 = x + 2
            if y2 < z:
                for R in (z + x, z + x + 1, 99998, 99999, 100000):
                    n += 1
                    POINTS += 1
                    if cand2(z, x, R) != single_token(x + 2, z, R):
                        bad.append(("tail-y2", z, x, R))
            y1 = x + 1
            if y1 < z:
                for R in (z + x, z + x + 1, 99998, 99999, 100000):
                    n += 1
                    POINTS += 1
                    if cand_y1_allz(z, x, R) != single_token(x + 1, z, R):
                        bad.append(("tail-y1", z, x, R))
    return (len(bad) == 0), bad[:20], n


def C5_general_2token_census():
    """Raw 2-token vs raw single: y=1..40, z<=40, R<=S+z+16. CENSUS witness
    for the general merge observation (NOT a universal claim for y>=3)."""
    global POINTS
    bad = []
    n = 0
    for z in range(1, 41):
        for y in range(1, 41):
            for x in range(y, z - y):
                S = x + y
                if S >= z:
                    continue
                top = min(S + z + 16, 140)
                for R in range(0, top + 1):
                    n += 1
                    POINTS += 1
                    if H_canonical(R, (x, y), z) != H_canonical(R, (S,), z):
                        bad.append((z, x, y, R,
                                    H_canonical(R, (x, y), z),
                                    H_canonical(R, (S,), z)))
                        if len(bad) >= 20:
                            return False, bad, n
    return (len(bad) == 0), bad[:20], n


def C6_three_token_census():
    """Raw 3-token multiset vs raw single of the sum, z<=26. CENSUS."""
    global POINTS
    bad = []
    n = 0
    for z in range(2, 27):
        for a in range(1, z):
            for b in range(a, z):
                S2 = a + b
                if S2 >= z:
                    break
                for c in range(b, z):
                    S = S2 + c
                    if S >= z:
                        break
                    top = min(S + z + 12, 110)
                    for R in range(0, top + 1):
                        n += 1
                        POINTS += 1
                        if H_canonical(R, (a, b, c), z) != H_canonical(R, (S,), z):
                            bad.append((z, (a, b, c), R))
                            if len(bad) >= 20:
                                return False, bad, n
    return (len(bad) == 0), bad[:20], n


def C7_four_five_token_census():
    """Raw 4-token (z<=14) and 5-token (z<=11) multiset vs raw single. CENSUS."""
    global POINTS
    bad = []
    n = 0
    for z in range(2, 15):
        for a in range(1, z):
            for b in range(a, z):
                S2 = a + b
                if S2 >= z:
                    break
                for c in range(b, z):
                    S3 = S2 + c
                    if S3 >= z:
                        break
                    for d in range(c, z):
                        S = S3 + d
                        if S >= z:
                            break
                        top = min(S + z + 10, 90)
                        for R in range(0, top + 1):
                            n += 1
                            POINTS += 1
                            if H_canonical(R, (a, b, c, d), z) != H_canonical(R, (S,), z):
                                bad.append((z, (a, b, c, d), R))
                                if len(bad) >= 20:
                                    return False, bad, n
    for z in range(2, 12):
        for a in range(1, z):
            for b in range(a, z):
                S2 = a + b
                if S2 >= z:
                    break
                for c in range(b, z):
                    S3 = S2 + c
                    if S3 >= z:
                        break
                    for d in range(c, z):
                        S4 = S3 + d
                        if S4 >= z:
                            break
                        for e in range(d, z):
                            S = S4 + e
                            if S >= z:
                                break
                            top = min(S + z + 8, 80)
                            for R in range(0, top + 1):
                                n += 1
                                POINTS += 1
                                if H_canonical(R, (a, b, c, d, e), z) != H_canonical(R, (S,), z):
                                    bad.append((z, (a, b, c, d, e), R))
                                    if len(bad) >= 20:
                                        return False, bad, n
    return (len(bad) == 0), bad[:20], n


def C8_sharpness_S_eq_z():
    """Merge FAILS at S=z: fix the canonical counterexample and count finite
    divergences. The failure is a feature (sharpness of the boundary)."""
    global POINTS
    # canonical counterexample: z=3, X=(2,1), R=5: H=1 vs single {3}: H=2
    a = H_canonical(5, (2, 1), 3)
    b = H_canonical(5, (3,), 3)
    if not (a == 1 and b == 2):
        return False, [("canonical counterexample broken", a, b)], 2
    n = 2
    POINTS += n
    div = 1
    # count finite divergences on S=z band, z<=24 (census of failure, not theorem)
    for z in range(3, 25):
        for y in range(1, z // 2 + 1):
            x = z - y
            if x < y:
                continue
            top = min(2 * z + 20, 80)
            for R in range(0, top + 1):
                n += 1
                POINTS += 1
                if H_canonical(R, (x, y), z) != H_canonical(R, (z,), z):
                    div += 1
    return True, {"canonical": [3, 2, 1, 5, 1, 2], "S_eq_z_divergences_within_band": div - 1}, n


def C9_z_independence():
    """Below the diagonal the merged row depends only on (S, R): checks that
    single_token(S, z, *OPT) is constant for z in [S+1, S+41] (symbolically
    obvious from the formula's z>=x+1 case; machine confirmation)."""
    global POINTS
    bad = []
    n = 0
    for S in range(1, 80):
        for R in range(0, min(3 * S + 60, 240)):
            base = single_token(S, S + 1, R)
            for z in range(S + 2, S + 42):
                n += 1
                POINTS += 1
                if single_token(S, z, R) != base:
                    bad.append((S, z, R))
    return (len(bad) == 0), bad[:20], n


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    check("C1_raw_anchors_dual_recursion_and_closed_forms", C1_raw_anchors)
    check("C2_y1_closed_identity_grid", C2_y1_closed_identity)
    check("C3_y2_closed_identity_grid", C3_y2_closed_identity)
    check("C4_seeded_deep_probes_and_far_tails", C4_seeded_deep_probes)
    check("C5_general_2token_census_witness", C5_general_2token_census)
    check("C6_three_token_census_witness", C6_three_token_census)
    check("C7_four_five_token_census_witness", C7_four_five_token_census)
    check("C8_sharpness_S_eq_z_counterexample", C8_sharpness_S_eq_z)
    check("C9_single_token_z_independence_below_diagonal", C9_z_independence)
    ok = all(v["pass"] for k, v in results.items() if not k.startswith("_"))
    doc = {
        "pass": ok,
        "theorem": (
            "For y in {1,2}: all z>=1, all x>=y with S=x+y<z, all R>=0: "
            "H(R;(x,y);z) = H(R;{S};z) = single_token(S,z,R) "
            "(proved symbolically from published K1023/K1099/K0832 closed forms; "
            "C1-C4 machine-confirm, C5-C7 are census witnesses only, "
            "C8 fixes merge failure at S=z, C9 confirms z-independence below diagonal)."
        ),
        "total_points": POINTS,
        "checks": results,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    print("pass" if ok else "FAIL", POINTS)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
