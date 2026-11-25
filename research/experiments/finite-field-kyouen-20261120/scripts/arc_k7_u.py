"""k=7: the u distribution conditioned on w.

From the k=7 profile formula, the profile is determined by (w, u).  The w
marginal is closed.  Now the u distribution given w.

MEASURED (q=5, per (C,T), over C(20,3)=1140 triples):

    w=0: u=1:16  u=2:100  u=3:416  u=4:152  u=5:16     (total 700)
    w=1: u=1:48  u=2:224  u=3:48                       (total 320)
    w=2: u=0:32  u=1:88                                (total 120)

MEASURED (q=7, over C(42,3)=11480 triples):

    w=0: u=0:64  u=1:1072  u=2:3004  u=3:2944  u=4:444  u=5:32  (7560)
    w=1: u=0:224 u=1:1424  u=2:1312  u=3:120                    (3080)
    w=2: u=0:416 u=1:424                                        (840)

STRUCTURE.  u counts the pencil circles through pairs of {x,y,z} that meet
T in 2 points, excluding W.  There are 3 pairs, and each pair's pencil has
j circles meeting T in 2 points (the k=6 quantity).  So

    u = |union of the 3 pencils| - [W in union]

The union size depends on how the 3 pencils overlap.

Let me measure the relationship between u and the j-triple, conditioned on w.

Run:  python arc_k7_u.py --q 5 7
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
            union = set()
            js = []
            for xy in itertools.combinations(xyz, 2):
                j = 0
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    if len(Tset & set(circles[cj])) == 2:
                        union.add(cj)
                        j += 1
                js.append(j)
            u = len(union - ({W} if W is not None else set()))
            joint[(w, tuple(sorted(js)), u)] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (w, j-triple, u) -> count", flush=True)
        for (w, js, u), cnt in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    w={w} js={js} u={u}: {cnt}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
