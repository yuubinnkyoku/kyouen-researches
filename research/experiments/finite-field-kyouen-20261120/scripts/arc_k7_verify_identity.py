"""k=7: the COMPLETE profile formula (4 through q+1 points per circle).

The gap: the formula only produced 4s and 5s, but a circle can carry up to
s = q+1 points of S.

THE FULL CLASSIFICATION.  For S = T u {x,y,z} with |T| = 4, T in C, and
x,y,z outside C, a circle C' != C carries at most 2 of T (since C' meets C
in <= 2 points).  So

    |C' cap S| = |C' cap T| + |C' cap {x,y,z}|  <=  2 + 3 = 5.

So NO circle other than C can carry more than 5 points of S!

The only circle that can carry 6 or 7 points is C itself (which carries
all 4 of T).  But C carries exactly 4 of S (the 4 points of T), since
x,y,z are outside C.

So where do 6-point circles come from?  They must be circles carrying
4 of T... impossible (max 2).

CONCLUSION: for k=7 with |T|=4, no circle carries 6 or 7 points of S.
So the profile really is only 4s and 5s.

Then the 1,414,000 gap must come from somewhere else.

Let me recheck: the exhaustive count says arcs=0, i.e. EVERY 7-set has a
4-circle.  The assembly says 1,414,000 sets have NO 4-circle.

But the assembly's profiles all have at least one 4 (the minimum is (4,)).
So the assembly never produces an arc.  Then arcs should be 0, not
1,414,000!

Let me recheck the arithmetic: bad = 98,470,400, C(n,7) = 99,884,400,
so arcs = 1,414,000.  But if every profile has >= 1 four-circle, then
every counted set is bad, and the uncounted 1,414,000 are... not counted
at all.

So the assembly UNDERCOUNTS the bad sets by 1,414,000.  Those are 7-sets
that have a 4-circle but are not counted by the tuple loop.

WHY?  Because the tuple loop fixes C = P^1(F_q).  A 7-set S is counted
only if C is one of its 4-circles.  If S's 4-circles are all different
from C, S is not counted.

The division by #4-circles(P) then gives the wrong answer: it divides by
the number of 4-circles, but only counts sets where C is among them.

CORRECT: sum over C of (count for that C) = sum over S of #4-circles(S).
So dividing by #4-circles(P) IS right... but only if we sum over ALL C.

The code uses scale = b, which multiplies the fixed-C count by b.  That
assumes every C gives the same count, which is true by symmetry.  So
sum over C = b * (fixed-C count).  That IS right.

Hmm.  Let me just check the numbers directly: does b * (fixed-C tuples)
equal sum over S of #4-circles(S)?

Run:  python arc_k7_verify_identity.py --q 7
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

from inversive_all_q import build_field, build_inversive_plane  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[7])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, sub = build_field(q)
        points, circles = build_inversive_plane(q)
        idx = {p: i for i, p in enumerate(points)}
        blocks = [tuple(sorted(idx[p] for p in c)) for c in circles]
        n = len(points)
        b = len(blocks)
        s = q + 1
        base = set(sub) | {None}
        ci = None
        for k, B in enumerate(blocks):
            if set(points[i] for i in B) == base:
                ci = k
                break
        B = blocks[ci]
        Bset = set(B)
        circ_of_triple = {}
        for k, BB in enumerate(blocks):
            for tri in itertools.combinations(BB, 3):
                circ_of_triple[tri] = k

        outside = [p for p in range(n) if p not in Bset]

        # LHS: b * (number of (T,xyz) tuples for the fixed C)
        tuples = 0
        for T in itertools.combinations(B, 4):
            for xyz in itertools.combinations(outside, 3):
                tuples += 1

        # RHS: sum over 7-sets of #4-circles
        circ_of_quad = {}
        for k, BB in enumerate(blocks):
            for quad in itertools.combinations(BB, 4):
                circ_of_quad[quad] = k
        rhs = 0
        for S in itertools.combinations(range(n), 7):
            hits = set()
            for quad in itertools.combinations(S, 4):
                cj = circ_of_quad.get(quad)
                if cj is not None:
                    hits.add(cj)
            rhs += len(hits)

        row = {"q": q, "n": n, "b": b, "s": s,
               "fixed_C_tuples": tuples,
               "b_times_tuples": b * tuples,
               "sum_over_S_of_4circles": rhs,
               "equal": b * tuples == rhs}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  fixed-C tuples = {tuples}", flush=True)
        print(f"  b * tuples = {b * tuples}", flush=True)
        print(f"  sum over S of #4-circles = {rhs}", flush=True)
        print(f"  equal: {row['equal']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
