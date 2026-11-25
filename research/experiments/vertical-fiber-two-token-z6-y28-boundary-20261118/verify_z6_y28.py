#!/usr/bin/env python3
"""Independent finite audit for the proved z=6, y=28 two-token slice."""
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


def O(r, a, b=None):
    return r >= a and (b is None or r <= b) and r % 2 == 1


def E(r, a, b=None):
    return r >= a and (b is None or r <= b) and r % 2 == 0


def h5(x, y, r):
    if r == 0:
        return 0
    s, d = x + y, x - y
    twos = {1, 3, 5}
    if d == 1 and y >= 2:
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
        one = E(r, 6, s + 2) if y >= 3 else False
    elif d == 1:
        one = (E(r, 6, s + 3) or r >= s + 4) if y >= 2 else r >= 4
    elif d == 2:
        one = E(r, 6, s) if y >= 2 else False
    elif d == 3:
        one = E(r, 6, s + 1) or r >= s + 2
    elif d == 4:
        one = E(r, 6, s)
    elif d == 5:
        one = E(r, 6, s - 1) or r >= s + 1
    elif d == 6:
        one = E(r, 6, s - 2)
    elif d % 2:
        one = E(r, 6, 2 * y + 4) or O(r, 2 * y + 7, s + 4) or r >= s + 6
    else:
        one = E(r, 6, 2 * y + 4) or O(r, 2 * y + 7, s + 5)
    return int(one)


def h27(x, r):
    if r == 0:
        return 0
    twos = {1, 3, 5}
    if x == 27:
        twos.add(57)
    elif x == 31:
        twos.add(59)
    elif x == 34:
        twos.update({61, 63, 65, 67})
    elif x >= 35:
        twos.add(61)
    if r in twos:
        return 2
    if x == 27:
        one = O(r, 7, 55)
    elif x == 28:
        one = O(r, 7, 55) or r >= 57
    elif x == 29:
        one = O(r, 7, 57)
    elif x == 30:
        one = O(r, 7, 57) or r >= 59
    elif x == 31:
        one = O(r, 7, 57)
    elif x == 32:
        one = O(r, 7, 59) or r >= 60
    elif x == 33:
        one = O(r, 7, 59)
    elif x == 34:
        one = O(r, 7, 59) or E(r, 62) or O(r, 69)
    elif x % 2:
        one = O(r, 7, 59) or E(r, 62, x + 33)
    else:
        one = O(r, 7, 59) or E(r, 62) or O(r, x + 35)
    return int(one)


def T28(x):
    result = {1, 3, 5}
    if x == 28:
        result.add(59)
    elif x == 32:
        result.add(61)
    elif x == 35:
        result.update({63, 65, 67, 69})
    elif x >= 36:
        result.add(63)
    return result


def h28(x, r):
    if r == 0:
        return 0
    if r in T28(x):
        return 2
    if x == 28:
        one = O(r, 7, 57)
    elif x == 29:
        one = O(r, 7, 57) or r >= 59
    elif x in (30, 32):
        one = O(r, 7, 59)
    elif x == 31:
        one = O(r, 7, 59) or r >= 61
    elif x == 33:
        one = O(r, 7, 61) or r >= 62
    elif x == 34:
        one = O(r, 7, 61)
    elif x == 35:
        one = O(r, 7, 61) or E(r, 64, 68) or r >= 70
    elif x % 2 == 0:
        one = O(r, 7, 61) or E(r, 64, x + 34)
    else:
        one = O(r, 7, 61) or E(r, 64, x + 33) or r >= x + 35
    return int(one)


def signature(x, r):
    q = r - 1
    a = h27(28, q) if x == 28 else h28(x - 1, q)
    b = h27(x, q)
    c = 1 ^ h5(x, 28, q)
    return {a, b, c}


def make_direct_engines():
    @lru_cache(None)
    def ordered(r, tokens, z):
        if r == 0:
            return 0
        options = []
        for i, token in enumerate(tokens):
            child = list(tokens)
            next_z = z
            if token >= 2:
                child[i] -= 1
            else:
                child.pop(i)
                next_z += 1
            options.append(ordered(r - 1, tuple(child), next_z))
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
            next_z = z
            if token >= 2:
                child[i] -= 1
            else:
                child.pop(i)
                next_z += 1
            options.append(canonical(r - 1, tuple(sorted(child, reverse=True)), next_z))
        if z:
            options.append(1 ^ canonical(r - 1, tokens, z - 1))
        return mex(options)

    return ordered, canonical


