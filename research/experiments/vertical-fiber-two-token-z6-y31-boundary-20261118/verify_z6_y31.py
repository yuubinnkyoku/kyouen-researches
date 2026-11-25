#!/usr/bin/env python3
"""Independent finite audit for the proved z=6, y=31 two-token slice."""
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
    """K0873: proved z=5 two-token formula."""
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


def h30(x, r):
    """K0947: proved z=6, y=30 slice."""
    if r == 0:
        return 0
    twos = {1, 3, 5}
    if x == 30:
        twos.add(63)
    elif x == 34:
        twos.add(65)
    elif x == 37:
        twos.update({67, 69, 71, 73})
    elif x >= 38:
        twos.add(67)
    if r in twos:
        return 2
    if x == 30:
        one = O(r, 7, 61)
    elif x == 31:
        one = O(r, 7) or E(r, 64)
    elif x == 32:
        one = O(r, 7, 63)
    elif x == 33:
        one = O(r, 7) or E(r, 66)
    elif x == 34:
        one = O(r, 7, 63)
    elif x == 35:
        one = O(r, 7) or E(r, 66)
    elif x == 36:
        one = O(r, 7, 65)
    elif x % 2:
        one = O(r, 7, 65) or E(r, 68, x + 35) or r >= x + 37
    else:
        one = O(r, 7, 65) or E(r, 68, x + 36)
    return int(one)


def T31(x):
    out = {1, 3, 5}
    if x == 31:
        out.add(65)
    elif x == 35:
        out.add(67)
    elif x == 38:
        out.update({69, 71, 73, 75})
    elif x >= 39:
        out.add(69)
    return out


def P31(x, r):
    if x == 31:
        return O(r, 7, 63)
    if x == 32:
        return O(r, 7, 69) or E(r, 66, 68) or r >= 70
    if x == 33:
        return O(r, 7, 65)
    if x == 34:
        return O(r, 7, 71) or E(r, 68, 70) or r >= 72
    if x == 35:
        return O(r, 7, 65)
    if x == 36:
        return O(r, 7, 73) or E(r, 68, 72) or r >= 74
    if x == 37:
        return O(r, 7, 67)
    if x == 38:
        return O(r, 7, 67) or E(r, 70, 74) or r >= 76
    if x % 2:
        return O(r, 7, 67) or E(r, 70, x + 37)
    return O(r, 7, 67) or E(r, 70, x + 36) or r >= x + 38


def h31(x, r):
    if r == 0:
        return 0
    if r in T31(x):
        return 2
    return int(P31(x, r))


def signature_from_formula(x, r):
    q = r - 1
    a = h30(x, q) if x == 31 else h31(x - 1, q)
    b = h30(x, q)
    c = 1 ^ h5(x, 31, q)
    return tuple(sorted({a, b, c}))


def expected_signature(x, r):
    """Explicit all-x signature table used by the induction proof."""
    if r & 1:
        if r <= 5:
            return (0, 1)
        if x == 31:
            if r <= 63: return (0,)
            if r == 65: return (0, 1)
            if r == 67: return (1,)
        elif x == 32:
            if r <= 69: return (0,)
        elif x == 33:
            if r <= 65: return (0,)
            if r <= 69: return (1,)
        elif x == 34:
            if r <= 71: return (0,)
        elif x == 35:
            if r <= 65: return (0,)
            if r == 67: return (0, 1)
            if r <= 71: return (1,)
        elif x == 36:
            if r <= 73: return (0,)
        elif x == 37:
            if r <= 67: return (0,)
            if r <= 73: return (1,)
        elif x == 38:
            if r <= 67: return (0,)
            if r <= 75: return (0, 1)
        elif x == 39:
            if r <= 67: return (0,)
            if r == 69: return (0, 1)
            if r <= 75: return (1,)
        elif x == 40:
            if r <= 67: return (0,)
            if r == 69: return (0, 1)
            if r <= 77: return (1,)
        elif x % 2:
            if r <= 67: return (0,)
            if r == 69: return (0, 1)
            if r <= x + 36: return (1,)
        else:
            if r <= 67: return (0,)
            if r == 69: return (0, 1)
            if r <= x + 37: return (1,)
    else:
        if r <= 6:
            return (2, 3)
        if x == 31:
            if r <= 68: return (1,)
        elif x == 32:
            if r <= 64: return (1,)
            if r == 66: return (0, 2, 3)
            if r == 68: return (0,)
        elif x == 33:
            if r <= 70: return (1,)
        elif x == 34:
            if r <= 64: return (1,)
            if r == 66: return (1, 2)
            if r <= 70: return (0,)
        elif x == 35:
            if r <= 72: return (1,)
        elif x == 36:
            if r <= 66: return (1,)
            if r == 68: return (0, 2, 3)
            if r <= 72: return (0,)
        elif x == 37:
            if r <= 66: return (1,)
            if r <= 74: return (1, 2, 3)
        elif x == 38:
            if r <= 66: return (1,)
            if r == 68: return (1, 2, 3)
            if r <= 74: return (0,)
        elif x == 39:
            if r <= 66: return (1,)
            if r == 68: return (1, 2, 3)
            if r <= 76: return (0, 2)
        elif x == 40:
            if r <= 66: return (1,)
            if r == 68: return (1, 2, 3)
            if r == 70: return (0, 2)
            if r <= 76: return (0,)
        elif x % 2:
            if r <= 66: return (1,)
            if r == 68: return (1, 2, 3)
            if r == 70: return (0, 2)
            if r <= x + 37: return (0,)
        else:
            if r <= 66: return (1,)
            if r == 68: return (1, 2, 3)
            if r == 70: return (0, 2)
            if r <= x + 36: return (0,)
    return None


