#!/usr/bin/env python3
"""Finite audit of the conjectured z=5 two-token Grundy-1 locus.

The formula is conjectural. This script compares a capped/canonical recurrence
with an uncapped/ordered recurrence over the complete stated finite grid, and
checks the previously published z=5 Grundy-2 locus at the same time.
"""
from __future__ import annotations

import json
import random
from pathlib import Path


class Engine:
    def __init__(self, capped: bool) -> None:
        self.capped = capped
        self.memo: dict[tuple[int, int, int, int], int] = {}

    def __call__(self, R: int, x: int, y: int, z: int) -> int:
        if R == 0:
            return 0
        if self.capped:
            x, y = sorted((min(x, R + 1), min(y, R + 1)), reverse=True)
        key = (R, x, y, z)
        old = self.memo.get(key)
        if old is not None:
            return old

        options: set[int] = set()
        if x:
            if x >= 2:
                options.add(self(R - 1, x - 1, y, z))
            else:
                options.add(self(R - 1, y, 0, z + 1))
        if y:
            if y >= 2:
                options.add(self(R - 1, x, y - 1, z))
            else:
                options.add(self(R - 1, x, 0, z + 1))
        if z:
            options.add(1 ^ self(R - 1, x, y, z - 1))

        value = 0
        while value in options:
            value += 1
        self.memo[key] = value
        return value


def predicted_g1(x: int, y: int, R: int) -> bool:
    d, S = x - y, x + y
    if d == 0:
        return y >= 3 and R % 2 == 0 and 6 <= R <= S + 2
    if d == 1:
        if y == 1:
            return R >= 4
        return (R % 2 == 0 and 6 <= R <= S + 3) or R >= S + 4
    if d == 2:
        return y >= 2 and R % 2 == 0 and 6 <= R <= S
    if d == 3:
        return (R % 2 == 0 and 6 <= R <= S + 1) or R >= S + 2
    if d == 4:
        return R % 2 == 0 and 6 <= R <= S
    if d == 5:
        return (R % 2 == 0 and 6 <= R <= S - 1) or R >= S + 1
    if d == 6:
        return R % 2 == 0 and 6 <= R <= S - 2
    if d >= 7 and d % 2 == 1:
        return (
            (R % 2 == 0 and 6 <= R <= 2 * y + 4)
            or (R % 2 == 1 and 2 * y + 7 <= R <= S + 4)
            or R >= S + 6
        )
    if d >= 8 and d % 2 == 0:
        return (
            (R % 2 == 0 and 6 <= R <= 2 * y + 4)
            or (R % 2 == 1 and 2 * y + 7 <= R <= S + 5)
        )
    raise AssertionError((x, y, R, d))


def predicted_g2(x: int, y: int, R: int) -> bool:
    d = x - y
    if d == 0:
        if y == 1:
            return R == 1
        if y == 2:
            return R in (1, 3)
        return R in (1, 3, 5)
    if d == 1:
        return R in ((1, 3) if y == 1 else (1, 3, 5, 2 * y + 3))
    if d == 2:
        return R in ((1, 3) if y == 1 else (1, 3, 5))
    if d in (3, 4):
        return R in (1, 3, 5)
    if d == 5:
        return R in (1, 3, 5, 2 * y + 5)
    if d == 6:
        return R in (1, 3, 5, 2 * y + 5, 2 * y + 7, 2 * y + 9, 2 * y + 11)
    return R in (1, 3, 5, 2 * y + 5)


def canonical_scatter(R: int, x: int, y: int, z: int) -> int:
    """Fresh local canonical cache, independent of the grid engine's memo."""
    memo: dict[tuple[int, int, int, int], int] = {}

    def rec(r: int, a: int, b: int, h: int) -> int:
        if r == 0:
            return 0
        a, b = sorted((min(a, r + 1), min(b, r + 1)), reverse=True)
        key = (r, a, b, h)
        old = memo.get(key)
        if old is not None:
            return old
        options: set[int] = set()
        if a:
            if a >= 2:
                options.add(rec(r - 1, a - 1, b, h))
            else:
                options.add(rec(r - 1, b, 0, h + 1))
        if b:
            if b >= 2:
                options.add(rec(r - 1, a, b - 1, h))
            else:
                options.add(rec(r - 1, a, 0, h + 1))
        if h:
            options.add(1 ^ rec(r - 1, a, b, h - 1))
        value = 0
        while value in options:
            value += 1
        memo[key] = value
        return value

    return rec(R, x, y, z)


def audit(max_x: int = 100, extra_after_sum: int = 8, scatter: int = 200) -> dict:
    canonical = Engine(capped=True)
    ordered = Engine(capped=False)
    checks = {
        "grid_states": 0,
        "candidate_value1_mismatches": 0,
        "candidate_value2_mismatches": 0,
        "engine_mismatches": 0,
        "parity_violations": 0,
        "tail_violations": 0,
        "scatter_checked": 0,
        "scatter_mismatches": 0,
    }
    first_mismatches: list[list[object]] = []

    for x in range(1, max_x + 1):
        for y in range(1, x + 1):
            S = x + y
            for R in range(S + extra_after_sum + 1):
                a = canonical(R, x, y, 5)
                b = ordered(R, x, y, 5)
                checks["grid_states"] += 1
                if a != b:
                    checks["engine_mismatches"] += 1
                    if len(first_mismatches) < 10:
                        first_mismatches.append(["engine", x, y, R, a, b])
                if (a == 1) != predicted_g1(x, y, R):
                    checks["candidate_value1_mismatches"] += 1
                    if len(first_mismatches) < 10:
                        first_mismatches.append(["value1", x, y, R, a])
                if (a == 2) != predicted_g2(x, y, R):
                    checks["candidate_value2_mismatches"] += 1
                    if len(first_mismatches) < 10:
                        first_mismatches.append(["value2", x, y, R, a])
                if (R % 2 == 0 and a > 1) or (R % 2 == 1 and a > 2):
                    checks["parity_violations"] += 1
                if R >= S + 6 and a != (S & 1):
                    checks["tail_violations"] += 1

    rng = random.Random(20261116)
    for _ in range(scatter):
        x = rng.randint(1, 300)
        y = rng.randint(1, x)
        S = x + y
        R = rng.randint(0, S + 5)
        a = canonical_scatter(R, x, y, 5)
        b = ordered(R, x, y, 5)
        checks["scatter_checked"] += 1
        if (
            a != b
            or ((a == 1) != predicted_g1(x, y, R))
            or ((a == 2) != predicted_g2(x, y, R))
        ):
            checks["scatter_mismatches"] += 1
            if len(first_mismatches) < 10:
                first_mismatches.append(["scatter", x, y, R, a, b])

    failures = [
        key for key, value in checks.items()
        if key.endswith("_mismatches") or key.endswith("_violations")
        if value != 0
    ]
    return {
        "target": "two-token z=5 Grundy-1 locus",
        "status": "finite-conjecture-audit",
        "domain": {
            "z": 5,
            "max_x": max_x,
            "y_range": "1..x",
            "R_range": "0..x+y+8",
            "scatter_seed": 20261116,
        },
        "checks": checks,
        "cache_states": {
            "canonical": len(canonical.memo),
            "ordered_after_scatter": len(ordered.memo),
        },
        "first_mismatches": first_mismatches,
        "all_checks_pass": not failures,
    }


def main() -> None:
    result = audit()
    out = Path(__file__).resolve().parent / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(out.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
