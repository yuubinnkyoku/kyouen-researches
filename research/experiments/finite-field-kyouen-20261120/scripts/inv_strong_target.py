"""Stronger exact search for "does a safe set of size k exist?" on a 3-design.

Improvements over inv_fast_target.py:

1. **Circle-pair pruning.**  Two distinct circles meet in at most 2 points.  If a
   set S has 3 points on circle C, then C is "used" and no further point of C
   may be added.  But more: for a *candidate* point p, the circles through p
   that already hold 3 points of S block p.  We precompute, for each point, the
   list of circles through it, and maintain a per-circle count of how many
   points of S it holds.  This makes the legality test O(deg) with no rescan.

2. **Look-ahead bound.**  For the remaining budget, count how many circles are
   still "usable" (holding <= 2 points of S and having at least
   (target - size) free points).  A circle that cannot reach 3 points of the
   final set cannot host a triple, so it must not be counted in the budget.

3. **Symmetry breaking** on the first point (transitivity of Aut).

4. **Fail-first ordering** by ascending degree.

The search is exact: exhausting it proves no safe set of that size exists.
"""

from __future__ import annotations

import argparse
import json
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


def exists_safe_set(q: int, target: int, node_cap: int = 200_000_000):
    pts, blocks, through = build(q)
    n = len(pts)
    n_blocks = len(blocks)
    nodes = 0

    order = sorted(range(n), key=lambda i: len(through[i]))
    rank = {p: r for r, p in enumerate(order)}

    # per-circle point lists as tuples for speed
    bpts = [tuple(b) for b in blocks]

    def rec(pmask: int, size: int, start_rank: int, cnt: list, chosen: list):
        """cnt[bi] = number of points of the current set on circle bi."""
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise TimeoutError(f"node cap {node_cap} exceeded")
        if size == target:
            return list(chosen)

        # budget prune: remaining triples must fit in circles that can still
        # reach 3 points
        remaining = target - size
        usable = 0
        for bi in range(n_blocks):
            c = cnt[bi]
            if c >= 3:
                continue
            # free points on this circle
            free = 0
            for j in bpts[bi]:
                if not (pmask >> j & 1):
                    free += 1
            if c + free >= 3:
                usable += 1
        need = comb(target, 3) - comb(size, 3)
        if need > usable:
            return None

        for r in range(start_rank, n):
            i = order[r]
            if pmask >> i & 1:
                continue
            ok = True
            for bi in through[i]:
                if cnt[bi] >= 3:
                    ok = False
                    break
            if not ok:
                continue
            for bi in through[i]:
                cnt[bi] += 1
            chosen.append(i)
            res = rec(pmask | (1 << i), size + 1, r + 1, cnt, chosen)
            chosen.pop()
            for bi in through[i]:
                cnt[bi] -= 1
            if res is not None:
                return res
        return None

    cnt = [0] * n_blocks
    try:
        i0 = order[0]
        for bi in through[i0]:
            cnt[bi] += 1
        witness = rec(1 << i0, 1, rank[i0] + 1, cnt, [i0])
    except TimeoutError as e:
        return None, nodes, str(e)
    if witness is None:
        return None, nodes, "exhausted (no set of this size)"
    return [pts[i] for i in witness], nodes, "found"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=9)
    ap.add_argument("--target", type=int, nargs="+", default=[9])
    ap.add_argument("--node-cap", type=int, default=200_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for t in args.target:
        witness, nodes, status = exists_safe_set(args.q, t, args.node_cap)
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
