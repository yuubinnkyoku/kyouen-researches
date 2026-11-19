#!/usr/bin/env python3
"""Independent audit for the z=16, y=1 two-token residual-game slice.

The proof itself is the x-outer induction plus the exhaustive symbolic
A/B/C signature partition in report.md. This program audits the transcription
with two direct recurrence engines and independently recomputes child values
from K0832 and K1020.
"""
from __future__ import annotations

import json
import random
from functools import lru_cache


def mex(values):
    values = set(values)
    g = 0
    while g in values:
        g += 1
    return g


@lru_cache(None)
def H_ordered(R: int, X: tuple[int, ...], z: int) -> int:
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1 :], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1 :], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)


@lru_cache(None)
def H_canonical(R: int, X: tuple[int, ...], z: int) -> int:
    X = tuple(sorted(X))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            Y = tuple(sorted(X[:i] + (v - 1,) + X[i + 1 :]))
            opts.add(H_canonical(R - 1, Y, z))
        else:
            opts.add(H_canonical(R - 1, X[:i] + X[i + 1 :], z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)


def single_token(x: int, z: int, R: int) -> int:
    if R == 0 or x <= 0:
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
        m = z if z % 2 else z - 1
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = x if x % 2 else x - 1
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))


# Published K1020: z=15, y=1.
def T15(x: int, r: int) -> bool:
    if x == 1:
        return r == 1
    if x == 16:
        return 1 <= r <= 17 and r % 2 == 1
    if x == 17:
        return 1 <= r <= 33 and r % 2 == 1
    if x <= 15:
        top = x + 1 if x % 2 == 0 else x
        return 1 <= r <= top and r % 2 == 1
    return 1 <= r <= 17 and r % 2 == 1


def P15(x: int, r: int) -> bool:
    if x % 2:
        if x <= 13:
            return False
        if x in (15, 17):
            return r == 16
        return r == 16 or (r % 2 == 1 and 19 <= r <= x + 16)
    if x <= 14:
        return r >= x + 2
    if x == 16:
        return r == 16 or r >= 18
    return r == 16 or (r % 2 == 1 and 19 <= r <= x + 16) or r >= x + 17


def h15(x: int, r: int) -> int:
    if r == 0:
        return 0
    if T15(x, r):
        return 2
    if P15(x, r):
        return 1
    return 0


# Candidate closed form for z=16, y=1.
def T16(x: int, r: int) -> bool:
    if x == 1:
        return r == 1
    if x == 15:
        return 1 <= r <= 17 and r % 2 == 1
    if x == 18:
        return (1 <= r <= 15 or 19 <= r <= 35) and r % 2 == 1
    if x <= 14:
        top = x + 1 if x % 2 == 0 else x
        return 1 <= r <= top and r % 2 == 1
    if x in (16, 17):
        return 1 <= r <= 15 and r % 2 == 1
    return (1 <= r <= 15 or r == 19) and r % 2 == 1


def P16(x: int, r: int) -> bool:
    if x % 2 == 1:
        if x <= 13 or x == 15:
            return False
        if x == 17:
            return r == 17
        return r == 17 or (r % 2 == 0 and 20 <= r <= x + 17)
    if x <= 14:
        return r >= x + 2
    if x == 16:
        return r >= 17
    if x == 18:
        return r == 17 or (r % 2 == 0 and 20 <= r <= 34) or r >= 36
    return r == 17 or (r % 2 == 0 and 20 <= r <= x + 16) or r >= x + 18


def candidate(x: int, R: int) -> int:
    if R == 0:
        return 0
    if T16(x, R):
        return 2
    if P16(x, R):
        return 1
    return 0


