#!/usr/bin/env python3
"""Independent finite audit for the universally proved z=6, y=20 slice."""
from __future__ import annotations

import hashlib
import json
import random
from functools import lru_cache


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
        one = even(r, 6, 2 * y + 4) or odd(r, 2 * y + 7, s + 4) or r >= s + 6
    else:
        one = even(r, 6, 2 * y + 4) or odd(r, 2 * y + 7, s + 5)
    return int(one)


def h19(x, r):
    if r == 0:
        return 0
    twos = {1, 3, 5}
    if x == 19:
        twos.add(41)
    elif x == 23:
        twos.add(43)
    elif x == 26:
        twos.update({45, 47, 49, 51})
    elif x >= 27:
        twos.add(45)
    if r in twos:
        return 2
    if x == 19:
        one = odd(r, 7, 39)
    elif x == 20:
        one = odd(r, 7) or even(r, 42)
    elif x == 21:
        one = odd(r, 7, 41)
    elif x == 22:
        one = odd(r, 7) or even(r, 44)
    elif x == 23:
        one = odd(r, 7, 41)
    elif x == 24:
        one = odd(r, 7) or even(r, 44)
    elif x == 25:
        one = odd(r, 7, 43)
    elif x % 2 == 0:
        one = odd(r, 7, 43) or even(r, 46, x + 24) or r >= x + 26
    else:
        one = odd(r, 7, 43) or even(r, 46, x + 25)
    return int(one)


def twos20(x):
    result = {1, 3, 5}
    if x == 20:
        result.add(43)
    elif x == 24:
        result.add(45)
    elif x == 27:
        result.update({47, 49, 51, 53})
    elif x >= 28:
        result.add(47)
    return result


def ones20(x, r):
    if x == 20:
        return odd(r, 7, 41)
    if x == 21:
        return odd(r, 7) or even(r, 44)
    if x == 22:
        return odd(r, 7, 43)
    if x == 23:
        return odd(r, 7) or even(r, 46)
    if x == 24:
        return odd(r, 7, 43)
    if x == 25:
        return odd(r, 7) or even(r, 46)
    if x == 26:
        return odd(r, 7, 45)
    if x % 2:
        return odd(r, 7, 45) or even(r, 48) or odd(r, x + 28)
    return odd(r, 7, 45) or even(r, 48, x + 26)


def h20(x, r):
    if r in twos20(x):
        return 2
    if ones20(x, r):
        return 1
    return 0


