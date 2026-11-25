"""The gap grows at least linearly in the area deficit -- a route to (B).

Data (det_gap_deficit.py):
  a=4: min ratio gap/deficit = 7/2
  a=5: min ratio gap/deficit = 25/6

So  bound - product >= k * (max_area - area)  with k roughly a^2/6.

If we can prove a linear inequality of the form

    Area * R^2 <= a^4/4 - k*(a^2/2 - Area)

for some k > 0, then (B) follows immediately (since the RHS is < a^4/4 whenever
Area < a^2/2).

Equivalently

    Area * R^2 + k*Area <= a^4/4 + k*a^2/2
    Area * (R^2 + k) <= a^4/4 + k*a^2/2

This script tests whether a clean k exists, e.g. k = a^2/6 or k = 1.

Actually a cleaner formulation: test whether

    Area * R^2 <= (a^2/2) * (a^2/2) * (Area/(a^2/2))^t

for some exponent t, i.e. whether the product is bounded by a power of the
area ratio.  If t = 1, the product is linear in Area, which would give
Area*R^2 <= (a^2/2)*Area, and at Area = a^2/2 that is a^4/4.

Let us test: is  R^2 <= a^2/2  whenever Area = a^2/2?  (yes, the corner triangle)
and more generally  R^2 <= a^2/2 * (a^2/2)/Area?  i.e.  Area*R^2 <= a^4/4.

That is just the target.  So instead test the LINEAR-IN-AREA conjecture:

    CONJECTURE L:  R^2 <= a^2/2  for ALL fitting triangles.
    (This is STEP2, which we already refuted.)

So we need the product form.  Let us test the specific inequality

    Area * R^2 <= a^4/4 - (a^2/2 - Area) * c_a

and find the largest valid c_a for each a.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[4, 5, 6, 7, 8])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        vecs = [(dx, dy) for dx in range(-a, a + 1) for dy in range(-a, a + 1)
                if (dx, dy) != (0, 0)]
        bound = Fraction(a ** 4, 4)
        max_area = Fraction(a * a, 2)
        best_c = None
        for u in vecs:
            for v in vecs:
                cc = u[0] * v[1] - u[1] * v[0]
                if cc == 0:
                    continue
                c = abs(cc)
                n1 = u[0] ** 2 + u[1] ** 2
                n2 = v[0] ** 2 + v[1] ** 2
                w = (u[0] - v[0], u[1] - v[1])
                n3 = w[0] ** 2 + w[1] ** 2
                Ox = Fraction(n1 * v[1] - n2 * u[1], 2 * cc)
                Oy = Fraction(n2 * u[0] - n1 * v[0], 2 * cc)
                xs = [Fraction(0), Fraction(u[0]), Fraction(v[0]), Ox]
                ys = [Fraction(0), Fraction(u[1]), Fraction(v[1]), Oy]
                if max(xs) - min(xs) > a or max(ys) - min(ys) > a:
                    continue
                area = Fraction(c, 2)
                R2 = Fraction(n1 * n2 * n3, 4 * c * c)
                prod = area * R2
                deficit = max_area - area
                if deficit > 0:
                    c_needed = (bound - prod) / deficit
                    if best_c is None or c_needed < best_c:
                        best_c = c_needed
        report.append({
            "a": a,
            "bound": str(bound),
            "max_area": str(max_area),
            "largest_valid_c": str(best_c) if best_c is not None else None,
            "c_over_a2": str(best_c / (a * a)) if best_c is not None else None,
        })
        print(f"a={a}: largest c with Area*R^2 <= a^4/4 - c*(a^2/2 - Area) "
              f"is c = {best_c}  (c/a^2 = {best_c/(a*a) if best_c else None})",
              flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
