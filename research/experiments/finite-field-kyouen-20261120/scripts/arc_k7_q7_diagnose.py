"""k=7 at q=7: the profile formula FAILS (non-integer result).

At q=5 the assembled count was an exact integer and matched the exhaustive
count.  At q=7 the same assembly gives

    bad = 4033248800/143   (NOT an integer)

so the formula is WRONG at q=7.

WHY?  The profile formula

    #4-circles = 1 + u + [w = 1]
    #5-circles = [w = 2]

was derived under the assumption that the circles carrying >= 4 points of
S are exactly:
  - C itself (4 points of T)
  - the pencil circles meeting T in 2 points (each 4 points)
  - W (5 or 4 points depending on w)

At q=5 that was complete.  At q=7 there are MORE ways for a circle to
carry >= 4 points of S:

  A circle C' can carry 3 of T and 1 of {x,y,z} -- but C' meets C in at
  most 2 points, so it cannot carry 3 of T.  So that is not it.

  A circle C' can carry 2 of T and 2 of {x,y,z} -- that is the pencil case.

  A circle C' can carry 2 of T and 3 of {x,y,z} -- that is W.

  A circle C' can carry 1 of T and 3 of {x,y,z} -- that is W with w=1.

  A circle C' can carry 0 of T and 4 of {x,y,z} -- IMPOSSIBLE, {x,y,z} has
  only 3 points.

So the classification IS complete.  Then why non-integer?

The issue must be the DIVISION.  #sets with profile P = tuples(P)/n4
assumes every 7-set with profile P is counted exactly n4 times.  That is
true only if the tuple loop enumerates (C, T, {x,y,z}) with C a 4-circle
of S and T = C cap S.

But the tuple loop fixes T as a 4-subset of C, and C is the circle through
0,1,infinity -- a FIXED circle.  So the loop only counts 7-sets whose
4-circle is THAT SPECIFIC C, not any 4-circle!

At q=5 the multiplication by b*C(s,4) happened to work because... let me
check.  Actually at q=5 it gave an integer and matched.  Let me re-examine.

Run:  python arc_k7_q7_diagnose.py --q 7
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction
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

        circ_through_pair = {}
        for k, BB in enumerate(blocks):
            for pair in itertools.combinations(BB, 2):
                circ_through_pair.setdefault(pair, []).append(k)
        circ_of_triple = {}
        for k, BB in enumerate(blocks):
            for tri in itertools.combinations(BB, 3):
                circ_of_triple[tri] = k

        outside = [p for p in range(n) if p not in Bset]

        # For each (T, {x,y,z}) compute the ACTUAL profile by brute force
        # and compare with the formula.
        mismatch = Counter()
        checked = 0
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            for xyz in itertools.combinations(outside, 3):
                Sset = Tset | set(xyz)
                # actual profile
                hits = {}
                for quad in itertools.combinations(sorted(Sset), 4):
                    cj = circ_of_triple.get(tuple(sorted(quad[:3])))
                    if cj is None:
                        continue
                    if all(p in blocks[cj] for p in quad):
                        hits[cj] = len(Sset & set(blocks[cj]))
                actual = tuple(sorted(hits.values(), reverse=True))
                # formula
                W = circ_of_triple.get(tuple(sorted(xyz)))
                WcapC = Bset & set(blocks[W]) if W is not None else set()
                w = len(WcapC)
                union = set()
                for xy in itertools.combinations(xyz, 2):
                    for kk in circ_through_pair.get(tuple(sorted(xy)), []):
                        if kk == ci:
                            continue
                        if len(Bset & set(blocks[kk])) == 2:
                            union.add(kk)
                u = len(union - ({W} if W is not None else set()))
                n4 = 1 + u + (1 if w == 1 else 0)
                n5 = 1 if w == 2 else 0
                pred = tuple([5] * n5 + [4] * n4)
                checked += 1
                if actual != pred:
                    mismatch[(actual, pred)] += 1
                if checked >= 20000:
                    break
            if checked >= 20000:
                break

        row = {"q": q, "checked": checked,
               "mismatches": sum(mismatch.values()),
               "examples": {str(k): v for k, v in
                            sorted(mismatch.items(), key=lambda x: -x[1])[:5]}}
        rows.append(row)
        print(f"q={q}: checked {checked} (T,xyz) pairs", flush=True)
        print(f"  mismatches: {sum(mismatch.values())}", flush=True)
        for (a, p), v in sorted(mismatch.items(), key=lambda x: -x[1])[:5]:
            print(f"    actual {a} vs predicted {p}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
