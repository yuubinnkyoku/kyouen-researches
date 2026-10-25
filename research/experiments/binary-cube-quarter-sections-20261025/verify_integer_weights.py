#!/usr/bin/env python3
"""Finite integer-weight audit of the exact-quarter section classification.

For each sorted positive integer weight tuple, enumerate all subset-sum levels.
This finite check is not a proof for arbitrary real weights.
"""
from collections import Counter
from itertools import combinations_with_replacement
import argparse
import json


def predicted_levels(w):
    k = len(w)
    if k == 2:
        a, b = w
        return {0, 2*a} if a == b else {0, a, b, a+b}
    if k == 3:
        a, b, c = w
        if a == b == c:
            return set()
        if a == b:
            return {a, a+c} | ({c} if c == 2*a else set())
        if b == c:
            return {b, a+b} | ({a} if a == 2*b else set())
        if a+b == c:
            return {c}
        return set()
    if k == 4:
        a, b, c, d = w
        if a == b == c == d:
            return {a, 3*a}
        if a == b and c == d and b != c:
            return {a+c}
        if a == b == c and d == 2*a:
            return {2*a, 3*a}
        return set()
    if k == 5:
        a, b, c, d, e = w
        if a == b == c == d and e == 2*a:
            return {3*a}
    return set()


def observed_levels(w):
    counts = {0: 1}
    for a in w:
        next_counts = {}
        for s, v in counts.items():
            next_counts[s] = next_counts.get(s, 0) + v
            next_counts[s+a] = next_counts.get(s+a, 0) + v
        counts = next_counts
    return {s for s, v in counts.items() if 4*v == (1 << len(w))}


def verify(bound=8, max_support=9):
    rows = []
    for k in range(2, max_support+1):
        examined = matching = 0
        for w in combinations_with_replacement(range(1, bound+1), k):
            examined += 1
            actual = observed_levels(w)
            expected = predicted_levels(w)
            if actual != expected:
                raise AssertionError(
                    f"k={k} weights={w} expected={sorted(expected)} actual={sorted(actual)}")
            matching += bool(actual)
        rows.append({"support": k, "tested_weight_multisets": examined,
                     "with_quarter_section": matching})
    return {"max_coefficient": bound, "rows": rows,
            "total_weight_multisets": sum(r["tested_weight_multisets"] for r in rows)}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--bound", type=int, default=8)
    p.add_argument("--max-support", type=int, default=9)
    args = p.parse_args()
    print(json.dumps(verify(args.bound, args.max_support), indent=2))
