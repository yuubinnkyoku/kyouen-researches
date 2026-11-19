#!/usr/bin/env python3
"""Independent audit for the proved z=11, y=4 two-token residual slice (K1015).

Universal proof: induction on x, with K1014 (z=11,y=3), K1006
(z=10,y=4), K0832's Theorem T, height-only reduction and general tail.
The two direct mex engines are finite independent audits, not the proof.
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


# K0832 single-token closed form.
def q_odd(k):
    return k if k % 2 else k - 1


def v_single(x, z, R):
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


# K1014: z=11, y=3.
def z11_y3_T(x, R):
    if x == 3:
        return R in (1, 3, 5)
    if x in (4, 5):
        return R in (1, 3, 5, 7)
    if x in (6, 7):
        return R in (1, 3, 5, 7, 9)
    if x == 8:
        return R in (1, 3, 5, 7, 9, 11, 13)
    if x == 9:
        return R in (1, 3, 5, 7, 9, 11)
    if x == 10:
        return R in (1, 3, 5, 7, 9, 11, 15)
    if x in (11, 12, 13):
        return R in (1, 3, 5, 7, 9, 11)
    if x == 14:
        return R in (1, 3, 5, 7, 9, 11, 17)
    if x == 15:
        return (R in (1, 3, 5, 7, 9, 11)
                or odd_between(R, 17, 29))
    return R in (1, 3, 5, 7, 9, 11, 17)


def z11_y3_P(x, R):
    if x in (3, 5, 7):
        return False
    if x == 4:
        return R >= 8
    if x == 6:
        return R >= 10
    if x == 8:
        return R == 12 or R >= 14
    if x in (9, 11):
        return R in (12, 14)
    if x in (10, 12):
        return R in (12, 14) or R >= 16
    if x == 13:
        return R in (12, 14, 16)
    if x == 14:
        return R in (12, 14, 16) or R >= 18
    if x == 15:
        return R in (12, 14, 16)
    if x % 2 == 0:
        return (R in (12, 14, 16)
                or odd_between(R, 19, x + 13)
                or R >= x + 15)
    return (R in (12, 14, 16)
            or odd_between(R, 19, x + 14))


def z11_y3(x, R):
    if R == 0:
        return 0
    if z11_y3_T(x, R):
        return 2
    return 1 if z11_y3_P(x, R) else 0


# K1006: z=10, y=4.
def z10_y4_T(x, R):
    if x == 4:
        return R in (1, 3, 5, 7)
    if x == 5:
        return R in (1, 3, 5, 7, 9)
    if x == 6:
        return R in (1, 3, 5, 7, 9, 11, 13)
    if x in (7, 9, 10, 11, 13, 14):
        return R in (1, 3, 5, 7, 9)
    if x == 8:
        return R in (1, 3, 5, 7, 9, 15)
    if x == 12:
        return R in (1, 3, 5, 7, 9, 17)
    if x == 15:
        return (R in (1, 3, 5, 7, 9)
                or odd_between(R, 19, 29))
    return R in (1, 3, 5, 7, 9, 19)


def z10_y4_P(x, R):
    if x in (4, 6):
        return False
    if x == 5:
        return R >= 10
    if x in (7, 9):
        return R in (11, 13, 15) or R >= 16
    if x == 8:
        return R in (11, 13)
    if x in (10, 12):
        return R in (11, 13, 15)
    if x in (11, 13):
        return R in (11, 13, 15, 17) or R >= 18
    if x == 14:
        return R in (11, 13, 15, 17)
    if x == 15:
        return (R in (11, 13, 15, 17)
                or even_between(R, 20, 30) or R >= 31)
    if x % 2 == 0:
        return (R in (11, 13, 15, 17)
                or even_between(R, 20, x + 14))
    return (R in (11, 13, 15, 17)
            or even_between(R, 20, x + 15)
            or R >= x + 16)


def z10_y4(x, R):
    if R == 0:
        return 0
    if z10_y4_T(x, R):
        return 2
    return 1 if z10_y4_P(x, R) else 0


# Candidate K1015: z=11, y=4.
def candidate_T(x, R):
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
        return R in (1, 3, 5, 7, 9, 11) or odd_between(R, 19, 31)
    return R in (1, 3, 5, 7, 9, 11, 19)


def candidate_P(x, R):
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
        return (R in (12, 14, 16, 18)
                or odd_between(R, 21, x + 15))
    return (R in (12, 14, 16, 18)
            or odd_between(R, 21, x + 14)
            or R >= x + 16)


def candidate(x, R):
    if R == 0:
        return 0
    if candidate_T(x, R):
        return 2
    return 1 if candidate_P(x, R) else 0


def bands_for(x):
    if x == 4:
        return [(1, 1, 7, "01"), (0, 2, 8, "23"), (None, 9, None, "1")]
    if x == 5:
        return [(1, 1, 9, "01"), (0, 2, 8, "23"),
                (None, 10, 10, "03"), (None, 11, None, "0")]
    if x == 6:
        return [(1, 1, 9, "01"), (0, 2, 10, "23"),
                (None, 11, 11, "1"), (0, 12, 14, "13"),
                (None, 13, 13, "1"), (None, 15, None, "1")]
    if x == 7:
        return [(1, 1, 11, "01"), (0, 2, 10, "23"),
                (0, 12, 14, "0"), (1, 13, 15, "01"),
                (None, 16, None, "0")]
    if x == 8:
        return [(1, 1, 11, "01"), (0, 2, 10, "23"),
                (0, 12, 14, "02"), (1, 13, 15, "1"),
                (None, 16, 16, "123"), (None, 17, None, "1")]
    if x == 9:
        return [(1, 1, 11, "01"), (0, 2, 10, "23"),
                (None, 12, 12, "02"), (None, 13, 13, "1"),
                (None, 14, 14, "0"), (None, 15, 15, "1"),
                (None, 16, None, "0")]
    if x == 10:
        return [(1, 1, 11, "01"), (0, 2, 10, "23"),
                (None, 12, 12, "02"), (None, 13, 13, "1"),
                (None, 14, 14, "0"), (None, 15, 15, "1"),
                (None, 16, 16, "02"), (None, 17, None, "1")]
    if x == 11:
        return [(1, 1, 11, "01"), (0, 2, 10, "23"),
                (None, 12, 12, "02"), (None, 13, 13, "1"),
                (None, 14, 14, "0"), (None, 15, 15, "1"),
                (None, 16, 16, "0"), (None, 17, 17, "01"),
                (None, 18, None, "0")]
    if x == 12:
        return [(1, 1, 11, "01"), (0, 2, 10, "23"),
                (None, 12, 12, "02"), (None, 13, 13, "1"),
                (None, 14, 14, "0"), (None, 15, 15, "1"),
                (None, 16, 16, "0"), (None, 17, 17, "1"),
                (None, 18, 18, "123"), (None, 19, None, "1")]
    if x == 13:
        return [(1, 1, 11, "01"), (0, 2, 10, "23"),
                (None, 12, 12, "02"), (None, 13, 13, "1"),
                (None, 14, 14, "0"), (None, 15, 15, "1"),
                (None, 16, 16, "0"), (None, 17, 17, "1"),
                (None, 18, None, "0")]
    if x == 14:
        return [(1, 1, 11, "01"), (0, 2, 10, "23"),
                (None, 12, 12, "02"), (None, 13, 13, "1"),
                (None, 14, 14, "0"), (None, 15, 15, "1"),
                (None, 16, 16, "0"), (None, 17, 17, "1"),
                (None, 18, 18, "02"), (None, 19, None, "1")]
    if x == 15:
        return [(1, 1, 11, "01"), (0, 2, 10, "23"),
                (None, 12, 12, "02"), (None, 13, 13, "1"),
                (None, 14, 14, "0"), (None, 15, 15, "1"),
                (None, 16, 16, "0"), (None, 17, 17, "1"),
                (None, 18, 18, "02"), (None, 19, 19, "01"),
                (None, 20, 20, "023"), (1, 21, 29, "0"),
                (0, 22, 30, "023"), (None, 31, None, "0")]
    if x == 16:
        return [(1, 1, 11, "01"), (0, 2, 10, "23"),
                (None, 12, 12, "02"), (None, 13, 13, "1"),
                (None, 14, 14, "0"), (None, 15, 15, "1"),
                (None, 16, 16, "0"), (None, 17, 17, "1"),
                (None, 18, 18, "02"), (None, 19, 19, "01"),
                (None, 20, 20, "123"), (1, 21, 31, "01"),
                (0, 22, 30, "1"), (None, 32, None, "1")]
    if x == 17:
        return [(1, 1, 11, "01"), (0, 2, 10, "23"),
                (None, 12, 12, "02"), (None, 13, 13, "1"),
                (None, 14, 14, "0"), (None, 15, 15, "1"),
                (None, 16, 16, "0"), (None, 17, 17, "1"),
                (None, 18, 18, "02"), (None, 19, 19, "01"),
                (None, 20, 20, "123"), (1, 21, 31, "0"),
                (0, 22, 32, "12"), (None, 33, None, "0")]
    if x % 2 == 1:
        return [(1, 1, 11, "01"), (0, 2, 10, "23"),
                (None, 12, 12, "02"), (None, 13, 13, "1"),
                (None, 14, 14, "0"), (None, 15, 15, "1"),
                (None, 16, 16, "0"), (None, 17, 17, "1"),
                (None, 18, 18, "02"), (None, 19, 19, "01"),
                (None, 20, 20, "123"), (1, 21, x + 14, "0"),
                (0, 22, x + 15, "1"), (None, x + 16, None, "0")]
    return [(1, 1, 11, "01"), (0, 2, 10, "23"),
            (None, 12, 12, "02"), (None, 13, 13, "1"),
            (None, 14, 14, "0"), (None, 15, 15, "1"),
            (None, 16, 16, "0"), (None, 17, 17, "1"),
            (None, 18, 18, "02"), (None, 19, 19, "01"),
            (None, 20, 20, "123"), (1, 21, x + 15, "0"),
            (0, 22, x + 14, "1"), (None, x + 16, None, "1")]


def band_signature(x, R):
    hits = []
    for parity, lo, hi, signature in bands_for(x):
        if (parity is None or R % 2 == parity) and R >= lo and (hi is None or R <= hi):
            hits.append(signature)
    return hits


def anchor_signature(x, R, y4_formula):
    r = R - 1
    a = y4_formula(x - 1, r) if x >= 5 else z11_y3(4, r)
    b = z11_y3(x, r)
    c = 1 ^ z10_y4(x, r)
    return "".join(str(v) for v in sorted({a, b, c}))


def audit_once():
    ordered, canonical = make_engines()
    failures = []
    counts = {}

    direct = 0
    for x in range(4, 81):
        for R in range(0, x + 41):
            expected = candidate(x, R)
            a = ordered(R, (x, 4), 11)
            b = canonical(R, (x, 4), 11)
            direct += 2
            if a != expected or b != expected or a != b:
                failures.append(("direct", x, R, a, b, expected))
    counts["ordered_and_canonical_direct_vs_formula"] = direct

    child_checks = 0
    for x in range(4, 81):
        for R in range(0, x + 41):
            if ordered(R, (x, 3), 11) != z11_y3(x, R):
                failures.append(("B-child", x, R))
            if ordered(R, (x, 4), 10) != z10_y4(x, R):
                failures.append(("C-child", x, R))
            child_checks += 2
    counts["B_C_child_anchor_direct_checks"] = child_checks

    signature_checks = parity_checks = 0
    for x in range(4, 3001):
        for R in range(1, x + 17):
            hits = band_signature(x, R)
            actual = anchor_signature(x, R, candidate)
            if len(hits) != 1:
                failures.append(("coverage", x, R, hits))
                continue
            if hits[0] != actual:
                failures.append(("signature", x, R, hits[0], actual))
                continue
            sig_values = {int(ch) for ch in hits[0]}
            value = mex(sig_values)
            signature_checks += 1
            if value != candidate(x, R):
                failures.append(("mex", x, R, hits[0], value, candidate(x, R)))
            if R % 2:
                if not sig_values.issubset({0, 1}) or value > 2:
                    failures.append(("Theorem-T-odd", x, R, hits[0], value))
            else:
                if value > 1:
                    failures.append(("Theorem-T-even", x, R, hits[0], value))
            parity_checks += 1
    counts["A_B_C_signature_coverage_identity_and_mex"] = signature_checks
    counts["Theorem_T_parity_bound"] = parity_checks

    low_checks = 0
    for x in range(4, 1001):
        for R in range(0, 13):
            if candidate(x, R) != v_single(x + 4, 11, R):
                failures.append(("height-only", x, R, candidate(x, R),
                                 v_single(x + 4, 11, R)))
            low_checks += 1
    counts["height_only_reduction_R_le_12"] = low_checks

    tail_checks = tail_signature_checks = 0
    for x in range(4, 10001):
        for offset in range(4):
            R = x + 16 + offset
            expected = (x + 4) % 2
            if candidate(x, R) != expected:
                failures.append(("tail", x, R, candidate(x, R), expected))
            sig = anchor_signature(x, R, candidate)
            expected_sig = "1" if x % 2 == 0 else "0"
            if sig != expected_sig:
                failures.append(("tail-signature", x, R, sig, expected_sig))
            tail_checks += 1
            tail_signature_checks += 1
    counts["general_tail"] = tail_checks
    counts["general_tail_signature"] = tail_signature_checks

    theorem_grid = 0
    for x in range(4, 3001):
        for R in range(0, x + 26):
            value = candidate(x, R)
            if value not in (0, 1, 2):
                failures.append(("range", x, R, value))
            if R % 2 == 0 and value > 1:
                failures.append(("even-parent-bound", x, R, value))
            if value == 2 and R % 2 == 0:
                failures.append(("even-value-two", x, R))
            theorem_grid += 1
    counts["Theorem_T_formula_grid"] = theorem_grid

    rng = random.Random(20261119)
    scatter = 0
    for _ in range(25000):
        x = rng.randint(4, 10000)
        R = rng.randint(0, x + 100)
        if R == 0:
            actual = 0
        else:
            actual = mex({
                candidate(x - 1, R - 1) if x >= 5 else z11_y3(4, R - 1),
                z11_y3(x, R - 1),
                1 ^ z10_y4(x, R - 1),
            })
        if actual != candidate(x, R):
            failures.append(("scatter", x, R, actual, candidate(x, R)))
        scatter += 1
    counts["fixed_seed_ABC_scatter"] = scatter

    return {
        "all_pass": not failures,
        "theorem": "K1015 z=11 y=4 two-token residual Grundy slice",
        "classification": "universal proof by x-induction and complete A/B/C signature bands",
        "finite_audit_role": "independent recurrence, transcription, band, mex, low-R, tail, and scatter checks only",
        "scope": {
            "target": "H(R;(x,4);11), x>=4, R>=0",
            "direct_x": [4, 80],
            "direct_R": "0..x+40",
            "signature_x": [4, 3000],
            "signature_R": "1..x+16",
            "low_R": "0..12",
            "tail_x": [4, 10000],
            "tail_R": "x+16..x+19",
            "scatter_points": 25000,
            "scatter_seed": 20261119,
        },
        "counts": counts,
        "total_checks": sum(counts.values()),
        "failure_count": len(failures),
        "first_failures": failures[:10],
        "ordered_cache": ordered.cache_info()._asdict(),
        "canonical_cache": canonical.cache_info()._asdict(),
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
