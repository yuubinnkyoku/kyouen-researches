#!/usr/bin/env python3
"""Finite independent audit for the universally proved z=6, y=17 slice."""
from __future__ import annotations

import hashlib
import json
import random
from functools import lru_cache
from pathlib import Path


def mex(values):
    present = set(values)
    value = 0
    while value in present:
        value += 1
    return value


def O(r, lo, hi=None):
    return r >= lo and (hi is None or r <= hi) and r % 2 == 1


def E(r, lo, hi=None):
    return r >= lo and (hi is None or r <= hi) and r % 2 == 0


def h5(x, y, r):
    if r == 0:
        return 0
    s, d = x + y, x - y
    value2 = {1, 3, 5}
    if d == 1:
        value2.add(2 * y + 3)
    elif d == 5:
        value2.add(2 * y + 5)
    elif d == 6:
        value2.update({2 * y + 5, 2 * y + 7, 2 * y + 9, 2 * y + 11})
    elif d >= 7:
        value2.add(2 * y + 5)
    if r in value2:
        return 2
    if d == 0:
        value1 = E(r, 6, s + 2)
    elif d == 1:
        value1 = E(r, 6, s + 3) or r >= s + 4
    elif d == 2:
        value1 = E(r, 6, s)
    elif d == 3:
        value1 = E(r, 6, s + 1) or r >= s + 2
    elif d == 4:
        value1 = E(r, 6, s)
    elif d == 5:
        value1 = E(r, 6, s - 1) or r >= s + 1
    elif d == 6:
        value1 = E(r, 6, s - 2)
    elif d >= 7 and d % 2:
        value1 = E(r, 6, 2 * y + 4) or O(r, 2 * y + 7, s + 4) or r >= s + 6
    else:
        value1 = E(r, 6, 2 * y + 4) or O(r, 2 * y + 7, s + 5)
    return int(value1)


def h6y16(x, r):
    if x < 16:
        raise ValueError("x must be at least 16")
    if r == 0:
        return 0
    value2 = {1, 3, 5}
    if x == 16:
        value2.add(35)
    elif x == 20:
        value2.add(37)
    elif x == 23:
        value2.update({39, 41, 43, 45})
    elif x >= 24:
        value2.add(39)
    if r in value2:
        return 2
    if x == 16:
        value1 = O(r, 7, 33)
    elif x == 17:
        value1 = O(r, 7, 35) or r >= 36
    elif x == 18:
        value1 = O(r, 7, 35)
    elif x == 19:
        value1 = O(r, 7, 35) or r >= 37
    elif x == 20:
        value1 = O(r, 7, 35)
    elif x == 21:
        value1 = O(r, 7, 35) or r >= 37
    elif x == 22:
        value1 = O(r, 7, 37)
    else:
        value1 = (O(r, 7, 37)
                  or E(r, 40, x + (21 if x % 2 else 22))
                  or (x % 2 == 1 and r >= x + 23))
    return int(value1)


def h6y17(x, r):
    if x < 17:
        raise ValueError("x must be at least 17")
    if r == 0:
        return 0
    value2 = {1, 3, 5}
    if x == 17:
        value2.add(37)
    elif x == 21:
        value2.add(39)
    elif x == 24:
        value2.update({41, 43, 45, 47})
    elif x >= 25:
        value2.add(41)
    if r in value2:
        return 2
    if x == 17:
        value1 = O(r, 7, 35)
    elif x == 18:
        value1 = O(r, 7, 41) or E(r, 38, 40) or r >= 42
    elif x == 19:
        value1 = O(r, 7, 37)
    elif x == 20:
        value1 = O(r, 7, 43) or E(r, 40, 42) or r >= 44
    elif x == 21:
        value1 = O(r, 7, 37)
    elif x == 22:
        value1 = O(r, 7, 45) or E(r, 40, 44) or r >= 46
    elif x == 23:
        value1 = O(r, 7, 39)
    elif x == 24:
        value1 = O(r, 7, 39) or E(r, 42, 46) or r >= 48
    elif x == 25:
        value1 = O(r, 7, 39) or E(r, 42, 48)
    elif x % 2 == 0:
        value1 = O(r, 7, 39) or E(r, 42, x + 22) or r >= x + 24
    else:
        value1 = O(r, 7, 39) or E(r, 42, x + 23)
    return int(value1)


