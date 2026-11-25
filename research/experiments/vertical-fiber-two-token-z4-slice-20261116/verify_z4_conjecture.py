#!/usr/bin/env python3
"""Finite audit of the two-token residual game at z=4 (CONJECTURE, not a theorem).

Checks, with two independent engines (capped canonical multiset recursion and
uncapped ordered labeled recursion):
  1. grid agreement of both engines with the candidate closed form F_4,
  2. induction-step consistency: option values built ONLY from the closed
     forms (A/B-children from F_4 and the proved single-token form at z=5,
     C-child from the proved z=3 slice) mex to F_4 itself,
  3. parity/tail structural checks,
  4. anchors: the proved z=3 slice and the proved single-token closed form
     against the raw engine (boundary inputs of the would-be induction),
  5. fixed-seed scatter.

The universal statement remains a conjecture: finite audits are not proofs.
"""
from __future__ import annotations

import json
import random
import sys
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(300000)
OUT = Path(__file__).resolve().parent / "output" / "audit.json"


def mex(values: set[int]) -> int:
    g = 0
    while g in values:
        g += 1
    return g


def make_canonical_engine():
    @lru_cache(maxsize=None)
    def inner(R: int, X: tuple[int, ...], z: int) -> int:
        if R == 0:
            return 0
        options: set[int] = set()
        for i, token in enumerate(X):
            if token >= 2:
                child = list(X)
                child[i] = token - 1
                options.add(value(R - 1, tuple(sorted(child)), z))
            else:
                options.add(value(R - 1, X[:i] + X[i + 1:], z + 1))
        if z >= 1:
            options.add(1 ^ value(R - 1, X, z - 1))
        return mex(options)

    def value(R: int, X: tuple[int, ...], z: int) -> int:
        if R == 0:
            return 0
        capped = tuple(sorted(min(t, R + 1) for t in X))
        return inner(R, capped, z)

    return value


def make_labeled_engine():
    @lru_cache(maxsize=None)
    def value(R: int, X: tuple[int, ...], z: int) -> int:
        if R == 0:
            return 0
        options: set[int] = set()
        for i, token in enumerate(X):
            if token >= 2:
                options.add(value(R - 1, X[:i] + (token - 1,) + X[i + 1:], z))
            else:
                options.add(value(R - 1, X[:i] + X[i + 1:], z + 1))
        if z >= 1:
            options.add(1 ^ value(R - 1, X, z - 1))
        return mex(options)

    return value


def q_odd(n: int) -> int:
    return n if n & 1 else n - 1


def single_token(x: int, z: int, R: int) -> int:
    """Proved H(R;(x);z) for all x>=1, z>=0, R>=0."""
    if R == 0:
        return 0
    if z == 0:
        return min(R, x) & 1
    if z == x:
        if R & 1 and R <= 2 * x - 1:
            return 2
        if not (R & 1) and R <= x - 1:
            return 0
        return x & 1
    if 1 <= z <= x - 1:
        threshold = q_odd(z)
        last = x + z + 1
        if R & 1 and R <= threshold:
            return 2
        if not (R & 1) and R <= threshold:
            return 0
        if threshold < R < last - 1:
            return (R + z) & 1
        return x & 1
    if z >= x + 1:
        threshold = q_odd(x)
        if R & 1 and R <= threshold:
            return 2
        if not (R & 1) and R <= threshold:
            return 0
        return x & 1
    raise AssertionError((x, z, R))


