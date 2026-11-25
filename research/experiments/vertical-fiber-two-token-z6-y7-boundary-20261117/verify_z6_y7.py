#!/usr/bin/env python3
"""Independent finite audit for the proved two-token residual slice z=6, y=7.

The unbounded result is proved in report.md by R-strong induction from the
z=5 and z=6,y=6 anchors, the complete A/B/C signature table, Theorem T,
and the general tail theorem. This script independently checks the raw
recurrence in two state representations and the published closed forms.
"""
from __future__ import annotations

import hashlib
import json
import random
from functools import lru_cache
from pathlib import Path


def mex(values: set[int] | list[int]) -> int:
    seen = set(values)
    n = 0
    while n in seen:
        n += 1
    return n


def even(r: int, lo: int, hi: int) -> bool:
    return r % 2 == 0 and lo <= r <= hi


def odd(r: int, lo: int, hi: int) -> bool:
    return r % 2 == 1 and lo <= r <= hi


@lru_cache(None)
def exact_ordered(r: int, tokens: tuple[int, ...], z: int) -> int:
    """Raw recurrence preserving the token order."""
    if r == 0:
        return 0
    options = []
    for i, token in enumerate(tokens):
        child = list(tokens)
        if token >= 2:
            child[i] = token - 1
            options.append(exact_ordered(r - 1, tuple(child), z))
        else:
            child.pop(i)
            options.append(exact_ordered(r - 1, tuple(child), z + 1))
    if z >= 1:
        options.append(1 ^ exact_ordered(r - 1, tokens, z - 1))
    return mex(options)


@lru_cache(None)
def exact_canonical(r: int, tokens: tuple[int, ...], z: int) -> int:
    """Independent recurrence sorting the token multiset after every move."""
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
        p = (even(r, 6, 2 * y + 4)
             or odd(r, 2 * y + 7, s + 4)
             or r >= s + 6)
    else:
        p = even(r, 6, 2 * y + 4) or odd(r, 2 * y + 7, s + 5)
    return int(p)


def h6_y6(x: int, r: int) -> int:
    """K0885: proved complete z=6, y=6 formula."""
    if r == 0:
        return 0
    base = {1, 3, 5}
    if x == 6:
        t, p = base | {15}, r in {7, 9, 11, 13}
    elif x == 7:
        t, p = base, r in {7, 9, 11, 13, 15} or r >= 16
    elif x == 8:
        t, p = base, r in {7, 9, 11, 13, 15}
    elif x == 9:
        t, p = base, r in {7, 9, 11, 13, 15} or r >= 17
    elif x == 10:
        t, p = base | {17}, r in {7, 9, 11, 13, 15}
    elif x == 11:
        t, p = base, r in {7, 9, 11, 13, 15, 17} or r >= 18
    elif x == 12:
        t, p = base, r in {7, 9, 11, 13, 15, 17}
    elif x >= 13 and x % 2 == 1:
        t = base | ({19, 21, 23, 25} if x == 13 else {19})
        p = (r in {7, 9, 11, 13, 15, 17}
             or even(r, 20, x + 12)
             or r >= x + 13)
    else:
        t = base | {19}
        p = r in {7, 9, 11, 13, 15, 17} or even(r, 20, x + 12)
    return 2 if r in t else int(p)


def h6_y7(x: int, r: int) -> int:
    """Candidate complete formula for the new z=6, y=7 theorem."""
    if r == 0:
        return 0
    base = {1, 3, 5}
    if x == 7:
        t, p = base | {17}, odd(r, 7, 15)
    elif x == 8:
        t, p = base, odd(r, 7, 17) or r >= 18
    elif x == 9:
        t, p = base, odd(r, 7, 17)
    elif x == 10:
        t, p = base, odd(r, 7, 17) or r >= 19
    elif x == 11:
        t, p = base | {19}, odd(r, 7, 17)
    elif x == 12:
        t, p = base, odd(r, 7, 19) or r >= 20
    elif x == 13:
        t, p = base, odd(r, 7, 19)
    elif x >= 14 and x % 2 == 0:
        t = base | ({21, 23, 25, 27} if x == 14 else {21})
        p = odd(r, 7, 19) or even(r, 22, x + 12) or r >= x + 14
    else:
        t = base | {21}
        p = odd(r, 7, 19) or even(r, 22, x + 13)
    return 2 if r in t else int(p)


