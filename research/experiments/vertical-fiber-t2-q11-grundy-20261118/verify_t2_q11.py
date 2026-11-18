#!/usr/bin/env python3
"""Independent recursive-mex audit for the pure t=2, q=11 fiber theorem."""
import argparse
import hashlib
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

CAP = 10
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
    9: ("0000000000", "1111111111", "0000000000", "1111111111", "0000000000", "1121111111", "1000200000", "1101112111", "1000100020", "1202120212"),
    10: ("00000000000", "11111111111", "00000000000", "11111111111", "00000000000", "11111111111", "01000000000", "11101111111", "01000100000", "11101110111", "01000100010"),
}


def mex(values):
    x = 0
    while x in values:
        x += 1
    return x


@lru_cache(None)
def h_direct(e, ell, r, parity):
    if r == 0 or e + ell == 0:
        return 0
    opts = set()
    if e:
        opts.add(h_direct(e - 1, ell + 1, r - 1, parity))
    if ell:
        opts.add(parity ^ h_direct(e, ell - 1, r - 1, parity))
    return mex(opts)


def h1(e, ell, r):
    return int(ROWS[r][min(e, r)][min(ell, r)])


def h0(e, ell, r):
    return min(r, 2 * e + ell) & 1


def cost(st):
    return sum(min(x, 2) for x in st)


def theorem(st, w, m):
    s = sum(x >= 2 for x in st)
    ell = sum(x == 1 for x in st)
    e = w - s - ell
    r = CAP - 2 * s - ell
    assert r >= 0
    x = 0
    for c in st:
        if c >= 2:
            x ^= (m - c) & 1
    return x ^ (h0(e, ell, r) if m % 2 == 0 else h1(e, ell, r))


@lru_cache(None)
def g_label(st, m):
    opts = set()
    for i, c in enumerate(st):
        if c < m:
            ch = st[:i] + (c + 1,) + st[i + 1:]
            if cost(ch) <= CAP:
                opts.add(g_label(ch, m))
    return mex(opts)


@lru_cache(None)
def g_canon(st, w, m):
    opts = set()
    for i, c in enumerate(st):
        if i and st[i] == st[i - 1]:
            continue
        if c < m:
            ch = list(st)
            ch[i] += 1
            ch = tuple(sorted(ch, reverse=True))
            if cost(ch) <= CAP:
                opts.add(g_canon(ch, w, m))
    if len(st) < w and cost(st) < CAP:
        opts.add(g_canon(tuple(sorted(st + (1,), reverse=True)), w, m))
    return mex(opts)


def enum_label(w, m):
    seen, stack = set(), [(0,) * w]
    while stack:
        st = stack.pop()
        if st in seen:
            continue
        seen.add(st)
        for i, c in enumerate(st):
            if c < m:
                ch = st[:i] + (c + 1,) + st[i + 1:]
                if cost(ch) <= CAP and ch not in seen:
                    stack.append(ch)
    return seen


