"""FAMILY C AND D: THE STRUCTURE IN THE NORMALISED PICTURE.

We have S = {0, 1, infinity} u T with T in F_{q^2} \\ F_q, and the exact
dictionary for the F_q part:

    a in F_q  <-->  alpha = alpha(1/a) in Z_{q+1},  a bijection,
    cell (a,b) with symbol c  <-->  gamma = alpha - beta  (mod q+1).

So the 3-net IS the cyclic group Z_{q+1}.

Now: what are families C and D?

FAMILY C.  {a, z, z', z''} concyclic, a in {0,1,inf}, z,z',z'' in T.
    Equivalently: z, z', z'' lie on a circle through a.

FAMILY D.  {z, z', z'', z'''} concyclic, all in T.

THE GEOMETRIC PICTURE.  Circles of the inversive plane are the images of
P^1(F_q) under PGL(2, F_{q^2}).  A circle through the three anchors
0, 1, infinity is exactly P^1(F_q), which meets T in nothing.  So:

    - a circle through 0 and 1 is a "P_0/P_1 line" (family B),
    - a circle through 0 and infinity is a "P_0/P_inf line" (family B),
    - a circle through 1 and infinity is a "P_1/P_inf line" (family B),
    - a circle through exactly ONE anchor is family C,
    - a circle through NO anchor is family D.

So families C and D are the circles that meet {0,1,inf} in 1 or 0 points.

COUNTING.  Circles through 0: q(q+1) total (the pencil).  Of these, q+1
pass through 1 (the pencil through 0 and 1), and q+1 through infinity.
The circle through 0,1,infinity is P^1(F_q) itself, counted in both.
So circles through 0 and exactly one of {1,inf}: q(q+1) - 2(q+1) + 1.

This script computes, for each q, the exact counts of circles by how many
anchors they contain, and the number of T-points on each.  That is the
quantitative shape of families C and D.

Run:  python net3_family_cd_counts.py
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field, build_inversive_plane  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7])
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'circles':>8} {'anchors in circle':>20} "
          f"{'T-points per circle':>22}")
    for q in args.q:
        F, sub = build_field(q)
        points, circles = build_inversive_plane(q)
        subset = set(sub)

        # the three anchors in the point set
        anchors = [F.zero, F.one, None]
        aset = set(anchors)
        missing = [a for a in anchors if a not in set(points)]
        if missing:
            print(f"q={q}: anchors {missing} not in point set; skipping",
                  flush=True)
            continue

        by_anchor_count = Counter()
        tcounts = Counter()
        for c in circles:
            k = len(aset & set(c))
            by_anchor_count[k] += 1
            t = sum(1 for z in c if z not in subset and z is not None)
            tcounts[(k, t)] += 1

        row = {"q": q, "circles": len(circles),
               "by_anchor_count": {str(k): v for k, v in
                                   sorted(by_anchor_count.items())},
               "by_anchor_and_T": {f"{k},{t}": v for (k, t), v in
                                   sorted(tcounts.items())}}
        rows.append(row)
        print(f"{q:>3} {len(circles):>8} "
              f"{str(dict(sorted(by_anchor_count.items()))):>20} "
              f"{str(dict(sorted(tcounts.items()))):>22}", flush=True)

    print()
    print("Circles with 3 anchors = P^1(F_q) itself (contains no T-point).")
    print("Circles with 2 anchors = the 3-net lines (family B).")
    print("Circles with 1 anchor = family C.")
    print("Circles with 0 anchors = family D.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
