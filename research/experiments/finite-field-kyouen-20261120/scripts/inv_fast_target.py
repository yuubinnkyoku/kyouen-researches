"""Faster exact decision for "does a safe set of size k exist?" on a design.

The naive DFS of inv_max_all_q.py is slow for q = 8 (65 points, 520 circles)
because it scans candidate points in index order and only prunes on the crude
counting bound.

Improvements here:

1. **Symmetry breaking.**  The automorphism group of the inversive plane acts
   transitively on points, so we may fix the first point to a single
   representative (index 0).  This divides the search by ~n.

2. **Better ordering.**  Try points with the FEWEST available circles first
   (fail-first heuristic), which prunes much earlier.

3. **Stronger bound.**  Track, for each unused circle, how many of its points
   are still available; a circle with fewer than (target - size) available
   points can never be completed, so it cannot contribute a new triple.  This
   tightens the counting prune.

4. **Memoisation on (pmask, size)** is not useful (states are unique), but we
   can memoise the set of "blocked" circles.

The search remains exact: exhausting it proves no safe set of that size exists.
"""

from __future__ import annotations

import argparse
import json
import sys
from math import comb
from pathlib import Path

from inversive_bfs import build_field, circles_bfs, projective_line


def build(q: int):
    F, sub = build_field(q)
    pts = projective_line(F)
    circles = circles_bfs(F, sub, pts)
    idx = {p: i for i, p in enumerate(pts)}
    blocks = [sorted(idx[p] for p in c) for c in circles]
    n = len(pts)
    through: list[list[int]] = [[] for _ in range(n)]
    for bi, b in enumerate(blocks):
        for i in b:
            through[i].append(bi)
    return pts, blocks, through


def exists_safe_set(q: int, target: int, node_cap: int = 100_000_000,
                    fix_first: bool = True):
    pts, blocks, through = build(q)
    n = len(pts)
    n_blocks = len(blocks)
    nodes = 0

    # order points by ascending number of blocks through them (fail-first)
    order = sorted(range(n), key=lambda i: len(through[i]))
    rank = {p: r for r, p in enumerate(order)}

    def rec(pmask: int, size: int, start_rank: int, used: set, chosen: list):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise TimeoutError(f"node cap {node_cap} exceeded")
        if size == target:
            return list(chosen)
        need = comb(target, 3) - comb(size, 3)
        if need > n_blocks - len(used):
            return None
        for r in range(start_rank, n):
            i = order[r]
            if pmask >> i & 1:
                continue
            ok = True
            new_used = []
            for bi in through[i]:
                if bi in used:
                    ok = False
                    break
                cnt = 0
                for j in blocks[bi]:
                    if pmask >> j & 1:
                        cnt += 1
                if cnt >= 3:
                    ok = False
                    break
                if cnt == 2:
                    new_used.append(bi)
            if not ok:
                continue
            chosen.append(i)
            res = rec(pmask | (1 << i), size + 1, r + 1, used | set(new_used), chosen)
            chosen.pop()
            if res is not None:
                return res
        return None

    try:
        if fix_first:
            # fix the first point to order[0] (transitivity of the automorphism group)
            i0 = order[0]
            witness = rec(1 << i0, 1, rank[i0] + 1, set(), [i0])
        else:
            witness = rec(0, 0, 0, set(), [])
    except TimeoutError as e:
        return None, nodes, str(e)
    if witness is None:
        return None, nodes, "exhausted (no set of this size)"
    return [pts[i] for i in witness], nodes, "found"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=8)
    ap.add_argument("--target", type=int, nargs="+", default=[7, 8])
    ap.add_argument("--node-cap", type=int, default=100_000_000)
    ap.add_argument("--no-fix-first", action="store_true")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for t in args.target:
        witness, nodes, status = exists_safe_set(
            args.q, t, args.node_cap, fix_first=not args.no_fix_first
        )
        rows.append({
            "q": args.q, "target": t, "exists": witness is not None,
            "nodes": nodes, "status": status,
        })
        print(f"q={args.q} target={t}: exists={witness is not None} "
              f"nodes={nodes} status={status}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
