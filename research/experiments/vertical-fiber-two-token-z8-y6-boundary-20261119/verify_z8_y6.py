#!/usr/bin/env python3
"""Independent audit for the proved z=8, y=6 two-token residual slice.

The universal proof is by induction on x using the explicit A/B/C signature
bands, K0991 (z=8,y=5), K0982 (z=7,y=6), K0832 Theorem T and its high-R tail.
The two direct mex engines below are finite independent audits only.
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



def odd(r, lo, hi):
    return r % 2 == 1 and lo <= r <= hi

def even(r, lo, hi):
    return r % 2 == 0 and lo <= r <= hi

def at_least(r, lo):
    return r >= lo

def in_I(R, a):
    return R >= a

def in_O(R, a, b):
    return a <= R <= b and R % 2 == 1

def in_E(R, a, b):
    return a <= R <= b and R % 2 == 0

def z8_y5(x, R):
    """Closed form: H(R;(x,5);8), x>=5."""
    if R == 0:
        return 0
    if x == 7:
        t = R in (1, 3, 5, 7, 15)
    elif x == 11:
        t = R in (1, 3, 5, 7, 17)
    elif x == 14:
        t = R in (1, 3, 5, 7) or odd(R, 19, 27)
    elif x >= 15:
        t = R in (1, 3, 5, 7, 19)
    else:
        t = R in (1, 3, 5, 7)
    if x == 5:
        p = odd(R, 9, 13)
    elif x == 6:
        p = odd(R, 9, 13) or at_least(R, 15)
    elif x == 7:
        p = odd(R, 9, 13)
    elif x == 8:
        p = odd(R, 9, 15) or at_least(R, 16)
    elif x == 9:
        p = odd(R, 9, 15)
    elif x == 10:
        p = odd(R, 9, 15) or at_least(R, 17)
    elif x == 11:
        p = odd(R, 9, 15)
    elif x == 12:
        p = odd(R, 9, 15) or at_least(R, 17)
    elif x == 13:
        p = odd(R, 9, 17)
    elif x == 14:
        p = odd(R, 9, 17) or even(R, 20, 28) or at_least(R, 29)
    elif x % 2 == 1:  # x>=15 odd
        p = odd(R, 9, 17) or even(R, 20, x + 13)
    else:  # x>=16 even
        p = odd(R, 9, 17) or even(R, 20, x + 14) or at_least(R, x + 15)
    return 2 if t else 1 if p else 0

def z7_y6(x, R):
    """K0982: H(R;(x,6);7), x>=6."""
    if R == 0:
        return 0
    isT = (
        (x in (6, 7, 8, 10, 11, 12) and R in (1, 3, 5, 7)) or
        (x == 9 and R in (1, 3, 5, 7, 17)) or
        (x == 13 and R in (1, 3, 5, 7, 19)) or
        (x == 14 and (R in (1, 3, 5, 7) or in_O(R, 19, 27))) or
        (x >= 15 and R in (1, 3, 5, 7, 19))
    )
    if isT:
        return 2
    isP = (
        (x == 6 and R in (8, 10, 12, 14)) or
        (x == 7 and (R in (8, 10, 12, 14, 16) or in_I(R, 17))) or
        (x == 8 and R in (8, 10, 12, 14, 16)) or
        (x == 9 and (R in (8, 10, 12, 14, 16, 18) or in_I(R, 19))) or
        (x == 10 and R in (8, 10, 12, 14, 16)) or
        (x == 11 and (R in (8, 10, 12, 14, 16, 18) or in_I(R, 19))) or
        (x == 12 and R in (8, 10, 12, 14, 16, 18)) or
        (x == 13 and (R in (8, 10, 12, 14, 16, 18, 20) or in_I(R, 21))) or
        (x == 14 and R in (8, 10, 12, 14, 16, 18)) or
        (x >= 15 and x % 2 == 1 and (R in (8, 10, 12, 14, 16, 18) or in_O(R, 21, x + 14) or in_I(R, x + 15))) or
        (x >= 16 and x % 2 == 0 and (R in (8, 10, 12, 14, 16, 18) or in_O(R, 21, x + 13)))
    )
    if isP:
        return 1
    return 0

def candidate(x, R):
    """Closed form: H(R;(x,6);8), x>=6."""
    if R == 0:
        return 0
    if x == 8:
        t = R in (1, 3, 5, 7, 17)
    elif x == 12:
        t = R in (1, 3, 5, 7, 19)
    elif x == 15:
        t = R in (1, 3, 5, 7) or odd(R, 21, 29)
    elif x >= 16:
        t = R in (1, 3, 5, 7, 21)
    else:
        t = R in (1, 3, 5, 7)
    if x == 6:
        p = odd(R, 9, 15)
    elif x == 7:
        p = odd(R, 9, 17) or at_least(R, 18)
    elif x == 8:
        p = odd(R, 9, 15)
    elif x == 9:
        p = odd(R, 9, 17) or at_least(R, 18)
    elif x == 10:
        p = odd(R, 9, 17)
    elif x == 11:
        p = odd(R, 9, 17) or at_least(R, 19)
    elif x == 12:
        p = odd(R, 9, 17)
    elif x == 13:
        p = odd(R, 9, 19) or at_least(R, 20)
    elif x == 14:
        p = odd(R, 9, 19)
    elif x == 15:
        p = odd(R, 9, 19) or even(R, 22, 30) or at_least(R, 31)
    elif x % 2 == 1:  # x>=17 odd
        p = odd(R, 9, 19) or even(R, 22, x + 15) or at_least(R, x + 16)
    else:  # x>=16 even
        p = odd(R, 9, 19) or even(R, 22, x + 14)
    return 2 if t else 1 if p else 0


def bands_for(x):
    # (parity, lower, upper, child-value-set signature); each R in 1..x+14
    # belongs to exactly one band, except the tail R >= x+15.
    if x == 6:
        return [(1, 1, 7, "01"), (1, 9, 15, "0"),
                (0, 2, 8, "23"), (0, 10, 20, "1"),
                (1, 17, 19, "1")]
    if x == 7:
        return [(1, 1, 7, "01"), (1, 9, 21, "0"),
                (0, 2, 8, "23"), (0, 10, 14, "1"), (0, 16, 16, "12"),
                (0, 18, 20, "0")]
    if x == 8:
        return [(1, 1, 7, "01"), (1, 9, 15, "0"), (1, 17, 17, "01"),
                (1, 19, 21, "1"),
                (0, 2, 8, "23"), (0, 10, 22, "1")]
    if x == 9:
        return [(1, 1, 7, "01"), (1, 9, 23, "0"),
                (0, 2, 8, "23"), (0, 10, 16, "1"), (0, 18, 18, "023"),
                (0, 20, 22, "0")]
    if x == 10:
        return [(1, 1, 7, "01"), (1, 9, 17, "0"), (1, 19, 23, "1"),
                (0, 2, 8, "23"), (0, 10, 24, "1")]
    if x == 11:
        return [(1, 1, 7, "01"), (1, 9, 25, "0"),
                (0, 2, 8, "23"), (0, 10, 16, "1"), (0, 18, 18, "12"),
                (0, 20, 24, "0")]
    if x == 12:
        return [(1, 1, 7, "01"), (1, 9, 17, "0"), (1, 19, 19, "01"),
                (1, 21, 25, "1"),
                (0, 2, 8, "23"), (0, 10, 26, "1")]
    if x == 13:
        return [(1, 1, 7, "01"), (1, 9, 27, "0"),
                (0, 2, 8, "23"), (0, 10, 18, "1"), (0, 20, 20, "023"),
                (0, 22, 26, "0")]
    if x == 14:
        return [(1, 1, 7, "01"), (1, 9, 19, "0"), (1, 21, 27, "1"),
                (0, 2, 8, "23"), (0, 10, 18, "1"), (0, 20, 28, "123")]
    if x == 15:
        return [(1, 1, 7, "01"), (1, 9, 19, "0"), (1, 21, 29, "01"),
                (0, 2, 8, "23"), (0, 10, 18, "1"), (0, 20, 20, "123"),
                (0, 22, 28, "0")]
    if x == 16:
        return [(1, 1, 7, "01"), (1, 9, 19, "0"), (1, 21, 21, "01"),
                (1, 23, 29, "1"),
                (0, 2, 8, "23"), (0, 10, 18, "1"), (0, 20, 20, "123"),
                (0, 22, 30, "02")]
    if x % 2 == 1:  # x>=17 odd
        return [(1, 1, 7, "01"), (1, 9, 19, "0"), (1, 21, 21, "01"),
                (1, 23, x + 14, "1"),
                (0, 2, 8, "23"), (0, 10, 18, "1"), (0, 20, 20, "123"),
                (0, 22, 22, "02"), (0, 24, x + 13, "0")]
    # x>=18 even
    return [(1, 1, 7, "01"), (1, 9, 19, "0"), (1, 21, 21, "01"),
            (1, 23, x + 13, "1"),
            (0, 2, 8, "23"), (0, 10, 18, "1"), (0, 20, 20, "123"),
            (0, 22, 22, "02"), (0, 24, x + 14, "0")]


def anchor_signature(x, R):
    r = R - 1
    if x == 6:
        a = b = z8_y5(6, r)
    else:
        a = candidate(x - 1, r)
        b = z8_y5(x, r)
    c = 1 ^ z7_y6(x, r)
    return "".join(str(v) for v in sorted({a, b, c}))

def band_signature(x, R):
    return [(p, lo, hi, sig) for p, lo, hi, sig in bands_for(x)
            if R % 2 == p and lo <= R <= hi]

def audit_once():
    failures = []
    ordered, canonical = make_engines()
    direct = anchor_direct = 0

    for x in range(6, 61):
        for R in range(0, x + 41):
            expected = candidate(x, R)
            a = ordered(R, (x, 6), 8)
            b = canonical(R, (x, 6), 8)
            direct += 2
            if a != expected or b != expected:
                failures.append(("target", x, R, a, b, expected))
            b_anchor = canonical(R, (x, 5), 8)
            c_anchor = canonical(R, (x, 6), 7)
            anchor_direct += 2
            if b_anchor != z8_y5(x, R):
                failures.append(("B-anchor", x, R, b_anchor, z8_y5(x, R)))
            if c_anchor != z7_y6(x, R):
                failures.append(("C-anchor", x, R, c_anchor, z7_y6(x, R)))

    signature_points = mex_points = odd_bound = even_bound = 0
    for x in range(6, 2001):
        for R in range(1, x + 15):
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
    for x in range(6, 5001):
        for offset in range(4):
            R = x + 15 + offset
            tail_checks += 1
            if candidate(x, R) != (x + 6) % 2:
                failures.append(("tail", x, R, candidate(x, R), (x + 6) % 2))

    tail_signature_checks = 0
    for x in range(6, 2001):
        expected = "1" if x % 2 == 0 else "0"
        for offset in range(4):
            R = x + 15 + offset
            tail_signature_checks += 1
            if anchor_signature(x, R) != expected:
                failures.append(("tail-signature", x, R,
                                 anchor_signature(x, R), expected))

    theorem_checks = 0
    for x in range(6, 2001):
        for R in range(0, x + 27):
            value = candidate(x, R)
            theorem_checks += 1
            if value not in (0, 1, 2):
                failures.append(("range", x, R, value))
            if R % 2 == 0 and value > 1:
                failures.append(("even-parent", x, R, value))
            if value == 2 and R % 2 == 0:
                failures.append(("even-value-two", x, R, value))

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
    }
    return {
        "all_pass": not failures,
        "classification": (
            "universal proof by induction on x using explicit A/B/C signature "
            "bands, K0991, K0982, K0832 Theorem T and the general high-R tail; "
            "finite checks are independent audits only"
        ),
        "counts": counts,
        "failures": failures,
        "scope": {
            "direct_x": [6, 60],
            "direct_R": "0 <= R <= x+40",
            "signature_x": [6, 2000],
            "signature_R": "1 <= R <= x+14",
            "tail_x": [6, 5000],
            "tail_offsets": [0, 3],
            "tail_signature_x": [6, 2000],
            "theorem_x": [6, 2000],
            "theorem_R": "0 <= R <= x+26",
        },
        "target": "H(R;(x,6);8), x>=6, R>=0",
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