def enum_canon(w, m):
    seen, stack = set(), [()]
    while stack:
        st = stack.pop()
        if st in seen:
            continue
        seen.add(st)
        for i, c in enumerate(st):
            if i and st[i] == st[i - 1]:
                continue
            if c < m:
                ch = list(st)
                ch[i] += 1
                ch = tuple(sorted(ch, reverse=True))
                if cost(ch) <= CAP and ch not in seen:
                    stack.append(ch)
        if len(st) < w and cost(st) < CAP:
            ch = tuple(sorted(st + (1,), reverse=True))
            if ch not in seen:
                stack.append(ch)
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path(__file__).parent / "output/audit.json")
    out = ap.parse_args().output

    table_n, h2 = 0, {}
    for r in range(CAP + 1):
        for e in range(r + 1):
            for ell in range(r + 1):
                if r == 0 or e + ell == 0:
                    want = 0
                else:
                    opts = set()
                    if e:
                        opts.add(int(ROWS[r - 1][min(e - 1, r - 1)][min(ell + 1, r - 1)]))
                    if ell:
                        opts.add(1 ^ int(ROWS[r - 1][min(e, r - 1)][min(ell - 1, r - 1)]))
                    want = mex(opts)
                got = int(ROWS[r][e][ell])
                assert got == want, (r, e, ell, got, want)
                if got == 2:
                    h2.setdefault(str(r), []).append([e, ell])
                table_n += 1

    direct_n = 0
    for r in range(CAP + 1):
        for e in range(80):
            for ell in range(80):
                assert h_direct(e, ell, r, 1) == h1(e, ell, r)
                assert h_direct(e, ell, r, 0) == h0(e, ell, r)
                direct_n += 2

    canon_n, canon_hist, max_wh = 0, Counter(), {}
    for w in range(1, 9):
        max_wh[str(w)] = []
        for m in range(2, 10):
            states = enum_canon(w, m)
            vals = []
            for st in states:
                g = g_canon(st, w, m)
                assert g == theorem(st, w, m), (w, m, st, g, theorem(st, w, m))
                canon_hist[g] += 1
                vals.append(g)
            want = 3 if m % 2 and w >= 6 else 1
            assert max(vals) == want, (w, m, max(vals), want)
            max_wh[str(w)].append(max(vals))
            canon_n += len(states)

    label_n, label_hist, label_pairs = 0, Counter(), 0
    for w in range(1, 9):
        mmax = 7 if w <= 6 else 5
        for m in range(2, mmax + 1):
            labels, canons = enum_label(w, m), enum_canon(w, m)
            projection = {tuple(sorted((x for x in st if x), reverse=True)) for st in labels}
            assert projection == canons
            for st in labels:
                g = g_label(st, m)
                pos = tuple(sorted((x for x in st if x), reverse=True))
                assert g == g_canon(pos, w, m) == theorem(pos, w, m)
                label_hist[g] += 1
            label_n += len(labels)
            label_pairs += 1

    h2_min = []
    for s in range(CAP // 2 + 1):
        best, cells = None, []
        for ell in range(CAP - 2 * s + 1):
            r = CAP - 2 * s - ell
            for e in range(r + 1):
                if h1(e, ell, r) == 2:
                    w = s + ell + e
                    if best is None or w < best:
                        best, cells = w, [{"e": e, "ell": ell, "R": r}]
                    elif w == best:
                        cells.append({"e": e, "ell": ell, "R": r})
        assert best is None or best >= 6
        h2_min.append({"s": s, "minimum_width": best, "cells": cells})

    parent = (3, 2, 2, 2, 1, 0)
    children = (
        (3, 3, 2, 2, 1, 0),
        (3, 2, 2, 2, 2, 0),
        (3, 2, 2, 2, 1, 1),
    )
    child_g = [theorem(ch, 6, 3) for ch in children]
    assert theorem(parent, 6, 3) == 3 and sorted(child_g) == [0, 1, 2]

    audit = {
        "scope": {
            "game": "pure fiber; t=2; q=11; no base-trace constraints",
            "safe_condition": "sum min(c_b,2) <= 10",
            "theorem": "all w>=1, m>=2",
            "canonical_audit": "56 pairs: w=1..8, m=2..9",
            "labeled_audit": "44 pairs: w<=6,m<=7; w=7,8,m<=5"
        },
        "odd_height_residual": {
            "rows": {str(r): list(ROWS[r]) for r in range(CAP + 1)},
            "cells": table_n,
            "H2_cells_by_R": h2,
            "maximum": 2
        },
        "even_height_residual": {
            "formula": "min(R,2e+ell) mod 2",
            "direct_checks": direct_n // 2
        },
        "direct_residual_checks": {
            "odd": direct_n // 2, "even": direct_n // 2, "mismatches": 0
        },
        "canonical_game": {
            "states": canon_n,
            "grundy_histogram": {str(k): canon_hist[k] for k in sorted(canon_hist)},
            "maximum_by_width_height": max_wh
        },
        "labeled_game": {
            "parameter_pairs": label_pairs,
            "states": label_n,
            "grundy_histogram": {str(k): label_hist[k] for k in sorted(label_hist)}
        },
        "minimum_width_for_H2": h2_min,
        "grundy_3_witness": {
            "w": 6, "m": 3, "occupancy": [3, 2, 2, 2, 1, 0],
            "parent": 3,
            "children": [
                {"occupancy": [3, 3, 2, 2, 1, 0], "grundy": 2},
                {"occupancy": [3, 2, 2, 2, 2, 0], "grundy": 0},
                {"occupancy": [3, 2, 2, 2, 1, 1], "grundy": 1}
            ]
        },
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "mismatches": 0
    }
    payload = json.dumps(audit, ensure_ascii=False, indent=2) + "\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
