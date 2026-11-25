#!/usr/bin/env python3
"""Verify the height-only collapse theorem for the kappa=1 residual game.

Two independent recurrence engines are used:
- H_multiset sorts the positive-token multiset after every move.
- H_ordered preserves token order and labels.

Both are compared with the published single-token closed form.
"""
from functools import lru_cache
from itertools import combinations_with_replacement
import json
import random


@lru_cache(maxsize=None)
def H_multiset(R, X, z):
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
    if R == 0:
        return 0
    options = set()
    for i, x in enumerate(X):
        Y = X[:i] + X[i + 1:]
        if x >= 2:
            options.add(H_ordered(R - 1, Y + (x - 1,), z))
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


def single_exact(x, z, R):
    """The proved single-token formula from K0832."""
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


def run_audit():
    stability_checks = 0
    for s in range(0, 51):
        for r in range(0, 41):
            for z in range(r, r + 4):
                a = single_exact(s, z, r)
                b = single_exact(s, z + 1, r)
                assert a == b, (s, r, z, a, b)
                stability_checks += 1

    multisets = list(all_multisets(4, 5))
    exhaustive_checks = 0
    for X in multisets:
        S = sum(X)
        for R in range(0, 13):
            for z in range(max(0, R - 1), R + 2):
                hm = H_multiset(R, X, z)
                ho = H_ordered(R, tuple(reversed(X)), z)
                hs = single_exact(S, z, R)
                assert hm == ho == hs, (X, S, R, z, hm, ho, hs)
                exhaustive_checks += 1

    small_R_checks = 0
    for X in multisets:
        S = sum(X)
        for R in range(3):
            for z in range(0, 10):
                hm = H_multiset(R, X, z)
                hs = single_exact(S, z, R)
                assert hm == hs, (X, S, R, z, hm, hs)
                small_R_checks += 1

    rng = random.Random(20261116)
    random_checks = 0
    for _ in range(160):
        n = rng.randint(0, 5)
        X = tuple(rng.randint(1, 12) for _ in range(n))
        S = sum(X)
        R = rng.randint(0, 20)
        z = max(0, R - 1) + rng.randint(0, 8)
        hm = H_multiset(R, tuple(sorted(X)), z)
        ho = H_ordered(R, X, z)
        hs = single_exact(S, z, R)
        assert hm == ho == hs, (X, S, R, z, hm, ho, hs)
        random_checks += 1

    sharpness_checks = 0
    for R in range(3, 41):
        if R % 2:
            k = R
            expected_general = 2
        else:
            k = R - 1
            expected_general = 1
        z = R - 2
        X = (1,) * k
        hm = H_multiset(R, X, z)
        hs = single_exact(k, z, R)
        assert hm == expected_general, (R, k, z, hm, expected_general)
        assert hs == 0, (R, k, z, hs)
        sharpness_checks += 1

    return {
        "theorem": "For kappa=1, H(R;X;z)=H(R;(sum(X));z) whenever R<=z+1; for R<=2 this holds for every z.",
        "stability_lemma": {
            "claim": "v(s,z,r)=v(s,z+1,r) for z>=r",
            "checks": stability_checks,
            "mismatches": 0
        },
        "exhaustive": {
            "multisets": "length 0..4, entries 1..5",
            "R": "0..12",
            "z": "max(0,R-1)..R+1",
            "checks": exhaustive_checks,
            "mismatches": 0
        },
        "small_R_all_z": {
            "multisets": "length 0..4, entries 1..5",
            "R": "0..2",
            "z": "0..9",
            "checks": small_R_checks,
            "mismatches": 0
        },
        "seeded_random": {
            "seed": 20261116,
            "checks": random_checks,
            "n": "0..5",
            "entries": "1..12",
            "R": "0..20",
            "z": "max(0,R-1) plus 0..8",
            "mismatches": 0
        },
        "uniform_threshold_sharpness": {
            "R": "3..40",
            "witness": "X=(1^R), z=R-2 for odd R; X=(1^(R-1)), z=R-2 for even R",
            "checks": sharpness_checks,
            "all_mismatch_general_vs_single": True
        },
        "engines": ["sorted multiset recurrence", "ordered labeled-token recurrence", "published single-token closed form"]
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), ensure_ascii=False, indent=2, sort_keys=True))
