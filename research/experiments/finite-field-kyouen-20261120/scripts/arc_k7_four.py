"""k=7: the (4,*) family — the genuinely new part.

MEASURED (q=5, n=26, b=130, s=6):

    (4,4)           15600
    (4,4,4)         96200
    (4,4,4,4)      312000
    (4,4,4,4,4)     78000
    (4,4,4,4,4,4)    5200
    ----------------------
    (4,*) total    507000

For k=6 the (4,*) family was indexed by j = number of second circles, and
each 7-set... no, each 6-set was counted (j+1) times.

For k=7 the situation is different: a 7-set with profile (4,4,4) has THREE
4-circles, so fixing one circle C and its 4-subset T counts it 3 times.
The multiplicity is the number of 4-circles, i.e. the number of entries
equal to 4 in the profile.

So:
    (4,4)           counted 2 times
    (4,4,4)         counted 3 times
    (4,4,4,4)       counted 4 times
    (4,4,4,4,4)     counted 5 times
    (4,4,4,4,4,4)   counted 6 times

Let me verify: sum over profiles of count * multiplicity should equal
b * C(s,4) * (number of ways to choose the remaining 3 points) restricted
to those where C is a 4-circle.

Actually the cleanest check: for fixed (C, T) with |T|=4, and 3 more points
{x,y,z} outside C, count how many circles carry >= 4 of S = T u {x,y,z}.
That number is the multiplicity.

Let me measure the distribution of "number of 4-circles" for fixed (C,T).

Run:  python arc_k7_four.py --q 5
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

        # for fixed (C,T) with |T|=4, and 3 outside points, count the
        # number of circles carrying >=4 of S
        T = tuple(B[:4])
        Tset = set(T)
        dist = Counter()
        for xyz in itertools.combinations(outside, 3):
            Sset = Tset | set(xyz)
            # circles carrying >= 4 of S
            hits = set()
            for quad in itertools.combinations(sorted(Sset), 4):
                cj = None
                # find a circle through this quad
                for cand in circ_through_pair.get(tuple(sorted(quad[:2])), []):
                    if all(p in circles[cand] for p in quad):
                        cj = cand
                        break
                if cj is not None:
                    hits.add(cj)
            dist[len(hits)] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "multiplicity_histogram": {str(k): v for k, v in
                                          sorted(dist.items())}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  #circles carrying >=4 of S, over 3 outside points:",
              flush=True)
        for k, v in sorted(dist.items()):
            print(f"    {k}: {v}", flush=True)
        print(f"  total {sum(dist.values())} vs C(n-s,3) = "
              f"{comb(n-s,3)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