@lru_cache(None)
def ordered(r, tokens, z):
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
    if z:
        options.append(1 ^ ordered(r - 1, tokens, z - 1))
    return mex(options)


@lru_cache(None)
def canonical(r, tokens, z):
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
    if z:
        options.append(1 ^ canonical(r - 1, tuple(sorted(tokens, reverse=True)), z - 1))
    return mex(options)


# Each row is (inclusive lower, inclusive upper, sorted option-value digits).
SIG = {
    17: ([(1, 5, "01"), (7, 35, "0"), (37, 37, "01"), (39, 39, "1")],
         [(2, 6, "23"), (8, 40, "1")]),
    18: ([(1, 5, "01"), (7, 41, "0")],
         [(2, 6, "23"), (8, 36, "1"), (38, 38, "023"), (40, 40, "0")]),
    19: ([(1, 5, "01"), (7, 37, "0"), (39, 41, "1")],
         [(2, 6, "23"), (8, 42, "1")]),
    20: ([(1, 5, "01"), (7, 43, "0")],
         [(2, 6, "23"), (8, 36, "1"), (38, 38, "12"), (40, 42, "0")]),
    21: ([(1, 5, "01"), (7, 37, "0"), (39, 39, "01"), (41, 43, "1")],
         [(2, 6, "23"), (8, 44, "1")]),
    22: ([(1, 5, "01"), (7, 45, "0")],
         [(2, 6, "23"), (8, 38, "1"), (40, 40, "023"), (42, 44, "0")]),
    23: ([(1, 5, "01"), (7, 39, "0"), (41, 45, "1")],
         [(2, 6, "23"), (8, 38, "1"), (40, 46, "123")]),
    24: ([(1, 5, "01"), (7, 39, "0"), (41, 47, "01")],
         [(2, 6, "23"), (8, 38, "1"), (40, 40, "123"), (42, 46, "0")]),
    25: ([(1, 5, "01"), (7, 39, "0"), (41, 41, "01"), (43, 47, "1")],
         [(2, 6, "23"), (8, 38, "1"), (40, 40, "123"), (42, 48, "02")]),
}


def expected_signature(x, r):
    if x <= 25:
        rows = SIG[x][0 if r % 2 else 1]
    elif r % 2:
        upper = x + 23 if x % 2 == 0 else x + 22
        rows = [(1, 5, "01"), (7, 39, "0"), (41, 41, "01"), (43, upper, "1")]
    else:
        upper = x + 22 if x % 2 == 0 else x + 23
        rows = [(2, 6, "23"), (8, 38, "1"), (40, 40, "123"),
                (42, 42, "02"), (44, upper, "0")]
    for lower, upper, digits in rows:
        if lower <= r <= upper and (r - lower) % 2 == 0:
            return tuple(int(digit) for digit in digits)
    return None


def actual_signature(x, r):
    a = h6y16(17, r - 1) if x == 17 else h6y17(x - 1, r - 1)
    b = h6y16(x, r - 1)
    c = 1 ^ h5(x, 17, r - 1)
    return tuple(sorted({a, b, c}))


def formula_value2(x):
    values = {1, 3, 5}
    if x == 17:
        values.add(37)
    elif x == 21:
        values.add(39)
    elif x == 24:
        values.update({41, 43, 45, 47})
    elif x >= 25:
        values.add(41)
    return values


