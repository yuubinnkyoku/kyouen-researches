#!/usr/bin/env python3
"""Recursive-mex audits for the t=2, q=6 pure fiber game."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from functools import lru_cache
from math import comb
from pathlib import Path

LIMIT = 5


def mex(values: set[int]) -> int:
    n = 0
    while n in values:
        n += 1
    return n


def formula(s: tuple[int, ...], w: int, m: int) -> int:
    s = tuple(sorted((x for x in s if x), reverse=True))
    k, total = len(s), sum(s)
    if w == 2:
        return total % 2
    if w == 3 or m % 2 == 0:
        return (total + 1) % 2
    if k == 0:
        return 1
    if k == 1:
        return (m - s[0]) % 2
    if k == 2:
        if s == (1, 1) and w == 4:
            return 2
        return (s[0] + s[1] + 1) % 2
    if k == 3:
        if s == (1, 1, 1):
            return 1 if w == 4 else 0
        if s[1] == 1:
            return 2 + ((m - s[0]) % 2)
        return (s[0] + s[1]) % 2
    if k == 4:
        if s == (1, 1, 1, 1):
            return 0 if w == 4 else 2
        return (s[0] + 1) % 2
    if k == 5:
        return 0
    raise AssertionError((w, m, s))


def canonical_count(w: int, m: int) -> int:
    return (1 + m + comb(m + 1, 2)
            + (m + comb(m, 2) if w >= 3 else 0)
            + (m if w >= 4 else 0) + (1 if w >= 5 else 0))


def labeled_count(w: int, m: int) -> int:
    return (1 + w * m + comb(w, 2) * m * m
            + comb(w, 3) * (1 + 3 * (m - 1) + 3 * (m - 1) ** 2)
            + comb(w, 4) * (1 + 4 * (m - 1)) + comb(w, 5))


def canonical_values(w: int, m: int) -> dict[tuple[int, ...], int]:
    @lru_cache(None)
    def g(s: tuple[int, ...]) -> int:
        options = set()
        cap = sum(min(x, 2) for x in s)
        for i, x in enumerate(s):
            if x < m:
                t = list(s)
                t[i] += 1
                child = tuple(sorted(t, reverse=True))
                if sum(min(y, 2) for y in child) <= LIMIT:
                    options.add(g(child))
        if len(s) < w and cap < LIMIT:
            options.add(g(tuple(sorted(s + (1,), reverse=True))))
        return mex(options)

    seen, stack = set(), [()]
    while stack:
        s = stack.pop()
        if s in seen:
            continue
        seen.add(s)
        cap = sum(min(x, 2) for x in s)
        for i, x in enumerate(s):
            if x < m:
                t = list(s)
                t[i] += 1
                child = tuple(sorted(t, reverse=True))
                if sum(min(y, 2) for y in child) <= LIMIT and child not in seen:
                    stack.append(child)
        if len(s) < w and cap < LIMIT:
            child = tuple(sorted(s + (1,), reverse=True))
            if child not in seen:
                stack.append(child)
    return {s: g(s) for s in seen}


def labeled_audit(w: int, m: int) -> tuple[Counter, int]:
    def cap(s: tuple[int, ...]) -> int:
        return sum(min(x, 2) for x in s)

    @lru_cache(None)
    def g(s: tuple[int, ...]) -> int:
        options = set()
        for i, x in enumerate(s):
            if x < m:
                t = s[:i] + (x + 1,) + s[i + 1:]
                if cap(t) <= LIMIT:
                    options.add(g(t))
        return mex(options)

    seen, stack = set(), [(0,) * w]
    while stack:
        s = stack.pop()
        if s in seen:
            continue
        seen.add(s)
        for i, x in enumerate(s):
            if x < m:
                t = s[:i] + (x + 1,) + s[i + 1:]
                if cap(t) <= LIMIT and t not in seen:
                    stack.append(t)

    hist = Counter()
    for s in seen:
        value = g(s)
        hist[value] += 1
        key = tuple(sorted((x for x in s if x), reverse=True))
        assert value == formula(key, w, m), (w, m, s, value, formula(key, w, m))
    return hist, len(seen)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    ch, cn, cpairs = Counter(), 0, 0
    for w in range(2, 13):
        for m in range(2, 21):
            values = canonical_values(w, m)
            cpairs += 1
            assert len(values) == canonical_count(w, m)
            for s, value in values.items():
                assert value == formula(s, w, m), (w, m, s, value)
                ch[value] += 1
            cn += len(values)

    lh, ln, lpairs = Counter(), 0, 0
    for w in range(2, 9):
        for m in range(2, 10):
            hist, count = labeled_audit(w, m)
            assert count == labeled_count(w, m)
            lh.update(hist)
            ln += count
            lpairs += 1

    witness = canonical_values(4, 3)
    parent = (2, 1, 1)
    children = {(3, 1, 1), (2, 2, 1), (2, 1, 1, 1)}
    child_rows = [
        {"occupancy": list(s) + [0] * (4 - len(s)), "grundy": witness[s]}
        for s in sorted(children, reverse=True)
    ]
    assert witness[parent] == 3
    assert sorted(row["grundy"] for row in child_rows) == [0, 1, 2]
    assert (cpairs, cn, lpairs, ln) == (209, 36860, 56, 137004)
    assert max(ch) == max(lh) == 3

    result = {
        "scope": {
            "rule": "pure fiber game; t=2; q=6; no base-trace constraints",
            "capacity_condition": "sum_b min(c_b,2) <= 5",
            "canonical_w_range": [2, 12],
            "canonical_m_range": [2, 20],
            "canonical_parameter_pairs": cpairs,
            "labeled_w_range": [2, 8],
            "labeled_m_range": [2, 9],
            "labeled_parameter_pairs": lpairs
        },
        "canonical_multiset_audit": {
            "representation": "sorted positive occupancy multisets; independently generated",
            "states_checked": cn,
            "state_count_formula": "1 + m + C(m+1,2) + [w>=3]*(m+C(m,2)) + [w>=4]*m + [w>=5]",
            "mismatches": 0,
            "grundy_histogram": {str(k): ch[k] for k in sorted(ch)},
            "maximum_grundy": max(ch)
        },
        "labeled_vector_audit": {
            "representation": "full labeled width-w occupancy vectors; independently generated",
            "states_checked": ln,
            "state_count_formula": "1 + w*m + C(w,2)*m^2 + C(w,3)*(1+3*(m-1)+3*(m-1)^2) + C(w,4)*(1+4*(m-1)) + C(w,5)",
            "mismatches": 0,
            "grundy_histogram": {str(k): lh[k] for k in sorted(lh)},
            "maximum_grundy": max(lh)
        },
        "minimal_grundy_3_witness": {
            "w": 4, "m": 3, "occupancy": [2, 1, 1, 0],
            "grundy": 3, "children": child_rows
        },
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "audit_note": "Finite recursive-mex audits support the formulas; the unbounded theorem is proved in report.md."
    }
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
