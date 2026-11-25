"""THE TANGENT CASE: |C' cap C| = 1.

MEASURED:
    q=5: (1,0)=80,  (1,1)=160   (sum 240)
    q=7: (1,0)=504, (1,1)=504   (sum 1008)

The sum is the number of (xy, C') with C' meeting C in exactly 1 point.

DERIVATION OF THE SUM.  Fix p in C.  A circle C' meeting C only at p is
TANGENT to C at p.  In the inversive plane, the circles through p form a
pencil; the ones tangent to C at p are all the circles through p that
share the tangent direction.

Actually in the inversive plane there is no "tangent direction" -- two
circles meet in 0, 1 or 2 points, and "1 point" means tangent.  For each
p in C, how many circles through p are tangent to C at p?

The circles through p number q(q+1) (the pencil).  Of these, q+1 meet C in
a second point... no: the circles through p that ALSO pass through another
point of C are the ones meeting C in 2 points.  For each of the q other
points p' of C, there are q circles through p,p' other than C.  So
q * q = q^2 circles meet C in 2 points (through p).  The remaining
q(q+1) - q^2 = q circles are tangent at p.

So there are exactly q tangent circles at each p.  []

Now count (xy, C') with C' tangent to C at p in T:
    p in T (4 choices) x q tangent circles x C(q-1,2) pairs {x,y}
    = 4*q*C(q-1,2)

Check q=5: 4*5*6 = 120.  But (1,1) = 160.  Doesn't match.

Hmm.  The issue: {x,y} must be outside C, and for a tangent circle C' at p,
C' meets C only at p, so C' has q points outside C, giving C(q,2) pairs,
not C(q-1,2).

    (1,1) = 4 * q * C(q,2)
    q=5: 4*5*10 = 200.  Still not 160.

Let me just measure the tangent-circle count directly.

Run:  python arc_k6_tangent.py --q 5 7
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

        # for each p in C, count circles through p meeting C only at p
        tangent = Counter()
        for p in B:
            cnt = 0
            for cj, BB in enumerate(circles):
                if cj == ci:
                    continue
                if p not in BB:
                    continue
                if len(Bset & set(BB)) == 1:
                    cnt += 1
            tangent[p] = cnt

        # for each T (4-subset), count (xy, C') with C' tangent at a point of T
        T = tuple(B[:4])
        Tset = set(T)
        tcount = Counter()
        for xy in itertools.combinations(outside, 2):
            for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                if cj == ci:
                    continue
                capC = len(Bset & set(circles[cj]))
                if capC != 1:
                    continue
                capT = len(Tset & set(circles[cj]))
                tcount[capT] += 1

        row = {"q": q, "n": n, "b": b,
               "tangent_per_point": dict(sorted(tangent.items())),
               "tangent_counts": dict(sorted(tcount.items()))}
        rows.append(row)
        print(f"q={q}: n={n}, circle size {q+1}", flush=True)
        print(f"  tangent circles per point of C: "
              f"{sorted(set(tangent.values()))} (q={q})", flush=True)
        print(f"  (xy,C') with C' tangent, by |T cap C'|: "
              f"{dict(sorted(tcount.items()))}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
