"""k=7: the sum_j distribution in Case A.

MEASURED (q=5, Case A, 840 triples):
    sum_j = 1: 64,  2: 196,  3: 432,  4: 140,  5: 8

MEASURED (q=5, Case B, 300 triples):
    sum_j = 2: 128, 3: 64,  4: 100,  5: 8

Case A: the three pencils are disjoint.  So sum_j = u = the total number of
pencil circles meeting T in 2 points, over the three pairs.

For a single pair {x,y}, j is the number of iota-pairs inside T, where iota
is the involution of the pencil.  From k=6, the distribution of j over
pairs is governed by N_xy(n2) and H(n2,n1,j,4).

In Case A the three pencils are disjoint, so the three j's are "independent
given the pencils".  But the pencils are not independent (they share
points).

Let me look at the structure differently: count, for each triple, the
number of circles through pairs of {x,y,z} that meet T in 2 points.  That
is sum_j.  Each such circle is a circle through 2 of {x,y,z} meeting T in
2 points.

Equivalently: count pairs (pair of {x,y,z}, circle through that pair
meeting T in 2 points).

Let me measure this by the "type" of the circle: how many of {x,y,z} it
contains (2 or 3) and how many of T.

Run:  python arc_k7_sumj.py --q 5
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
        circ_through_pair = {}
        for ci, B in enumerate(circles):
            for pair in itertools.combinations(B, 2):
                circ_through_pair.setdefault(pair, []).append(ci)

        ci = 0
        B = circles[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]
        T = tuple(B[:4])
        Tset = set(T)

        # for each triple, list the circles through pairs meeting T in 2
        # points, and classify by |circle cap {x,y,z}| and |circle cap T|
        joint = Counter()
        for xyz in itertools.combinations(outside, 3):
            xyzset = set(xyz)
            found = {}
            for xy in itertools.combinations(xyz, 2):
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    capT = len(Tset & set(circles[cj]))
                    if capT == 2:
                        capX = len(xyzset & set(circles[cj]))
                        found[cj] = (capX, capT)
            # classify the multiset of (capX, capT)
            prof = tuple(sorted(found.values()))
            joint[prof] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  profile of (|C' cap xyz|, |C' cap T|) over the pencils:",
              flush=True)
        for prof, cnt in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    {prof}: {cnt}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
