"""k=7: the (5,*) family closes exactly.

MEASURED (q=5, n=26, b=130, s=6):

    (6,)      = 2600  = b*C(s,6)*C(n-s,1)          EXACT
    (5,4)     = 62400
    (5,4,4)   = 85800
    ----------------------
    (5,*) sum = 148200 = b*C(s,5)*C(n-s,2)          EXACT

So the (5,*) family splits the naive count b*C(s,5)*C(n-s,2) into two
parts: those where a SECOND circle also carries 4 points (profile (5,4,4))
and those where it does not (profile (5,4)).

This is exactly the same structure as k=6's (4,*) family: fix the circle C
and its 5-subset T, then the remaining 2 points {x,y} outside C determine
whether a second circle appears.

For k=6 the second circle had to meet T in exactly 2 points.  Here T has 5
points and the second circle C' must carry 4 of S = T u {x,y}.  Since
|C' cap C| <= 2, C' can carry at most 2 of T, so it must carry both x and y
plus exactly 2 of T.

So the condition is IDENTICAL to k=6: C' passes through x,y and meets T in
exactly 2 points.  The only difference is that T now has 5 points instead
of 4.

So the (5,*) split is governed by the SAME pencil involution, with T of
size 5 instead of 4.

Let me verify: for T of size 5, the number of 5-subsets containing exactly
j pairs of the involution is

    H5(n2, n1, j) = sum_a C(n2,j)*C(n2-j,a)*2^a*C(n1, 5-2j-a)

and the (5,*) split should be
    (5,4,4) = b * sum_{n2} N_xy(n2) * H5(n2,n1,1)   (j=1 -> one second circle)
    (5,4)   = b * sum_{n2} N_xy(n2) * H5(n2,n1,0)

Wait: j is the number of second circles.  j=0 -> (5,4), j=1 -> (5,4,4).
And each 7-set with profile (5,4,4) is counted twice (once per 4-circle)?
No -- the profile (5,4,4) has ONE 5-circle and TWO 4-circles.  Fixing the
5-circle, it is counted once.  So no division.

Let me verify numerically.

Run:  python arc_k7_five.py --q 5
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
from arc_k6_pure import N_xy  # noqa: E402


def H(n2, n1, j, k):
    total = 0
    for a in range(0, n2 - j + 1):
        used = 2 * j + a
        if used > k:
            break
        rest = k - used
        if rest < 0 or rest > n1:
            continue
        total += comb(n2, j) * comb(n2 - j, a) * (2 ** a) * comb(n1, rest)
    return total


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

        # for T of size 5, count j distribution
        groups = Counter()
        for T in itertools.combinations(B, 5):
            Tset = set(T)
            d = Counter()
            for xy in itertools.combinations(outside, 2):
                j = 0
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    if len(Tset & set(circles[cj])) == 2:
                        j += 1
                d[j] += 1
            groups[tuple(sorted(d.items()))] += 1

        # closed form
        pred = {}
        for n2, cnt in N_xy(q).items():
            n1 = s - 2 * n2
            for j in (0, 1, 2):
                pred[j] = pred.get(j, 0) + b * cnt * H(n2, n1, j, 5)

        row = {"q": q, "n": n, "b": b, "groups": {str(k): v for k, v in
                                                  groups.items()},
               "predicted_by_j": pred}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        for dist, cnt in groups.items():
            print(f"  {cnt} T-subsets with j-dist {dict(dist)}", flush=True)
        print(f"  predicted (5,*) split by j: {pred}", flush=True)
        # observed
        obs = Counter()
        for dist, cnt in groups.items():
            for j, v in dict(dist).items():
                obs[j] += v * cnt
        print(f"  observed by j: {dict(sorted(obs.items()))}", flush=True)
        print(f"  match: {dict(sorted(obs.items())) == pred}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
