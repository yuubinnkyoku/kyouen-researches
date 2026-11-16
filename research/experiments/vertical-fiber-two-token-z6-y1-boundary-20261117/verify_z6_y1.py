#!/usr/bin/env python3
"""Independent recurrence audit for the two-token residual slice z=6, y=1.

Uses only the Python standard library.  The proof is in report.md; this
program checks the published formula, its A/B/C option-signature table,
the z=5 and single-token anchors, and a bounded direct recurrence engine.
"""
from __future__ import annotations

import hashlib
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


def qodd(n: int) -> int:
    return n if n % 2 else n - 1


@lru_cache(None)
def exact_h(R: int, X: tuple[int, ...], z: int) -> int:
    """Direct ordered-token recurrence; no formula or cap reduction."""
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


def single_token(x: int, z: int, R: int) -> int:
    """K0832 single-token theorem, used only at z=7."""
    if R == 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        threshold = qodd(z)
        terminal = x + z
        if R % 2 and R <= threshold:
            return 2
        if R % 2 == 0 and R <= threshold:
            return 0
        if threshold < R < terminal:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        threshold = qodd(x)
        if R % 2 and R <= threshold:
            return 2
        if R % 2 == 0 and R <= threshold:
            return 0
        return x % 2
    raise AssertionError((x, z, R))


def z5_y1(x: int, R: int) -> int:
    """Previously proved H(R;(x,1);5) boundary slice (K0873)."""
    if R == 0:
        return 0
    if x == 1:
        return 2 if R == 1 else 0
    if x in (2, 3):
        twos = {1, 3}
    elif x in (4, 5):
        twos = {1, 3, 5}
    elif x == 6:
        twos = {1, 3, 5, 7}
    elif x == 7:
        twos = {1, 3, 5, 7, 9, 11, 13}
    else:
        twos = {1, 3, 5, 7}
    if R in twos:
        return 2
    if x == 2:
        return int(R >= 4)
    if x == 3:
        return 0
    if x == 4:
        return int(R >= 6)
    if x == 5:
        return int(R == 6)
    if x == 6:
        return int(R == 6 or R >= 8)
    if x == 7:
        return int(R == 6)
    if x >= 8 and x % 2 == 0:
        return int(R == 6 or (R % 2 == 1 and 9 <= R <= x + 5) or R >= x + 7)
    if x >= 9 and x % 2 == 1:
        return int(R == 6 or (R % 2 == 1 and 9 <= R <= x + 6))
    return 0


def z6_y1(x: int, R: int) -> int:
    """Proposed complete formula for H(R;(x,1);6)."""
    if R == 0:
        return 0
    if x == 1:
        twos = {1}
    elif x in (2, 3):
        twos = {1, 3}
    elif x == 4:
        twos = {1, 3, 5}
    elif x == 5:
        twos = {1, 3, 5, 7}
    elif x in (6, 7):
        twos = {1, 3, 5}
    elif x == 8:
        twos = {1, 3, 5, 9, 11, 13, 15}
    else:
        twos = {1, 3, 5, 9}
    if R in twos:
        return 2
    if x == 1:
        return 0
    if x == 2:
        return int(R >= 4)
    if x == 3:
        return 0
    if x == 4:
        return int(R >= 6)
    if x == 5:
        return 0
    if x == 6:
        return int(R >= 7)
    if x == 7:
        return int(R == 7)
    if x >= 8 and x % 2 == 0:
        return int(R == 7 or (R % 2 == 0 and 10 <= R <= x + 6) or R >= x + 8)
    if x >= 9 and x % 2 == 1:
        return int(R == 7 or (R % 2 == 0 and 10 <= R <= x + 7))
    return 0


def option_values_from_anchors(x: int, R: int) -> set[int]:
    """Reconstruct A/B/C children from already proved anchor formulas."""
    if R == 0:
        return set()
    if x == 1:
        # Both tokens are 1, so either B move gives the same one-token child.
        options = [single_token(1, 7, R - 1)]
    else:
        options = [
            z6_y1(x - 1, R - 1),       # A
            single_token(x, 7, R - 1),  # B
        ]
    options.append(1 ^ z5_y1(x, R - 1))  # C
    return set(options)