def make_direct_engines():
    @lru_cache(None)
    def ordered(r, tokens, z):
        if r == 0:
            return 0
        options = []
        for i, token in enumerate(tokens):
            child = list(tokens)
            nz = z
            if token >= 2:
                child[i] -= 1
            else:
                child.pop(i)
                nz += 1
            options.append(ordered(r - 1, tuple(child), nz))
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
            nz = z
            if token >= 2:
                child[i] -= 1
            else:
                child.pop(i)
                nz += 1
            options.append(canonical(r - 1, tuple(sorted(child, reverse=True)), nz))
        if z:
            options.append(1 ^ canonical(r - 1, tokens, z - 1))
        return mex(options)

    return ordered, canonical


def audit_once():
    failures = []
    ordered, canonical = make_direct_engines()
    direct = 0
    for x in range(31, 81):
        for r in range(x + 51):
            cases = (
                ("target", (x, 31), 6, h31(x, r)),
                ("y30", (x, 30), 6, h30(x, r)),
                ("z5", (x, 31), 5, h5(x, 31, r)),
            )
            for tag, tokens, z, formula in cases:
                a = ordered(r, tokens, z)
                b = canonical(r, tuple(sorted(tokens, reverse=True)), z)
                direct += 2
                if a != formula or b != formula:
                    failures.append(("direct", tag, x, r, tokens, z, a, b, formula))

    signatures = mexes = odd_bound = even_bound = 0
    parameters = 0
    for x in range(31, 2001):
        seen_twos = set()
        for r in range(1, x + 38):
            actual = signature_from_formula(x, r)
            expected = expected_signature(x, r)
            signatures += 1
            if actual != expected:
                failures.append(("signature", x, r, actual, expected))
                continue
            value = mex(actual)
            mexes += 1
            if value != h31(x, r):
                failures.append(("mex", x, r, value, h31(x, r), actual))
            if r & 1:
                odd_bound += 1
                if not set(actual).issubset({0, 1}):
                    failures.append(("odd-bound", x, r, actual))
            else:
                even_bound += 1
                if value > 1:
                    failures.append(("even-bound", x, r, value, actual))
            if value == 2:
                seen_twos.add(r)
        parameters += 1
        if seen_twos != T31(x):
            failures.append(("T31", x, sorted(seen_twos), sorted(T31(x))))

    tail = 0
    for x in range(31, 2001):
        for offset in range(65):
            r = x + 38 + offset
            tail += 1
            if h31(x, r) != ((x + 31) & 1):
                failures.append(("tail", x, r, h31(x, r), (x + 31) & 1))

    rng = random.Random(20261118)
    far_tail = 0
    for _ in range(5000):
        x = rng.randint(31, 1_000_000)
        r = x + 38 + rng.randint(0, 1_000_000)
        far_tail += 1
        if h31(x, r) != ((x + 31) & 1):
            failures.append(("far-tail", x, r, h31(x, r), (x + 31) & 1))

    counts = {
        "direct_formula_and_two_engine_checks": direct,
        "even_parent_upper_bound": even_bound,
        "far_tail_seeded_checks": far_tail,
        "mex_identities": mexes,
        "odd_parent_option_bound": odd_bound,
        "signature_points": signatures,
        "tail_checks": tail,
        "value2_locus_parameters": parameters,
    }
    return {
        "all_pass": not failures,
        "classification": (
            "universal proof by induction on x using explicit A/B/C signatures, "
            "K0947, K0873, K0832 Theorem T, and the general tail theorem; "
            "finite checks are independent audits only"
        ),
        "counts": counts,
        "failures": failures,
        "scope": {
            "direct_R": "0 <= R <= x+50 (target and y=30/z=5 anchors)",
            "direct_x": [31, 80],
            "far_tail_samples": far_tail,
            "far_tail_seed": 20261118,
            "signature_R": "1 <= R < x+38",
            "signature_x": [31, 2000],
            "tail_offsets": [0, 64],
            "tail_x": [31, 2000],
        },
        "target": "H(R;(x,31);6), x>=31, R>=0",
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
    out = Path(__file__).with_name("output")
    out.mkdir(exist_ok=True)
    (out / "audit.json").write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "all_pass": result["all_pass"],
                "counts": result["counts"],
                "failures": len(result["failures"]),
                "repeat_byte_identical": same,
                "sha256_without_hash_field": result["sha256_without_hash_field"],
                "total_checks": result["total_checks"],
            },
            sort_keys=True,
        )
    )
    if not result["all_pass"] or not same:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
