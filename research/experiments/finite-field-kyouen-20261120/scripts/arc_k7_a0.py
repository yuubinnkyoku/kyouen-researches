"""k=7: the a=0 types (W disjoint from C).

MEASURED (q=5, a=0, 600 triples, 5 types):

    (0,1):1 (0,2):2 (0,3):11 (0,4):1        240
    (0,2):1 (0,3):11 (0,4):2 (0,5):1        120
    (0,2):5 (0,3):8 (0,4):2                 120
    (0,2):2 (0,3):8 (0,4):5                  60
    (0,3):6 (0,4):9                          40
    (0,2):9 (0,3):6                          20

Wait, that is 6 types summing to 600.  Let me recount: 240+120+120+60+40+20
= 600.  So a=0 has SIX types, not five.

For a=0, W is disjoint from C, so w = 0 always.  Hence all distributions
have w=0 only.  The variation is in u.

So for a=0 the type is determined by the u-distribution over T.

u = number of involution pairs inside T.  The three involutions are
pairwise disjoint (case A, since a != 2).  So u = j1+j2+j3 where each j is
the count for one involution.

The u-distribution over T depends on the three involutions' pair sets.
Since they are disjoint as PAIRS but may share POINTS, the distribution
depends on the point-level overlap.

Let me measure the a=0 types by (n2-triple, point-overlap vector).

Run:  python arc_k7_a0.py --q 5
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

        joint = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = None
            for cj, BB in enumerate(circles):
                if cj == ci:
                    continue
                if all(p in BB for p in xyz):
                    W = cj
                    break
            WcapC = Bset & set(circles[W]) if W is not None else set()
            a = len(WcapC)
            if a != 0:
                continue
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
            covered = [set(p for pr in inv for p in pr) for inv in invs]
            ov = (len(covered[0] & covered[1]), len(covered[0] & covered[2]),
                  len(covered[1] & covered[2]))
            union_pts = len(covered[0] | covered[1] | covered[2])

            dist = Counter()
            for T in itertools.combinations(B, 4):
                Tset = set(T)
                u = set()
                for inv in invs:
                    for pr in inv:
                        if pr[0] in Tset and pr[1] in Tset:
                            u.add(pr)
                dist[(0, len(u))] += 1
            joint[(tuple(sorted(n2s)), tuple(sorted(ov)), union_pts,
                   tuple(sorted(dist.items())))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}  (a=0 only)", flush=True)
        print(f"  (n2, point-overlap, |union pts|, dist) -> count", flush=True)
        for k, v in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
