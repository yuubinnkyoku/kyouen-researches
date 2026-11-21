"""THE INVOLUTION CLOSES k=6: j depends only on n2 and the pairing.

VERIFIED:
    q=5: 190 pairs {x,y}, 0 involution violations,
         n2 histogram {2: 120, 3: 70}
    q=7: 861 pairs {x,y}, 0 involution violations,
         n2 histogram {3: 504, 4: 357}

So the pencil through {x,y} induces an INVOLUTION iota on C (disjoint
pairs), with n2 = number of pairs, and n2 takes exactly TWO values.

    q=5: n2 in {2, 3}   (q-3 = 2, q-2 = 3)
    q=7: n2 in {3, 4}   (q-4 = 3, q-3 = 4)

Hmm, q=5: {2,3} = {q-3, q-2}; q=7: {3,4} = {q-4, q-3}.  Not the same
offset.  Let me look at it as: n2 = (q+1 - n1)/2 and n1 = number of
tangent circles.  Since n0 = n2 and n0+n1+n2 = q+1, we get
2*n2 + n1 = q+1.

    q=5: n2=2 -> n1=2;  n2=3 -> n1=0
    q=7: n2=3 -> n1=2;  n2=4 -> n1=0

So the two cases are "n1 = 2" and "n1 = 0": the pencil either has 2
tangent circles or none.

NOW: j = #{pairs of iota with both points in T}.

Given n2 pairs (an involution on 2*n2 points of C) and a 4-subset T of C,
j counts how many of the n2 pairs lie inside T.

The distribution of j over T depends on how T sits relative to iota.  But
iota is determined by {x,y}, and T is fixed.  So for fixed T, as {x,y}
varies, j varies.

The KEY question: for fixed T, how many {x,y} give j=0, 1, 2?

This is now a clean combinatorial question about involutions on P^1(F_q)
and 4-subsets.  Let me compute it exactly.

Run:  python arc_k6_involution2.py --q 5 7
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

        # For each {x,y}: build the involution, then for each T count j
        # Group by (n2, j) to see the structure
        joint = Counter()
        for xy in itertools.combinations(outside, 2):
            pencil = circ_through_pair.get(tuple(sorted(xy)), [])
            pairs = []
            for cj in pencil:
                if cj == ci:
                    continue
                cap = Bset & set(circles[cj])
                if len(cap) == 2:
                    pairs.append(tuple(sorted(cap)))
            n2 = len(pairs)
            for T in itertools.combinations(B, 4):
                Tset = set(T)
                j = sum(1 for pr in pairs if pr[0] in Tset and pr[1] in Tset)
                joint[(n2, j)] += 1

        row = {"q": q, "n": n, "b": b,
               "joint_n2_j": {f"{a},{c}": v for (a, c), v in
                              sorted(joint.items())}}
        rows.append(row)
        print(f"q={q}: n={n}, circle size {q+1}", flush=True)
        print(f"  (n2, j) -> count", flush=True)
        for (a, c), v in sorted(joint.items()):
            print(f"    n2={a}, j={c}: {v}", flush=True)
        # marginals
        byj = Counter()
        for (a, c), v in joint.items():
            byj[c] += v
        print(f"  by j: {dict(sorted(byj.items()))}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
