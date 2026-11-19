"""Cross blocks in AG(2,q) for q = 1 mod 4: a general upper bound on K.

When -1 is a square in F_q (i.e. q = 1 mod 4), the form x^2+y^2 factors as
(x+iy)(x-iy) with i^2 = -1.  In the split coordinates

    s = x + i y,   t = x - i y

the circle equation x^2+y^2+Dx+Ey+F = 0 becomes

    s t + a s + b t + c = 0

and the DEGENERATE members (those that factor as (s+a)(t+b) = 0) are exactly
"column c union row r": the set of points with s = -a or t = -b.

Such a cross has 2q - 1 points.  A safe set meets each cross in at most 3 points.
Summing the q^2 cross constraints gives

    q * sum_c a_c + q * sum_r b_r - |S| <= 3 q^2
    2q|S| - |S| <= 3q^2
    (2q-1)|S| <= 3q^2
    |S| <= 3q^2/(2q-1)  ~  3q/2

This is a general upper bound for q = 1 mod 4.

This script:
  1. builds AG(2,q) for q = 5, 9, 13 (all = 1 mod 4),
  2. identifies the cross blocks (size 2q-1) and verifies there are q^2 of them,
  3. computes the resulting bound 3q^2/(2q-1),
  4. compares with the known/estimated K.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from ag2_prime_power import build_ag


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[5, 9, 13])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        sizes = Counter(len(b) for b in blocks)
        cross_size = 2 * q - 1
        n_cross = sizes.get(cross_size, 0)
        # general bound
        bound = Fraction(3 * q * q, 2 * q - 1)
        floor_bound = bound.numerator // bound.denominator
        report.append({
            "q": q,
            "q_mod_4": q % 4,
            "points": len(pts),
            "blocks": len(blocks),
            "block_sizes": dict(sorted(sizes.items())),
            "cross_size": cross_size,
            "n_cross": n_cross,
            "expected_cross": q * q,
            "cross_count_ok": n_cross == q * q,
            "bound_3q2_over_2q_minus_1": str(bound),
            "K_upper": floor_bound,
        })
        print(f"q={q} (mod4={q % 4}): {len(pts)} points, {len(blocks)} blocks, "
              f"sizes={dict(sorted(sizes.items()))}", flush=True)
        print(f"   cross blocks (size {cross_size}): {n_cross} "
              f"(expected q^2={q*q})  {'OK' if n_cross == q*q else 'MISMATCH'}",
              flush=True)
        print(f"   general bound: K <= 3q^2/(2q-1) = {bound} -> K <= {floor_bound}",
              flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
