"""THE k=6 CLOSED FORM: derived from the second-circle distribution.

For q=5 the (C, T, xy) triples split by the number of SECOND circles that
meet T in exactly 2 points:

    0 second circles :  62400
    1 second circle  : 265200
    2 second circles :  42900
    -------------------------
    total            : 370500

Each 6-set with profile (4,) is counted once (its unique 4-circle).
Each 6-set with profile (4,4) is counted TWICE (once per 4-circle).
Each 6-set with profile (4,4,4) is counted THREE times.

Check:

    (4,)    = 62400 / 1 =  62400   matches the observed 62400
    (4,4)   = 265200 / 2 = 132600   matches the observed 132600
    (4,4,4) =  42900 / 3 =  14300   matches the observed  14300

So the profile counts are exactly the second-circle histogram divided by
the multiplicity.  This gives the k=6 closed form:

    #6-arcs = C(n,6) - b*C(q+1,6) - b*C(q+1,5)*(n-q-1)
                       - [N0 + N1/2 + N2/3]

where N_j = #{(C, T, {x,y}) : exactly j second circles meet T in 2 points}.

The remaining task is to compute N0, N1, N2 in closed form.  This script
does that by measuring them for several q and fitting.

Run:  python arc_k6_formula.py --q 5 7
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


def measure(q: int):
    F, ovoid, circles = build(q)
    n = len(ovoid)
    b = len(circles)
    circ_through_pair = {}
    for ci, B in enumerate(circles):
        for pair in itertools.combinations(B, 2):
            circ_through_pair.setdefault(pair, []).append(ci)

    dist = Counter()
    for ci, B in enumerate(circles):
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            for xy in itertools.combinations(outside, 2):
                cnt = 0
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    if len(Tset & set(circles[cj])) == 2:
                        cnt += 1
                dist[cnt] += 1
    return n, b, dist


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        n, b, dist = measure(q)
        total = sum(dist.values())
        # profile counts
        prof = {j: dist.get(j, 0) // (j + 1) for j in sorted(dist)}
        bad = (b * comb(q + 1, 6) + b * comb(q + 1, 5) * (n - q - 1)
               + sum(prof.values()))
        arcs = comb(n, 6) - bad
        row = {"q": q, "n": n, "b": b, "total_triples": total,
               "histogram": {str(k): v for k, v in sorted(dist.items())},
               "profile_counts": {str(k): v for k, v in sorted(prof.items())},
               "bad": bad, "arcs": arcs}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}", flush=True)
        print(f"  histogram {dict(sorted(dist.items()))}", flush=True)
        print(f"  profiles  {dict(sorted(prof.items()))}", flush=True)
        print(f"  bad={bad}, arcs={arcs}", flush=True)
        # normalise
        print(f"  N0/total={dist.get(0,0)/total:.6f}  "
              f"N1/total={dist.get(1,0)/total:.6f}  "
              f"N2/total={dist.get(2,0)/total:.6f}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
