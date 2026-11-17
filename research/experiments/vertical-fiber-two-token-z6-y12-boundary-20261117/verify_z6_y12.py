#!/usr/bin/env python3
"""Independent finite audit for the proved two-token residual slice z=6,y=12."""
from __future__ import annotations

import hashlib
import json
import random
from functools import lru_cache
from pathlib import Path


def mex(values):
    seen = set(values)
    value = 0
    while value in seen:
        value += 1
    return value


def odd(r, lo, hi=None):
    return r >= lo and (hi is None or r <= hi) and r % 2 == 1


def even(r, lo, hi=None):
    return r >= lo and (hi is None or r <= hi) and r % 2 == 0


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


def h6_y11(x, r):
    if r == 0:
        return 0
    t = {1, 3, 5}
    if x == 11:
        t.add(25)
    elif x == 15:
        t.add(27)
    elif x == 18:
        t.update({29, 31, 33, 35})
    elif x >= 19:
        t.add(29)
    if r in t:
        return 2
    if x == 11:
        p = odd(r, 7, 23)
    elif x == 12:
        p = odd(r, 7) or even(r, 26)
    elif x == 13:
        p = odd(r, 7, 25)
    elif x == 14:
        p = odd(r, 7) or even(r, 28)
    elif x == 15:
        p = odd(r, 7, 25)
    elif x == 16:
        p = odd(r, 7) or even(r, 28)
    elif x == 17:
        p = odd(r, 7, 27)
    elif x % 2 == 0:
        p = odd(r, 7, 27) or even(r, 30) or r >= x + 18
    else:
        p = odd(r, 7, 27) or even(r, 30, x + 17)
    return int(p)


def h6_y12(x, r):
    if r == 0:
        return 0
    t = {1, 3, 5}
    if x == 12:
        t.add(27)
    elif x == 16:
        t.add(29)
    elif x == 19:
        t.update({31, 33, 35, 37})
    elif x >= 20:
        t.add(31)
    if r in t:
        return 2
    if x == 12:
        p = odd(r, 7, 25)
    elif x == 13:
        p = odd(r, 7) or even(r, 28)
    elif x == 14:
        p = odd(r, 7, 27)
    elif x == 15:
        p = odd(r, 7) or even(r, 30)
    elif x == 16:
        p = odd(r, 7, 27)
    elif x == 17:
        p = odd(r, 7) or even(r, 30)
    elif x == 18:
        p = odd(r, 7, 29)
    elif x == 19:
        p = odd(r, 7, 29) or even(r, 32) or odd(r, 39)
    elif x % 2 == 0:
        p = odd(r, 7, 29) or even(r, 32, x + 18)
    else:
        p = odd(r, 7, 29) or even(r, 32) or odd(r, x + 20)
    return int(p)


SMALL_SIGNATURES = {
    12: {
        1: [(1, 5, "01"), (7, 25, "0"), (27, 27, "01"), (29, 29, "1")],
        0: [(2, 6, "23"), (8, 30, "1")],
    },
    13: {
        1: [(1, 5, "01"), (7, 31, "0")],
        0: [(2, 6, "23"), (8, 26, "1"), (28, 28, "023"), (30, 30, "0")],
    },
    14: {
        1: [(1, 5, "01"), (7, 27, "0"), (29, 31, "1")],
        0: [(2, 6, "23"), (8, 32, "1")],
    },
    15: {
        1: [(1, 5, "01"), (7, 33, "0")],
        0: [(2, 6, "23"), (8, 26, "1"), (28, 28, "12"), (30, 32, "0")],
    },
    16: {
        1: [(1, 5, "01"), (7, 27, "0"), (29, 29, "01"), (31, 33, "1")],
        0: [(2, 6, "23"), (8, 34, "1")],
    },
    17: {
        1: [(1, 5, "01"), (7, 35, "0")],
        0: [(2, 6, "23"), (8, 28, "1"), (30, 30, "023"), (32, 34, "0")],
    },
    18: {
        1: [(1, 5, "01"), (7, 29, "0"), (31, 35, "1")],
        0: [(2, 6, "23"), (8, 28, "1"), (30, 36, "123")],
    },
    19: {
        1: [(1, 5, "01"), (7, 29, "0"), (31, 37, "01")],
        0: [(2, 6, "23"), (8, 28, "1"), (30, 30, "123"), (32, 36, "0")],
    },
    20: {
        1: [(1, 5, "01"), (7, 29, "0"), (31, 31, "01"), (33, 37, "1")],
        0: [(2, 6, "23"), (8, 28, "1"), (30, 30, "123"), (32, 38, "02")],
    },
}


