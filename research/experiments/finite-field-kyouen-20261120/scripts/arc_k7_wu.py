"""k=7: the (w,u) joint distribution.

From the k=7 profile formula, the profile of S = T u {x,y,z} is

    #4-circles = 1 + u + [w = 1]
    #5-circles = [w = 2]

where W is the circle through x,y,z, w = |T cap W|, and u is the number of
pencil circles (meeting T in 2 points) other than W.

So the whole k=7 count reduces to the joint distribution of (w, u) over
(C, T, {x,y,z}).

MEASURED (q=5, per (C,T) with |T|=4, over C(20,3)=1140 triples):

    w=0 u=3: 416    w=1 u=2: 224    w=0 u=4: 152
    w=0 u=2: 100    w=2 u=1:  88    w=1 u=3:  48
    w=1 u=1:  48    w=2 u=0:  32    w=0 u=1:  16
    w=0 u=5:  16

Total 1140.

Let me derive each entry.

w = |T cap W|: W is the circle through x,y,z.  For fixed T (4 points of C),
as {x,y,z} varies, W varies over all circles meeting C in 0,1,2 points.
w = |T cap W| is determined by |C cap W| and which points.

u: the number of pencil circles through pairs of {x,y,z} meeting T in 2
points, excluding W.

Let me measure the marginals and the conditional structure.

Run:  python arc_k7_wu.py --q 5
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
        w_marg = Counter()
        u_marg = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = circ_of_triple.get(tuple(sorted(xyz)))
            w = len(Tset & set(circles[W])) if W is not None else 0
            union = set()
            for xy in itertools.combinations(xyz, 2):
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    if len(Tset & set(circles[cj])) == 2:
                        union.add(cj)
            u = len(union - ({W} if W is not None else set()))
            joint[(w, u)] += 1
            w_marg[w] += 1
            u_marg[u] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {f"{a},{c}": v for (a, c), v in sorted(joint.items())},
               "w_marginal": dict(sorted(w_marg.items())),
               "u_marginal": dict(sorted(u_marg.items()))}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}, "
              f"C(n-s,3)={comb(n-s,3)}", flush=True)
        print(f"  w marginal: {dict(sorted(w_marg.items()))}", flush=True)
        print(f"  u marginal: {dict(sorted(u_marg.items()))}", flush=True)
        print(f"  joint (w,u):", flush=True)
        for (a, c), v in sorted(joint.items()):
            print(f"    w={a} u={c}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
