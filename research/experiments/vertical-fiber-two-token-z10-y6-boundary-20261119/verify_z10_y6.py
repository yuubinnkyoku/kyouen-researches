#!/usr/bin/env python3
"""Independent audit for the proved z=10, y=6 two-token residual slice (K1008).

The universal proof is by induction on x using the explicit A/B/C signature
bands, K1007 (z=10, y=5), K0994 (z=9, y=6), K0832 Theorem T / height-only
reduction and the general high-R tail.  The two direct mex engines below are
finite independent audits only.  Mirror of verify_z10_y5.py.

Children of H(R;(x,6);10) for R>=1:
  A = H(R-1;(x-1,6);10)   (x-outer induction; for x=6 both token moves
                            collapse to H(R-1;(6,5);10) = K1007 row x=6)
  B = H(R-1;(x,5);10)     (K1007)
  C = 1 ^ H(R-1;(x,6);9)  (K0994)
"""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path

def mex(values):
    seen = set(values)
    n = 0
    while n in seen:
        n += 1
    return n

def make_engines():
    @lru_cache(None)
    def ordered(R, tokens, z):
        if R == 0:
            return 0
        options = set()
        for i, value in enumerate(tokens):
            if value > 1:
                child = tokens[:i] + (value - 1,) + tokens[i + 1:]
                options.add(ordered(R - 1, child, z))
            else:
                child = tokens[:i] + tokens[i + 1:]
                options.add(ordered(R - 1, child, z + 1))
        if z:
            options.add(1 ^ ordered(R - 1, tokens, z - 1))
        return mex(options)

    @lru_cache(None)
    def canonical(R, tokens, z):
        if R == 0:
            return 0
        options = set()
        seen = set()
        for i, value in enumerate(tokens):
            if value in seen:
                continue
            seen.add(value)
            if value > 1:
                child = tuple(sorted(tokens[:i] + (value - 1,) + tokens[i + 1:],
                                     reverse=True))
                options.add(canonical(R - 1, child, z))
            else:
                child = tuple(sorted(tokens[:i] + tokens[i + 1:], reverse=True))
                options.add(canonical(R - 1, child, z + 1))
        if z:
            options.add(1 ^ canonical(R - 1, tokens, z - 1))
        return mex(options)

    return ordered, canonical

# ------------------------------------------------------- K0832 single token
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

# ------------------------------------------------------- K1007 (z=10, y=5)
def z10_y5_T(x, R):
    if x == 5:
        return R in (1, 3, 5, 7, 9, 11, 13, 15)
    if x == 9:
        return R in (1, 3, 5, 7, 9, 17)
    if x == 13:
        return R in (1, 3, 5, 7, 9, 19)
    if x == 16:
        return R in (1, 3, 5, 7, 9) or (21 <= R <= 31 and R % 2 == 1)
    if x in (6, 7, 8, 10, 11, 12, 14, 15):
        return R in (1, 3, 5, 7, 9)
    return R in (1, 3, 5, 7, 9, 21)

def z10_y5_P(x, R):
    if x == 5:
        return False
    if x == 6:
        return R in (11, 13, 15) or R >= 16
    if x == 7:
        return R in (11, 13, 15)
    if x == 8:
        return R in (11, 13, 15, 17) or R >= 18
    if x == 9:
        return R in (11, 13, 15)
    if x == 10:
        return R in (11, 13, 15, 17) or R >= 18
    if x == 11:
        return R in (11, 13, 15, 17)
    if x == 12:
        return R in (11, 13, 15, 17, 19) or R >= 20
    if x == 13:
        return R in (11, 13, 15, 17)
    if x == 14:
        return R in (11, 13, 15, 17, 19) or R >= 20
    if x == 15:
        return R in (11, 13, 15, 17, 19)
    if x == 16:
        return (R in (11, 13, 15, 17, 19)
                or (22 <= R <= 32 and R % 2 == 0)
                or R >= 33)
    if x % 2 == 0:  # even x >= 18
        return (R in (11, 13, 15, 17, 19)
                or (22 <= R <= x + 16 and R % 2 == 0)
                or R >= x + 17)
    # odd x >= 17
    return R in (11, 13, 15, 17, 19) or (22 <= R <= x + 15 and R % 2 == 0)

def z10_y5(x, R):
    """K1007 closed form: H(R;(x,5);10), x>=5."""
    if R == 0:
        return 0
    if z10_y5_T(x, R):
        return 2
    return 1 if z10_y5_P(x, R) else 0

