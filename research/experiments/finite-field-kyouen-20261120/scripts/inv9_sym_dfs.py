"""Decide the inversive plane q=9 maximum safe size with symmetry breaking.

The inversive plane of order q has automorphism group PGL(2, q^2) acting
3-transitively on the q^2+1 points.  So for a safe set of size k >= 3 we may fix
the first three points to any three fixed points.

This reduces the search by a factor of ~ (q^2+1)^3.

For q=9: 82 points, 738 circles of size 10.  Known: size 9 exists.
Question: does size 10 exist?

This script runs the fixed-target search with the first three points fixed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_bfs import build_field, circles_bfs, projective_line  # noqa: E402


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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=9)
    ap.add_argument("--target", type=int, default=10)
    ap.add_argument("--node-cap", type=int, default=100_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    pts, blocks, through = build(args.q)
    n = len(pts)
    n_blocks = len(blocks)
    print(f"q={args.q}: {n} points, {n_blocks} circles of size {len(blocks[0])}",
          flush=True)

    # PGL(2,q^2) is 3-transitive, so fix the first three points to indices 0,1,2
    fixed = [0, 1, 2]
    nodes = 0
    found = None
    target = args.target

    def rec(start: int, chosen: list, pmask: int, cnt: list):
        nonlocal nodes, found
        nodes += 1
        if nodes > args.node_cap:
            raise TimeoutError(f"node cap {args.node_cap} exceeded")
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
        rec(3, list(fixed), pmask, cnt)
    except TimeoutError as e:
        print(f"TIMEOUT: {e} nodes={nodes}", flush=True)
        return

    if found is None:
        print(f"NO safe set of size {target} with first 3 points fixed "
              f"(exhausted, nodes={nodes})", flush=True)
        print(f"  => by 3-transitivity, NO safe set of size {target} exists",
              flush=True)
        result = {"q": args.q, "target": target, "exists": False, "nodes": nodes}
    else:
        print(f"FOUND size {target}: {found} (nodes={nodes})", flush=True)
        result = {"q": args.q, "target": target, "exists": True, "nodes": nodes,
                  "witness": found}

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
