"""CLOSED FORM FOR THE MEET HISTOGRAM.

MEASURED (T = any 4-subset of a circle C):

    q=5:  meet = {0: 560, 1: 400, 2: 180},  total 1140 = C(20,2)*6
    q=7:  meet = {0: 4074, 1: 2184, 2: 630}, total 6888 = C(42,2)*8

The total is exactly C(n-q-1, 2) * (q+1): every pair {x,y} outside C lies
on q+1 circles, and each such circle meets T in 0, 1 or 2 points.

Now derive the per-m counts.

Fix p in T (4 choices).  Count pairs ({x,y}, C') with p in C', x,y in C',
x,y outside C, and C' != C.

C' passes through p, and C' meets C in at most 2 points, so C' meets C in
exactly {p, p'} for some p' in C \ {p} (q choices) -- OR C' meets C only in
p (tangent-like), which in the inversive plane means C' is the unique
circle through p and {x,y} that touches C at p.  Since two circles meet in
0, 1 or 2 points, and here they share p, they meet in 1 or 2 points.

Case 2 points: C' through p, p' (q choices of p'), C' != C.  The circles
through p and p' number q+1; one is C, so q others.  For each, {x,y} must
be 2 points of C' outside C: C(q-1, 2) choices.

    contribution = 4 * q * q * C(q-1, 2)

Check q=5: 4*5*5*6 = 600.  But the total is 1140, so there is a second
case.

Case 1 point (tangent): C' meets C only in p.  Then C' contains p and
{x,y}, with x,y outside C.  The number of such C' for fixed p and {x,y}:
the circle through p,x,y is unique, and it meets C in p plus possibly one
more point.  "Meets C only in p" is a tangency condition.

Let me count the 1-point case by subtraction: total - 2-point case.

    q=5: 1140 - 600 = 540
    q=7: 6888 - 2940 = 3948

Hmm, but the meet histogram counts |T ∩ C'|, and a C' meeting C in 2 points
both in T contributes 2, while meeting in 1 point in T contributes 1.

Let me just compute the three counts directly and fit.

Run:  python arc_k6_meet2.py --q 5 7
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
        T = tuple(B[:4])
        Tset = set(T)

        # classify each (xy, C') by |C' cap C| and |T cap C'|
        joint = Counter()
        for xy in itertools.combinations(outside, 2):
            for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                if cj == ci:
                    continue
                capC = len(Bset & set(circles[cj]))
                capT = len(Tset & set(circles[cj]))
                joint[(capC, capT)] += 1

        row = {"q": q, "n": n, "b": b,
               "joint": {f"{a},{c}": v for (a, c), v in sorted(joint.items())}}
        rows.append(row)
        print(f"q={q}: n={n}, circle size {q+1}", flush=True)
        print(f"  (|C' cap C|, |T cap C'|) -> count", flush=True)
        for (a, c), v in sorted(joint.items()):
            print(f"    ({a},{c}): {v}", flush=True)
        # marginals
        by_capC = Counter()
        by_capT = Counter()
        for (a, c), v in joint.items():
            by_capC[a] += v
            by_capT[c] += v
        print(f"  by |C' cap C|: {dict(sorted(by_capC.items()))}", flush=True)
        print(f"  by |T cap C'|: {dict(sorted(by_capT.items()))}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