# ------------------------------------------------------- K0994 (z=9, y=6)
def z9_y6(x, R):
    """K0994 closed form: H(R;(x,6);9), x>=6."""
    if R == 0:
        return 0
    if x == 7:
        t = R in (1, 3, 5, 7, 9, 17)
    elif x == 11:
        t = R in (1, 3, 5, 7, 9, 19)
    elif x == 15:
        t = R in (1, 3, 5, 7, 9, 21)
    elif x == 16:
        t = R in (1, 3, 5, 7, 9) or (21 <= R <= 31 and R % 2 == 1)
    elif x >= 17:
        t = R in (1, 3, 5, 7, 9, 21)
    else:
        t = R in (1, 3, 5, 7, 9)
    if x == 6:
        p = (10 <= R <= 16 and R % 2 == 0)
    elif x == 7:
        p = (10 <= R <= 18 and R % 2 == 0) or R >= 19
    elif x == 8:
        p = (10 <= R <= 16 and R % 2 == 0)
    elif x == 9:
        p = (10 <= R <= 18 and R % 2 == 0) or R >= 19
    elif x == 10:
        p = (10 <= R <= 18 and R % 2 == 0)
    elif x == 11:
        p = (10 <= R <= 18 and R % 2 == 0) or R >= 20
    elif x == 12:
        p = (10 <= R <= 18 and R % 2 == 0)
    elif x == 13:
        p = (10 <= R <= 20 and R % 2 == 0) or R >= 21
    elif x == 14:
        p = (10 <= R <= 20 and R % 2 == 0)
    elif x == 15:
        p = (10 <= R <= 20 and R % 2 == 0) or R >= 22
    elif x == 16:
        p = (10 <= R <= 20 and R % 2 == 0)
    elif x % 2 == 1:  # x>=17 odd
        p = ((10 <= R <= 20 and R % 2 == 0)
             or (23 <= R <= x + 16 and R % 2 == 1)
             or R >= x + 17)
    else:  # x>=18 even
        p = (10 <= R <= 20 and R % 2 == 0) or (23 <= R <= x + 15 and R % 2 == 1)
    return 2 if t else 1 if p else 0

# ---------------------------------------------- candidate K1008 (z=10, y=6)
def candidate_T(x, R):
    if x == 6:
        return R in (1, 3, 5, 7, 9, 17)
    if x == 10:
        return R in (1, 3, 5, 7, 9, 19)
    if x == 14:
        return R in (1, 3, 5, 7, 9, 21)
    if x == 17:
        return R in (1, 3, 5, 7, 9) or (23 <= R <= 33 and R % 2 == 1)
    if x in (7, 8, 9, 11, 12, 13, 15, 16):
        return R in (1, 3, 5, 7, 9)
    return R in (1, 3, 5, 7, 9, 23)

def candidate_P(x, R):
    if x == 6:
        return R in (11, 13, 15)
    if x == 7:
        return R in (11, 13, 15) or R >= 17
    if x == 8:
        return R in (11, 13, 15, 17)
    if x == 9:
        return R in (11, 13, 15, 17) or R >= 19
    if x == 10:
        return R in (11, 13, 15, 17)
    if x == 11:
        return R in (11, 13, 15, 17) or R >= 19
    if x == 12:
        return R in (11, 13, 15, 17, 19)
    if x == 13:
        return R in (11, 13, 15, 17, 19) or R >= 21
    if x == 14:
        return R in (11, 13, 15, 17, 19)
    if x == 15:
        return R in (11, 13, 15, 17, 19) or R >= 21
    if x == 16:
        return R in (11, 13, 15, 17, 19, 21)
    if x == 17:
        return (R in (11, 13, 15, 17, 19, 21)
                or (24 <= R <= 32 and R % 2 == 0)
                or R >= 34)
    if x % 2 == 0:  # even x >= 18
        return (R in (11, 13, 15, 17, 19, 21)
                or (24 <= R <= x + 16 and R % 2 == 0))
    # odd x >= 19
    return (R in (11, 13, 15, 17, 19, 21)
            or (24 <= R <= x + 15 and R % 2 == 0)
            or R >= x + 17)

def candidate(x, R):
    """K1008 closed form: H(R;(x,6);10), x>=6."""
    if R == 0:
        return 0
    if candidate_T(x, R):
        return 2
    return 1 if candidate_P(x, R) else 0

