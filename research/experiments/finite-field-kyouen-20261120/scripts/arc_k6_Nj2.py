"""CLOSED FORM FOR N_j VIA THE MEET HISTOGRAM.

For q=5 the histogram of |T ∩ C'| over all (C, T, {x,y}, C') is

    |T ∩ C'| = 0 : 1,092,000
    |T ∩ C'| = 1 :   780,000
    |T ∩ C'| = 2 :   351,000
    -------------------------
    total        : 2,223,000

Note 2,223,000 = 370,500 * 6 = total_triples * (q+1), since each pair
{x,y} lies on exactly q+1 circles.  Check: 370500*6 = 2,223,000.  YES.

So the average number of second circles meeting T in 2 points is

    N1 + 2*N2 = 265200 + 2*42900 = 351000

which is exactly the |T ∩ C'| = 2 count.  Consistent.

NOW: can we get the counts in closed form?

For a fixed circle C and 4-subset T of C, and a fixed pair {x,y} outside C,
the q+1 circles through x,y each meet C in 0, 1 or 2 points.  Since C has
q+1 points and the pencil through x,y is a partition-like structure, the
counts should be determined by q alone.

Let me compute, for a FIXED (C, T), the distribution over {x,y} of
|{C' in pencil(x,y) : |T ∩ C'| = 2}|, and see whether it depends only on q.

Run:  python arc_k6_Nj2.py --q 5 7
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
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

        # For each (C, T) record the distribution over {x,y}
        per_CT = []
        for ci, B in enumerate(circles):
            Bset = set(B)
            outside = [p for p in range(n) if p not in Bset]
            for T in itertools.combinations(B, 4):
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
                per_CT.append(tuple(sorted(d.items())))

        # how many distinct distributions appear?
        uniq = Counter(per_CT)
        row = {"q": q, "n": n, "b": b,
               "distinct_distributions": len(uniq),
               "top": {str(k): v for k, v in uniq.most_common(5)}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, {len(per_CT)} (C,T) pairs", flush=True)
        print(f"  distinct per-(C,T) distributions: {len(uniq)}", flush=True)
        for k, v in uniq.most_common(5):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
