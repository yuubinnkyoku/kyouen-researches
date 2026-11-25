#!/usr/bin/env python3
"""Independent canonical-multiset Grundy audit for t=2, q=5.

Unlike verify_t2_q5.py, this checker stores only sorted positive occupancies.
It generates canonical states by combinations-with-replacement and generates
moves by incrementing one distinct occupancy or starting a fresh column.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import combinations_with_replacement
import json


def canonical_states(w: int, m: int):
    for size in range(min(w, 4) + 1):
        for values in combinations_with_replacement(range(1, m + 1), size):
            state = tuple(sorted(values, reverse=True))
            if sum(min(x, 2) for x in state) <= 4:
                yield state


def make_grundy(w: int, m: int):
    @lru_cache(maxsize=None)
    def grundy(state: tuple[int, ...]) -> int:
        options: set[int] = set()
        seen: set[int] = set()

        for i, value in enumerate(state):
            if value in seen or value == m:
                seen.add(value)
                continue
            seen.add(value)
            child = list(state)
            child[i] += 1
            child_state = tuple(sorted(child, reverse=True))
            if sum(min(x, 2) for x in child_state) <= 4:
                options.add(grundy(child_state))

        capacity = sum(min(x, 2) for x in state)
        if len(state) < w and capacity < 4:
            child_state = tuple(sorted(state + (1,), reverse=True))
            options.add(grundy(child_state))

        mex = 0
        while mex in options:
            mex += 1
        return mex
    return grundy


def closed_form(state: tuple[int, ...], m: int, w: int) -> int:
    a = tuple(sorted(state, reverse=True))
    if not a:
        return int(w == 3 and m % 2 == 1)
    if len(a) == 1:
        c = a[0]
        if c == 1:
            if m % 2 == 0:
                return 1
            return 0 if w == 3 else 2
        return (m - c) % 2
    if len(a) == 2:
        c, d = a
        if c == d == 1:
            return int(m % 2 == 1 and w == 3)
        if c >= 2 and d >= 2:
            return ((m - c) % 2) ^ ((m - d) % 2)
        saturated = c if c >= 2 else d
        if m % 2 == 0:
            return 1 - (saturated % 2)
        return 3 if saturated % 2 == 0 else 2
    if len(a) == 3:
        c = a[0]
        if c == 1:
            if m % 2 == 0:
                return 1
            return 0 if w == 3 else 2
        return (m - c) % 2
    if len(a) == 4:
        return 0
    raise AssertionError(a)


def audit():
    records = []
    total = 0
    for w in range(3, 13):
        for m in range(2, 17):
            states = list(canonical_states(w, m))
            grundy = make_grundy(w, m)
            histogram: dict[int, int] = {}
            for state in states:
                actual = grundy(state)
                predicted = closed_form(state, m, w)
                if actual != predicted:
                    raise AssertionError(
                        f"canonical mismatch w={w} m={m} state={state}: "
                        f"mex={actual}, formula={predicted}"
                    )
                histogram[actual] = histogram.get(actual, 0) + 1
            expected_max = 3 if m % 2 else 1
            if max(histogram) != expected_max:
                raise AssertionError(
                    f"canonical max mismatch w={w} m={m}: {histogram}"
                )
            records.append({
                "w": w,
                "m": m,
                "canonical_states": len(states),
                "grundy_histogram": {
                    str(k): histogram[k] for k in sorted(histogram)
                },
                "max_grundy": max(histogram),
                "mismatches": 0,
            })
            total += len(states)
    return {
        "scope": {
            "representation": "sorted positive occupancy multisets",
            "w_range": [3, 12],
            "m_range": [2, 16],
            "parameter_pairs": len(records),
        },
        "result": {
            "canonical_state_instances_checked": total,
            "mismatches": 0,
        },
        "records": records,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2, sort_keys=True))
