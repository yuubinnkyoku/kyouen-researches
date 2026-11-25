#!/usr/bin/env python3
"""Independent finite audit for the proved two-token residual slice z=6, y=15.

The universal theorem is proved in report.md by the A/B/C signature partition,
Theorem T, the general tail theorem, and strong induction on R. This script is
a finite audit, not the source of the universal quantifiers.
"""
from __future__ import annotations

import hashlib
import json
import random
from functools import lru_cache
from pathlib import Path


def mex(values):
    seen = set(values)
    g = 0
    while g in seen:
        g += 1
    return g


def odd(r, lo, hi=None):
    return r >= lo and (hi is None or r <= hi) and r % 2 == 1


def even(r, lo, hi=None):
    return r >= lo and (hi is None or r <= hi) and r % 2 == 0


def h5(x, y, r):
    """K0873: proved z=5 two-token formula."""
    if r == 0:
        return 0
    s, d = x + y, x - y
    if d == 0:
        t = {1, 3, 5}
    elif d == 1:
        t = {1, 3, 5, 2 * y + 3}
    elif d == 2:
        t = {1, 3, 5}
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
        p = even(r, 6, s + 2)
    elif d == 1:
        p = even(r, 6, s + 3) or r >= s + 4
    elif d == 2:
        p = even(r, 6, s)
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


def h6_y14(x, r):
    """K0901: proved z=6, y=14 boundary slice."""
    if r == 0:
        return 0
    t = {1, 3, 5}
    if x == 14:
        t.add(31)
    elif x == 18:
        t.add(33)
    elif x == 21:
        t.update({35, 37, 39, 41})
    elif x >= 22:
        t.add(35)
    if r in t:
        return 2

    if x == 14:
        p = odd(r, 7, 29)
    elif x == 15:
        p = odd(r, 7, 35) or even(r, 32, 34) or r >= 36
    elif x == 16:
        p = odd(r, 7, 31)
    elif x == 17:
        p = odd(r, 7, 37) or even(r, 34, 36) or r >= 38
    elif x == 18:
        p = odd(r, 7, 31)
    elif x == 19:
        p = odd(r, 7, 39) or even(r, 34, 38) or r >= 40
    elif x == 20:
        p = odd(r, 7, 33)
    elif x == 21:
        p = odd(r, 7, 33) or even(r, 36, 40) or r >= 42
    elif x % 2 == 0:
        p = odd(r, 7, 33) or even(r, 36, x + 20)
    else:
        p = odd(r, 7, 33) or even(r, 36, x + 19) or r >= x + 21
    return int(p)


def h6_y15(x, r):
    """Candidate closed formula proved in report.md."""
    if r == 0:
        return 0
    t = {1, 3, 5}
    if x == 15:
        t.add(33)
    elif x == 19:
        t.add(35)
    elif x == 22:
        t.update({37, 39, 41, 43})
    elif x >= 23:
        t.add(37)
    if r in t:
        return 2

    if x == 15:
        p = odd(r, 7, 31)
    elif x == 16:
        p = odd(r, 7, 37) or even(r, 34, 36) or r >= 38
    elif x == 17:
        p = odd(r, 7, 33)
    elif x == 18:
        p = odd(r, 7, 39) or even(r, 36, 38) or r >= 40
    elif x == 19:
        p = odd(r, 7, 33)
    elif x == 20:
        p = odd(r, 7, 41) or even(r, 36, 40) or r >= 42
    elif x == 21:
        p = odd(r, 7, 35)
    elif x == 22:
        p = odd(r, 7, 35) or even(r, 38, 42) or r >= 44
    elif x % 2:
        p = odd(r, 7, 35) or even(r, 38, x + 21)
    else:
        p = odd(r, 7, 35) or even(r, 38, x + 20) or r >= x + 22
    return int(p)


@lru_cache(None)
def ordered(r, tokens, z):
    """Direct recurrence retaining token order."""
    if r == 0:
        return 0
    options = []
    for i, token in enumerate(tokens):
        child = list(tokens)
        if token >= 2:
            child[i] = token - 1
            child_z = z
        else:
            child.pop(i)
            child_z = z + 1
        options.append(ordered(r - 1, tuple(child), child_z))
    if z >= 1:
        options.append(1 ^ ordered(r - 1, tokens, z - 1))
    return mex(options)


