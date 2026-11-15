#!/usr/bin/env python3
"""Two-representation recursive-mex audit for the full t=3, q=7 classification.

Independent checks:
  1. canonical multiset engine vs t3q7_formulas.formula (w=1..12, m=2..20)
  2. labeled width-w vector engine vs formula (w=1..8, m=2..12)
  3. cross-representation projection agreement
  4. E_TABLE self-consistency: every table state satisfies its own mex
     equation with children read from the table (finite complete check of
     the closed residual box), and an independent memoized recursion
     reproduces the table on the box and the e0-saturation lemma
  5. per-(w,m) maxima reproduce the published max-value theorem
  6. labeled histogram reproduces the published max-value audit histogram
     (w=1..8, m=2..12: 0:91819, 1:76926, 2:8505, 3:2490)
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

from t3q7_formulas import CAPACITY, E_TABLE, T, formula

PUBLISHED_HISTOGRAM = {"0": 91819, "1": 76926, "2": 8505, "3": 2490}


def mex(values: set[int]) -> int:
    n = 0
    while n in values:
        n += 1
    return n


def canonical_engine(w: int, m: int) -> dict[tuple[int, ...], int]:
    def cap(s: tuple[int, ...]) -> int:
        return sum(min(x, T) for x in s)

    @lru_cache(None)
    def g(s: tuple[int, ...]) -> int:
        opts: set[int] = set()
        for i, v in enumerate(s):
            if v < m:
                t = list(s)
                t[i] += 1
                ch = tuple(sorted(t, reverse=True))
                if cap(ch) <= CAPACITY:
                    opts.add(g(ch))
        if len(s) < w and cap(s) < CAPACITY:
            opts.add(g(tuple(sorted(s + (1,), reverse=True))))
        return mex(opts)

    seen, stack = set(), [()]
    while stack:
        s = stack.pop()
        if s in seen:
            continue
        seen.add(s)
        for i, v in enumerate(s):
            if v < m:
                t = list(s)
                t[i] += 1
                ch = tuple(sorted(t, reverse=True))
                if cap(ch) <= CAPACITY and ch not in seen:
                    stack.append(ch)
        if len(s) < w and cap(s) < CAPACITY:
            ch = tuple(sorted(s + (1,), reverse=True))
            if ch not in seen:
                stack.append(ch)
    return {s: g(s) for s in seen}


def labeled_engine(w: int, m: int) -> dict[tuple[int, ...], int]:
    def cap(s: tuple[int, ...]) -> int:
        return sum(min(x, T) for x in s)

    @lru_cache(None)
    def g(s: tuple[int, ...]) -> int:
        opts: set[int] = set()
        for i, v in enumerate(s):
            if v < m:
                ch = s[:i] + (v + 1,) + s[i + 1:]
                if cap(ch) <= CAPACITY:
                    opts.add(g(ch))
        return mex(opts)

    seen, stack = set(), [(0,) * w]
    while stack:
        s = stack.pop()
        if s in seen:
            continue
        seen.add(s)
        for i, v in enumerate(s):
            if v < m:
                ch = s[:i] + (v + 1,) + s[i + 1:]
                if cap(ch) <= CAPACITY and ch not in seen:
                    stack.append(ch)
    return {s: g(s) for s in seen}


@lru_cache(None)
def e_recurse(R: int, e0: int, e1: int, e2: int) -> int:
    """Independent memoized recursion for the m even >= 4 residual game."""
    opts: set[int] = set()
    if R >= 1:
        if e0 >= 1:
            opts.add(e_recurse(R - 1, e0 - 1, e1 + 1, e2))
        if e1 >= 1:
            opts.add(e_recurse(R - 1, e0, e1 - 1, e2 + 1))
        if e2 >= 1:
            opts.add(1 ^ e_recurse(R - 1, e0, e1, e2 - 1))
    return mex(opts)


def box_states() -> list[tuple[int, int, int, int]]:
    """All states of the closed residual box: D = R+e1+2e2 in {0,3,6}, e0<=R."""
    states = []
    for D in (6, 3, 0):
        for R in range(0, D + 1):
            t = D - R
            for e2 in range(0, t // 2 + 1):
                e1 = t - 2 * e2
                for e0 in range(0, R + 1):
                    states.append((R, e0, e1, e2))
    return sorted(states)


def table_lookup(R: int, e0: int, e1: int, e2: int) -> int:
    """E value with the (universally proved) e0-saturation lemma applied."""
    return E_TABLE[(R, min(e0, R), e1, e2)]


def closed_box_states(e0_max: int = 9) -> list[tuple[int, int, int, int]]:
    """Closed residual box: D = R+e1+2e2 in {0,3,6}, 0 <= e0 <= e0_max.

    Closed under the residual recursion (children keep e0 <= e0_max,
    keep D in {0,3,6}, and R >= 0 whenever a move exists).
    """
    states = []
    for D in (6, 3, 0):
        for R in range(0, D + 1):
            t = D - R
            for e2 in range(0, t // 2 + 1):
                e1 = t - 2 * e2
                for e0 in range(0, e0_max + 1):
                    states.append((R, e0, e1, e2))
    return sorted(states)


def check_e_table() -> dict:
    issues: list[str] = []
    sat_states = box_states()
    assert len(sat_states) == 64
    assert set(sat_states) == set(E_TABLE), "table keys != saturated box states"
    box = closed_box_states(9)
    # (a) mex fixed-point check on the closed box: every state satisfies its
    #     own mex equation with child values read from the table (with the
    #     e0-saturation lemma applied to children whose e0 exceeds their R).
    for (R, e0, e1, e2) in box:
        opts: set[int] = set()
        if R >= 1:
            if e0 >= 1:
                opts.add(table_lookup(R - 1, e0 - 1, e1 + 1, e2))
            if e1 >= 1:
                opts.add(table_lookup(R - 1, e0, e1 - 1, e2 + 1))
            if e2 >= 1:
                opts.add(1 ^ table_lookup(R - 1, e0, e1, e2 - 1))
        want = mex(opts)
        if table_lookup(R, e0, e1, e2) != want:
            issues.append(f"mex fixed-point fails at {(R, e0, e1, e2)}")
    # (b) independent unconstrained memoized recursion reproduces the table
    #     (with saturation) on the whole closed box, e0 <= 9.
    for key in box:
        if e_recurse(*key) != table_lookup(*key):
            issues.append(f"independent recursion disagrees at {key}")
    # (c) saturation spot check up to e0 = 20 on saturated edge states.
    for (R, e0, e1, e2) in sat_states:
        if e0 == R:
            for big in range(R + 1, 21):
                if e_recurse(R, big, e1, e2) != E_TABLE[(R, e0, e1, e2)]:
                    issues.append(f"saturation fails at (R={R}, e0={big})")
    # (d) value range.
    if sorted(set(E_TABLE.values())) != [0, 1, 2]:
        issues.append("table values are not exactly {0,1,2}")
    assert not issues, issues[:10]
    return {
        "saturated_table_states": len(sat_states),
        "closed_box_states_checked": len(box),
        "closed_box_e0_range": [0, 9],
        "mex_fixed_point_on_closed_box": "PASS",
        "independent_recursion_matches_table": "PASS",
        "e0_saturation_spot_check_e0_le_20": "PASS",
        "table_value_set": sorted(set(E_TABLE.values())),
        "issues": 0,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    e_table_audit = check_e_table()

    # 1. canonical multiset audit
    ch: Counter = Counter()
    cn = cpairs = 0
    maxima: dict[str, int] = {}
    for w in range(1, 13):
        for m in range(2, 21):
            vals = canonical_engine(w, m)
            cpairs += 1
            for s, v in vals.items():
                f = formula(s, w, m)
                assert f == v, ("canonical mismatch", w, m, s, v, f)
                ch[v] += 1
            cn += len(vals)
            mx = max(vals.values())
            maxima[f"{w},{m}"] = mx
            assert mx == (3 if w >= 3 and m >= 4 and m % 2 == 0 else 1), (w, m, mx)

    # 2. labeled audit with cross-representation projection
    lh: Counter = Counter()
    ln = lpairs = 0
    for w in range(1, 9):
        for m in range(2, 13):
            labeled = labeled_engine(w, m)
            canonical = canonical_engine(w, m)
            projection: dict[tuple[int, ...], int] = {}
            for vec, v in labeled.items():
                key = tuple(sorted((x for x in vec if x), reverse=True))
                prev = projection.setdefault(key, v)
                assert prev == v, ("permutation mismatch", w, m, vec)
                assert formula(key, w, m) == v, ("labeled mismatch", w, m, vec, v)
                lh[v] += 1
            assert set(projection) == set(canonical), ("state-set mismatch", w, m)
            for s, v in canonical.items():
                assert projection[s] == v, ("cross-rep mismatch", w, m, s)
            ln += len(labeled)
            lpairs += 1

    histogram = {str(k): lh[k] for k in sorted(lh)}
    assert histogram == PUBLISHED_HISTOGRAM, (histogram, PUBLISHED_HISTOGRAM)

    result = {
        "scope": {
            "rule": "pure fiber game; t=3; q=7; no base-trace constraints",
            "safety": "sum_b min(c_b,3) <= 6",
            "classification": ("w=1 chain parity; w>=2 m odd: x XOR "
                               "min(R,3e0+2e1+e2) mod 2; m=2: "
                               "min(6-|S|,2w-|S|) mod 2; m even >=4: "
                               "x XOR E-table"),
        },
        "e_table_audit": e_table_audit,
        "canonical_multiset_audit": {
            "w_range": [1, 12], "m_range": [2, 20],
            "parameter_pairs": cpairs, "states_checked": cn,
            "mismatches": 0,
            "grundy_histogram": {str(k): ch[k] for k in sorted(ch)},
        },
        "labeled_vector_audit": {
            "w_range": [1, 8], "m_range": [2, 12],
            "parameter_pairs": lpairs, "states_checked": ln,
            "mismatches": 0,
            "grundy_histogram": histogram,
            "matches_published_maxvalue_audit_histogram": True,
        },
        "per_pair_maxima_match_published_theorem": True,
        "verifier_sha256": hashlib.sha256(
            Path(__file__).read_bytes()).hexdigest(),
        "formulas_sha256": hashlib.sha256(
            Path(__file__).with_name("t3q7_formulas.py").read_bytes()).hexdigest(),
        "audit_note": (
            "Finite recursive-mex audits support the closed forms; the "
            "universal statements are proved in report.md. Abstract fiber "
            "polynomial game; no claim about any standard 2D board."),
    }
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload)


if __name__ == "__main__":
    main()
