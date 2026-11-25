"""k=7: the (4,*) tuple counts via the 3-point structure.

For k=7 the (4,*) tuples are (C, T, {x,y,z}) with |T| = 4.  The profile of
S = T u {x,y,z} depends on how many circles carry >= 4 of S.

A second circle C' carries >= 4 of S iff it carries 2 of T and both of some
pair from {x,y,z}, OR 1 of T and all three of {x,y,z} (impossible: C' meets
C in <= 2 points so carries <= 2 of T), OR 0 of T and all three (also
impossible for the same reason).

So C' must carry exactly 2 of T and exactly 2 of {x,y,z}.

Therefore the profile is determined by the GRAPH on {x,y,z}: for each pair
of {x,y,z}, count the circles through that pair meeting T in exactly 2
points.  That is exactly the pencil quantity j({x,y}) from k=6!

So for each of the 3 pairs {x,y}, {x,z}, {y,z} we get j-values j1, j2, j3,
and the number of 4-circles of S is 1 (for C) + (number of distinct
second circles).

This script measures the joint distribution of (j1,j2,j3) and checks that
the profile is determined by it.

Run:  python arc_k7_triples.py --q 5
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
        circ_of_quad = {}
        for ci, B in enumerate(circles):
            for quad in itertools.combinations(B, 4):
                circ_of_quad[quad] = ci

        ci = 0
        B = circles[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]
        T = tuple(B[:4])
        Tset = set(T)

        joint = Counter()
        for xyz in itertools.combinations(outside, 3):
            Sset = Tset | set(xyz)
            # profile
            hits = {}
            for quad in itertools.combinations(sorted(Sset), 4):
                cj = circ_of_quad.get(quad)
                if cj is None:
                    continue
                hits[cj] = len(Sset & set(circles[cj]))
            prof = tuple(sorted(hits.values(), reverse=True))
            # j values for the 3 pairs
            js = []
            for xy in itertools.combinations(xyz, 2):
                j = 0
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    if len(Tset & set(circles[cj])) == 2:
                        j += 1
                js.append(j)
            joint[(tuple(sorted(js)), prof)] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (j-triple, profile) -> count", flush=True)
        for (js, prof), cnt in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    js={js} prof={prof}: {cnt}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