def z3_slice(x: int, y: int, R: int) -> int:
    """Proved H(R;(x,y);3) (z=3 slice theorem, landed on main)."""
    S = x + y
    d = x - y
    if (x, y) == (1, 1):
        T = {1}
    else:
        T = {1, 3}
        if d == 3:
            T.add(S)
        if d == 4:
            T |= {2 * y + 3, 2 * y + 5, 2 * y + 7}
        if d >= 5:
            T.add(2 * y + 3)
    if R in T:
        return 2
    # value-1 sets per the z=3 theorem
    if d in (0, 2, 4):
        O: set[int] = set()
        if d in (0, 2):
            if 4 <= R <= S and R % 2 == 0:
                return 1
        if d == 4:
            if 4 <= R <= 2 * y + 2 and R % 2 == 0:
                return 1
        return 0
    if d in (1, 3):
        if R >= S + 1:
            return 1
        if 4 <= R <= min(S, 2 * y + 2) and R % 2 == 0:
            return 1
        return 0
    if d >= 5 and d % 2 == 1:
        if R >= S + 4:
            return 1
        if R % 2 == 1 and R >= 2 * y + 5:
            return 1
        if 4 <= R <= 2 * y + 2 and R % 2 == 0:
            return 1
        return 0
    if d >= 6 and d % 2 == 0:
        if 4 <= R <= 2 * y + 2 and R % 2 == 0:
            return 1
        if R % 2 == 1 and 2 * y + 5 <= R <= S + 3:
            return 1
        return 0
    raise AssertionError((x, y, R))


def z4_candidate(x: int, y: int, R: int) -> int:
    """Conjectured H(R;(x,y);4)."""
    if R == 0:
        return 0
    if x < y:
        x, y = y, x
    S = x + y
    d = x - y
    if (x, y) == (1, 1):
        return 2 if R == 1 else 0
    if R in (1, 3):
        return 2
    if d == 0 and y == 2 and R == S + 1:
        return 2
    if d == 2 and R == 2 * y + 3:
        return 2
    if d == 5 and R in (S, S + 2, S + 4):
        return 2
    if d >= 6 and R == 2 * y + 5:
        return 2
    # value-1 sets
    if d == 0:
        return 1 if (5 <= R <= 2 * y + 1 and R % 2 == 1) else 0
    if d == 1:
        if (5 <= R <= 2 * y + 3 and R % 2 == 1) or R >= 2 * y + 4 or ((x, y) == (2, 1) and R == 4):
            return 1
        return 0
    if d == 2:
        return 1 if (5 <= R <= 2 * y + 1 and R % 2 == 1) else 0
    if d == 3:
        return 1 if ((5 <= R <= 2 * y + 3 and R % 2 == 1) or R >= 2 * y + 4) else 0
    if d == 4:
        return 1 if (5 <= R <= 2 * y + 3 and R % 2 == 1) else 0
    if d >= 5 and d % 2 == 1:
        if (5 <= R <= 2 * y + 3 and R % 2 == 1):
            return 1
        if R % 2 == 0 and 2 * y + 6 <= R <= S + 5:
            return 1
        if R >= S + 6:
            return 1
        return 0
    if d >= 6 and d % 2 == 0:
        if (5 <= R <= 2 * y + 3 and R % 2 == 1):
            return 1
        if R % 2 == 0 and 2 * y + 6 <= R <= S + 4:
            return 1
        return 0
    raise AssertionError((x, y, R))


def z4_options_from_closed_forms(x: int, y: int, R: int) -> set[int]:
    """Option value set at (x,y,R,z=4) using ONLY closed forms for the children.

    A-child: decrement a token >=2, stays at z=4 -> z4_candidate.
    B-child: remove a token 1, z -> 5: two-token if the other token remains,
             single-token if it was the last.
    C-child: z -> 3 -> 1 XOR z3_slice.
    """
    options: set[int] = set()
    for tok in (x, y):
        if tok >= 2:
            other = y if tok == x else x
            a, b = sorted((tok - 1, other), reverse=True)
            options.add(z4_candidate(a, b, R - 1))
        else:
            other = y if tok == x else x
            options.add(single_token(other, 5, R - 1))
    options.add(1 ^ z3_slice(x, y, R - 1))
    return options


