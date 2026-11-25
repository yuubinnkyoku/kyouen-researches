#!/usr/bin/env python3
"""Proof-table and independent finite audit for the z=5, y=1 slice."""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

# The ordered recurrence is recursive in R; the published scatter reaches R>2000.
sys.setrecursionlimit(max(sys.getrecursionlimit(), 5000))


def mex(values: set[int]) -> int:
    value = 0
    while value in values:
        value += 1
    return value


def odd_floor(n: int) -> int:
    return n if n % 2 else n - 1


def single_token(x: int, z: int, R: int) -> int:
    if R == 0:
        return 0
    parity = x & 1
    if z == 0:
        return min(R, x) & 1
    if z == x:
        if R & 1 and R <= 2 * x - 1:
            return 2
        if not (R & 1) and R <= x - 1:
            return 0
        return parity
    if 1 <= z <= x - 1:
        threshold = odd_floor(z)
        if R & 1 and R <= threshold:
            return 2
        if not (R & 1) and R <= threshold:
            return 0
        if threshold < R < x + z:
            return (R + z) & 1
        return parity
    if z >= x + 1:
        threshold = odd_floor(x)
        if R & 1 and R <= threshold:
            return 2
        if not (R & 1) and R <= threshold:
            return 0
        return parity
    raise AssertionError((x, z, R))


def z4_y1(x: int, R: int) -> int:
    if R == 0:
        return 0
    d = x - 1
    S = x + 1
    if x == 1:
        T = {1}
    elif d == 2:
        T = {1, 3, 5}
    elif d == 5:
        T = {1, 3, S, S + 2, S + 4}
    elif d >= 6:
        T = {1, 3, 7}
    else:
        T = {1, 3}
    if R in T:
        return 2
    if d == 0:
        in_P = (R & 1) and 5 <= R <= S + 1 and R not in T
    elif d == 1:
        in_P = ((R & 1) and 5 <= R <= 5) or R >= 6 or (x == 2 and R == 4)
    elif d == 2:
        in_P = False
    elif d == 3:
        in_P = ((R & 1) and 5 <= R <= 5) or R >= 6
    elif d == 4:
        in_P = (R & 1) and 5 <= R <= 5
    elif d >= 5 and d % 2 == 1:
        in_P = (
            ((R & 1) and 5 <= R <= 5)
            or (not (R & 1) and 8 <= R <= S + 5)
            or R >= S + 6
        )
    else:
        in_P = (
            ((R & 1) and 5 <= R <= 5)
            or (not (R & 1) and 8 <= R <= S + 4)
        )
    return 1 if in_P else 0


def candidate(x: int, R: int) -> int:
    if x == 1:
        return 2 if R == 1 else 0
    d = x - 1
    S = x + 1
    if d == 1:
        T = {1, 3}
        in_P = R >= 4
    elif d == 2:
        T = {1, 3}
        in_P = False
    elif d == 3:
        T = {1, 3, 5}
        in_P = R == 6 or R >= 7
    elif d == 4:
        T = {1, 3, 5}
        in_P = R == 6
    elif d == 5:
        T = {1, 3, 5, 7}
        in_P = R == 6 or R >= 8
    elif d == 6:
        T = {1, 3, 5, 7, 9, 11, 13}
        in_P = R == 6
    elif d >= 7 and d % 2 == 1:
        T = {1, 3, 5, 7}
        in_P = R == 6 or ((R & 1) and 9 <= R <= S + 4) or R >= S + 6
    else:
        T = {1, 3, 5, 7}
        in_P = R == 6 or ((R & 1) and 9 <= R <= S + 5)
    if R in T:
        return 2
    return 1 if in_P else 0


def expected_small_signature(x: int, R: int) -> set[int]:
    rows = {
        2: [{0, 1}, {2, 3}, {0, 1}, {0, 3}, {0}, {0}, {0}, {0}],
        3: [{0, 1}, {2, 3}, {0, 1}, {2, 3}, {1}, {1, 3}, {1}, {1}],
        4: [{0, 1}, {2, 3}, {0, 1}, {2, 3}, {0, 1}, {0}, {0}, {0}],
        5: [{0, 1}, {2, 3}, {0, 1}, {2, 3}, {0, 1}, {0, 2}, {1}, {1}],
        6: [{0, 1}, {2, 3}, {0, 1}, {2, 3}, {0, 1}, {0, 2}, {0, 1}, {0, 2, 3}],
        7: [{0, 1}, {2, 3}, {0, 1}, {2, 3}, {0, 1}, {0, 2}, {0, 1}, {1, 2, 3}],
    }
    return rows.get(x, rows[7])[R - 1]


def expected_large_signature(x: int, R: int) -> set[int]:
    if x == 2:
        return {0}
    if x == 3:
        return {1}
    if x == 4:
        return {0}
    if x == 5:
        return {1}
    if x == 6:
        return {0, 2, 3} if not (R & 1) and R <= 12 else {0}
    if x == 7:
        return {0, 1} if (R & 1) and R <= 13 else {1}
    if x == 8:
        return {1, 2} if not (R & 1) and R <= 14 else {0}
    if x >= 9 and R >= x + 7:
        return {0} if x % 2 == 0 else {1}
    return {0} if R & 1 else {1}


