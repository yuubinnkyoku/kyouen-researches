"""Sharpen the centre-inside case: Area * R^2 <= a^4/4.

When the circumcentre O lies in the square [0,a]^2, we have R^2 = |O - p1|^2
with both O and p1 in the square, so R^2 <= 2a^2.  That alone gives
Area*R^2 <= (a^2/2)(2a^2) = a^4, four times too weak.

The extremal cases suggest a sharper relation.  Let us parametrise:

    p1 = (0,0)  (translate; the square becomes a shifted square, but for the
                 extremal analysis we can keep the square fixed and let p1 vary)

Actually the cleanest parametrisation: let the three points be p1,p2,p3 and let
O be the circumcentre.  Then

    Area = (1/2)|(p2-p1) x (p3-p1)|

and R^2 = |O-p1|^2.

This script computes, for each triple with O inside the square, the ratio

    Area * R^2 / a^4

and reports the maximum, plus the extremal configuration.  It also tests
whether the bound is attained only by the two families found earlier.

Additionally it tests a CONJECTURE that would give a clean proof:

    CONJECTURE:  Area * R^2 <= (a^2/2) * (a^2/2) = a^4/4
    with equality iff the triangle is a right isosceles triangle with legs a
    (odd a) or the (0,0),(a,0),(a/2,a/2) triangle (even a).
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path


def det3(m) -> int:
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def coeffs(p1, p2, p3):
    rows3 = [(p1[0], p1[1], p1[0] ** 2 + p1[1] ** 2, 1),
             (p2[0], p2[1], p2[0] ** 2 + p2[1] ** 2, 1),
             (p3[0], p3[1], p3[0] ** 2 + p3[1] ** 2, 1)]
    out = []
    for j in range(4):
        minor = [[rows3[r][c] for c in range(4) if c != j] for r in range(3)]
        out.append((1 if (3 + j) % 2 == 0 else -1) * det3(minor))
    return out


def circle_data(coef):
    alpha, beta, gamma, delta = coef
    if gamma == 0:
        return None
    cx = Fraction(-alpha, 2 * gamma)
    cy = Fraction(-beta, 2 * gamma)
    R2 = cx * cx + cy * cy - Fraction(delta, gamma)
    return cx, cy, R2


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[3, 4, 5, 6, 7, 8])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        pts = [(x, y) for y in range(a + 1) for x in range(a + 1)]
        bound = Fraction(a ** 4, 4)
        best = Fraction(0)
        best_info = None
        attaining = []
        for tri in itertools.combinations(pts, 3):
            coef = coeffs(*tri)
            g = abs(coef[2])
            if g == 0:
                continue
            cd = circle_data(coef)
            if cd is None:
                continue
            cx, cy, R2 = cd
            if not (0 <= cx <= a and 0 <= cy <= a):
                continue
            area = Fraction(g, 2)
            prod = area * R2
            if prod == bound:
                attaining.append(list(tri))
            if prod > best:
                best = prod
                best_info = {"triple": list(tri), "area": str(area),
                             "R2": str(R2), "centre": [str(cx), str(cy)],
                             "product": str(prod)}
        report.append({
            "a": a, "bound": str(bound),
            "max_area_R2_centre_inside": str(best),
            "at_bound": best == bound,
            "num_attaining": len(attaining),
            "attaining": attaining[:10],
            "extremal": best_info,
        })
        print(f"a={a}: bound {bound}, max Area*R^2 (centre inside) = {best} "
              f"({'AT BOUND' if best == bound else 'below'}), "
              f"attaining triples: {len(attaining)}", flush=True)
        if best_info:
            print(f"   extremal {best_info['triple']} area={best_info['area']} "
                  f"R2={best_info['R2']} centre={best_info['centre']}", flush=True)
        if attaining:
            print(f"   attaining: {attaining[:4]}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
