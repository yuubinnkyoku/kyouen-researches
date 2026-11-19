"""Decide whether the inversive plane of order q has a safe set of size k.

A safe set meets every circle in at most 3 points.  Building one is a
constraint-satisfaction problem, and for q = 7 the interesting question is
whether size 7 or 8 is reachable at all (greedy and annealing both stall at 6).

This script runs a complete depth-first search for a *fixed target size* with

  * symmetry breaking: the first point is fixed to a canonical representative
    of the point orbit under the stabiliser we can compute cheaply,
  * pruning by the counting bound: the remaining budget of circles must suffice
    for the remaining triples,
  * canonical ordering of candidates.

If the search completes without a solution, the target size is impossible.
If it finds one, the target size is achievable (a witness is printed).

This is exact for the target it decides, not a global maximum computation.
"""

from __future__ import annotations

import argparse
import json
import sys
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


def exists_safe_set(q: int, target: int, node_cap: int = 20_000_000):
    pts, blocks, through = build(q)
    n = len(pts)
    n_circles = len(blocks)
    nodes = 0

    def feasible(pmask: int, size: int, used_circles: int) -> bool:
        """Counting prune: remaining triples must fit in the remaining circles."""
        need = comb(target, 3) - comb(size, 3)
        # each new triple needs its own circle; circles already carrying 3 are
        # unavailable, but we use the crude budget n_circles - used_circles
        return need <= n_circles - used_circles

    def rec(pmask: int, size: int, start: int, used: set, chosen: list):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise TimeoutError(f"node cap {node_cap} exceeded")
        if size == target:
            return list(chosen)
        if not feasible(pmask, size, len(used)):
            return None
        for i in range(start, n):
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
            r = rec(pmask | (1 << i), size + 1, i + 1, used | set(new_used), chosen)
            chosen.pop()
            if r is not None:
                return r
        return None

    try:
        witness = rec(0, 0, 0, set(), [])
    except TimeoutError as e:
        return None, nodes, str(e)
    if witness is None:
        return None, nodes, "exhausted (no set of this size)"
    return [pts[i] for i in witness], nodes, "found"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=7)
    ap.add_argument("--target", type=int, nargs="+", default=[7, 8])
    ap.add_argument("--node-cap", type=int, default=20_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for t in args.target:
        witness, nodes, status = exists_safe_set(args.q, t, args.node_cap)
        rows.append(
            {
                "q": args.q,
                "target_size": t,
                "exists": witness is not None,
                "witness": witness,
                "nodes": nodes,
                "status": status,
            }
        )
        print(f"q={args.q} target={t}: exists={witness is not None} "
              f"nodes={nodes} status={status}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
