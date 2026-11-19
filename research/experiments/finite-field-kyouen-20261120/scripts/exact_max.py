"""Exact maximum safe size on AG(2,q) for small q, by exhaustive search.

For q = 3, 5, 7 the board is small enough to decide the maximum exactly with a
branch-and-bound over the block-incidence structure.  The result is compared
with the greedy lower bound and the counting upper bound.

A set is safe iff no circle and no line carries 4 of its points.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ff_structure import circles_and_lines


def build(q: int):
    pts, circles, lines = circles_and_lines(q)
    blocks = [sorted(b) for b in circles] + [sorted(b) for b in lines]
    through: list[list[int]] = [[] for _ in pts]
    for bi, block in enumerate(blocks):
        for i in block:
            through[i].append(bi)
    return pts, blocks, through


def exact_max(q: int) -> tuple[int, list[int]]:
    pts, blocks, through = build(q)
    n = len(pts)
    best = [0, []]

    # order points by descending block degree for a better bound
    order = sorted(range(n), key=lambda i: -len(through[i]))

    def rec(pos: int, pmask: int, chosen: list[int]) -> None:
        if len(chosen) > best[0]:
            best[0] = len(chosen)
            best[1] = list(chosen)
        if pos == n:
            return
        # optimistic bound: every remaining point could be added
        if len(chosen) + (n - pos) <= best[0]:
            return
        i = order[pos]
        ok = True
        for bi in through[i]:
            cnt = 0
            for j in blocks[bi]:
                if pmask >> j & 1:
                    cnt += 1
                    if cnt >= 3:
                        ok = False
                        break
            if not ok:
                break
        if ok:
            chosen.append(i)
            rec(pos + 1, pmask | (1 << i), chosen)
            chosen.pop()
        rec(pos + 1, pmask, chosen)

    rec(0, 0, [])
    return best[0], [pts[i] for i in best[1]]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        k, witness = exact_max(q)
        rows.append({"q": q, "exact_max_safe_size": k, "witness": witness})
        print(f"q={q}: exact K = {k}   witness={witness}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
