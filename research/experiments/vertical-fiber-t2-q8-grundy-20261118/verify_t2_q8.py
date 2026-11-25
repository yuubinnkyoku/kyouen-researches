#!/usr/bin/env python3
"""Recursive-mex audit for the pure t=2, q=8 fiber theorem."""
from __future__ import annotations
import argparse
import hashlib
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

CAP = 7
ROWS = {
    0: ("0",),
    1: ("00", "12"),
    2: ("000", "111", "010"),
    3: ("0000", "1111", "0020", "0212"),
    4: ("00000", "11111", "00000", "10111", "00010"),
    5: ("000000", "111111", "000000", "112111", "100020", "120212"),
    6: ("0000000", "1111111", "0000000", "1111111", "0100000", "1110111", "0100010"),
    7: ("00000000", "11111111", "00000000", "11111111", "00200000", "01112111", "00100020", "02120212"),
}

def mex(values: set[int]) -> int:
    x = 0
    while x in values:
        x += 1
    return x

@lru_cache(None)
def h_direct(e: int, ell: int, r: int, p: int) -> int:
    if r == 0 or e + ell == 0:
        return 0
    options = set()
    if e:
        options.add(h_direct(e - 1, ell + 1, r - 1, p))
    if ell:
        options.add(p ^ h_direct(e, ell - 1, r - 1, p))
    return mex(options)

def h1(e: int, ell: int, r: int) -> int:
    return int(ROWS[r][min(e, r)][min(ell, r)])

def cap(state: tuple[int, ...]) -> int:
    return sum(min(x, 2) for x in state)

def formula(state: tuple[int, ...], w: int, m: int) -> int:
    s = sum(x >= 2 for x in state)
    ell = sum(x == 1 for x in state)
    e = w - s - ell
    r = CAP - 2 * s - ell
    assert r >= 0
    x = 0
    for a in state:
        if a >= 2:
            x ^= (m - a) & 1
    h = (min(r, 2 * e + ell) & 1) if m % 2 == 0 else h1(e, ell, r)
    return x ^ h

@lru_cache(None)
def g_can(state: tuple[int, ...], w: int, m: int) -> int:
    opts = set()
    for i, a in enumerate(state):
        if i and state[i] == state[i - 1]:
            continue
        if a < m:
            child = list(state)
            child[i] += 1
            child = tuple(sorted(child, reverse=True))
            if cap(child) <= CAP:
                opts.add(g_can(child, w, m))
    if len(state) < w and cap(state) < CAP:
        opts.add(g_can(tuple(sorted(state + (1,), reverse=True)), w, m))
    return mex(opts)

@lru_cache(None)
def g_lab(state: tuple[int, ...], m: int) -> int:
    opts = set()
    for i, a in enumerate(state):
        if a < m:
            child = state[:i] + (a + 1,) + state[i + 1:]
            if cap(child) <= CAP:
                opts.add(g_lab(child, m))
    return mex(opts)

def enum_can(w: int, m: int) -> set[tuple[int, ...]]:
    seen, stack = set(), [()]
    while stack:
        state = stack.pop()
        if state in seen:
            continue
        seen.add(state)
        for i, a in enumerate(state):
            if i and state[i] == state[i - 1]:
                continue
            if a < m:
                child = list(state)
                child[i] += 1
                child = tuple(sorted(child, reverse=True))
                if cap(child) <= CAP and child not in seen:
                    stack.append(child)
        if len(state) < w and cap(state) < CAP:
            child = tuple(sorted(state + (1,), reverse=True))
            if child not in seen:
                stack.append(child)
    return seen

