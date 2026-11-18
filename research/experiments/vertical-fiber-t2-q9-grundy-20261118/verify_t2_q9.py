#!/usr/bin/env python3
"""Independent recursive-mex audit for the pure t=2, q=9 fiber theorem."""
from __future__ import annotations
import argparse
import hashlib
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

CAP = 8
ROWS = {
    0: ("0",),
    1: ("00", "12"),
    2: ("000", "111", "010"),
    3: ("0000", "1111", "0020", "0212"),
    4: ("00000", "11111", "00000", "10111", "00010"),
    5: ("000000", "111111", "000000", "112111", "100020", "120212"),
    6: ("0000000", "1111111", "0000000", "1111111", "0100000", "1110111", "0100010"),
    7: ("00000000", "11111111", "00000000", "11111111", "00200000", "01112111", "00100020", "02120212"),
    8: ("000000000", "111111111", "000000000", "111111111", "000000000", "101111111", "000100000", "101110111", "000100010"),
}

def mex(values: set[int]) -> int:
    value = 0
    while value in values:
        value += 1
    return value

@lru_cache(None)
def h_direct(e: int, ell: int, r: int, parity: int) -> int:
    if r == 0 or e + ell == 0:
        return 0
    options: set[int] = set()
    if e:
        options.add(h_direct(e - 1, ell + 1, r - 1, parity))
    if ell:
        options.add(parity ^ h_direct(e, ell - 1, r - 1, parity))
    return mex(options)

def h_odd_table(e: int, ell: int, r: int) -> int:
    return int(ROWS[r][min(e, r)][min(ell, r)])

def h_even_formula(e: int, ell: int, r: int) -> int:
    return min(r, 2 * e + ell) & 1

def capped_cost(state: tuple[int, ...]) -> int:
    return sum(min(value, 2) for value in state)

def theorem_value(state: tuple[int, ...], width: int, height: int) -> int:
    saturated = sum(value >= 2 for value in state)
    singletons = sum(value == 1 for value in state)
    empty = width - saturated - singletons
    residual = CAP - 2 * saturated - singletons
    assert residual >= 0
    chain_xor = 0
    for value in state:
        if value >= 2:
            chain_xor ^= (height - value) & 1
    residual_value = (
        h_even_formula(empty, singletons, residual)
        if height % 2 == 0
        else h_odd_table(empty, singletons, residual)
    )
    return chain_xor ^ residual_value

@lru_cache(None)
def grundy_labeled(state: tuple[int, ...], height: int) -> int:
    options: set[int] = set()
    for index, value in enumerate(state):
        if value < height:
            child = state[:index] + (value + 1,) + state[index + 1:]
            if capped_cost(child) <= CAP:
                options.add(grundy_labeled(child, height))
    return mex(options)

@lru_cache(None)
def grundy_canonical(state: tuple[int, ...], width: int, height: int) -> int:
    options: set[int] = set()
    for index, value in enumerate(state):
        if index and state[index] == state[index - 1]:
            continue
        if value < height:
            child_list = list(state)
            child_list[index] += 1
            child = tuple(sorted(child_list, reverse=True))
            if capped_cost(child) <= CAP:
                options.add(grundy_canonical(child, width, height))
    if len(state) < width and capped_cost(state) < CAP:
        child = tuple(sorted(state + (1,), reverse=True))
        options.add(grundy_canonical(child, width, height))
    return mex(options)

def enumerate_labeled(width: int, height: int) -> set[tuple[int, ...]]:
    seen: set[tuple[int, ...]] = set()
    stack = [(0,) * width]
    while stack:
        state = stack.pop()
        if state in seen:
            continue
        seen.add(state)
        for index, value in enumerate(state):
            if value < height:
                child = state[:index] + (value + 1,) + state[index + 1:]
                if capped_cost(child) <= CAP and child not in seen:
                    stack.append(child)
    return seen

