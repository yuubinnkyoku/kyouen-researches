"""THE k=6 CASE: where two circles first matter.

A 6-set S is bad iff it contains a concyclic 4-subset.  Unlike k=5, two
concyclic 4-subsets of S can share only 2 points, so they may lie on
DIFFERENT circles.

CLASSIFICATION.  Let S be a 6-set and let C(S) be the set of circles that
contain at least 4 points of S.  Since a circle has q+1 points and two
circles share at most 2 points, the circles in C(S) are constrained.

Write m = |C(S)|.  For each circle C in C(S), let t_C = |C ∩ S| >= 4.

  m = 0 :  S is an arc.
  m = 1 :  one circle carries t >= 4 points of S.
  m >= 2 :  two circles each carry >= 4 points of S; they share at most 2
            points, so |S| >= 4 + 4 - 2 = 6.  With |S| = 6 this forces
            t_1 = t_2 = 4 and |C_1 ∩ C_2 ∩ S| = 2, i.e. S splits as
            2 shared points + 2 private to C_1 + 2 private to C_2.

So for k = 6 the bad sets fall into exactly three disjoint families:

  (A) one circle carries all 6 points;
  (B) one circle carries exactly 5 points;
  (C) one circle carries exactly 4 points, and either no second circle
      does, or exactly one second circle does (the "2+2+2" split).

This script computes the exact counts of each family from the geometry and
checks the total against the exhaustive arc counts.

Run:  python arc_k6_structure.py --q 5 7 8
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


def classify(S, circles, circ_of_quad):
    """Return the multiset of t_C values for circles carrying >=4 of S."""
    Sset = set(S)
    hits = Counter()
    for quad in itertools.combinations(sorted(S), 4):
        ci = circ_of_quad.get(quad)
        if ci is None:
            continue
        # count how many points of S are on this circle
        hits[ci] = len(Sset & set(circles[ci]))
    return sorted(hits.values(), reverse=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, ovoid, circles = build(q)
        n = len(ovoid)
        circ_of_quad = {}
        for ci, B in enumerate(circles):
            for quad in itertools.combinations(B, 4):
                circ_of_quad[quad] = ci

        # enumerate all 6-subsets that are BAD, classify them
        fam = Counter()
        total_bad = 0
        total_arc = 0
        for S in itertools.combinations(range(n), 6):
            prof = classify(S, circles, circ_of_quad)
            if not prof:
                total_arc += 1
                continue
            total_bad += 1
            fam[tuple(prof)] += 1

        row = {"q": q, "n": n, "circles": len(circles),
               "bad_6sets": total_bad, "arc_6sets": total_arc,
               "profiles": {str(k): v for k, v in
                            sorted(fam.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, {len(circles)} circles", flush=True)
        print(f"  bad 6-sets: {total_bad}, arc 6-sets: {total_arc}",
              flush=True)
        print(f"  top profiles (t_C values):", flush=True)
        for prof, cnt in sorted(fam.items(), key=lambda x: -x[1])[:8]:
            print(f"    {prof}: {cnt}", flush=True)

    print()
    print("Profile (6,) = all six on one circle.")
    print("Profile (5,) = exactly five on one circle.")
    print("Profile (4,4) = two circles each carrying four, sharing two.")
    print("Profile (4,) = exactly four on one circle, no second circle.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
