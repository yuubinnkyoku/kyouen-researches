"""Attempt (B): for non-maximal area, Area * R^2 < a^4/4.

Setup.  u, v integer vectors, c = |u x v|, n1=|u|^2, n2=|v|^2, n3=|u-v|^2.
    Area = c/2
    R^2  = n1 n2 n3 / (4 c^2)
    Area * R^2 = n1 n2 n3 / (8c)

The bounding-box condition: {0, u, v, O} fits in an a x a square, where
    O = ((n1 v_y - n2 u_y)/(2c'), (n2 u_x - n1 v_x)/(2c'))   with c' = u x v (signed).

KEY IDEA for (B).  The condition that O lies within distance a of the other
points gives a lower bound on c in terms of the side lengths.  Specifically,
since O is the circumcentre, |O - 0| = R, |O - u| = R, |O - v| = R.  If all four
points fit in an a x a square, then the DIAMETER of the set {0,u,v,O} is at most
a*sqrt(2).  In particular R = |O| <= a*sqrt(2), so R^2 <= 2a^2.

That is weak.  But we also know the triangle's circumradius satisfies
    R >= (longest side)/2.
And the longest side is at most a*sqrt(2).

Better: use the formula  Area = (1/2)|u||v| sin(theta)  and  R = |u-v|/(2 sin(theta))
where theta is the angle at the vertex opposite to side |u-v|.  Then

    Area * R^2 = (1/2)|u||v| sin(theta) * |u-v|^2/(4 sin^2(theta))
               = |u||v||u-v|^2 / (8 sin(theta)).

Since sin(theta) >= 2*Area/(|u||v|) ... circular.

Let us instead do a DIRECT numeric study: for each a, compute the maximum of
Area*R^2 subject to the bounding-box condition, and record the gap from a^4/4
as a function of the "area deficit" a^2/2 - Area.  If the gap grows linearly
in the deficit, that suggests a proof by a linear inequality.

This script measures that relation.
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
        # for each area, the max product
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
                prod = area * R2
                if area not in frontier or prod > frontier[area]:
                    frontier[area] = prod
        items = sorted(frontier.items())
        # gap = bound - product, deficit = max_area - area
        rows = []
        for area, prod in items:
            gap = bound - prod
            deficit = max_area - area
            rows.append((deficit, gap, area, prod))
        # check: is gap >= deficit * something?  Report the ratio gap/deficit
        ratios = []
        for deficit, gap, area, prod in rows:
            if deficit > 0:
                ratios.append((deficit, gap, gap / deficit))
        report.append({
            "a": a,
            "bound": str(bound),
            "max_area": str(max_area),
            "frontier": [[str(ar), str(pr)] for ar, pr in items],
            "gap_over_deficit": [[str(d), str(g), str(r)] for d, g, r in ratios],
        })
        print(f"a={a}: bound {bound}, max area {max_area}", flush=True)
        print(f"   deficit -> gap (gap = bound - product):", flush=True)
        for deficit, gap, area, prod in rows[:10]:
            print(f"      deficit={deficit}: gap={gap}  (area={area}, product={prod})",
                  flush=True)
        if ratios:
            min_ratio = min(r for _, _, r in ratios)
            print(f"   min gap/deficit ratio = {min_ratio}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
