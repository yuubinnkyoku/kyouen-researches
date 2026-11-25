#!/usr/bin/env python3
"""Independent audit for the proved z=10, y=7 two-token residual slice (K1009).

The universal proof is by induction on x using the explicit A/B/C signature
bands, K1008 (z=10, y=6), K0997 (z=9, y=7), K0832 Theorem T / height-only
reduction and the general high-R tail.  The two direct mex engines below are
finite independent audits only.  Mirror of verify_z10_y6.py.

Children of H(R;(x,7);10) for R>=1:
  A = H(R-1;(x-1,7);10)   (x-outer induction; for x=7 both token moves
                            collapse to H(R-1;(7,6);10) = K1008 row x=7)
  B = H(R-1;(x,6);10)     (K1008)
  C = 1 ^ H(R-1;(x,7);9)  (K0997)
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

# ------------------------------------------------------- K1008 (z=10, y=6)
def z10_y6_T(x, R):
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

def z10_y6_P(x, R):
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

def z10_y6(x, R):
    """K1008 closed form: H(R;(x,6);10), x>=6."""
    if R == 0:
        return 0
    if z10_y6_T(x, R):
        return 2
    return 1 if z10_y6_P(x, R) else 0

# ------------------------------------------------------- K0997 (z=9, y=7)
def _odd(r, lo, hi):
    return r % 2 == 1 and lo <= r <= hi

def _even(r, lo, hi):
    return r % 2 == 0 and lo <= r <= hi

def z9_y7(x, R):
    """K0997 closed form: H(R;(x,7);9), x>=7."""
    if R == 0:
        return 0
    if x == 8:
        t = R in (1, 3, 5, 7, 9, 19)
    elif x == 12:
        t = R in (1, 3, 5, 7, 9, 21)
    elif x == 16:
        t = R in (1, 3, 5, 7, 9, 23)
    elif x == 17:
        t = R in (1, 3, 5, 7, 9) or _odd(R, 23, 33)
    elif x >= 18:
        t = R in (1, 3, 5, 7, 9, 23)
    else:
        t = R in (1, 3, 5, 7, 9)
    if x == 7:
        p = _even(R, 10, 18)
    elif x in (8, 10):
        p = _even(R, 10, 20) or R >= 21
    elif x == 9:
        p = _even(R, 10, 18)
    elif x in (11, 13):
        p = _even(R, 10, 20)
    elif x in (12, 14):
        p = _even(R, 10, 22) or R >= 23
    elif x == 15:
        p = _even(R, 10, 22)
    elif x == 16:
        p = _even(R, 10, 22) or R >= 24
    elif x == 17:
        p = _even(R, 10, 22)
    elif x % 2 == 1:  # x>=19 odd
        p = _even(R, 10, 22) or _odd(R, 25, x + 16)
    else:  # x>=18 even
        p = _even(R, 10, 22) or _odd(R, 25, x + 17) or R >= x + 18
    return 2 if t else 1 if p else 0

# ---------------------------------------------- candidate K1009 (z=10, y=7)
def candidate_T(x, R):
    if x == 7:
        return R in (1, 3, 5, 7, 9, 19)
    if x == 11:
        return R in (1, 3, 5, 7, 9, 21)
    if x == 15:
        return R in (1, 3, 5, 7, 9, 23)
    if x == 18:
        return R in (1, 3, 5, 7, 9) or (25 <= R <= 35 and R % 2 == 1)
    if x in (8, 9, 10, 12, 13, 14, 16, 17):
        return R in (1, 3, 5, 7, 9)
    return R in (1, 3, 5, 7, 9, 25)

def candidate_P(x, R):
    if x == 7:
        return R in (11, 13, 15, 17)
    if x == 8:
        return R in (11, 13, 15, 17) or R >= 19
    if x == 9:
        return R in (11, 13, 15, 17, 19)
    if x == 10:
        return R in (11, 13, 15, 17, 19) or R >= 21
    if x == 11:
        return R in (11, 13, 15, 17, 19)
    if x == 12:
        return R in (11, 13, 15, 17, 19) or R >= 21
    if x == 13:
        return R in (11, 13, 15, 17, 19, 21)
    if x == 14:
        return R in (11, 13, 15, 17, 19, 21) or R >= 23
    if x == 15:
        return R in (11, 13, 15, 17, 19, 21)
    if x == 16:
        return R in (11, 13, 15, 17, 19, 21) or R >= 23
    if x == 17:
        return R in (11, 13, 15, 17, 19, 21, 23)
    if x == 18:
        return (R in (11, 13, 15, 17, 19, 21, 23)
                or (26 <= R <= 34 and R % 2 == 0)
                or R >= 36)
    if x % 2 == 1:  # odd x >= 19
        return (R in (11, 13, 15, 17, 19, 21, 23)
                or (26 <= R <= x + 17 and R % 2 == 0))
    # even x >= 20
    return (R in (11, 13, 15, 17, 19, 21, 23)
            or (26 <= R <= x + 16 and R % 2 == 0)
            or R >= x + 18)

def candidate(x, R):
    """K1009 closed form: H(R;(x,7);10), x>=7."""
    if R == 0:
        return 0
    if candidate_T(x, R):
        return 2
    return 1 if candidate_P(x, R) else 0

# ------------------------------------------------------ signature bands
def bands_for(x):
    # contiguous runs (lo, hi, signature of the A/B/C child value set);
    # the runs cover [1, x+17] exactly and the tail starts at R = x+18.
    ladder = [(i, i, "01" if i % 2 == 1 else "23") for i in range(1, 11)]
    base = [(i, i, "0" if i % 2 == 1 else "1") for i in range(11, 24)]
    if x == 7:
        return ladder + base[:8] + [(19, 19, "01"), (20, 24, "1")]
    if x == 8:
        return ladder + base[:9] + [(20, 20, "023"), (21, 25, "0")]
    if x == 9:
        return ladder + base[:9] + [(20, 26, "1")]
    if x == 10:
        return ladder + base[:9] + [(20, 20, "12"), (21, 27, "0")]
    if x == 11:
        return ladder + base[:10] + [(21, 21, "01"), (22, 28, "1")]
    if x == 12:
        return (ladder + base[:10] + [(21, 21, "0"), (22, 22, "023"),
                                      (23, 29, "0")])
    if x == 13:
        return ladder + base[:10] + [(21, 21, "0"), (22, 30, "1")]
    if x == 14:
        return ladder + base[:11] + [(22, 22, "12"), (23, 31, "0")]
    if x == 15:
        return (ladder + base[:11] + [(22, 22, "1"), (23, 23, "01"),
                                      (24, 32, "1")])
    if x == 16:
        return (ladder + base[:12] + [(23, 23, "0"), (24, 24, "023"),
                                      (25, 33, "0")])
    if x == 17:
        return (ladder + base[:13] + [(24, 24, "123"), (25, 25, "1"),
                                      (26, 26, "123"), (27, 27, "1"),
                                      (28, 28, "123"), (29, 29, "1"),
                                      (30, 30, "123"), (31, 31, "1"),
                                      (32, 32, "123"), (33, 33, "1"),
                                      (34, 34, "123")])
    if x == 18:  # sweep row
        return (ladder + base[:13] + [(24, 24, "123"), (25, 25, "01"),
                                      (26, 26, "0"), (27, 27, "01"),
                                      (28, 28, "0"), (29, 29, "01"),
                                      (30, 30, "0"), (31, 31, "01"),
                                      (32, 32, "0"), (33, 33, "01"),
                                      (34, 34, "0"), (35, 35, "01")])
    if x == 19:  # transition row (A child crosses the sweep row)
        runs = (ladder + base[:13] + [(24, 24, "123"), (25, 25, "01"),
                                       (26, 26, "02")])
        R = 27
        while R <= x + 17:
            runs.append((R, R, "1" if R % 2 == 1 else "02"))
            R += 1
        return runs
    runs = (ladder + base + [(24, 24, "123"), (25, 25, "01"),
                              (26, 26, "02")])
    R = 27
    while R <= x + 17:
        runs.append((R, R, "1" if R % 2 == 1 else "0"))
        R += 1
    return runs

def anchor_signature(x, R):
    r = R - 1
    if x == 7:
        a = b = z10_y6(7, r)
    else:
        a = candidate(x - 1, r)
        b = z10_y6(x, r)
    c = 1 ^ z9_y7(x, r)
    return "".join(str(v) for v in sorted({a, b, c}))

def band_signature(x, R):
    return [(lo, hi, sig) for lo, hi, sig in bands_for(x)
            if lo <= R <= hi]

# -------------------------------------------------------------- audit
def audit_once():
    failures = []
    ordered, canonical = make_engines()
    direct = anchor_direct = 0

    for x in range(7, 61):
        for R in range(0, x + 41):
            expected = candidate(x, R)
            a = ordered(R, (x, 7), 10)
            b = canonical(R, (x, 7), 10)
            direct += 2
            if a != expected or b != expected:
                failures.append(("target", x, R, a, b, expected))
            b_anchor = canonical(R, (x, 6), 10)
            c_anchor = canonical(R, (x, 7), 9)
            anchor_direct += 2
            if b_anchor != z10_y6(x, R):
                failures.append(("B-anchor", x, R, b_anchor, z10_y6(x, R)))
            if c_anchor != z9_y7(x, R):
                failures.append(("C-anchor", x, R, c_anchor, z9_y7(x, R)))

    signature_points = mex_points = odd_bound = even_bound = 0
    for x in range(7, 2001):
        runs = bands_for(x)
        # coverage: runs must tile [1, x+17] exactly
        cursor = 1
        for lo, hi, _sig in runs:
            if lo != cursor:
                failures.append(("coverage-gap", x, lo, cursor))
            cursor = hi + 1
        if cursor != x + 18:
            failures.append(("coverage-end", x, cursor, x + 18))
        lo_hi = {}
        for lo, hi, sig in runs:
            for R in range(lo, hi + 1):
                lo_hi[R] = sig
        for R in range(1, x + 18):
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
    for x in range(7, 5001):
        for offset in range(4):
            R = x + 18 + offset
            tail_checks += 1
            if candidate(x, R) != (x + 7) % 2:
                failures.append(("tail", x, R, candidate(x, R), (x + 7) % 2))

    tail_signature_checks = 0
    for x in range(7, 2001):
        expected = "1" if x % 2 == 1 else "0"
        for offset in range(4):
            R = x + 18 + offset
            tail_signature_checks += 1
            if anchor_signature(x, R) != expected:
                failures.append(("tail-signature", x, R,
                                 anchor_signature(x, R), expected))

    theorem_checks = 0
    for x in range(7, 2001):
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
    for x in range(7, 501):
        for R in range(1, 12):
            height_checks += 1
            if candidate(x, R) != v_single(x + 7, 10, R):
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
            "bands, K1008, K0997, K0832 Theorem T / height-only reduction and "
            "the general high-R tail; finite checks are independent audits only"
        ),
        "counts": counts,
        "failures": failures,
        "scope": {
            "direct_x": [7, 60],
            "direct_R": "0 <= R <= x+40",
            "signature_x": [7, 2000],
            "signature_R": "1 <= R <= x+17",
            "tail_x": [7, 5000],
            "tail_R": "x+18 <= R <= x+21",
            "tail_signature_x": [7, 2000],
            "tail_signature_R": "x+18 <= R <= x+21",
            "theorem_x": [7, 2000],
            "theorem_R": "0 <= R <= x+24",
            "height_only_x": [7, 500],
            "height_only_R": "1 <= R <= 11",
        },
        "target": "H(R;(x,7);10), x>=7, R>=0",
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