@lru_cache(None)
def canonical(r, tokens, z):
    """Independent recurrence sorting the token multiset after every move."""
    if r == 0:
        return 0
    options = []
    for i, token in enumerate(tokens):
        child = list(tokens)
        if token >= 2:
            child[i] = token - 1
            child_z = z
        else:
            child.pop(i)
            child_z = z + 1
        options.append(canonical(r - 1, tuple(sorted(child, reverse=True)), child_z))
    if z >= 1:
        options.append(1 ^ canonical(r - 1, tuple(sorted(tokens, reverse=True)), z - 1))
    return mex(options)


def actual_signature(x, r):
    if x == 15:
        a = b = h6_y14(15, r - 1)  # A and B coincide after sorting.
    else:
        a = h6_y15(x - 1, r - 1)
        b = h6_y14(x, r - 1)
    c = 1 ^ h5(x, 15, r - 1)
    return tuple(sorted({a, b, c}))


def expected_signature(x, r):
    """The explicit signature partition printed in report.md."""
    if x == 15:
        rows = ([(1, 5, "01"), (7, 31, "0"), (33, 33, "01"), (35, 35, "1")]
                if r % 2 else [(2, 6, "23"), (8, 36, "1")])
    elif x == 16:
        rows = ([(1, 5, "01"), (7, 37, "0")]
                if r % 2 else [(2, 6, "23"), (8, 32, "1"),
                               (34, 34, "023"), (36, 36, "0")])
    elif x == 17:
        rows = ([(1, 5, "01"), (7, 33, "0"), (35, 37, "1")]
                if r % 2 else [(2, 6, "23"), (8, 38, "1")])
    elif x == 18:
        rows = ([(1, 5, "01"), (7, 39, "0")]
                if r % 2 else [(2, 6, "23"), (8, 32, "1"),
                               (34, 34, "12"), (36, 38, "0")])
    elif x == 19:
        rows = ([(1, 5, "01"), (7, 33, "0"), (35, 35, "01"), (37, 39, "1")]
                if r % 2 else [(2, 6, "23"), (8, 40, "1")])
    elif x == 20:
        rows = ([(1, 5, "01"), (7, 41, "0")]
                if r % 2 else [(2, 6, "23"), (8, 34, "1"),
                               (36, 36, "023"), (38, 40, "0")])
    elif x == 21:
        rows = ([(1, 5, "01"), (7, 35, "0"), (37, 41, "1")]
                if r % 2 else [(2, 6, "23"), (8, 34, "1"), (36, 42, "123")])
    elif x == 22:
        rows = ([(1, 5, "01"), (7, 35, "0"), (37, 43, "01")]
                if r % 2 else [(2, 6, "23"), (8, 34, "1"),
                               (36, 36, "123"), (38, 42, "0")])
    elif x == 23:
        rows = ([(1, 5, "01"), (7, 35, "0"), (37, 37, "01"), (39, 43, "1")]
                if r % 2 else [(2, 6, "23"), (8, 34, "1"),
                               (36, 36, "123"), (38, 44, "02")])
    else:
        u = x + 20 if x % 2 else x + 21
        v = x + 21 if x % 2 else x + 20
        rows = ([(1, 5, "01"), (7, 35, "0"), (37, 37, "01"), (39, u, "1")]
                if r % 2 else
                [(2, 6, "23"), (8, 34, "1"), (36, 36, "123"),
                 (38, 38, "02"), (40, v, "0")])
    for lo, hi, digits in rows:
        if lo <= r <= hi and (r - lo) % 2 == 0:
            return tuple(int(ch) for ch in digits)
    return ()


def expected_value2(x):
    t = {1, 3, 5}
    if x == 15:
        t.add(33)
    elif x == 19:
        t.add(35)
    elif x == 22:
        t.update({37, 39, 41, 43})
    elif x >= 23:
        t.add(37)
    return t