_SMALL_SIGNATURES = {
    7: {
        1: [(1, 5, "01"), (7, 15, "0"), (17, 17, "01"), (19, 19, "1")],
        0: [(2, 6, "23"), (8, 20, "1")],
    },
    8: {
        1: [(1, 5, "01"), (7, 21, "0")],
        0: [(2, 6, "23"), (8, 16, "1"), (18, 18, "023"), (20, 20, "0")],
    },
    9: {
        1: [(1, 5, "01"), (7, 17, "0"), (19, 21, "1")],
        0: [(2, 6, "23"), (8, 22, "1")],
    },
    10: {
        1: [(1, 5, "01"), (7, 23, "0")],
        0: [(2, 6, "23"), (8, 16, "1"), (18, 18, "12"), (20, 22, "0")],
    },
    11: {
        1: [(1, 5, "01"), (7, 17, "0"), (19, 19, "01"), (21, 23, "1")],
        0: [(2, 6, "23"), (8, 24, "1")],
    },
    12: {
        1: [(1, 5, "01"), (7, 25, "0")],
        0: [(2, 6, "23"), (8, 18, "1"), (20, 20, "023"), (22, 24, "0")],
    },
    13: {
        1: [(1, 5, "01"), (7, 19, "0"), (21, 25, "1")],
        0: [(2, 6, "23"), (8, 18, "1"), (20, 26, "123")],
    },
    14: {
        1: [(1, 5, "01"), (7, 19, "0"), (21, 27, "01")],
        0: [(2, 6, "23"), (8, 18, "1"), (20, 20, "123"), (22, 26, "0")],
    },
    15: {
        1: [(1, 5, "01"), (7, 19, "0"), (21, 21, "01"), (23, 27, "1")],
        0: [(2, 6, "23"), (8, 18, "1"), (20, 20, "123"), (22, 28, "02")],
    },
}


def expected_signature(x: int, r: int) -> set[int]:
    if x >= 16:
        upper_odd = x + 13 if x % 2 == 0 else x + 12
        upper_even = x + 12 if x % 2 == 0 else x + 13
        rows = {
            1: [(1, 5, "01"), (7, 19, "0"), (21, 21, "01"),
                (23, upper_odd, "1")],
            0: [(2, 6, "23"), (8, 18, "1"), (20, 20, "123"),
                (22, 22, "02"), (24, upper_even, "0")],
        }
    else:
        rows = _SMALL_SIGNATURES[x]
    for lo, hi, digits in rows[r % 2]:
        if lo <= r <= hi:
            return {int(ch) for ch in digits}
    return set()


def actual_signature(x: int, r: int) -> set[int]:
    # At x=7 the two token-reduction moves both lead to the (7,6) child.
    a = h6_y6(7, r - 1) if x == 7 else h6_y7(x - 1, r - 1)
    b = h6_y6(x, r - 1)
    c = 1 ^ h5(x, 7, r - 1)
    return {a, b, c}


