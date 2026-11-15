#!/usr/bin/env python3
"""Recursive-mex audits for the t=3 pure fiber games, q=4,5,6.

Two independently generated state representations:
  - canonical: sorted positive-occupancy multisets (zeros implicit, w tracked)
  - labeled: full width-w occupancy vectors
Both are checked against the closed forms in t3_formulas.py, and the two
representations are cross-checked against each other on their overlap.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from functools import lru_cache
from math import comb
from pathlib import Path

from t3_formulas import formula

T = 3


def mex(values: set[int]) -> int:
    n = 0
    while n in values:
        n += 1
    return n


def canonical_count(q: int, w: int, m: int) -> int:
    """Safe multiset count, derived combinatorially per q (t=3)."""
    if q == 4:  # (), (a) a=1..m, (1,1), (2,1), (1,1,1)
        return m + 3 + (1 if w >= 3 else 0)
    if q == 5:  # (), (a), (a,1) a=1..m, (2,2), (1,1,1), (2,1,1), (1,1,1,1)
        return 2 * m + 2 + (2 if w >= 3 else 0) + (1 if w >= 4 else 0)
    if q == 6:
        # (), (a), (a,1) a=1..m, (a,2) a=2..m, (a,1,1) a=1..m [w>=3],
        # (2,2,1) [w>=3], (1,1,1,1)+(2,1,1,1) [w>=4], (1^5) [w>=5]
        if w == 2:
            return 3 * m
        if w == 3:
            return 4 * m + 1
        if w == 4:
            return 4 * m + 3
        return 4 * m + 4
    raise AssertionError(q)


def labeled_count(q: int, w: int, m: int) -> int:
    """Safe labeled-vector count, derived combinatorially per q (t=3)."""
    if q == 4:
        return 1 + w * m + 3 * comb(w, 2) + comb(w, 3)
    if q == 5:
        return (1 + w * m + 2 * comb(w, 2) + (m - 1) * w * (w - 1)
                + 4 * comb(w, 3) + comb(w, 4))
    if q == 6:
        return (1 + w * m + 2 * comb(w, 2) + (2 * m - 3) * w * (w - 1)
                + (3 * m + 1) * comb(w, 3) + 5 * comb(w, 4) + comb(w, 5))
    raise AssertionError(q)


def canonical_values(q: int, w: int, m: int) -> dict[tuple[int, ...], int]:
    limit = q - 1

    def cap(s: tuple[int, ...]) -> int:
        return sum(min(x, T) for x in s)

    @lru_cache(None)
    def g(s: tuple[int, ...]) -> int:
        options = set()
        for i, x in enumerate(s):
            if x < m:
                t = list(s)
                t[i] += 1
                child = tuple(sorted(t, reverse=True))
                if cap(child) <= limit:
                    options.add(g(child))
        if len(s) < w and cap(s) < limit:
            options.add(g(tuple(sorted(s + (1,), reverse=True))))
        return mex(options)

    seen, stack = set(), [()]
    while stack:
        s = stack.pop()
        if s in seen:
            continue
        seen.add(s)
        for i, x in enumerate(s):
            if x < m:
                t = list(s)
                t[i] += 1
                child = tuple(sorted(t, reverse=True))
                if cap(child) <= limit and child not in seen:
                    stack.append(child)
        if len(s) < w and cap(s) < limit:
            child = tuple(sorted(s + (1,), reverse=True))
            if child not in seen:
                stack.append(child)
    return {s: g(s) for s in seen}


def labeled_audit(q: int, w: int, m: int) -> tuple[Counter, int, set]:
    limit = q - 1

    def cap(s: tuple[int, ...]) -> int:
        return sum(min(x, T) for x in s)

    @lru_cache(None)
    def g(s: tuple[int, ...]) -> int:
        options = set()
        for i, x in enumerate(s):
            if x < m:
                t = s[:i] + (x + 1,) + s[i + 1:]
                if cap(t) <= limit:
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
                if cap(t) <= limit and t not in seen:
                    stack.append(t)

    hist = Counter()
    types = set()
    for s in seen:
        value = g(s)
        hist[value] += 1
        key = tuple(sorted((x for x in s if x), reverse=True))
        types.add(key)
        assert value == formula(key, w, m, q), (q, w, m, s, value)
    return hist, len(seen), types


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    per_q = {}
    for q in (4, 5, 6):
        ch, cn, cpairs = Counter(), 0, 0
        for w in range(2, 13):
            for m in range(2, 21):
                values = canonical_values(q, w, m)
                cpairs += 1
                assert len(values) == canonical_count(q, w, m), (q, w, m)
                for s, value in values.items():
                    assert value == formula(s, w, m, q), (q, w, m, s, value)
                    ch[value] += 1
                cn += len(values)

        lh, ln, lpairs = Counter(), 0, 0
        for w in range(2, 9):
            for m in range(2, 10):
                hist, count, types = labeled_audit(q, w, m)
                assert count == labeled_count(q, w, m), (q, w, m)
                # cross-representation: labeled projection == canonical state set
                assert types == set(canonical_values(q, w, m)), (q, w, m)
                lh.update(hist)
                ln += count
                lpairs += 1
        per_q[q] = {
            "canonical_multiset_audit": {
                "w_range": [2, 12], "m_range": [2, 20],
                "parameter_pairs": cpairs, "states_checked": cn,
                "mismatches": 0,
                "grundy_histogram": {str(k): ch[k] for k in sorted(ch)},
                "maximum_grundy": max(ch)},
            "labeled_vector_audit": {
                "w_range": [2, 8], "m_range": [2, 9],
                "parameter_pairs": lpairs, "states_checked": ln,
                "mismatches": 0,
                "grundy_histogram": {str(k): lh[k] for k in sorted(lh)},
                "maximum_grundy": max(lh)},
        }

    # minimal witnesses (canonical engines)
    w4 = canonical_values(4, 2, 4)
    assert w4[(2,)] == 2 and w4[(3,)] == 1 and w4[(2, 1)] == 0
    w5 = canonical_values(5, 2, 4)
    assert w5[(1,)] == 2 and w5[(2,)] == 1 and w5[(1, 1)] == 0
    w6 = canonical_values(6, 3, 4)
    assert w6[(1, 1)] == 2 and w6[(2, 1)] == 1 and w6[(1, 1, 1)] == 0
    # q=6 w=2 has max 1 (fixed length); m odd / m=2 parity regimes max 1
    for (w, m) in [(2, 4), (3, 5), (3, 2)]:
        vals = canonical_values(6, w, m)
        assert max(vals.values()) == 1, (w, m)

    result = {
        "scope": {
            "rule": "pure fiber game; t=3; q in {4,5,6}; no base-trace constraints",
            "capacity_condition": "sum_b min(c_b,3) <= q-1",
            "grundy_convention": "mex over legal single-stone increments",
        },
        "classifications": {
            "q4": per_q[4], "q5": per_q[5], "q6": per_q[6],
        },
        "minimal_maximum_witnesses": {
            "q4": {"w": 2, "m": 4, "occupancy": [2, 0], "grundy": 2,
                   "children": [[3, 0], [2, 1]], "child_values": [1, 0]},
            "q5": {"w": 2, "m": 4, "occupancy": [1, 0], "grundy": 2,
                   "children": [[2, 0], [1, 1]], "child_values": [1, 0]},
            "q6": {"w": 3, "m": 4, "occupancy": [1, 1, 0], "grundy": 2,
                   "children": [[2, 1, 0], [1, 1, 1]], "child_values": [1, 0]},
        },
        "maximum_grundy_summary": {
            "q4": {"m odd or m=2": 1, "m even >=4": 2},
            "q5": {"m odd or m=2": 1, "m even >=4": 2},
            "q6": {"w=2 (all m)": 1, "w>=3, m odd or m=2": 1,
                   "w>=3, m even >=4": 2},
        },
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "audit_note": ("Finite recursive-mex audits support the closed forms; "
                       "the unbounded statements are proved in report.md. "
                       "Abstract fiber polynomial game; makes no claim about "
                       "any standard 2D geometric board."),
    }
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