def option_signature(x: int, R: int) -> set[int]:
    options: set[int] = set()
    if x >= 2:
        options.add(candidate(x - 1, R - 1))
    options.add(single_token(x, 6, R - 1))
    options.add(1 ^ z4_y1(x, R - 1))
    return options


class Engine:
    def __init__(self, canonical: bool):
        self.canonical = canonical
        self.memo: dict[tuple[int, tuple[int, ...], int], int] = {}

    def __call__(self, R: int, tokens: tuple[int, ...], z: int) -> int:
        if self.canonical:
            tokens = tuple(sorted((min(a, R + 1) for a in tokens), reverse=True))
        if R == 0:
            return 0
        key = (R, tokens, z)
        old = self.memo.get(key)
        if old is not None:
            return old
        options: set[int] = set()
        for i, token in enumerate(tokens):
            child = list(tokens)
            if token >= 2:
                child[i] = token - 1
                options.add(self(R - 1, tuple(child), z))
            else:
                child.pop(i)
                options.add(self(R - 1, tuple(child), z + 1))
        if z >= 1:
            options.add(1 ^ self(R - 1, tokens, z - 1))
        value = mex(options)
        self.memo[key] = value
        return value


def audit() -> dict:
    canonical = Engine(canonical=True)
    ordered = Engine(canonical=False)
    checks = {
        "direct_grid_states": 0,
        "direct_engine_mismatches": 0,
        "candidate_mismatches": 0,
        "parity_violations": 0,
        "tail_violations": 0,
        "induction_step_checks": 0,
        "induction_step_mismatches": 0,
        "option_signature_checks": 0,
        "option_signature_mismatches": 0,
        "scatter_checks": 0,
        "scatter_mismatches": 0,
    }
    first_mismatches: list[list[object]] = []
    for x in range(1, 201):
        for R in range(0, x + 9):
            a = canonical(R, (x, 1), 5)
            b = ordered(R, (x, 1), 5)
            checks["direct_grid_states"] += 1
            if a != b:
                checks["direct_engine_mismatches"] += 1
                if len(first_mismatches) < 10:
                    first_mismatches.append(["engine", x, R, a, b])
            expected = candidate(x, R)
            if a != expected:
                checks["candidate_mismatches"] += 1
                if len(first_mismatches) < 10:
                    first_mismatches.append(["candidate", x, R, a, expected])
            if (R % 2 == 0 and a > 1) or (R % 2 == 1 and a > 2):
                checks["parity_violations"] += 1
            if R >= x + 7 and a != ((x + 1) & 1):
                checks["tail_violations"] += 1

    for x in range(2, 1001):
        for R in range(1, x + 10):
            options = option_signature(x, R)
            value = mex(options)
            expected = candidate(x, R)
            checks["induction_step_checks"] += 1
            checks["option_signature_checks"] += 1
            if value != expected:
                checks["induction_step_mismatches"] += 1
                if len(first_mismatches) < 10:
                    first_mismatches.append(["step", x, R, sorted(options), value, expected])
            signature = expected_small_signature(x, R) if R <= 8 else expected_large_signature(x, R)
            if options != signature:
                checks["option_signature_mismatches"] += 1
                if len(first_mismatches) < 10:
                    first_mismatches.append(["signature", x, R, sorted(options), sorted(signature)])

    rng = random.Random(20261116)
    for _ in range(200):
        x = rng.randint(1, 2000)
        R = rng.randint(0, x + 8)
        a = canonical(R, (x, 1), 5)
        b = ordered(R, (x, 1), 5)
        expected = candidate(x, R)
        checks["scatter_checks"] += 1
        if a != b or a != expected:
            checks["scatter_mismatches"] += 1
            if len(first_mismatches) < 10:
                first_mismatches.append(["scatter", x, R, a, b, expected])

    failures = [
        key for key, value in checks.items()
        if key.endswith("_mismatches") or key.endswith("_violations")
        if value != 0
    ]
    return {
        "target": "two-token z=5, y=1 full Grundy slice",
        "status": "proved-by-R-induction; finite-audit-is-independent-check",
        "domain": {
            "theorem": "all x>=1, R>=0, fixed y=1, z=5",
            "direct_grid": "1<=x<=200, 0<=R<=x+8",
            "induction_signature_grid": "2<=x<=1000, 1<=R<=x+9",
            "scatter_seed": 20261116,
            "scatter": "200 samples, 1<=x<=2000, 0<=R<=x+8",
        },
        "checks": {
            **checks,
            "canonical_cached_states": len(canonical.memo),
            "ordered_cached_states": len(ordered.memo),
        },
        "first_mismatches": first_mismatches,
        "all_checks_pass": not failures,
    }


def main() -> None:
    result = audit()
    out = Path(__file__).resolve().parent / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
