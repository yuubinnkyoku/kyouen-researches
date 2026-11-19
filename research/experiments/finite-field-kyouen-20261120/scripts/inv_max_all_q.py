"""Maximum safe size on the inversive plane of order q, for q up to 9.

A safe set meets every circle in at most 3 points.  For q >= 7 the full
enumeration is impossible, so this script decides the maximum exactly by
running the fixed-target complete search of inv7_exact_target.py for
increasing target sizes until one fails.

The search is exact for each target: if it exhausts without a solution, no safe
set of that size exists.
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


def exists_safe_set(q: int, target: int, node_cap: int = 50_000_000):
    pts, blocks, through = build(q)
    n = len(pts)
    n_circles = len(blocks)
    nodes = 0

    def rec(pmask: int, size: int, start: int, used: set, chosen: list):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise TimeoutError(f"node cap {node_cap} exceeded")
        if size == target:
            return list(chosen)
        # counting prune
        need = comb(target, 3) - comb(size, 3)
        if need > n_circles - len(used):
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
    ap.add_argument("--q", type=int, nargs="+", default=[7, 8, 9])
    ap.add_argument("--max-target", type=int, default=12)
    ap.add_argument("--node-cap", type=int, default=50_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        results = []
        K = None
        for t in range(4, args.max_target + 1):
            witness, nodes, status = exists_safe_set(q, t, args.node_cap)
            results.append(
                {"target": t, "exists": witness is not None, "nodes": nodes, "status": status}
            )
            print(f"q={q} target={t}: exists={witness is not None} "
                  f"nodes={nodes} status={status}", flush=True)
            if witness is None:
                K = t - 1
                break
        rows.append({"q": q, "K": K, "results": results})
        print(f"q={q}: K = {K}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
