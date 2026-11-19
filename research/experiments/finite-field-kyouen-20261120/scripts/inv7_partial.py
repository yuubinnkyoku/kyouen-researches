"""Inversive plane of order q: structural results for q = 7 without full enumeration.

For q = 7 the design has n = 50 points and b = 350 circles of size s = 8, so the
full safe-set enumeration of q = 3, 5 is out of reach.  What is still exact:

(1) the design axioms (verified by construction),
(2) the safe-layer count L_k for k <= 5, via the disjoint-event formula
        L_k = C(n,k) - b * sum_{j=4}^{min(k,s)} C(s,j) C(n-s, k-j),
    justified because two circles meet in at most 2 points, so two bad events
    can coexist only from k = 6 onwards,
(3) a greedy lower bound and a counting upper bound on K.

This script computes those and reports them, making clear which are exact and
which are bounds.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
from math import comb
from pathlib import Path

from inversive_plane import GF, circles_of_inversive_plane, find_non_residue, projective_line


def disjoint_layer(q: int, k: int) -> int:
    n = q * q + 1
    b = q * (q * q + 1)
    s = q + 1
    if k < 4:
        return comb(n, k)
    per = sum(comb(s, j) * comb(n - s, k - j) for j in range(4, min(k, s) + 1))
    return comb(n, k) - b * per


def counting_upper_bound(q: int) -> int:
    """C(k,3) <= b (each triple on exactly one circle, each circle holds <= 3)."""
    b = q * (q * q + 1)
    k = 3
    while comb(k + 1, 3) <= b:
        k += 1
    return k


def greedy_lower(q: int, circles, rng: random.Random, trials: int) -> int:
    pts = projective_line(GF(q, find_non_residue(q)))
    idx = {p: i for i, p in enumerate(pts)}
    blocks = [sorted(idx[p] for p in c) for c in circles]
    n = len(pts)
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

    best = 0
    for _ in range(trials):
        order = list(range(n))
        rng.shuffle(order)
        pmask = 0
        size = 0
        for i in order:
            if can_add(i, pmask):
                pmask |= 1 << i
                size += 1
        best = max(best, size)
    return best


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[7])
    ap.add_argument("--trials", type=int, default=300)
    ap.add_argument("--seed", type=int, default=20261120)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    rows = []
    for q in args.q:
        F = GF(q, find_non_residue(q))
        pts = projective_line(F)
        circles = circles_of_inversive_plane(F, pts)
        n = len(pts)
        b = len(circles)
        s = len(next(iter(circles))) if circles else 0

        layers = {k: disjoint_layer(q, k) for k in range(0, 6)}
        upper = counting_upper_bound(q)
        lower = greedy_lower(q, circles, rng, args.trials)

        rows.append(
            {
                "q": q,
                "points": n,
                "circles": b,
                "circle_size": s,
                "layer_counts_k_le_5_exact": layers,
                "K_lower_greedy": lower,
                "K_upper_counting": upper,
                "trials": args.trials,
            }
        )
        print(f"q={q}: points={n} circles={b} circle_size={s}", flush=True)
        print(f"   exact layer counts (k<=5): {layers}", flush=True)
        print(f"   K: {lower} <= K <= {upper}  (greedy {args.trials} trials, counting bound)",
              flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