def predicted_value2_positions(x: int) -> set[int]:
    """Specialization of K0832's three-family conjecture at y=7,z=6."""
    d = x - 7
    extra = set()
    if d <= 6 and d % 2 == 0 and (6 + d) % 4 == 2 and 7 >= (6 - d) // 2:
        extra.add(14 + (6 + d) // 2)
    if d == 7:
        extra.update(14 + delta for delta in range(7, 14, 2))
    elif d >= 8:
        extra.add(21)
    return {1, 3, 5} | extra


def run_audit() -> dict:
    failures = []
    direct_checks = 0
    for x in range(7, 46):
        for r in range(0, x + 21):
            cases = (
                (6, (x, 7), h6_y7(x, r)),
                (6, (x, 6), h6_y6(x, r)),
                (5, (x, 7), h5(x, 7, r)),
            )
            for z, tokens, formula in cases:
                ordered = exact_ordered(r, tokens, z)
                canonical = exact_canonical(
                    r, tuple(sorted(tokens, reverse=True)), z
                )
                direct_checks += 1
                if ordered != canonical or ordered != formula:
                    failures.append({
                        "kind": "direct-recurrence",
                        "x": x, "r": r, "z": z, "tokens": tokens,
                        "ordered": ordered, "canonical": canonical,
                        "formula": formula,
                    })

    signature_checks = 0
    mex_checks = 0
    odd_bound_checks = 0
    even_bound_checks = 0
    family_checks = 0
    for x in range(7, 2001):
        for r in range(1, x + 14):
            options = actual_signature(x, r)
            signature = expected_signature(x, r)
            signature_checks += 1
            if options != signature:
                failures.append({
                    "kind": "signature", "x": x, "r": r,
                    "actual": sorted(options), "expected": sorted(signature),
                })
            value = mex(options)
            mex_checks += 1
            if value != h6_y7(x, r):
                failures.append({
                    "kind": "mex", "x": x, "r": r,
                    "options": sorted(options), "actual": value,
                    "formula": h6_y7(x, r),
                })
            if r % 2:
                odd_bound_checks += 1
                if not options <= {0, 1}:
                    failures.append({
                        "kind": "odd-parent-option-bound",
                        "x": x, "r": r, "options": sorted(options),
                    })
            else:
                even_bound_checks += 1
                if h6_y7(x, r) > 1:
                    failures.append({
                        "kind": "even-parent-value-bound",
                        "x": x, "r": r, "value": h6_y7(x, r),
                    })
        actual_t = {
            r for r in range(1, x + 14) if h6_y7(x, r) == 2
        }
        predicted_t = predicted_value2_positions(x)
        family_checks += 1
        if actual_t != predicted_t:
            failures.append({
                "kind": "three-family-specialization",
                "x": x, "actual": sorted(actual_t),
                "predicted": sorted(predicted_t),
            })

    tail_checks = 0
    for x in range(7, 2001):
        for offset in range(65):
            r = x + 14 + offset
            tail_checks += 1
            if h6_y7(x, r) != (x + 7) % 2:
                failures.append({
                    "kind": "tail", "x": x, "r": r,
                    "actual": h6_y7(x, r), "expected": (x + 7) % 2,
                })

    rng = random.Random(20261117)
    random_tail_checks = 0
    for _ in range(2000):
        x = rng.randint(7, 100000)
        r = x + 14 + rng.randint(0, 100000)
        random_tail_checks += 1
        if h6_y7(x, r) != (x + 7) % 2:
            failures.append({
                "kind": "random-tail", "x": x, "r": r,
                "actual": h6_y7(x, r), "expected": (x + 7) % 2,
            })

    counts = {
        "direct_two_engine_formula_anchor_checks": direct_checks,
        "option_signature_checks": signature_checks,
        "mex_identity_checks": mex_checks,
        "odd_parent_option_bound_checks": odd_bound_checks,
        "even_parent_value_bound_checks": even_bound_checks,
        "three_family_value2_specialization_checks": family_checks,
        "tail_checks": tail_checks,
        "fixed_seed_random_tail_checks": random_tail_checks,
    }
    audit = {
        "schema": "two-token-z6-y7-audit-v1",
        "claim": "H(R;(x,7);6) is given by the complete formula for all x>=7,R>=0",
        "classification": "finite-independent-audit-not-proof",
        "counts": counts,
        "total_checks": sum(counts.values()),
        "seed": 20261117,
        "failures": failures,
        "pass": not failures,
    }
    encoded = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    audit["sha256_without_hash_field"] = hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()
    return audit


def main() -> None:
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