def family_value2(x):
    """K0832's three-family conjecture specialized to z=6, y=15."""
    d = x - 15
    t = {1, 3, 5}
    if d in (0, 4):
        t.add(30 + (6 + d) // 2)
    elif d == 7:
        t.update({37, 39, 41, 43})
    elif d >= 8:
        t.add(37)
    return t


def run_audit():
    failures = []
    direct = 0
    for x in range(15, 71):
        for r in range(x + 61):
            cases = (
                (6, (x, 15), h6_y15(x, r)),
                (6, (x, 14), h6_y14(x, r)),
                (5, (x, 15), h5(x, 15, r)),
            )
            for z, tokens, formula in cases:
                a = ordered(r, tokens, z)
                b = canonical(r, tuple(sorted(tokens, reverse=True)), z)
                direct += 1
                if a != b or a != formula:
                    failures.append({
                        "kind": "direct", "x": x, "r": r, "z": z,
                        "tokens": tokens, "ordered": a, "canonical": b,
                        "formula": formula,
                    })

    signatures = mex_checks = odd_bounds = even_bounds = 0
    locus_checks = family_checks = 0
    for x in range(15, 2001):
        observed = set()
        for r in range(1, x + 22):
            actual = actual_signature(x, r)
            expected = expected_signature(x, r)
            signatures += 1
            if actual != expected:
                failures.append({
                    "kind": "signature", "x": x, "r": r,
                    "actual": actual, "expected": expected,
                })
            value = mex(actual)
            mex_checks += 1
            if value != h6_y15(x, r):
                failures.append({
                    "kind": "mex", "x": x, "r": r,
                    "actual": value, "formula": h6_y15(x, r),
                })
            if value == 2:
                observed.add(r)
            if r % 2:
                odd_bounds += 1
                if not set(actual).issubset({0, 1}):
                    failures.append({
                        "kind": "odd-parent-bound", "x": x, "r": r,
                        "options": actual,
                    })
            else:
                even_bounds += 1
                if value > 1:
                    failures.append({
                        "kind": "even-parent-bound", "x": x, "r": r,
                        "value": value,
                    })
        locus_checks += 1
        if observed != expected_value2(x):
            failures.append({
                "kind": "value2-locus", "x": x,
                "actual": sorted(observed), "expected": sorted(expected_value2(x)),
            })
        family_checks += 1
        if expected_value2(x) != family_value2(x):
            failures.append({
                "kind": "three-family-specialization", "x": x,
                "actual": sorted(expected_value2(x)),
                "predicted": sorted(family_value2(x)),
            })

    tail_checks = 0
    for x in range(15, 2001):
        for offset in range(65):
            r = x + 22 + offset
            tail_checks += 1
            if h6_y15(x, r) != (x + 15) % 2:
                failures.append({
                    "kind": "tail", "x": x, "r": r,
                    "actual": h6_y15(x, r), "expected": (x + 15) % 2,
                })

    rng = random.Random(20261117)
    random_tail = 0
    for _ in range(2000):
        x = rng.randint(15, 100000)
        r = x + 22 + rng.randint(0, 100000)
        random_tail += 1
        if h6_y15(x, r) != (x + 15) % 2:
            failures.append({
                "kind": "fixed-seed-far-tail", "x": x, "r": r,
                "actual": h6_y15(x, r), "expected": (x + 15) % 2,
            })

    counts = {
        "direct_ordered_canonical_formula_anchors": direct,
        "option_signatures": signatures,
        "mex_identity": mex_checks,
        "odd_parent_bounds": odd_bounds,
        "even_parent_bounds": even_bounds,
        "value2_locus": locus_checks,
        "three_family_specialization": family_checks,
        "tail": tail_checks,
        "fixed_seed_far_tail": random_tail,
    }
    return {
        "schema": "two-token-z6-y15-audit-v1",
        "claim": "H(R;(x,15);6) is given by the complete formula for all x>=15,R>=0",
        "classification": "finite-independent-audit-not-proof",
        "counts": counts,
        "total_checks": sum(counts.values()),
        "seed": 20261117,
        "failures": failures,
        "pass": not failures,
    }


def main():
    audit = run_audit()
    unhashed = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    audit["sha256_without_hash_field"] = hashlib.sha256(unhashed.encode("utf-8")).hexdigest()
    encoded = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    output = Path(__file__).resolve().parent / "output" / "audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(encoded, encoding="utf-8")
    print(json.dumps({
        "pass": audit["pass"],
        "total_checks": audit["total_checks"],
        "failures": len(audit["failures"]),
        "counts": audit["counts"],
        "sha256_without_hash_field": audit["sha256_without_hash_field"],
    }, ensure_ascii=False, sort_keys=True))
    if not audit["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
