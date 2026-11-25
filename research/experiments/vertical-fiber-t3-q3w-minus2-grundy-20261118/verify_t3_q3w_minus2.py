#!/usr/bin/env python3
"""Independent finite audit for the t=3, q=3w-2 pure-fiber Grundy theorem."""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path


def mex(values: tuple[int, ...] | list[int]) -> int:
    seen = set(values)
    n = 0
    while n in seen:
        n += 1
    return n


@lru_cache(maxsize=None)
def residual_even_mex(e0: int, e1: int, e2: int) -> int:
    """Exact residual mex recurrence for even m (spawn nimber z=1)."""
    remaining = 3 * e0 + 2 * e1 + e2
    if remaining == 3:
        return 0
    options: list[int] = []
    if e0:
        options.append(residual_even_mex(e0 - 1, e1 + 1, e2))
    if e1:
        options.append(residual_even_mex(e0, e1 - 1, e2 + 1))
    if e2:
        options.append(1 ^ residual_even_mex(e0, e1, e2 - 1))
    return mex(options)


@lru_cache(maxsize=None)
def residual_odd_mex(e0: int, e1: int, e2: int) -> int:
    """Exact residual mex recurrence for odd m (spawn nimber z=0)."""
    remaining = 3 * e0 + 2 * e1 + e2
    if remaining == 3:
        return 0
    options: list[int] = []
    if e0:
        options.append(residual_odd_mex(e0 - 1, e1 + 1, e2))
    if e1:
        options.append(residual_odd_mex(e0, e1 - 1, e2 + 1))
    if e2:
        options.append(residual_odd_mex(e0, e1, e2 - 1))
    return mex(options)


def residual_even_formula(e0: int, e1: int, e2: int) -> int:
    """Closed form for even-height residual states with 3e0+2e1+e2 >= 3."""
    if 3 * e0 + 2 * e1 + e2 < 3:
        raise ValueError("unsafe residual state")
    if (e0 >= 1 and e2 == e0) or (e0 == 0 and e2 == 2):
        return 2
    if e0 == 0 and e2 <= 1:
        return (e1 + 1) & 1
    if (e0, e1, e2) == (1, 0, 0):
        return 0
    return (e1 + (1 if e2 < e0 else 0)) & 1


def residual_odd_formula(e0: int, e1: int, e2: int) -> int:
    remaining = 3 * e0 + 2 * e1 + e2
    if remaining < 3:
        raise ValueError("unsafe residual state")
    return (remaining - 3) & 1


def safe(c: tuple[int, ...]) -> bool:
    w = len(c)
    return sum(min(v, 3) for v in c) <= 3 * w - 3


@lru_cache(maxsize=None)
def full_ordered_mex(m: int, c: tuple[int, ...]) -> int:
    """Direct game recursion retaining the labels of all fibers."""
    options: list[int] = []
    for i, value in enumerate(c):
        if value == m:
            continue
        child = list(c)
        child[i] += 1
        child_tuple = tuple(child)
        if safe(child_tuple):
            options.append(full_ordered_mex(m, child_tuple))
    return mex(options)


@lru_cache(maxsize=None)
def full_canonical_mex(m: int, c: tuple[int, ...]) -> int:
    """Independent direct recursion on sorted occupancy multisets."""
    options: list[int] = []
    for i, value in enumerate(c):
        if value == m:
            continue
        child = list(c)
        child[i] += 1
        child_tuple = tuple(sorted(child))
        if safe(child_tuple):
            options.append(full_canonical_mex(m, child_tuple))
    return mex(options)


def full_formula(m: int, c: tuple[int, ...]) -> int:
    w = len(c)
    if not safe(c):
        raise ValueError("unsafe board state")
    if m == 1:
        return 0 if w == 1 else (w - sum(c)) & 1
    if m == 2:
        if w == 1:
            return 0
        if w == 2:
            return (3 - sum(c)) & 1
        return sum((2 - v) & 1 for v in c) & 1

    e0 = sum(v == 0 for v in c)
    e1 = sum(v == 1 for v in c)
    e2 = sum(v == 2 for v in c)
    chain_xor = 0
    for v in c:
        if v >= 3:
            chain_xor ^= (m - v) & 1
    if m & 1:
        residual = residual_odd_formula(e0, e1, e2)
    else:
        residual = residual_even_formula(e0, e1, e2)
    return chain_xor ^ residual