def three_family20(x):
    """K0832 three-family conjecture specialized to z=6,y=20."""
    d = x - 20
    result = {1, 3, 5}
    if d <= 6 and d % 2 == 0 and (6 + d) % 4 == 2:
        result.add(40 + (6 + d) // 2)
    elif d == 7:
        result.update({47, 49, 51, 53})
    elif d >= 8:
        result.add(47)
    return result


def signature_expected(x, r):
    odd_parent = r % 2 == 1
    rows = {
        20: (
            [(1, 5, "01"), (7, 41, "0"), (43, 43, "01"), (45, 45, "1")],
            [(2, 6, "23"), (8, 46, "1")],
        ),
        21: (
            [(1, 5, "01"), (7, 47, "0")],
            [(2, 6, "23"), (8, 42, "1"), (44, 44, "023"), (46, 46, "0")],
        ),
        22: (
            [(1, 5, "01"), (7, 43, "0"), (45, 47, "1")],
            [(2, 6, "23"), (8, 48, "1")],
        ),
        23: (
            [(1, 5, "01"), (7, 49, "0")],
            [(2, 6, "23"), (8, 42, "1"), (44, 44, "12"), (46, 48, "0")],
        ),
        24: (
            [(1, 5, "01"), (7, 43, "0"), (45, 45, "01"), (47, 49, "1")],
            [(2, 6, "23"), (8, 50, "1")],
        ),
        25: (
            [(1, 5, "01"), (7, 51, "0")],
            [(2, 6, "23"), (8, 44, "1"), (46, 46, "023"), (48, 50, "0")],
        ),
        26: (
            [(1, 5, "01"), (7, 45, "0"), (47, 51, "1")],
            [(2, 6, "23"), (8, 44, "1"), (46, 52, "123")],
        ),
        27: (
            [(1, 5, "01"), (7, 45, "0"), (47, 53, "01")],
            [(2, 6, "23"), (8, 44, "1"), (46, 46, "123"), (48, 52, "0")],
        ),
        28: (
            [(1, 5, "01"), (7, 45, "0"), (47, 47, "01"), (49, 53, "1")],
            [(2, 6, "23"), (8, 44, "1"), (46, 46, "123"), (48, 54, "02")],
        ),
    }
    if x in rows:
        intervals = rows[x][0 if odd_parent else 1]
    elif odd_parent:
        upper = x + 26 if x % 2 else x + 25
        intervals = [
            (1, 5, "01"),
            (7, 45, "0"),
            (47, 47, "01"),
            (49, upper, "1"),
        ]
    else:
        upper = x + 25 if x % 2 else x + 26
        intervals = [
            (2, 6, "23"),
            (8, 44, "1"),
            (46, 46, "123"),
            (48, 48, "02"),
            (50, upper, "0"),
        ]
    for lo, hi, digits in intervals:
        if lo <= r <= hi and (r - lo) % 2 == 0:
            return tuple(int(digit) for digit in digits)
    return None


def actual_signature(x, parent_r):
    child_r = parent_r - 1
    if x == 20:
        a = h19(20, child_r)
    else:
        a = h20(x - 1, child_r)
    b = h19(x, child_r)
    c = 1 ^ h5(x, 20, child_r)
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

    for x in range(20, 71):
        for r in range(x + 51):
            cases = (
                ((x, 20), 6, h20(x, r)),
                ((x, 19), 6, h19(x, r)),
                ((x, 20), 5, h5(x, 20, r)),
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
    for x in range(20, 2001):
        observed_twos = set()
        for r in range(1, x + 27):
            actual = actual_signature(x, r)
            expected = signature_expected(x, r)
            signatures += 1
            if actual != expected:
                failures.append(("signature", x, r, actual, expected))
            value = mex(actual)
            mex_checks += 1
            if value != h20(x, r):
                failures.append(("mex", x, r, actual, value, h20(x, r)))
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
        if observed_twos != twos20(x):
            failures.append(("value2-locus", x, sorted(observed_twos), sorted(twos20(x))))
        family_specialization += 1
        if twos20(x) != three_family20(x):
            failures.append(("three-family", x, sorted(twos20(x)), sorted(three_family20(x))))

    tail = 0
    for x in range(20, 2001):
        for offset in range(65):
            r = x + 27 + offset
            tail += 1
            if h20(x, r) != ((x + 20) % 2):
                failures.append(("tail", x, r, h20(x, r)))

    rng = random.Random(20261118)
    far_tail = 0
    for _ in range(2000):
        x = rng.randint(20, 100000)
        r = x + 27 + rng.randint(0, 100000)
        far_tail += 1
        if h20(x, r) != ((x + 20) % 2):
            failures.append(("far-tail", x, r, h20(x, r)))

    counts = {
        "direct_ordered_canonical_formula_anchors": direct,
        "option_signatures": signatures,
        "mex_identity": mex_checks,
        "odd_parent_bounds": odd_bounds,
        "even_parent_bounds": even_bounds,
        "value2_locus": value2_locus,
        "three_family_specialization": family_specialization,
        "tail": tail,
        "fixed_seed_far_tail": far_tail,
    }
    payload = {
        "schema": "two-token-z6-y20-audit-v1",
        "claim": "H(R;(x,20);6) is given by the complete formula for all x>=20,R>=0",
        "classification": (
            "universal proof by the A/B/C option-signature cases, Theorem T, "
            "the general tail theorem, and strong induction on R; finite checks "
            "are independent audits only"
        ),
        "counts": counts,
        "total_checks": sum(counts.values()),
        "mismatches": len(failures),
        "first_failures": failures[:20],
        "cache": {
            "ordered": ordered_recurrence.cache_info()._asdict(),
            "canonical": canonical_recurrence.cache_info()._asdict(),
        },
    }
    raw = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    payload["sha256_without_hash_field"] = hashlib.sha256(raw).hexdigest()
    return payload


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(0 if result["mismatches"] == 0 else 1)
