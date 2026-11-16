#!/usr/bin/env python3
"""Independent finite audit of the two-token residual game at z=3.

The universal claim is proved by strong induction in report.md. This program
corroborates the recurrence with two state representations and checks the
induction-option signatures used in the proof.
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
                options.add(value(R - 1, tuple(sorted(child, reverse=True)), z))
            else:
                options.add(value(R - 1, X[:i] + X[i + 1 :], z + 1))
        if z >= 1:
            options.add(1 ^ value(R - 1, X, z - 1))
        return mex(options)

    def value(R: int, X: tuple[int, ...], z: int) -> int:
        if R == 0:
            return 0
        capped = tuple(sorted((min(token, R + 1) for token in X), reverse=True))
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


def odd_round(n: int) -> int:
    return n if n & 1 else n - 1


def single_token(x: int, z: int, R: int) -> int:
    """Previously proved H(R;(x);z), from K0832."""
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
        threshold = odd_round(z)
        last = x + z + 1
        if R & 1 and R <= threshold:
            return 2
        if not (R & 1) and R <= threshold:
            return 0
        if threshold < R < last - 1:
            return (R + z) & 1
        return x & 1
    if z >= x + 1:
        threshold = odd_round(x)
        if R & 1 and R <= threshold:
            return 2
        if not (R & 1) and R <= threshold:
            return 0
        return x & 1
    raise AssertionError((x, z, R))


def z2_formula(x: int, y: int, R: int) -> int:
    """Previously proved full z=2 slice."""
    d, S = x - y, x + y
    if R in (0, 2):
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
    if d in (1, 3):
        return int(R >= S + 1)
    if d >= 5 and d & 1:
        return int(R >= 2 * y + 4)
    if d >= 4 and not (d & 1):
        return int(2 * y + 4 <= R <= S + 2)
    return 0


def formula_z3(x: int, y: int, R: int) -> int:
    """Proposed full closed form, x >= y >= 1."""
    assert x >= y >= 1 and R >= 0
    d, S = x - y, x + y

    if (x, y) == (1, 1):
        return 2 if R == 1 else 0
    if R in (1, 3):
        return 2
    if d == 3 and R == S:
        return 2
    if d == 4 and R in (2 * y + 3, 2 * y + 5, 2 * y + 7):
        return 2
    if d >= 5 and R == 2 * y + 3:
        return 2

    if R % 2 == 0 and 4 <= R <= min(S, 2 * y + 2):
        return 1
    if d in (1, 3) and R >= S + 1:
        return 1
    if d >= 5 and d & 1 and (
        (R & 1 and R >= 2 * y + 5) or R >= S + 4
    ):
        return 1
    if d >= 6 and not (d & 1) and (
        R & 1 and 2 * y + 5 <= R <= S + 3
    ):
        return 1
    return 0


def candidate_options(x: int, y: int, R: int) -> set[int]:
    """A/B/C option values after substituting induction hypotheses."""
    assert R >= 1
    options: set[int] = set()
    if x >= 2:
        a, b = sorted((x - 1, y), reverse=True)
        options.add(formula_z3(a, b, R - 1))
    if y >= 2:
        a, b = sorted((x, y - 1), reverse=True)
        options.add(formula_z3(a, b, R - 1))
    else:
        # Removing one 1 leaves the other token, including x=y=1.
        options.add(single_token(x, 4, R - 1))
    options.add(1 ^ z2_formula(x, y, R - 1))
    return options


def expected_odd_options(x: int, y: int, R: int) -> set[int]:
    """Exact option set for odd parent R; all children are 0/1 by Theorem T."""
    d, S = x - y, x + y
    if R == 1:
        return {0, 1}
    if R == 3:
        return {1} if (x, y) == (1, 1) else {0, 1}
    assert R >= 5 and R & 1
    if d == 0:
        return {1}
    if d == 1:
        return {1} if R <= S else {0}
    if d == 2:
        return {1}
    if d == 3:
        if R <= S - 2:
            return {1}
        if R == S:
            return {0, 1}
        return {0}
    if d == 4:
        if R <= 2 * y + 1:
            return {1}
        if R in (2 * y + 3, 2 * y + 5, 2 * y + 7):
            return {0, 1}
        return {1}
    if d >= 5 and d & 1:
        if R <= 2 * y + 1:
            return {1}
        if R == 2 * y + 3:
            return {0, 1}
        return {0}
    if d >= 6 and not (d & 1):
        if R <= 2 * y + 1:
            return {1}
        if R == 2 * y + 3:
            return {0, 1}
        if R <= S + 3:
            return {0}
        return {1}
    raise AssertionError((x, y, R))


def expected_even_has_zero(x: int, y: int, R: int) -> bool:
    """For even parent R>=2, H<=1; this predicts whether 0 is an option."""
    d, S = x - y, x + y
    if R == 2:
        return False
    if R == 4:
        return (x, y) != (1, 1)
    assert R >= 6 and R % 2 == 0
    if d == 0:
        return R <= S
    if d in (1, 3):
        return True
    if d == 2:
        return R <= S
    if d == 4:
        return R <= 2 * y + 2
    if d >= 5 and d & 1:
        return R <= 2 * y + 2 or R >= S + 4
    if d >= 6 and not (d & 1):
        return R <= 2 * y + 2
    raise AssertionError((x, y, R))


def expected_h2_positions(x: int, y: int) -> set[int]:
    d, S = x - y, x + y
    if (x, y) == (1, 1):
        return {1}
    result = {1, 3}
    if d == 3:
        result.add(S)
    elif d == 4:
        result.update((2 * y + 3, 2 * y + 5, 2 * y + 7))
    elif d >= 5:
        result.add(2 * y + 3)
    return result


def audit(max_x: int = 20, extra_R_after_S: int = 8, random_cases: int = 50) -> dict:
    canonical = make_canonical_engine()
    labeled = make_labeled_engine()
    counters = {
        "grid_states": 0,
        "canonical_labeled_mismatches": 0,
        "labeled_formula_mismatches": 0,
        "canonical_formula_mismatches": 0,
        "odd_option_table_checks": 0,
        "odd_option_table_mismatches": 0,
        "even_zero_table_checks": 0,
        "even_zero_table_mismatches": 0,
        "range_checks": 0,
        "range_violations": 0,
        "parity_bound_checks": 0,
        "parity_bound_violations": 0,
        "tail_checks_R_ge_S_plus_4": 0,
        "tail_violations": 0,
        "h2_position_checks": 0,
        "h2_position_violations": 0,
    }
    first_mismatch = None

    for x in range(1, max_x + 1):
        for y in range(1, x + 1):
            S = x + y
            h2 = expected_h2_positions(x, y)
            for R in range(S + extra_R_after_S + 1):
                a = canonical(R, (x, y), 3)
                b = labeled(R, (x, y), 3)
                f = formula_z3(x, y, R)
                counters["grid_states"] += 1
                counters["canonical_labeled_mismatches"] += a != b
                counters["labeled_formula_mismatches"] += b != f
                counters["canonical_formula_mismatches"] += a != f
                counters["range_checks"] += 1
                counters["range_violations"] += a not in (0, 1, 2)
                counters["parity_bound_checks"] += 1
                counters["parity_bound_violations"] += (
                    (R % 2 == 0 and a > 1) or (R % 2 == 1 and a > 2)
                )
                if R >= S + 4:
                    counters["tail_checks_R_ge_S_plus_4"] += 1
                    counters["tail_violations"] += a != (S & 1)
                if R & 1:
                    counters["h2_position_checks"] += 1
                    counters["h2_position_violations"] += (
                        (a == 2) != (R in h2)
                    )
                if R >= 1:
                    opts = candidate_options(x, y, R)
                    if R & 1:
                        counters["odd_option_table_checks"] += 1
                        counters["odd_option_table_mismatches"] += (
                            opts != expected_odd_options(x, y, R)
                        )
                    else:
                        counters["even_zero_table_checks"] += 1
                        counters["even_zero_table_mismatches"] += (
                            (0 in opts) != expected_even_has_zero(x, y, R)
                        )
                if first_mismatch is None and (a != b or b != f):
                    first_mismatch = {
                        "x": x, "y": y, "R": R,
                        "canonical": a, "labeled": b, "formula": f,
                    }

    rng = random.Random(20261116)
    random_bad = 0
    random_first = None
    for _ in range(random_cases):
        x = rng.randint(1, 300)
        y = rng.randint(1, x)
        R = rng.randint(0, x + y + 30)
        a = canonical(R, (x, y), 3)
        b = labeled(R, (x, y), 3)
        f = formula_z3(x, y, R)
        bad = a != b or b != f
        random_bad += bad
        if bad and random_first is None:
            random_first = {
                "x": x, "y": y, "R": R,
                "canonical": a, "labeled": b, "formula": f,
            }

    counters["random_cases"] = random_cases
    counters["random_mismatches"] = random_bad
    counters["random_first_mismatch"] = random_first
    counters["first_grid_mismatch"] = first_mismatch
    counters["canonical_cache"] = canonical.cache_info()._asdict()
    counters["labeled_cache"] = labeled.cache_info()._asdict()
    return counters


def main() -> None:
    first = audit()
    second = audit()
    result = {
        "date": "2026-11-16",
        "subject": "two-token residual game, z=3 full Grundy slice",
        "status": "theorem by strong induction; finite audits are independent corroboration",
        "formula_summary": (
            "H=2 at {1,3} except (x,y)=(1,1), where only {1}; add {S} if d=3, "
            "{2y+3,2y+5,2y+7} if d=4, or {2y+3} if d>=5. "
            "H=1 at even 4<=R<=min(S,2y+2); additionally d=1 or 3: R>=S+1; "
            "d>=5 odd: (odd R>=2y+5) or R>=S+4; "
            "d>=6 even: odd 2y+5<=R<=S+3. Here S=x+y,d=x-y."
        ),
        "engines": [
            "sorted multiset recursion with proved cap_{R+1} lemma",
            "ordered labeled-token recursion without capping or sorting",
        ],
        "audit": first,
        "second_run_identical": first == second,
    }
    if first != second:
        raise SystemExit("non-deterministic audit")
    for key in (
        "canonical_labeled_mismatches",
        "labeled_formula_mismatches",
        "canonical_formula_mismatches",
        "odd_option_table_mismatches",
        "even_zero_table_mismatches",
        "range_violations",
        "parity_bound_violations",
        "tail_violations",
        "h2_position_violations",
        "random_mismatches",
    ):
        if first[key]:
            raise SystemExit(f"{key} != 0")
    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "audit.json").write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
