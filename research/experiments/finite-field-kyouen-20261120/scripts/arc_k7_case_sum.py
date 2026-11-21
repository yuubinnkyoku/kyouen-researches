"""k=7: the (w,u) distribution via the involution cases.

From the involution structure:
  Case A (disjoint involutions): u = j1+j2+j3, and w is independent of the
      involutions (W is not in any pencil).
  Case B (one common pair = W cap C): u = j1+j2+j3 - 3*[w=2].

MEASURED (q=5, per (C,T), over 1140 triples):

    Case A: w=0 -> 680, w=1 -> 160          (total 840)
    Case B: w=0 ->  20, w=1 -> 160, w=2 -> 120  (total 300)

So in Case A, w is 0 or 1 only (never 2), and in Case B all three occur.

WHY?  In Case A the three pencils are disjoint, so no circle through a pair
of {x,y,z} meets T in 2 points AND passes through the third point.  W
passes through all three, so W is in all three pencils -- contradiction
unless W meets T in <= 1 point.  Hence w <= 1 in Case A.  []

In Case B, W IS the common pair's circle, so w can be 0, 1 or 2.

NOW: the (w,u) distribution needs, for each case, the joint law of
(w, j1+j2+j3).

Let me measure the (case, w, sum_j) distribution.

Run:  python arc_k7_case_sum.py --q 5
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
        T = tuple(B[:4])
        Tset = set(T)

        joint = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = circ_of_triple.get(tuple(sorted(xyz)))
            w = len(Tset & set(circles[W])) if W is not None else 0
            invs = []
            js = []
            for xy in itertools.combinations(xyz, 2):
                pairs = set()
                j = 0
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    cap = Bset & set(circles[cj])
                    if len(cap) == 2:
                        pairs.add(tuple(sorted(cap)))
                        if len(Tset & set(circles[cj])) == 2:
                            j += 1
                invs.append(frozenset(pairs))
                js.append(j)
            common = (len(invs[0] & invs[1]), len(invs[0] & invs[2]),
                      len(invs[1] & invs[2]))
            case = "B" if common == (1, 1, 1) else "A"
            joint[(case, w, sum(js))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (case, w, sum_j) -> count", flush=True)
        for k, v in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
