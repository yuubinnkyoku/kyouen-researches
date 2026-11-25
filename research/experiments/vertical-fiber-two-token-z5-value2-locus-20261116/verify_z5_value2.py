#!/usr/bin/env python3
"""Finite audit of the z=5 two-token Grundy-2 locus.

The proposed locus is conjectural. This checks a complete finite grid against
two independently keyed recurrences (canonical capped and ordered uncapped),
plus the proved parity and tail constraints.
"""
from __future__ import annotations

import json
import random
from dataclasses import dataclass

BASE = 1024


def mex(values: set[int]) -> int:
    g = 0
    while g in values:
        g += 1
    return g


@dataclass
class Engine:
    capped: bool

    def __post_init__(self) -> None:
        self.memo: dict[int, int] = {}

    def __call__(self, R: int, x: int, y: int, z: int) -> int:
        if R == 0:
            return 0
        if self.capped:
            x, y = sorted((min(x, R + 1), min(y, R + 1)), reverse=True)
        # Zero is the sentinel for an absent token; token values are positive.
        key = (((R * BASE + x) * BASE + y) * 8 + z)
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
        if z >= 1:
            options.add(1 ^ self(R - 1, x, y, z - 1))
        value = mex(options)
        self.memo[key] = value
        return value


def conjectured_two_positions(x: int, y: int) -> set[int]:
    """Candidate set {R : H(R;(x,y);5)=2}, x>=y>=1."""
    d = x - y
    if d == 0:
        if y == 1:
            return {1}
        if y == 2:
            return {1, 3}
        return {1, 3, 5}
    if d == 1:
        if y == 1:
            return {1, 3}
        return {1, 3, 5, 2 * y + 3}
    if d == 2:
        return {1, 3} if y == 1 else {1, 3, 5}
    if d in (3, 4):
        return {1, 3, 5}
    if d == 5:
        return {1, 3, 5, 2 * y + 5}
    if d == 6:
        return {1, 3, 5, 2 * y + 5, 2 * y + 7, 2 * y + 9, 2 * y + 11}
    return {1, 3, 5, 2 * y + 5}


def canonical_value_for_scatter(R: int, x: int, y: int, z: int) -> int:
    # Separate local cache keeps the ordered engine genuinely independent.
    memo: dict[tuple[int, int, int, int], int] = {}

    def rec(r: int, a: int, b: int, h: int) -> int:
        if r == 0:
            return 0
        a, b = sorted((min(a, r + 1), min(b, r + 1)), reverse=True)
        key = (r, a, b, h)
        if key in memo:
            return memo[key]
        opts: set[int] = set()
        if a:
            if a >= 2:
                opts.add(rec(r - 1, a - 1, b, h))
            else:
                opts.add(rec(r - 1, b, 0, h + 1))
        if b:
            if b >= 2:
                opts.add(rec(r - 1, a, b - 1, h))
            else:
                opts.add(rec(r - 1, a, 0, h + 1))
        if h:
            opts.add(1 ^ rec(r - 1, a, b, h - 1))
        value = mex(opts)
        memo[key] = value
        return value

    return rec(R, x, y, z)


def audit(max_x: int = 100, extra: int = 8, scatter: int = 200) -> dict:
    checks = {
        "grid_states": 0,
        "candidate_mismatches": 0,
        "engine_mismatches": 0,
        "parity_violations": 0,
        "tail_violations": 0,
        "scatter_checked": 0,
        "scatter_mismatches": 0,
    }

    # Engine 1: cap each token at R+1 and canonicalize order.
    canonical = Engine(capped=True)
    first_bad = []
    for x in range(1, max_x + 1):
        for y in range(1, x + 1):
            S = x + y
            target = conjectured_two_positions(x, y)
            for R in range(0, S + extra + 1):
                value = canonical(R, x, y, 5)
                checks["grid_states"] += 1
                if (value == 2) != (R in target):
                    checks["candidate_mismatches"] += 1
                    if len(first_bad) < 10:
                        first_bad.append((x, y, R, value, sorted(target)))
                if (R % 2 == 0 and value > 1) or (R % 2 == 1 and value > 2):
                    checks["parity_violations"] += 1
                if R >= S + 6 and value != (S & 1):
                    checks["tail_violations"] += 1
    checks["canonical_states_cached"] = len(canonical.memo)
    del canonical

    # Engine 2: ordered tokens, no cap and no sorting.
    ordered = Engine(capped=False)
    first_ordered_bad = []
    for x in range(1, max_x + 1):
        for y in range(1, x + 1):
            S = x + y
            target = conjectured_two_positions(x, y)
            for R in range(0, S + extra + 1):
                value = ordered(R, x, y, 5)
                if (value == 2) != (R in target):
                    checks["engine_mismatches"] += 1
                    if len(first_ordered_bad) < 10:
                        first_ordered_bad.append((x, y, R, value, sorted(target)))
    checks["ordered_states_cached"] = len(ordered.memo)

    # Deterministic large-parameter scatter, independently checked by both
    # engines. The tail theorem handles all R >= S+6; scatter stays below it.
    rng = random.Random(20261116)
    for _ in range(scatter):
        x = rng.randint(1, 300)
        y = rng.randint(1, x)
        S = x + y
        R = rng.randint(0, S + 5)
        target = conjectured_two_positions(x, y)
        a = ordered(R, x, y, 5)
        b = canonical_value_for_scatter(R, x, y, 5)
        checks["scatter_checked"] += 1
        if a != b or ((a == 2) != (R in target)):
            checks["scatter_mismatches"] += 1

    return {
        "target": "two-token z=5 Grundy-2 locus",
        "status": "finite-conjecture-audit",
        "max_x": max_x,
        "extra_R_after_S": extra,
        "checks": checks,
        "first_candidate_mismatches": first_bad,
        "first_ordered_mismatches": first_ordered_bad,
        "all_checks_pass": all(
            checks[k] == 0
            for k in (
                "candidate_mismatches",
                "engine_mismatches",
                "parity_violations",
                "tail_violations",
                "scatter_mismatches",
            )
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