def family_value2(x):
    d = x - 17
    values = {1, 3, 5}
    if d <= 6 and d % 2 == 0 and (6 + d) % 4 == 2:
        values.add(34 + (6 + d) // 2)
    elif d == 7:
        values.update({41, 43, 45, 47})
    elif d >= 8:
        values.add(41)
    return values


def run_audit():
    failures = []
    direct = 0
    for x in range(17, 81):
        for r in range(x + 51):
            cases = (
                ((x, 17), 6, h6y17(x, r)),
                ((x, 16), 6, h6y16(x, r)),
                ((x, 17), 5, h5(x, 17, r)),
            )
            for tokens, z, formula in cases:
                first = ordered(r, tokens, z)
                second = canonical(r, tuple(sorted(tokens, reverse=True)), z)
                direct += 1
                if first != second or first != formula:
                    failures.append({
                        "kind": "direct", "x": x, "r": r, "tokens": tokens, "z": z,
                        "ordered": first, "canonical": second, "formula": formula,
                    })

    signatures = mex_checks = odd_bounds = even_bounds = 0
    loci = families = 0
    for x in range(17, 2001):
        observed = set()
        for r in range(1, x + 24):
            actual = actual_signature(x, r)
            expected = expected_signature(x, r)
            signatures += 1
            if actual != expected:
                failures.append({"kind": "signature", "x": x, "r": r,
                                 "actual": actual, "expected": expected})
            value = mex(actual)
            mex_checks += 1
            if value != h6y17(x, r):
                failures.append({"kind": "mex", "x": x, "r": r,
                                 "actual": value, "formula": h6y17(x, r)})
            if value == 2:
                observed.add(r)
            if r % 2:
                odd_bounds += 1
                if not set(actual).issubset({0, 1}):
                    failures.append({"kind": "odd-bound", "x": x, "r": r,
                                     "options": actual})
            else:
                even_bounds += 1
                if value > 1:
                    failures.append({"kind": "even-bound", "x": x, "r": r,
                                     "value": value})
        predicted = formula_value2(x)
        loci += 1
        if observed != predicted:
            failures.append({"kind": "value2-locus", "x": x,
                             "actual": sorted(observed), "expected": sorted(predicted)})
        family = family_value2(x)
        families += 1
        if predicted != family:
            failures.append({"kind": "three-family", "x": x,
                             "actual": sorted(predicted), "predicted": sorted(family)})

    tail = 0
    for x in range(17, 2001):
        for offset in range(65):
            r = x + 24 + offset
            tail += 1
            if h6y17(x, r) != (x + 17) % 2:
                failures.append({"kind": "tail", "x": x, "r": r,
                                 "actual": h6y17(x, r), "expected": (x + 17) % 2})

    rng = random.Random(20261117)
    far = 0
    for _ in range(2000):
        x = rng.randint(17, 100000)
        r = x + 24 + rng.randint(0, 100000)
        far += 1
        if h6y17(x, r) != (x + 17) % 2:
            failures.append({"kind": "far-tail", "x": x, "r": r})

    counts = {
        "direct_ordered_canonical_formula_anchors": direct,
        "option_signatures": signatures,
        "mex_identity": mex_checks,
        "odd_parent_bounds": odd_bounds,
        "even_parent_bounds": even_bounds,
        "value2_locus": loci,
        "three_family_specialization": families,
        "tail": tail,
        "fixed_seed_far_tail": far,
    }
    return {
        "schema": "two-token-z6-y17-audit-v1",
        "claim": "H(R;(x,17);6) is given by the complete formula for all x>=17,R>=0",
        "classification": "finite-independent-audit-not-proof",
        "counts": counts,
        "total_checks": sum(counts.values()),
        "seed": 20261117,
        "failures": failures,
        "pass": not failures,
    }


def main():
    audit = run_audit()
    base = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    audit["sha256_without_hash_field"] = hashlib.sha256(base.encode("utf-8")).hexdigest()
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