def band_signature(x: int, R: int) -> str:
    """Exact set {A,B,C} on the disjoint R bands listed in report.md."""
    if x == 1:
        return "01" if R == 1 else "23" if R == 2 else "1"
    if 2 <= x <= 14:
        if x % 2:
            if R % 2 and R <= x:
                return "01"
            if R % 2 == 0 and R <= x + 1:
                return "23"
            return "1"
        if R % 2 and R <= x + 1:
            return "01"
        if R % 2 == 0 and R <= x:
            return "23"
        if R == x + 2:
            return "03"
        return "0"
    if x == 15:
        if R % 2 and R <= 17:
            return "01"
        if R % 2 == 0 and R <= 16:
            return "23"
        return "1"
    if x == 16:
        if R % 2 and R <= 15:
            return "01"
        if R % 2 == 0 and R <= 16:
            return "23"
        if R == 17:
            return "0"
        if R == 18:
            return "023"
        return "0"
    if x == 17:
        if R % 2 and R <= 15:
            return "01"
        if R % 2 == 0 and R <= 16:
            return "23"
        if R == 17:
            return "0"
        if R == 18:
            return "123"
        if R % 2 and 19 <= R <= 33:
            return "1"
        if R % 2 == 0 and 20 <= R <= 34:
            return "123"
        return "1"
    if x == 18:
        if R % 2 and R <= 15:
            return "01"
        if R % 2 == 0 and R <= 16:
            return "23"
        if R == 17:
            return "0"
        if R == 18:
            return "123"
        if R % 2 and 19 <= R <= 35:
            return "01"
        return "0"
    if x == 19:
        if R % 2 and R <= 15:
            return "01"
        if R % 2 == 0 and R <= 16:
            return "23"
        if R == 17:
            return "0"
        if R == 18:
            return "123"
        if R == 19:
            return "01"
        if R % 2 == 0 and 20 <= R <= 36:
            return "02"
        if R % 2 and 21 <= R <= 35:
            return "1"
        return "1"
    if R % 2 and R <= 15:
        return "01"
    if R % 2 == 0 and R <= 16:
        return "23"
    if R == 17:
        return "0"
    if R == 18:
        return "123"
    if R == 19:
        return "01"
    if R == 20:
        return "02"
    if x % 2 == 0:
        if R % 2 and 21 <= R <= x + 17:
            return "1"
        if R % 2 == 0 and 22 <= R <= x + 16:
            return "0"
        return "0"
    if R % 2 and 21 <= R <= x + 16:
        return "1"
    if R % 2 == 0 and 22 <= R <= x + 17:
        return "0"
    return "1"


def values_of(sig: str) -> set[int]:
    return {int(c) for c in sig}


