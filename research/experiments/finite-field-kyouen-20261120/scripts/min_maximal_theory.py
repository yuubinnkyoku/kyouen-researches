"""WHY IS s(q) = 5 FOR ALL q?  A CONSTRUCTION.

Numerical finding (min_maximal2.py):

    q = 3:  s = 5, K = 5,  maximal sets: {5: 72}
    q = 4:  s = 5, K = 5,  maximal sets: {5: 2040}
    q = 5:  s = 5, K = 6,  maximal sets: {5: 10400, 6: 5200}
    q = 7:  s = 5, K = 6,  maximal sets: {5: 11760, 6: 1254400}

So the MINIMUM maximal safe set has size 5 for every q tested, while K
grows.  That is a new invariant, and it is surprising: it says a player can
always force the game to end after only 5 stones, no matter how large q is.

WHY 5?  A maximal safe set S of size k needs every outside point blocked:

    q^2 + 1 - k  <=  C(k,3) * (q - 2).

For k = 5:  C(5,3) = 10, so we need q^2 + 1 - 5 <= 10(q-2), i.e.
q^2 - 10q + 16 <= 0, i.e. (q-2)(q-8) <= 0, i.e. 2 <= q <= 8.

So the blocking bound says k = 5 can only be maximal for q <= 8!
For q >= 9 a maximal set of size 5 is IMPOSSIBLE by the blocking bound.

That predicts s(q) > 5 for q >= 9.  This script tests that prediction and
also constructs the 5-point maximal sets explicitly to see their shape.

Run:  python min_maximal_theory.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
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


def find_maximal_of_size(n, blocks, tri_circle, target, cap=50_000_000):
    """Find one maximal safe set of exactly `target` points."""
    chosen: list[int] = []
    inS = [False] * n
    block = [0] * n
    nblocked = [0]
    state = {"nodes": 0}
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
        return False

    rec(0)
    return (result[0] if result else None), state["nodes"]


def blocking_bound_min_k(q: int) -> int:
    """Smallest k with q^2+1-k <= C(k,3)*(q-2)."""
    k = 3
    while k <= q + 3:
        if q * q + 1 - k <= comb(k, 3) * (q - 2):
            return k
        k += 1
    return -1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7])
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'n':>4} {'blocking min k':>15} {'5-maximal exists?':>18} "
          f"{'witness':>26}")
    for q in args.q:
        n, blocks, tri_circle = build(q)
        bmin = blocking_bound_min_k(q)
        w, nodes = find_maximal_of_size(n, blocks, tri_circle, 5)
        row = {"q": q, "n": n, "blocking_min_k": bmin,
               "five_maximal_exists": w is not None,
               "witness": w, "nodes": nodes}
        rows.append(row)
        print(f"{q:>3} {n:>4} {bmin:>15} {str(w is not None):>18} "
              f"{str(w):>26}", flush=True)

    print()
    print("BLOCKING BOUND: a maximal safe set of size k needs")
    print("    q^2 + 1 - k <= C(k,3)*(q-2).")
    print("For k = 5 this reads (q-2)(q-8) <= 0, i.e. q <= 8.")
    print("So s(q) = 5 is possible only for q <= 8; for q >= 9 the minimum")
    print("maximal size must grow.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
