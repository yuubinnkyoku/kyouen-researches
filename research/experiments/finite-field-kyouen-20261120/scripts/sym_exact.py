"""General symmetry-broken exact search for K on AG(2,q) and the inversive plane.

Symmetry facts:
  * AGL(2,q) acts 2-transitively on AG(2,q)  (translations + GL(2,q) transitive
    on nonzero vectors).  So for k >= 2 we may fix the first two points.
  * PGL(2, q^2) acts 3-transitively on the inversive plane of order q.
    So for k >= 3 we may fix the first three points.

This script decides "does a safe set of size k exist?" for a given board and k,
using the appropriate number of fixed points.

It also reports the number of nodes, so the difficulty is measurable.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def build_ag(q: int):
    from ag2_prime_power import build_ag as _build
    pts, blocks, through, nc, nl = _build(q)
    return pts, blocks, through


def build_inv(q: int):
    from inversive_bfs import build_field, circles_bfs, projective_line
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


def exists_safe_set(pts, blocks, through, target: int, n_fixed: int,
                    node_cap: int = 200_000_000):
    n = len(pts)
    n_blocks = len(blocks)
    nodes = 0
    found = None
    fixed = list(range(n_fixed))

    def rec(start: int, chosen: list, pmask: int, cnt: list):
        nonlocal nodes, found
        nodes += 1
        if nodes > node_cap:
            raise TimeoutError(f"node cap {node_cap} exceeded")
        if found is not None:
            return
        if len(chosen) == target:
            found = list(chosen)
            return
        need = target - len(chosen)
        if n - start < need:
            return
        for p in range(start, n):
            if pmask >> p & 1:
                continue
            ok = True
            for bi in through[p]:
                if cnt[bi] >= 3:
                    ok = False
                    break
            if not ok:
                continue
            for bi in through[p]:
                cnt[bi] += 1
            chosen.append(p)
            rec(p + 1, chosen, pmask | (1 << p), cnt)
            chosen.pop()
            for bi in through[p]:
                cnt[bi] -= 1
            if found is not None:
                return

    cnt = [0] * n_blocks
    pmask = 0
    for p in fixed:
        for bi in through[p]:
            cnt[bi] += 1
        pmask |= 1 << p
    try:
        rec(n_fixed, list(fixed), pmask, cnt)
    except TimeoutError as e:
        return None, nodes, str(e)
    if found is None:
        return None, nodes, "exhausted (no set of this size)"
    return [pts[i] for i in found], nodes, "found"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", choices=["ag", "inv"], required=True)
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--target", type=int, nargs="+", required=True)
    ap.add_argument("--node-cap", type=int, default=200_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    if args.board == "ag":
        pts, blocks, through = build_ag(args.q)
        n_fixed = 2
    else:
        pts, blocks, through = build_inv(args.q)
        n_fixed = 3
    print(f"{args.board}(q={args.q}): {len(pts)} points, {len(blocks)} blocks, "
          f"fixing {n_fixed} points", flush=True)

    rows = []
    for t in args.target:
        witness, nodes, status = exists_safe_set(
            pts, blocks, through, t, n_fixed, args.node_cap
        )
        rows.append({"target": t, "exists": witness is not None,
                     "nodes": nodes, "status": status})
        print(f"  target={t}: exists={witness is not None} nodes={nodes} "
              f"status={status}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
