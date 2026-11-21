"""s(q) FOR LARGE q, USING THE FAST OVOID CONSTRUCTION.

The elliptic-quadric model builds the inversive plane of order q in
O(q^3) instead of O(q^5), so q = 13, 16, 17, 19 are now reachable.

The blocking inequality proves s(q) >= k* where

    k* = min{ k : q^2 + 1 - k <= C(k,3)*(q-2) }.

To get s(q) = k* we only need to FIND one maximal safe set of size k*.
Random restarts suffice (they found k*-maximal sets in a handful of tries
for q <= 11).

Run:  python s_q_large.py --q 9 11 13 16 17 19
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
import time
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_ovoid import build_ovoid, planes_of_pg3  # noqa: E402


def kstar(q: int) -> int:
    k = 3
    while k <= q + 3:
        if q * q + 1 - k <= comb(k, 3) * (q - 2):
            return k
        k += 1
    return -1


def build(q: int):
    """Return (n, blocks, tri_circle, circles_of) via the ovoid model."""
    F, params, ovoid = build_ovoid(q)
    _, planes = planes_of_pg3(q)
    idx = {v: i for i, v in enumerate(ovoid)}
    blocks = []
    for c in planes:
        sec = []
        for v in ovoid:
            s = F.zero
            for ci, vi in zip(c, v):
                s = F.add(s, F.mul(ci, vi))
            if F.is_zero(s):
                sec.append(idx[v])
        if len(sec) == q + 1:
            blocks.append(tuple(sorted(sec)))
    blocks = sorted(set(blocks))
    n = len(ovoid)
    tri_circle = {}
    for ci, B in enumerate(blocks):
        for tri in itertools.combinations(B, 3):
            tri_circle[tri] = ci
    circles_of = [[] for _ in range(n)]
    for ci, B in enumerate(blocks):
        for p in B:
            circles_of[p].append(ci)
    return n, blocks, tri_circle, circles_of


def one_trial(n, blocks, tri_circle, circles_of, target, rng):
    order = list(range(n))
    rng.shuffle(order)
    chosen: list[int] = []
    inS = [False] * n
    block = [0] * n
    cnt = [0] * len(blocks)
    for v in order:
        if len(chosen) == target:
            break
        if block[v] > 0:
            continue
        inS[v] = True
        chosen.append(v)
        for ci in circles_of[v]:
            cnt[ci] += 1
            if cnt[ci] == 3:
                for p in blocks[ci]:
                    if not inS[p]:
                        block[p] += 1
    if len(chosen) < target:
        return None
    unblocked = sum(1 for p in range(n) if not inS[p] and block[p] == 0)
    return chosen, unblocked


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[9, 11, 13])
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=20261122)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        t0 = time.time()
        n, blocks, tri_circle, circles_of = build(q)
        tb = time.time() - t0
        ks = kstar(q)
        rng = random.Random(args.seed + q)
        best = None
        found = None
        t = 0
        for t in range(args.trials):
            res = one_trial(n, blocks, tri_circle, circles_of, ks, rng)
            if res is None:
                continue
            w, nun = res
            if best is None or nun < best[1]:
                best = (w, nun)
            if nun == 0:
                found = w
                break
        dt = time.time() - t0
        row = {"q": q, "n": n, "circles": len(blocks), "k_star": ks,
               "found": found is not None, "witness": found,
               "best_unblocked": best[1] if best else None,
               "trials": t + 1, "build_seconds": round(tb, 2),
               "total_seconds": round(dt, 2)}
        rows.append(row)
        print(f"q={q:>3} n={n:>4} k*={ks}: "
              + (f"FOUND {found}" if found
                 else f"not found (best unblocked={best[1] if best else '-'})")
              + f"  [{t+1} trials, build {tb:.1f}s, total {dt:.1f}s]",
              flush=True)

    print()
    print("Blocking inequality => s(q) >= k*.  A maximal set of size k* =>")
    print("s(q) <= k*.  Together: s(q) = k*.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
