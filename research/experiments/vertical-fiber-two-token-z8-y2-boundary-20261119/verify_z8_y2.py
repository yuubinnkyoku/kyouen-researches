#!/usr/bin/env python3
"""Independent audit for the proved z=8, y=2 two-token residual-game slice.

The proof uses outer induction on x.  The audit separately checks the
closed form by two direct mex engines and checks every A/B/C signature band
on a large finite rectangle.  Finite checks are not the source of the
universal quantifiers; the signature table and K0832 tail theorem are.
"""
from __future__ import annotations

import hashlib
import json
import random
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
        for i, value in enumerate(tokens):
            if i and tokens[i - 1] == value:
                continue
            if value > 1:
                child = tuple(sorted(tokens[:i] + (value - 1,) + tokens[i + 1:]))
                options.add(canonical(R - 1, child, z))
            else:
                child = tuple(sorted(tokens[:i] + tokens[i + 1:]))
                options.add(canonical(R - 1, child, z + 1))
        if z:
            options.add(1 ^ canonical(R - 1, tokens, z - 1))
        return mex(options)

    return ordered, canonical


def z8_y1(x, R):
    """K0983: H(R;(x,1);8)."""
    if R == 0:
        return 0
    if x == 1:
        twos = {1}
    elif x in (2, 3):
        twos = {1, 3}
    elif x in (4, 5):
        twos = {1, 3, 5}
    elif x == 6:
        twos = {1, 3, 5, 7}
    elif x == 7:
        twos = {1, 3, 5, 7, 9}
    elif x in (8, 9):
        twos = {1, 3, 5, 7}
    elif x == 10:
        twos = {1, 3, 5, 7} | set(range(11, 20, 2))
    else:
        twos = {1, 3, 5, 7, 11}
    if R in twos:
        return 2
    if x in (1, 3, 5, 7):
        one = False
    elif x == 2:
        one = R >= 4
    elif x == 4:
        one = R >= 6
    elif x == 6:
        one = R >= 8
    elif x == 8:
        one = R >= 9
    elif x == 9:
        one = R == 9
    elif x == 10:
        one = R == 9 or (12 <= R <= 18 and R % 2 == 0) or R >= 20
    elif x % 2:
        one = R == 9 or (12 <= R <= x + 9 and R % 2 == 0)
    else:
        one = R == 9 or (12 <= R <= x + 8 and R % 2 == 0) or R >= x + 10
    return 1 if one else 0


def z7_y2(x, R):
    """K0978: H(R;(x,2);7)."""
    if R == 0:
        return 0
    if x == 2:
        twos = {1, 3}
    elif x in (3, 4):
        twos = {1, 3, 5}
    elif x == 5:
        twos = {1, 3, 5, 7, 9}
    elif x in (6, 7, 8):
        twos = {1, 3, 5, 7}
    elif x == 9:
        twos = {1, 3, 5, 7, 11}
    elif x == 10:
        twos = {1, 3, 5, 7, 11} | set(range(13, 20, 2))
    else:
        twos = {1, 3, 5, 7, 11}
    if R in twos:
        return 2
    if x in (2, 4):
        one = False
    elif x == 3:
        one = R >= 6
    elif x in (5, 7):
        one = R == 8 or R >= 10
    elif x == 6:
        one = R == 8
    elif x in (8, 10):
        one = R in (8, 10)
    elif x == 9:
        one = R in (8, 10) or R >= 12
    elif x >= 11 and x % 2:
        one = (R in (8, 10)
               or (13 <= R <= x + 9 and R % 2 == 1)
               or R >= x + 10)
    else:
        one = R in (8, 10) or (13 <= R <= x + 9 and R % 2 == 1)
    return 1 if one else 0


def value2_positions(x):
    if x == 2:
        return {1, 3}
    if x in (3, 4):
        return {1, 3, 5}
    if x == 5:
        return {1, 3, 5, 7}
    if x == 6:
        return {1, 3, 5, 7, 9}
    if x == 7:
        return {1, 3, 5, 7}
    if x == 8:
        return {1, 3, 5, 7, 11}
    if x in (9, 10):
        return {1, 3, 5, 7}
    if x == 11:
        return {1, 3, 5, 7} | set(range(13, 22, 2))
    return {1, 3, 5, 7, 13}


