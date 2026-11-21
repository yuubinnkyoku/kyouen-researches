"""THE (4,*) FAMILIES AT k=6: counting via circle pairs.

For a 6-set S with profile (4,), (4,4) or (4,4,4), the circles carrying
exactly 4 points of S are the key objects.  Two such circles share at most
2 points, and since each carries 4 of the 6 points, they share exactly 2.

So the (4,*) families are governed by PAIRS OF CIRCLES MEETING IN 2 POINTS.

Let me count directly.

SETUP.  Fix a circle C (b choices) and 4 points of it (C(q+1,4) choices).
The remaining 2 points x, y are outside C.  The profile depends on how
many OTHER circles carry 4 points of S:

  (4,)    : no other circle carries 4 of S
  (4,4)   : exactly one other circle carries 4 of S
  (4,4,4) : exactly two others

A second circle C' carries 4 points of S iff it contains 2 points of C∩S
and both x and y (since it can hold at most 2 of C's points, and needs 4
total from the 6).  So:

    C' must pass through x and y, and through 2 of the 4 chosen points.

The circles through x and y form a pencil of q+1 circles.  Of these, the
ones that also meet the chosen 4 points in exactly 2 are the "second
circles".

So the count depends on how many of the q+1 circles through x,y meet a
given 4-subset of C in exactly 2 points.  That is a geometric quantity
depending on the configuration.

This script measures that quantity empirically and looks for a formula.

Run:  python arc_k6_pairs.py --q 5 7
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
        # circles through each pair of points
        circ_through_pair = {}
        for ci, B in enumerate(circles):
            for pair in itertools.combinations(B, 2):
                circ_through_pair.setdefault(pair, []).append(ci)

        # for each (circle C, 4-subset T of C, pair {x,y} outside C),
        # count how many circles through x,y meet T in exactly 2 points
        dist = Counter()
        samples = 0
        for ci, B in enumerate(circles):
            Bset = set(B)
            outside = [p for p in range(n) if p not in Bset]
            for T in itertools.combinations(B, 4):
                Tset = set(T)
                for xy in itertools.combinations(outside, 2):
                    cnt = 0
                    for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                        if cj == ci:
                            continue
                        if len(Tset & set(circles[cj])) == 2:
                            cnt += 1
                    dist[cnt] += 1
                    samples += 1
        row = {"q": q, "n": n, "b": b, "samples": samples,
               "second_circle_count_histogram":
                   {str(k): v for k, v in sorted(dist.items())}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, {samples} (C,T,xy) triples", flush=True)
        print(f"  #second circles meeting T in exactly 2 points:", flush=True)
        for k, v in sorted(dist.items()):
            print(f"    {k}: {v}  ({v/samples:.4f})", flush=True)

    print()
    print("If the histogram is concentrated on a few values, the (4,*)")
    print("counts can be expressed through it.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
