#!/usr/bin/env python3
"""Exact two-representation audit of the pure-fiber t=2, q=4 theorem."""
from collections import Counter
from functools import lru_cache
from math import comb
from pathlib import Path
import hashlib
import json


def mex(xs):
    g = 0
    while g in xs:
        g += 1
    return g


def formula(s, m, w):
    if not s:
        return (m + 1) % 2
    if len(s) == 1:
        return (m - s[0] + 1) % 2
    if len(s) == 2:
        a, b = s
        assert a == 1
        if b == 1:
            return (m + 1) % 2 if w == 2 else (1 if m % 2 == 0 else 2)
        return (m - b) % 2
    assert s == (1, 1, 1) and w >= 3
    return 0


def labeled(w, m):
    @lru_cache(None)
    def g(s):
        opts = set()
        for i, x in enumerate(s):
            if x < m:
                t = list(s)
                t[i] += 1
                t = tuple(t)
                if sum(min(y, 2) for y in t) <= 3:
                    opts.add(g(t))
        return mex(opts)

    seen = set()
    def visit(s):
        if s in seen:
            return
        seen.add(s)
        for i, x in enumerate(s):
            if x < m:
                t = list(s)
                t[i] += 1
                t = tuple(t)
                if sum(min(y, 2) for y in t) <= 3:
                    visit(t)
    visit((0,) * w)
    hist = Counter()
    for s in seen:
        hist[g(s)] += 1
        assert g(s) == formula(tuple(sorted(x for x in s if x)), m, w)
    expected = 1 + w*m + comb(w, 2)*(2*m-1) + (comb(w, 3) if w >= 3 else 0)
    assert len(seen) == expected
    return len(seen), hist


def canonical(w, m):
    @lru_cache(None)
    def g(s):
        opts = set()
        for i, x in enumerate(s):
            if x < m:
                t = list(s)
                t[i] += 1
                t = tuple(sorted(t))
                if sum(min(y, 2) for y in t) <= 3:
                    opts.add(g(t))
        if len(s) < w and sum(min(y, 2) for y in s) + 1 <= 3:
            opts.add(g(tuple(sorted(s + (1,)))))
        return mex(opts)

    seen = set()
    def visit(s):
        if s in seen:
            return
        seen.add(s)
        for i, x in enumerate(s):
            if x < m:
                t = list(s)
                t[i] += 1
                t = tuple(sorted(t))
                if sum(min(y, 2) for y in t) <= 3:
                    visit(t)
        if len(s) < w and sum(min(y, 2) for y in s) + 1 <= 3:
            visit(tuple(sorted(s + (1,))))
    visit(())
    hist = Counter()
    for s in seen:
        hist[g(s)] += 1
        assert g(s) == formula(s, m, w)
    assert len(seen) == 1 + 2*m + (1 if w >= 3 else 0)
    return len(seen), hist, g


def main():
    lt = ct = pairs = max_states = 0
    lh, ch = Counter(), Counter()
    for w in range(2, 13):
        for m in range(2, 21):
            ln, lhist = labeled(w, m)
            cn, chist, _ = canonical(w, m)
            lt += ln
            ct += cn
            pairs += 1
            max_states = max(max_states, ln)
            lh.update(lhist)
            ch.update(chist)
    _, _, witness = canonical(3, 3)
    assert witness((1, 1)) == 2 and witness((1, 2)) == 1 and witness((1, 1, 1)) == 0
    result = {
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": {"rule": "pure fiber game; t=2; q=4; no base-trace constraints",
                  "w_range": [2, 12], "m_range": [2, 20], "parameter_pairs": pairs},
        "labeled_vector_audit": {
            "states_checked": lt, "mismatches": 0,
            "state_count_formula": "1 + w*m + C(w,2)*(2*m-1) + C(w,3) for w>=3; 1 + 2*m + (2*m-1) = 4*m for w=2",
            "grundy_histogram": dict(sorted(lh.items())), "max_states_per_parameter": max_states},
        "canonical_multiset_audit": {
            "states_checked": ct, "mismatches": 0,
            "representation": "sorted positive occupancy multisets; independently generated",
            "state_count_formula": "1 + 2*m + (1 if w>=3 else 0)",
            "grundy_histogram": dict(sorted(ch.items()))},
        "maximum_grundy": {"w_eq_2": 1, "w_ge_3_even_m": 1, "w_ge_3_odd_m": 2},
        "minimal_grundy_2_witness": {
            "w": 3, "m": 3, "occupancy": [1, 1, 0],
            "children": [{"occupancy": [2, 1, 0], "grundy": 1},
                         {"occupancy": [1, 1, 1], "grundy": 0}],
            "grundy": 2}}
    out = Path(__file__).parent / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