def expected_option_signature(x: int, R: int) -> set[int]:
    """Literal finite-case table used in the R-induction proof."""
    s = lambda *values: set(values)
    if R == 0:
        return set()
    if x == 1:
        if R == 1:
            return s(0, 1)
        if R == 2:
            return s(2, 3)
        return s(1)
    if x == 2:
        if R in (1, 3):
            return s(0, 1)
        if R == 2:
            return s(2, 3)
        if R == 4:
            return s(0, 3)
        return s(0)
    if x == 3:
        if R in (1, 3):
            return s(0, 1)
        if R in (2, 4):
            return s(2, 3)
        return s(1)
    if x == 4:
        if R in (1, 3, 5):
            return s(0, 1)
        if R in (2, 4):
            return s(2, 3)
        if R == 6:
            return s(0, 3)
        return s(0)
    if x == 5:
        if R in (1, 3, 5, 7):
            return s(0, 1)
        if R in (2, 4, 6):
            return s(2, 3)
        return s(1)
    if x == 6:
        if R in (1, 3, 5):
            return s(0, 1)
        if R in (2, 4, 6):
            return s(2, 3)
        if R == 7:
            return s(0)
        if R == 8:
            return s(0, 2, 3)
        return s(0)
    if x == 7:
        if R in (1, 3, 5):
            return s(0, 1)
        if R in (2, 4, 6):
            return s(2, 3)
        if R == 7:
            return s(0)
        if R % 2 == 0 and 8 <= R <= 14:
            return s(1, 2, 3)
        return s(1)
    if x == 8:
        if R in (1, 3, 5):
            return s(0, 1)
        if R in (2, 4, 6):
            return s(2, 3)
        if R == 7:
            return s(0)
        if R == 8:
            return s(1, 2, 3)
        if R % 2 == 1 and 9 <= R <= 15:
            return s(0, 1)
        return s(0)
    if R in (1, 3, 5):
        return s(0, 1)
    if R in (2, 4, 6):
        return s(2, 3)
    if R == 7:
        return s(0)
    if R == 8:
        return s(1, 2, 3)
    if R == 9:
        return s(0, 1)
    if R == 10:
        return s(0, 2)
    if x == 9:
        if R % 2 == 1:
            return s(1)
        return s(0, 2) if R <= 16 else s(1)
    if x % 2 == 0:
        if R % 2 == 1:
            return s(1) if R <= x + 7 else s(0)
        return s(0)
    if R % 2 == 1:
        return s(1)
    return s(0) if R <= x + 7 else s(1)


def main() -> None:
    rng = random.Random(20261117)
    counts = {
        "direct_two_token_states": 0,
        "single_token_anchor_states": 0,
        "z5_boundary_anchor_states": 0,
        "option_signature_states": 0,
        "tail_states": 0,
        "random_states": 0,
    }
    failures = []

    # Independent direct recurrence against the candidate.
    for x in range(1, 61):
        for R in range(0, 121):
            got = exact_h(R, (x, 1), 6)
            want = z6_y1(x, R)
            counts["direct_two_token_states"] += 1
            if got != want:
                failures.append(["direct", x, R, got, want])

    # Verify the two published anchors against the same direct engine.
    for x in range(1, 81):
        for R in range(0, 101):
            got = exact_h(R, (x,), 7)
            want = single_token(x, 7, R)
            counts["single_token_anchor_states"] += 1
            if got != want:
                failures.append(["single", x, R, got, want])
            got = exact_h(R, (x, 1), 5)
            want = z5_y1(x, R)
            counts["z5_boundary_anchor_states"] += 1
            if got != want:
                failures.append(["z5", x, R, got, want])

    # Reconstruct all A/B/C option sets and check the induction table + mex.
    for x in range(1, 2001):
        for R in range(0, x + 25):
            got_options = option_values_from_anchors(x, R)
            expected = expected_option_signature(x, R)
            counts["option_signature_states"] += 1
            if got_options != expected:
                failures.append(["options", x, R, sorted(got_options), sorted(expected)])
            got = z6_y1(x, R)
            want = mex(got_options)
            if got != want:
                failures.append(["mex", x, R, got, want, sorted(got_options)])

    # The known tail theorem gives H(R;(x,1);6)=(x+1) mod 2 for R>=x+8.
    for x in range(1, 5001):
        for R in (x + 8, x + 9, x + 10, 2 * x + 25):
            counts["tail_states"] += 1
            got = z6_y1(x, R)
            want = (x + 1) % 2
            if got != want:
                failures.append(["tail", x, R, got, want])

    # Deterministic far-out spot checks of the recurrence identity.
    for _ in range(2000):
        x = rng.randint(1, 100_000)
        R = rng.randint(0, 2 * x + 100)
        options = option_values_from_anchors(x, R)
        counts["random_states"] += 1
        got = z6_y1(x, R)
        want = mex(options)
        if got != want:
            failures.append(["random", x, R, got, want, sorted(options)])

    script_path = Path(__file__).resolve()
    result = {
        "schema": "two-token-z6-y1-audit-v1",
        "claim": "H(R;(x,1);6) is given by the z6_y1 formula in report.md",
        "classification": "finite-independent-audit-not-proof",
        "seed": 20261117,
        "counts": counts,
        "total_checks": sum(counts.values()),
        "failures": failures,
        "direct_engine_cache": {
            "hits": exact_h.cache_info().hits,
            "misses": exact_h.cache_info().misses,
        },
        "pass": not failures,
    }
    out = script_path.parent / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
