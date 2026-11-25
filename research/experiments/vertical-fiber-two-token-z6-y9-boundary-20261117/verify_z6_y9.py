#!/usr/bin/env python3
"""Independent finite audit for the proved two-token residual slice z=6,y=9."""
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


def even(r, lo, hi):
    return r % 2 == 0 and lo <= r <= hi


def odd(r, lo, hi):
    return r % 2 == 1 and lo <= r <= hi


@lru_cache(None)
def exact_ordered(r, tokens, z):
    if r == 0:
        return 0
    options = []
    for i, token in enumerate(tokens):
        child = list(tokens)
        if token >= 2:
            child[i] = token - 1
            next_z = z
        else:
            child.pop(i)
            next_z = z + 1
        options.append(exact_ordered(r - 1, tuple(child), next_z))
    if z >= 1:
        options.append(1 ^ exact_ordered(r - 1, tokens, z - 1))
    return mex(options)


@lru_cache(None)
def exact_canonical(r, tokens, z):
    if r == 0:
        return 0
    options = []
    for i, token in enumerate(tokens):
        child = list(tokens)
        if token >= 2:
            child[i] = token - 1
            next_z = z
        else:
            child.pop(i)
            next_z = z + 1
        options.append(exact_canonical(
            r - 1, tuple(sorted(child, reverse=True)), next_z
        ))
    if z >= 1:
        options.append(1 ^ exact_canonical(r - 1, tokens, z - 1))
    return mex(options)


def h5(x, y, r):
    if r == 0:
        return 0
    s, d = x + y, x - y
    if d == 0:
        t = {1} if y == 1 else ({1, 3} if y == 2 else {1, 3, 5})
    elif d == 1:
        t = {1, 3} if y == 1 else {1, 3, 5, 2 * y + 3}
    elif d == 2:
        t = {1, 3} if y == 1 else {1, 3, 5}
    elif d in (3, 4):
        t = {1, 3, 5}
    elif d == 5:
        t = {1, 3, 5, 2 * y + 5}
    elif d == 6:
        t = {1, 3, 5, 2 * y + 5, 2 * y + 7, 2 * y + 9, 2 * y + 11}
    else:
        t = {1, 3, 5, 2 * y + 5}
    if r in t:
        return 2
    if d == 0:
        p = y >= 3 and even(r, 6, s + 2)
    elif d == 1:
        p = (r >= 4) if y == 1 else (even(r, 6, s + 3) or r >= s + 4)
    elif d == 2:
        p = y >= 2 and even(r, 6, s)
    elif d == 3:
        p = even(r, 6, s + 1) or r >= s + 2
    elif d == 4:
        p = even(r, 6, s)
    elif d == 5:
        p = even(r, 6, s - 1) or r >= s + 1
    elif d == 6:
        p = even(r, 6, s - 2)
    elif d >= 7 and d % 2:
        p = even(r, 6, 2 * y + 4) or odd(r, 2 * y + 7, s + 4) or r >= s + 6
    else:
        p = even(r, 6, 2 * y + 4) or odd(r, 2 * y + 7, s + 5)
    return int(p)


def h6_y8(x, r):
    if r == 0:
        return 0
    base = {1, 3, 5}
    if x == 8:
        t, p = base | {19}, odd(r, 7, 17)
    elif x == 9:
        t, p = base, odd(r, 7, 19) or r >= 20
    elif x == 10:
        t, p = base, odd(r, 7, 19)
    elif x == 11:
        t, p = base, odd(r, 7, 21) or r >= 22
    elif x == 12:
        t, p = base | {21}, odd(r, 7, 19)
    elif x == 13:
        t, p = base, odd(r, 7, 21) or r >= 22
    elif x == 14:
        t, p = base, odd(r, 7, 21)
    elif x == 15:
        t, p = base | {23, 25, 27, 29}, odd(r, 7, 21) or even(r, 24, 28) or r >= 30
    elif x >= 16 and x % 2 == 0:
        t, p = base | {23}, odd(r, 7, 21) or even(r, 24, x + 14)
    else:
        t, p = base | {23}, odd(r, 7, 21) or even(r, 24, x + 13) or r >= x + 15
    return 2 if r in t else int(p)


