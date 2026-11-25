"""Decide AG(2,9) size 10 with full symmetry breaking.

Key fact (verified in ag9_orbits.py): GL(2,9) acts TRANSITIVELY on the 80
nonzero vectors of F_9^2.  Hence AGL(2,9) acts 2-transitively on the 81 points
of AG(2,9).

Therefore, for any safe set S of size k >= 2, we may assume:
    the first point is (0,0),
    the second point is (0,1)   (a fixed representative).

This reduces the search by a factor of 81*80 = 6480.

Moreover, the stabiliser of the ordered pair ((0,0),(0,1)) in AGL(2,9) is the
group of matrices [[1, b],[0, 1]] (shears) together with scalings that fix the
direction -- but since we only need ONE representative per orbit, fixing two
points is enough for the search.

This script runs the fixed-target search with the first two points fixed.
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
    ap.add_argument("--node-cap", type=int, default=100_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    blocks, kinds, through = make_board()
    n_blocks = len(blocks)
    n = Q * Q

    # points are indexed s*Q + t; (0,0) -> 0, (0,1) -> 1
    p0, p1 = 0, 1

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
    for p in (p0, p1):
        for bi in through[p]:
            cnt[bi] += 1
    try:
        rec(2, [p0, p1], (1 << p0) | (1 << p1), cnt)
    except TimeoutError as e:
        print(f"TIMEOUT: {e} nodes={nodes}", flush=True)
        return

    if found is None:
        print(f"NO safe set of size {target} with first two points fixed "
              f"(exhausted, nodes={nodes})", flush=True)
        print("  => by 2-transitivity, NO safe set of size "
              f"{target} exists at all", flush=True)
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