# ------------------------------------------------------ signature bands
def bands_for(x):
    # contiguous runs (lo, hi, signature of the A/B/C child value set);
    # the runs cover [1, x+16] exactly and the tail starts at R = x+17.
    ladder = [(i, i, "01" if i % 2 == 1 else "23") for i in range(1, 11)]
    base = [(i, i, "0" if i % 2 == 1 else "1") for i in range(11, 22)]
    if x == 6:
        return ladder + base[:6] + [(17, 17, "01"), (18, 22, "1")]
    if x == 7:
        return ladder + base[:6] + [(17, 17, "0"), (18, 18, "023"),
                                    (19, 23, "0")]
    if x == 8:
        return ladder + base[:6] + [(17, 17, "0"), (18, 24, "1")]
    if x == 9:
        return ladder + base[:6] + [(17, 17, "0"), (18, 18, "12"),
                                    (19, 25, "0")]
    if x == 10:
        return ladder + base[:6] + [(17, 17, "0"), (18, 18, "1"),
                                    (19, 19, "01"), (20, 26, "1")]
    if x == 11:
        return ladder + base[:6] + [(17, 17, "0"), (18, 18, "1"),
                                    (19, 19, "0"), (20, 20, "023"),
                                    (21, 27, "0")]
    if x == 12:
        return ladder + base[:6] + [(17, 17, "0"), (18, 18, "1"),
                                    (19, 19, "0"), (20, 28, "1")]
    if x == 13:
        return ladder + base[:6] + [(17, 17, "0"), (18, 18, "1"),
                                    (19, 19, "0"), (20, 20, "12"),
                                    (21, 29, "0")]
    if x == 14:
        return ladder + base[:6] + [(17, 17, "0"), (18, 18, "1"),
                                    (19, 19, "0"), (20, 20, "1"),
                                    (21, 21, "01"), (22, 30, "1")]
    if x == 15:
        return ladder + base[:6] + [(17, 17, "0"), (18, 18, "1"),
                                    (19, 19, "0"), (20, 20, "1"),
                                    (21, 21, "0"), (22, 22, "023"),
                                    (23, 31, "0")]
    if x == 16:
        return ladder + base + [(22, 22, "123"), (23, 23, "1"),
                               (24, 24, "123"), (25, 25, "1"),
                               (26, 26, "123"), (27, 27, "1"),
                               (28, 28, "123"), (29, 29, "1"),
                               (30, 30, "123"), (31, 31, "1"),
                               (32, 32, "123")]
    if x == 17:  # sweep row
        return (ladder + base + [(22, 22, "123"), (23, 23, "01"),
                                 (24, 24, "0"), (25, 25, "01"),
                                 (26, 26, "0"), (27, 27, "01"),
                                 (28, 28, "0"), (29, 29, "01"),
                                 (30, 30, "0"), (31, 31, "01"),
                                 (32, 32, "0"), (33, 33, "01")])
    if x == 18:  # transition row (A child crosses the sweep row)
        return (ladder + base + [(22, 22, "123"), (23, 23, "01"),
                                 (24, 24, "02"), (25, 25, "1"),
                                 (26, 26, "02"), (27, 27, "1"),
                                 (28, 28, "02"), (29, 29, "1"),
                                 (30, 30, "02"), (31, 31, "1"),
                                 (32, 32, "02"), (33, 33, "1"),
                                 (34, 34, "02")])
    runs = ladder + base + [(22, 22, "123"), (23, 23, "01"), (24, 24, "02")]
    R = 25
    while R <= x + 16:
        runs.append((R, R, "1" if R % 2 == 1 else "0"))
        R += 1
    return runs

def anchor_signature(x, R):
    r = R - 1
    if x == 6:
        a = b = z10_y5(6, r)
    else:
        a = candidate(x - 1, r)
        b = z10_y5(x, r)
    c = 1 ^ z9_y6(x, r)
    return "".join(str(v) for v in sorted({a, b, c}))

def band_signature(x, R):
    return [(lo, hi, sig) for lo, hi, sig in bands_for(x)
            if lo <= R <= hi]