def h6_y9(x, r):
    if r == 0:
        return 0
    base = {1, 3, 5}
    if x == 9:
        extra = {21}
    elif x == 13:
        extra = {23}
    elif x == 16:
        extra = {25, 27, 29, 31}
    elif x >= 17:
        extra = {25}
    else:
        extra = set()
    t = base | extra
    if x == 9:
        p = odd(r, 7, 19)
    elif x == 10:
        p = odd(r, 7, 25) or r >= 22
    elif x == 11:
        p = odd(r, 7, 21)
    elif x == 12:
        p = odd(r, 7, 27) or r >= 24
    elif x == 13:
        p = odd(r, 7, 21)
    elif x == 14:
        p = odd(r, 7, 29) or r >= 24
    elif x == 15:
        p = odd(r, 7, 23)
    elif x == 16:
        p = odd(r, 7, 23) or even(r, 26, 30) or r >= 32
    elif x == 17:
        p = odd(r, 7, 23) or even(r, 26, 32)
    elif x >= 18 and x % 2 == 0:
        p = odd(r, 7, 23) or even(r, 26, x + 14) or r >= x + 16
    else:
        p = odd(r, 7, 23) or even(r, 26, x + 15)
    return 2 if r in t else int(p)


SMALL_SIGNATURES = {
    9: {
        1: [(1, 5, "01"), (7, 19, "0"), (21, 21, "01"), (23, 23, "1")],
        0: [(2, 6, "23"), (8, 24, "1")],
    },
    10: {
        1: [(1, 5, "01"), (7, 25, "0")],
        0: [(2, 6, "23"), (8, 20, "1"), (22, 22, "023"), (24, 24, "0")],
    },
    11: {
        1: [(1, 5, "01"), (7, 21, "0"), (23, 25, "1")],
        0: [(2, 6, "23"), (8, 26, "1")],
    },
    12: {
        1: [(1, 5, "01"), (7, 27, "0")],
        0: [(2, 6, "23"), (8, 20, "1"), (22, 22, "12"), (24, 26, "0")],
    },
    13: {
        1: [(1, 5, "01"), (7, 21, "0"), (23, 23, "01"), (25, 27, "1")],
        0: [(2, 6, "23"), (8, 28, "1")],
    },
    14: {
        1: [(1, 5, "01"), (7, 29, "0")],
        0: [(2, 6, "23"), (8, 22, "1"), (24, 24, "023"), (26, 28, "0")],
    },
    15: {
        1: [(1, 5, "01"), (7, 23, "0"), (25, 29, "1")],
        0: [(2, 6, "23"), (8, 22, "1"), (24, 30, "123")],
    },
    16: {
        1: [(1, 5, "01"), (7, 23, "0"), (25, 31, "01")],
        0: [(2, 6, "23"), (8, 22, "1"), (24, 24, "123"), (26, 30, "0")],
    },
    17: {
        1: [(1, 5, "01"), (7, 23, "0"), (25, 25, "01"), (27, 31, "1")],
        0: [(2, 6, "23"), (8, 22, "1"), (24, 24, "123"), (26, 32, "02")],
    },
}


def expected_signature(x, r):
    if x < 18:
        rows = SMALL_SIGNATURES[x][r % 2]
    elif r % 2:
        upper = x + 15 if x % 2 == 0 else x + 14
        rows = [(1, 5, "01"), (7, 23, "0"), (25, 25, "01"), (27, upper, "1")]
    else:
        upper = x + 14 if x % 2 == 0 else x + 15
        rows = [(2, 6, "23"), (8, 22, "1"), (24, 24, "123"),
                (26, 26, "02"), (28, upper, "0")]
    for lo, hi, digits in rows:
        if lo <= r <= hi and (r - lo) % 2 == 0:
            return {int(ch) for ch in digits}
    return set()


def actual_signature(x, r):
    a = h6_y8(9, r - 1) if x == 9 else h6_y9(x - 1, r - 1)
    b = h6_y8(x, r - 1)
    c = 1 ^ h5(x, 9, r - 1)
    return {a, b, c}


def predicted_value2_positions(x):
    extra = ({21} if x == 9 else {23} if x == 13
             else {25, 27, 29, 31} if x == 16
             else {25} if x >= 17 else set())
    return {1, 3, 5} | extra


