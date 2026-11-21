"""k=7: the (4,*) family — corrected multiplicity accounting.

The previous attempt counted only circles containing the FIXED 4-subset T.
But a 7-set S with profile (4,4,4) has three 4-circles, and only some of
them contain T.

CORRECT ACCOUNTING.  Sum over all (C, T, {x,y,z}) where C is a circle, T is
a 4-subset of C, and {x,y,z} are 3 points outside C.  For each such tuple,
let m = number of 4-circles of S = T u {x,y,z}.

Then summing m over all tuples counts each 7-set once per (4-circle,
4-subset of it) pair, i.e. (number of 4-circles) times.

So:
    sum over tuples of m  =  sum over 7-sets of (#4-circles)^2

That is not what we want.  What we want is:

    #7-sets with profile P  =  (1/|P|) * #{(C,T,xyz) : the 4-circles of S
                                              are exactly the entries of P
                                              and C is one of them}

Let me just measure, for each tuple, the FULL profile of S, and then
reconstruct.

Run:  python arc_k7_four2.py --q 5
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

        # for each (C,T,xyz) with |T|=4, record the profile of S
        prof_hist = Counter()
        for ci, B in enumerate(circles):
            Bset = set(B)
            outside = [p for p in range(n) if p not in Bset]
            for T in itertools.combinations(B, 4):
                Tset = set(T)
                for xyz in itertools.combinations(outside, 3):
                    Sset = Tset | set(xyz)
                    hits = {}
                    for quad in itertools.combinations(sorted(Sset), 4):
                        cj = circ_of_quad.get(quad)
                        if cj is None:
                            continue
                        hits[cj] = len(Sset & set(circles[cj]))
                    prof = tuple(sorted(hits.values(), reverse=True))
                    prof_hist[prof] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "profile_histogram": {str(k): v for k, v in
                                     sorted(prof_hist.items(),
                                            key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  profiles over (C,T,xyz) tuples:", flush=True)
        for prof, cnt in sorted(prof_hist.items(), key=lambda x: -x[1]):
            print(f"    {prof}: {cnt}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
