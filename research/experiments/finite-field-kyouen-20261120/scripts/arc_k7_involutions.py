"""k=7: the j-triple marginal.

MEASURED (q=5, per (C,T), over C(20,3)=1140 triples):

    (0,0,1):  64    (0,0,2):  12    (0,1,1): 312    (0,1,2):  96
    (0,2,2):  16    (1,1,1): 400    (1,1,2): 224    (1,2,2):  16

Total 1140.

STRUCTURE.  For a fixed pair {x,y}, j({x,y}) is the number of iota-pairs
inside T, where iota is the involution induced by the pencil through x,y.
From k=6 we know j in {0,1,2} and the distribution over pairs is

    N_xy(n2) pairs have n2 2-secant circles, and the count of T with
    exactly j pairs inside is H(n2, n1, j, 4).

For the TRIPLE, the three pairs share points, so the j's are correlated.
The observed j-triples are all of the form (a,b,c) with a <= b <= c and
c - a <= 2, and never (0,0,0) at q=5 (but (0,0,0) DOES occur at q=7).

Let me look for the structure: the three involutions iota(x,y), iota(x,z),
iota(y,z) are related.  In fact, for a triple {x,y,z}, the three pencils
are the "sides" of a triangle, and there is a classical relation.

Let me measure the joint distribution of the three involutions directly
(as permutations of C) and see how they relate.

Run:  python arc_k7_involutions.py --q 5
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
        T = tuple(B[:4])
        Tset = set(T)

        # for each triple, record the three involutions as frozensets of pairs
        rel = Counter()
        for xyz in itertools.combinations(outside, 3):
            invs = []
            for xy in itertools.combinations(xyz, 2):
                pairs = set()
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    cap = Bset & set(circles[cj])
                    if len(cap) == 2:
                        pairs.add(tuple(sorted(cap)))
                invs.append(frozenset(pairs))
            # how do the three involutions relate?
            # count common pairs
            common = (len(invs[0] & invs[1]), len(invs[0] & invs[2]),
                      len(invs[1] & invs[2]))
            rel[tuple(sorted(common))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "common_pairs": {str(k): v for k, v in
                                sorted(rel.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  pairwise common-pair counts among the 3 involutions:",
              flush=True)
        for k, v in sorted(rel.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