# -------------------------------------------------------------- audit
def audit_once():
    failures = []
    ordered, canonical = make_engines()
    direct = anchor_direct = 0

    for x in range(6, 61):
        for R in range(0, x + 41):
            expected = candidate(x, R)
            a = ordered(R, (x, 6), 10)
            b = canonical(R, (x, 6), 10)
            direct += 2
            if a != expected or b != expected:
                failures.append(("target", x, R, a, b, expected))
            b_anchor = canonical(R, (x, 5), 10)
            c_anchor = canonical(R, (x, 6), 9)
            anchor_direct += 2
            if b_anchor != z10_y5(x, R):
                failures.append(("B-anchor", x, R, b_anchor, z10_y5(x, R)))
            if c_anchor != z9_y6(x, R):
                failures.append(("C-anchor", x, R, c_anchor, z9_y6(x, R)))

    signature_points = mex_points = odd_bound = even_bound = 0
    for x in range(6, 2001):
        runs = bands_for(x)
        # coverage: runs must tile [1, x+16] exactly
        cursor = 1
        for lo, hi, _sig in runs:
            if lo != cursor:
                failures.append(("coverage-gap", x, lo, cursor))
            cursor = hi + 1
        if cursor != x + 17:
            failures.append(("coverage-end", x, cursor, x + 17))
        lo_hi = {}
        for lo, hi, sig in runs:
            for R in range(lo, hi + 1):
                lo_hi[R] = sig
        for R in range(1, x + 17):
            signature_points += 1
            sig = lo_hi.get(R)
            if sig is None:
                failures.append(("coverage", x, R))
                continue
            expected = tuple(int(c) for c in sig)
            actual = anchor_signature(x, R)
            if actual != sig:
                failures.append(("signature", x, R, sig, actual))
                continue
            value = mex(expected)
            mex_points += 1
            if value != candidate(x, R):
                failures.append(("mex", x, R, value, candidate(x, R)))
            if R % 2:
                odd_bound += 1
                if not set(expected).issubset({0, 1}) or value > 2:
                    failures.append(("odd-parent-bound", x, R, expected, value))
            else:
                even_bound += 1
                if value > 1:
                    failures.append(("even-parent-bound", x, R, value))

    tail_checks = 0
    for x in range(6, 5001):
        for offset in range(4):
            R = x + 17 + offset
            tail_checks += 1
            if candidate(x, R) != (x + 6) % 2:
                failures.append(("tail", x, R, candidate(x, R), (x + 6) % 2))

    tail_signature_checks = 0
    for x in range(6, 2001):
        expected = "1" if x % 2 == 0 else "0"
        for offset in range(4):
            R = x + 17 + offset
            tail_signature_checks += 1
            if anchor_signature(x, R) != expected:
                failures.append(("tail-signature", x, R,
                                 anchor_signature(x, R), expected))

    theorem_checks = 0
    for x in range(6, 2001):
        for R in range(0, x + 25):
            value = candidate(x, R)
            theorem_checks += 1
            if value not in (0, 1, 2):
                failures.append(("range", x, R, value))
            if R % 2 == 0 and value > 1:
                failures.append(("even-parent", x, R, value))
            if value == 2 and R % 2 == 0:
                failures.append(("even-value-two", x, R, value))

    height_checks = 0
    for x in range(6, 501):
        for R in range(1, 12):
            height_checks += 1
            if candidate(x, R) != v_single(x + 6, 10, R):
                failures.append(("height-only", x, R))

    counts = {
        "direct_formula_two_engines": direct,
        "independent_BC_anchor_direct": anchor_direct,
        "signature_coverage_and_identity": signature_points,
        "mex_identity": mex_points,
        "odd_parent_bound": odd_bound,
        "even_parent_bound": even_bound,
        "tail_formula": tail_checks,
        "tail_signature": tail_signature_checks,
        "Theorem_T_formula_grid": theorem_checks,
        "height_only_reduction": height_checks,
    }
    return {
        "all_pass": not failures,
        "classification": (
            "universal proof by induction on x using explicit A/B/C signature "
            "bands, K1007, K0994, K0832 Theorem T / height-only reduction and "
            "the general high-R tail; finite checks are independent audits only"
        ),
        "counts": counts,
        "failures": failures,
        "scope": {
            "direct_x": [6, 60],
            "direct_R": "0 <= R <= x+40",
            "signature_x": [6, 2000],
            "signature_R": "1 <= R <= x+16",
            "tail_x": [6, 5000],
            "tail_R": "x+17 <= R <= x+20",
            "tail_signature_x": [6, 2000],
            "tail_signature_R": "x+17 <= R <= x+20",
            "theorem_x": [6, 2000],
            "theorem_R": "0 <= R <= x+24",
            "height_only_x": [6, 500],
            "height_only_R": "1 <= R <= 11",
        },
        "target": "H(R;(x,6);10), x>=6, R>=0",
        "total_checks": sum(counts.values()),
    }

def run():
    first = audit_once()
    second = audit_once()
    same = (json.dumps(first, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"))
            == json.dumps(second, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":")))
    base = dict(first, repeat_runs=2, repeat_byte_identical=same)
    raw = json.dumps(base, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode()
    result = dict(base, sha256_without_hash_field=hashlib.sha256(raw).hexdigest())
    out = Path(__file__).with_name("output")
    out.mkdir(exist_ok=True)
    (out / "audit.json").write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "all_pass": result["all_pass"],
        "counts": result["counts"],
        "failures": len(result["failures"]),
        "repeat_byte_identical": same,
        "sha256_without_hash_field": result["sha256_without_hash_field"],
        "total_checks": result["total_checks"],
    }, sort_keys=True))
    if not result["all_pass"] or not same:
        raise SystemExit(1)

if __name__ == "__main__":
    run()
