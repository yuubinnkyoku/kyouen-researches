#!/usr/bin/env python3
"""Independent recursive-mex audit for the t=3, q=7 pure-fiber game."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

T = 3
CAPACITY = 6


def mex(values: set[int]) -> int:
    n = 0
    while n in values:
        n += 1
    return n


def canonical_engine(w: int, m: int) -> dict[tuple[int, ...], int]:
    def cap(state: tuple[int, ...]) -> int:
        return sum(min(x, T) for x in state)

    @lru_cache(None)
    def grundy(state: tuple[int, ...]) -> int:
        options: set[int] = set()
        for i, value in enumerate(state):
            if value < m:
                child_list = list(state)
                child_list[i] += 1
                child = tuple(sorted(child_list, reverse=True))
                if cap(child) <= CAPACITY:
                    options.add(grundy(child))
        if len(state) < w and cap(state) < CAPACITY:
            child = tuple(sorted(state + (1,), reverse=True))
            options.add(grundy(child))
        return mex(options)

    seen = {()}
    stack = [()]
    while stack:
        state = stack.pop()
        children = []
        for i, value in enumerate(state):
            if value < m:
                child_list = list(state)
                child_list[i] += 1
                child = tuple(sorted(child_list, reverse=True))
                if cap(child) <= CAPACITY:
                    children.append(child)
        if len(state) < w and cap(state) < CAPACITY:
            children.append(tuple(sorted(state + (1,), reverse=True)))
        for child in children:
            if child not in seen:
                seen.add(child)
                stack.append(child)
    return {state: grundy(state) for state in seen}


def labeled_engine(w: int, m: int) -> dict[tuple[int, ...], int]:
    def cap(state: tuple[int, ...]) -> int:
        return sum(min(x, T) for x in state)

    @lru_cache(None)
    def grundy(state: tuple[int, ...]) -> int:
        options: set[int] = set()
        for i, value in enumerate(state):
            if value < m:
                child = state[:i] + (value + 1,) + state[i + 1:]
                if cap(child) <= CAPACITY:
                    options.add(grundy(child))
        return mex(options)

    initial = (0,) * w
    seen = {initial}
    stack = [initial]
    while stack:
        state = stack.pop()
        for i, value in enumerate(state):
            if value < m:
                child = state[:i] + (value + 1,) + state[i + 1:]
                if cap(child) <= CAPACITY and child not in seen:
                    seen.add(child)
                    stack.append(child)
    return {state: grundy(state) for state in seen}


def predicted_maximum(w: int, m: int) -> int:
    return 3 if w >= 3 and m >= 4 and m % 2 == 0 else 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-width", type=int, default=8)
    parser.add_argument("--max-height", type=int, default=12)
    args = parser.parse_args()
    if args.max_width < 1 or args.max_height < 2:
        raise SystemExit("require max-width >= 1 and max-height >= 2")

    canonical_total = 0
    labeled_total = 0
    histogram: Counter[int] = Counter()
    mismatches = 0
    for w in range(1, args.max_width + 1):
        for m in range(2, args.max_height + 1):
            canonical = canonical_engine(w, m)
            labeled = labeled_engine(w, m)
            projection: dict[tuple[int, ...], int] = {}
            for vector, value in labeled.items():
                key = tuple(sorted((x for x in vector if x), reverse=True))
                previous = projection.setdefault(key, value)
                if previous != value:
                    mismatches += 1
                    raise AssertionError(("permutation mismatch", w, m, vector))
            if set(projection) != set(canonical):
                mismatches += 1
                raise AssertionError(("state-set mismatch", w, m))
            for state, value in canonical.items():
                if projection[state] != value:
                    mismatches += 1
                    raise AssertionError(("Grundy mismatch", w, m, state))
            maximum = max(canonical.values())
            expected = predicted_maximum(w, m)
            if maximum != expected:
                mismatches += 1
                raise AssertionError(("maximum mismatch", w, m, maximum, expected))
            if maximum > 3:
                raise AssertionError(("universal upper bound violated", w, m, maximum))
            canonical_total += len(canonical)
            labeled_total += len(labeled)
            histogram.update(labeled.values())

    witness_engine = canonical_engine(3, 4)
    assert witness_engine[(3, 2)] == 3
    children = {
        (4, 2): witness_engine[(4, 2)],
        (3, 3): witness_engine[(3, 3)],
        (3, 2, 1): witness_engine[(3, 2, 1)],
    }
    assert children == {(4, 2): 2, (3, 3): 0, (3, 2, 1): 1}

    result = {
        "scope": {
            "game": "pure fiber occupancy game",
            "t": 3, "q": 7,
            "safety": "sum_b min(c_b, 3) <= 6",
            "move": "increment one coordinate by one if the child is safe",
            "grundy": "mex of legal-child Grundy values",
            "height_range": [2, args.max_height],
            "width_range": [1, args.max_width],
        },
        "audit": {
            "parameter_pairs": args.max_width * (args.max_height - 1),
            "canonical_multiset_states": canonical_total,
            "labeled_vector_states": labeled_total,
            "labeled_grundy_histogram": {
                str(k): histogram[k] for k in sorted(histogram)
            },
            "mismatches": mismatches,
            "all_parameter_maxima_match_theorem": True,
            "all_values_at_most_3": True,
        },
        "minimum_value_3_witness": {
            "w": 3, "m": 4, "occupancy": [3, 2, 0], "grundy": 3,
            "children": [
                {"occupancy": [4, 2, 0], "grundy": 2},
                {"occupancy": [3, 3, 0], "grundy": 0},
                {"occupancy": [3, 2, 1], "grundy": 1},
            ],
        },
        "interpretation": (
            "Finite recursive-mex audit only; the all-parameter theorem is "
            "proved in report.md."
        ),
    }
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