def audit_once() -> dict:
    failures: list[dict] = []
    residual_even_count = 0
    residual_odd_count = 0

    residual_even_mex.cache_clear()
    residual_odd_mex.cache_clear()
    full_ordered_mex.cache_clear()
    full_canonical_mex.cache_clear()

    BOX = 32
    for e0 in range(BOX + 1):
        for e1 in range(BOX + 1):
            for e2 in range(BOX + 1):
                remaining = 3 * e0 + 2 * e1 + e2
                if remaining < 3:
                    continue
                actual_even = residual_even_mex(e0, e1, e2)
                expected_even = residual_even_formula(e0, e1, e2)
                residual_even_count += 1
                if actual_even != expected_even:
                    failures.append({
                        "kind": "residual-even",
                        "state": [e0, e1, e2],
                        "actual": actual_even,
                        "expected": expected_even,
                    })
                actual_odd = residual_odd_mex(e0, e1, e2)
                expected_odd = residual_odd_formula(e0, e1, e2)
                residual_odd_count += 1
                if actual_odd != expected_odd:
                    failures.append({
                        "kind": "residual-odd",
                        "state": [e0, e1, e2],
                        "actual": actual_odd,
                        "expected": expected_odd,
                    })

    board_states = 0
    by_parameter: list[dict] = []
    nimber_histogram: Counter[int] = Counter()
    for w in range(1, 6):
        for m in range(1, 8):
            count = 0
            local_hist: Counter[int] = Counter()
            for c in itertools.product(range(m + 1), repeat=w):
                if not safe(c):
                    continue
                ordered = full_ordered_mex(m, c)
                canonical = full_canonical_mex(m, tuple(sorted(c)))
                expected = full_formula(m, c)
                count += 1
                board_states += 1
                local_hist[expected] += 1
                nimber_histogram[expected] += 1
                if ordered != canonical or ordered != expected:
                    failures.append({
                        "kind": "full-board",
                        "w": w,
                        "m": m,
                        "state": list(c),
                        "ordered": ordered,
                        "canonical": canonical,
                        "formula": expected,
                    })
            by_parameter.append({
                "w": w,
                "m": m,
                "safe_states": count,
                "nimber_histogram": {str(k): local_hist[k] for k in sorted(local_hist)},
            })

    witnesses = {
        "w1_m4_empty": (4, (0,)),
        "w2_m4": (4, (0, 2)),
        "w3_m4": (4, (0, 2, 3)),
        "w3_m5_empty": (5, (0, 0, 0)),
    }
    witness_results = {}
    for name, (m, c) in witnesses.items():
        value = full_formula(m, c)
        direct = full_ordered_mex(m, c)
        witness_results[name] = {"m": m, "occupancies": list(c), "grundy": value}
        if value != direct:
            failures.append({"kind": "witness", "name": name, "direct": direct, "formula": value})

    return {
        "all_pass": not failures,
        "target": "pure fiber game t=3, q=3w-2",
        "residual_box": {"e0": [0, BOX], "e1": [0, BOX], "e2": [0, BOX]},
        "counts": {
            "residual_even_mex_vs_formula": residual_even_count,
            "residual_odd_mex_vs_formula": residual_odd_count,
            "full_board_states_two_direct_engines_vs_formula": board_states,
        },
        "full_board_parameters": by_parameter,
        "full_board_nimber_histogram": {str(k): nimber_histogram[k] for k in sorted(nimber_histogram)},
        "sharp_maximum_witnesses": witness_results,
        "failures": failures,
    }


def run() -> None:
    first = audit_once()
    second = audit_once()
    same = (
        json.dumps(first, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        == json.dumps(second, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    )
    payload = dict(first)
    payload["repeat_runs"] = 2
    payload["repeat_byte_identical"] = same
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    payload["sha256_without_hash_field"] = hashlib.sha256(raw).hexdigest()
    output = Path(__file__).with_name("output")
    output.mkdir(parents=True, exist_ok=True)
    (output / "audit.json").write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "all_pass": payload["all_pass"],
        "repeat_byte_identical": same,
        "counts": payload["counts"],
        "failures": len(payload["failures"]),
        "sha256_without_hash_field": payload["sha256_without_hash_field"],
    }, ensure_ascii=False, sort_keys=True))
    if not payload["all_pass"] or not same:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
