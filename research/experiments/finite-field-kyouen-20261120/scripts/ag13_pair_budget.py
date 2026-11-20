"""Decide AG(2,13) K with a stronger prune: pencil saturation + budget.

Known: K >= 13 (size 13 found in 171 nodes).  Bound: K <= q+3 = 16.

The pencil saturation prune: if some pair {p,q} in S has all lambda_2 blocks
through it already holding 3 points of S, no more points can be added.

Let me strengthen further: for each pair {p,q} in S, count the number of blocks
through p,q that can still accept a third point.  If that number is less than
the number of points we still need to add, prune.

Actually the key insight: for a pair {p,q}, the remaining points r must each
occupy a DISTINCT block through p,q.  So if we need to add `need` more points,
we need at least `need` blocks through p,q that are not yet full.

Let me implement this "pair budget" prune.
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

    pair_blocks: dict[tuple[int, int], list[int]] = {}
    for bi, b in enumerate(blocks):
        for i in range(len(b)):
            for j in range(i + 1, len(b)):
                pair_blocks.setdefault((b[i], b[j]), []).append(bi)

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
            # pair budget prune: for each pair in S, count non-full blocks
            for a in range(len(chosen)):
                for b in range(a + 1, len(chosen)):
                    bl = pair_blocks.get((chosen[a], chosen[b]), [])
                    free = sum(1 for bi in bl if cnt[bi] < 3)
                    if free < need:
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
