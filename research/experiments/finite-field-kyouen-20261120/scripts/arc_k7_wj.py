"""k=7: the (w, j-triple) joint distribution.

Everything in k=7 now reduces to the joint distribution of
(w, j1, j2, j3) over (C, T, {x,y,z}).

MEASURED (q=5, per (C,T), over C(20,3)=1140 triples):

    w=0 js=(1,1,1) 320    w=0 js=(1,1,2) 136    w=0 js=(0,1,2)  96
    w=0 js=(0,1,1)  88    w=0 js=(0,0,1)  16    w=0 js=(1,2,2)  16
    w=0 js=(0,2,2)  16    w=0 js=(0,0,2)  12
    w=1 js=(0,1,1) 224    w=1 js=(1,1,1)  48    w=1 js=(0,0,1)  48
    w=2 js=(1,1,2)  88    w=2 js=(1,1,1)  32

MEASURED (q=7, over C(42,3)=11480 triples):

    w=0 js=(0,1,1) 2800   w=0 js=(1,1,1) 2016   w=0 js=(0,0,1) 1072
    w=0 js=(0,1,2)  928   w=0 js=(1,1,2)  388   w=0 js=(0,0,2)  204
    w=0 js=(0,0,0)   64   w=0 js=(0,2,2)   56   w=0 js=(1,2,2)   32
    w=1 js=(0,0,1) 1424   w=1 js=(0,1,1) 1312   w=1 js=(0,0,0)  224
    w=1 js=(1,1,1)  120
    w=2 js=(1,1,2)  424   w=2 js=(1,1,1)  416

STRUCTURE.  The j's are the k=6 pencil quantities for the three pairs.
For a FIXED pair {x,y}, j({x,y}) depends only on the pencil through x,y,
which is determined by the pair.  The three pairs share points, so the
j's are correlated.

KEY: j({x,y}) = number of circles through x,y meeting T in exactly 2
points.  From k=6, this is determined by the involution iota(x,y) on C:
j = number of iota-pairs inside T.

So the j-triple is determined by the three involutions iota(x,y),
iota(x,z), iota(y,z).  These three involutions are related: they come from
the three pencils through the pairs of a triple.

Let me measure the joint distribution of the three involutions' pair
counts inside T, and look for the closed form.

Run:  python arc_k7_wj.py --q 5 7
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
            js = []
            for xy in itertools.combinations(xyz, 2):
                j = 0
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    if len(Tset & set(circles[cj])) == 2:
                        j += 1
                js.append(j)
            joint[(w, tuple(sorted(js)))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (w, j-triple) -> count", flush=True)
        for (w, js), cnt in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    w={w} js={js}: {cnt}", flush=True)
        # marginals
        wm = Counter()
        jm = Counter()
        for (w, js), cnt in joint.items():
            wm[w] += cnt
            jm[js] += cnt
        print(f"  w marginal: {dict(sorted(wm.items()))}", flush=True)
        print(f"  j-triple marginal: {dict(sorted(jm.items()))}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
