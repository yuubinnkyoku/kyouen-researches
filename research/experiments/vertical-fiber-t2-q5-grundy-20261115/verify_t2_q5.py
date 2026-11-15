#!/usr/bin/env python3
"""Labeled-state Grundy audit for the pure t=2, q=5 fiber game.

The state generator enumerates labeled occupancy vectors directly.  It does
not use the proposed closed form to decide safety or generate transitions.
Only the Python standard library is required.
"""
from __future__ import annotations

from collections import Counter
from functools import lru_cache
from math import comb
import json


def safe_states(w: int, m: int):
    """Yield all labeled c in {0,...,m}^w with sum min(c_i,2) <= 4."""
    def visit(i: int, remaining: int, prefix: list[int]):
        if i == w:
            yield tuple(prefix)
            return
        for value in range(m + 1):
            cost = min(value, 2)
            if cost <= remaining:
                prefix.append(value)
                yield from visit(i + 1, remaining - cost, prefix)
                prefix.pop()
    yield from visit(0, 4, [])


def make_grundy(m: int):
    @lru_cache(maxsize=None)
    def grundy(state: tuple[int, ...]) -> int:
        options: set[int] = set()
        for i, value in enumerate(state):
            if value == m:
                continue
            child = list(state)
            child[i] += 1
            child_state = tuple(child)
            if sum(min(x, 2) for x in child_state) <= 4:
                options.add(grundy(child_state))
        mex = 0
        while mex in options:
            mex += 1
        return mex
    return grundy


def closed_form(state: tuple[int, ...], m: int, w: int) -> int:
    """The theorem's formula, expressed by the sorted positive occupancies."""
    a = sorted((x for x in state if x > 0), reverse=True)
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

    raise AssertionError(f"impossible safe occupancy shape: {a}")


def expected_state_count(w: int, m: int) -> int:
    # Empty; one occupied column; two arbitrary positive columns;
    # three columns of shape (a,1,1); four singleton columns.
    return (
        1 + w * m
        + comb(w, 2) * m * m
        + comb(w, 3) * (1 + 3 * (m - 1))
        + comb(w, 4)
    )


def audit():
    records = []
    total_states = 0
    total_histogram: Counter[int] = Counter()

    for w in range(3, 13):
        for m in range(2, 17):
            states = list(safe_states(w, m))
            expected = expected_state_count(w, m)
            if len(states) != expected or len(set(states)) != expected:
                raise AssertionError(
                    f"state census failed at w={w}, m={m}: "
                    f"got {len(states)}, expected {expected}"
                )

            grundy = make_grundy(m)
            histogram: Counter[int] = Counter()
            state_set = set(states)
            for state in states:
                actual = grundy(state)
                predicted = closed_form(state, m, w)
                if actual != predicted:
                    raise AssertionError(
                        f"mismatch w={w} m={m} state={state}: "
                        f"mex={actual}, formula={predicted}"
                    )
                histogram[actual] += 1

                # Check that every legal child is present in the independently
                # generated safe-state set.
                for i, value in enumerate(state):
                    if value == m:
                        continue
                    child = list(state)
                    child[i] += 1
                    child = tuple(child)
                    if sum(min(x, 2) for x in child) <= 4 and child not in state_set:
                        raise AssertionError(f"safe child omitted: {child}")

            expected_max = 3 if m % 2 else 1
            if max(histogram) != expected_max:
                raise AssertionError(
                    f"maximum nimber mismatch at w={w}, m={m}: {histogram}"
                )

            records.append({
                "w": w,
                "m": m,
                "safe_labeled_states": len(states),
                "grundy_histogram": {
                    str(k): histogram[k] for k in sorted(histogram)
                },
                "max_grundy": max(histogram),
                "mismatches": 0,
            })
            total_states += len(states)
            total_histogram.update(histogram)

    witness = (2, 1, 0)
    witness_grundy = make_grundy(3)
    child_records = []
    for i, value in enumerate(witness):
        if value == 3:
            continue
        child = list(witness)
        child[i] += 1
        child = tuple(child)
        if sum(min(x, 2) for x in child) <= 4:
            child_records.append({
                "state": list(child),
                "grundy": witness_grundy(child),
            })
    if witness_grundy(witness) != 3:
        raise AssertionError("minimal Grundy-3 witness failed")
    if sorted(x["grundy"] for x in child_records) != [0, 1, 2]:
        raise AssertionError("Grundy-3 witness children are not exactly {0,1,2}")

    return {
        "scope": {
            "rule": "pure fiber game; t=2; q=5; no base-trace constraints",
            "w_range": [3, 12],
            "m_range": [2, 16],
            "parameter_pairs": len(records),
        },
        "result": {
            "labeled_safe_state_instances_checked": total_states,
            "distinct_grundy_values": sorted(total_histogram),
            "global_histogram": {
                str(k): total_histogram[k] for k in sorted(total_histogram)
            },
            "max_grundy_by_m_parity": {"even": 1, "odd": 3},
            "mismatches": 0,
        },
        "minimal_grundy_3_witness": {
            "w": 3,
            "m": 3,
            "occupancy": list(witness),
            "grundy": witness_grundy(witness),
            "children": child_records,
        },
        "records": records,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2, sort_keys=True))
