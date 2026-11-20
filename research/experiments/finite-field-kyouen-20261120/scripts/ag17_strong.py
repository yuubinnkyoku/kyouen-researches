"""Decide AG(2,17) K exactly with the block-budget prune.

AG(2,17): 289 points, 5219 blocks (4624 of size 16, 306 of size 17, 289 of size 33).
Known: size 17 exists (11,633 nodes).  Size 18 is undecided.

The block-budget prune: for a partial set S of size s and target k,
    need_triples = C(k,3) - C(s,3)
    available = #blocks that can still reach 3 points of the final set
    if need_triples > available: prune

Plus fail-first ordering by the number of "almost full" blocks.

This script decides size 18 (and 19 if feasible).
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
    ap.add_argument("--q", type=int, default=17)
    ap.add_argument("--target", type=int, nargs="+", default=[18])
    ap.add_argument("--node-cap", type=int, default=100_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    pts, blocks, through, nc, nl = build_ag(args.q)
    n = len(pts)
    n_blocks = len(blocks)
    bpts = [tuple(b) for b in blocks]
    print(f"AG(2,{args.q}): {n} points, {n_blocks} blocks", flush=True)

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
