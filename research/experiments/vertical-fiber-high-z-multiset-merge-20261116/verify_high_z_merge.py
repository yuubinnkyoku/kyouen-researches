#!/usr/bin/env python3
"""Verify the large-z merging theorem for the kappa=1 residual game.

The theorem itself is proved in report.md by induction on R.  This verifier
uses two independently represented recurrences:
  * sorted multiset states;
  * ordered/labeled token states, with no sorting during transitions.
It checks both against the closed high-z formula on exhaustive and seeded
finite samples, and records a counterexample outside the sufficient region.
"""
from functools import lru_cache
from itertools import combinations_with_replacement
import json
import random


@lru_cache(maxsize=None)
def H_multiset(R, X, z):
    """Canonical sorted-multiset recurrence."""
    if R == 0:
        return 0
    options = set()
    for x in set(X):
        Y = list(X)
        Y.remove(x)
        if x >= 2:
            Y.append(x - 1)
            Y.sort()
            options.add(H_multiset(R - 1, tuple(Y), z))
        else:
            Y.sort()
            options.add(H_multiset(R - 1, tuple(Y), z + 1))
    if z >= 1:
        options.add(1 ^ H_multiset(R - 1, X, z - 1))
    g = 0
    while g in options:
        g += 1
    return g


@lru_cache(maxsize=None)
def H_ordered(R, X, z):
    """Ordered/labeled recurrence; token order is preserved, never canonicalized."""
    if R == 0:
        return 0
    options = set()
    for i, x in enumerate(X):
        Y = X[:i] + X[i + 1:]
        if x >= 2:
            Y = Y + (x - 1,)
            options.add(H_ordered(R - 1, Y, z))
        else:
            options.add(H_ordered(R - 1, Y, z + 1))
    if z >= 1:
        options.add(1 ^ H_ordered(R - 1, X, z - 1))
    g = 0
    while g in options:
        g += 1
    return g


def odd_floor(n):
    return n if n % 2 else n - 1


def high_formula(total, R):
    """Single-token value in the stable z >= total+1 region."""
    if total == 0:
        return 0
    q = odd_floor(total)
    if R % 2:
        return 2 if R <= q else total % 2
    return 0 if R <= q else total % 2


def single_exact(x, z, R):
    """Published all-parameter single-token closed form."""
    if x == 0:
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
        q = odd_floor(z)
        if R % 2 and R <= q:
            return 2
        if R % 2 == 0 and R <= q:
            return 0
        if q < R < x + z:
            return (R + z) % 2
        return x % 2
    q = odd_floor(x)
    if R % 2 and R <= q:
        return 2
    if R % 2 == 0 and R <= q:
        return 0
    return x % 2


def all_multisets(max_len, max_value):
    yield ()
    for n in range(1, max_len + 1):
        yield from combinations_with_replacement(range(1, max_value + 1), n)


def main():
    checks = 0
    for X in all_multisets(4, 5):
        total = sum(X)
        for R in range(17):
            z0 = max(0, total + R - 1)
            for z in range(z0, z0 + 4):
                a = H_multiset(R, X, z)
                b = H_ordered(R, X, z)
                c = high_formula(total, R)
                checks += 1
                assert a == b == c, (X, total, z, R, a, b, c)

    rng = random.Random(20261116)
    random_checks = 0
    for _ in range(120):
        n = rng.randint(0, 6)
        X = tuple(rng.randint(1, 10) for _ in range(n))
        total = sum(X)
        R = rng.randint(0, 28)
        z = max(0, total + R - 1) + rng.randint(0, 8)
        a = H_multiset(R, tuple(sorted(X)), z)
        b = H_ordered(R, X, z)
        c = high_formula(total, R)
        random_checks += 1
        assert a == b == c, (X, total, z, R, a, b, c)

    # The sufficient region is not claimed to be necessary.
    X, z, R = (2, 3), 5, 9
    total = sum(X)
    boundary = {
        "X": list(X),
        "sum_X": total,
        "z": z,
        "R": R,
        "condition_z_ge_sum_plus_R_minus_1": z >= total + R - 1,
        "general_H": H_multiset(R, X, z),
        "single_token_H": single_exact(total, z, R),
    }
    assert boundary["general_H"] == 1
    assert boundary["single_token_H"] == 2
    assert boundary["condition_z_ge_sum_plus_R_minus_1"] is False

    print(json.dumps({
        "theorem": "kappa=1; z >= sum(X)+R-1 implies H(R;X;z)=H(R;(sum(X));z)",
        "exhaustive": {
            "multisets": "length 0..4, entries 1..5",
            "R": "0..16",
            "z": "max(0,sum(X)+R-1)..that+3",
            "checks": checks,
            "mismatches": 0,
        },
        "seeded_random": {
            "seed": 20261116,
            "checks": random_checks,
            "n": "0..6",
            "entries": "1..10",
            "R": "0..28",
            "z": "max(0,sum(X)+R-1) plus 0..8",
            "mismatches": 0,
        },
        "outside_region_example": boundary,
        "engines": ["sorted multiset recurrence", "ordered/labeled recurrence"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
