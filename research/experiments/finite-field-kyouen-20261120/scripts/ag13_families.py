"""Why does AG(2,q) allow larger safe sets than the inversive plane?

For q=13: AG K >= 13, inversive K = 10.

Both boards have nearly the same number of points (169 vs 170) and the same
number of blocks (2379 vs 2210).  But the block SIZE distributions differ:

  AG(2,13):   circles of size 14 (2028 of them), lines of size 13 (182)
  inversive:  circles of size 14 (2210 of them)

So AG has 182 blocks of size 13 (the lines) that the inversive plane lacks,
and 182 fewer circles.

Hypothesis: the LINES are "easier" constraints than circles because they are
smaller (13 vs 14 points) and because a line meets a circle in at most 2 points,
so the line constraints are "independent" of the circle constraints in a way
that gives more freedom.

Let us test this by computing, for AG(2,13), the maximum safe size when we
DROP the line constraints (circles only).  If that maximum is much larger,
the lines are not the limiting factor.  If it is smaller, the lines are
actually helping to constrain.

Actually the right comparison: the inversive plane of order q is AG(2,q) plus
one point at infinity, with lines replaced by "lines + infinity".  So the
inversive plane has FEWER distinct blocks (2210 vs 2379) but each line-block is
one point larger.

Let us compute:
  (a) AG(2,13) circles only (drop lines): max safe size?
  (b) AG(2,13) lines only: max safe size?
  (c) full AG(2,13): >= 13

This tells us which family of blocks is binding.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def max_safe(pts, blocks, n_fixed: int, node_cap: int = 20_000_000):
    n = len(pts)
    n_blocks = len(blocks)
    through: list[list[int]] = [[] for _ in range(n)]
    for bi, b in enumerate(blocks):
        for i in b:
            through[i].append(bi)
    nodes = 0
    best = [0]

    def rec(start: int, chosen: list, pmask: int, cnt: list):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise TimeoutError
        if len(chosen) > best[0]:
            best[0] = len(chosen)
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
    except TimeoutError:
        return best[0], nodes, "timeout"
    return best[0], nodes, "complete"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=13)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    pts, blocks, through, nc, nl = build_ag(args.q)
    circles = [b for b in blocks if len(b) == args.q + 1]
    lines = [b for b in blocks if len(b) == args.q]
    print(f"AG(2,{args.q}): {len(pts)} points, {nc} circles (size {args.q+1}), "
          f"{nl} lines (size {args.q})", flush=True)

    rows = []
    for name, bl in [("circles only", circles), ("lines only", lines),
                     ("full", blocks)]:
        k, nodes, status = max_safe(pts, bl, 2)
        rows.append({"family": name, "blocks": len(bl), "max_safe": k,
                     "nodes": nodes, "status": status})
        print(f"  {name}: {len(bl)} blocks -> max safe >= {k} "
              f"(nodes={nodes}, {status})", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
