"""Decide AG(2,9) size 10 with a much stronger search.

The cross constraint alone leaves ~4.7e10 candidates, so a plain DFS is hopeless.
We need to use the LINE blocks (90 of size 9) and CONIC blocks (648 of size 8)
as early as possible.

Key idea: process the grid ROW BY ROW, and after each row, check all blocks that
are already "closed" (i.e. all their points are in processed rows).  This prunes
early.

Even better: use the fact that a safe set meets every LINE in at most 3 points.
The 90 lines are: 9 horizontal (rows), 9 vertical (columns), and 72 diagonal
(8 directions x 9 offsets).  So the constraint is:

  * every row has <= 3 points,
  * every column has <= 3 points,
  * every diagonal (in each of 8 directions) has <= 3 points.

This is a strong "no 4 in a line" constraint on a 9x9 toroidal-like grid.

Let us first check: how many 10-subsets of the 9x9 grid satisfy "no 4 in any
line (row, column, or the 8 diagonal directions)"?  If that number is small,
we can enumerate them and test the conics.

This script counts them with a DFS over cells, using the line constraints.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag9_search import make_board  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=10)
    ap.add_argument("--node-cap", type=int, default=100_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    blocks, kinds, through = make_board()
    Q = 9
    # line blocks are those of size 9
    lines = [tuple(b) for b, k in zip(blocks, kinds) if k == "line"]
    conics = [tuple(b) for b, k in zip(blocks, kinds) if k == "conic"]
    crosses = [tuple(b) for b, k in zip(blocks, kinds) if k == "cross"]
    print(f"lines={len(lines)} conics={len(conics)} crosses={len(crosses)}",
          flush=True)

    # For each point, the lines through it
    line_through = [[] for _ in range(Q * Q)]
    for li, L in enumerate(lines):
        for p in L:
            line_through[p].append(li)

    nodes = 0
    found = None
    target = args.target

    def rec(start: int, chosen: list, pmask: int, linecnt: list):
        nonlocal nodes, found
        nodes += 1
        if nodes > args.node_cap:
            raise TimeoutError(f"node cap {args.node_cap} exceeded")
        if found is not None:
            return
        if len(chosen) == target:
            # check conics and crosses
            for b in conics:
                c = 0
                for p in b:
                    if pmask >> p & 1:
                        c += 1
                        if c >= 4:
                            return
            for b in crosses:
                c = 0
                for p in b:
                    if pmask >> p & 1:
                        c += 1
                        if c >= 4:
                            return
            found = list(chosen)
            return
        need = target - len(chosen)
        if Q * Q - start < need:
            return
        for p in range(start, Q * Q):
            if pmask >> p & 1:
                continue
            ok = True
            for li in line_through[p]:
                if linecnt[li] >= 3:
                    ok = False
                    break
            if not ok:
                continue
            for li in line_through[p]:
                linecnt[li] += 1
            chosen.append(p)
            rec(p + 1, chosen, pmask | (1 << p), linecnt)
            chosen.pop()
            for li in line_through[p]:
                linecnt[li] -= 1
            if found is not None:
                return

    try:
        rec(0, [], 0, [0] * len(lines))
    except TimeoutError as e:
        print(f"TIMEOUT: {e} nodes={nodes}", flush=True)
        return

    if found is None:
        print(f"NO safe set of size {target} (exhausted, nodes={nodes})", flush=True)
        result = {"target": target, "exists": False, "nodes": nodes}
    else:
        print(f"FOUND size {target}: {found} (nodes={nodes})", flush=True)
        result = {"target": target, "exists": True, "nodes": nodes, "witness": found}

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
