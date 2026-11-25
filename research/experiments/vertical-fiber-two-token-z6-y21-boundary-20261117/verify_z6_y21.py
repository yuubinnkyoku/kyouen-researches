#!/usr/bin/env python3
"""Independent finite audit for the universally proved z=6, y=21 slice."""
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
    twos = {1, 3, 5}
    if d == 1:
        twos.add(2 * y + 3)
    elif d == 5:
        twos.add(2 * y + 5)
    elif d == 6:
        twos.update({2 * y + 5, 2 * y + 7, 2 * y + 9, 2 * y + 11})
    elif d >= 7:
        twos.add(2 * y + 5)
    if r in twos:
        return 2
    if d == 0:
        one = even(r, 6, s + 2)
    elif d == 1:
        one = even(r, 6, s + 3) or r >= s + 4
    elif d == 2:
        one = even(r, 6, s)
    elif d == 3:
        one = even(r, 6, s + 1) or r >= s + 2
    elif d == 4:
        one = even(r, 6, s)
    elif d == 5:
        one = even(r, 6, s - 1) or r >= s + 1
    elif d == 6:
        one = even(r, 6, s - 2)
    elif d >= 7 and d % 2:
        one = (
            even(r, 6, 2 * y + 4)
            or odd(r, 2 * y + 7, s + 4)
            or r >= s + 6
        )
    else:
        one = even(r, 6, 2 * y + 4) or odd(r, 2 * y + 7, s + 5)
    return int(one)


def h20(x, r):
    if r == 0:
        return 0
    twos = {1, 3, 5}
    if x == 20:
        twos.add(43)
    elif x == 24:
        twos.add(45)
    elif x == 27:
        twos.update({47, 49, 51, 53})
    elif x >= 28:
        twos.add(47)
    if r in twos:
        return 2
    if x == 20:
        one = odd(r, 7, 41)
    elif x == 21:
        one = odd(r, 7) or even(r, 44)
    elif x == 22:
        one = odd(r, 7, 43)
    elif x == 23:
        one = odd(r, 7) or even(r, 46)
    elif x == 24:
        one = odd(r, 7, 43)
    elif x == 25:
        one = odd(r, 7) or even(r, 46)
    elif x == 26:
        one = odd(r, 7, 45)
    elif x % 2:
        one = odd(r, 7, 45) or even(r, 48) or odd(r, x + 28)
    else:
        one = odd(r, 7, 45) or even(r, 48, x + 26)
    return int(one)


def twos21(x):
    result = {1, 3, 5}
    if x == 21:
        result.add(45)
    elif x == 25:
        result.add(47)
    elif x == 28:
        result.update({49, 51, 53, 55})
    elif x >= 29:
        result.add(49)
    return result


def ones21(x, r):
    if x == 21:
        return odd(r, 7, 43)
    if x == 22:
        return odd(r, 7) or even(r, 46)
    if x == 23:
        return odd(r, 7, 45)
    if x == 24:
        return odd(r, 7) or even(r, 48)
    if x == 25:
        return odd(r, 7, 45)
    if x == 26:
        return odd(r, 7) or even(r, 48)
    if x == 27:
        return odd(r, 7, 47)
    if x == 28:
        return odd(r, 7, 47) or even(r, 50) or odd(r, 57)
    if x == 29:
        return odd(r, 7, 47) or even(r, 50, 56)
    if x % 2:
        return odd(r, 7, 47) or even(r, 50, x + 27)
    return odd(r, 7, 47) or even(r, 50) or odd(r, x + 29)


def h21(x, r):
    if r in twos21(x):
        return 2
    if ones21(x, r):
        return 1
    return 0


