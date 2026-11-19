"""Structure of the power function for a lattice triangle's circumcircle.

For three lattice points p1,p2,p3 with area A (half-integer, A >= 1/2 when
non-collinear), the circumcircle has centre O and radius R with

    R = xyz / (4A)          (x,y,z the side lengths)

and the power of a point P is

    power(P) = |P - O|^2 - R^2.

We want to bound  A * max_{P in [0,a]^2} |power(P)|  by  a^4/4.

Key observation: the maximum of |power| over the square is attained at a corner
or at the clamped centre.  At the centre, power = -R^2, so |power| = R^2.
At a corner C, power(C) = |C-O|^2 - R^2.

This script decomposes the maximum into these cases and measures, for each
triangle, which case attains it and what the resulting product is.

The goal is to find the structural inequality that closes the proof.
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


def power_at(cx, cy, R2, x, y):
    return (x - cx) ** 2 + (y - cy) ** 2 - R2


def analyse(coef, a: int):
    """Return (max|power|, which case, details)."""
    cd = circle_data(coef)
    if cd is None:
        return None
    cx, cy, R2 = cd
    best = Fraction(0)
    case = None
    detail = None
    for (x, y) in [(0, 0), (a, 0), (0, a), (a, a)]:
        v = abs(power_at(cx, cy, R2, x, y))
        if v > best:
            best, case, detail = v, "corner", (x, y)
    px = min(max(cx, Fraction(0)), Fraction(a))
    py = min(max(cy, Fraction(0)), Fraction(a))
    v = abs(power_at(cx, cy, R2, px, py))
    if v > best:
        best, case, detail = v, "centre", (px, py)
    return best, case, detail, (cx, cy, R2)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[3, 4, 5, 6, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        pts = [(x, y) for y in range(a + 1) for x in range(a + 1)]
        bound = Fraction(a ** 4, 4)
        case_counts = {"corner": 0, "centre": 0}
        worst = Fraction(0)
        worst_info = None
        for tri in itertools.combinations(pts, 3):
            coef = coeffs(*tri)
            g = abs(coef[2])
            if g == 0:
                continue
            area = Fraction(g, 2)
            res = analyse(coef, a)
            if res is None:
                continue
            p, case, detail, (cx, cy, R2) = res
            case_counts[case] += 1
            prod = area * p
            if prod > worst:
                worst = prod
                worst_info = {
                    "triple": list(tri), "area": str(area), "power": str(p),
                    "case": case, "detail": [str(d) for d in detail],
                    "centre": [str(cx), str(cy)], "R2": str(R2),
                    "product": str(prod),
                }
        report.append({
            "a": a,
            "bound": str(bound),
            "worst_product": str(worst),
            "worst": worst_info,
            "case_counts": case_counts,
        })
        print(f"a={a}: bound {bound}, worst Area*power = {worst} "
              f"({'AT BOUND' if worst == bound else 'below'})", flush=True)
        print(f"   cases: {case_counts}", flush=True)
        if worst_info:
            print(f"   worst triple {worst_info['triple']} area={worst_info['area']} "
                  f"power={worst_info['power']} case={worst_info['case']}", flush=True)
            print(f"   centre={worst_info['centre']} R2={worst_info['R2']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
