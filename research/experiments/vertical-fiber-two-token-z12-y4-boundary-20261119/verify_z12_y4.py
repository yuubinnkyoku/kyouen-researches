#!/usr/bin/env python3
"""Independent audit for K1024: z=12, y=4 two-token residual slice.

The universal argument is x-induction with K1021 as the B-child,
K1015 as the C-child, and the complete signature-band table in report.md.
The two direct mex engines and finite grids below audit transcription; they
are not used as a substitute for the all-x proof.
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


def odd_between(r, lo, hi):
    return lo <= r <= hi and r % 2 == 1


def even_between(r, lo, hi):
    return lo <= r <= hi and r % 2 == 0


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
        tokens = tuple(sorted(tokens, reverse=True))
        if R == 0:
            return 0
        options = set()
        previous = None
        for i, value in enumerate(tokens):
            if value == previous:
                continue
            previous = value
            if value > 1:
                child = tuple(sorted(
                    tokens[:i] + (value - 1,) + tokens[i + 1:],
                    reverse=True,
                ))
                options.add(canonical(R - 1, child, z))
            else:
                child = tuple(sorted(tokens[:i] + tokens[i + 1:],
                                     reverse=True))
                options.add(canonical(R - 1, child, z + 1))
        if z:
            options.add(1 ^ canonical(R - 1, tokens, z - 1))
        return mex(options)

    return ordered, canonical


# K0832 single-token closed form.
def q_odd(k):
    return k if k % 2 else k - 1


def single_token(x, z, R):
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


# K1015: z=11, y=4.
def z11_y4_T(x, R):
    if x == 4:
        return R in (1, 3, 5, 7)
    if x in (5, 6):
        return R in (1, 3, 5, 7, 9)
    if x == 7:
        return R in (1, 3, 5, 7, 9, 11, 13, 15)
    if x in (8, 9, 10):
        return R in (1, 3, 5, 7, 9, 11)
    if x == 11:
        return R in (1, 3, 5, 7, 9, 11, 17)
    if x in (12, 13, 14):
        return R in (1, 3, 5, 7, 9, 11)
    if x == 15:
        return R in (1, 3, 5, 7, 9, 11, 19)
    if x == 16:
        return (R in (1, 3, 5, 7, 9, 11)
                or odd_between(R, 19, 31))
    return R in (1, 3, 5, 7, 9, 11, 19)


def z11_y4_P(x, R):
    if x == 4:
        return False
    if x == 5:
        return R >= 10
    if x == 6:
        return False
    if x == 7:
        return R in (12, 14) or R >= 16
    if x == 8:
        return R in (12, 14)
    if x == 9:
        return R in (12, 14) or R >= 16
    if x == 10:
        return R in (12, 14, 16)
    if x == 11:
        return R in (12, 14, 16) or R >= 18
    if x == 12:
        return R in (12, 14, 16)
    if x == 13:
        return R in (12, 14, 16) or R >= 18
    if x == 14:
        return R in (12, 14, 16, 18)
    if x == 15:
        return R in (12, 14, 16, 18) or R >= 20
    if x == 16:
        return R in (12, 14, 16, 18)
    if x % 2 == 0:
        return R in (12, 14, 16, 18) or odd_between(R, 21, x + 15)
    return (R in (12, 14, 16, 18)
            or odd_between(R, 21, x + 14)
            or R >= x + 16)


def z11_y4(x, R):
    if R == 0:
        return 0
    if z11_y4_T(x, R):
        return 2
    return 1 if z11_y4_P(x, R) else 0


# K1021: z=12, y=3.
def z12_y3_T(x, R):
    if x == 3:
        return odd_between(R, 1, 5)
    if x == 4:
        return odd_between(R, 1, 7)
    if x == 5:
        return odd_between(R, 1, 7)
    if x == 6:
        return odd_between(R, 1, 9)
    if x == 7:
        return odd_between(R, 1, 9)
    if x == 8:
        return odd_between(R, 1, 11)
    if x == 9:
        return odd_between(R, 1, 15)
    if x in (10, 11, 12):
        return odd_between(R, 1, 11)
    if x == 13:
        return odd_between(R, 1, 11) or R == 17
    if x in (14, 15):
        return odd_between(R, 1, 11)
    if x == 16:
        return odd_between(R, 1, 11) or odd_between(R, 19, 31)
    return odd_between(R, 1, 11) or R == 19


def z12_y3_P(x, R):
    if x in (3, 5, 7, 9):
        return False
    if x == 4:
        return R >= 8
    if x == 6:
        return R >= 10
    if x == 8:
        return R >= 12
    if x == 10:
        return R in (13, 15) or R >= 16
    if x == 11:
        return R in (13, 15)
    if x == 12:
        return R in (13, 15) or R >= 17
    if x == 13:
        return R in (13, 15)
    if x == 14:
        return R in (13, 15) or R >= 17
    if x == 15:
        return R in (13, 15, 17)
    if x == 16:
        return (R in (13, 15, 17)
                or even_between(R, 20, 32) or R >= 33)
    if x % 2 == 1:
        return (R in (13, 15, 17)
                or even_between(R, 20, x + 15))
    return (R in (13, 15, 17)
            or even_between(R, 20, x + 16)
            or R >= x + 17)


def z12_y3(x, R):
    if R == 0:
        return 0
    if z12_y3_T(x, R):
        return 2
    return 1 if z12_y3_P(x, R) else 0


# K1024 candidate: z=12, y=4.
def z12_y4_T(x, R):
    if x == 4:
        return odd_between(R, 1, 7)
    if x in (5, 6):
        return odd_between(R, 1, 9)
    if x == 7:
        return odd_between(R, 1, 11)
    if x == 8:
        return odd_between(R, 1, 15)
    if x == 9:
        return odd_between(R, 1, 11)
    if x == 10:
        return odd_between(R, 1, 11) or R == 17
    if x in (11, 12, 13):
        return odd_between(R, 1, 11)
    if x == 14:
        return odd_between(R, 1, 11) or R == 19
    if x in (15, 16):
        return odd_between(R, 1, 11)
    if x == 17:
        return odd_between(R, 1, 11) or odd_between(R, 21, 33)
    return odd_between(R, 1, 11) or R == 21


def z12_y4_P(x, R):
    if x == 4:
        return False
    if x == 5:
        return R >= 10
    if x == 6:
        return False
    if x == 7:
        return R >= 12
    if x == 8:
        return False
    if x == 9:
        return R in (13, 15) or R >= 17
    if x == 10:
        return R in (13, 15)
    if x == 11:
        return R in (13, 15, 17) or R >= 18
    if x == 12:
        return R in (13, 15, 17)
    if x == 13:
        return R in (13, 15, 17) or R >= 19
    if x == 14:
        return R in (13, 15, 17)
    if x == 15:
        return R in (13, 15, 17) or R >= 19
    if x == 16:
        return R in (13, 15, 17, 19)
    if x == 17:
        return (R in (13, 15, 17, 19)
                or even_between(R, 22, 32) or R >= 34)
    if x == 18:
        return (R in (13, 15, 17, 19)
                or even_between(R, 22, 34))
    if x % 2 == 0:
        return (R in (13, 15, 17, 19)
                or even_between(R, 22, x + 16))
    return (R in (13, 15, 17, 19)
            or even_between(R, 22, x + 15)
            or R >= x + 17)


def z12_y4(x, R):
    if R == 0:
        return 0
    if z12_y4_T(x, R):
        return 2
    return 1 if z12_y4_P(x, R) else 0


# Complete A/B/C signature bands. A signature is the sorted set of child
# Grundy values. parity=1/0 means odd/even; None means both parities.
def bands_for(x):
    if x == 4:
        return [(1,1,7,"01"), (1,9,None,"1"),
                (0,2,8,"23"), (0,10,None,"1")]
    if x == 5:
        return [(1,1,9,"01"), (1,11,None,"0"),
                (0,2,8,"23"), (0,10,10,"03"), (0,12,None,"0")]
    if x == 6:
        return [(1,1,9,"01"), (1,11,None,"1"),
                (0,2,10,"23"), (0,12,None,"1")]
    if x == 7:
        return [(1,1,11,"01"), (1,13,None,"0"),
                (0,2,10,"23"), (0,12,16,"03"), (0,18,None,"0")]
    if x == 8:
        return [(1,1,15,"01"), (1,17,None,"1"),
                (0,2,12,"23"), (0,14,None,"1")]
    if x == 9:
        return [(1,1,11,"01"), (1,13,None,"0"),
                (0,2,12,"23"), (0,14,16,"12"), (0,18,None,"0")]
    if x == 10:
        return [(1,1,11,"01"), (1,13,15,"0"), (1,17,17,"01"),
                (1,19,None,"1"), (0,2,12,"23"), (0,14,None,"1")]
    if x == 11:
        return [(1,1,11,"01"), (1,13,None,"0"),
                (0,2,12,"23"), (0,14,16,"1"),
                (0,18,18,"023"), (0,20,None,"0")]
    if x == 12:
        return [(1,1,11,"01"), (1,13,17,"0"), (1,19,None,"1"), (0,2,12,"23"), (0,14,None,"1")]
    if x == 13:
        return [(1,1,11,"01"), (1,13,None,"0"),
                (0,2,12,"23"), (0,14,16,"1"),
                (0,18,18,"12"), (0,20,None,"0")]
    if x == 14:
        return [(1,1,11,"01"), (1,13,17,"0"), (1,19,19,"01"),
                (1,21,None,"1"), (0,2,12,"23"), (0,14,None,"1")]
    if x == 15:
        return [(1,1,11,"01"), (1,13,None,"0"),
                (0,2,12,"23"), (0,14,18,"1"),
                (0,20,20,"023"), (0,22,None,"0")]
    if x == 16:
        return [(1,1,11,"01"), (1,13,19,"0"), (1,21,None,"1"),
                (0,2,12,"23"), (0,14,18,"1"),
                (0,20,32,"123"), (0,34,None,"1")]
    if x == 17:
        return [(1,1,11,"01"), (1,13,19,"0"), (1,21,33,"01"),
                (1,35,None,"0"), (0,2,12,"23"), (0,14,18,"1"),
                (0,20,20,"123"), (0,22,None,"0")]
    if x == 18:
        return [(1,1,11,"01"), (1,13,19,"0"), (1,21,21,"01"),
                (1,23,None,"1"), (0,2,12,"23"), (0,14,18,"1"),
                (0,20,20,"123"), (0,22,34,"02"), (0,36,None,"1")]
    if x % 2 == 1:
        return [(1,1,11,"01"), (1,13,19,"0"), (1,21,21,"01"),
                (1,23,x+16,"1"), (1,x+18,None,"0"),
                (0,2,12,"23"), (0,14,18,"1"), (0,20,20,"123"),
                (0,22,22,"02"), (0,24,None,"0")]
    return [(1,1,11,"01"), (1,13,19,"0"), (1,21,21,"01"),
            (1,23,None,"1"), (0,2,12,"23"), (0,14,18,"1"),
            (0,20,20,"123"), (0,22,22,"02"),
            (0,24,x+16,"0"), (0,x+18,None,"1")]


def band_signatures(x, R):
    return [sig for parity, lo, hi, sig in bands_for(x)
            if (parity is None or R % 2 == parity)
            and R >= lo and (hi is None or R <= hi)]


def child_signature(x, R):
    r = R - 1
    if x == 4:
        values = {z12_y3(x, r), 1 ^ z11_y4(x, r)}
    else:
        values = {
            z12_y4(x - 1, r),
            z12_y3(x, r),
            1 ^ z11_y4(x, r),
        }
    return "".join(str(v) for v in sorted(values))


def audit_once():
    ordered, canonical = make_engines()
    failures = []
    counts = {}

    direct = 0
    for x in range(4, 61):
        for R in range(0, x + 41):
            expected = z12_y4(x, R)
            a = ordered(R, (x, 4), 12)
            b = canonical(R, (x, 4), 12)
            direct += 2
            if a != expected or b != expected or a != b:
                failures.append(("direct", x, R, a, b, expected))
    counts["ordered_and_canonical_direct_vs_formula"] = direct

    child_checks = 0
    for x in range(3, 61):
        for R in range(0, x + 41):
            b1 = ordered(R, (x, 3), 12)
            b2 = canonical(R, (x, 3), 12)
            c1 = ordered(R, (x, 4), 11)
            c2 = canonical(R, (x, 4), 11)
            if b1 != z12_y3(x, R) or b2 != z12_y3(x, R):
                failures.append(("B-child", x, R, b1, b2, z12_y3(x, R)))
            if x >= 4 and (c1 != z11_y4(x, R) or c2 != z11_y4(x, R)):
                failures.append(("C-child", x, R, c1, c2, z11_y4(x, R)))
            child_checks += 4
    counts["B_C_child_anchor_direct_checks"] = child_checks

    signature_checks = parity_checks = 0
    for x in range(4, 1201):
        for R in range(1, x + 18):
            hits = band_signatures(x, R)
            actual = child_signature(x, R)
            if len(hits) != 1:
                failures.append(("coverage", x, R, hits))
                continue
            if hits[0] != actual:
                failures.append(("signature", x, R, hits[0], actual))
                continue
            value = mex({int(ch) for ch in hits[0]})
            expected = z12_y4(x, R)
            signature_checks += 1
            if value != expected:
                failures.append(("mex", x, R, hits[0], value, expected))
            if R % 2:
                if value > 2:
                    failures.append(("Theorem-T-odd", x, R, hits[0], value))
            elif value > 1:
                failures.append(("Theorem-T-even", x, R, hits[0], value))
            parity_checks += 1
    counts["A_B_C_signature_coverage_identity_and_mex"] = signature_checks
    counts["Theorem_T_parity_bound"] = parity_checks

    low_checks = 0
    for x in range(4, 401):
        for R in range(0, 14):
            a = z12_y4(x, R)
            b = single_token(x + 4, 12, R)
            if a != b:
                failures.append(("height-only", x, R, a, b))
            low_checks += 1
    counts["height_only_reduction_R_le_13"] = low_checks

    tail_checks = tail_signature_checks = 0
    for x in range(4, 5001):
        for offset in range(4):
            R = x + 17 + offset
            expected = (x + 4) % 2
            actual = z12_y4(x, R)
            sig = child_signature(x, R)
            expected_sig = "0" if x % 2 else "1"
            if actual != expected:
                failures.append(("tail", x, R, actual, expected))
            if sig != expected_sig:
                failures.append(("tail-signature", x, R, sig, expected_sig))
            tail_checks += 1
            tail_signature_checks += 1
    counts["general_tail"] = tail_checks
    counts["general_tail_signature"] = tail_signature_checks

    formula_grid = 0
    for x in range(4, 1201):
        for R in range(0, x + 27):
            value = z12_y4(x, R)
            if value not in (0, 1, 2):
                failures.append(("range", x, R, value))
            if R % 2 == 0 and value > 1:
                failures.append(("even-parent-bound", x, R, value))
            if value == 2 and R % 2 == 0:
                failures.append(("even-value-two", x, R))
            formula_grid += 1
    counts["formula_and_Theorem_T_grid"] = formula_grid

    rng = random.Random(20261119)
    scatter = 0
    for _ in range(12000):
        x = rng.randint(4, 10000)
        R = rng.randint(0, x + 100)
        if R == 0:
            actual = 0
        else:
            actual = mex({
                z12_y4(x - 1, R - 1) if x >= 5 else z12_y3(x, R - 1),
                z12_y3(x, R - 1),
                1 ^ z11_y4(x, R - 1),
            })
        if actual != z12_y4(x, R):
            failures.append(("fixed-seed-ABC", x, R, actual, z12_y4(x, R)))
        scatter += 1
    counts["fixed_seed_ABC_scatter"] = scatter

    return {
        "all_pass": not failures,
        "theorem": "K1024 z=12 y=4 two-token residual Grundy slice",
        "classification": "universal proof by x-induction and complete A/B/C signature bands",
        "finite_audit_role": "independent recurrence, child-anchor, transcription, band, mex, low-R, tail, and scatter checks only",
        "scope": {
            "target": "H(R;(x,4);12), x>=4, R>=0",
            "direct_x": [4, 60],
            "direct_R": "0..x+40",
            "signature_x": [4, 1200],
            "signature_R": "1..x+17",
            "low_R": "0..13",
            "tail_x": [4, 5000],
            "tail_R": "x+17..x+20",
            "scatter_points": 12000,
            "scatter_seed": 20261119,
        },
        "counts": counts,
        "total_checks": sum(counts.values()),
        "failure_count": len(failures),
        "first_failures": failures[:10],
    }


def run():
    first = audit_once()
    second = audit_once()
    first_bytes = json.dumps(first, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode()
    second_bytes = json.dumps(second, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":")).encode()
    same = first_bytes == second_bytes
    result = {
        **first,
        "repeat_runs": 2,
        "repeat_byte_identical": same,
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sha256_without_hash_field": hashlib.sha256(first_bytes).hexdigest(),
    }
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    (out / "audit.json").write_text(payload, encoding="utf-8")
    print(payload, end="")
    if not result["all_pass"] or not same:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
