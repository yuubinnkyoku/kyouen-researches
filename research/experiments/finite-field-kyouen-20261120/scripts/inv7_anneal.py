"""Simulated annealing for the maximum safe set on the inversive plane.

Constraint: |S cap C| <= 3 for every circle C.

State: a safe set S.  Move: pick a random empty point p and a random subset R of
S of size 1..2, replace R by {p} (if the result is safe), else accept with a
small probability proportional to the size change.  We also allow "add" moves
when p is already addable.

This is a heuristic lower bound.  It is used to improve on plain greedy, which
stalls badly on q = 7.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from math import comb
from pathlib import Path

from inversive_plane import GF, circles_of_inversive_plane, find_non_residue, projective_line


def build(q: int):
    F = GF(q, find_non_residue(q))
    pts = projective_line(F)
    circles = circles_of_inversive_plane(F, pts)
    idx = {p: i for i, p in enumerate(pts)}
    blocks = [sorted(idx[p] for p in c) for c in circles]
    n = len(pts)
    through: list[list[int]] = [[] for _ in range(n)]
    for bi, b in enumerate(blocks):
        for i in b:
            through[i].append(bi)
    return pts, blocks, through


def is_safe(pmask: int, blocks) -> bool:
    for b in blocks:
        cnt = 0
        for j in b:
            if pmask >> j & 1:
                cnt += 1
                if cnt >= 4:
                    return False
    return True


def anneal(q: int, rng: random.Random, restarts: int, iters: int) -> tuple[int, list[int]]:
    pts, blocks, through = build(q)
    n = len(pts)
    best, best_set = 0, []

    for _ in range(restarts):
        pmask = 0
        cur = 0
        T = 1.5
        for it in range(iters):
            T = max(0.01, 1.5 * (1 - it / iters))
            empty = [i for i in range(n) if not pmask >> i & 1]
            if not empty:
                break
            p = rng.choice(empty)
            # try pure add first
            cand = pmask | (1 << p)
            if is_safe(cand, blocks):
                pmask = cand
                cur += 1
            else:
                # try remove 1 and add p
                chosen = [i for i in range(n) if pmask >> i & 1]
                if not chosen:
                    continue
                r = rng.choice(chosen)
                cand = (pmask & ~(1 << r)) | (1 << p)
                if is_safe(cand, blocks):
                    pmask = cand
                    cur = cur  # size unchanged
                else:
                    # accept a random worsening move rarely
                    if rng.random() < math.exp(-1.0 / T):
                        r2 = rng.choice([i for i in chosen if i != r])
                        cand = (pmask & ~(1 << r) & ~(1 << r2)) | (1 << p)
                        if is_safe(cand, blocks):
                            pmask = cand
                            cur -= 1
            if cur > best:
                best, best_set = cur, [i for i in range(n) if pmask >> i & 1]

    return best, [pts[i] for i in best_set]


def counting_upper_bound(q: int) -> int:
    b = q * (q * q + 1)
    k = 3
    while comb(k + 1, 3) <= b:
        k += 1
    return k


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    ap.add_argument("--restarts", type=int, default=30)
    ap.add_argument("--iters", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=20261120)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    rows = []
    for q in args.q:
        k, witness = anneal(q, rng, args.restarts, args.iters)
        ub = counting_upper_bound(q)
        rows.append(
            {
                "q": q,
                "points": q * q + 1,
                "circles": q * (q * q + 1),
                "anneal_best": k,
                "witness": witness,
                "counting_upper_bound": ub,
            }
        )
        print(f"q={q}: anneal K >= {k}  (counting bound {ub})", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
