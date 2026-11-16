#!/usr/bin/env python3
"""Independent finite audit for the two-token residual slice z=6, y=3.

The proof is an R-strong induction using the A/B/C signature table in
report.md. This verifier separately evaluates the raw token recurrence on
bounded grids, then reconstructs A/B/C only from the proved z=5 and z=6,y=2
anchor formulae. Finite checks are not the proof of the unbounded claim.
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


def ev(r, lo, hi):
    return r % 2 == 0 and lo <= r <= hi


def od(r, lo, hi):
    return r % 2 == 1 and lo <= r <= hi


@lru_cache(None)
def exact_h(R: int, X: tuple[int, ...], z: int) -> int:
    """Raw ordered-token recurrence; no cap reduction or formula lookup."""
    if R == 0:
        return 0
    options = []
    for i, token in enumerate(X):
        child = list(X)
        if token >= 2:
            child[i] = token - 1
            options.append(exact_h(R - 1, tuple(sorted(child, reverse=True)), z))
        else:
            child.pop(i)
            options.append(exact_h(R - 1, tuple(sorted(child, reverse=True)), z + 1))
    if z >= 1:
        options.append(1 ^ exact_h(R - 1, X, z - 1))
    return mex(options)


def h5(x: int, y: int, r: int) -> int:
    """K0873: proved full two-token z=5 formula."""
    if r == 0:
        return 0
    s, d = x + y, x - y
    if d == 0:
        t = {1} if y == 1 else ({1, 3} if y == 2 else {1, 3, 5})
    elif d == 1:
        t = {1, 3} if y == 1 else {1, 3, 5, 2*y+3}
    elif d == 2:
        t = {1, 3} if y == 1 else {1, 3, 5}
    elif d in (3, 4):
        t = {1, 3, 5}
    elif d == 5:
        t = {1, 3, 5, 2*y+5}
    elif d == 6:
        t = {1, 3, 5, 2*y+5, 2*y+7, 2*y+9, 2*y+11}
    else:
        t = {1, 3, 5, 2*y+5}
    if r in t:
        return 2
    if d == 0:
        p = y >= 3 and ev(r, 6, s+2)
    elif d == 1:
        p = (r >= 4) if y == 1 else (ev(r, 6, s+3) or r >= s+4)
    elif d == 2:
        p = y >= 2 and ev(r, 6, s)
    elif d == 3:
        p = ev(r, 6, s+1) or r >= s+2
    elif d == 4:
        p = ev(r, 6, s)
    elif d == 5:
        p = ev(r, 6, s-1) or r >= s+1
    elif d == 6:
        p = ev(r, 6, s-2)
    elif d >= 7 and d % 2:
        p = ev(r, 6, 2*y+4) or od(r, 2*y+7, s+4) or r >= s+6
    else:
        p = ev(r, 6, 2*y+4) or od(r, 2*y+7, s+5)
    return int(p)


def h6_y2(x: int, r: int) -> int:
    """K0878: proved z=6,y=2 boundary formula."""
    if r == 0:
        return 0
    if x == 2:
        t, p = {1, 3}, False
    elif x == 3:
        t, p = {1, 3, 5}, r >= 6
    elif x == 4:
        t, p = {1, 3, 5, 7}, False
    elif x == 5:
        t, p = {1, 3, 5}, (r == 7 or r >= 9)
    elif x == 6:
        t, p = {1, 3, 5, 9}, r == 7
    elif x == 7:
        t, p = {1, 3, 5}, (r == 7 or r >= 9)
    elif x == 8:
        t, p = {1, 3, 5}, r in (7, 9)
    elif x == 9:
        t, p = {1, 3, 5, 11, 13, 15, 17}, (r in (7, 9) or ev(r, 12, 16) or r >= 18)
    elif x % 2 == 0:
        t, p = {1, 3, 5, 11}, (r in (7, 9) or ev(r, 12, x+8))
    else:
        t, p = {1, 3, 5, 11}, (r in (7, 9) or ev(r, 12, x+7) or r >= x+9)
    return 2 if r in t else int(p)


def z6_y3(x: int, r: int) -> int:
    """Proposed complete formula for H(R;(x,3);6), x>=3."""
    if r == 0:
        return 0
    if x == 3:
        t, p = {1, 3, 5, 7, 9}, False
    elif x == 4:
        t, p = {1, 3, 5}, (r == 7 or r >= 9)
    elif x == 5:
        t, p = {1, 3, 5}, r in (7, 9)
    elif x == 6:
        t, p = {1, 3, 5}, (r in (7, 9, 11) or r >= 12)
    elif x == 7:
        t, p = {1, 3, 5, 11}, r in (7, 9)
    elif x == 8:
        t, p = {1, 3, 5}, (r in (7, 9, 11) or r >= 12)
    elif x == 9:
        t, p = {1, 3, 5}, r in (7, 9, 11)
    elif x == 10:
        t = {1, 3, 5, 13, 15, 17, 19}
        p = r in (7, 9, 11) or ev(r, 14, 18) or r >= 20
    elif x % 2 == 0:
        t = {1, 3, 5, 13}
        p = r in (7, 9, 11) or ev(r, 14, x+8) or r >= x+10
    else:
        t = {1, 3, 5, 13}
        p = r in (7, 9, 11) or ev(r, 14, x+9)
    return 2 if r in t else int(p)


def options_from_anchors(x: int, r: int) -> set[int]:
    """A/B/C children, with the duplicate A/B move merged at x=3."""
    if r == 0:
        return set()
    if x == 3:
        a = b = h6_y2(3, r-1)
    else:
        a = z6_y3(x-1, r-1)
        b = h6_y2(x, r-1)
    c = 1 ^ h5(x, 3, r-1)
    return {a, b, c}


def expected_signature(x: int, r: int) -> set[int]:
    """Complete A/B/C set table from report.md; digits denote set members."""
    if r == 0:
        return set()
    if x == 3:
        if r % 2:
            return {0, 1} if r <= 9 else {1}
        return {2, 3} if r <= 6 else {1}
    if x == 4:
        if r % 2:
            return {0, 1} if r <= 5 else {0}
        if r <= 6:
            return {2, 3}
        if r == 8:
            return {1, 2}
        if r == 10:
            return {0, 2, 3}
        return {0}
    if x == 5:
        if r % 2:
            if r <= 5:
                return {0, 1}
            if r <= 9:
                return {0}
            return {1}
        return {2, 3} if r <= 6 else {1}
    if x == 6:
        if r % 2:
            return {0, 1} if r <= 5 else {0}
        if r <= 6:
            return {2, 3}
        if r == 8:
            return {1}
        if r == 10:
            return {1, 2}
        return {0}
    if x == 7:
        if r % 2:
            if r in (1, 3, 5, 11):
                return {0, 1}
            if r in (7, 9):
                return {0}
            return {1}
        return {2, 3} if r <= 6 else {1}
    if x == 8:
        if r % 2:
            return {0, 1} if r <= 5 else {0}
        if r <= 6:
            return {2, 3}
        if r in (8, 10):
            return {1}
        if r == 12:
            return {0, 2, 3}
        return {0}
    if x == 9:
        if r % 2:
            if r <= 5:
                return {0, 1}
            if r <= 11:
                return {0}
            return {1}
        if r <= 6:
            return {2, 3}
        if r in (8, 10):
            return {1}
        if r <= 18:
            return {1, 2, 3}
        return {1}
    if x == 10:
        if r % 2:
            if r <= 5:
                return {0, 1}
            if r <= 11:
                return {0}
            if r <= 19:
                return {0, 1}
            return {0}
        if r <= 6:
            return {2, 3}
        if r in (8, 10):
            return {1}
        if r == 12:
            return {1, 2, 3}
        return {0}
    if x == 11:
        if r % 2:
            if r <= 5:
                return {0, 1}
            if r <= 11:
                return {0}
            if r == 13:
                return {0, 1}
            return {1}
        if r <= 6:
            return {2, 3}
        if r in (8, 10):
            return {1}
        if r == 12:
            return {1, 2, 3}
        if r <= 20:
            return {0, 2}
        return {1}
    # x >= 12
    if r >= x + 10:
        return {0} if x % 2 == 0 else {1}
    if r % 2:
        if r <= 5:
            return {0, 1}
        if r <= 11:
            return {0}
        if r == 13:
            return {0, 1}
        return {1}
    if r <= 6:
        return {2, 3}
    if r in (8, 10):
        return {1}
    if r == 12:
        return {1, 2, 3}
    if r == 14:
        return {0, 2}
    return {0}


def main() -> None:
    rng = random.Random(20261117)
    counts = {
        "direct_z6_y3_states": 0,
        "z5_y3_anchor_states": 0,
        "z6_y2_anchor_states": 0,
        "option_signature_states": 0,
        "mex_states": 0,
        "tail_states": 0,
        "random_signature_states": 0,
        "theorem_t_violations": 0,
    }
    failures = []

    # Raw recurrence versus the proposed z=6,y=3 closed form.
    for x in range(3, 46):
        for r in range(0, x + 81):
            got = exact_h(r, (x, 3), 6)
            want = z6_y3(x, r)
            counts["direct_z6_y3_states"] += 1
            if got != want:
                failures.append(["direct", x, r, got, want])
            if got > 2 or (r % 2 == 0 and got > 1):
                counts["theorem_t_violations"] += 1
                failures.append(["theorem-T", x, r, got])

    # Independently check the proved anchors used in the A/B/C proof.
    for x in range(3, 61):
        for r in range(0, 101):
            got = exact_h(r, (x, 3), 5)
            want = h5(x, 3, r)
            counts["z5_y3_anchor_states"] += 1
            if got != want:
                failures.append(["z5-anchor", x, r, got, want])
    for x in range(2, 61):
        for r in range(0, 101):
            got = exact_h(r, (x, 2), 6)
            want = h6_y2(x, r)
            counts["z6_y2_anchor_states"] += 1
            if got != want:
                failures.append(["z6-y2-anchor", x, r, got, want])

    # Check the complete symbolic A/B/C table and its mex consequence.
    for x in range(3, 2001):
        for r in range(1, x + 21):
            got = options_from_anchors(x, r)
            want = expected_signature(x, r)
            counts["option_signature_states"] += 1
            if got != want:
                failures.append(["signature", x, r, sorted(got), sorted(want)])
            if mex(got) != z6_y3(x, r):
                failures.append(["mex", x, r, sorted(got), mex(got), z6_y3(x, r)])
            counts["mex_states"] += 1

    # Theorem T tail: R >= x+10 gives parity of S=x+3.
    for x in range(3, 5001):
        for r in (x+10, x+11, x+12, 2*x+40):
            counts["tail_states"] += 1
            got = z6_y3(x, r)
            want = (x + 3) % 2
            if got != want:
                failures.append(["tail", x, r, got, want])

    # Fixed-seed distant checks of the symbolic signature and mex.
    for _ in range(2000):
        x = rng.randint(3, 1_000_000)
        r = rng.randint(1, x + 40)
        got = options_from_anchors(x, r)
        want = expected_signature(x, r)
        counts["random_signature_states"] += 1
        if got != want or mex(got) != z6_y3(x, r):
            failures.append(["random", x, r, sorted(got), sorted(want),
                             mex(got), z6_y3(x, r)])

    result = {
        "schema": "two-token-z6-y3-audit-v1",
        "claim": "H(R;(x,3);6) is given by the z6_y3 formula in report.md for all x>=3,R>=0",
        "classification": "finite-independent-audit-not-proof",
        "seed": 20261117,
        "counts": counts,
        "total_checks": sum(counts.values()),
        "direct_engine_cache": {
            "hits": exact_h.cache_info().hits,
            "misses": exact_h.cache_info().misses,
        },
        "failures": failures,
        "pass": not failures,
    }
    out = Path(__file__).resolve().parent / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    out.write_text(encoded, encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
