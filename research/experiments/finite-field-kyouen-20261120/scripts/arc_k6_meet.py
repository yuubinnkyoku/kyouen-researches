"""THE meet HISTOGRAM IS ORBIT-INDEPENDENT: a clean structural theorem.

MEASURED:

    q=5: 1 orbit,  meet = {0:560, 1:400, 2:180}
    q=7: 2 orbits, BOTH have meet = {0:4074, 1:2184, 2:630}

So the total number of (C', xy) incidences with |T ∩ C'| = m does NOT
depend on the orbit of T.  Only the JOINT distribution (how many xy give
0, 1 or 2 second circles) depends on the orbit.

WHY?  The meet histogram counts, over all pairs {x,y} outside C and all
circles C' through x,y, how many points of T lie on C'.  Summing over all
{x,y} and all C' is a "double count" that only sees the SIZE of T, not its
orbit.  Specifically:

    sum over {x,y}, C' of |T ∩ C'|  =  sum over p in T of
        #{({x,y}, C') : p in C', x,y in C', x,y outside C}

and this depends only on |T| = 4.

So the meet histogram is a function of q alone.  []

CONSEQUENCE.  Write the joint distribution as a matrix
    M[j][m] = #{(x,y) : j second circles, and total meet-count m}
but we only observe the marginals.  The orbit dependence lives entirely in
the j-marginal.

Let me compute the meet histogram in closed form.

For a fixed p in T and a fixed circle C' through p: C' meets C in at most
2 points, and p is one of them (p is in C and in C').  So C' meets C in
exactly 2 points, one of which is p.  The other point p' is any of the q
other points of C.  Then {x,y} must be 2 points of C' outside C, so
C(q-1, 2) choices.

So for each p in T (4 choices) and each p' in C \\ {p} (q choices), and each
C' through p,p' (there are q+1 such circles, but one of them is C itself),
we get q circles C' != C, each contributing C(q-1,2) pairs {x,y}.

    meet total = 4 * q * q * C(q-1,2)

Check q=5: 4*5*5*C(4,2) = 4*25*6 = 600.  But observed total is
560+400+180 = 1140.  Not matching -- because each (C', {x,y}) pair is
counted once per point of T on C', so the total is
sum over (C',xy) of |T ∩ C'|, and my count above already includes the
multiplicity.  Let me recount: 4*5*5*6 = 600 vs 1140.  Factor ~1.9.

Let me just fit numerically.

Run:  python arc_k6_meet.py --q 5 7
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
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, ovoid, circles = build(q)
        n = len(ovoid)
        b = len(circles)
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

        meet = Counter()
        for xy in itertools.combinations(outside, 2):
            for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                if cj == ci:
                    continue
                meet[len(Tset & set(circles[cj]))] += 1

        total = sum(meet.values())
        row = {"q": q, "n": n, "b": b, "meet": dict(sorted(meet.items())),
               "total": total,
               "pairs_xy": comb(n - q - 1, 2),
               "circles_per_pair": q + 1}
        rows.append(row)
        print(f"q={q}: n={n}, circle size {q+1}", flush=True)
        print(f"  meet histogram {dict(sorted(meet.items()))}, "
              f"total {total}", flush=True)
        print(f"  C(n-q-1,2)*(q+1) = {comb(n-q-1,2)*(q+1)}", flush=True)
        print(f"  total/(q+1) = {total/(q+1)}", flush=True)
        print(f"  total/4 = {total/4}", flush=True)
        # try formulas
        print(f"  4*q*q*C(q-1,2) = {4*q*q*comb(q-1,2)}", flush=True)
        print(f"  4*q*(q+1)*C(q-1,2) = {4*q*(q+1)*comb(q-1,2)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
