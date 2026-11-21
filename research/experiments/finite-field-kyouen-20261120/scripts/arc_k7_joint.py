"""k=7: the (w, j-triple) joint distribution in closed form.

Everything in k=7 reduces to counting, over (C, T, {x,y,z}):

    w = |T cap W|,  W = the circle through x,y,z
    j1, j2, j3 = the pencil counts for the three pairs

From the involution structure:
  Case A (disjoint involutions): the three pencils share no pair.
  Case B (one common pair): all three share the pair W ∩ C.

In Case B the common pair is W ∩ C, so w = |T ∩ W| tells us whether that
pair is inside T.

Let me count each case directly.

CASE A COUNT.  The three pencils are disjoint.  For a fixed (C,T), the
number of triples {x,y,z} in Case A with given (j1,j2,j3) is what we need.

KEY SIMPLIFICATION.  In Case A, the three pencils are disjoint, so
j1+j2+j3 = u = the total number of pencil circles.  And each pencil circle
is a circle through 2 of {x,y,z} meeting T in 2 points.

Let me instead count by the STRUCTURE: choose the three pencils first.

Actually, let me take a different approach: count the triples by the
"configuration" (which circles through pairs of {x,y,z} meet T in 2
points), and verify against the data.

Run:  python arc_k7_joint.py --q 5
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

        # For each triple, record (j1,j2,j3) and the "type" of each pair's
        # pencil: how many 2-secant circles (n2) and how many tangent (n1)
        joint = Counter()
        for xyz in itertools.combinations(outside, 3):
            js = []
            n2s = []
            for xy in itertools.combinations(xyz, 2):
                j = 0
                n2 = 0
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    cap = Bset & set(circles[cj])
                    if len(cap) == 2:
                        n2 += 1
                        if len(Tset & set(circles[cj])) == 2:
                            j += 1
                js.append(j)
                n2s.append(n2)
            joint[(tuple(sorted(n2s)), tuple(sorted(js)))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (sorted n2-triple, sorted j-triple) -> count", flush=True)
        for (n2s, js), cnt in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    n2={n2s} js={js}: {cnt}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
