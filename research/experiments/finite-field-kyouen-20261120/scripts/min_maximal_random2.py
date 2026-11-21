"""FAST RANDOMISED SEARCH FOR SMALL MAXIMAL SETS.

The blocking inequality proves s(q) >= k*, where

    k* = min{ k : q^2 + 1 - k <= C(k,3)*(q-2) }.

To prove s(q) = k* it suffices to FIND one maximal safe set of size k*.

SPEEDUP.  Precompute, for every point v, the list of circles through v.
Then "adding v blocks p" is checked via circle membership, and the greedy
score (how many currently-unblocked points would v block) is computed by
iterating over the circles through v only -- O(deg) instead of O(k^2 * q).

Run:  python min_maximal_random2.py --q 5 7 9 11 13
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

from inversive_all_q import build_inversive_plane  # noqa: E402


def build(q: int):
    points, circles = build_inversive_plane(q)
    idx = {p: i for i, p in enumerate(points)}
    blocks = [tuple(sorted(idx[p] for p in c)) for c in circles]
    n = len(points)
    tri_circle = {}
    for ci, B in enumerate(blocks):
        for tri in itertools.combinations(B, 3):
            tri_circle[tri] = ci
    circles_of = [[] for _ in range(n)]
    for ci, B in enumerate(blocks):
        for p in B:
            circles_of[p].append(ci)
    return n, blocks, tri_circle, circles_of


def blocking_min_k(q: int) -> int:
    k = 3
    while k <= q + 3:
        if q * q + 1 - k <= comb(k, 3) * (q - 2):
            return k
        k += 1
    return -1


def try_build(n, blocks, tri_circle, circles_of, target, rng):
    """Greedy build of a safe set of size `target`, preferring blockers."""
    chosen: list[int] = []
    inS = [False] * n
    block = [0] * n
    # count of S-points on each circle
    cnt = [0] * len(blocks)

    def add(v):
        inS[v] = True
        chosen.append(v)
        # circles through v that now carry 3 points of S block their points
        for ci in circles_of[v]:
            cnt[ci] += 1
            if cnt[ci] == 3:
                for p in blocks[ci]:
                    if not inS[p]:
                        block[p] += 1

    while len(chosen) < target:
        cands = [v for v in range(n) if not inS[v] and block[v] == 0]
        if not cands:
            return None
        scored = []
        for v in cands:
            gain = 0
            for ci in circles_of[v]:
                if cnt[ci] == 2:
                    for p in blocks[ci]:
                        if not inS[p] and block[p] == 0 and p != v:
                            gain += 1
            scored.append((gain, rng.random(), v))
        scored.sort(reverse=True)
        add(scored[0][2])

    unblocked = sum(1 for p in range(n) if not inS[p] and block[p] == 0)
    return list(chosen), unblocked


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7, 9, 11, 13])
    ap.add_argument("--restarts", type=int, default=300)
    ap.add_argument("--seed", type=int, default=20261121)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        n, blocks, tri_circle, circles_of = build(q)
        kstar = blocking_min_k(q)
        rng = random.Random(args.seed + q)
        t0 = time.time()
        best = None
        found = None
        r = 0
        for r in range(args.restarts):
            res = try_build(n, blocks, tri_circle, circles_of, kstar, rng)
            if res is None:
                continue
            w, nun = res
            if best is None or nun < best[1]:
                best = (w, nun)
            if nun == 0:
                found = w
                break
        dt = time.time() - t0
        row = {"q": q, "n": n, "k_star": kstar,
               "found_maximal": found is not None, "witness": found,
               "best_unblocked": best[1] if best else None,
               "restarts_used": r + 1, "seconds": round(dt, 2)}
        rows.append(row)
        print(f"q={q:>3} n={n:>4} k*={kstar}: "
              + (f"FOUND {found}" if found
                 else f"not found (best unblocked={best[1] if best else '-'})")
              + f"  [{r+1} restarts, {dt:.1f}s]", flush=True)

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
