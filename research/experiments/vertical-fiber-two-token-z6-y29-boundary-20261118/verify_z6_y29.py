#!/usr/bin/env python3
"""Independent finite audit for the universal z=6, y=29 slice theorem."""
from __future__ import annotations

import hashlib
import json
import random
import runpy
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ANCHOR = runpy.run_path(str(ROOT / "research/experiments/vertical-fiber-two-token-z6-y28-boundary-20261118/verify_z6_y28.py"))
h5, h28, O, E = (ANCHOR[k] for k in ("h5", "h28", "O", "E"))


def mex(values):
    seen = set(values)
    n = 0
    while n in seen:
        n += 1
    return n


def T29(x):
    out = {1, 3, 5}
    if x == 29:
        out.add(61)
    elif x == 33:
        out.add(63)
    elif x == 36:
        out.update((65, 67, 69, 71))
    elif x >= 37:
        out.add(65)
    return out


def P29(x, r):
    if x == 29:
        return O(r, 7, 59)
    if x == 30:
        return O(r, 7) or E(r, 62)
    if x == 31:
        return O(r, 7, 61)
    if x == 32:
        return O(r, 7) or E(r, 64)
    if x == 33:
        return O(r, 7, 61)
    if x == 34:
        return O(r, 7) or E(r, 64)
    if x == 35:
        return O(r, 7, 63)
    if x % 2 == 0:
        return O(r, 7, 63) or E(r, 66) or O(r, x + 37)
    return O(r, 7, 63) or E(r, 66, x + 35)


def h29(x, r):
    if r == 0:
        return 0
    if r in T29(x):
        return 2
    return int(P29(x, r))


def expected_signature(x, r):
    """Exact value-set partition for A/B/C when 1 <= R < x+36."""
    if r & 1:
        if r <= 5:
            return (0, 1)
        odd = {
            29: ((0, 59, (0,)), (61, 61, (0, 1)), (63, 63, (1,))),
            30: ((7, 65, (0,)),),
            31: ((7, 61, (0,)), (63, 65, (1,))),
            32: ((7, 67, (0,)),),
            33: ((7, 61, (0,)), (63, 63, (0, 1)), (65, 67, (1,))),
            34: ((7, 69, (0,)),),
            35: ((7, 63, (0,)), (65, 69, (1,))),
            36: ((7, 63, (0,)), (65, 71, (0, 1))),
        }
        if x in odd:
            for lo, hi, sig in odd[x]:
                if lo <= r <= hi:
                    return sig
        elif r <= 63:
            return (0,)
        elif r == 65:
            return (0, 1)
        elif r <= x + 35:
            return (1,)
    else:
        if r <= 6:
            return (2, 3)
        even = {
            29: ((8, 64, (1,)),),
            30: ((8, 60, (1,)), (62, 62, (0, 2, 3)), (64, 64, (0,))),
            31: ((8, 66, (1,)),),
            32: ((8, 60, (1,)), (62, 62, (1, 2)), (64, 66, (0,))),
            33: ((8, 68, (1,)),),
            34: ((8, 62, (1,)), (64, 64, (0, 2, 3)), (66, 68, (0,))),
            35: ((8, 62, (1,)), (64, 70, (1, 2, 3))),
            36: ((8, 62, (1,)), (64, 64, (1, 2, 3)), (66, 70, (0,))),
            37: ((8, 62, (1,)), (64, 64, (1, 2, 3)), (66, 72, (0, 2))),
        }
        if x in even:
            for lo, hi, sig in even[x]:
                if lo <= r <= hi:
                    return sig
        elif x % 2:  # odd x >= 39
            if r <= 62:
                return (1,)
            if r == 64:
                return (1, 2, 3)
            if r == 66:
                return (0, 2)
            if r <= x + 35:
                return (0,)
        else:  # even x >= 38
            if r <= 62:
                return (1,)
            if r == 64:
                return (1, 2, 3)
            if r == 66:
                return (0, 2)
            if r <= x + 34:
                return (0,)
    return None


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


def actual_signature(x, r):
    q = r - 1
    a = h28(29, q) if x == 29 else h29(x - 1, q)
    b = h28(x, q)
    c = 1 ^ h5(x, 29, q)
    return tuple(sorted({a, b, c}))


