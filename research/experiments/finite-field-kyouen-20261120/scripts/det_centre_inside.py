"""The correct power bound: the centre is usually OUTSIDE the square.

The previous attempt bounded Area*R^2, but R^2 is only attained as |power| when
the centre lies INSIDE the square.  For nearly-degenerate triangles (small area)
the circumcentre is far outside, and the power at square points is much smaller
than R^2.

Correct decomposition.  For a point P and circle (O,R):

    power(P) = |P-O|^2 - R^2.

If O is outside the square, then for all P in the square |P-O| >= d where d is
the distance from O to the square, and

    |power(P)| <= max( |P-O|^2 - R^2 )  or  R^2 - |P-O|^2

The maximum of |power| over the square is attained at a corner or at the
clamped centre.  When O is outside, the clamped centre is the nearest square
point to O, and there |power| = R^2 - d^2 (if d < R) or d^2 - R^2.

So the relevant quantity is NOT R^2 but |R^2 - d^2| where d = dist(O, square).

This script computes, for each triangle, the exact max|power| and compares it
with R^2, to quantify how much the "outside centre" case saves.

It also tests the KEY INEQUALITY in the form that should be provable:

    Area * max|power| <= a^4/4

by checking it directly (already done) and by examining the extremal triangles.
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


def dist2_to_square(cx, cy, a: int) -> Fraction:
    """Squared distance from (cx,cy) to the square [0,a]^2."""
    dx = Fraction(0)
    if cx < 0:
        dx = -cx
    elif cx > a:
        dx = cx - a
    dy = Fraction(0)
    if cy < 0:
        dy = -cy
    elif cy > a:
        dy = cy - a
    return dx * dx + dy * dy


def max_abs_power(cx, cy, R2, a: int):
    best = Fraction(0)
    arg = None
    for (x, y) in [(0, 0), (a, 0), (0, a), (a, a)]:
        v = abs((x - cx) ** 2 + (y - cy) ** 2 - R2)
        if v > best:
            best, arg = v, (x, y)
    px = min(max(cx, Fraction(0)), Fraction(a))
    py = min(max(cy, Fraction(0)), Fraction(a))
    v = abs((px - cx) ** 2 + (py - cy) ** 2 - R2)
    if v > best:
        best, arg = v, (px, py)
    return best, arg


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[3, 4, 5, 6, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        pts = [(x, y) for y in range(a + 1) for x in range(a + 1)]
        bound = Fraction(a ** 4, 4)
        inside = 0
        outside = 0
        worst_inside = Fraction(0)
        worst_outside = Fraction(0)
        worst_info = None
        for tri in itertools.combinations(pts, 3):
            coef = coeffs(*tri)
            g = abs(coef[2])
            if g == 0:
                continue
            area = Fraction(g, 2)
            cd = circle_data(coef)
            if cd is None:
                continue
            cx, cy, R2 = cd
            p, arg = max_abs_power(cx, cy, R2, a)
            prod = area * p
            in_square = (0 <= cx <= a) and (0 <= cy <= a)
            if in_square:
                inside += 1
                worst_inside = max(worst_inside, prod)
            else:
                outside += 1
                worst_outside = max(worst_outside, prod)
            if worst_info is None or prod > Fraction(worst_info["product"]):
                worst_info = {
                    "triple": list(tri), "area": str(area), "power": str(p),
                    "centre": [str(cx), str(cy)], "R2": str(R2),
                    "in_square": in_square, "product": str(prod),
                }
        report.append({
            "a": a, "bound": str(bound),
            "centre_inside": inside, "centre_outside": outside,
            "worst_inside": str(worst_inside),
            "worst_outside": str(worst_outside),
            "worst": worst_info,
        })
        print(f"a={a}: bound {bound}", flush=True)
        print(f"   centre inside: {inside} triples, worst Area*power = {worst_inside}",
              flush=True)
        print(f"   centre outside: {outside} triples, worst Area*power = {worst_outside}",
              flush=True)
        if worst_info:
            print(f"   overall worst: triple={worst_info['triple']} "
                  f"area={worst_info['area']} power={worst_info['power']} "
                  f"inside={worst_info['in_square']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
