#!/usr/bin/env python3
"""Independent finite audit for the two-token residual slice z=6, y=4.

The unbounded claim is proved in report.md by R-strong induction. This
script checks the raw recurrence in two state representations, verifies the
z=5 and z=6,y=3 anchors on finite grids, and reconstructs the complete
A/B/C signature table from those proved anchors. Finite checks are not the
proof of the unbounded theorem.
"""
from __future__ import annotations

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


def even(r: int, lo: int, hi: int) -> bool:
    return r % 2 == 0 and lo <= r <= hi


def odd(r: int, lo: int, hi: int) -> bool:
    return r % 2 == 1 and lo <= r <= hi


@lru_cache(None)
def exact_ordered(r: int, tokens: tuple[int, ...], z: int) -> int:
    """Ordered-token recurrence; child token order is never normalized."""
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
    """Independent multiset recurrence; every child is sorted descending."""
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
    """K0873: proved full two-token z=5 formula."""
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


def h6_y3(x: int, r: int) -> int:
    """K0879: proved z=6, y=3 boundary formula."""
    if r == 0:
        return 0
    if x == 3:
        t, p = {1, 3, 5, 7, 9}, False
    elif x == 4:
        t, p = {1, 3, 5}, (r == 7 or r >= 9)
    elif x == 5:
        t, p = {1, 3, 5}, r in (7, 9)
    elif x == 6:
        t, p = {1, 3, 5}, r in (7, 9, 11) or r >= 12
    elif x == 7:
        t, p = {1, 3, 5, 11}, r in (7, 9)
    elif x == 8:
        t, p = {1, 3, 5}, r in (7, 9, 11) or r >= 12
    elif x == 9:
        t, p = {1, 3, 5}, r in (7, 9, 11)
    elif x == 10:
        t = {1, 3, 5, 13, 15, 17, 19}
        p = r in (7, 9, 11) or even(r, 14, 18) or r >= 20
    elif x % 2 == 0:
        t = {1, 3, 5, 13}
        p = r in (7, 9, 11) or even(r, 14, x + 8) or r >= x + 10
    else:
        t = {1, 3, 5, 13}
        p = r in (7, 9, 11) or even(r, 14, x + 9)
    return 2 if r in t else int(p)


def h6_y4(x: int, r: int) -> int:
    """Proposed complete formula for H(r;(x,4);6), x>=4."""
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


def options_from_anchors(x: int, r: int) -> set[int]:
    """A/B/C option values reconstructed only from proved z=5 and y=3 slices."""
    if r == 0:
        return set()
    if x == 4:
        a = b = h6_y3(4, r - 1)
    else:
        a = h6_y4(x - 1, r - 1)
        b = h6_y3(x, r - 1)
    c = 1 ^ h5(x, 4, r - 1)
    return {a, b, c}


def expected_signature(x: int, r: int) -> set[int]:
    """Complete pre-tail A/B/C signature table in report.md."""
    if r == 0:
        return set()
    if x == 4:
        if r % 2:
            if r <= 5:
                return {0, 1}
            if r <= 9:
                return {0}
            if r == 11:
                return {0, 1}
            return {1}
        return {2, 3} if r <= 6 else {1}
    if x == 5:
        if r % 2:
            return {0, 1} if r <= 5 else {0}
        if r <= 6:
            return {2, 3}
        if r <= 10:
            return {1}
        if r == 12:
            return {0, 2, 3}
        return {0}
    if x == 6:
        if r % 2:
            if r <= 5:
                return {0, 1}
            if r <= 11:
                return {0}
            return {1}
        return {2, 3} if r <= 6 else {1}
    if x == 7:
        if r % 2:
            return {0, 1} if r <= 5 else {0}
        if r <= 6:
            return {2, 3}
        if r <= 10:
            return {1}
        if r == 12:
            return {1, 2}
        return {0}
    if x == 8:
        if r % 2:
            if r <= 5:
                return {0, 1}
            if r <= 11:
                return {0}
            if r == 13:
                return {0, 1}
            return {1}
        return {2, 3} if r <= 6 else {1}
    if x == 9:
        if r % 2:
            return {0, 1} if r <= 5 else {0}
        if r <= 6:
            return {2, 3}
        if r <= 12:
            return {1}
        if r == 14:
            return {0, 2, 3}
        return {0}
    if x == 10:
        if r % 2:
            return {0, 1} if r <= 5 else ({0} if r <= 13 else {1})
        if r <= 6:
            return {2, 3}
        if r <= 12:
            return {1}
        return {1, 2, 3}
    if x == 11:
        if r % 2:
            if r <= 5:
                return {0, 1}
            if r <= 13:
                return {0}
            return {0, 1}
        if r <= 6:
            return {2, 3}
        if r <= 12:
            return {1}
        if r == 14:
            return {1, 2, 3}
        return {0}
    if x == 12:
        if r % 2:
            if r <= 5:
                return {0, 1}
            if r <= 13:
                return {0}
            if r == 15:
                return {0, 1}
            return {1}
        if r <= 6:
            return {2, 3}
        if r <= 12:
            return {1}
        if r == 14:
            return {1, 2, 3}
        return {0, 2}
    if r % 2:
        if r <= 5:
            return {0, 1}
        if r <= 13:
            return {0}
        if r == 15:
            return {0, 1}
        return {1}
    if r <= 6:
        return {2, 3}
    if r <= 12:
        return {1}
    if r == 14:
        return {1, 2, 3}
    if r == 16:
        return {0, 2}
    return {0}


