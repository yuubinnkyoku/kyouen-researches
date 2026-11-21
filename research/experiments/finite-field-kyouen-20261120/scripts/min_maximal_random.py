"""FINDING SMALL MAXIMAL SETS BY RANDOMISED SEARCH (for larger q).

The exhaustive DFS in min_maximal_q9.py is too slow for q >= 11 because it
must prove non-existence at every smaller size.  But we only need to FIND
one maximal set of size k* -- existence is enough to confirm s(q) <= k*,
and the blocking inequality already proves s(q) >= k*.

STRATEGY.  Randomised greedy with restarts:

    1. pick a random safe set of size k* (greedy, random order);
    2. if it is maximal, done;
    3. otherwise, try to "repair": swap points to block the unblocked ones.

A cheaper and very effective variant: build the set greedily but PREFER
points that block many currently-unblocked points.  That directly targets
maximality.

Run:  python min_maximal_random.py --q 11 13 16
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
    return n, blocks, tri_circle


def blocking_min_k(q: int) -> int:
    k = 3
    while k <= q + 3:
        if q * q + 1 - k <= comb(k, 3) * (q - 2):
            return k
        k += 1
    return -1


def try_build(n, blocks, tri_circle, target, rng, greedy=True):
    """Build a safe set of size `target`, preferring points that block more."""
    chosen: list[int] = []
    inS = [False] * n
    block = [0] * n

    def add(v):
        undo = []
        inS[v] = True
        chosen.append(v)
        for pair in itertools.combinations(chosen[:-1], 2):
            ci = tri_circle.get(tuple(sorted((pair[0], pair[1], v))))
            if ci is None:
                continue
            for p in blocks[ci]:
                if inS[p]:
                    continue
                block[p] += 1
                undo.append(p)
        return undo

    def remove(v, undo):
        for p in undo:
            block[p] -= 1
        chosen.pop()
        inS[v] = False

    while len(chosen) < target:
        cands = [v for v in range(n) if not inS[v] and block[v] == 0]
        if not cands:
            return None
        if greedy:
            # prefer points that block many currently-unblocked points
            scored = []
            for v in cands:
                gain = 0
                for pair in itertools.combinations(chosen, 2):
                    ci = tri_circle.get(tuple(sorted((pair[0], pair[1], v))))
                    if ci is None:
                        continue
                    for p in blocks[ci]:
                        if not inS[p] and block[p] == 0 and p != v:
                            gain += 1
                scored.append((gain, rng.random(), v))
            scored.sort(reverse=True)
            v = scored[0][2]
        else:
            v = rng.choice(cands)
        add(v)

    # maximal?
    unblocked = [p for p in range(n) if not inS[p] and block[p] == 0]
    return (list(chosen), len(unblocked)) if not unblocked else (list(chosen),
                                                                 len(unblocked))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[11, 13])
    ap.add_argument("--restarts", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20261121)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        n, blocks, tri_circle = build(q)
        kstar = blocking_min_k(q)
        rng = random.Random(args.seed + q)
        t0 = time.time()
        best = None
        found = None
        for r in range(args.restarts):
            res = try_build(n, blocks, tri_circle, kstar, rng, greedy=True)
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
               "found_maximal": found is not None,
               "witness": found,
               "best_unblocked": best[1] if best else None,
               "restarts_used": r + 1, "seconds": round(dt, 2)}
        rows.append(row)
        print(f"q={q:>3} n={n:>4} k*={kstar}: "
              + (f"FOUND maximal {found}" if found
                 else f"not found (best unblocked={best[1] if best else '-'})")
              + f"  [{r+1} restarts, {dt:.1f}s]", flush=True)

    print()
    print("The blocking inequality proves s(q) >= k*.")
    print("Finding a maximal set of size k* proves s(q) <= k*, hence s(q) = k*.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
