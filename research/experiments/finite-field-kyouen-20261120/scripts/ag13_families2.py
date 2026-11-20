"""Test the line-block hypothesis: does removing lines change K?

Hypothesis: AG(2,q) allows larger safe sets than the inversive plane because it
has extra LINE blocks, and lines interact weakly with circles.

Test: compute the maximum safe size on AG(2,13) with
  (a) circles only (drop the 182 lines),
  (b) lines only (drop the 2028 circles),
  (c) full board.

If (a) is much larger than (c), the lines are binding (they restrict).
If (a) is close to (c), the circles alone already restrict.

Note: the inversive plane of order q is AG(2,q) plus a point at infinity with
lines replaced by "line + infinity".  So comparing (a) with the inversive K
tells us whether the lines matter.

Use a bounded search (node cap) and report the best found, clearly marking it
as a lower bound when the cap is hit.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def best_safe(pts, blocks, n_fixed: int, node_cap: int):
    n = len(pts)
    n_blocks = len(blocks)
    through: list[list[int]] = [[] for _ in range(n)]
    for bi, b in enumerate(blocks):
        for i in b:
            through[i].append(bi)
    nodes = 0
    best = [0, None]

    def rec(start: int, chosen: list, pmask: int, cnt: list):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise TimeoutError
        if len(chosen) > best[0]:
            best[0] = len(chosen)
            best[1] = list(chosen)
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

    cnt = [0] * n_blocks
    pmask = 0
    for p in range(n_fixed):
        for bi in through[p]:
            cnt[bi] += 1
        pmask |= 1 << p
    try:
        rec(n_fixed, list(range(n_fixed)), pmask, cnt)
        return best[0], nodes, "complete"
    except TimeoutError:
        return best[0], nodes, "capped"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=13)
    ap.add_argument("--node-cap", type=int, default=3_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    pts, blocks, through, nc, nl = build_ag(args.q)
    circles = [b for b in blocks if len(b) != args.q]  # everything that is not a line
    lines = [b for b in blocks if len(b) == args.q]
    print(f"AG(2,{args.q}): {len(pts)} points, {nc} circles, {nl} lines",
          flush=True)

    rows = []
    for name, bl in [("circles only", circles), ("lines only", lines),
                     ("full", blocks)]:
        k, nodes, status = best_safe(pts, bl, 2, args.node_cap)
        rows.append({"family": name, "blocks": len(bl), "best_safe": k,
                     "nodes": nodes, "status": status})
        print(f"  {name}: {len(bl)} blocks -> best safe {k} "
              f"(nodes={nodes}, {status})", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
