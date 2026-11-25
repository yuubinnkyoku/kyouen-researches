"""THE COMPLETE k=6 CLOSED FORM: no enumeration needed.

Using the fully closed joint intersection table, the k=6 arc count is now a
pure formula in q.

DERIVATION.

A 6-set S is bad iff some circle carries >= 4 of its points.  The profiles
are (6,), (5,), (4,), (4,4), (4,4,4).

    (6,) = b*C(q+1,6)
    (5,) = b*C(q+1,5)*(n-q-1)

For the (4,*) profiles, fix the circle C and its 4-subset T.  The remaining
2 points {x,y} are outside C.  The number of SECOND circles (circles C'
through x,y meeting T in exactly 2 points) determines the profile:

    j = 0  ->  (4,)
    j = 1  ->  (4,4)
    j = 2  ->  (4,4,4)

and each profile is counted (j+1) times over all (C,T,{x,y}).

Now, C' meets T in exactly 2 points.  Since T is a 4-subset of C and C'
meets C in a points, |T ∩ C'| = 2 requires a = 2 (if a <= 1 then
|T ∩ C'| <= 1).  So the second circles are EXACTLY the a=2 circles with
c=2, i.e. the (2,2) entries.

Therefore:

    sum over (C,T,{x,y}) of j  =  (2,2) count  =  6*q*C(q-1,2) per (C,T)

Wait -- (2,2) as computed is the count over ALL {x,y} for ONE (C,T).  So
the total over all (C,T) is b*C(q+1,4) times that.

And sum of j over all {x,y} for one (C,T) = (2,2) = 6*q*C(q-1,2).

So:
    N1 + 2*N2 = b*C(q+1,4) * 6*q*C(q-1,2)

But we need N0 + N1/2 + N2/3, which needs the individual N_j, not just
the sum.  The joint table gives us the marginals but not the joint
distribution of j.

Hmm.  So the joint table alone does NOT close k=6; we still need how the
(2,2) circles distribute over {x,y}.

Let me check: is the number of (2,2) circles per {x,y} determined by the
joint table?  No -- the joint table counts (xy, C') pairs, not per-xy
counts.

So k=6 needs one more ingredient: the distribution of j.  That is exactly
the PGL-orbit-dependent quantity found earlier.

CONCLUSION: the joint table is fully closed, but the k=6 arc count still
needs the per-orbit j-distribution.  Let me state this precisely and check
whether the j-distribution can be derived from the joint table plus
symmetry.

Run:  python arc_k6_final.py --q 5 7
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

        # per (C,T): distribution of j over {x,y}
        groups = Counter()
        for T in itertools.combinations(B, 4):
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

        # closed-form predictions
        n_pts = q * q + 1
        term6 = b * comb(q + 1, 6)
        term5 = b * comb(q + 1, 5) * (n_pts - q - 1)
        # sum of j over all (C,T,xy)
        sum_j = b * comb(q + 1, 4) * 6 * q * comb(q - 1, 2)

        row = {"q": q, "n": n_pts, "b": b,
               "groups": {str(k): v for k, v in groups.items()},
               "term6": term6, "term5": term5,
               "sum_j_closed": sum_j}
        rows.append(row)
        print(f"q={q}: n={n_pts}, b={b}", flush=True)
        print(f"  (6,) = {term6}, (5,) = {term5}", flush=True)
        print(f"  sum of j over all (C,T,xy) = {sum_j}", flush=True)
        for dist, cnt in groups.items():
            d = dict(dist)
            sj = sum(k * v for k, v in d.items())
            print(f"  {cnt} subsets with dist {d}, sum_j per subset {sj}",
                  flush=True)
        # check sum_j
        tot_sj = sum(sum(k * v for k, v in dict(dist).items()) * cnt
                     for dist, cnt in groups.items())
        print(f"  total sum_j from data = {tot_sj} "
              f"(closed {sum_j}) -> {tot_sj == sum_j}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
