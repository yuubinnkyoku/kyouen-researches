#!/usr/bin/env python3
"""Independent audit for the proved z=10, y=8 two-token residual slice.

The universal proof is by x-induction using explicit A/B/C signature bands,
K1009 (z=10,y=7), K0998 (z=9,y=8), K0832 Theorem T, height-only reduction,
and the general high-R tail. Finite checks are audits, not the proof itself.
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


def z10_y7(x, R):
    """K1009: H(R;(x,7);10), x>=7."""
    if R == 0:
        return 0
    if x == 7:
        t = R in (1, 3, 5, 7, 9, 19)
    elif x == 11:
        t = R in (1, 3, 5, 7, 9, 21)
    elif x == 15:
        t = R in (1, 3, 5, 7, 9, 23)
    elif x == 18:
        t = R in (1, 3, 5, 7, 9) or odd(R, 25, 35)
    elif x in (8, 9, 10, 12, 13, 14, 16, 17):
        t = R in (1, 3, 5, 7, 9)
    else:
        t = R in (1, 3, 5, 7, 9, 25)

    if x == 7:
        p = R in (11, 13, 15, 17)
    elif x == 8:
        p = R in (11, 13, 15, 17) or at_least(R, 19)
    elif x == 9:
        p = R in (11, 13, 15, 17, 19)
    elif x == 10:
        p = R in (11, 13, 15, 17, 19) or at_least(R, 21)
    elif x == 11:
        p = R in (11, 13, 15, 17, 19)
    elif x == 12:
        p = R in (11, 13, 15, 17, 19) or at_least(R, 21)
    elif x == 13:
        p = R in (11, 13, 15, 17, 19, 21)
    elif x == 14:
        p = R in (11, 13, 15, 17, 19, 21) or at_least(R, 23)
    elif x == 15:
        p = R in (11, 13, 15, 17, 19, 21)
    elif x == 16:
        p = R in (11, 13, 15, 17, 19, 21) or at_least(R, 23)
    elif x == 17:
        p = R in (11, 13, 15, 17, 19, 21, 23)
    elif x == 18:
        p = (R in (11, 13, 15, 17, 19, 21, 23)
             or even(R, 26, 34) or at_least(R, 36))
    elif x % 2 == 1:
        p = R in (11, 13, 15, 17, 19, 21, 23) or even(R, 26, x + 17)
    else:
        p = (R in (11, 13, 15, 17, 19, 21, 23)
             or even(R, 26, x + 16) or at_least(R, x + 18))
    return 2 if t else 1 if p else 0


def z9_y8(x, R):
    """K0998: H(R;(x,8);9), x>=8."""
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


def k1002_candidate(x, R):
    """General z=10,y>=6 candidate specialized to y=8."""
    if R == 0:
        return 0
    d = x - 8
    S = x + 8
    if R >= S + 11:
        return S % 2
    t = R in (1, 3, 5, 7, 9)
    if d in (0, 4, 8):
        t = t or R == 21 + d // 2
    elif d == 11:
        t = t or odd(R, 27, S + 10)
    elif d >= 12:
        t = t or R == 27

    if d % 2 == 0 and d <= 10:
        p = odd(R, 11, 19 + 2 * ((d + 3) // 4))
    elif d % 2 == 0 and d >= 12:
        p = odd(R, 11, 25) or even(R, 28, S + 10)
    elif d % 2 == 1 and d <= 9:
        p = (odd(R, 11, S + 10)
             or even(R, 22 + 2 * ((d + 1) // 4), S + 9))
    elif d % 2 == 1 and d >= 11:
        p = odd(R, 11, 25) or even(R, 28, S + 9)
    else:
        p = False
    return 2 if t else 1 if p else 0


def theorem_piecewise(x, R):
    """Theorem read directly from the x=8..20 rows and x>=21 stable row."""
    if R == 0:
        return 0
    S = x + 8
    if R >= S + 11:
        return S % 2
    t = R in (1, 3, 5, 7, 9)
    if x == 8:
        t = t or R == 21
    elif x == 12:
        t = t or R == 23
    elif x == 16:
        t = t or R == 25
    elif x == 19:
        t = t or odd(R, 27, 37)
    elif x >= 20:
        t = t or R == 27

    if x == 8:
        p = odd(R, 11, 19)
    elif x == 9:
        p = odd(R, 11, 27) or even(R, 22, 26)
    elif x == 10:
        p = odd(R, 11, 21)
    elif x == 11:
        p = odd(R, 11, 29) or even(R, 24, 28)
    elif x == 12:
        p = odd(R, 11, 21)
    elif x == 13:
        p = odd(R, 11, 31) or even(R, 24, 30)
    elif x == 14:
        p = odd(R, 11, 23)
    elif x == 15:
        p = odd(R, 11, 33) or even(R, 26, 32)
    elif x == 16:
        p = odd(R, 11, 23)
    elif x == 17:
        p = odd(R, 11, 35) or even(R, 26, 34)
    elif x == 18:
        p = odd(R, 11, 25)
    elif x == 19:
        p = odd(R, 11, 25) or even(R, 28, 36)
    elif x == 20:
        p = odd(R, 11, 25) or even(R, 28, 38)
    elif x % 2 == 0:
        p = odd(R, 11, 25) or even(R, 28, S + 10)
    else:
        p = odd(R, 11, 25) or even(R, 28, S + 9)
    return 2 if t else 1 if p else 0


# (parity, lower, upper, child-value signature), parity 1=odd, 0=even.
# The finite transition rows are x=8,...,20; x>=21 is the stable row.
BANDS = {
    8: [(1, 1, 9, "01"), (0, 2, 10, "23"),
        (1, 11, 19, "0"), (0, 12, 26, "1"),
        (1, 21, 21, "01"), (1, 23, 25, "1")],
    9: [(1, 1, 9, "01"), (0, 2, 10, "23"),
        (1, 11, 27, "0"), (0, 12, 20, "1"),
        (0, 22, 22, "023"), (0, 24, 26, "0")],
    10: [(1, 1, 9, "01"), (0, 2, 10, "23"),
         (1, 11, 21, "0"), (0, 12, 28, "1"),
         (1, 23, 27, "1")],
    11: [(1, 1, 9, "01"), (0, 2, 10, "23"),
         (1, 11, 29, "0"), (0, 12, 20, "1"),
         (0, 22, 22, "12"), (0, 24, 28, "0")],
    12: [(1, 1, 9, "01"), (0, 2, 10, "23"),
         (1, 11, 21, "0"), (0, 12, 30, "1"),
         (1, 23, 23, "01"), (1, 25, 29, "1")],
    13: [(1, 1, 9, "01"), (0, 2, 10, "23"),
         (1, 11, 31, "0"), (0, 12, 22, "1"),
         (0, 24, 24, "023"), (0, 26, 30, "0")],
    14: [(1, 1, 9, "01"), (0, 2, 10, "23"),
         (1, 11, 23, "0"), (0, 12, 32, "1"),
         (1, 25, 31, "1")],
    15: [(1, 1, 9, "01"), (0, 2, 10, "23"),
         (1, 11, 33, "0"), (0, 12, 22, "1"),
         (0, 24, 24, "12"), (0, 26, 32, "0")],
    16: [(1, 1, 9, "01"), (0, 2, 10, "23"),
         (1, 11, 23, "0"), (0, 12, 34, "1"),
         (1, 25, 25, "01"), (1, 27, 33, "1")],
    17: [(1, 1, 9, "01"), (0, 2, 10, "23"),
         (1, 11, 35, "0"), (0, 12, 24, "1"),
         (0, 26, 26, "023"), (0, 28, 34, "0")],
    18: [(1, 1, 9, "01"), (0, 2, 10, "23"),
         (1, 11, 25, "0"), (0, 12, 24, "1"),
         (0, 26, 36, "123"), (1, 27, 35, "1")],
    19: [(1, 1, 9, "01"), (0, 2, 10, "23"),
         (1, 11, 25, "0"), (0, 12, 24, "1"),
         (0, 26, 26, "123"), (1, 27, 37, "01"),
         (0, 28, 36, "0")],
    20: [(1, 1, 9, "01"), (0, 2, 10, "23"),
         (1, 11, 25, "0"), (0, 12, 24, "1"),
         (0, 26, 26, "123"), (1, 27, 27, "01"),
         (0, 28, 38, "02"), (1, 29, 37, "1")],
}


def bands_for(x):
    if x in BANDS:
        return BANDS[x]
    return [
        (1, 1, 9, "01"), (0, 2, 10, "23"),
        (1, 11, 25, "0"), (0, 12, 24, "1"),
        (0, 26, 26, "123"), (1, 27, 27, "01"),
        (0, 28, 28, "02"), (1, 29, x + 18, "1"),
        (0, 30, x + 18, "0"),
    ]


def band_signature(x, R):
    matches = [s for p, lo, hi, s in bands_for(x)
               if R % 2 == p and lo <= R <= hi]
    return matches[0] if len(matches) == 1 else None


def anchor_signature(x, R):
    r = R - 1
    if x == 8:
        a = b = z10_y7(8, r)
    else:
        a = theorem_piecewise(x - 1, r)
        b = z10_y7(x, r)
    c = 1 ^ z9_y8(x, r)
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
        for R in range(0, x + 41):
            expected = theorem_piecewise(x, R)
            a = ordered(R, (x, 8), 10)
            b = canonical(R, (x, 8), 10)
            direct += 2
            if a != expected or b != expected:
                failures.append(("target", x, R, a, b, expected))
            b_anchor = canonical(R, (x, 7), 10)
            c_anchor = canonical(R, (x, 8), 9)
            anchor_direct += 2
            if b_anchor != z10_y7(x, R):
                failures.append(("B-anchor", x, R, b_anchor, z10_y7(x, R)))
            if c_anchor != z9_y8(x, R):
                failures.append(("C-anchor", x, R, c_anchor, z9_y8(x, R)))

    signature_points = mex_points = odd_bound = even_bound = 0
    for x in range(8, 2001):
        bands = bands_for(x)
        for parity in (0, 1):
            covered = set()
            for p, lo, hi, _signature in bands:
                if p == parity:
                    for R in range(lo, hi + 1, 2):
                        if R % 2 == parity:
                            if R in covered:
                                failures.append(("overlap", x, R))
                            covered.add(R)
            expected = {R for R in range(1, x + 19) if R % 2 == parity}
            if covered != expected:
                failures.append(("coverage", x, parity,
                                 sorted(expected - covered)[:5],
                                 sorted(covered - expected)[:5]))

        for R in range(1, x + 19):
            signature_points += 1
            expected_signature = band_signature(x, R)
            actual_signature = anchor_signature(x, R)
            if expected_signature is None:
                failures.append(("coverage-point", x, R))
                continue
            if actual_signature != expected_signature:
                failures.append(("signature", x, R,
                                 expected_signature, actual_signature))
                continue
            value = mex(int(ch) for ch in expected_signature)
            mex_points += 1
            if value != theorem_piecewise(x, R):
                failures.append(("mex", x, R, expected_signature,
                                 value, theorem_piecewise(x, R)))
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
            R = x + 19 + offset
            tail_checks += 1
            if theorem_piecewise(x, R) != (x + 8) % 2:
                failures.append(("tail", x, R, theorem_piecewise(x, R),
                                 (x + 8) % 2))

    tail_signature_checks = 0
    for x in range(8, 2001):
        expected = "1" if x % 2 == 0 else "0"
        for offset in range(4):
            R = x + 19 + offset
            tail_signature_checks += 1
            actual = anchor_signature(x, R)
            if actual != expected:
                failures.append(("tail-signature", x, R, actual, expected))

    theorem_checks = 0
    for x in range(8, 2001):
        for R in range(0, x + 25):
            value = theorem_piecewise(x, R)
            theorem_checks += 1
            if value not in (0, 1, 2):
                failures.append(("range", x, R, value))
            if R % 2 == 0 and value > 1:
                failures.append(("even-parent", x, R, value))
            if value == 2 and R % 2 == 0:
                failures.append(("even-parent-value-two", x, R, value))

    height_checks = 0
    for x in range(8, 501):
        S = x + 8
        for R in range(1, 12):
            if R <= 9:
                value = 2 if R % 2 else 0
            elif R < S + 10:
                value = (R + 10) % 2
            else:
                value = S % 2
            height_checks += 1
            if theorem_piecewise(x, R) != value:
                failures.append(("height-only", x, R,
                                 theorem_piecewise(x, R), value))

    agreement_checks = 0
    for x in range(8, 2001):
        for R in range(0, x + 25):
            agreement_checks += 1
            a = k1002_candidate(x, R)
            b = theorem_piecewise(x, R)
            if a != b:
                failures.append(("K1002-agreement", x, R, a, b))

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
        "K1002_agreement_grid": agreement_checks,
    }
    return {
        "all_pass": not failures,
        "classification": (
            "universal proof by x-induction using explicit A/B/C signature "
            "bands, K1009, K0998, K0832 Theorem T, height-only reduction and "
            "the general high-R tail; finite checks are independent audits only"
        ),
        "counts": counts,
        "failures": failures,
        "scope": {
            "direct_x": [8, 60],
            "direct_R": "0 <= R <= x+40",
            "signature_x": [8, 2000],
            "signature_R": "1 <= R <= x+18",
            "tail_x": [8, 5000],
            "tail_R": "x+19 <= R <= x+22",
            "tail_signature_x": [8, 2000],
            "tail_signature_R": "x+19 <= R <= x+22",
            "theorem_x": [8, 2000],
            "theorem_R": "0 <= R <= x+24",
            "height_only_x": [8, 500],
            "height_only_R": "1 <= R <= 11",
            "K1002_agreement_x": [8, 2000],
            "K1002_agreement_R": "0 <= R <= x+24",
        },
        "target": "H(R;(x,8);10), x>=8, R>=0",
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
    }, ensure_ascii=False, sort_keys=True))
    if not result["all_pass"] or not same:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
