#!/usr/bin/env python3
"""Independent audit for the proved z=9, y=8 two-token residual slice.

The universal proof is by induction on x using explicit A/B/C signature
bands, K0997 (z=9,y=7), K0996 (z=8,y=8), K0832 Theorem T and its high-R tail.
Finite direct recurrences below are audits, not the universal proof.
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


def odd(r, lo, hi):
    return r % 2 == 1 and lo <= r <= hi


def even(r, lo, hi):
    return r % 2 == 0 and lo <= r <= hi


def at_least(r, lo):
    return r >= lo


def z9_y7(x, R):
    """K0997: H(R;(x,7);9), x>=7."""
    if R == 0:
        return 0
    if x == 8:
        t = R in (1, 3, 5, 7, 9, 19)
    elif x == 12:
        t = R in (1, 3, 5, 7, 9, 21)
    elif x == 16:
        t = R in (1, 3, 5, 7, 9, 23)
    elif x == 17:
        t = R in (1, 3, 5, 7, 9) or odd(R, 23, 33)
    elif x >= 18:
        t = R in (1, 3, 5, 7, 9, 23)
    else:
        t = R in (1, 3, 5, 7, 9)

    if x == 7:
        p = even(R, 10, 18)
    elif x in (8, 10):
        p = even(R, 10, 20) or at_least(R, 21)
    elif x == 9:
        p = even(R, 10, 18)
    elif x in (11, 13):
        p = even(R, 10, 20)
    elif x in (12, 14):
        p = even(R, 10, 22) or at_least(R, 23)
    elif x == 15:
        p = even(R, 10, 22)
    elif x == 16:
        p = even(R, 10, 22) or at_least(R, 24)
    elif x == 17:
        p = even(R, 10, 22)
    elif x % 2 == 1:
        p = even(R, 10, 22) or odd(R, 25, x + 16)
    else:
        p = even(R, 10, 22) or odd(R, 25, x + 17) or at_least(R, x + 18)
    return 2 if t else 1 if p else 0


def z8_y8(x, R):
    """K0996: H(R;(x,8);8), x>=8."""
    if R == 0:
        return 0
    if x == 10:
        t = R in (1, 3, 5, 7, 21)
    elif x == 14:
        t = R in (1, 3, 5, 7, 23)
    elif x == 17:
        t = R in (1, 3, 5, 7) or odd(R, 25, 33)
    elif x >= 18:
        t = R in (1, 3, 5, 7, 25)
    else:
        t = R in (1, 3, 5, 7)

    if x == 8:
        p = odd(R, 9, 19)
    elif x in (9, 11):
        p = odd(R, 9, 19) or at_least(R, 21)
    elif x == 10:
        p = odd(R, 9, 19)
    elif x == 12:
        p = odd(R, 9, 21)
    elif x in (13, 15):
        p = odd(R, 9, 21) or at_least(R, 23)
    elif x == 14:
        p = odd(R, 9, 21)
    elif x == 16:
        p = odd(R, 9, 23)
    elif x == 17:
        p = odd(R, 9, 23) or even(R, 26, 32) or at_least(R, 34)
    elif x == 18:
        p = odd(R, 9, 23) or even(R, 26, 34)
    else:
        p = odd(R, 9, 23) or even(R, 26, x + 16) or (x % 2 == 1 and at_least(R, x + 17))
    return 2 if t else 1 if p else 0


def candidate(x, R):
    """Closed form for H(R;(x,8);9), x>=8."""
    if R == 0:
        return 0

    t = R in (1, 3, 5, 7, 9)
    if x == 9:
        t = t or R == 21
    elif x == 13:
        t = t or R == 23
    elif x == 17:
        t = t or R == 25
    elif x == 18:
        t = t or odd(R, 25, 35)
    elif x >= 19:
        t = t or R == 25

    if x == 8:
        p = even(R, 10, 20)
    elif x == 9:
        p = even(R, 10, 22) or at_least(R, 23)
    elif x == 10:
        p = even(R, 10, 20)
    elif x == 11:
        p = even(R, 10, 22) or at_least(R, 23)
    elif x == 12:
        p = even(R, 10, 22)
    elif x == 13:
        p = even(R, 10, 24) or at_least(R, 25)
    elif x == 14:
        p = even(R, 10, 22)
    elif x == 15:
        p = even(R, 10, 24) or at_least(R, 25)
    elif x == 16:
        p = even(R, 10, 24)
    elif x == 17:
        p = even(R, 10, 24) or at_least(R, 26)
    elif x == 18:
        p = even(R, 10, 24)
    else:
        p = (even(R, 10, 24) or odd(R, 27, x + 17)
             or (x % 2 == 1 and at_least(R, x + 18)))
    return 2 if t else 1 if p else 0


# Each tuple is (R parity, lower, upper, set of child Grundy values).
# The listed bands partition 1 <= R <= x+17. The tail begins at x+18.
BANDS = {
    8: [
        (1, 1, 9, "01"), (1, 11, 25, "1"),
        (0, 2, 8, "23"), (0, 10, 10, "02"),
        (0, 12, 18, "0"), (0, 20, 20, "02"), (0, 22, 24, "1"),
    ],
    9: [
        (1, 1, 9, "01"), (1, 11, 19, "1"), (1, 21, 21, "01"), (1, 23, 25, "0"),
        (0, 2, 8, "23"), (0, 10, 10, "02"), (0, 12, 26, "0"),
    ],
    10: [
        (1, 1, 9, "01"), (1, 11, 27, "1"),
        (0, 2, 8, "23"), (0, 10, 10, "02"), (0, 12, 20, "0"),
        (0, 22, 22, "123"), (0, 24, 26, "1"),
    ],
    11: [
        (1, 1, 9, "01"), (1, 11, 21, "1"), (1, 23, 27, "0"),
        (0, 2, 8, "23"), (0, 10, 10, "02"), (0, 12, 28, "0"),
    ],
    12: [
        (1, 1, 9, "01"), (1, 11, 29, "1"),
        (0, 2, 8, "23"), (0, 10, 10, "02"), (0, 12, 20, "0"),
        (0, 22, 22, "02"), (0, 24, 28, "1"),
    ],
    13: [
        (1, 1, 9, "01"), (1, 11, 21, "1"), (1, 23, 23, "01"), (1, 25, 29, "0"),
        (0, 2, 8, "23"), (0, 10, 10, "02"), (0, 12, 30, "0"),
    ],
    14: [
        (1, 1, 9, "01"), (1, 11, 31, "1"),
        (0, 2, 8, "23"), (0, 10, 10, "02"), (0, 12, 22, "0"),
        (0, 24, 24, "123"), (0, 26, 30, "1"),
    ],
    15: [
        (1, 1, 9, "01"), (1, 11, 23, "1"), (1, 25, 31, "0"),
        (0, 2, 8, "23"), (0, 10, 10, "02"), (0, 12, 32, "0"),
    ],
    16: [
        (1, 1, 9, "01"), (1, 11, 33, "1"),
        (0, 2, 8, "23"), (0, 10, 10, "02"), (0, 12, 22, "0"),
        (0, 24, 24, "02"), (0, 26, 32, "1"),
    ],
    17: [
        (1, 1, 9, "01"), (1, 11, 23, "1"), (1, 25, 25, "01"), (1, 27, 33, "0"),
        (0, 2, 8, "23"), (0, 10, 10, "02"), (0, 12, 22, "0"),
        (0, 24, 24, "02"), (0, 26, 34, "023"),
    ],
    18: [
        (1, 1, 9, "01"), (1, 11, 23, "1"), (1, 25, 35, "01"),
        (0, 2, 8, "23"), (0, 10, 10, "02"), (0, 12, 22, "0"),
        (0, 24, 24, "02"), (0, 26, 26, "123"), (0, 28, 34, "1"),
    ],
    19: [
        (1, 1, 9, "01"), (1, 11, 23, "1"), (1, 25, 25, "01"), (1, 27, 35, "0"),
        (0, 2, 8, "23"), (0, 10, 10, "02"), (0, 12, 22, "0"),
        (0, 24, 24, "02"), (0, 26, 26, "123"), (0, 28, 36, "12"),
    ],
}


def bands_for(x):
    if x in BANDS:
        return BANDS[x]
    # Stable signature bands for every x>=20.
    return [
        (1, 1, 9, "01"), (1, 11, 23, "1"), (1, 25, 25, "01"),
        (1, 27, x + 17, "0"),
        (0, 2, 8, "23"), (0, 10, 10, "02"), (0, 12, 22, "0"),
        (0, 24, 24, "02"), (0, 26, 26, "123"), (0, 28, x + 17, "1"),
    ]


def anchor_signature(x, R):
    r = R - 1
    a = z9_y7(x, r) if x == 8 else candidate(x - 1, r)
    b = z9_y7(x, r)
    c = 1 ^ z8_y8(x, r)
    return "".join(str(v) for v in sorted({a, b, c}))


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


def audit_once():
    failures = []
    ordered, canonical = make_engines()
    direct = anchor_direct = 0

    for x in range(8, 61):
        for R in range(x + 41):
            expected = candidate(x, R)
            a = ordered(R, (x, 8), 9)
            b = canonical(R, (x, 8), 9)
            direct += 2
            if a != expected or b != expected:
                failures.append(("target", x, R, a, b, expected))

            b_anchor = canonical(R, (x, 7), 9)
            c_anchor = canonical(R, (x, 8), 8)
            anchor_direct += 2
            if b_anchor != z9_y7(x, R):
                failures.append(("B-anchor", x, R, b_anchor, z9_y7(x, R)))
            if c_anchor != z8_y8(x, R):
                failures.append(("C-anchor", x, R, c_anchor, z8_y8(x, R)))

    signature_points = mex_points = odd_bound = even_bound = 0
    for x in range(8, 2001):
        for R in range(1, x + 18):
            signature_points += 1
            matches = [(p, lo, hi, s) for p, lo, hi, s in bands_for(x)
                       if R % 2 == p and lo <= R <= hi]
            if len(matches) != 1:
                failures.append(("coverage", x, R, len(matches)))
                continue
            actual = anchor_signature(x, R)
            if actual != matches[0][3]:
                failures.append(("signature", x, R, matches[0][3], actual))
                continue
            value = mex(int(ch) for ch in matches[0][3])
            mex_points += 1
            if value != candidate(x, R):
                failures.append(("mex", x, R, value, candidate(x, R)))
            if R % 2:
                odd_bound += 1
                if value > 2:
                    failures.append(("odd-parent-bound", x, R, value))
            else:
                even_bound += 1
                if value > 1:
                    failures.append(("even-parent-bound", x, R, value))

    tail_checks = 0
    for x in range(8, 5001):
        for offset in range(4):
            R = x + 18 + offset
            tail_checks += 1
            if candidate(x, R) != (x + 8) % 2:
                failures.append(("tail", x, R, candidate(x, R), (x + 8) % 2))

    tail_signature_checks = 0
    for x in range(8, 2001):
        expected = str((x + 7) % 2)
        for offset in range(4):
            R = x + 18 + offset
            tail_signature_checks += 1
            actual = anchor_signature(x, R)
            if actual != expected:
                failures.append(("tail-signature", x, R, actual, expected))

    theorem_checks = 0
    for x in range(8, 2001):
        for R in range(x + 29):
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
            "bands, K0997, K0996, K0832 Theorem T and the general high-R tail; "
            "finite checks are independent audits only"
        ),
        "counts": counts,
        "failures": failures,
        "scope": {
            "direct_x": [8, 60],
            "direct_R": "0 <= R <= x+40",
            "signature_x": [8, 2000],
            "signature_R": "1 <= R <= x+17",
            "tail_x": [8, 5000],
            "tail_offsets": [0, 3],
            "tail_signature_x": [8, 2000],
            "theorem_x": [8, 2000],
            "theorem_R": "0 <= R <= x+28",
        },
        "target": "H(R;(x,8);9), x>=8, R>=0",
        "total_checks": sum(counts.values()),
    }


def run():
    first = audit_once()
    second = audit_once()
    same = (
        json.dumps(first, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        == json.dumps(second, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    )
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