def run_audit() -> dict:
    audit = {"checks": {}, "fail": [], "n_points": 0}

    def record(name, bad, points, example=None, **extra):
        audit["checks"][name] = {
            "ok": bad == 0,
            "points": points,
            "bad": bad,
            "example": example,
            **extra,
        }
        if bad:
            audit["fail"].append(name)
        audit["n_points"] += points

    # V1-V3: two genuinely separate direct recurrences vs the closed form.
    bad = [0, 0, 0]
    ex = [None, None, None]
    n = 0
    for x in range(1, 81):
        for R in range(0, x + 46):
            n += 1
            a = H_ordered(R, (x, 1), 16)
            b = H_canonical(R, (x, 1), 16)
            c = candidate(x, R)
            for j, ok in enumerate((a == c, b == c, a == b)):
                if not ok:
                    bad[j] += 1
                    if ex[j] is None:
                        ex[j] = (x, R, a, b, c)
    for j, name in enumerate(
        (
            "V1_ordered_direct_vs_formula",
            "V2_canonical_direct_vs_formula",
            "V3_direct_engines_agree",
        )
    ):
        record(name, bad[j], n, ex[j])

    # V4-V8: child-only mex and the complete symbolic signature partition.
    names = (
        "V4_ABC_mex_vs_formula",
        "V5_signature_coverage",
        "V6_signature_vs_child_values",
        "V7_signature_mex_vs_ABC_mex",
        "V8_signature_mex_vs_formula",
    )
    bad = [0] * 5
    ex = [None] * 5
    n = 0
    for x in range(1, 1001):
        for R in range(1, x + 31):
            n += 1
            r = R - 1
            opts = set()
            if x >= 2:
                opts.add(candidate(x - 1, r))
            opts.add(single_token(x, 17, r))
            opts.add(1 ^ h15(x, r))
            am = mex(opts)
            actual = "".join(map(str, sorted(opts)))
            expected = band_signature(x, R)
            checks = (
                am == candidate(x, R),
                expected is not None,
                expected == actual,
                mex(values_of(expected)) == am,
                mex(values_of(expected)) == candidate(x, R),
            )
            for j, ok in enumerate(checks):
                if not ok:
                    bad[j] += 1
                    if ex[j] is None:
                        ex[j] = (x, R, actual, expected, am, candidate(x, R))
    for j, name in enumerate(names):
        record(name, bad[j], n, ex[j])

    # V9: general tail.
    bad = 0
    ex = None
    for x in range(1, 10001):
        for off in range(5):
            R = x + 18 + off
            got = candidate(x, R)
            want = (x + 1) % 2
            if got != want:
                bad += 1
                if ex is None:
                    ex = (x, R, got, want)
    record("V9_tail_R_ge_x_plus_18", bad, 50000, ex)

    # V10: Theorem T parity cap.
    bad = 0
    ex = None
    n = 0
    for x in range(1, 1001):
        for R in range(1, x + 31):
            n += 1
            got = candidate(x, R)
            bound = 2 if R % 2 else 1
            if got > bound:
                bad += 1
                if ex is None:
                    ex = (x, R, got, bound)
    record("V10_theorem_T_parity", bad, n, ex)

    # V11: single-token z=17 anchor.
    bad = 0
    ex = None
    n = 0
    for x in range(1, 81):
        for R in range(0, 81):
            n += 1
            a = H_ordered(R, (x,), 17)
            b = single_token(x, 17, R)
            if a != b:
                bad += 1
                if ex is None:
                    ex = (x, R, a, b)
    record("V11_single_token_z17", bad, n, ex)

    # V12: K1020 child anchor.
    bad = 0
    ex = None
    n = 0
    for x in range(1, 81):
        for R in range(0, x + 46):
            n += 1
            a = H_ordered(R, (x, 1), 15)
            b = h15(x, R)
            if a != b:
                bad += 1
                if ex is None:
                    ex = (x, R, a, b)
    record("V12_K1020_child_anchor", bad, n, ex)

    # V13: fixed-seed large-x spot checks (supporting audit only).
    rng = random.Random(20261119)
    bad = 0
    ex = None
    n = 20000
    for _ in range(n):
        x = rng.randint(1, 100000)
        R = rng.randint(0, x + 50)
        got = candidate(x, R)
        if got > (2 if R % 2 else 1):
            bad += 1
            if ex is None:
                ex = (x, R, got)
    record(
        "V13_fixed_seed_large_x_spots",
        bad,
        n,
        ex,
        seed=20261119,
        x_max=100000,
    )

    # V14: height-only reduction R <= z+1.
    bad = 0
    ex = None
    n = 0
    for x in range(1, 501):
        for R in range(0, 18):
            n += 1
            a = H_ordered(R, (x, 1), 16)
            b = single_token(x + 1, 16, R)
            if a != b:
                bad += 1
                if ex is None:
                    ex = (x, R, a, b)
    record("V14_height_only_R_le_17", bad, n, ex)

    audit["all_pass"] = not audit["fail"]
    audit["cache"] = {
        "ordered": H_ordered.cache_info()._asdict(),
        "canonical": H_canonical.cache_info()._asdict(),
    }
    return audit


if __name__ == "__main__":
    result = run_audit()
    out = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    print(out, end="")
    if not result["all_pass"]:
        raise SystemExit(1)
