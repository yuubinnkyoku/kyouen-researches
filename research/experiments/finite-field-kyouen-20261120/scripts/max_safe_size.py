"""Maximum safe-set size on AG(2,q) using block incidence, not quad lists.

A set S is safe iff no circle and no line carries 4 points of S.  Instead of
materialising the (very numerous) forbidden 4-subsets, we keep for every point
the list of blocks through it and test "does adding p complete a 4-in-a-block"
by counting, for each block through p, how many of its points are already in S.

Cost per candidate point is O(sum over blocks through p of |block|) = O(q^2),
which is far cheaper than scanning quad lists.

Double counting triples gives the upper bound

    C(k,3) <= (#circles) + (#lines) = q^2(q-1) + q(q+1) = q^3 + q.
"""

from __future__ import annotations

import argparse
import json
import random
from math import comb
from pathlib import Path

from ff_structure import circles_and_lines


def build_incidence(q: int):
    pts, circles, lines = circles_and_lines(q)
    blocks = [sorted(b) for b in circles] + [sorted(b) for b in lines]
    through: list[list[int]] = [[] for _ in pts]
    for bi, block in enumerate(blocks):
        for i in block:
            through[i].append(bi)
    return pts, blocks, through


def can_add(i: int, pmask: int, blocks, through) -> bool:
    """True iff adding point i keeps the set safe (no block reaches 4 points)."""
    for bi in through[i]:
        cnt = 0
        for j in blocks[bi]:
            if pmask >> j & 1:
                cnt += 1
                if cnt >= 3:
                    return False
    return True


def greedy(through, blocks, n: int, rng: random.Random) -> list[int]:
    idx = list(range(n))
    rng.shuffle(idx)
    chosen: list[int] = []
    pmask = 0
    for i in idx:
        if can_add(i, pmask, blocks, through):
            chosen.append(i)
            pmask |= 1 << i
    return chosen


def counting_upper_bound(q: int) -> int:
    budget = q**3 + q
    k = 3
    while comb(k + 1, 3) <= budget:
        k += 1
    return k


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7, 11, 13, 17, 19])
    ap.add_argument("--trials", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20261120)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    rows = []
    for q in args.q:
        pts, blocks, through = build_incidence(q)
        best, best_set = 0, None
        for _ in range(args.trials):
            s = greedy(through, blocks, len(pts), rng)
            if len(s) > best:
                best, best_set = len(s), s
        ub = counting_upper_bound(q)
        rows.append(
            {
                "q": q,
                "points": len(pts),
                "blocks": len(blocks),
                "greedy_best": best,
                "greedy_witness": [pts[i] for i in best_set] if best_set else None,
                "counting_upper_bound": ub,
                "trials": args.trials,
            }
        )
        print(
            f"q={q:3d}: greedy K>={best:3d}  counting K<={ub:3d}  "
            f"(board {len(pts)}, blocks {len(blocks)})",
            flush=True,
        )

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
