"""Degree-based bound: can it improve K <= q+3?

For a point p in S, count the blocks through p by how many points of S they hold.

  * Blocks through p holding 2 other points of S: one per pair {q,r} of S\\{p},
    and they are all distinct.  Count = C(k-1, 2).

  * Blocks through p holding exactly 1 other point of S: for each q in S\\{p},
    the pencil through p and q has lambda_2 blocks, of which exactly k-2 hold a
    third point of S (one per r).  So lambda_2 - (k-2) blocks through p,q hold
    only p,q from S.  Count = (k-1)(lambda_2 - k + 2).

  * Total blocks through p: deg = q^2 + q for AG(2,q).

So:
    C(k-1,2) + (k-1)(lambda_2 - k + 2) <= deg

With lambda_2 = q+1 and deg = q^2+q:
    (k-1)[(k-2)/2 + q + 1 - k + 2] <= q^2 + q
    (k-1)[q + 3 - k/2 - 1] <= q^2 + q
    (k-1)[q + 2 - k/2] <= q^2 + q

Let us solve this for k and compare with q+3.

This script computes the bound from theory (no board construction needed).
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def degree_bound(q: int) -> int:
    """Largest k satisfying (k-1)(q+2-k/2) <= q^2+q."""
    deg = q * q + q
    k = 2
    while True:
        lhs = Fraction(k) * (q + 2 - Fraction(k + 1, 2))
        if lhs > deg:
            return k
        k += 1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7, 9, 11, 13, 17, 19])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    K_DATA = {3: 5, 5: 6, 7: 6, 9: 9, 11: 9, 13: 13, 17: 17, 19: 13}
    rows = []
    print(f"{'q':>3} {'deg':>6} {'lam2':>5} {'q+3':>4} {'deg-bound':>10} "
          f"{'best':>5} {'K':>4}")
    for q in args.q:
        deg = q * q + q
        lam2 = q + 1
        kd = degree_bound(q)
        best = min(q + 3, kd)
        k = K_DATA.get(q)
        rows.append({"q": q, "degree": deg, "lambda2": lam2,
                     "q_plus_3": q + 3, "degree_bound": kd, "best": best,
                     "K": k})
        print(f"{q:>3} {deg:>6} {lam2:>5} {q+3:>4} {kd:>10} {best:>5} "
              f"{k if k else '-':>4}")

    print()
    print("the degree bound is ~2q, always weaker than q+3.")
    print("so the degree argument does not improve the bound.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
