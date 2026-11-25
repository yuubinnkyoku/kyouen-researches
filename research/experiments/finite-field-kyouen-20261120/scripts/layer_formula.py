"""Exact safe-layer counts on the inversive plane of order q.

Setting.  The inversive plane of order q is a 3-(q^2+1, q+1, 1) design: n = q^2+1
points, b = q(q^2+1) circles, every circle has s = q+1 points, every triple lies
on exactly one circle, and two distinct circles meet in at most 2 points.

A set S is safe iff no circle carries 4 points of S.  Write B_c for the event
"|S cap c| >= 4".  The count of safe k-sets is

    L_k = C(n,k) - |union_c B_c|.

Key structural fact.  If two distinct circles c1 != c2 both satisfy
|S cap c_i| >= 4, then

    |S| >= |S cap c1| + |S cap c2| - |c1 cap c2| >= 4 + 4 - 2 = 6.

So for k <= 5 the events B_c are pairwise disjoint and

    L_k = C(n,k) - b * sum_{j=4}^{min(k,s)} C(s,j) C(n-s, k-j)      (k <= 5).

For k >= 6 the events can overlap and the formula over-subtracts; the exact
count then needs genuine inclusion-exclusion over circle pairs.

This script verifies the k <= 5 formula and exhibits the k = 6 failure.
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


def disjoint_formula(q: int, k: int) -> int:
    """Valid for k <= 5 (see module docstring)."""
    n = q * q + 1
    b = q * (q * q + 1)
    s = q + 1
    if k < 4:
        return comb(n, k)
    per = sum(comb(s, j) * comb(n - s, k - j) for j in range(4, min(k, s) + 1))
    return comb(n, k) - b * per


def overlap_witness(q: int, circles, points) -> dict | None:
    """Find a 6-set with >=4 points on two distinct circles (the k=6 obstruction)."""
    idx = {p: i for i, p in enumerate(points)}
    blocks = [frozenset(idx[p] for p in c) for c in circles]
    for c1, c2 in itertools.combinations(blocks, 2):
        u = c1 | c2
        if len(u) <= 6:
            return {"circle1": sorted(c1), "circle2": sorted(c2), "union_size": len(u)}
    return None


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
        checks = {}
        for k, v in layers.items():
            pred = disjoint_formula(q, k)
            checks[k] = {"exact": v, "disjoint_formula": pred, "match": v == pred}
        row = {
            "q": q,
            "points": len(points),
            "circles": len(circles),
            "circle_size": q + 1,
            "layers": checks,
            "formula_valid_through_k": max(
                [k for k, c in checks.items() if c["match"]], default=-1
            ),
            "overlap_witness": overlap_witness(q, circles, points),
        }
        rows.append(row)
        print(f"q={q}: disjoint formula valid through k={row['formula_valid_through_k']}",
              flush=True)
        for k, c in checks.items():
            print(f"   k={k}: exact={c['exact']:8d} formula={c['disjoint_formula']:8d} "
                  f"{'OK' if c['match'] else 'DIFF'}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
