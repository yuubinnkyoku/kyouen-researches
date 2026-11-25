"""Decide AG(2,9) size 10 using the cross structure as a strong constraint.

Key structural facts for AG(2,9) (verified in ag9_board.py):
  * 81 points arranged as a 9x9 grid (split coordinates s,t).
  * 81 "cross" blocks: for each (column c, row r), the union of column c and
    row r, of size 17.  A safe set meets each cross in at most 3 points.
  * 90 line blocks of size 9.
  * 648 conic blocks of size 8.

The cross constraint alone gives: for all (c,r),
    a_c + b_r - x_{cr} <= 3
where a_c = |S cap col c|, b_r = |S cap row r|, x_{cr} in {0,1}.

This implies a_c <= 3 and b_r <= 3 for all c,r (taking r with x=0 or using
the sum over r).

Strategy: enumerate all 9x9 0/1 matrices with row and column sums <= 3 and
satisfying the cross constraint, with exactly k ones, then test the remaining
738 blocks.  The cross constraint is very restrictive: it forces that if a
column has 3 points, then every row can have at most 1 point in that column's
"cross" sense...

Actually let us just enumerate directly with a DFS over columns, tracking the
row counts, and prune with the cross constraint.  For k=10 the search space is
manageable if we prune well.

This script does an exact DFS over the 9x9 grid.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag9_search import make_board  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=10)
    ap.add_argument("--node-cap", type=int, default=200_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    blocks, kinds, through = make_board()
    Q = 9
    n = Q * Q
    # index of point (s,t) -> s*Q + t
    def idx(s, t):
        return s * Q + t

    # precompute for each point the list of blocks through it (as tuples)
    bpts = [tuple(b) for b in blocks]
    nodes = 0
    found = None

    # DFS over columns; state = row counts
    def rec(col: int, rowcnt: list, chosen: list, pmask: int):
        nonlocal nodes, found
        nodes += 1
        if nodes > args.node_cap:
            raise TimeoutError(f"node cap {args.node_cap} exceeded")
        if found is not None:
            return
        if len(chosen) == args.target:
            # verify all blocks
            ok = True
            for b in bpts:
                c = 0
                for p in b:
                    if pmask >> p & 1:
                        c += 1
                        if c >= 4:
                            ok = False
                            break
                if not ok:
                    break
            if ok:
                found = list(chosen)
            return
        if col == Q:
            return
        # remaining columns
        remaining_cols = Q - col
        need = args.target - len(chosen)
        if need > 2 * remaining_cols:
            return
        # choose 0,1,2 points in this column
        for k in (0, 1, 2):
            if k > need:
                continue
            for rows in itertools.combinations(range(Q), k):
                # cross constraint: a_col = k, b_row = rowcnt[r] + (r in rows)
                ok = True
                for r in range(Q):
                    present = 1 if r in rows else 0
                    if k + rowcnt[r] + present - present > 3:
                        # a_c + b_r - x_cr <= 3 with x_cr = present
                        # a_c = k, b_r = rowcnt[r] + present
                        # so k + rowcnt[r] + present - present = k + rowcnt[r]
                        if k + rowcnt[r] > 3:
                            ok = False
                            break
                if not ok:
                    continue
                # also need: after placing, row counts <= 3
                newcnt = list(rowcnt)
                for r in rows:
                    newcnt[r] += 1
                    if newcnt[r] > 3:
                        ok = False
                        break
                if not ok:
                    continue
                # place
                newmask = pmask
                for r in rows:
                    newmask |= 1 << idx(col, r)
                chosen.extend(idx(col, r) for r in rows)
                rec(col + 1, newcnt, chosen, newmask)
                for _ in rows:
                    chosen.pop()
                if found is not None:
                    return

    try:
        rec(0, [0] * Q, [], 0)
    except TimeoutError as e:
        print(f"TIMEOUT: {e}", flush=True)
        print(f"nodes={nodes}", flush=True)
        return

    if found is None:
        print(f"NO safe set of size {args.target} exists (exhausted, nodes={nodes})",
              flush=True)
        result = {"target": args.target, "exists": False, "nodes": nodes}
    else:
        print(f"FOUND safe set of size {args.target}: {found}", flush=True)
        print(f"nodes={nodes}", flush=True)
        result = {"target": args.target, "exists": True, "nodes": nodes,
                  "witness": found}

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
