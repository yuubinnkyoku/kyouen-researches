#!/usr/bin/env python3
"""Independent audit for the proved z=10, y=3 two-token residual slice (K1005).

The universal proof is by induction on x using the explicit A/B/C signature
bands, K1004 (z=10, y=2), K0989 (z=9, y=3), K0832 Theorem T / height-only
reduction and the general high-R tail.  The two direct mex engines below are
finite independent audits only.  Mirror of verify_z9_y2.py / verify_z10_y2.py.

Children of H(R;(x,3);10) for R>=1:
  A = H(R-1;(x-1,3);10)   (x-outer induction; for x=3 both token moves
                            collapse to H(R-1;(2,3);10) = K1004 row x=3)
  B = H(R-1;(x,2);10)     (K1004)
  C = 1 ^ H(R-1;(x,3);9)  (K0989)
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

# ------------------------------------------------------- K1004 (z=10, y=2)
def z10_y2_T(x, R):
    if x == 2:
        return R in (1, 3)
    if x in (3, 4):
        return R in (1, 3, 5)
    if x in (5, 6):
        return R in (1, 3, 5, 7)
    if x == 7:
        return R in (1, 3, 5, 7, 9)
    if x == 8:
        return R in (1, 3, 5, 7, 9, 11)
    if x in (9, 11, 12):
        return R in (1, 3, 5, 7, 9)
    if x == 10:
        return R in (1, 3, 5, 7, 9, 13)
    if x == 13:
        return R in (1, 3, 5, 7, 9) or (15 <= R <= 25 and R % 2 == 1)
    return R in (1, 3, 5, 7, 9, 15)

def z10_y2_P(x, R):
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
    if x % 2 == 0:  # even x >= 14
        return R in (11, 13) or (16 <= R <= x + 12 and R % 2 == 0)
    # odd x >= 13
    return (R in (11, 13)
            or (16 <= R <= x + 11 and R % 2 == 0)
            or R >= x + 13)

def z10_y2(x, R):
    if R == 0:
        return 0
    if z10_y2_T(x, R):
        return 2
    return 1 if z10_y2_P(x, R) else 0

# ------------------------------------------------------- K0989 (z=9, y=3)
def z9_y3(x, R):
    if R == 0:
        return 0
    if x == 3:
        is_two = R in (1, 3, 5)
        is_one = False
    elif x == 4:
        is_two = R in (1, 3, 5, 7)
        is_one = R >= 8
    elif x == 5:
        is_two = R in (1, 3, 5, 7)
        is_one = False
    elif x == 6:
        is_two = R in (1, 3, 5, 7, 9, 11)
        is_one = R in (10, 12) or R >= 13
    elif x == 7:
        is_two = R in (1, 3, 5, 7, 9)
        is_one = R in (10, 12)
    elif x == 8:
        is_two = R in (1, 3, 5, 7, 9, 13)
        is_one = R in (10, 12) or R >= 14
    elif x == 9:
        is_two = R in (1, 3, 5, 7, 9)
        is_one = R in (10, 12)
    elif x == 10:
        is_two = R in (1, 3, 5, 7, 9)
        is_one = R in (10, 12) or R >= 14
    elif x == 11:
        is_two = R in (1, 3, 5, 7, 9)
        is_one = R in (10, 12, 14)
    elif x == 12:
        is_two = R in (1, 3, 5, 7, 9, 15)
        is_one = R in (10, 12, 14) or R >= 16
    elif x == 13:
        is_two = R in (1, 3, 5, 7, 9, 15) or (R % 2 == 1 and 17 <= R <= 25)
        is_one = R in (10, 12, 14)
    elif x % 2 == 0:
        is_two = R in (1, 3, 5, 7, 9, 15)
        is_one = (R in (10, 12, 14)
                  or (R % 2 == 1 and 17 <= R <= x + 13)
                  or R >= x + 14)
    else:
        is_two = R in (1, 3, 5, 7, 9, 15)
        is_one = R in (10, 12, 14) or (R % 2 == 1 and 17 <= R <= x + 12)
    if is_two:
        return 2
    return 1 if is_one else 0

# ---------------------------------------------- candidate K1005 (z=10, y=3)
def candidate_T(x, R):
    if x == 3:
        return R in (1, 3, 5)
    if x in (4, 5):
        return R in (1, 3, 5, 7)
    if x == 6:
        return R in (1, 3, 5, 7, 9)
    if x == 7:
        return R in (1, 3, 5, 7, 9, 11, 13)
    if x == 11:
        return R in (1, 3, 5, 7, 9, 15)
    if x == 14:
        return R in (1, 3, 5, 7, 9) or (17 <= R <= 27 and R % 2 == 1)
    if x in (8, 9, 10, 12, 13):
        return R in (1, 3, 5, 7, 9)
    return R in (1, 3, 5, 7, 9, 17)

def candidate_P(x, R):
    if x in (3, 5, 7):
        return False
    if x == 4:
        return R >= 8
    if x == 6:
        return R >= 10
    if x in (9, 11):
        return R in (11, 13)
    if x == 8:
        return R in (11, 13) or R >= 14
    if x in (10, 12):
        return R in (11, 13) or R >= 15
    if x == 13:
        return R in (11, 13, 15)
    if x % 2 == 0:  # even x >= 14
        return (R in (11, 13, 15)
                or (18 <= R <= x + 12 and R % 2 == 0)
                or R >= x + 14)
    # odd x >= 15
    return R in (11, 13, 15) or (18 <= R <= x + 13 and R % 2 == 0)

def candidate(x, R):
    """K1005 closed form: H(R;(x,3);10), x>=3."""
    if R == 0:
        return 0
    if candidate_T(x, R):
        return 2
    return 1 if candidate_P(x, R) else 0

# ------------------------------------------------------ signature bands
def bands_for(x):
    # (parity, lower, upper, child-value-set signature); each R in 1..x+13
    # belongs to exactly one band, and the tail starts at R = x+14.
    hi = x + 13
    head = [(1, 1, 9, "01"), (0, 2, 10, "23"), (1, 11, 15, "0"),
            (0, 12, 14, "1"), (0, 16, 16, "123")]
    if x == 3:
        return [(1, 1, 5, "01"), (0, 2, 6, "23"),
                (1, 7, hi, "1"), (0, 8, hi, "1")]
    if x == 4:
        return [(1, 1, 7, "01"), (0, 2, 6, "23"), (0, 8, 8, "03"),
                (1, 9, hi, "0"), (0, 10, hi, "0")]
    if x == 5:
        return [(1, 1, 7, "01"), (0, 2, 8, "23"),
                (1, 9, hi, "1"), (0, 10, hi, "1")]
    if x == 6:
        return [(1, 1, 9, "01"), (0, 2, 8, "23"), (0, 10, 12, "03"),
                (1, 11, hi, "0"), (0, 14, hi, "0")]
    if x == 7:
        return [(1, 1, 13, "01"), (0, 2, 10, "23"),
                (0, 12, hi, "1"), (1, 15, hi, "1")]
    if x == 8:
        return [(1, 1, 9, "01"), (0, 2, 10, "23"),
                (1, 11, hi, "0"), (0, 12, 12, "12"), (0, 14, 14, "023"),
                (0, 16, hi, "0")]
    if x == 9:
        return [(1, 1, 9, "01"), (0, 2, 10, "23"),
                (1, 11, 13, "0"), (0, 12, hi, "1"), (1, 15, hi, "1")]
    if x == 10:
        return [(1, 1, 9, "01"), (0, 2, 10, "23"),
                (1, 11, hi, "0"), (0, 12, 12, "1"), (0, 14, 14, "12"),
                (0, 16, hi, "0")]
    if x == 11:
        return [(1, 1, 9, "01"), (0, 2, 10, "23"),
                (1, 11, 13, "0"), (0, 12, hi, "1"), (1, 15, 15, "01"),
                (1, 17, hi, "1")]
    if x == 12:
        return [(1, 1, 9, "01"), (0, 2, 10, "23"),
                (1, 11, hi, "0"), (0, 12, 14, "1"), (0, 16, 16, "023"),
                (0, 18, hi, "0")]
    if x == 13:
        return [(1, 1, 9, "01"), (0, 2, 10, "23"),
                (1, 11, 15, "0"), (0, 12, 14, "1"), (0, 16, hi, "123"),
                (1, 17, hi, "1")]
    if x == 14:  # sweep row
        return head + [(1, 17, 27, "01"), (0, 18, 26, "0")]
    if x == 15:  # transition row (A child crosses the sweep row)
        return head + [(1, 17, 17, "01"), (0, 18, hi, "02"),
                       (1, 19, x + 12, "1")]
    if x % 2 == 0:  # even x >= 16
        return head + [(1, 17, 17, "01"), (0, 18, 18, "02"),
                       (1, 19, x + 13, "1"), (0, 20, x + 12, "0")]
    # odd x >= 17
    return head + [(1, 17, 17, "01"), (0, 18, 18, "02"),
                   (1, 19, x + 12, "1"), (0, 20, x + 13, "0")]

def anchor_signature(x, R):
    r = R - 1
    if x == 3:
        a = b = z10_y2(3, r)
    else:
        a = candidate(x - 1, r)
        b = z10_y2(x, r)
    c = 1 ^ z9_y3(x, r)
    return "".join(str(v) for v in sorted({a, b, c}))

def band_signature(x, R):
    return [(p, lo, hi, sig) for p, lo, hi, sig in bands_for(x)
            if R % 2 == p and lo <= R <= hi]

# -------------------------------------------------------------- audit
def audit_once():
    failures = []
    ordered, canonical = make_engines()
    direct = anchor_direct = 0

    for x in range(3, 61):
        for R in range(0, x + 41):
            expected = candidate(x, R)
            a = ordered(R, (x, 3), 10)
            b = canonical(R, (x, 3), 10)
            direct += 2
            if a != expected or b != expected:
                failures.append(("target", x, R, a, b, expected))
            b_anchor = canonical(R, (x, 2), 10)
            c_anchor = canonical(R, (x, 3), 9)
            anchor_direct += 2
            if b_anchor != z10_y2(x, R):
                failures.append(("B-anchor", x, R, b_anchor, z10_y2(x, R)))
            if c_anchor != z9_y3(x, R):
                failures.append(("C-anchor", x, R, c_anchor, z9_y3(x, R)))

    signature_points = mex_points = odd_bound = even_bound = 0
    for x in range(3, 2001):
        for R in range(1, x + 14):
            signature_points += 1
            matches = band_signature(x, R)
            if len(matches) != 1:
                failures.append(("coverage", x, R, len(matches)))
                continue
            expected = tuple(int(c) for c in matches[0][3])
            actual = anchor_signature(x, R)
            if "".join(str(v) for v in sorted(actual)) != matches[0][3]:
                failures.append(("signature", x, R, matches[0][3], actual))
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
    for x in range(3, 5001):
        for offset in range(4):
            R = x + 14 + offset
            tail_checks += 1
            if candidate(x, R) != (x + 3) % 2:
                failures.append(("tail", x, R, candidate(x, R), (x + 3) % 2))

    tail_signature_checks = 0
    for x in range(3, 2001):
        expected = "0" if x % 2 == 0 else "1"
        for offset in range(4):
            R = x + 14 + offset
            tail_signature_checks += 1
            if anchor_signature(x, R) != expected:
                failures.append(("tail-signature", x, R,
                                 anchor_signature(x, R), expected))

    theorem_checks = 0
    for x in range(3, 2001):
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
    for x in range(3, 501):
        for R in range(1, 12):
            height_checks += 1
            if candidate(x, R) != v_single(x + 3, 10, R):
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
            "bands, K1004, K0989, K0832 Theorem T / height-only reduction and "
            "the general high-R tail; finite checks are independent audits only"
        ),
        "counts": counts,
        "failures": failures,
        "scope": {
            "direct_x": [3, 60],
            "direct_R": "0 <= R <= x+40",
            "signature_x": [3, 2000],
            "signature_R": "1 <= R <= x+13",
            "tail_x": [3, 5000],
            "tail_offsets": [0, 3],
            "tail_R": "x+14 <= R <= x+17",
            "tail_signature_x": [3, 2000],
            "theorem_x": [3, 2000],
            "theorem_R": "0 <= R <= x+24",
            "height_only_x": [3, 500],
            "height_only_R": "1 <= R <= 11",
        },
        "target": "H(R;(x,3);10), x>=3, R>=0",
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
