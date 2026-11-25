"""WHY IS s(q) = k*?  THE DEFECT VIEWPOINT.

For a maximal safe set S of size k, define the DEFECT

    delta(S) = C(k,3)*(q-2) - (q^2 + 1 - k).

The blocking inequality says delta(S) >= 0.  Equality (delta = 0) means
every outside point is covered exactly once.

COMPUTED DEFECTS (from the witnesses):

    q=3, k=5:  capacity 10, needed  5, delta =  5
    q=4, k=5:  capacity 20, needed 12, delta =  8
    q=5, k=5:  capacity 30, needed 21, delta =  9
    q=8, k=5:  capacity 60, needed 60, delta =  0   <-- EQUALITY

So q=8 is the unique tight case for k=5, exactly as the algebra says.

THE KEY QUESTION.  Why does a maximal set of size k* always EXIST?
The blocking inequality only gives the lower bound s(q) >= k*.

IDEA: CONSTRUCTIVE LOWER BOUND VIA A "PENCIL" FAMILY.

Take k points on a single circle?  No -- a circle has q+1 points and any 4
of them are concyclic, so at most 3 points may lie on one circle.

Take k points such that the C(k,3) circles through triples are as
"spread out" as possible.  The blocking inequality is exactly the
statement that this spreading can cover everything when k = k*.

A CLEANER ANGLE: the problem is a COVERING DESIGN question.

    We need a k-set S whose triple-circles cover all of F_{q^2}+1 minus S.

Equivalently, in the dual: we need a set of C(k,3) circles, arising from a
k-point set, that covers q^2+1-k points.

This script measures, for the actual witnesses, how the coverage is
distributed, and checks whether a simple greedy construction reproduces
k* for all q.  If it does, that is a constructive proof of s(q) <= k*.

Run:  python s_q_constructive.py --q 3 4 5 7 9 11
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_inversive_plane  # noqa: E402


def kstar(q: int) -> int:
    k = 3
    while k <= q + 3:
        if q * q + 1 - k <= comb(k, 3) * (q - 2):
            return k
        k += 1
    return -1


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


def greedy_construct(n, blocks, tri_circle, circles_of, target):
    """Deterministic greedy: repeatedly add the point that blocks most."""
    chosen: list[int] = []
    inS = [False] * n
    block = [0] * n
    cnt = [0] * len(blocks)

    def add(v):
        inS[v] = True
        chosen.append(v)
        for ci in circles_of[v]:
            cnt[ci] += 1
            if cnt[ci] == 3:
                for p in blocks[ci]:
                    if not inS[p]:
                        block[p] += 1

    while len(chosen) < target:
        best_v, best_gain = None, -1
        for v in range(n):
            if inS[v] or block[v] > 0:
                continue
            gain = 0
            for ci in circles_of[v]:
                if cnt[ci] == 2:
                    for p in blocks[ci]:
                        if not inS[p] and block[p] == 0 and p != v:
                            gain += 1
            if gain > best_gain:
                best_gain, best_v = gain, v
        if best_v is None:
            return None
        add(best_v)

    unblocked = sum(1 for p in range(n) if not inS[p] and block[p] == 0)
    return list(chosen), unblocked


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7, 9])
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'n':>4} {'k*':>3} {'greedy maximal?':>16} "
          f"{'unblocked':>10} {'defect':>7}")
    for q in args.q:
        n, blocks, tri_circle, circles_of = build(q)
        ks = kstar(q)
        res = greedy_construct(n, blocks, tri_circle, circles_of, ks)
        if res is None:
            print(f"{q:>3} {n:>4} {ks:>3}  greedy stuck", flush=True)
            continue
        w, nun = res
        defect = comb(ks, 3) * (q - 2) - (n - ks)
        row = {"q": q, "n": n, "k_star": ks, "witness": w,
               "unblocked": nun, "maximal": nun == 0, "defect": defect}
        rows.append(row)
        print(f"{q:>3} {n:>4} {ks:>3} {str(nun == 0):>16} {nun:>10} "
              f"{defect:>7}", flush=True)

    print()
    print("If the deterministic greedy always succeeds, that is a")
    print("constructive proof of s(q) <= k* for the tested q.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
