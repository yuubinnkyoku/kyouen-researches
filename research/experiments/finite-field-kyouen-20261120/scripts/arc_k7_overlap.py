"""k=7: what distinguishes the two (A, (2,2,3), 0) types?

MEASURED: (A, (2,2,3), |W cap C|=0) splits into two types:

    dist1 = (0,1):1 (0,2):2 (0,3):11 (0,4):1        240 triples
    dist2 = (0,2):5 (0,3):8 (0,4):2                  120 triples

Both have case A, n2-triple (2,2,3), and W disjoint from C.

The difference must be in HOW the three involutions' pairs sit relative to
each other.  In case A they are disjoint, so the union has 2+2+3 = 7 pairs
covering 14 points of C (s=6, so this is impossible!).

Wait: s = q+1 = 6, so C has only 6 points.  An involution on C has at most
3 pairs.  n2-triple (2,2,3) means the three involutions have 2, 2 and 3
pairs.  In case A they are disjoint, so the union has 7 pairs = 14 points,
but C has only 6 points.  Contradiction!

So "disjoint" must mean something else.  Let me re-check: the involutions
are on C, which has s = q+1 = 6 points.  An involution with 3 pairs covers
all 6 points.  Two disjoint involutions would need 12 points.

So case A cannot mean "disjoint as sets of pairs".  Let me re-read the
earlier measurement: the "common pair" counts were (0,0,0) or (1,1,1).
(0,0,0) means no pair is shared between any two of the three involutions.
But the involutions can still OVERLAP in points without sharing a pair.

So case A = "no shared pair", not "disjoint point sets".

Let me measure the actual point-level overlap.

Run:  python arc_k7_overlap.py --q 5
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
        circ_of_triple = {}
        for ci, B in enumerate(circles):
            for tri in itertools.combinations(B, 3):
                circ_of_triple[tri] = ci

        ci = 0
        B = circles[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]

        joint = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = circ_of_triple.get(tuple(sorted(xyz)))
            WcapC = Bset & set(circles[W]) if W is not None else set()
            invs = []
            n2s = []
            for xy in itertools.combinations(xyz, 2):
                pairs = set()
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    cap = Bset & set(circles[cj])
                    if len(cap) == 2:
                        pairs.add(tuple(sorted(cap)))
                invs.append(frozenset(pairs))
                n2s.append(len(pairs))
            common = (len(invs[0] & invs[1]), len(invs[0] & invs[2]),
                      len(invs[1] & invs[2]))
            case = "B" if common == (1, 1, 1) else "A"

            # point-level overlap: how many points of C are covered by
            # each involution, and the union size
            covered = [set(p for pr in inv for p in pr) for inv in invs]
            union_pts = covered[0] | covered[1] | covered[2]
            # pairwise point overlaps
            ov = (len(covered[0] & covered[1]), len(covered[0] & covered[2]),
                  len(covered[1] & covered[2]))

            dist = Counter()
            for T in itertools.combinations(B, 4):
                Tset = set(T)
                w = len(Tset & WcapC)
                u = set()
                for inv in invs:
                    for pr in inv:
                        if pr[0] in Tset and pr[1] in Tset:
                            u.add(pr)
                dist[(w, len(u))] += 1
            joint[(case, tuple(sorted(n2s)), len(WcapC),
                   tuple(sorted(ov)), len(union_pts),
                   tuple(sorted(dist.items())))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (case, n2, |W cap C|, point-overlaps, |union pts|, dist)"
              f" -> count", flush=True)
        for k, v in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
