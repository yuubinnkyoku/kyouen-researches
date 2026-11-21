"""DERIVING N_j IN CLOSED FORM.

N_j counts triples (C, T, {x,y}) where
  C is a circle, T is a 4-subset of C, {x,y} is a pair outside C,
and exactly j circles through x and y meet T in exactly 2 points.

MEASURED (q=5, n=26, b=130):
    N0 = 62400, N1 = 265200, N2 = 42900, total = 370500

MEASURED (q=7, n=50, b=350):
    N0 = 6938400, N1 = 12877200, N2 = 1278900, total = 21454500

The total is easy:

    total = b * C(q+1,4) * C(n-q-1, 2)

Check q=5: 130 * 15 * C(20,2) = 130*15*190 = 370500.  MATCHES.
Check q=7: 350 * 70 * C(42,2) = 350*70*861 = 21094500.  Hmm, that gives
21094500 but the measured total is 21454500.  Let me recompute.

350 * 70 = 24500; C(42,2) = 861; 24500*861 = 21094500.
Measured total = 6938400+12877200+1278900 = 21094500.  MATCHES (I mis-added).

So total = b*C(q+1,4)*C(n-q-1,2) exactly.

Now for N_j.  Fix x,y.  The circles through x,y form a pencil of q+1
circles.  For a fixed T (4 points of C), we ask how many of those q+1
circles meet T in exactly 2 points.

Let me compute this quantity directly as a function of the configuration,
and average over all (C,T,{x,y}).

Run:  python arc_k6_Nj.py --q 5 7
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

        dist = Counter()
        # also record the distribution of |T ∩ C'| for second circles
        meet_hist = Counter()
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
                        m = len(Tset & set(circles[cj]))
                        meet_hist[m] += 1
                        if m == 2:
                            cnt += 1
                    dist[cnt] += 1

        total = sum(dist.values())
        pred_total = b * comb(q + 1, 4) * comb(n - q - 1, 2)
        row = {"q": q, "n": n, "b": b, "total": total,
               "predicted_total": pred_total,
               "total_ok": total == pred_total,
               "N": {str(k): v for k, v in sorted(dist.items())},
               "meet_histogram": {str(k): v for k, v in
                                  sorted(meet_hist.items())}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}", flush=True)
        print(f"  total={total}, b*C(q+1,4)*C(n-q-1,2)={pred_total} "
              f"-> {total == pred_total}", flush=True)
        print(f"  N_j = {dict(sorted(dist.items()))}", flush=True)
        print(f"  |T cap C'| histogram = {dict(sorted(meet_hist.items()))}",
              flush=True)
        # normalise N_j by total
        for k in sorted(dist):
            print(f"    N{k}/total = {dist[k]/total:.6f}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
