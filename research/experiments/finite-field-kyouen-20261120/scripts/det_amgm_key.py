"""Extend the bounding-box verification to larger a, and look for the proof key.

We have: for integer vectors u,v with c = |u x v| != 0, the circumcentre is

    O = ((n1*v_y - n2*u_y)/(2c), (n2*u_x - n1*v_x)/(2c))

and the condition that {0, u, v, O} fits in an a x a square is

    max(0, u_x, v_x, O_x) - min(0, u_x, v_x, O_x) <= a
    max(0, u_y, v_y, O_y) - min(0, u_y, v_y, O_y) <= a

Under this condition we observed max Area*R^2 = a^4/4 exactly (a <= 7).

This script pushes to larger a (8, 9, 10) to confirm, and reports the extremal
configuration.  It also tests a candidate PROOF KEY:

    KEY:  if the four points {0,u,v,O} fit in an a x a square, then
          Area <= a^2/2  and  R^2 <= a^2/2  cannot both be near their maxima
          unless the triangle is the corner right triangle.

Concretely, test whether  Area + R^2 <= a^2  holds under the condition.
If it did, then Area*R^2 <= ((Area+R^2)/2)^2 <= a^4/4 by AM-GM, giving the bound!

That would be a clean proof.  Let us test it.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[3, 4, 5, 6, 7, 8, 9, 10])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        vecs = [(dx, dy) for dx in range(-a, a + 1) for dy in range(-a, a + 1)
                if (dx, dy) != (0, 0)]
        bound = Fraction(a ** 4, 4)
        best = Fraction(0)
        best_info = None
        max_sum = Fraction(0)
        sum_info = None
        sum_violations = 0
        n_fit = 0
        for u in vecs:
            for v in vecs:
                c = u[0] * v[1] - u[1] * v[0]
                if c == 0:
                    continue
                c = abs(c)
                n1 = u[0] ** 2 + u[1] ** 2
                n2 = v[0] ** 2 + v[1] ** 2
                w = (u[0] - v[0], u[1] - v[1])
                n3 = w[0] ** 2 + w[1] ** 2
                # centre (relative to p1 at origin); sign of c matters for O
                cc = u[0] * v[1] - u[1] * v[0]
                Ox = Fraction(n1 * v[1] - n2 * u[1], 2 * cc)
                Oy = Fraction(n2 * u[0] - n1 * v[0], 2 * cc)
                xs = [Fraction(0), Fraction(u[0]), Fraction(v[0]), Ox]
                ys = [Fraction(0), Fraction(u[1]), Fraction(v[1]), Oy]
                if max(xs) - min(xs) > a or max(ys) - min(ys) > a:
                    continue
                n_fit += 1
                area = Fraction(c, 2)
                R2 = Fraction(n1 * n2 * n3, 4 * c * c)
                prod = area * R2
                if prod > best:
                    best = prod
                    best_info = {"u": list(u), "v": list(v), "c": c,
                                 "area": str(area), "R2": str(R2),
                                 "product": str(prod)}
                s = area + R2
                if s > max_sum:
                    max_sum = s
                    sum_info = {"u": list(u), "v": list(v), "c": c,
                                "area": str(area), "R2": str(R2), "sum": str(s)}
                if s > a * a:
                    sum_violations += 1
        report.append({
            "a": a, "bound": str(bound), "fitting": n_fit,
            "max_area_R2": str(best), "at_bound": best == bound,
            "extremal": best_info,
            "max_area_plus_R2": str(max_sum),
            "sum_bound_a2": a * a,
            "KEY_holds": sum_violations == 0,
            "sum_violations": sum_violations,
            "sum_extremal": sum_info,
        })
        print(f"a={a}: fitting={n_fit}  max Area*R^2={best} "
              f"({'AT BOUND' if best == bound else 'below'})", flush=True)
        print(f"   KEY (Area+R^2 <= a^2): "
              f"{'HOLDS' if sum_violations == 0 else 'FAILS'}  "
              f"max sum={max_sum} (bound {a*a})", flush=True)
        if sum_info and sum_violations:
            print(f"   sum violation: u={sum_info['u']} v={sum_info['v']} "
                  f"area={sum_info['area']} R2={sum_info['R2']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