def value1_at(x, R):
    if x in (2, 4, 6):
        return False
    if x == 3:
        return R >= 6
    if x == 5:
        return R >= 8
    if x in (7, 9):
        return R == 9 or R >= 11
    if x == 8:
        return R == 9
    if x == 10:
        return R in (9, 11)
    if x == 11:
        return (R in (9, 11)
                or (14 <= R <= 20 and R % 2 == 0)
                or R >= 22)
    if x >= 12 and x % 2 == 0:
        return (R in (9, 11)
                or (14 <= R <= x + 10 and R % 2 == 0))
    return (R in (9, 11)
            or (14 <= R <= x + 9 and R % 2 == 0)
            or R >= x + 11)


def candidate(x, R):
    if R == 0:
        return 0
    if R in value2_positions(x):
        return 2
    return 1 if value1_at(x, R) else 0


def anchor_signature(x, R):
    r = R - 1
    if x == 2:
        a = b = z8_y1(2, r)
    else:
        a = candidate(x - 1, r)
        b = z8_y1(x, r)
    c = 1 ^ z7_y2(x, r)
    return tuple(sorted({a, b, c}))


def band_signature(x, R):
    """The explicit A/B/C signature table in the proof report."""
    if x == 2:
        if R == 1: return (0, 1)
        if R == 2: return (2, 3)
        if R == 3: return (0, 1)
        if R == 4: return (2, 3)
        return (1,)
    if x == 3:
        if R in (1, 3, 5): return (0, 1)
        if R in (2, 4): return (2, 3)
        if R == 6: return (0, 3)
        return (0,)
    if x == 4:
        if R in (1, 3, 5): return (0, 1)
        if R in (2, 4, 6): return (2, 3)
        return (1,)
    if x == 5:
        if R in (1, 3, 5, 7): return (0, 1)
        if R in (2, 4, 6): return (2, 3)
        if R in (8, 10): return (0, 3)
        return (0,)
    if x == 6:
        if 1 <= R <= 9: return (0, 1) if R % 2 else (2, 3)
        return (1,)
    if x == 7:
        if 1 <= R <= 8: return (0, 1) if R % 2 else (2, 3)
        if R == 9: return (0,)
        if R == 10: return (1, 2)
        return (0,)
    if x == 8:
        if 1 <= R <= 8: return (0, 1) if R % 2 else (2, 3)
        if R == 9: return (0,)
        if R == 10: return (1,)
        if R == 11: return (0, 1)
        return (1,)
    if x == 9:
        if 1 <= R <= 8: return (0, 1) if R % 2 else (2, 3)
        if R == 9: return (0,)
        if R == 10: return (1,)
        if R == 11: return (0,)
        if R == 12: return (0, 2, 3)
        return (0,)
    if x == 10:
        if 1 <= R <= 8: return (0, 1) if R % 2 else (2, 3)
        if R == 9: return (0,)
        if R == 10: return (1,)
        if R == 11: return (0,)
        if R == 12: return (1, 2, 3)
        if 13 <= R <= 20:
            return (1,) if R % 2 else (1, 2, 3)
        return (1,)
    if x == 11:
        if 1 <= R <= 8: return (0, 1) if R % 2 else (2, 3)
        if R == 9: return (0,)
        if R == 10: return (1,)
        if R == 11: return (0,)
        if R == 12: return (1, 2, 3)
        if 13 <= R <= 21: return (0, 1) if R % 2 else (0,)
        return (0,)
    if x == 12:
        if 1 <= R <= 8: return (0, 1) if R % 2 else (2, 3)
        if R == 9: return (0,)
        if R == 10: return (1,)
        if R == 11: return (0,)
        if R == 12: return (1, 2, 3)
        if R == 13: return (0, 1)
        if R == 14: return (0, 2)
        if 15 <= R <= 22: return (1,) if R % 2 else (0, 2)
        return (1,)
    if x >= 13 and x % 2:
        if 1 <= R <= 8: return (0, 1) if R % 2 else (2, 3)
        if R == 9: return (0,)
        if R == 10: return (1,)
        if R == 11: return (0,)
        if R == 12: return (1, 2, 3)
        if R == 13: return (0, 1)
        if R == 14: return (0, 2)
        if 15 <= R <= x + 10: return (1,) if R % 2 else (0,)
        return (0,)
    if x >= 14 and x % 2 == 0:
        if 1 <= R <= 8: return (0, 1) if R % 2 else (2, 3)
        if R == 9: return (0,)
        if R == 10: return (1,)
        if R == 11: return (0,)
        if R == 12: return (1, 2, 3)
        if R == 13: return (0, 1)
        if R == 14: return (0, 2)
        if 15 <= R <= x + 10: return (1,) if R % 2 else (0,)
        return (1,)
    raise ValueError((x, R))


