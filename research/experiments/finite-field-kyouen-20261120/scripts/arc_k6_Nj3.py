"""N_j HAS A CLOSED FORM: the per-(C,T) distribution is uniform.

MEASURED (q=5): for EVERY one of the 1950 (C,T) pairs, the distribution of
the number of second circles over the C(n-q-1,2) = 190 pairs {x,y} is

    0 second circles :  32
    1 second circle  : 136
    2 second circles :  22
    ----------------------
    total            : 190

So N_j = b * C(q+1,4) * (that count):

    N0 = 130 * 15 * 32  =  62400   (measured 62400)  OK
    N1 = 130 * 15 * 136 = 265200   (measured 265200) OK
    N2 = 130 * 15 * 22  =  42900   (measured 42900)  OK

So the whole k=6 count reduces to the three integers (32, 136, 22), which
depend only on q.

WHY UNIFORM?  The inversive plane is 3-transitive and its automorphism
group acts transitively on (circle, 4-subset) pairs.  So the distribution
is the same for every (C,T).  []

NOW: what are (32, 136, 22) as functions of q?

For q=5: 32, 136, 22, total 190 = C(20,2).
Let me get q=7 and q=8 and fit.

Run:  python arc_k6_Nj3.py --q 5 7
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
        circ_through_pair = {}
        for ci, B in enumerate(circles):
            for pair in itertools.combinations(B, 2):
                circ_through_pair.setdefault(pair, []).append(ci)

        # take ONE (C,T) and compute the distribution (uniform, so one suffices)
        ci = 0
        B = circles[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]
        T = tuple(B[:4])
        Tset = set(T)
        d = Counter()
        for xy in itertools.combinations(outside, 2):
            cnt = 0
            for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                if cj == ci:
                    continue
                if len(Tset & set(circles[cj])) == 2:
                    cnt += 1
            d[cnt] += 1

        total = sum(d.values())
        row = {"q": q, "n": n, "b": b, "pairs_xy": total,
               "distribution": {str(k): v for k, v in sorted(d.items())},
               "N0": b * comb(q + 1, 4) * d.get(0, 0),
               "N1": b * comb(q + 1, 4) * d.get(1, 0),
               "N2": b * comb(q + 1, 4) * d.get(2, 0)}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, C(n-q-1,2)={total}", flush=True)
        print(f"  per-(C,T) distribution: {dict(sorted(d.items()))}",
              flush=True)
        print(f"  N0={row['N0']}, N1={row['N1']}, N2={row['N2']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
