"""The product is maximised at MAXIMUM area, not at small area.

Frontier data (det_frontier.py) shows:
  a=4: max product 64 at Area=8 = a^2/2 (the maximum possible area)
  a=5: max product 625/4 at Area=25/2 = a^2/2 (the maximum possible area)

So under the bounding-box condition, the product Area*R^2 is maximised when the
area is MAXIMAL, i.e. the triangle is the corner right triangle with legs a.

This is the opposite of the unconstrained case (where small area gave huge R^2).
The bounding-box condition kills the small-area / huge-R^2 configurations.

PROOF STRATEGY that now looks viable:

  (P1) Under the condition, Area <= a^2/2.  [trivial: triangle inside square]
  (P2) Under the condition, R^2 <= a^2/2.  [FALSE in general -- see det_step2]
  (P3) But the product is maximised at Area = a^2/2, where R^2 = a^2/2.

Since (P2) is false, we need a coupled statement.  Let us test the following
CONJECTURE, which would suffice:

    CONJECTURE (monotone trade-off):
        Area * R^2 <= (a^2/2) * (a^2/2) = a^4/4
    and moreover the function Area -> max R^2 is such that the product is
    maximised at the largest Area.

This script verifies the monotonicity claim: is the product non-decreasing in
Area along the frontier?  If yes, the bound reduces to checking the maximum-area
triangle, which is the corner right triangle, giving a^4/4.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[4, 5, 6, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        vecs = [(dx, dy) for dx in range(-a, a + 1) for dy in range(-a, a + 1)
                if (dx, dy) != (0, 0)]
        frontier: dict[Fraction, Fraction] = {}
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
                if area not in frontier or R2 > frontier[area]:
                    frontier[area] = R2
        items = sorted(frontier.items())
        products = [(ar, ar * r2) for ar, r2 in items]
        # is the product non-decreasing in area?
        monotone = all(products[i][1] <= products[i + 1][1]
                       for i in range(len(products) - 1))
        # where is the max product?
        max_prod = max(p for _, p in products)
        max_area = max(ar for ar, p in products if p == max_prod)
        max_possible_area = Fraction(a * a, 2)
        report.append({
            "a": a,
            "frontier_points": len(items),
            "product_monotone_in_area": monotone,
            "max_product": str(max_prod),
            "max_product_at_area": str(max_area),
            "max_possible_area": str(max_possible_area),
            "max_at_max_area": max_area == max_possible_area,
            "bound": str(Fraction(a ** 4, 4)),
            "at_bound": max_prod == Fraction(a ** 4, 4),
        })
        print(f"a={a}: product monotone in Area: {monotone}  "
              f"max product {max_prod} at Area={max_area} "
              f"(max possible Area={max_possible_area})  "
              f"{'AT BOUND' if max_prod == Fraction(a**4,4) else 'below'}", flush=True)
        if not monotone:
            # show where it decreases
            for i in range(len(products) - 1):
                if products[i][1] > products[i + 1][1]:
                    print(f"   decrease at Area={products[i][0]} -> {products[i+1][0]}: "
                          f"{products[i][1]} -> {products[i+1][1]}", flush=True)
                    break

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