ROWS = {
    21: (
        [(1, 5, "01"), (7, 43, "0"), (45, 45, "01"), (47, 47, "1")],
        [(2, 6, "23"), (8, 48, "1")],
    ),
    22: (
        [(1, 5, "01"), (7, 49, "0")],
        [(2, 6, "23"), (8, 44, "1"), (46, 46, "023"), (48, 48, "0")],
    ),
    23: (
        [(1, 5, "01"), (7, 45, "0"), (47, 49, "1")],
        [(2, 6, "23"), (8, 50, "1")],
    ),
    24: (
        [(1, 5, "01"), (7, 51, "0")],
        [(2, 6, "23"), (8, 44, "1"), (46, 46, "12"), (48, 50, "0")],
    ),
    25: (
        [(1, 5, "01"), (7, 45, "0"), (47, 47, "01"), (49, 51, "1")],
        [(2, 6, "23"), (8, 52, "1")],
    ),
    26: (
        [(1, 5, "01"), (7, 53, "0")],
        [(2, 6, "23"), (8, 46, "1"), (48, 48, "023"), (50, 52, "0")],
    ),
    27: (
        [(1, 5, "01"), (7, 47, "0"), (49, 53, "1")],
        [(2, 6, "23"), (8, 46, "1"), (48, 54, "123")],
    ),
    28: (
        [(1, 5, "01"), (7, 47, "0"), (49, 55, "01")],
        [(2, 6, "23"), (8, 46, "1"), (48, 48, "123"), (50, 54, "0")],
    ),
    29: (
        [(1, 5, "01"), (7, 47, "0"), (49, 49, "01"), (51, 55, "1")],
        [(2, 6, "23"), (8, 46, "1"), (48, 48, "123"), (50, 56, "02")],
    ),
}


def expected_signature(x, parent_r):
    odd_parent = parent_r % 2 == 1
    if x in ROWS:
        intervals = ROWS[x][0 if odd_parent else 1]
    elif odd_parent:
        upper = x + 26 if x % 2 else x + 27
        intervals = [
            (1, 5, "01"),
            (7, 47, "0"),
            (49, 49, "01"),
            (51, upper, "1"),
        ]
    else:
        upper = x + 27 if x % 2 else x + 26
        intervals = [
            (2, 6, "23"),
            (8, 46, "1"),
            (48, 48, "123"),
            (50, 50, "02"),
            (52, upper, "0"),
        ]
    for lo, hi, digits in intervals:
        if lo <= parent_r <= hi and (parent_r - lo) % 2 == 0:
            return tuple(int(digit) for digit in digits)
    return None