def audit_once():
    failures = []
    ordered, canonical = make_engines()
    direct = anchor_direct = 0

    for x in range(2, 61):
        for R in range(0, x + 41):
            expected = candidate(x, R)
            a = ordered(R, (x, 2), 8)
            b = canonical(R, (2, x), 8)
            direct += 2
            if a != expected or b != expected:
                failures.append(("target", x, R, a, b, expected))
            ba = canonical(R, (x, 1), 8)
            ca = canonical(R, (x, 2), 7)
            anchor_direct += 2
            if ba != z8_y1(x, R):
                failures.append(("B-anchor", x, R, ba, z8_y1(x, R)))
            if ca != z7_y2(x, R):
                failures.append(("C-anchor", x, R, ca, z7_y2(x, R)))

    signature_points = mex_points = odd_bound = even_bound = 0
    for x in range(2, 2001):
        for R in range(1, x + 16):
            signature_points += 1
            actual = anchor_signature(x, R)
            expected = band_signature(x, R)
            if actual != expected:
                failures.append(("signature", x, R, actual, expected))
                continue
            value = mex(actual)
            mex_points += 1
            if value != candidate(x, R):
                failures.append(("mex", x, R, value, candidate(x, R), actual))
            if R % 2:
                odd_bound += 1
                if not set(actual).issubset({0, 1}) or value > 2:
                    failures.append(("odd-parent-bound", x, R, actual, value))
            else:
                even_bound += 1
                if value > 1:
                    failures.append(("even-parent-bound", x, R, actual, value))

    tail_checks = 0
    for x in range(2, 5001):
        for offset in range(4):
            R = x + 11 + offset
            tail_checks += 1
            if candidate(x, R) != (x + 2) % 2:
                failures.append(("tail", x, R, candidate(x, R), (x + 2) % 2))

    rng = random.Random(20261119)
    far_tail = 0
    for _ in range(5000):
        x = rng.randint(2, 1_000_000)
        R = x + 11 + rng.randint(0, 1_000_000)
        far_tail += 1
        if candidate(x, R) != (x + 2) % 2:
            failures.append(("far-tail", x, R))

    counts = {
        "direct_formula_and_two_engine_checks": direct,
        "independent_anchor_direct_checks": anchor_direct,
        "signature_points": signature_points,
        "mex_identities": mex_points,
        "odd_parent_option_bounds": odd_bound,
        "even_parent_value_bounds": even_bound,
        "tail_checks": tail_checks,
        "far_tail_seeded_checks": far_tail,
    }
    return {
        "all_pass": not failures,
        "classification": (
            "universal proof by induction on x using the explicit A/B/C "
            "signature bands, K0983, K0978, K0832 Theorem T and the general "
            "tail theorem; finite checks are independent audits only"
        ),
        "counts": counts,
        "failures": failures,
        "scope": {
            "direct_x": [2, 60],
            "direct_R": "0 <= R <= x+40",
            "signature_x": [2, 2000],
            "signature_R": "1 <= R <= x+15",
            "tail_x": [2, 5000],
            "tail_offsets": [0, 3],
            "far_tail_samples": far_tail,
            "far_tail_seed": 20261119,
        },
        "target": "H(R;(x,2);8), x>=2, R>=0",
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