def enumerate_canonical(width: int, height: int) -> set[tuple[int, ...]]:
    seen: set[tuple[int, ...]] = set()
    stack = [()]
    while stack:
        state = stack.pop()
        if state in seen:
            continue
        seen.add(state)
        for index, value in enumerate(state):
            if index and state[index] == state[index - 1]:
                continue
            if value < height:
                child_list = list(state)
                child_list[index] += 1
                child = tuple(sorted(child_list, reverse=True))
                if capped_cost(child) <= CAP and child not in seen:
                    stack.append(child)
        if len(state) < width and capped_cost(state) < CAP:
            child = tuple(sorted(state + (1,), reverse=True))
            if child not in seen:
                stack.append(child)
    return seen

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).parent / "output/audit.json")
    output = parser.parse_args().output

    table_cells = 0
    for residual in range(CAP + 1):
        for empty in range(residual + 1):
            for singletons in range(residual + 1):
                if residual == 0 or empty + singletons == 0:
                    expected = 0
                else:
                    options: set[int] = set()
                    if empty:
                        options.add(int(
                            ROWS[residual - 1][min(empty - 1, residual - 1)]
                            [min(singletons + 1, residual - 1)]
                        ))
                    if singletons:
                        options.add(1 ^ int(
                            ROWS[residual - 1][min(empty, residual - 1)]
                            [min(singletons - 1, residual - 1)]
                        ))
                    expected = mex(options)
                assert int(ROWS[residual][empty][singletons]) == expected
                table_cells += 1

    direct_odd = direct_even = 0
    for residual in range(CAP + 1):
        for empty in range(31):
            for singletons in range(31):
                assert h_direct(empty, singletons, residual, 1) == h_odd_table(
                    empty, singletons, residual)
                assert h_direct(empty, singletons, residual, 0) == h_even_formula(
                    empty, singletons, residual)
                direct_odd += 1
                direct_even += 1

    labeled_total = canonical_total = parameter_pairs = 0
    labeled_histogram: Counter[int] = Counter()
    canonical_histogram: Counter[int] = Counter()
    maximum_by_width: dict[str, list[int]] = {}

    for width in range(1, 9):
        row: list[int] = []
        for height in range(2, 9):
            labeled_states = enumerate_labeled(width, height)
            canonical_states = enumerate_canonical(width, height)
            projected = {
                tuple(sorted((value for value in state if value), reverse=True))
                for state in labeled_states
            }
            assert projected == canonical_states

            pair_labeled_hist: Counter[int] = Counter()
            pair_canonical_hist: Counter[int] = Counter()
            for state in labeled_states:
                actual = grundy_labeled(state, height)
                positive = tuple(sorted((value for value in state if value), reverse=True))
                assert actual == theorem_value(positive, width, height)
                assert actual == grundy_canonical(positive, width, height)
                pair_labeled_hist[actual] += 1
            for state in canonical_states:
                actual = grundy_canonical(state, width, height)
                assert actual == theorem_value(state, width, height)
                pair_canonical_hist[actual] += 1

            expected_maximum = 3 if height % 2 == 1 and width >= 5 else 1
            actual_maximum = max(pair_labeled_hist)
            assert actual_maximum == expected_maximum
            row.append(actual_maximum)
            labeled_total += len(labeled_states)
            canonical_total += len(canonical_states)
            labeled_histogram.update(pair_labeled_hist)
            canonical_histogram.update(pair_canonical_hist)
            parameter_pairs += 1
        maximum_by_width[str(width)] = row

    parent = (3, 3, 2, 1, 0)
    children = ((3, 3, 3, 1, 0), (3, 3, 2, 2, 0), (3, 3, 2, 1, 1))
    child_values = [theorem_value(child, 5, 3) for child in children]
    assert theorem_value(parent, 5, 3) == 3
    assert sorted(child_values) == [0, 1, 2]

    data = {
        "scope": {
            "game": "pure fiber game; degree bound t=2; forbidden-point count q=9; no base-trace constraints",
            "safe_condition": "sum_b min(c_b,2) <= 8",
            "width_range": [1, 8], "height_range": [2, 8],
            "parameter_pairs": parameter_pairs,
            "claim": "finite audit only; all-parameter theorem is proved in report.md"
        },
        "odd_height_residual_table": {
            "row_convention": "fixed R; row e=0..R; character index ell=0..R",
            "rows": {str(r): list(ROWS[r]) for r in range(CAP + 1)},
            "cells_checked_against_recurrence": table_cells,
            "direct_recursive_checks": direct_odd, "mismatches": 0
        },
        "even_height_residual_formula": {
            "formula": "min(R,2e+ell) mod 2",
            "direct_recursive_checks": direct_even, "mismatches": 0
        },
        "game_audit": {
            "canonical_multiset_states": canonical_total,
            "labeled_vector_states": labeled_total,
            "canonical_grundy_histogram": {
                str(k): canonical_histogram[k] for k in sorted(canonical_histogram)},
            "labeled_grundy_histogram": {
                str(k): labeled_histogram[k] for k in sorted(labeled_histogram)},
            "maximum_by_width_height": maximum_by_width
        },
        "minimum_width_grundy_3_witness": {
            "width": 5, "height": 3, "occupancy": list(parent), "grundy": 3,
            "children": [
                {"occupancy": list(child), "grundy": value}
                for child, value in zip(children, child_values)]
        },
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "audit_note": (
            "Finite recursive-mex checks support the formula; all-parameter scope "
            "follows from the saturation-chain decomposition and the 285-cell "
            "odd-height residual table proof.")
    }
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(payload, encoding="utf-8")
    print(payload, end="")

if __name__ == "__main__":
    main()
