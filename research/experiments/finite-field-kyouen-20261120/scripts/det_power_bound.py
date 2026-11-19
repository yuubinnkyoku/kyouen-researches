"""Attempt an analytic upper bound for D(n) via the circle-power interpretation.

Setup.  Fix three lattice points p1,p2,p3 in [0,a]^2.  Expanding the 4x4
determinant along the last row gives

    Delta(x,y) = alpha*x + beta*y + gamma*(x^2+y^2) + delta

with (alpha,beta,gamma,delta) 3x3 minors.  When p1,p2,p3 are not collinear,
gamma != 0 and

    Delta(x,y) / gamma = (x - cx)^2 + (y - cy)^2 - R^2

is the power of (x,y) with respect to the circle through p1,p2,p3, where
(cx,cy) is the centre and R the radius.

So the claim |Delta| <= a^2*floor(a^2/2) is equivalent to a bound on
|gamma| * |power| over the square.

This script measures, for each triple, the quantities
    |gamma|, centre, R^2, max |power| over the square,
and looks for the structural relation that makes the corner family extremal.

The goal is to find a proof strategy, not to assert one.
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
    return out  # alpha, beta, gamma, delta


def circle_data(p1, p2, p3):
    """Return (gamma, cx, cy, R2) as Fractions, or None if collinear."""
    alpha, beta, gamma, delta = coeffs(p1, p2, p3)
    if gamma == 0:
        return None
    # Delta/gamma = x^2+y^2 + (alpha/gamma) x + (beta/gamma) y + delta/gamma
    # centre = (-alpha/(2 gamma), -beta/(2 gamma))
    cx = Fraction(-alpha, 2 * gamma)
    cy = Fraction(-beta, 2 * gamma)
    # R^2 = cx^2 + cy^2 - delta/gamma
    R2 = cx * cx + cy * cy - Fraction(delta, gamma)
    return gamma, cx, cy, R2


def max_abs_power(cx, cy, R2, a: int):
    best = Fraction(0)
    arg = None
    for x in range(a + 1):
        for y in range(a + 1):
            v = (x - cx) ** 2 + (y - cy) ** 2 - R2
            if abs(v) > best:
                best, arg = abs(v), (x, y)
    return best, arg


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="+", default=[4, 5, 6])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for n in args.n:
        a = n - 1
        pts = [(x, y) for y in range(n) for x in range(n)]
        best = 0
        best_info = None
        for tri in itertools.combinations(pts, 3):
            cd = circle_data(*tri)
            if cd is None:
                continue
            gamma, cx, cy, R2 = cd
            pw, arg = max_abs_power(cx, cy, R2, a)
            v = abs(gamma) * pw
            if v > best:
                best = v
                best_info = {
                    "triple": tri,
                    "gamma": gamma,
                    "centre": (str(cx), str(cy)),
                    "R2": str(R2),
                    "max_power": str(pw),
                    "argmax": arg,
                    "value": str(v),
                }
        formula = a * a * ((a * a) // 2)
        report.append(
            {
                "n": n,
                "a": a,
                "max_via_power": best,
                "formula": formula,
                "match": best == formula,
                "extremal": best_info,
            }
        )
        print(f"n={n}: max |gamma|*|power| = {best}  formula = {formula}  "
              f"{'MATCH' if best == formula else 'MISMATCH'}", flush=True)
        if best_info:
            print(f"   triple={best_info['triple']}", flush=True)
            print(f"   gamma={best_info['gamma']} centre={best_info['centre']} "
                  f"R2={best_info['R2']}", flush=True)
            print(f"   max|power|={best_info['max_power']} at {best_info['argmax']}",
                  flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
