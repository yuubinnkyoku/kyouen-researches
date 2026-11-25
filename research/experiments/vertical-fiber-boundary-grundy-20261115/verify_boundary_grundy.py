#!/usr/bin/env python3
"""Exhaustively audit the boundary-layer Grundy formula for the pure fiber rule."""
from __future__ import annotations

from functools import lru_cache
from itertools import product
import json


def mex(values: set[int]) -> int:
    x = 0
    while x in values:
        x += 1
    return x


def audit_case(w: int, m: int, t: int) -> int:
    checked = 0
    for q in range(1, w * t + 2):
        @lru_cache(maxsize=None)
        def grundy(c: tuple[int, ...]) -> int:
            options = set()
            for b, count in enumerate(c):
                if count == m:
                    continue
                child = list(c)
                child[b] += 1
                child_t = tuple(child)
                if sum(min(x, t) for x in child_t) <= q - 1:
                    options.add(grundy(child_t))
            return mex(options)

        for c in product(range(m + 1), repeat=w):
            if sum(min(x, t) for x in c) != q - 1:
                continue
            actual = grundy(c)
            predicted = 0
            for count in c:
                if count >= t:
                    predicted ^= (m - count) & 1
            if actual != predicted:
                raise AssertionError({
                    "w": w, "m": m, "t": t, "q": q,
                    "occupancy": c, "actual": actual,
                    "predicted": predicted,
                })
            checked += 1
    return checked


def main() -> None:
    by_width = []
    total = 0
    cases = 0
    for w in range(1, 5):
        width_total = 0
        width_cases = 0
        for m in range(1, 5):
            for t in range(1, 5):
                width_total += audit_case(w, m, t)
                width_cases += 1
        by_width.append({
            "w": w,
            "parameter_cases": width_cases,
            "boundary_states": width_total,
        })
        total += width_total
        cases += width_cases

    print(json.dumps({
        "audit": "pure-fiber-polynomial-boundary-grundy",
        "range": {"w": [1, 4], "m": [1, 4], "t": [1, 4]},
        "parameter_cases": cases,
        "boundary_states": total,
        "all_match": True,
        "by_width": by_width,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
