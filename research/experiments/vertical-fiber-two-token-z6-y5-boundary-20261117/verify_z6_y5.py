#!/usr/bin/env python3
"""Independent finite audit for the proved two-token residual slice z=6, y=5.

The unbounded result is proved in report.md by R-strong induction from the
z=6,y=4 and z=5 anchors, the signature table, Theorem T, and the tail theorem.
This script checks the recurrence in two independent state representations,
the complete pre-tail signature table on a large x-range, and the tail.
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


def even(r: int, lo: int, hi: int) -> bool:
    return r % 2 == 0 and lo <= r <= hi


def exact_ordered(r: int, tokens: tuple[int, ...], z: int) -> int:
    """Order-preserving recurrence: token labels are never normalized."""
    return _exact_ordered(r, tokens, z)


@lru_cache(None)
def _exact_ordered(r: int, tokens: tuple[int, ...], z: int) -> int:
    if r == 0:
        return 0
    options = []
    for i, token in enumerate(tokens):
        child = list(tokens)
        if token >= 2:
            child[i] = token - 1
            options.append(_exact_ordered(r - 1, tuple(child), z))
        else:
            child.pop(i)
            options.append(_exact_ordered(r - 1, tuple(child), z + 1))
    if z >= 1:
        options.append(1 ^ _exact_ordered(r - 1, tokens, z - 1))
    return mex(options)


@lru_cache(None)
def exact_canonical(r: int, tokens: tuple[int, ...], z: int) -> int:
    """Independent multiset recurrence: sort after every token move."""
    if r == 0:
        return 0
    options = []
    for i, token in enumerate(tokens):
        child = list(tokens)
        if token >= 2:
            child[i] = token - 1
            options.append(exact_canonical(
                r - 1, tuple(sorted(child, reverse=True)), z
            ))
        else:
            child.pop(i)
            options.append(exact_canonical(
                r - 1, tuple(sorted(child, reverse=True)), z + 1
            ))
    if z >= 1:
        options.append(1 ^ exact_canonical(r - 1, tokens, z - 1))
    return mex(options)


def h5(x: int, y: int, r: int) -> int:
    """K0873: proved complete two-token z=5 formula."""
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
        p = even(r, 6, 2 * y + 4) or (r % 2 == 1 and 2 * y + 7 <= r <= s + 4) or r >= s + 6
    else:
        p = even(r, 6, 2 * y + 4) or (r % 2 == 1 and 2 * y + 7 <= r <= s + 5)
    return int(p)


def h6_y4(x: int, r: int) -> int:
    """K0880: proved complete z=6, y=4 slice."""
    if r == 0:
        return 0
    base = {1, 3, 5}
    if x == 4:
        t, p = base | {11}, r in {7, 9}
    elif x == 5:
        t, p = base, r in {7, 9} or r >= 11
    elif x == 6:
        t, p = base, r in {7, 9, 11}
    elif x == 7:
        t, p = base, r in {7, 9, 11} or r >= 13
    elif x == 8:
        t, p = base | {13}, r in {7, 9, 11}
    elif x == 9:
        t, p = base, r in {7, 9, 11} or r >= 13
    elif x == 10:
        t, p = base, r in {7, 9, 11, 13}
    elif x == 11:
        t = base | {15, 17, 19, 21}
        p = r in {7, 9, 11, 13} or even(r, 16, 20) or r >= 22
    elif x >= 12 and x % 2 == 0:
        t = base | {15}
        p = r in {7, 9, 11, 13} or even(r, 16, x + 10)
    else:
        t = base | {15}
        p = r in {7, 9, 11, 13} or even(r, 16, x + 9) or r >= x + 11
    return 2 if r in t else int(p)


def h6_y5(x: int, r: int) -> int:
    """Candidate closed form for the new z=6, y=5 theorem."""
    if r == 0:
        return 0
    base = {1, 3, 5}
    if x == 5:
        t, p = base | {13}, r in {7, 9, 11}
    elif x == 6:
        t, p = base, r in {7, 9, 11, 13} or r >= 14
    elif x == 7:
        t, p = base, r in {7, 9, 11, 13}
    elif x == 8:
        t, p = base, r in {7, 9, 11, 13} or r >= 15
    elif x == 9:
        t, p = base | {15}, r in {7, 9, 11, 13}
    elif x == 10:
        t, p = base, r in {7, 9, 11, 13} or r >= 15
    elif x == 11:
        t, p = base, r in {7, 9, 11, 13, 15}
    elif x >= 12 and x % 2 == 0:
        t = base | ({17, 19, 21, 23} if x == 12 else {17})
        p = (r in {7, 9, 11, 13, 15}
             or even(r, 18, x + 10)
             or r >= x + 12)
    else:
        t = base | {17}
        p = (r in {7, 9, 11, 13, 15}
             or even(r, 18, x + 11))
    return 2 if r in t else int(p)


# Complete A/B/C signature table on 1 <= R < x+12.
_SMALL_SIGNATURES = {
    5: {
        1: [(1, 5, "01"), (7, 11, "0"), (13, 13, "01"), (15, 15, "1")],
        0: [(2, 6, "23"), (8, 16, "1")],
    },
    6: {
        1: [(1, 5, "01"), (7, 17, "0")],
        0: [(2, 6, "23"), (8, 12, "1"), (14, 14, "023"), (16, 16, "0")],
    },
    7: {
        1: [(1, 5, "01"), (7, 13, "0"), (15, 17, "1")],
        0: [(2, 6, "23"), (8, 18, "1")],
    },
    8: {
        1: [(1, 5, "01"), (7, 19, "0")],
        0: [(2, 6, "23"), (8, 12, "1"), (14, 14, "12"), (16, 18, "0")],
    },
    9: {
        1: [(1, 5, "01"), (7, 13, "0"), (15, 15, "01"), (17, 19, "1")],
        0: [(2, 6, "23"), (8, 20, "1")],
    },
    10: {
        1: [(1, 5, "01"), (7, 21, "0")],
        0: [(2, 6, "23"), (8, 14, "1"), (16, 16, "023"), (18, 20, "0")],
    },
    11: {
        1: [(1, 5, "01"), (7, 15, "0"), (17, 21, "1")],
        0: [(2, 6, "23"), (8, 14, "1"), (16, 22, "123")],
    },
    12: {
        1: [(1, 5, "01"), (7, 15, "0"), (17, 23, "01")],
        0: [(2, 6, "23"), (8, 14, "1"), (16, 16, "123"), (18, 22, "0")],
    },
}


def _parse_signature(digits: str) -> set[int]:
    return {int(ch) for ch in digits}


def expected_signature(x: int, r: int) -> set[int]:
    if r == 0:
        return set()
    parity = r % 2
    if x in _SMALL_SIGNATURES:
        for lo, hi, digits in _SMALL_SIGNATURES[x][parity]:
            if lo <= r <= hi:
                return _parse_signature(digits)
        return set()
    if parity:
        if r <= 5:
            return {0, 1}
        if r <= 15:
            return {0}
        if r == 17:
            return {0, 1}
        upper = x + 11 if x % 2 == 0 else x + 10
        if 19 <= r <= upper:
            return {1}
        return set()
    if 2 <= r <= 6:
        return {2, 3}
    if 8 <= r <= 14:
        return {1}
    if r == 16:
        return {1, 2, 3}
    if x == 13:
        return {0, 2} if 18 <= r <= 24 else set()
    if r == 18:
        return {0, 2}
    upper = x + 10 if x % 2 == 0 else x + 11
    if 20 <= r <= upper:
        return {0}
    return set()


def predicted_value2_positions(x: int) -> set[int]:
    """Specialization of the existing three-family conjecture at y=5,z=6."""
    extra = set()
    d = x - 5
    if d <= 6 and (6 + d) % 4 == 2 and 5 >= (6 - d) // 2:
        extra.add(10 + (6 + d) // 2)
    if d == 7:
        extra.update(10 + delta for delta in range(7, 14, 2))
    elif d >= 8:
        extra.add(17)
    return {1, 3, 5} | extra


def run_audit() -> dict:
    failures = []
    direct_checks = 0
    for x in range(5, 31):
        for r in range(0, x + 21):
            cases = (
                (6, (x, 5), lambda: h6_y5(x, r)),
                (6, (x, 4), lambda: h6_y4(x, r)),
                (5, (x, 5), lambda: h5(x, 5, r)),
            )
            for z, tokens, formula in cases:
                ordered = exact_ordered(r, tokens, z)
                canonical = exact_canonical(r, tuple(sorted(tokens, reverse=True)), z)
                expected = formula()
                direct_checks += 1
                if ordered != canonical or ordered != expected:
                    failures.append({
                        "kind": "direct-recurrence",
                        "x": x, "r": r, "z": z, "tokens": tokens,
                        "ordered": ordered, "canonical": canonical,
                        "formula": expected,
                    })

    signature_checks = 0
    mex_checks = 0
    odd_option_bound_checks = 0
    even_parent_bound_checks = 0
    family_position_checks = 0
    for x in range(5, 2001):
        for r in range(1, x + 12):
            if x == 5:
                a = h6_y4(5, r - 1)
                b = h6_y4(5, r - 1)
            else:
                a = h6_y5(x - 1, r - 1)
                b = h6_y4(x, r - 1)
            c = 1 ^ h5(x, 5, r - 1)
            options = {a, b, c}
            signature = expected_signature(x, r)
            signature_checks += 1
            if options != signature:
                failures.append({
                    "kind": "signature",
                    "x": x, "r": r,
                    "actual": sorted(options),
                    "expected": sorted(signature),
                })
            value = mex(options)
            mex_checks += 1
            if value != h6_y5(x, r):
                failures.append({
                    "kind": "mex",
                    "x": x, "r": r,
                    "options": sorted(options),
                    "actual": value,
                    "formula": h6_y5(x, r),
                })
            if r % 2:
                odd_option_bound_checks += 1
                if not options <= {0, 1}:
                    failures.append({
                        "kind": "odd-parent-option-bound",
                        "x": x, "r": r, "options": sorted(options),
                    })
            else:
                even_parent_bound_checks += 1
                if h6_y5(x, r) > 1:
                    failures.append({
                        "kind": "even-parent-bound",
                        "x": x, "r": r, "value": h6_y5(x, r),
                    })
        actual_t = {
            r for r in range(1, x + 12) if h6_y5(x, r) == 2
        }
        predicted_t = predicted_value2_positions(x)
        family_position_checks += 1
        if actual_t != predicted_t:
            failures.append({
                "kind": "three-family-specialization",
                "x": x,
                "actual": sorted(actual_t),
                "predicted": sorted(predicted_t),
            })

    tail_checks = 0
    for x in range(5, 2001):
        tail_value = (x + 5) % 2
        for offset in range(65):
            r = x + 12 + offset
            tail_checks += 1
            if h6_y5(x, r) != tail_value:
                failures.append({
                    "kind": "tail",
                    "x": x, "r": r,
                    "actual": h6_y5(x, r),
                    "expected": tail_value,
                })

    rng = random.Random(20261117)
    random_tail_checks = 0
    for _ in range(2000):
        x = rng.randint(5, 100000)
        r = x + 12 + rng.randint(0, 100000)
        random_tail_checks += 1
        if h6_y5(x, r) != (x + 5) % 2:
            failures.append({
                "kind": "random-tail",
                "x": x, "r": r,
                "actual": h6_y5(x, r),
                "expected": (x + 5) % 2,
            })

    counts = {
        "direct_recurrence_formula_anchor_checks": direct_checks,
        "option_signature_checks": signature_checks,
        "mex_identity_checks": mex_checks,
        "odd_parent_option_bound_checks": odd_option_bound_checks,
        "even_parent_value_bound_checks": even_parent_bound_checks,
        "three_family_value2_specialization_checks": family_position_checks,
        "tail_checks": tail_checks,
        "fixed_seed_random_tail_checks": random_tail_checks,
    }
    audit = {
        "schema": "two-token-z6-y5-audit-v1",
        "claim": "H(R;(x,5);6) is given by the complete formula for all x>=5,R>=0",
        "classification": "finite-independent-audit-not-proof",
        "counts": counts,
        "total_checks": sum(counts.values()),
        "ordered_engine_cache": {
            "hits": _exact_ordered.cache_info().hits,
            "misses": _exact_ordered.cache_info().misses,
        },
        "canonical_engine_cache": {
            "hits": exact_canonical.cache_info().hits,
            "misses": exact_canonical.cache_info().misses,
        },
        "seed": 20261117,
        "failures": failures,
        "pass": not failures,
    }
    encoded = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    audit["sha256_without_hash_field"] = hashlib.sha256(encoded.encode("utf-8")).hexdigest()
    return audit


if __name__ == "__main__":
    result = run_audit()
    out = Path(__file__).resolve().parent / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    if not result["pass"]:
        raise SystemExit(1)