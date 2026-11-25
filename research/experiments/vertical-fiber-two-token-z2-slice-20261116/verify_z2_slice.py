#!/usr/bin/env python3
"""Independent finite audit of the two-token residual game at z=2.

The proof is the strong-induction argument in report.md. This script checks
the recurrence with two independent state representations and checks the
induction-table signatures used in that proof.
"""
from __future__ import annotations

import json
import random
from functools import lru_cache
from pathlib import Path


def mex(values: set[int]) -> int:
    g = 0
    while g in values:
        g += 1
    return g


def make_canonical_engine():
    """Sorted multiset recursion using the proved cap_{R+1} lemma."""
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
                options.add(value(R - 1, X[:i] + X[i + 1 :], z + 1))
        if z >= 1:
            options.add(1 ^ value(R - 1, X, z - 1))
        return mex(options)

    def value(R: int, X: tuple[int, ...], z: int) -> int:
        if R == 0:
            return 0
        capped = tuple(sorted(min(token, R + 1) for token in X))
        return inner(R, capped, z)

    value.cache_info = inner.cache_info  # type: ignore[attr-defined]
    return value


def make_labeled_engine():
    """Ordered labeled-token recursion, with no capping or sorting."""
    @lru_cache(maxsize=None)
    def value(R: int, X: tuple[int, ...], z: int) -> int:
        if R == 0:
            return 0
        options: set[int] = set()
        for i, token in enumerate(X):
            if token >= 2:
                options.add(value(R - 1, X[:i] + (token - 1,) + X[i + 1 :], z))
            else:
                options.add(value(R - 1, X[:i] + X[i + 1 :], z + 1))
        if z >= 1:
            options.add(1 ^ value(R - 1, X, z - 1))
        return mex(options)

    return value


def q_odd(n: int) -> int:
    return n if n & 1 else n - 1


def single_token(x: int, z: int, R: int) -> int:
    """Previously proved H(R;(x);z), copied as a proof-side boundary formula."""
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


def z1_formula(x: int, y: int, R: int) -> int:
    """Previously proved full z=1 slice."""
    S, d = x + y, x - y
    if R == 0:
        return 0
    if R == 1:
        return 2
    if R == 2:
        return 1
    if 3 <= R <= 2 * y:
        return (R + 1) & 1
    if R == 2 * y + 1:
        return 2 if d else 0
    if 2 * y + 2 <= R <= S:
        return R & 1
    if R == S + 1:
        if d == 1:
            return S & 1
        if d == 2:
            return 2
        return R & 1
    return S & 1


def value_two_token_z2(x: int, y: int, R: int) -> int:
    """Proposed full closed form, x >= y >= 1."""
    assert x >= y >= 1 and R >= 0
    d, S = x - y, x + y
    if R == 0 or R == 2:
        return 0
    if R == 1:
        return 2
    if R & 1:
        if d == 0:
            if R <= S - 1:
                return 1
            if R == S + 1:
                return 2
            return 0
        if d == 1:
            return 1
        if d == 2:
            return int(R <= S - 1)
        if d == 3:
            if R <= S - 2 or R >= S + 4:
                return 1
            if R in (S, S + 2):
                return 2
            return 0
        if R <= 2 * y + 1:
            return 1
        if R == 2 * y + 3:
            return 2
        if d & 1 and R >= S + 4:
            return 1
        return 0

    # Even R >= 4.
    if d in (1, 3):
        return int(R >= S + 1)
    if d >= 5 and d & 1:
        return int(R >= 2 * y + 4)
    if d >= 4 and not (d & 1):
        return int(2 * y + 4 <= R <= S + 2)
    return 0


def expected_option_flags(x: int, y: int, R: int) -> set[int]:
    """The O intersect {0,1} table in report.md."""
    d, S = x - y, x + y
    if R == 1:
        return {0, 1}
    if R == 2:
        return set()
    if R & 1:
        if d == 0:
            if R <= S - 1:
                return {0}
            if R == S + 1:
                return {0, 1}
            return {1}
        if d == 1:
            return {0}
        if d == 2:
            return {0} if R <= S - 1 else {1}
        if d == 3:
            if R <= S - 2:
                return {0}
            if R in (S, S + 2):
                return {0, 1}
            return {0}
        if R <= 2 * y + 1:
            return {0}
        if R == 2 * y + 3:
            return {0, 1}
        if d & 1:
            return {1} if R <= S + 2 else {0}
        return {1}

    if d in (0, 2):
        return {1}
    if d in (1, 3):
        return {0} if R >= S + 1 else {1}
    if d >= 4 and not (d & 1):
        return {0} if 2 * y + 4 <= R <= S + 2 else {1}
    if d >= 5 and d & 1:
        return {0} if R >= 2 * y + 4 else {1}
    return {1}


def candidate_options(x: int, y: int, R: int) -> set[int]:
    """Options obtained from the induction hypothesis and known z=0/1 slices."""
    assert R >= 1
    options: set[int] = set()
    if x >= 2:
        a, b = sorted((x - 1, y), reverse=True)
        options.add(value_two_token_z2(a, b, R - 1))
    if y >= 2:
        a, b = sorted((x, y - 1), reverse=True)
        options.add(value_two_token_z2(a, b, R - 1))
    if y == 1:
        options.add(single_token(x, 3, R - 1))
    options.add(1 ^ z1_formula(x, y, R - 1))
    return options


