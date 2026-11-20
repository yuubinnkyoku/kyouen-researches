"""Decide AG(2,13) K exactly, using the bound K <= q+3 = 16.

Known: K >= 13 (size 13 found in 171 nodes).  Bound: K <= 16.
So we need to decide sizes 14, 15, 16.

The search space is large.  Let me use the strongest available pruning:
  * symmetry breaking (fix first 2 points, by 2-transitivity),
  * block-budget prune,
  * fail-first ordering.

Plus: since K <= 16, if we find size 16 we are done (bound attained).
If size 16 is impossible, try 15, then 14.

Let me also use a "pencil saturation" prune: for the current partial set S,
for each pair {p,q} in S, count how many blocks through p,q already contain a
third point of S.  If some pair has all lambda_2 blocks saturated, then no more
points can be added (since any new point r would need a block through p,q
containing p,q,r, but all are used).  That is a strong prune!

Actually more precisely: if a pair {p,q} has all lambda_2 blocks through it
already containing 3 points of S, then adding any new point r would create the
triple {p,q,r} which must lie on a block through p,q -- but all such blocks
already have 3 points of S, so the block would have 4 points.  Contradiction.
So the search can be pruned.

This is a very strong prune.  Let me implement it.
"""

from __future__ import annotations

import argparse
import json
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=13)
    ap.add_argument("--target", type=int, nargs="+", default=[14])
    ap.add_argument("--node-cap", type=int, default=50_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    pts, blocks, through, nc, nl = build_ag(args.q)
    n = len(pts)
    n_blocks = len(blocks)
    bpts = [tuple(b) for b in blocks]
    print(f"AG(2,{args.q}): {n} points, {n_blocks} blocks", flush=True)

    # for each pair of points, the list of blocks through both
    pair_blocks: dict[tuple[int, int], list[int]] = {}
    for bi, b in enumerate(blocks):
        for i in range(len(b)):
            for j in range(i + 1, len(b)):
                key = (b[i], b[j])
                pair_blocks.setdefault(key, []).append(bi)
    print(f"  pairs with blocks: {len(pair_blocks)}", flush=True)

    rows = []
    for target in args.target:
        nodes = 0
        found = None
        fixed = [0, 1]

        def rec(start: int, chosen: list, pmask: int, cnt: list):
            nonlocal nodes, found
            nodes += 1
            if nodes > args.node_cap:
                raise TimeoutError(f"node cap {args.node_cap} exceeded")
            if found is not None:
                return
            s = len(chosen)
            if s == target:
                found = list(chosen)
                return
            need = target - s
            if n - start < need:
                return
            # pencil saturation prune: if some pair in S has all its blocks
            # already holding 3 points of S, no more points can be added
            for a in range(len(chosen)):
                for b in range(a + 1, len(chosen)):
                    key = (chosen[a], chosen[b])
                    bl = pair_blocks.get(key, [])
                    if bl and all(cnt[bi] >= 3 for bi in bl):
                        return
            # block budget prune
            need_triples = comb(target, 3) - comb(s, 3)
            available = 0
            for bi in range(n_blocks):
                c = cnt[bi]
                if c >= 3:
                    continue
                free = 0
                for j in bpts[bi]:
                    if not (pmask >> j & 1):
                        free += 1
                if c + free >= 3:
                    available += 1
            if need_triples > available:
                return
            cands = []
            for p in range(start, n):
                if pmask >> p & 1:
                    continue
                ok = True
                cost = 0
                for bi in through[p]:
                    if cnt[bi] >= 3:
                        ok = False
                        break
                    if cnt[bi] == 2:
                        cost += 1
                if ok:
                    cands.append((cost, p))
            cands.sort()
            for cost, p in cands:
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
            rec(2, list(fixed), pmask, cnt)
        except TimeoutError as e:
            print(f"  target={target}: TIMEOUT ({e}) nodes={nodes}", flush=True)
            rows.append({"target": target, "status": "timeout", "nodes": nodes})
            continue

        if found is None:
            print(f"  target={target}: NO (exhausted, nodes={nodes})", flush=True)
            rows.append({"target": target, "exists": False, "nodes": nodes})
        else:
            print(f"  target={target}: FOUND (nodes={nodes})", flush=True)
            rows.append({"target": target, "exists": True, "nodes": nodes,
                         "witness": found})

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
