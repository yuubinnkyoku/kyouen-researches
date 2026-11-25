"""CHEAP RANDOMISED SEARCH FOR SMALL MAXIMAL SETS.

The blocking inequality proves s(q) >= k*.  To get s(q) = k* we only need
to FIND one maximal safe set of size k*.

The expensive part of the previous attempt was the greedy "gain" score,
which is O(n * deg) per step.  Here we use a much cheaper scheme:

    build a RANDOM safe set of size k* (uniform random order),
    then check maximality.

For small k* (5, 6, 7) the probability of hitting a maximal set is not
tiny, and each trial costs only O(k*^2 * q).  So many restarts are cheap.

Run:  python min_maximal_random3.py --q 5 7 9 11 13 16 17
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


def one_trial(n, blocks, tri_circle, circles_of, target, rng):
    """Random safe set of size `target`; return (set, #unblocked)."""
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
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7, 9, 11, 13])
    ap.add_argument("--trials", type=int, default=20000)
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
        t = 0
        for t in range(args.trials):
            res = one_trial(n, blocks, tri_circle, circles_of, kstar, rng)
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
               "trials_used": t + 1, "seconds": round(dt, 2)}
        rows.append(row)
        print(f"q={q:>3} n={n:>4} k*={kstar}: "
              + (f"FOUND {found}" if found
                 else f"not found (best unblocked={best[1] if best else '-'})")
              + f"  [{t+1} trials, {dt:.1f}s]", flush=True)

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