def run_audit():
    failures = []
    direct = 0
    for x in range(9, 46):
        for r in range(x + 36):
            cases = (
                (6, (x, 9), h6_y9(x, r)),
                (6, (x, 8), h6_y8(x, r)),
                (5, (x, 9), h5(x, 9, r)),
            )
            for z, tokens, formula in cases:
                ordered = exact_ordered(r, tokens, z)
                canonical = exact_canonical(
                    r, tuple(sorted(tokens, reverse=True)), z
                )
                direct += 1
                if ordered != canonical or ordered != formula:
                    failures.append({
                        "kind": "direct-recurrence", "x": x, "r": r,
                        "z": z, "tokens": tokens, "ordered": ordered,
                        "canonical": canonical, "formula": formula,
                    })

    signature_checks = mex_checks = odd_checks = even_checks = 0
    family_checks = 0
    for x in range(9, 2001):
        actual_t = set()
        for r in range(1, x + 16):
            options = actual_signature(x, r)
            expected = expected_signature(x, r)
            signature_checks += 1
            if options != expected:
                failures.append({
                    "kind": "signature", "x": x, "r": r,
                    "actual": sorted(options), "expected": sorted(expected),
                })
            value = mex(options)
            mex_checks += 1
            if value != h6_y9(x, r):
                failures.append({
                    "kind": "mex", "x": x, "r": r,
                    "options": sorted(options), "actual": value,
                    "formula": h6_y9(x, r),
                })
            if value == 2:
                actual_t.add(r)
            if r % 2:
                odd_checks += 1
                if not options <= {0, 1}:
                    failures.append({
                        "kind": "odd-parent-bound", "x": x, "r": r,
                        "options": sorted(options),
                    })
            else:
                even_checks += 1
                if value > 1:
                    failures.append({
                        "kind": "even-parent-bound", "x": x, "r": r,
                        "value": value,
                    })
        family_checks += 1
        predicted = predicted_value2_positions(x)
        if actual_t != predicted:
            failures.append({
                "kind": "three-family-specialization", "x": x,
                "actual": sorted(actual_t), "predicted": sorted(predicted),
            })

    tail_checks = 0
    for x in range(9, 2001):
        for offset in range(65):
            r = x + 16 + offset
            tail_checks += 1
            if h6_y9(x, r) != (x + 9) % 2:
                failures.append({
                    "kind": "tail", "x": x, "r": r,
                    "actual": h6_y9(x, r), "expected": (x + 9) % 2,
                })

    rng = random.Random(20261117)
    random_tail_checks = 0
    for _ in range(2000):
        x = rng.randint(9, 100000)
        r = x + 16 + rng.randint(0, 100000)
        random_tail_checks += 1
        if h6_y9(x, r) != (x + 9) % 2:
            failures.append({"kind": "random-tail", "x": x, "r": r})

    counts = {
        "direct_two_engine_formula_anchor_checks": direct,
        "option_signature_checks": signature_checks,
        "mex_identity_checks": mex_checks,
        "odd_parent_option_bound_checks": odd_checks,
        "even_parent_value_bound_checks": even_checks,
        "three_family_value2_specialization_checks": family_checks,
        "tail_checks": tail_checks,
        "fixed_seed_random_tail_checks": random_tail_checks,
    }
    audit = {
        "schema": "two-token-z6-y9-audit-v1",
        "claim": "H(R;(x,9);6) is given by the complete formula for all x>=9,R>=0",
        "classification": "finite-independent-audit-not-proof",
        "counts": counts,
        "total_checks": sum(counts.values()),
        "seed": 20261117,
        "failures": failures,
        "pass": not failures,
    }
    encoded = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    audit["sha256_without_hash_field"] = hashlib.sha256(encoded.encode("utf-8")).hexdigest()
    return audit


def main():
    audit = run_audit()
    output = Path(__file__).resolve().parent / "output" / "audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "pass": audit["pass"],
        "total_checks": audit["total_checks"],
        "failures": len(audit["failures"]),
        "sha256_without_hash_field": audit["sha256_without_hash_field"],
        "output": str(output),
    }, ensure_ascii=False, sort_keys=True))
    if not audit["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