def audit(max_x: int = 24, extra: int = 8, scatter: int = 200) -> dict:
    canon = make_canonical_engine()
    labeled = make_labeled_engine()
    checks = {}

    # 1. three-way grid agreement
    n = 0
    bad3: list[tuple] = []
    for x in range(1, max_x + 1):
        for y in range(1, x + 1):
            S = x + y
            for R in range(0, S + extra + 1):
                vc = canon(R, (x, y), 4)
                vl = labeled(R, (x, y), 4)
                vf = z4_candidate(x, y, R)
                n += 1
                if not (vc == vl == vf):
                    bad3.append((x, y, R, vc, vl, vf))
    checks["grid_states"] = n
    checks["grid_mismatches"] = len(bad3)
    checks["grid_bad_first"] = bad3[:5]

    # 2. induction-step consistency (mex of closed-form options == candidate)
    ni = 0
    badi: list[tuple] = []
    for x in range(1, max_x + 1):
        for y in range(1, x + 1):
            S = x + y
            for R in range(1, S + extra + 1):
                opts = z4_options_from_closed_forms(x, y, R)
                m = mex(opts)
                ni += 1
                if m != z4_candidate(x, y, R):
                    badi.append((x, y, R, sorted(opts), m))
    checks["induction_steps_checked"] = ni
    checks["induction_mismatches"] = len(badi)
    checks["induction_bad_first"] = badi[:5]

    # 3. tail/parity: R >= S+5 -> H == S mod 2 ; even R -> H <= 1; odd R -> H <= 2
    nt = npar = 0
    badt: list[tuple] = []
    badpar: list[tuple] = []
    for x in range(1, max_x + 1):
        for y in range(1, x + 1):
            S = x + y
            for R in range(0, S + extra + 1):
                v = z4_candidate(x, y, R)
                if R >= S + 5:
                    nt += 1
                    if v != (S & 1):
                        badt.append((x, y, R, v))
                npar += 1
                if R % 2 == 0 and v > 1:
                    badpar.append((x, y, R, v))
                if R % 2 == 1 and v > 2:
                    badpar.append((x, y, R, v))
    checks["tail_checked"] = nt
    checks["tail_violations"] = len(badt)
    checks["parity_checked"] = npar
    checks["parity_violations"] = len(badpar)

    # 4. anchors: proved z=3 slice and single-token z=5 vs raw engines
    na = nsa = 0
    bada: list[tuple] = []
    bads: list[tuple] = []
    for x in range(1, max_x + 1):
        for y in range(1, x + 1):
            S = x + y
            for R in range(0, S + extra + 1):
                v = canon(R, (x, y), 3)
                f = z3_slice(x, y, R)
                na += 1
                if v != f:
                    bada.append((x, y, R, v, f))
    for x in range(1, max_x + 1):
        for z in range(0, 8):
            for R in range(0, x + z + 8):
                v = canon(R, (x,), z)
                f = single_token(x, z, R)
                nsa += 1
                if v != f:
                    bads.append((x, z, R, v, f))
    checks["z3_anchor_checked"] = na
    checks["z3_anchor_mismatches"] = len(bada)
    checks["single_anchor_checked"] = nsa
    checks["single_anchor_mismatches"] = len(bads)

    # 5. fixed-seed scatter
    rng = random.Random(20261116)
    nsc = 0
    badsc: list[tuple] = []
    for _ in range(scatter):
        x = rng.randint(1, 150)
        y = rng.randint(1, x)
        S = x + y
        R = rng.randint(0, S + 25)
        vc = canon(R, (x, y), 4)
        vf = z4_candidate(x, y, R)
        nsc += 1
        if vc != vf:
            badsc.append((x, y, R, vc, vf))
    checks["scatter_checked"] = nsc
    checks["scatter_mismatches"] = len(badsc)
    checks["scatter_bad_first"] = badsc[:5]

    return {
        "target": "two-token residual z=4 slice closed form (CONJECTURE)",
        "status": "conjecture-finite-audit",
        "max_x": max_x,
        "extra_R_after_S": extra,
        "checks": checks,
        "all_zero_mismatch": (
            checks["grid_mismatches"] == 0
            and checks["induction_mismatches"] == 0
            and checks["tail_violations"] == 0
            and checks["parity_violations"] == 0
            and checks["z3_anchor_mismatches"] == 0
            and checks["single_anchor_mismatches"] == 0
            and checks["scatter_mismatches"] == 0
        ),
    }


def main() -> None:
    result = audit()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
