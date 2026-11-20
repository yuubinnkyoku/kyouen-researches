"""Decide AG(2,9) size 10 with row-mask DFS and strong pruning.

Represent a placement as 9 row masks (each a 9-bit integer).  Constraints:
  * popcount(row) <= 3
  * popcount(column) <= 3
  * every line block (9 points) has <= 3 points
  * every conic block (8 points) has <= 3 points
  * every cross block (17 points) has <= 3 points

Process rows one at a time.  For each row choose a mask with popcount <= 3.
After choosing rows 0..r, check:
  - column counts <= 3
  - all blocks whose points lie entirely in rows 0..r have <= 3 points
  - a bound: remaining rows can add at most 3 each

The key pruning is the "closed block" check: a block is closed once all its
rows are processed.  Since blocks have 8-17 points spread over many rows, most
blocks close late.  But the column constraint and the row constraint are strong.

Additional pruning: for each block, count how many of its points are already
placed; if that count plus the number of its points in unprocessed rows is
< 4, the block can never be violated, so we can ignore it.  Conversely if a
block already has 3 points and has unprocessed points, we must forbid placing
more of its points.

Let us implement this with per-block counters.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag9_search import make_board  # noqa: E402

Q = 9


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=10)
    ap.add_argument("--node-cap", type=int, default=50_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    blocks, kinds, through = make_board()
    n_blocks = len(blocks)
    # for each point, the blocks through it
    bpts = [tuple(b) for b in blocks]

    # row masks: for each row r and each 9-bit mask m with popcount<=3,
    # precompute the list of blocks touched and the increment
    row_options = []
    for r in range(Q):
        opts = []
        for m in range(1 << Q):
            if bin(m).count("1") > 3:
                continue
            pts = [r * Q + c for c in range(Q) if m >> c & 1]
            opts.append((m, pts))
        row_options.append(opts)

    nodes = 0
    found = None
    target = args.target

    def rec(r: int, colcnt: list, blockcnt: list, chosen: list, total: int):
        nonlocal nodes, found
        nodes += 1
        if nodes > args.node_cap:
            raise TimeoutError(f"node cap {args.node_cap} exceeded")
        if found is not None:
            return
        if total == target:
            found = list(chosen)
            return
        if r == Q:
            return
        # bound: remaining rows can add at most 3 each
        if total + 3 * (Q - r) < target:
            return
        for m, pts in row_options[r]:
            if total + len(pts) > target:
                continue
            # column constraint
            ok = True
            for c in range(Q):
                if m >> c & 1 and colcnt[c] >= 3:
                    ok = False
                    break
            if not ok:
                continue
            # block constraint
            touched = []
            for p in pts:
                for bi in through[p]:
                    if blockcnt[bi] >= 3:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                continue
            # apply
            for p in pts:
                for bi in through[p]:
                    blockcnt[bi] += 1
                    touched.append(bi)
            for c in range(Q):
                if m >> c & 1:
                    colcnt[c] += 1
            chosen.extend(pts)
            rec(r + 1, colcnt, blockcnt, chosen, total + len(pts))
            for _ in pts:
                chosen.pop()
            for c in range(Q):
                if m >> c & 1:
                    colcnt[c] -= 1
            for bi in touched:
                blockcnt[bi] -= 1
            if found is not None:
                return

    try:
        rec(0, [0] * Q, [0] * n_blocks, [], 0)
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
