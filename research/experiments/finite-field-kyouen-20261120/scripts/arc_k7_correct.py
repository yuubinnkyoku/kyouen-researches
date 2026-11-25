"""k=7: the CORRECT decomposition using the circle through {x,y,z}.

The profile of S = T u {x,y,z} is determined by, for each circle C' != C
carrying >= 4 of S:
    - how many of T it carries (must be 2, since C' meets C in <= 2 points)
    - how many of {x,y,z} it carries (2 or 3)

C' carries 3 of {x,y,z} iff C' is THE circle through x,y,z (unique).
C' carries 2 of {x,y,z} iff C' is in the pencil of that pair.

So the classification is:

  Let W = the circle through x,y,z (unique, W != C in general).
  Let w = |T cap W|  (0, 1 or 2).

  Case w = 2:  W carries 2 of T and 3 of {x,y,z} -> 5 points of S.
               Profile gets a 5.
  Case w <= 1: W carries <= 1 of T, so W is not a 4-circle.

  Separately, for each of the 3 pairs, the pencil circles meeting T in 2
  points give 4-circles (carrying 2 of T and 2 of {x,y,z}).

So the profile is:
    (5, ...) if w = 2
    (4, ...) if w <= 1

and the number of 4s is 1 (for C) + |union of pencil circles| minus those
that are W itself.

This script verifies that (w, |union|) determines the profile.

Run:  python arc_k7_correct.py --q 5
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
        circ_of_triple = {}
        for ci, B in enumerate(circles):
            for tri in itertools.combinations(B, 3):
                circ_of_triple[tri] = ci

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

            W = circ_of_triple.get(tuple(sorted(xyz)))
            w = len(Tset & set(circles[W])) if W is not None else 0

            union = set()
            for xy in itertools.combinations(xyz, 2):
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    if len(Tset & set(circles[cj])) == 2:
                        union.add(cj)
            # remove W from the union (it is counted separately via w)
            union_no_W = union - ({W} if W is not None else set())

            joint[(w, len(union_no_W), prof)] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (w, |union without W|, profile) -> count", flush=True)
        for (w, u, prof), cnt in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    w={w} |union\\W|={u} prof={prof}: {cnt}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