def family_value2(x):
    """K0832 three-family conjecture specialized to z=6, y=21."""
    d = x - 21
    result = {1, 3, 5}
    if d <= 6 and d % 2 == 0 and (6 + d) % 4 == 2:
        result.add(42 + (6 + d) // 2)
    elif d == 7:
        result.update({49, 51, 53, 55})
    elif d >= 8:
        result.add(49)
    return result


def actual_signature(x, parent_r):
    child_r = parent_r - 1
    a = h20(21, child_r) if x == 21 else h21(x - 1, child_r)
    b = h20(x, child_r)
    c = 1 ^ h5(x, 21, child_r)
    return tuple(sorted({a, b, c}))


@lru_cache(None)
def ordered_recurrence(r, tokens, z):
    if r == 0:
        return 0
    options = []
    for i, token in enumerate(tokens):
        child = list(tokens)
        child_z = z
        if token >= 2:
            child[i] -= 1
        else:
            child.pop(i)
            child_z += 1
        options.append(ordered_recurrence(r - 1, tuple(child), child_z))
    if z:
        options.append(1 ^ ordered_recurrence(r - 1, tokens, z - 1))
    return mex(options)


@lru_cache(None)
def canonical_recurrence(r, tokens, z):
    if r == 0:
        return 0
    options = []
    for i, token in enumerate(tokens):
        child = list(tokens)
        child_z = z
        if token >= 2:
            child[i] -= 1
        else:
            child.pop(i)
            child_z += 1
        options.append(
            canonical_recurrence(
                r - 1, tuple(sorted(child, reverse=True)), child_z
            )
        )
    if z:
        options.append(
            1
            ^ canonical_recurrence(
                r - 1, tuple(sorted(tokens, reverse=True)), z - 1
            )
        )
    return mex(options)


def run():
    ordered_recurrence.cache_clear()
    canonical_recurrence.cache_clear()
    failures = []
    direct = 0

    for x in range(21, 72):
        for r in range(x + 51):
            cases = (
                ((x, 21), 6, h21(x, r)),
                ((x, 20), 6, h20(x, r)),
                ((x, 21), 5, h5(x, 21, r)),
            )
            for tokens, z, expected in cases:
                left = ordered_recurrence(r, tokens, z)
                right = canonical_recurrence(
                    r, tuple(sorted(tokens, reverse=True)), z
                )
                direct += 1
                if left != right or left != expected:
                    failures.append(
                        ("direct", x, r, tokens, z, left, right, expected)
                    )

    signatures = mex_checks = odd_bounds = even_bounds = 0
    value2_locus = family_specialization = 0
    for x in range(21, 2001):
        observed_twos = set()
        for r in range(1, x + 28):
            actual = actual_signature(x, r)
            expected = expected_signature(x, r)
            signatures += 1
            if actual != expected:
                failures.append(("signature", x, r, actual, expected))
                continue
            value = mex(actual)
            mex_checks += 1
            if value != h21(x, r):
                failures.append(("mex", x, r, actual, value, h21(x, r)))
            if r % 2:
                odd_bounds += 1
                if not set(actual) <= {0, 1}:
                    failures.append(("odd-parent-bound", x, r, actual))
            else:
                even_bounds += 1
                if value > 1:
                    failures.append(("even-parent-bound", x, r, value))
            if value == 2:
                observed_twos.add(r)
        value2_locus += 1
        if observed_twos != twos21(x):
            failures.append(("value2-locus", x, sorted(observed_twos), sorted(twos21(x))))
        family_specialization += 1
        if twos21(x) != family_value2(x):
            failures.append(("three-family", x, sorted(twos21(x)), sorted(family_value2(x))))

    tail = 0
    for x in range(21, 2001):
        for offset in range(65):
            r = x + 28 + offset
            tail += 1
            if h21(x, r) != ((x + 21) % 2):
                failures.append(("tail", x, r, h21(x, r)))

    rng = random.Random(20261117)
    far_tail = 0
    for _ in range(2000):
        x = rng.randint(21, 100000)
        r = x + 28 + rng.randint(0, 100000)
        far_tail += 1
        if h21(x, r) != ((x + 21) % 2):
            failures.append(("far-tail", x, r, h21(x, r)))

    counts = {
        "direct_ordered_canonical_anchor": direct,
        "choice_signatures": signatures,
        "mex_identities": mex_checks,
        "odd_parent_upper_bound": odd_bounds,
        "even_parent_upper_bound": even_bounds,
        "value2_locus": value2_locus,
        "three_family_specialization": family_specialization,
        "tail": tail,
        "fixed_seed_far_tail": far_tail,
    }
    payload = {
        "target": "H(R;(x,21);6), x>=21, R>=0",
        "classification": "universal proof by signature table, Theorem T, general tail, and strong induction on R",
        "audit_scope": {
            "direct_x": [21, 71],
            "direct_r": "0 <= R < x+51",
            "signature_x": [21, 2000],
            "signature_r": "1 <= R <= x+27",
            "tail_x": [21, 2000],
            "tail_offsets": [0, 64],
            "far_tail_seed": 20261117,
            "far_tail_samples": far_tail,
        },
        "counts": counts,
        "total_checks": sum(counts.values()),
        "failures": failures,
        "all_pass": not failures,
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    payload["sha256_without_hash_field"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    output = Path(__file__).with_name("output")
    output.mkdir(parents=True, exist_ok=True)
    (output / "audit.json").write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "all_pass": payload["all_pass"],
        "total_checks": payload["total_checks"],
        "counts": counts,
        "failures": len(failures),
        "sha256_without_hash_field": payload["sha256_without_hash_field"],
    }, ensure_ascii=False, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
