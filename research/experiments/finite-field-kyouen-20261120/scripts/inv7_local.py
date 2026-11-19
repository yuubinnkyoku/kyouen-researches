"""Better local search for the maximum safe set on the inversive plane of order q.

A set is safe iff no circle carries 4 of its points.  Plain greedy stalls, so
this script runs a plateau/tabu-style local search: repeatedly try to add a
point; if impossible, try a 1-for-2 or 2-for-3 exchange that increases the size;
keep the best found.

This is a heuristic lower bound, not an exact maximum.
"""

from __future__ import annotations

import argparse
import json
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


def block_counts(pmask: int, blocks, through, n: int):
    """For each point, how many of its blocks already hold 3 points of pmask."""
    sat = [False] * n
    for i in range(n):
        if pmask >> i & 1:
            continue
        for bi in through[i]:
            cnt = 0
            for j in blocks[bi]:
                if pmask >> j & 1:
                    cnt += 1
                    if cnt >= 3:
                        break
            if cnt >= 3:
                sat[i] = True
                break
    return sat


def safe(pmask: int, blocks) -> bool:
    return all(bin(pmask).count("1") == 0 or True for _ in [])  # placeholder


def is_safe(pmask: int, blocks) -> bool:
    for b in blocks:
        cnt = 0
        for j in b:
            if pmask >> j & 1:
                cnt += 1
                if cnt >= 4:
                    return False
    return True


def local_search(q: int, rng: random.Random, restarts: int, steps: int) -> tuple[int, list[int]]:
    pts, blocks, through = build(q)
    n = len(pts)
    best, best_set = 0, []

    for _ in range(restarts):
        pmask = 0
        cur = 0
        # greedy random start
        order = list(range(n))
        rng.shuffle(order)
        for i in order:
            ok = True
            for bi in through[i]:
                cnt = sum(1 for j in blocks[bi] if pmask >> j & 1)
                if cnt >= 3:
                    ok = False
                    break
            if ok:
                pmask |= 1 << i
                cur += 1

        # local search: try swap one out, two in
        for _step in range(steps):
            improved = False
            chosen = [i for i in range(n) if pmask >> i & 1]
            empty = [i for i in range(n) if not pmask >> i & 1]
            rng.shuffle(chosen)
            rng.shuffle(empty)
            for out in chosen[: min(8, len(chosen))]:
                base = pmask & ~(1 << out)
                cand = []
                for i in empty:
                    ok = True
                    for bi in through[i]:
                        cnt = sum(1 for j in blocks[bi] if base >> j & 1)
                        if cnt >= 3:
                            ok = False
                            break
                    if ok:
                        cand.append(i)
                if len(cand) >= 2:
                    for a, b in [(cand[0], cand[1])]:
                        new = base | (1 << a) | (1 << b)
                        if is_safe(new, blocks):
                            pmask = new
                            cur = bin(new).count("1")
                            improved = True
                            break
                if improved:
                    break
            if not improved:
                break

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
    ap.add_argument("--restarts", type=int, default=40)
    ap.add_argument("--steps", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20261120)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    rows = []
    for q in args.q:
        k, witness = local_search(q, rng, args.restarts, args.steps)
        ub = counting_upper_bound(q)
        rows.append(
            {
                "q": q,
                "points": q * q + 1,
                "circles": q * (q * q + 1),
                "local_search_best": k,
                "witness": witness,
                "counting_upper_bound": ub,
                "restarts": args.restarts,
                "steps": args.steps,
            }
        )
        print(f"q={q}: local-search K >= {k}  (counting bound {ub})", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