def expected_signature(x, r):
    if x in SMALL_SIGNATURES:
        rows = SMALL_SIGNATURES[x][r % 2]
    else:
        assert x >= 21
        if r % 2:
            upper = x + 18 if x % 2 else x + 17
            rows = [(1, 5, "01"), (7, 29, "0"), (31, 31, "01"), (33, upper, "1")]
        else:
            upper = x + 17 if x % 2 else x + 18
            rows = [
                (2, 6, "23"), (8, 28, "1"), (30, 30, "123"),
                (32, 32, "02"), (34, upper, "0"),
            ]
    for lo, hi, digits in rows:
        if lo <= r <= hi and (r - lo) % 2 == 0:
            return {int(ch) for ch in digits}
    return set()


def actual_signature(x, r):
    a = h6_y11(12, r - 1) if x == 12 else h6_y12(x - 1, r - 1)
    b = h6_y11(x, r - 1)
    c = 1 ^ h5(x, 12, r - 1)
    return {a, b, c}


def predicted_value2_positions(x):
    if x == 12:
        extra = {27}
    elif x == 16:
        extra = {29}
    elif x == 19:
        extra = {31, 33, 35, 37}
    elif x >= 20:
        extra = {31}
    else:
        extra = set()
    return {1, 3, 5} | extra


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


def run_audit():
    failures = []
    direct = 0
    for x in range(12, 41):
        for r in range(x + 36):
            cases = (
                (6, (x, 12), h6_y12(x, r)),
                (6, (x, 11), h6_y11(x, r)),
                (5, (x, 12), h5(x, 12, r)),
            )
            for z, tokens, formula in cases:
                ordered = exact_ordered(r, tokens, z)
                canonical = exact_canonical(
                    r, tuple(sorted(tokens, reverse=True)), z
                )
                direct += 1
                if ordered != canonical or ordered != formula:
                    failures.append({
                        "kind": "direct-two-engine-formula-anchor",
                        "x": x, "r": r, "z": z, "tokens": tokens,
                        "ordered": ordered, "canonical": canonical,
                        "formula": formula,
                    })

    signature_checks = mex_checks = odd_checks = even_checks = 0
    family_checks = 0
    for x in range(12, 2001):
        observed_t = set()
        for r in range(1, x + 19):
            actual = actual_signature(x, r)
            expected = expected_signature(x, r)
            signature_checks += 1
            if actual != expected:
                failures.append({
                    "kind": "signature", "x": x, "r": r,
                    "actual": sorted(actual), "expected": sorted(expected),
                })
            value = mex(actual)
            mex_checks += 1
            if value != h6_y12(x, r):
                failures.append({
                    "kind": "mex", "x": x, "r": r,
                    "actual": value, "formula": h6_y12(x, r),
                })
            if value == 2:
                observed_t.add(r)
            if r % 2:
                odd_checks += 1
                if not actual <= {0, 1}:
                    failures.append({
                        "kind": "odd-parent-bound", "x": x, "r": r,
                        "options": sorted(actual),
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
        if observed_t != predicted:
            failures.append({
                "kind": "three-family-specialization", "x": x,
                "actual": sorted(observed_t), "predicted": sorted(predicted),
            })

    tail_checks = 0
    for x in range(12, 2001):
        for offset in range(65):
            r = x + 19 + offset
            tail_checks += 1
            if h6_y12(x, r) != (x + 12) % 2:
                failures.append({
                    "kind": "tail", "x": x, "r": r,
                    "actual": h6_y12(x, r), "expected": (x + 12) % 2,
                })

    rng = random.Random(20261117)
    random_tail_checks = 0
    for _ in range(2000):
        x = rng.randint(12, 100000)
        r = x + 19 + rng.randint(0, 100000)
        random_tail_checks += 1
        if h6_y12(x, r) != (x + 12) % 2:
            failures.append({"kind": "random-tail", "x": x, "r": r})

    counts = {
        "direct_ordered_canonical_formula": direct,
        "option_signatures": signature_checks,
        "mex": mex_checks,
        "odd_parent_bounds": odd_checks,
        "even_parent_bounds": even_checks,
        "three_family_specialization": family_checks,
        "tail": tail_checks,
        "fixed_seed_random_tail": random_tail_checks,
    }
    return {
        "schema": "two-token-z6-y12-audit-v1",
        "claim": "H(R;(x,12);6) is given by the complete formula for all x>=12,R>=0",
        "classification": "finite-independent-audit-not-proof",
        "counts": counts,
        "total_checks": sum(counts.values()),
        "seed": 20261117,
        "failures": failures,
        "pass": not failures,
    }


def main():
    audit = run_audit()
    encoded = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    audit["sha256_without_hash_field"] = hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()
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
    }, ensure_ascii=False, sort_keys=True))
    if not audit["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