def enum_lab(w: int, m: int) -> set[tuple[int, ...]]:
    seen, stack = set(), [(0,) * w]
    while stack:
        state = stack.pop()
        if state in seen:
            continue
        seen.add(state)
        for i, a in enumerate(state):
            if a < m:
                child = state[:i] + (a + 1,) + state[i + 1:]
                if cap(child) <= CAP and child not in seen:
                    stack.append(child)
    return seen

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path(__file__).parent / "output/audit.json")
    out = ap.parse_args().output

    h1_checks = h0_checks = 0
    for r in range(8):
        for e in range(21):
            for ell in range(21):
                assert h_direct(e, ell, r, 1) == h1(e, ell, r)
                assert h_direct(e, ell, r, 0) == (min(r, 2 * e + ell) & 1)
                h1_checks += 1
                h0_checks += 1

    table_checks = 0
    for r in range(8):
        for e in range(r + 1):
            for ell in range(r + 1):
                if r == 0 or e + ell == 0:
                    expected = 0
                else:
                    opts = set()
                    if e:
                        opts.add(h1(e - 1, ell + 1, r - 1))
                    if ell:
                        opts.add(1 ^ h1(e, ell - 1, r - 1))
                    expected = mex(opts)
                assert h1(e, ell, r) == expected
                table_checks += 1

    canonical_total = labeled_total = 0
    canonical_hist, labeled_hist = Counter(), Counter()
    max_by_width, mismatches = {}, 0
    for w in range(1, 9):
        row = []
        for m in range(2, 9):
            cs, ls = enum_can(w, m), enum_lab(w, m)
            ch, lh = Counter(), Counter()
            for state in cs:
                actual = g_can(state, w, m)
                assert actual == formula(state, w, m), ("canonical", w, m, state, actual)
                ch[actual] += 1
            for state in ls:
                actual = g_lab(state, m)
                positive = tuple(sorted((x for x in state if x), reverse=True))
                assert actual == formula(positive, w, m), ("labeled", w, m, state, actual)
                assert actual == g_can(positive, w, m), ("cross", w, m, state, actual)
                lh[actual] += 1
            expected_max = 3 if m % 2 and w >= 5 else 1
            assert max(ch) == max(lh) == expected_max, ("maximum", w, m, ch, lh)
            row.append(expected_max)
            canonical_total += len(cs)
            labeled_total += len(ls)
            canonical_hist.update(ch)
            labeled_hist.update(lh)
        max_by_width[str(w)] = row

    parent = (3, 2, 1, 1, 0)
    children = ((3, 3, 1, 1, 0), (3, 2, 2, 1, 0), (3, 2, 1, 1, 1))
    child_values = [formula(child, 5, 3) for child in children]
    assert formula(parent, 5, 3) == 3 and sorted(child_values) == [0, 1, 2]

    data = {
        "scope": {
            "game": "pure fiber game; degree bound t=2; forbidden-point count q=8; no base-trace constraints",
            "safe_condition": "sum_b min(c_b,2) <= 7",
            "width_range": [1, 8], "height_range": [2, 8], "parameter_pairs": 56,
            "claim": "finite audit only; all-parameter theorem is proved in report.md",
        },
        "residual_table": {
            "row_convention": "fixed R; row e=0..R; character index ell=0..R",
            "rows": {str(r): list(ROWS[r]) for r in range(8)},
            "recurrence_entries_checked": table_checks,
            "direct_h1_checks": h1_checks, "direct_h0_checks": h0_checks,
            "mismatches": 0,
        },
        "game_audit": {
            "canonical_multiset_states": canonical_total,
            "labeled_vector_states": labeled_total,
            "canonical_grundy_histogram": {str(k): canonical_hist[k] for k in sorted(canonical_hist)},
            "labeled_grundy_histogram": {str(k): labeled_hist[k] for k in sorted(labeled_hist)},
            "mismatches": mismatches, "maximum_by_width_height": max_by_width,
        },
        "minimum_width_grundy_3_witness": {
            "width": 5, "height": 3, "occupancy": list(parent), "grundy": 3,
            "children": [{"occupancy": list(c), "grundy": v} for c, v in zip(children, child_values)],
        },
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "audit_note": "Finite recursive-mex checks support the formula; all-parameter scope follows from the decomposition and finite residual table proof.",
    }
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(payload, encoding="utf-8")
    print(payload, end="")

if __name__ == "__main__":
    main()
