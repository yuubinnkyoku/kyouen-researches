#!/usr/bin/env python3
"""Finite audit of the conjectured two-token H=2 locus.

The sorted engine is scanned on x<=60, z<=60.
The order-preserving engine is scanned on x<=60, z<=45 in bounded z blocks.
Both engines are compared directly on x<=20, z<=20.

This is a finite audit, not a proof of the all-parameter conjecture.
Only the Python standard library is required.
"""
from __future__ import annotations

import argparse
import json
from functools import lru_cache
from pathlib import Path


def odd_leq(k: int) -> int:
    return k if k >= 1 and k % 2 else k - 1


def odd_ge(k: int) -> int:
    return k if k % 2 else k + 1


def predicted_value2(x: int, y: int, z: int) -> set[int]:
    """The three-family conjecture recorded in K0832."""
    total = x + y
    d = x - y
    result = set(range(1, odd_leq(min(total, z)) + 1, 2))

    # Family B: PT corner and EXT ray.
    if d <= z and (d - z) % 2 == 0:
        y_star = (z - d) // 2
        if y_star >= 1 and y == y_star:
            lo = odd_ge(d + 1)  # smin(d)
            hi = 2 * ((z + d + 3) // 4) - 1
            result.update(2 * y + delta for delta in range(lo, hi + 1, 2))
        if (z + d) % 4 == 2 and y >= y_star:
            result.add(2 * y + (z + d) // 2)

    # Family A: the transition run and the stable point.
    if d == z + 1:
        lo = odd_ge(z)
        hi = 2 * z + 1
        result.update(2 * y + delta for delta in range(lo, hi + 1, 2))
    elif d >= z + 2:
        result.add(2 * y + odd_ge(z))

    return result


@lru_cache(maxsize=None)
def grundy_sorted(R: int, X: tuple[int, ...], z: int) -> int:
    """Canonical multiset recursion: sort after every A move."""
    if R == 0:
        return 0
    options: set[int] = set()
    for i, value in enumerate(X):
        if value >= 2:
            child = list(X)
            child[i] = value - 1
            child.sort(reverse=True)
            options.add(grundy_sorted(R - 1, tuple(child), z))
    if 1 in X:
        child = list(X)
        child.remove(1)
        options.add(grundy_sorted(R - 1, tuple(child), z + 1))
    if z >= 1:
        options.add(grundy_sorted(R - 1, X, z - 1) ^ 1)
    mex = 0
    while mex in options:
        mex += 1
    return mex


@lru_cache(maxsize=None)
def grundy_ordered(R: int, X: tuple[int, ...], z: int) -> int:
    """Labeled-token recursion: preserve tuple order and never sort."""
    if R == 0:
        return 0
    options: set[int] = set()
    for i, value in enumerate(X):
        if value >= 2:
            child = list(X)
            child[i] = value - 1
            options.add(grundy_ordered(R - 1, tuple(child), z))
    if 1 in X:
        child = list(X)
        child.remove(1)
        options.add(grundy_ordered(R - 1, tuple(child), z + 1))
    if z >= 1:
        options.add(grundy_ordered(R - 1, X, z - 1) ^ 1)
    mex = 0
    while mex in options:
        mex += 1
    return mex


def scan_sorted(x_max: int, z_max: int) -> dict:
    grundy_sorted.cache_clear()
    cases = 0
    mismatches = []
    for z in range(z_max + 1):
        for x in range(1, x_max + 1):
            for y in range(1, x + 1):
                total = x + y
                predicted = predicted_value2(x, y, z)
                # The proved tail starts at R >= total + z + 1.
                for R in range(total + z + 1):
                    actual = grundy_sorted(R, (x, y), z)
                    if (actual == 2) != (R in predicted):
                        mismatches.append({
                            "x": x, "y": y, "z": z, "R": R,
                            "actual": actual, "predicted_value2": R in predicted,
                        })
                        return {
                            "cases": cases + 1,
                            "mismatches": mismatches,
                            "cache": grundy_sorted.cache_info()._asdict(),
                        }
                    cases += 1
    return {
        "cases": cases,
        "mismatches": mismatches,
        "cache": grundy_sorted.cache_info()._asdict(),
    }


def ordered_blocks(z_max: int) -> list[tuple[int, int]]:
    fixed = [(0, 10), (11, 20), (21, 30), (31, 40), (41, 45)]
    blocks = [(lo, min(hi, z_max)) for lo, hi in fixed if lo <= z_max]
    if z_max > 45:
        raise ValueError("the recorded ordered-engine audit is bounded by z_max=45")
    return blocks


def scan_ordered(x_max: int, z_max: int) -> dict:
    cases = 0
    mismatches = []
    blocks = ordered_blocks(z_max)
    for z_lo, z_hi in blocks:
        grundy_ordered.cache_clear()
        for z in range(z_lo, z_hi + 1):
            for x in range(1, x_max + 1):
                for y in range(1, x + 1):
                    total = x + y
                    predicted = predicted_value2(x, y, z)
                    for R in range(total + z + 1):
                        actual = grundy_ordered(R, (x, y), z)
                        if (actual == 2) != (R in predicted):
                            mismatches.append({
                                "x": x, "y": y, "z": z, "R": R,
                                "actual": actual, "predicted_value2": R in predicted,
                            })
                            return {
                                "cases": cases + 1,
                                "mismatches": mismatches,
                                "z_blocks": blocks,
                            }
                        cases += 1
    return {"cases": cases, "mismatches": mismatches, "z_blocks": blocks}


def cross_check(x_max: int, z_max: int) -> dict:
    grundy_sorted.cache_clear()
    grundy_ordered.cache_clear()
    cases = 0
    mismatches = []
    for z in range(z_max + 1):
        for x in range(1, x_max + 1):
            for y in range(1, x + 1):
                total = x + y
                predicted = predicted_value2(x, y, z)
                for R in range(total + z + 1):
                    a = grundy_sorted(R, (x, y), z)
                    b = grundy_ordered(R, (x, y), z)
                    if a != b or ((a == 2) != (R in predicted)):
                        mismatches.append({
                            "x": x, "y": y, "z": z, "R": R,
                            "sorted": a, "ordered": b,
                            "predicted_value2": R in predicted,
                        })
                        return {"cases": cases + 1, "mismatches": mismatches}
                    cases += 1
    return {"cases": cases, "mismatches": mismatches}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--x-max", type=int, default=60)
    parser.add_argument("--z-max", type=int, default=60)
    parser.add_argument("--ordered-z-max", type=int, default=45)
    parser.add_argument("--cross-x-max", type=int, default=20)
    parser.add_argument("--cross-z-max", type=int, default=20)
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).parent / "output" / "audit.json",
    )
    args = parser.parse_args()

    sorted_result = scan_sorted(args.x_max, args.z_max)
    ordered_result = scan_ordered(args.x_max, args.ordered_z_max)
    cross_result = cross_check(args.cross_x_max, args.cross_z_max)
    result = {
        "schema": "kyouen.two_token_value2_grid_audit.v1",
        "status": "finite_audit_only",
        "claim_tested": "the K0832 three-family conjecture for H(R;(x,y);z)=2",
        "sorted_canonical_engine": {
            "x_max": args.x_max,
            "z_max": args.z_max,
            "y_range": "1 <= y <= x",
            "R_range": "0 <= R <= x+y+z",
            **sorted_result,
        },
        "ordered_labeled_engine": {
            "x_max": args.x_max,
            "z_max": args.ordered_z_max,
            "y_range": "1 <= y <= x",
            "R_range": "0 <= R <= x+y+z",
            "sorting": False,
            **ordered_result,
        },
        "direct_engine_cross_check": {
            "x_max": args.cross_x_max,
            "z_max": args.cross_z_max,
            "R_range": "0 <= R <= x+y+z",
            **cross_result,
        },
        "tail_scope": (
            "The proved tail theorem gives H(R;(x,y);z)=x+y mod 2 for "
            "R >= x+y+z+1. Therefore no value-2 positions can occur beyond "
            "the finite R range scanned for each tested (x,y,z)."
        ),
        "limitations": [
            "Finite parameter boxes do not prove the conjecture for all x,y,z.",
            "The ordered engine is scanned only through z=45.",
            "This audit classifies only the value-2 locus, not all values 0,1,2.",
            "The all-parameter three-family conjecture remains unproved.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
