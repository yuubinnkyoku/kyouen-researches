"""N_xy(n2): the structure across q, including the even case.

MEASURED:
    q=5: n1 histogram {0: 70, 2: 120},   N_xy {2:120, 3:70}
    q=7: n1 histogram {0: 357, 2: 504},  N_xy {3:504, 4:357}
    q=8: n1 histogram {1: 1512, 9: 28},  N_xy {0:28, 4:1512}

For q odd the two cases are n1 = 0 and n1 = 2.
For q = 8 (even) the cases are n1 = 1 and n1 = 9 = q+1.

The n1 = q+1 case means EVERY circle in the pencil is tangent to C, i.e.
the pencil is the "tangent pencil" at a point.  That happens when {x,y}
lies on a circle tangent to C at some point... more precisely when the
line/circle through x,y is tangent.

Let me identify the special pairs.

For q=8: 28 pairs give n1 = 9.  Note 28 = C(8,2) = C(q,2).  And
q=5: 70 = ?  C(6,2)=15, no.  70 = C(8,4)?  Let me check: 70 = C(8,4).
q=7: 357 = ?  357 = 21*17 = C(7,2)*17.  Hmm.

Let me look at the special pairs geometrically: they are the pairs {x,y}
such that the circle through x,y is tangent to C.  In the inversive plane,
"the circle through x,y tangent to C" -- there are 2 such circles in
general (through 2 points, tangent to a given circle).

Let me just measure which pairs are special and characterise them.

Run:  python arc_k6_special.py --q 5 7 8
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
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7, 8])
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

        # classify pairs by n1
        by_n1 = {}
        for xy in itertools.combinations(outside, 2):
            pencil = circ_through_pair.get(tuple(sorted(xy)), [])
            n1 = 0
            for cj in pencil:
                if cj == ci:
                    continue
                if len(Bset & set(circles[cj])) == 1:
                    n1 += 1
            by_n1.setdefault(n1, []).append(xy)

        row = {"q": q, "n": n, "b": b,
               "n1_classes": {str(k): len(v) for k, v in
                              sorted(by_n1.items())}}
        rows.append(row)
        print(f"q={q}: n={n}, circle size {q+1}", flush=True)
        for n1, lst in sorted(by_n1.items()):
            print(f"  n1={n1}: {len(lst)} pairs", flush=True)
            # are these pairs "special"?  check if they lie on a circle
            # tangent to C
            print(f"    sample: {lst[:3]}", flush=True)
        # check: for the extreme class, is the pair on a tangent circle?
        for n1, lst in sorted(by_n1.items()):
            if n1 == q + 1:
                print(f"  n1=q+1 class: the whole pencil is tangent to C",
                      flush=True)
                # count circles tangent to C through each point
                print(f"    {len(lst)} pairs, C(q,2)={comb(q,2)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
