#!/usr/bin/env python3
"""Independent finite audit of the two-token residual game at z=1."""
from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path


def mex(values: set[int]) -> int:
    g = 0
    while g in values:
        g += 1
    return g


def formula(x: int, y: int, r: int) -> int:
    assert x >= y >= 1 and r >= 0
    s, d = x + y, x - y
    if r == 0:
        return 0
    if r == 1:
        return 2
    if r == 2:
        return 1
    if 3 <= r <= 2 * y:
        return (r + 1) & 1
    if r == 2 * y + 1:
        return 2 if d else 0
    if 2 * y + 2 <= r <= s:
        return r & 1
    if r == s + 1:
        if d == 1:
            return s & 1
        if d == 2:
            return 2
        return r & 1
    return s & 1


def make_canonical_engine():
    @lru_cache(maxsize=None)
    def H(r: int, X: tuple[int, ...], z: int) -> int:
        if r == 0:
            return 0
        X = tuple(sorted(min(t, r + 1) for t in X))
        options: set[int] = set()
        for i, t in enumerate(X):
            if t >= 2:
                Y = list(X)
                Y[i] = t - 1
                options.add(H(r - 1, tuple(sorted(Y)), z))
            else:
                options.add(H(r - 1, X[:i] + X[i + 1 :], z + 1))
        if z >= 1:
            options.add(1 ^ H(r - 1, X, z - 1))
        return mex(options)
    return H


def make_labeled_engine():
    @lru_cache(maxsize=None)
    def H(r: int, X: tuple[int, ...], z: int) -> int:
        if r == 0:
            return 0
        options: set[int] = set()
        for i, t in enumerate(X):
            if t >= 2:
                options.add(H(r - 1, X[:i] + (t - 1,) + X[i + 1 :], z))
            else:
                options.add(H(r - 1, X[:i] + X[i + 1 :], z + 1))
        if z >= 1:
            options.add(1 ^ H(r - 1, X, z - 1))
        return mex(options)
    return H


def run_grid(max_x: int) -> dict:
    canonical, labeled = make_canonical_engine(), make_labeled_engine()
    checks = engine_bad = formula_bad = 0
    first_mismatch = None
    for x in range(1, max_x + 1):
        for y in range(1, x + 1):
            for r in range(x + y + 8):
                a = canonical(r, (x, y), 1)
                b = labeled(r, (x, y), 1)
                f = formula(x, y, r)
                checks += 1
                engine_bad += a != b
                formula_bad += a != f
                if first_mismatch is None and (a != b or a != f):
                    first_mismatch = {
                        "x": x, "y": y, "R": r,
                        "canonical": a, "labeled": b, "formula": f,
                    }
    return {
        "max_x": max_x,
        "checks": checks,
        "engine_disagreements": engine_bad,
        "formula_disagreements": formula_bad,
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


def run_parity_and_tail(max_x: int) -> dict:
    H = make_canonical_engine()
    parity_checks = parity_failures = tail_checks = tail_failures = 0
    for x in range(1, max_x + 1):
        for y in range(1, x + 1):
            s = x + y
            for r in range(s + 12):
                value = H(r, (x, y), 1)
                parity_checks += 1
                if (r % 2 == 0 and value > 1) or (r % 2 == 1 and value > 2):
                    parity_failures += 1
                if r >= s + 2:
                    tail_checks += 1
                    if value != (s & 1):
                        tail_failures += 1
    return {
        "parity_checks": parity_checks,
        "parity_failures": parity_failures,
        "tail_checks": tail_checks,
        "tail_failures": tail_failures,
    }


def main() -> None:
    first, second = run_grid(80), run_grid(80)
    structural = run_parity_and_tail(80)
    audit = {
        "date": "2026-11-16",
        "subject": "two-token residual game, z=1 full Grundy slice",
        "status": "theorem; finite audits are independent corroboration only",
        "formula": (
            "0 at R=0; 2 at R=1; 1 at R=2; (R+1) mod 2 for "
            "3<=R<=2y; 2 at R=2y+1 iff x>y (otherwise 0); "
            "R mod 2 for 2y+2<=R<=x+y; at R=x+y+1 use 1 if x-y=1, "
            "2 if x-y=2, otherwise R mod 2; (x+y) mod 2 for R>=x+y+2"
        ),
        "engines": [
            "sorted multiset recursion with proved cap_{R+1} lemma",
            "ordered labeled-token recursion without capping",
        ],
        "audit": first,
        "second_run_identical": first == second,
        "structural_checks": structural,
    }
    encoded = json.dumps(audit, indent=2, sort_keys=True) + "\n"
    if first != second:
        raise SystemExit("non-deterministic audit")
    if first["engine_disagreements"] or first["formula_disagreements"]:
        raise SystemExit("engine/formula mismatch")
    if structural["parity_failures"] or structural["tail_failures"]:
        raise SystemExit("structural invariant mismatch")
    Path("output").mkdir(exist_ok=True)
    Path("output/audit.json").write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
