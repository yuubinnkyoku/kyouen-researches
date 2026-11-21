"""THE SPECIAL PAIRS ARE THE TANGENT PAIRS: N_xy closes.

MEASURED:
    q=5: n1=0 -> 70 pairs,  n1=2 -> 120 pairs
    q=7: n1=0 -> 357 pairs, n1=2 -> 504 pairs
    q=8: n1=1 -> 1512 pairs, n1=9=q+1 -> 28 = C(q,2) pairs

At q=8 the extreme class (n1 = q+1, the whole pencil tangent to C) has
exactly C(q,2) = 28 pairs, and the samples (3,4), (5,6), (7,8) are
CONSECUTIVE indices -- these are the pairs {x,y} that lie on a circle
TANGENT to C.

WHY C(q,2)?  A circle tangent to C touches it at one point p.  The tangent
circles at p number q-1 (proved earlier).  Each tangent circle at p has q
points outside C, giving C(q,2) pairs.  But those pairs are counted once
per tangent circle, and a pair {x,y} lies on exactly one circle, so the
number of pairs on SOME tangent circle is

    (number of tangent circles) * C(q,2) / (multiplicity)

Hmm, that overcounts.  Let me think again: the pairs {x,y} whose pencil is
entirely tangent to C.  If {x,y} lies on a tangent circle C' at p, then the
pencil through x,y contains C', and... the whole pencil is tangent only if
every circle through x,y is tangent to C, which is impossible unless the
pencil is the tangent pencil at p.

Actually: the pencil through x,y consists of q+1 circles.  If ALL are
tangent to C, they must all be tangent at the SAME point p (since two
circles tangent to C at different points meet C in 2 distinct points, so
they are not tangent).  So the pencil = the tangent pencil at p, which
means x,y both lie on every tangent circle at p -- impossible unless...

Let me just measure: for the q=8 extreme class, what is the structure?

Let me check whether the extreme pairs are exactly the pairs at "distance 1"
in the ovoid's natural indexing, and derive the count.

Run:  python arc_k6_tangentpairs.py --q 5 7 8
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

from arc_on_quadric import build  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7, 8])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, ovoid, circles = build(q)
        n = len(ovoid)
        b = len(circles)
        circ_through_pair = {}
        for ci, B in enumerate(circles):
            for pair in itertools.combinations(B, 2):
                circ_through_pair.setdefault(pair, []).append(ci)

        ci = 0
        B = circles[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]

        # for each pair, record (n1, n2) and whether the pair lies on a
        # circle tangent to C
        tangent_circles = set()
        for cj, BB in enumerate(circles):
            if cj == ci:
                continue
            if len(Bset & set(BB)) == 1:
                tangent_circles.add(cj)

        stats = Counter()
        for xy in itertools.combinations(outside, 2):
            pencil = circ_through_pair.get(tuple(sorted(xy)), [])
            n1 = n2 = 0
            on_tangent = False
            for cj in pencil:
                if cj == ci:
                    continue
                cap = len(Bset & set(circles[cj]))
                if cap == 1:
                    n1 += 1
                    on_tangent = True
                elif cap == 2:
                    n2 += 1
            stats[(n1, n2, on_tangent)] += 1

        row = {"q": q, "n": n, "b": b,
               "stats": {str(k): v for k, v in sorted(stats.items())},
               "tangent_circles": len(tangent_circles)}
        rows.append(row)
        print(f"q={q}: n={n}, circle size {q+1}, "
              f"{len(tangent_circles)} tangent circles", flush=True)
        for (n1, n2, ot), cnt in sorted(stats.items()):
            print(f"  (n1={n1}, n2={n2}, on_tangent={ot}): {cnt}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
