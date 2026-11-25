"""N_xy IN CLOSED FORM: the last piece of k=6.

MEASURED:
    q=5: tangent circles 24 = q^2-1;  N_xy {2:120, 3:70}
    q=7: tangent circles 48 = q^2-1;  N_xy {3:504, 4:357}
    q=8: tangent circles 63 = q^2-1;  N_xy {0:28, 4:1512}

THEOREM 1.  The number of circles tangent to C is q^2 - 1.

PROOF.  Each point p of C has q-1 tangent circles (proved earlier), and
each tangent circle touches C at exactly one point.  So the total is
(q+1)(q-1) = q^2 - 1.  []

THEOREM 2.  A pair {x,y} outside C lies on a tangent circle iff its
pencil contains a tangent circle.  The number of such pairs:

    #pairs on some tangent circle = (q^2-1) * C(q,2) / (multiplicity)

Each tangent circle has q points outside C, so C(q,2) pairs.  A pair lies
on exactly ONE circle, so no overcounting:

    #pairs on a tangent circle = (q^2-1) * C(q,2)

Check q=5: 24*10 = 240.  But measured on_tangent pairs = 120.  Factor 2.

Hmm.  A pair {x,y} lies on exactly one circle, so the count of
(pair, tangent circle) incidences is (q^2-1)*C(q,2), and each pair is
counted once per tangent circle containing it.  If a pair is on a tangent
circle, it is counted once.  So #pairs = (q^2-1)*C(q,2) only if each pair
is on at most one tangent circle -- true.  So #pairs should be 240, but
measured 120.

The discrepancy: the tangent circle through x,y might BE the circle C
itself?  No, C is not tangent to itself.

Resolution: a tangent circle at p has q points outside C, but the pair
{x,y} must have BOTH points outside C.  That is C(q,2) per tangent circle.
24 * 10 = 240 pairs, but each pair is on exactly one circle, so 240
distinct pairs.  Measured 120.  Factor 2 means each pair is on TWO tangent
circles?  Impossible (two circles meet in at most 2 points).

Let me just measure the multiplicity directly.

Run:  python arc_k6_multiplicity.py --q 5 7 8
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
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7, 8])
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

        tangent = [cj for cj, BB in enumerate(circles)
                   if cj != ci and len(Bset & set(BB)) == 1]

        # multiplicity: how many tangent circles contain each pair
        mult = Counter()
        for cj in tangent:
            pts = [p for p in circles[cj] if p not in Bset]
            for xy in itertools.combinations(pts, 2):
                mult[tuple(sorted(xy))] += 1

        hist = Counter(mult.values())
        row = {"q": q, "n": n, "b": b, "tangent_circles": len(tangent),
               "pairs_on_tangent": len(mult),
               "multiplicity_histogram": {str(k): v for k, v in
                                          sorted(hist.items())},
               "incidences": sum(mult.values()),
               "predicted_incidences": len(tangent) * comb(q, 2)}
        rows.append(row)
        print(f"q={q}: {len(tangent)} tangent circles, "
              f"{len(mult)} pairs on them", flush=True)
        print(f"  multiplicity histogram: {dict(sorted(hist.items()))}",
              flush=True)
        print(f"  incidences {sum(mult.values())} vs "
              f"(q^2-1)*C(q,2) = {len(tangent)*comb(q,2)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
