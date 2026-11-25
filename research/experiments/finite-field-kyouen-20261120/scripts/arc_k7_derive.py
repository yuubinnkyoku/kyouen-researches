"""k=7: the profile structure via the circle-count m.

For k=6 the profiles were indexed by the multiset of t_C values (how many
points of S each circle carries).  For k=7 the same indexing works but
there are more profiles.

KEY REDUCTION.  A k-set S is bad iff some circle carries >= 4 of its
points.  Let m = number of circles carrying >= 4 points of S.  Two circles
share at most 2 points, so

    |S| >= 4m - 2*C(m,2)   ... (*)

For k=7:  m=1 -> 4, m=2 -> 6, m=3 -> 6, m=4 -> 4, m=5 -> -2.

So (*) does not bound m for k=7.  But there is a better bound: the circles
carrying >= 4 points of S must be "compatible" with |S| = 7.

Let me instead classify by the PROFILE (sorted t_C values) and find the
closed form for each profile count, as was done for k=6.

MEASURED (q=5, C(26,7)=657800, arcs=0):

    (4,4,4,4)      312000
    (4,4,4)         96200
    (5,4,4)         85800
    (4,4,4,4,4)     78000
    (5,4)           62400
    (4,4)           15600
    (4,4,4,4,4,4)    5200
    (6,)             2600

This script derives each count from the "choose the circles, then the
points" decomposition and checks.

Run:  python arc_k7_derive.py --q 5
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
    ap.add_argument("--q", type=int, nargs="+", default=[5])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, ovoid, circles = build(q)
        n = len(ovoid)
        b = len(circles)
        s = q + 1
        circ_of_quad = {}
        for ci, B in enumerate(circles):
            for quad in itertools.combinations(B, 4):
                circ_of_quad[quad] = ci

        fam = Counter()
        for S in itertools.combinations(range(n), 7):
            Sset = set(S)
            hits = {}
            for quad in itertools.combinations(S, 4):
                ci = circ_of_quad.get(quad)
                if ci is None:
                    continue
                hits[ci] = len(Sset & set(circles[ci]))
            if not hits:
                continue
            fam[tuple(sorted(hits.values(), reverse=True))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "profiles": {str(k): v for k, v in
                            sorted(fam.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  {'profile':>20} {'count':>10} {'m':>3} {'sum t':>6}",
              flush=True)
        for prof, cnt in sorted(fam.items(), key=lambda x: -x[1]):
            print(f"  {str(prof):>20} {cnt:>10} {len(prof):>3} "
                  f"{sum(prof):>6}", flush=True)

        # try: count = b * C(s, t1) * (ways to place the rest)
        print()
        print("  candidate decompositions:", flush=True)
        for prof, cnt in sorted(fam.items(), key=lambda x: -x[1]):
            t1 = prof[0]
            naive = b * comb(s, t1) * comb(n - s, 7 - t1)
            print(f"  {str(prof):>20}: count {cnt}, "
                  f"b*C(s,{t1})*C(n-s,{7-t1}) = {naive}, "
                  f"ratio {cnt/naive if naive else 0:.4f}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
