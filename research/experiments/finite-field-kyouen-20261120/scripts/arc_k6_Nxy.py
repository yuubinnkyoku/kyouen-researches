"""DERIVING N_xy(n2): the last quantity in the k=6 formula.

MEASURED:
    q=5: N_xy = {2: 120, 3: 70},   total 190 = C(20,2)
    q=7: N_xy = {3: 504, 4: 357},  total 861 = C(42,2)

n2 is the number of 2-secant circles in the pencil through {x,y}, and
n1 = q+1-2*n2 is the number of tangent circles.

The two cases are n1 = 2 and n1 = 0.

WHY ONLY TWO VALUES?  The pencil through {x,y} is a set of q+1 circles
covering C.  The number of tangent circles n1 is the number of circles in
the pencil meeting C in exactly 1 point.  Since n0 = n2 and
2*n2 + n1 = q+1, n1 has the same parity as q+1.

For q odd, q+1 is even, so n1 is even.  The measured values are 2 and 0.

WHY n1 in {0, 2}?  A circle C' in the pencil is tangent to C at p iff
C' meets C only at p.  The set of tangent circles is related to the
"contact" structure.  Let me measure n1 directly and see whether it can be
0 or 2 only, or whether larger values appear for larger q.

Let me also compute N_xy for q=8 (even) to see the pattern.

Run:  python arc_k6_Nxy.py --q 5 7 8
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

        N_xy = Counter()
        n1_hist = Counter()
        for xy in itertools.combinations(outside, 2):
            pencil = circ_through_pair.get(tuple(sorted(xy)), [])
            n2 = n1 = 0
            for cj in pencil:
                if cj == ci:
                    continue
                cap = len(Bset & set(circles[cj]))
                if cap == 2:
                    n2 += 1
                elif cap == 1:
                    n1 += 1
            N_xy[n2] += 1
            n1_hist[n1] += 1

        row = {"q": q, "n": n, "b": b,
               "N_xy": {str(k): v for k, v in sorted(N_xy.items())},
               "n1_hist": {str(k): v for k, v in sorted(n1_hist.items())},
               "total": sum(N_xy.values()),
               "C(n-q-1,2)": comb(n - q - 1, 2)}
        rows.append(row)
        print(f"q={q}: n={n}, circle size {q+1}", flush=True)
        print(f"  N_xy (by n2) = {dict(sorted(N_xy.items()))}", flush=True)
        print(f"  n1 histogram = {dict(sorted(n1_hist.items()))}", flush=True)
        print(f"  total {sum(N_xy.values())} vs C(n-q-1,2) = "
              f"{comb(n-q-1,2)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
