"""k=7: the (5,*) family is EXACTLY the k=6 machinery with |T| = 5.

VERIFIED (q=5, n=26, b=130, s=6):

    per (C,T) with |T|=5:  j=1 -> 480,  j=2 -> 660   (j=0 never occurs)
    times b = 130:         j=1 -> 62400, j=2 -> 85800

and the measured profile counts are

    (5,4)   = 62400   <- j=1
    (5,4,4) = 85800   <- j=2

EXACT MATCH.

So the (5,*) family is governed by the SAME pencil involution as k=6,
with T of size 5 instead of 4:

    H(n2, n1, j, k) = sum_a C(n2,j)*C(n2-j,a)*2^a*C(n1, k-2j-a)

and

    (5,4)   = b * sum_{n2} N_xy(n2) * H(n2,n1,1,5)
    (5,4,4) = b * sum_{n2} N_xy(n2) * H(n2,n1,2,5)

Note j=0 is impossible for |T|=5: an involution with n2 pairs on s points
always has at least one pair meeting a 5-subset in 2 points (since
5 > n1 = s-2n2 in both cases: q=5 gives n1=2 or 0, and 5 > 2).

Let me verify the closed form numerically and then handle the (4,*) family,
which is the genuinely new part of k=7.

Run:  python arc_k7_five2.py --q 5
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
from arc_k6_pure import N_xy  # noqa: E402


def H(n2, n1, j, k):
    total = 0
    for a in range(0, n2 - j + 1):
        used = 2 * j + a
        if used > k:
            break
        rest = k - used
        if rest < 0 or rest > n1:
            continue
        total += comb(n2, j) * comb(n2 - j, a) * (2 ** a) * comb(n1, rest)
    return total


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

        pred = {}
        for n2, cnt in N_xy(q).items():
            n1 = s - 2 * n2
            for j in (0, 1, 2):
                pred[j] = pred.get(j, 0) + b * cnt * H(n2, n1, j, 5)

        row = {"q": q, "n": n, "b": b, "s": s,
               "predicted_5star": pred}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  predicted (5,*) by j: {pred}", flush=True)
        print(f"  => (5,4) = {pred.get(1,0)}, (5,4,4) = {pred.get(2,0)}",
              flush=True)
        print(f"  measured: (5,4) = 62400, (5,4,4) = 85800", flush=True)
        print(f"  match: {pred.get(1,0) == 62400 and pred.get(2,0) == 85800}",
              flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