def audit_once():
    failures = []
    ordered, canonical = make_direct_engines()
    direct = 0
    for x in range(28, 61):
        for r in range(x + 45):
            cases = (
                ((x, 28), 6, h28(x, r)),
                ((x, 27), 6, h27(x, r)),
                ((x, 28), 5, h5(x, 28, r)),
            )
            for tokens, z, formula in cases:
                a = ordered(r, tokens, z)
                b = canonical(r, tuple(sorted(tokens, reverse=True)), z)
                direct += 2
                if a != formula or b != formula:
                    failures.append(("direct", x, r, tokens, z, a, b, formula))

    signature_points = mexes = odd_bound = even_bound = 0
    value2_parameters = 0
    for x in range(28, 2001):
        seen_twos = set()
        for r in range(1, x + 35):
            children = signature(x, r)
            signature_points += 1
            value = mex(children)
            mexes += 1
            if value != h28(x, r):
                failures.append(("mex", x, r, sorted(children), value, h28(x, r)))
            if value not in (0, 1, 2):
                failures.append(("range", x, r, value))
            if value == 2:
                seen_twos.add(r)
            if r % 2:
                odd_bound += 1
                if not children.issubset({0, 1}):
                    failures.append(("odd-parent-bound", x, r, sorted(children)))
            else:
                even_bound += 1
                if value > 1:
                    failures.append(("even-parent-bound", x, r, value, sorted(children)))
        value2_parameters += 1
        if seen_twos != T28(x):
            failures.append(("value2-locus", x, sorted(seen_twos), sorted(T28(x))))

    tail = 0
    for x in range(28, 2001):
        for offset in range(65):
            r = x + 35 + offset
            tail += 1
            if h28(x, r) != (x + 28) % 2:
                failures.append(("tail", x, r, h28(x, r), (x + 28) % 2))

    rng = random.Random(20261118)
    far_tail = 0
    for _ in range(5000):
        x = rng.randint(28, 1_000_000)
        r = x + 35 + rng.randint(0, 1_000_000)
        far_tail += 1
        if h28(x, r) != (x + 28) % 2:
            failures.append(("far-tail", x, r))

    counts = {
        "direct_formula_and_two_engine_checks": direct,
        "even_parent_upper_bound": even_bound,
        "far_tail_seeded_checks": far_tail,
        "mex_identities": mexes,
        "odd_parent_option_bound": odd_bound,
        "signature_points": signature_points,
        "tail_checks": tail,
        "value2_locus_parameters": value2_parameters,
    }
    return {
        "all_pass": not failures,
        "classification": "universal proof by induction on x using explicit A/B/C signatures, K0940, K0873, K0832 Theorem T, and the general tail theorem; finite checks are independent audits only",
        "counts": counts,
        "failures": failures,
        "scope": {
            "direct_R": "0 <= R < x+45 (target and y=27/z=5 anchors)",
            "direct_x": [28, 60],
            "far_tail_samples": far_tail,
            "far_tail_seed": 20261118,
            "signature_R": "1 <= R < x+35",
            "signature_x": [28, 2000],
            "tail_offsets": [0, 64],
            "tail_x": [28, 2000],
        },
        "target": "H(R;(x,28);6), x>=28, R>=0",
        "total_checks": sum(counts.values()),
    }


def run():
    first = audit_once()
    second = audit_once()
    same = json.dumps(first, ensure_ascii=False, sort_keys=True, separators=(",", ":")) == json.dumps(second, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    base = dict(first, repeat_runs=2, repeat_byte_identical=same)
    raw = json.dumps(base, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    result = dict(base, sha256_without_hash_field=hashlib.sha256(raw).hexdigest())
    output = Path(__file__).with_name("output")
    output.mkdir(exist_ok=True)
    (output / "audit.json").write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": result["all_pass"], "counts": result["counts"], "failures": len(result["failures"]), "repeat_byte_identical": same, "sha256_without_hash_field": result["sha256_without_hash_field"], "total_checks": result["total_checks"]}, sort_keys=True))
    if not result["all_pass"] or not same:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