def main() -> None:
    rng = random.Random(20261117)
    counts = {
        "direct_ordered_canonical_states": 0,
        "direct_formula_states": 0,
        "theorem_t_checks": 0,
        "z5_y4_anchor_states": 0,
        "z6_y3_anchor_states": 0,
        "option_signature_states": 0,
        "mex_identity_states": 0,
        "tail_states": 0,
        "random_anchor_signature_states": 0,
    }
    failures = []

    for x in range(4, 46):
        for r in range(0, x + 81):
            ordered = exact_ordered(r, (x, 4), 6)
            canonical = exact_canonical(r, (x, 4), 6)
            formula = h6_y4(x, r)
            counts["direct_ordered_canonical_states"] += 1
            counts["direct_formula_states"] += 1
            counts["theorem_t_checks"] += 1
            if ordered != canonical:
                failures.append(["engine", x, r, ordered, canonical])
            if ordered != formula:
                failures.append(["formula", x, r, ordered, formula])
            if ordered > 2 or (r % 2 == 0 and ordered > 1):
                failures.append(["Theorem-T", x, r, ordered])

    for x in range(4, 61):
        for r in range(0, 101):
            got, want = exact_ordered(r, (x, 4), 5), h5(x, 4, r)
            counts["z5_y4_anchor_states"] += 1
            if got != want:
                failures.append(["z5-anchor", x, r, got, want])
    for x in range(4, 61):
        for r in range(0, 101):
            got, want = exact_ordered(r, (x, 3), 6), h6_y3(x, r)
            counts["z6_y3_anchor_states"] += 1
            if got != want:
                failures.append(["z6-y3-anchor", x, r, got, want])

    for x in range(4, 2001):
        for r in range(1, x + 11):
            got = options_from_anchors(x, r)
            want = expected_signature(x, r)
            counts["option_signature_states"] += 1
            if got != want:
                failures.append(["signature", x, r, sorted(got), sorted(want)])
            got_mex, want_mex = mex(got), h6_y4(x, r)
            counts["mex_identity_states"] += 1
            if got_mex != want_mex:
                failures.append(["mex", x, r, sorted(got), got_mex, want_mex])

    for x in range(4, 5001):
        for r in (x + 11, x + 12, x + 13, 2 * x + 50):
            counts["tail_states"] += 1
            got, want = h6_y4(x, r), (x + 4) % 2
            if got != want:
                failures.append(["tail", x, r, got, want])

    for _ in range(2000):
        x = rng.randint(4, 1_000_000)
        r = rng.randint(1, x + 50)
        options = options_from_anchors(x, r)
        got, want = mex(options), h6_y4(x, r)
        counts["random_anchor_signature_states"] += 1
        if got != want:
            failures.append(["random", x, r, sorted(options), got, want])

    result = {
        "schema": "two-token-z6-y4-audit-v1",
        "claim": "H(R;(x,4);6) is given by the z6_y4 formula for all x>=4,R>=0",
        "classification": "finite-independent-audit-not-proof",
        "seed": 20261117,
        "counts": counts,
        "total_checks": sum(counts.values()),
        "ordered_engine_cache": {
            "hits": exact_ordered.cache_info().hits,
            "misses": exact_ordered.cache_info().misses,
        },
        "canonical_engine_cache": {
            "hits": exact_canonical.cache_info().hits,
            "misses": exact_canonical.cache_info().misses,
        },
        "failures": failures,
        "pass": not failures,
    }
    output = Path(__file__).resolve().parent / "output" / "audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
