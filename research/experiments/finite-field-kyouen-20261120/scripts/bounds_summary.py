"""Summary of all upper bounds and their sharpness.

This script consolidates the bounds we have proved and measures their sharpness
against the known K values.

Bounds (all proved):
  (T) triple:      C(k,3) <= b,  b = q^3 + q
  (L) lambda_2:    k <= lambda_2 + 2 = q + 3        [unconditional]
  (C) cross:       k <= q + 2                        [q = 1 mod 4 only]

Known K values:
  AG(2,q): q=3:5, 4:5, 5:6, 7:6, 8:8, 9:9, 11:9, 13:>=13, 16:>=12, 17:>=17, 19:>=13
  inversive: q=3:5, 4:5, 5:6, 7:6, 8:7, 9:9, 11:9, 13:10, 16:>=11

Let me tabulate the bounds and the gaps.
"""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path


AG = {3: (5, True), 4: (5, True), 5: (6, True), 7: (6, True), 8: (8, True),
      9: (9, True), 11: (9, True), 13: (13, False), 16: (12, False),
      17: (17, False), 19: (13, False)}
INV = {3: (5, True), 4: (5, True), 5: (6, True), 7: (6, True), 8: (7, True),
       9: (9, True), 11: (9, True), 13: (10, True), 16: (11, False)}


def triple_bound(q: int) -> int:
    b = q ** 3 + q
    k = 3
    while comb(k + 1, 3) <= b:
        k += 1
    return k


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    print("AG(2,q):")
    print(f"{'q':>3} {'mod4':>5} {'K':>4} {'ex':>3} {'triple':>7} {'lam2':>5} "
          f"{'cross':>6} {'best':>5} {'gap':>4}")
    for q in sorted(AG):
        k, exact = AG[q]
        tb = triple_bound(q)
        lb = q + 3
        cb = q + 2 if q % 4 == 1 else None
        best = min(x for x in (tb, lb, cb) if x is not None)
        rows.append({"board": "AG", "q": q, "K": k, "exact": exact,
                     "triple": tb, "lambda2": lb, "cross": cb, "best": best,
                     "gap": best - k})
        print(f"{q:>3} {q%4:>5} {k:>4} {'Y' if exact else 'n':>3} {tb:>7} "
              f"{lb:>5} {cb if cb else '-':>6} {best:>5} {best-k:>4}")

    print()
    print("inversive plane:")
    print(f"{'q':>3} {'K':>4} {'ex':>3} {'triple':>7} {'lam2':>5} {'best':>5} {'gap':>4}")
    for q in sorted(INV):
        k, exact = INV[q]
        tb = triple_bound(q)
        lb = q + 3
        best = min(tb, lb)
        rows.append({"board": "inv", "q": q, "K": k, "exact": exact,
                     "triple": tb, "lambda2": lb, "cross": None, "best": best,
                     "gap": best - k})
        print(f"{q:>3} {k:>4} {'Y' if exact else 'n':>3} {tb:>7} {lb:>5} "
              f"{best:>5} {best-k:>4}")

    print()
    print("the lambda_2 bound q+3 is the best general bound;")
    print("the cross bound q+2 is slightly better for q = 1 mod 4.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