def audit_once():
    failures = []
    ordered, canonical = make_direct_engines()
    direct_checks = 0
    for x in range(29, 81):
        for r in range(x + 51):
            cases = (
                ("target", (x, 29), 6, h29(x, r)),
                ("y28", (x, 28), 6, h28(x, r)),
                ("z5", (x, 29), 5, h5(x, 29, r)),
            )
            for tag, tokens, z, formula in cases:
                a = ordered(r, tokens, z)
                b = canonical(r, tuple(sorted(tokens, reverse=True)), z)
                direct_checks += 2
                if a != formula or b != formula:
                    failures.append(("direct", tag, x, r, a, b, formula))

    signature_checks = mex_checks = odd_bound_checks = even_bound_checks = 0
    value2_parameter_checks = 0
    for x in range(29, 2001):
        seen_twos = set()
        for r in range(1, x + 36):
            actual = actual_signature(x, r)
            expected = expected_signature(x, r)
            signature_checks += 1
            if actual != expected:
                failures.append(("signature", x, r, actual, expected))
                continue
            value = mex(actual)
            mex_checks += 1
            if value != h29(x, r):
                failures.append(("mex", x, r, value, h29(x, r), actual))
            if value not in (0, 1, 2):
                failures.append(("range", x, r, value))
            if value == 2:
                seen_twos.add(r)
            if r & 1:
                odd_bound_checks += 1
                if not set(actual).issubset({0, 1}):
                    failures.append(("odd-parent-bound", x, r, actual))
            else:
                even_bound_checks += 1
                if value > 1:
                    failures.append(("even-parent-bound", x, r, value, actual))
        value2_parameter_checks += 1
        if seen_twos != T29(x):
            failures.append(("value2-locus", x, sorted(seen_twos), sorted(T29(x))))

    tail_checks = 0
    for x in range(29, 2001):
        for offset in range(65):
            r = x + 36 + offset
            tail_checks += 1
            if h29(x, r) != (x + 29) % 2:
                failures.append(("tail", x, r, h29(x, r), (x + 29) % 2))

    rng = random.Random(20261118)
    far_tail_checks = 0
    for _ in range(5000):
        x = rng.randint(29, 1_000_000)
        r = x + 36 + rng.randint(0, 1_000_000)
        far_tail_checks += 1
        if h29(x, r) != (x + 29) % 2:
            failures.append(("far-tail", x, r))

    counts = {
        "direct_formula_and_two_engine_checks": direct_checks,
        "even_parent_upper_bound": even_bound_checks,
        "far_tail_seeded_checks": far_tail_checks,
        "mex_identities": mex_checks,
        "odd_parent_option_bound": odd_bound_checks,
        "signature_points": signature_checks,
        "tail_checks": tail_checks,
        "value2_locus_parameters": value2_parameter_checks,
    }
    return {
        "all_pass": not failures,
        "classification": "universal proof by induction on x using explicit A/B/C signatures, K0942, K0873, K0832 Theorem T, and the general tail theorem; finite checks are independent audits only",
        "counts": counts,
        "failures": failures,
        "scope": {
            "direct_R": "0 <= R <= x+50 (target and y=28/z=5 anchors)",
            "direct_x": [29, 80],
            "far_tail_samples": far_tail_checks,
            "far_tail_seed": 20261118,
            "signature_R": "1 <= R < x+36",
            "signature_x": [29, 2000],
            "tail_offsets": [0, 64],
            "tail_x": [29, 2000],
        },
        "target": "H(R;(x,29);6), x>=29, R>=0",
        "total_checks": sum(counts.values()),
    }


def run():
    first = audit_once()
    second = audit_once()
    same = json.dumps(first, ensure_ascii=False, sort_keys=True, separators=(",", ":")) == json.dumps(
        second, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    base = dict(first, repeat_runs=2, repeat_byte_identical=same)
    raw = json.dumps(base, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    result = dict(base, sha256_without_hash_field=hashlib.sha256(raw).hexdigest())
    output = Path(__file__).with_name("output")
    output.mkdir(exist_ok=True)
    (output / "audit.json").write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "all_pass": result["all_pass"],
        "counts": result["counts"],
        "failures": len(result["failures"]),
        "repeat_byte_identical": same,
        "sha256_without_hash_field": result["sha256_without_hash_field"],
        "total_checks": result["total_checks"],
    }, sort_keys=True))
    if not result["all_pass"] or not same:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
