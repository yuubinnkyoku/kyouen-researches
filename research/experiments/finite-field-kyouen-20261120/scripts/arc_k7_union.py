"""k=7: why the j-triple does not determine the profile.

MEASURED (q=5): the same j-triple (1,1,1) gives profiles (4,4,4,4),
(4,4,4,4,4) and (5,4).  So j alone is not enough.

REASON.  j({x,y}) counts the circles through x,y meeting T in exactly 2
points.  For the three pairs of {x,y,z} these circle sets can OVERLAP: a
circle through all three of x,y,z is counted in all three j's.

So the profile depends on the UNION of the three circle sets, not the sum.

Let me measure the union size directly and check that it determines the
profile.

Run:  python arc_k7_union.py --q 5
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
            hits = {}
            for quad in itertools.combinations(sorted(Sset), 4):
                cj = circ_of_quad.get(quad)
                if cj is None:
                    continue
                hits[cj] = len(Sset & set(circles[cj]))
            prof = tuple(sorted(hits.values(), reverse=True))
            # union of second circles over the 3 pairs
            union = set()
            for xy in itertools.combinations(xyz, 2):
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    if len(Tset & set(circles[cj])) == 2:
                        union.add(cj)
            joint[(len(union), prof)] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (|union of second circles|, profile) -> count", flush=True)
        for (u, prof), cnt in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    |union|={u} prof={prof}: {cnt}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