def audit(max_x: int = 80, extra_R_after_S: int = 8, random_cases: int = 200) -> dict:
    canonical = make_canonical_engine()
    labeled = make_labeled_engine()
    checks = 0
    canonical_labeled_bad = labeled_formula_bad = canonical_formula_bad = 0
    option_flag_checks = option_flag_bad = 0
    range_checks = range_bad = 0
    even_checks = even_bad = 0
    tail_checks = tail_bad = 0
    odd_position_checks = odd_position_bad = 0
    first_mismatch = None

    for x in range(1, max_x + 1):
        for y in range(1, x + 1):
            S = x + y
            for R in range(S + extra_R_after_S + 1):
                a = canonical(R, (x, y), 2)
                b = labeled(R, (x, y), 2)
                f = value_two_token_z2(x, y, R)
                checks += 1
                canonical_labeled_bad += a != b
                labeled_formula_bad += b != f
                canonical_formula_bad += a != f
                range_checks += 1
                range_bad += a not in (0, 1, 2)
                if R >= 1:
                    option_flag_checks += 1
                    actual_flags = candidate_options(x, y, R) & {0, 1}
                    option_flag_bad += actual_flags != expected_option_flags(x, y, R)
                if R % 2 == 0:
                    even_checks += 1
                    even_bad += a > 1
                if R >= S + 3:
                    tail_checks += 1
                    tail_bad += a != (S & 1)
                if R % 2 == 1:
                    odd_position_checks += 1
                    d = x - y
                    expected_T = {1}
                    if d == 0:
                        expected_T.add(S + 1)
                    elif d == 3:
                        expected_T.update((S, S + 2))
                    elif d >= 4:
                        expected_T.add(2 * y + 3)
                    odd_position_bad += (a == 2) != (R in expected_T)
                if first_mismatch is None and (a != b or b != f):
                    first_mismatch = {
                        "x": x, "y": y, "R": R,
                        "canonical": a, "labeled": b, "formula": f,
                    }

    rng = random.Random(20261116)
    random_bad = 0
    random_first = None
    for _ in range(random_cases):
        x = rng.randint(1, 250)
        y = rng.randint(1, x)
        R = rng.randint(0, x + y + 20)
        a = canonical(R, (x, y), 2)
        b = labeled(R, (x, y), 2)
        f = value_two_token_z2(x, y, R)
        bad = a != b or b != f
        random_bad += bad
        if bad and random_first is None:
            random_first = {
                "x": x, "y": y, "R": R,
                "canonical": a, "labeled": b, "formula": f,
            }

    return {
        "max_x": max_x,
        "extra_R_after_S": extra_R_after_S,
        "grid_states": checks,
        "canonical_vs_labeled_mismatches": canonical_labeled_bad,
        "labeled_vs_formula_mismatches": labeled_formula_bad,
        "canonical_vs_formula_mismatches": canonical_formula_bad,
        "option_flag_table_checks": option_flag_checks,
        "option_flag_table_mismatches": option_flag_bad,
        "value_range_checks": range_checks,
        "value_range_mismatches": range_bad,
        "even_R_parity_checks": even_checks,
        "even_R_gt_1": even_bad,
        "tail_checks_R_ge_S_plus_3": tail_checks,
        "tail_mismatches": tail_bad,
        "odd_R_H2_position_checks": odd_position_checks,
        "H2_position_mismatches": odd_position_bad,
        "random_cases": random_cases,
        "random_mismatches": random_bad,
        "random_first_mismatch": random_first,
        "first_grid_mismatch": first_mismatch,
        "canonical_cache": canonical.cache_info()._asdict(),
        "labeled_cache": labeled.cache_info()._asdict(),
    }


def main() -> None:
    first = audit()
    second = audit()
    result = {
        "date": "2026-11-16",
        "subject": "two-token residual game, z=2 full Grundy slice",
        "status": "theorem by strong induction; finite audits are independent corroboration",
        "formula": (
            "R=0,2:0; R=1:2. For odd R>=3, H=2 at T={1} plus "
            "{S+1 if d=0; S,S+2 if d=3; 2y+3 if d>=4}; "
            "H=1 at d=0:R<=S-1; d=1:all; d=2:R<=S-1; "
            "d=3:R<=S-2 or R>=S+4; d>=4:R<=2y+1 or "
            "(d odd and R>=S+4); otherwise 0. For even R>=4, "
            "H=1 iff (d in {1,3} and R>=S+1) or "
            "(d>=5 odd and R>=2y+4) or "
            "(d>=4 even and 2y+4<=R<=S+2); otherwise 0. "
            "Here S=x+y,d=x-y,x>=y>=1."
        ),
        "engines": [
            "sorted multiset recursion with proved cap_{R+1} lemma",
            "ordered labeled-token recursion without capping or sorting",
        ],
        "audit": first,
        "second_run_identical": first == second,
    }
    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if first != second:
        raise SystemExit("non-deterministic audit")
    for key in (
        "canonical_vs_labeled_mismatches",
        "labeled_vs_formula_mismatches",
        "canonical_vs_formula_mismatches",
        "option_flag_table_mismatches",
        "value_range_mismatches",
        "even_R_gt_1",
        "tail_mismatches",
        "H2_position_mismatches",
        "random_mismatches",
    ):
        if first[key]:
            raise SystemExit(f"{key} != 0")
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "audit.json").write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
