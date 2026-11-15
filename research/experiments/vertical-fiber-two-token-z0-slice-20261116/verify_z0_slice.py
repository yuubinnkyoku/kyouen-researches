#!/usr/bin/env python3
"""Exact finite audit for the z=0 two-token residual-game slice.

The theorem is proved in report.md by strong induction on R.  This script
corroborates it on a finite grid using two separately represented recurrences:
(1) sorted multisets with the already-proved cap_{R+1} lemma, and
(2) ordered labeled tokens without capping.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path


def mex(values: set[int]) -> int:
    g = 0
    while g in values:
        g += 1
    return g


def make_canonical_engine():
    @lru_cache(maxsize=None)
    def H(R: int, X: tuple[int, ...], z: int) -> int:
        if R == 0:
            return 0
        X = tuple(sorted(min(t, R + 1) for t in X))
        options: set[int] = set()
        for i, t in enumerate(X):
            if t >= 2:
                Y = list(X)
                Y[i] = t - 1
                options.add(H(R - 1, tuple(sorted(Y)), z))
            else:
                options.add(H(R - 1, X[:i] + X[i + 1 :], z + 1))
        if z >= 1:
            options.add(1 ^ H(R - 1, X, z - 1))
        return mex(options)

    return H


def make_labeled_engine():
    @lru_cache(maxsize=None)
    def H(R: int, X: tuple[int, ...], z: int) -> int:
        if R == 0:
            return 0
        options: set[int] = set()
        for i, t in enumerate(X):
            if t >= 2:
                options.add(H(R - 1, X[:i] + (t - 1,) + X[i + 1 :], z))
            else:
                options.add(H(R - 1, X[:i] + X[i + 1 :], z + 1))
        if z >= 1:
            options.add(1 ^ H(R - 1, X, z - 1))
        return mex(options)

    return H


def formula(x: int, y: int, R: int) -> int:
    assert x >= y >= 1 and R >= 0
    S = x + y
    if R <= 2 * y:
        return R % 2
    if x > y and R == 2 * y + 1:
        return 2
    if x > y and R <= S:
        return 1 - (R % 2)
    return S % 2


def run_grid(max_x: int) -> dict:
    canonical = make_canonical_engine()
    labeled = make_labeled_engine()
    checks = 0
    first_mismatch = None

    for x in range(1, max_x + 1):
        for y in range(1, x + 1):
            # The tail theorem starts at R >= x+y+1; +4 also checks beyond it.
            for R in range(0, x + y + 5):
                a = canonical(R, (x, y), 0)
                b = labeled(R, (x, y), 0)
                f = formula(x, y, R)
                checks += 1
                if a != b or a != f:
                    first_mismatch = {
                        "x": x,
                        "y": y,
                        "R": R,
                        "canonical": a,
                        "labeled": b,
                        "formula": f,
                    }
                    break
            if first_mismatch is not None:
                break
        if first_mismatch is not None:
            break

    return {
        "max_x": max_x,
        "checks": checks,
        "mismatches": 0 if first_mismatch is None else 1,
        "first_mismatch": first_mismatch,
        "canonical_cache": {
            "hits": canonical.cache_info().hits,
            "misses": canonical.cache_info().misses,
        },
        "labeled_cache": {
            "hits": labeled.cache_info().hits,
            "misses": labeled.cache_info().misses,
        },
    }


def main() -> None:
    first = run_grid(60)
    second = run_grid(60)
    audit = {
        "date": "2026-11-16",
        "subject": "two-token residual game, z=0 full Grundy slice",
        "status": "theorem; finite audit is corroboration only",
        "engines": [
            "sorted-multiset recursion with the proved cap_{R+1} lemma",
            "ordered labeled-token recursion without capping",
        ],
        "formula": (
            "R mod 2 for 0<=R<=2y; 2 if x>y and R=2y+1; "
            "1-(R mod 2) if x>y and 2y+2<=R<=x+y; "
            "(x+y) mod 2 if R>=x+y+1"
        ),
        "audit": first,
        "second_run_identical": first == second,
    }
    encoded = json.dumps(audit, indent=2, sort_keys=True) + "\n"
    if first != second:
        raise SystemExit("non-deterministic audit")
    if first["mismatches"] != 0:
        raise SystemExit("formula mismatch")
    Path("output").mkdir(exist_ok=True)
    Path("output/audit.json").write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
