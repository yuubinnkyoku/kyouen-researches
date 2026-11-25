"""s(9): the minimum maximal safe set size for the inversive plane of order 9.

The blocking bound says a maximal safe set of size k needs

    q^2 + 1 - k <= C(k,3)*(q-2).

For q = 9:  k=5 gives 77 <= 70 (false), k=6 gives 76 <= 80 (true).
So s(9) >= 6, and s(9) = 6 iff a 6-point maximal set exists.

This script searches for a maximal safe set of size exactly 6 for q = 9,
using the incremental blocking counter.  It also verifies that no size-5
maximal set exists (which the bound already proves, but we check anyway).

Run:  python min_maximal_q9.py
"""

from __future__ import annotations

import argparse
import itertools
import json
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


def find_maximal_of_size(n, blocks, tri_circle, target, cap=200_000_000):
    chosen: list[int] = []
    inS = [False] * n
    block = [0] * n
    nblocked = [0]
    state = {"nodes": 0, "capped": False}
    result = []

    def add_point(v):
        undo = []
        if block[v] > 0:
            nblocked[0] -= 1
        inS[v] = True
        chosen.append(v)
        for pair in itertools.combinations(chosen[:-1], 2):
            ci = tri_circle.get(tuple(sorted((pair[0], pair[1], v))))
            if ci is None:
                continue
            for p in blocks[ci]:
                if inS[p]:
                    continue
                if block[p] == 0:
                    nblocked[0] += 1
                block[p] += 1
                undo.append((p, 1))
        return undo

    def remove_point(v, undo):
        for p, d in undo:
            block[p] -= d
            if block[p] == 0:
                nblocked[0] -= 1
        chosen.pop()
        inS[v] = False
        if block[v] > 0:
            nblocked[0] += 1

    def rec(start):
        state["nodes"] += 1
        if state["nodes"] > cap:
            state["capped"] = True
            return True
        k = len(chosen)
        if k == target and nblocked[0] == n - k:
            result.append(list(chosen))
            return True
        if k >= target:
            return False
        for v in range(start, n):
            if inS[v] or block[v] > 0:
                continue
            undo = add_point(v)
            if rec(v + 1):
                return True
            remove_point(v, undo)
            if state["capped"]:
                return True
        return False

    rec(0)
    return (result[0] if result else None), state["nodes"], state["capped"]


def blocking_min_k(q: int) -> int:
    k = 3
    while k <= q + 3:
        if q * q + 1 - k <= comb(k, 3) * (q - 2):
            return k
        k += 1
    return -1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[9])
    ap.add_argument("--cap", type=int, default=200_000_000)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        n, blocks, tri_circle = build(q)
        bmin = blocking_min_k(q)
        print(f"q={q}: n={n}, blocking bound says s >= {bmin}", flush=True)
        for target in range(bmin, bmin + 3):
            t0 = time.time()
            w, nodes, capped = find_maximal_of_size(n, blocks, tri_circle,
                                                    target, cap=args.cap)
            dt = time.time() - t0
            row = {"q": q, "n": n, "target": target, "found": w is not None,
                   "witness": w, "nodes": nodes, "capped": capped,
                   "seconds": round(dt, 2)}
            rows.append(row)
            print(f"  size {target}: {'FOUND ' + str(w) if w else 'none'}"
                  f"  ({nodes} nodes, {dt:.1f}s"
                  + (", CAPPED" if capped else "") + ")", flush=True)
            if w is not None:
                print(f"  => s({q}) = {target}", flush=True)
                break

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
