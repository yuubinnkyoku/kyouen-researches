"""Exact safe-layer counts on the inversive plane, by inclusion-exclusion.

A set S is safe iff no circle carries 4 of its points.  Counting safe k-sets
directly is inclusion-exclusion over the family of "bad" events
    B_c = {S : |S cap c| >= 4}
indexed by circles c.  Because the inversive plane is a 3-(q^2+1, q+1, 1)
design, the intersection of two circles is at most 2 points, so the events for
distinct circles interact only through their point sets.

For q = 3 (circles of size 4) a 4-subset lies on at most one circle, so the
events are disjoint and the count is exactly

    L_k = C(n,k) - (#circles) * C(n-(q+1), k-4).

For q >= 5 (circles of size >= 6) a 4-subset can lie on several circles, so the
simple formula over-counts.  This script computes the exact counts by direct
enumeration for small q and reports the discrepancy, which quantifies how much
the naive inclusion-exclusion fails.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from math import comb
from pathlib import Path

from inversive_plane import GF, circles_of_inversive_plane, find_non_residue, projective_line


def exact_layers(points, circles) -> dict[int, int]:
    n = len(points)
    idx = {p: i for i, p in enumerate(points)}
    blocks = [sorted(idx[p] for p in c) for c in circles]
    through: list[list[int]] = [[] for _ in range(n)]
    for bi, b in enumerate(blocks):
        for i in b:
            through[i].append(bi)

    def can_add(i: int, pmask: int) -> bool:
        for bi in through[i]:
            cnt = 0
            for j in blocks[bi]:
                if pmask >> j & 1:
                    cnt += 1
                    if cnt >= 3:
                        return False
        return True

    layers: Counter = Counter()
    stack = [(0, 0)]
    while stack:
        start, pmask = stack.pop()
        layers[pmask.bit_count()] += 1
        for i in range(start, n):
            if pmask >> i & 1:
                continue
            if can_add(i, pmask):
                stack.append((i + 1, pmask | (1 << i)))
    return dict(sorted(layers.items()))


def naive_formula(q: int, k: int) -> int:
    n = q * q + 1
    c = q * (q * q + 1)
    s = q + 1
    v = comb(n, k)
    if k >= 4:
        v -= c * comb(n - s, k - 4)
    return v


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        d = find_non_residue(q)
        F = GF(q, d)
        points = projective_line(F)
        circles = circles_of_inversive_plane(F, points)
        layers = exact_layers(points, circles)
        row = {
            "q": q,
            "points": len(points),
            "circles": len(circles),
            "circle_size": q + 1,
            "exact_layers": layers,
            "naive_formula": {k: naive_formula(q, k) for k in layers},
            "naive_matches": all(naive_formula(q, k) == v for k, v in layers.items()),
        }
        rows.append(row)
        print(f"q={q}: naive formula matches = {row['naive_matches']}", flush=True)
        for k, v in layers.items():
            nv = naive_formula(q, k)
            print(f"   k={k}: exact={v:8d}  naive={nv:8d}  {'OK' if v == nv else 'DIFF'}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
