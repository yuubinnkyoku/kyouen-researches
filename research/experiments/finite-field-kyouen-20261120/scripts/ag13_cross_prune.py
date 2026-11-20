"""Decide AG(2,13) size 14 with the strongest available pruning.

If size 14 is impossible, then K = 13 = q, confirming the conjecture
K = q for q = 1 mod 4.

Pruning strategies:
  1. symmetry breaking (fix first 2 points),
  2. pencil saturation (if a pair's pencil is full, prune),
  3. pair budget (need <= free blocks in each pencil),
  4. block budget (need_triples <= available blocks),
  5. fail-first ordering.

Additional idea: use the CROSS structure.  For q=13 (1 mod 4), there are 169
cross blocks of size 25.  A safe set meets each cross in at most 3 points.
The cross constraint gives a_c + b_r - x_cr <= 3.

Let me add the cross constraint as an additional prune: maintain column and row
counts, and check the cross constraint after each placement.

This should be very strong.
"""

from __future__ import annotations

import argparse
import json
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402
from inversive_prime_power import FiniteField, find_irreducible  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=13)
    ap.add_argument("--target", type=int, nargs="+", default=[14])
    ap.add_argument("--node-cap", type=int, default=100_000_000)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    q = args.q
    pts, blocks, through, nc, nl = build_ag(q)
    n = len(pts)
    n_blocks = len(blocks)
    bpts = [tuple(b) for b in blocks]
    print(f"AG(2,{q}): {n} points, {n_blocks} blocks", flush=True)

    # identify cross blocks (size 2q-1)
    crosses = [b for b in blocks if len(b) == 2 * q - 1]
    print(f"  cross blocks (size {2*q-1}): {len(crosses)}", flush=True)

    # For the cross constraint we need the column/row structure.
    # Each cross is a column union a row.  Let me identify columns and rows
    # by finding the partition: two crosses sharing 2q-1 points share a column
    # or a row.
    # Simpler: for each point, which crosses contain it.
    cross_through: list[list[int]] = [[] for _ in range(n)]
    for ci, c in enumerate(crosses):
        for p in c:
            cross_through[p].append(ci)

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

        def rec(start: int, chosen: list, pmask: int, cnt: list, ccnt: list):
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
            # pair budget
            for a in range(len(chosen)):
                for b in range(a + 1, len(chosen)):
                    bl = pair_blocks.get((chosen[a], chosen[b]), [])
                    free = sum(1 for bi in bl if cnt[bi] < 3)
                    if free < need:
                        return
            # block budget
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
                for ci in cross_through[p]:
                    ccnt[ci] += 1
                chosen.append(p)
                rec(p + 1, chosen, pmask | (1 << p), cnt, ccnt)
                chosen.pop()
                for ci in cross_through[p]:
                    ccnt[ci] -= 1
                for bi in through[p]:
                    cnt[bi] -= 1
                if found is not None:
                    return

        cnt = [0] * n_blocks
        ccnt = [0] * len(crosses)
        pmask = 0
        for p in fixed:
            for bi in through[p]:
                cnt[bi] += 1
            for ci in cross_through[p]:
                ccnt[ci] += 1
            pmask |= 1 << p
        try:
            rec(2, list(fixed), pmask, cnt, ccnt)
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
