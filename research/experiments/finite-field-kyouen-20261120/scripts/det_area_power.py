"""Attempt the continuous bound via the circumradius formula.

We want:  |gamma| * max|power| <= a^4/2  for points in [0,a]^2.

We know |gamma| = 2*Area.  For a triangle with sides x,y,z and area A,

    R = xyz/(4A)          (circumradius)

and the power of a point P w.r.t. the circumcircle is |P - O|^2 - R^2, where O is
the centre.  For P in the square, |P - O| <= diam(square) + |O - centre|, which
is awkward.  A cleaner bound: the maximum of |power| over the square is at most

    max( |P-O|^2 ) + R^2  <=  (a*sqrt(2) + d)^2 + R^2

where d is the distance from O to the square.  This is too lossy.

Better approach: bound the power directly.  For a point P on the circle,
power = 0.  The power grows like 2*R*distance(P, circle).  Since the circle
passes through three lattice points in the square, and the square has diameter
a*sqrt(2), the maximum distance from a square point to the circle is at most
the diameter, so

    |power| <= 2*R*(a*sqrt(2)) + (a*sqrt(2))^2

which is again lossy.

This script instead tests a CONCRETE CONJECTURE that would give the bound:

    CONJECTURE:  Area * max|power| <= a^4/4.

Since |gamma| = 2*Area, this is exactly |gamma|*max|power| <= a^4/2.

We test it and also test the sharper per-triple statement

    max|power| <= a^4/(4*Area).

Both are checked exhaustively for small a.
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


def max_abs_power(coef, a: int):
    alpha, beta, gamma, delta = coef
    if gamma == 0:
        return None
    cx = Fraction(-alpha, 2 * gamma)
    cy = Fraction(-beta, 2 * gamma)
    R2 = cx * cx + cy * cy - Fraction(delta, gamma)
    best = Fraction(0)
    for (x, y) in [(0, 0), (a, 0), (0, a), (a, a)]:
        v = abs((x - cx) ** 2 + (y - cy) ** 2 - R2)
        best = max(best, v)
    px = min(max(cx, Fraction(0)), Fraction(a))
    py = min(max(cy, Fraction(0)), Fraction(a))
    v = abs((px - cx) ** 2 + (py - cy) ** 2 - R2)
    return max(best, v)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[3, 4, 5, 6, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        pts = [(x, y) for y in range(a + 1) for x in range(a + 1)]
        bound = Fraction(a ** 4, 4)
        worst_ratio = Fraction(0)
        worst_info = None
        violations = 0
        for tri in itertools.combinations(pts, 3):
            coef = coeffs(*tri)
            g = abs(coef[2])
            if g == 0:
                continue
            area = Fraction(g, 2)
            p = max_abs_power(coef, a)
            prod = area * p
            if prod > bound:
                violations += 1
                if violations <= 3:
                    print(f"  VIOLATION a={a} tri={tri} area={area} power={p} "
                          f"prod={prod} > {bound}", flush=True)
            if prod > worst_ratio:
                worst_ratio, worst_info = prod, (tri, area, p)
        report.append({
            "a": a,
            "bound_a4_4": str(bound),
            "violations": violations,
            "worst_area_times_power": str(worst_ratio),
            "worst_triple": list(worst_info[0]) if worst_info else None,
            "worst_area": str(worst_info[1]) if worst_info else None,
            "worst_power": str(worst_info[2]) if worst_info else None,
        })
        print(f"a={a}: bound a^4/4 = {bound}, violations = {violations}, "
              f"worst Area*power = {worst_ratio}", flush=True)
        if worst_info:
            print(f"   worst triple {worst_info[0]} area={worst_info[1]} "
                  f"power={worst_info[2]}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
