#!/usr/bin/env python3
"""Independent audit for the proved z=8, y=3 two-token residual slice.

The universal proof is by induction on x using the explicit A/B/C signature
bands, K0984 (z=8,y=2), K0979 (z=7,y=3), K0832 Theorem T and its high-R tail.
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


def z8_y2(x, R):
    """K0984: H(R;(x,2);8)."""
    if R == 0:
        return 0
    if x == 2:
        twos = {1, 3}
    elif x in (3, 4):
        twos = {1, 3, 5}
    elif x == 5:
        twos = {1, 3, 5, 7}
    elif x == 6:
        twos = {1, 3, 5, 7, 9}
    elif x == 7:
        twos = {1, 3, 5, 7}
    elif x == 8:
        twos = {1, 3, 5, 7, 11}
    elif x in (9, 10):
        twos = {1, 3, 5, 7}
    elif x == 11:
        twos = {1, 3, 5, 7} | set(range(13, 22, 2))
    else:
        twos = {1, 3, 5, 7, 13}
    if R in twos:
        return 2
    if x in (2, 4, 6):
        one = False
    elif x == 3:
        one = R >= 6
    elif x == 5:
        one = R >= 8
    elif x in (7, 9):
        one = R == 9 or R >= 11
    elif x == 8:
        one = R == 9
    elif x == 10:
        one = R in (9, 11)
    elif x == 11:
        one = (R in (9, 11)
               or (14 <= R <= 20 and R % 2 == 0)
               or R >= 22)
    elif x >= 12 and x % 2 == 0:
        one = (R in (9, 11)
               or (14 <= R <= x + 10 and R % 2 == 0))
    else:
        one = (R in (9, 11)
               or (14 <= R <= x + 9 and R % 2 == 0)
               or R >= x + 11)
    return 1 if one else 0


def z7_y3(x, R):
    """K0979: H(R;(x,3);7)."""
    if R == 0:
        return 0
    if x == 3:
        twos = {1, 3, 5}
    elif x == 4:
        twos = {1, 3, 5, 7, 9}
    elif x in (5, 7, 8, 9):
        twos = {1, 3, 5, 7}
    elif x == 6:
        twos = {1, 3, 5, 7, 11}
    elif x == 10:
        twos = {1, 3, 5, 7, 13}
    elif x == 11:
        twos = {1, 3, 5, 7} | set(range(13, 22, 2))
    else:
        twos = {1, 3, 5, 7, 13}
    if R in twos:
        return 2
    if x == 3:
        one = False
    elif x == 4:
        one = R in (8, 10) or R >= 11
    elif x in (5, 7):
        one = R in (8, 10)
    elif x in (6, 8):
        one = R in (8, 10) or R >= 12
    elif x in (9, 11):
        one = R in (8, 10, 12)
    elif x == 10:
        one = R in (8, 10, 12) or R >= 14
    elif x >= 12 and x % 2 == 0:
        one = (R in (8, 10, 12)
               or (R % 2 == 1 and 15 <= R <= x + 9)
               or R >= x + 11)
    else:
        one = (R in (8, 10, 12)
               or (R % 2 == 1 and 15 <= R <= x + 10))
    return 1 if one else 0


def odd(R, lo, hi):
    return R % 2 == 1 and lo <= R <= hi


def even(R, lo, hi):
    return R % 2 == 0 and lo <= R <= hi


def candidate(x, R):
    """K0986 closed form: H(R;(x,3);8), x>=3."""
    if R == 0:
        return 0
    if x == 3:
        is_two = R in (1, 3, 5)
        is_one = False
    elif x == 4:
        is_two = R in (1, 3, 5, 7)
        is_one = R >= 8
    elif x == 5:
        is_two = R in (1, 3, 5, 7, 9, 11)
        is_one = False
    elif x == 6:
        is_two = R in (1, 3, 5, 7)
        is_one = R == 9 or R >= 11
    elif x == 7:
        is_two = R in (1, 3, 5, 7)
        is_one = R in (9, 11)
    elif x == 8:
        is_two = R in (1, 3, 5, 7)
        is_one = R in (9, 11) or R >= 13
    elif x == 9:
        is_two = R in (1, 3, 5, 7, 13)
        is_one = R in (9, 11)
    elif x == 10:
        is_two = R in (1, 3, 5, 7)
        is_one = R in (9, 11) or R >= 13
    elif x == 11:
        is_two = R in (1, 3, 5, 7)
        is_one = R in (9, 11, 13)
    elif x == 12:
        is_two = (R in (1, 3, 5, 7) or odd(R, 15, 23))
        is_one = (R in (9, 11, 13) or even(R, 16, 22) or R >= 24)
    elif x >= 13 and x % 2 == 1:
        is_two = R in (1, 3, 5, 7, 15)
        is_one = R in (9, 11, 13) or even(R, 16, x + 11)
    else:
        is_two = R in (1, 3, 5, 7, 15)
        is_one = (R in (9, 11, 13)
                  or even(R, 16, x + 10)
                  or R >= x + 12)
    if is_two:
        return 2
    return 1 if is_one else 0


def bands_for(x):
    # (parity, lower, upper, child-value-set signature)
    if x == 3:
        return [(1,1,5,"01"), (1,7,13,"1"),
                (0,2,6,"23"), (0,8,14,"1")]
    if x == 4:
        return [(1,1,7,"01"), (1,9,15,"0"),
                (0,2,6,"23"), (0,8,10,"03"), (0,12,14,"0")]
    if x == 5:
        return [(1,1,11,"01"), (1,13,15,"1"),
                (0,2,8,"23"), (0,10,16,"1")]
    if x == 6:
        return [(1,1,7,"01"), (1,9,17,"0"),
                (0,2,8,"23"), (0,10,10,"12"),
                (0,12,12,"023"), (0,14,16,"0")]
    if x == 7:
        return [(1,1,7,"01"), (1,9,11,"0"), (1,13,17,"1"),
                (0,2,8,"23"), (0,10,18,"1")]
    if x == 8:
        return [(1,1,7,"01"), (1,9,19,"0"),
                (0,2,8,"23"), (0,10,10,"1"), (0,12,12,"12"),
                (0,14,18,"0")]
    if x == 9:
        return [(1,1,7,"01"), (1,9,11,"0"), (1,13,13,"01"),
                (1,15,19,"1"), (0,2,8,"23"), (0,10,20,"1")]
    if x == 10:
        return [(1,1,7,"01"), (1,9,21,"0"),
                (0,2,8,"23"), (0,10,12,"1"), (0,14,14,"023"),
                (0,16,20,"0")]
    if x == 11:
        return [(1,1,7,"01"), (1,9,13,"0"), (1,15,21,"1"),
                (0,2,8,"23"), (0,10,12,"1"), (0,14,22,"123")]
    if x == 12:
        return [(1,1,7,"01"), (1,9,13,"0"), (1,15,23,"01"),
                (0,2,8,"23"), (0,10,12,"1"), (0,14,14,"123"),
                (0,16,22,"0")]
    if x == 13:
        return [(1,1,7,"01"), (1,9,13,"0"), (1,15,15,"01"),
                (1,17,23,"1"), (0,2,8,"23"), (0,10,12,"1"),
                (0,14,14,"123"), (0,16,24,"02")]
    if x % 2 == 0:  # x>=14
        return [(1,1,7,"01"), (1,9,13,"0"), (1,15,15,"01"),
                (1,17,x+11,"1"), (0,2,8,"23"), (0,10,12,"1"),
                (0,14,14,"123"), (0,16,16,"02"), (0,18,x+10,"0")]
    return [(1,1,7,"01"), (1,9,13,"0"), (1,15,15,"01"),
            (1,17,x+10,"1"), (0,2,8,"23"), (0,10,12,"1"),
            (0,14,14,"123"), (0,16,16,"02"), (0,18,x+11,"0")]


def anchor_signature(x, R):
    r = R - 1
    if x == 3:
        a = b = z8_y2(3, r)
    else:
        a = candidate(x - 1, r)
        b = z8_y2(x, r)
    c = 1 ^ z7_y3(x, r)
    return tuple(sorted({a, b, c}))


def band_signature(x, R):
    return [(p, lo, hi, sig) for p, lo, hi, sig in bands_for(x)
            if R % 2 == p and lo <= R <= hi]


def audit_once():
    failures = []
    ordered, canonical = make_engines()
    direct = anchor_direct = 0

    for x in range(3, 61):
        for R in range(0, x + 41):
            expected = candidate(x, R)
            a = ordered(R, (x, 3), 8)
            b = canonical(R, (x, 3), 8)
            direct += 2
            if a != expected or b != expected:
                failures.append(("target", x, R, a, b, expected))
            b_anchor = canonical(R, (x, 2), 8)
            c_anchor = canonical(R, (x, 3), 7)
            anchor_direct += 2
            if b_anchor != z8_y2(x, R):
                failures.append(("B-anchor", x, R, b_anchor, z8_y2(x, R)))
            if c_anchor != z7_y3(x, R):
                failures.append(("C-anchor", x, R, c_anchor, z7_y3(x, R)))

    signature_points = mex_points = odd_bound = even_bound = 0
    for x in range(3, 2001):
        for R in range(1, x + 12):
            signature_points += 1
            matches = band_signature(x, R)
            if len(matches) != 1:
                failures.append(("coverage", x, R, len(matches)))
                continue
            expected = tuple(int(c) for c in matches[0][3])
            actual = anchor_signature(x, R)
            if expected != actual:
                failures.append(("signature", x, R, expected, actual))
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
                    failures.append(("even-parent-bound", x, R, expected, value))

    tail_checks = 0
    for x in range(3, 5001):
        for offset in range(4):
            R = x + 12 + offset
            tail_checks += 1
            if candidate(x, R) != (x + 3) % 2:
                failures.append(("tail", x, R, candidate(x, R), (x + 3) % 2))

    tail_signature_checks = 0
    for x in range(3, 2001):
        expected = (1,) if x % 2 else (0,)
        for offset in range(4):
            R = x + 12 + offset
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
            "bands, K0984, K0979, K0832 Theorem T and the general high-R tail; "
            "finite checks are independent audits only"
        ),
        "counts": counts,
        "failures": failures,
        "scope": {
            "direct_x": [3, 60],
            "direct_R": "0 <= R <= x+40",
            "signature_x": [3, 2000],
            "signature_R": "1 <= R <= x+11",
            "tail_x": [3, 5000],
            "tail_offsets": [0, 3],
            "tail_signature_x": [3, 2000],
            "theorem_x": [3, 2000],
            "theorem_R": "0 <= R <= x+24",
        },
        "target": "H(R;(x,3);8), x>=3, R>=0",
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
