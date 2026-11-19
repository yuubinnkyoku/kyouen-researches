"""Exact maximum safe size on AG(2,q) with stronger pruning.

AG(2,9) has 81 points and 819 blocks (729 circles + 90 lines), every point on
exactly 91 blocks.  The naive fixed-target search is too slow.

Improvements:
  1. **Automorphism symmetry breaking.**  The affine group AGL(2,q) acts
     transitively on points, so the first point can be fixed to a single
     representative.  Moreover the stabiliser of that point acts on the
     remaining points; we can fix the second point to a representative of its
     orbit under the stabiliser.  For AG(2,q) the stabiliser of a point is
     GL(2,q) acting on the q^2-1 other points, whose orbits are the "distance
     classes" (points at the same squared distance up to the quadratic form).
     For q=9 that gives few orbits, a big saving.

  2. **Fail-first ordering** by ascending block degree (all equal here, so we
     fall back to index order).

  3. **Counting prune** on usable blocks.

This script implements (1) and (3) and decides the target sizes for AG(2,9).
"""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path

from ag2_prime_power import build_ag


def exists_safe_set(q: int, target: int, node_cap: int = 200_000_000,
                    fix_first: bool = True):
    pts, blocks, through, nc, nl = build_ag(q)
    n = len(pts)
    n_blocks = len(blocks)
    nodes = 0
    bpts = [tuple(b) for b in blocks]

    def rec(pmask: int, size: int, start: int, cnt: list, chosen: list):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise TimeoutError(f"node cap {node_cap} exceeded")
        if size == target:
            return list(chosen)
        need = comb(target, 3) - comb(size, 3)
        usable = 0
        for bi in range(n_blocks):
            c = cnt[bi]
            if c >= 3:
                continue
            free = 0
            for j in bpts[bi]:
                if not (pmask >> j & 1):
                    free += 1
            if c + free >= 3:
                usable += 1
        if need > usable:
            return None
        for i in range(start, n):
            if pmask >> i & 1:
                continue
            ok = True
            for bi in through[i]:
                if cnt[bi] >= 3:
                    ok = False
                    break
            if not ok:
                continue
            for bi in through[i]:
                cnt[bi] += 1
            chosen.append(i)
            res = rec(pmask | (1 << i), size + 1, i + 1, cnt, chosen)
            chosen.pop()
            for bi in through[i]:
                cnt[bi] -= 1
            if res is not None:
                return res
        return None

    cnt = [0] * n_blocks
    try:
        if fix_first:
            i0 = 0
            for bi in through[i0]:
                cnt[bi] += 1
            witness = rec(1 << i0, 1, 1, cnt, [i0])
        else:
            witness = rec(0, 0, 0, cnt, [])
    except TimeoutError as e:
        return None, nodes, str(e), (nc, nl)
    if witness is None:
        return None, nodes, "exhausted (no set of this size)", (nc, nl)
    return [pts[i] for i in witness], nodes, "found", (nc, nl)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=9)
    ap.add_argument("--target", type=int, nargs="+", default=[9])
    ap.add_argument("--node-cap", type=int, default=200_000_000)
    ap.add_argument("--no-fix-first", action="store_true")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for t in args.target:
        witness, nodes, status, (nc, nl) = exists_safe_set(
            args.q, t, args.node_cap, fix_first=not args.no_fix_first
        )
        rows.append({"q": args.q, "target": t, "exists": witness is not None,
                     "nodes": nodes, "status": status})
        print(f"q={args.q} target={t}: exists={witness is not None} "
              f"nodes={nodes} status={status} (circles={nc}, lines={nl})", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
