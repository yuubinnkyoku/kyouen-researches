"""DERIVING THE k=6 PROFILE COUNTS.

Observed profiles for q=5 (n=26, b=130, circle size 6):

    (6,)      :    130
    (5,)      :  15600
    (4,)      :  62400
    (4,4)     : 132600
    (4,4,4)   :  14300
    ---------------------
    total bad : 225030
    arc 6-sets:   5200   (C(26,6) = 230230)

The simple formulas work for (6,) and (5,):

    (6,) = b * C(q+1, 6)
    (5,) = b * C(q+1, 5) * (n - q - 1)

For (4,) the naive count b*C(q+1,4)*(n-q-1) = 39000 is too small; the
observed 62400 is larger.  The reason: a 6-set with exactly one circle
carrying 4 points can have its remaining 2 points arranged so that NO
second circle carries 4 -- but the naive count picks the 4 circle points
and 2 arbitrary outside points, and some of those choices produce a
SECOND circle with 4 points, which should be counted under (4,4) instead.

So the naive count OVERCOUNTS (4,) and UNDERCOUNTS nothing... but we
observe (4,) LARGER than naive.  That means the naive count is not even
the right starting point: a 6-set with profile (4,) can have its 4 circle
points chosen in more than one way?  No -- the circle is unique.

Let me just compute the exact counts by direct enumeration and fit.

Run:  python arc_k6_derive.py --q 5 7
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
        circ_of_quad = {}
        for ci, B in enumerate(circles):
            for quad in itertools.combinations(B, 4):
                circ_of_quad[quad] = ci

        fam = Counter()
        for S in itertools.combinations(range(n), 6):
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

        print(f"q={q}: n={n}, b={b}, circle size {q+1}", flush=True)
        print(f"  C(n,6) = {comb(n,6)}", flush=True)
        tot_bad = sum(fam.values())
        print(f"  bad = {tot_bad}, arcs = {comb(n,6)-tot_bad}", flush=True)
        print(f"  {'profile':>12} {'count':>10} {'naive':>12} {'ratio':>8}",
              flush=True)
        for prof, cnt in sorted(fam.items(), key=lambda x: -x[1]):
            # naive: pick the largest circle, then fill
            t = prof[0]
            naive = b * comb(q + 1, t) * comb(n - q - 1, 6 - t)
            print(f"  {str(prof):>12} {cnt:>10} {naive:>12} "
                  f"{cnt/naive if naive else 0:>8.4f}", flush=True)
        rows.append({"q": q, "n": n, "b": b,
                     "profiles": {str(k): v for k, v in fam.items()},
                     "bad": tot_bad, "arcs": comb(n, 6) - tot_bad})

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
