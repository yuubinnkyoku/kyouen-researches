"""PROVING THE s(q) CONJECTURE: the blocking bound is tight.

CONJECTURE (verified q <= 9):

    s(q) = min{ k : q^2 + 1 - k <= C(k,3)*(q-2) }.

The inequality is NECESSARY (blocking bound, proved).  The conjecture says
it is also SUFFICIENT: whenever the counting allows a maximal set of size
k, one exists.

WHY IT MIGHT BE TRUE.  The blocking bound counts

    (number of triples of S) x (points on a circle outside S)
        = C(k,3) * (q-2)

as an upper bound on the number of blocked points.  It is tight exactly
when the circles determined by triples of S are PAIRWISE DISJOINT outside
S.  Two circles through different triples of S meet in at most 2 points,
and those 2 points are in S (they are the shared points of the triples).
So the circles are automatically disjoint outside S whenever the triples
share at most 2 points -- which is always.

Wait: two triples of S sharing 2 points give two circles meeting in those
2 points, both in S.  Two triples sharing 1 point give circles meeting in
that 1 point (in S) plus at most 1 more point, which could be outside S.
Two triples sharing 0 points give circles meeting in at most 2 points,
which could be outside S.

So the bound is tight iff no two circles from disjoint-or-1-sharing
triples meet outside S.  That is a strong "general position" condition.

CONSTRUCTION.  The witnesses found are consecutive points [0,1,2,3,4,5]
in the index order, which is an artefact of the search order, not a
geometric statement.  Let me look at what the witnesses actually are
geometrically, and whether a clean family exists.

Run:  python min_maximal_construct.py
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
    return points, n, blocks, tri_circle


def is_maximal(chosen, n, blocks, tri_circle):
    S = set(chosen)
    blocked = set()
    for tri in itertools.combinations(chosen, 3):
        ci = tri_circle.get(tuple(sorted(tri)))
        if ci is None:
            continue
        for p in blocks[ci]:
            if p not in S:
                blocked.add(p)
    return len(blocked) == n - len(S), len(blocked)


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
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7, 9])
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'n':>4} {'k*':>3} {'witness':>30} {'blocked':>9} "
          f"{'needed':>7} {'tight?':>7}")
    for q in args.q:
        points, n, blocks, tri_circle = build(q)
        kstar = blocking_min_k(q)
        # find a maximal set of size k* by DFS
        chosen: list[int] = []
        inS = [False] * n
        block = [0] * n
        nblocked = [0]
        found = []

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
            if found:
                return True
            k = len(chosen)
            if k == kstar and nblocked[0] == n - k:
                found.append(list(chosen))
                return True
            if k >= kstar:
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
        if not found:
            print(f"{q:>3} {n:>4} {kstar:>3}  NOT FOUND", flush=True)
            continue
        w = found[0]
        ok, nb = is_maximal(w, n, blocks, tri_circle)
        needed = n - len(w)
        cap = comb(len(w), 3) * (q - 2)
        row = {"q": q, "n": n, "k_star": kstar, "witness": w,
               "blocked": nb, "needed": needed, "maximal": ok,
               "capacity": cap, "tight": nb == cap}
        rows.append(row)
        print(f"{q:>3} {n:>4} {kstar:>3} {str(w):>30} {nb:>9} {needed:>7} "
              f"{str(nb == cap):>7}", flush=True)

    print()
    print("'tight' means the number of blocked points equals the capacity")
    print("C(k,3)*(q-2), i.e. the blocking bound is achieved with no waste.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
