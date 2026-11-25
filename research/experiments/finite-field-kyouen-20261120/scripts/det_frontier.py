"""Find the exact trade-off curve under the bounding-box condition.

The AM-GM key (Area + R^2 <= a^2) FAILS, yet Area*R^2 <= a^4/4 holds.
So the constraint is not on the sum but on the product.

Let us look at the actual feasible region.  For each fitting triangle compute
(Area, R^2) and plot/measure the Pareto frontier: for each value of Area, what
is the maximum R^2?

If the frontier satisfies  R^2 <= a^4/(4*Area)  then the product bound holds.

This script computes the frontier exactly (as a step function) and reports it.
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
        bound = Fraction(a ** 4, 4)
        # frontier: for each area, max R^2
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
        # check the product bound on the frontier
        violations = 0
        worst = Fraction(0)
        worst_area = None
        for area, R2 in frontier.items():
            prod = area * R2
            if prod > bound:
                violations += 1
            if prod > worst:
                worst, worst_area = prod, area
        # report the frontier sorted by area
        items = sorted(frontier.items())
        report.append({
            "a": a,
            "bound": str(bound),
            "frontier_points": len(items),
            "violations": violations,
            "max_product": str(worst),
            "max_product_area": str(worst_area) if worst_area else None,
            "frontier": [[str(ar), str(r2)] for ar, r2 in items],
        })
        print(f"a={a}: frontier has {len(items)} points, "
              f"violations {violations}, max product {worst} "
              f"(at Area={worst_area})", flush=True)
        print(f"   frontier (Area -> max R^2):", flush=True)
        for ar, r2 in items[:12]:
            print(f"      Area={ar}: R^2={r2}  product={ar*r2}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
