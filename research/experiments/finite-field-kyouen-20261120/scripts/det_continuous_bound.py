"""Analytic bound for the circle determinant: the continuous relaxation.

Goal: prove that for any three lattice points p1,p2,p3 in [0,a]^2 and any real
(x,y) in [0,a]^2,

    |Delta(x,y)| <= a^4/2 + [a odd]/2

where Delta(x,y) = alpha x + beta y + gamma(x^2+y^2) + delta.

This is the continuous relaxation of the lattice bound D(n) = a^2*floor(a^2/2).
Observed (a <= 12): the continuous max equals a^4/2 for even a and a^4/2 + 1/2
for odd a, while the lattice max is a^2*floor(a^2/2) = a^4/2 - [a odd]/2.

Strategy explored here:

  Delta/gamma = (x-cx)^2 + (y-cy)^2 - R^2   (power of the point)

so |Delta| = |gamma| * |power|.  Over the square, the power is maximised at a
corner (it is a convex function of (x,y) separately in x and y, so its maximum
over a rectangle is on the boundary, and on each edge it is a convex quadratic,
hence maximised at an endpoint).  Therefore

    max over the square of |power| = max over the 4 corners of |power|.

This reduces the continuous problem to four corner evaluations, which is a
finite (and small) computation for each triple.  The remaining task is to bound
|gamma| * max_corner |power| over all triples.

This script verifies the corner-reduction claim and computes the resulting
bound, comparing with a^4/2.
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


def delta_at(coef, x, y):
    alpha, beta, gamma, delta = coef
    return alpha * x + beta * y + gamma * (x * x + y * y) + delta


def max_abs_on_square_exact(coef, a: int):
    """Exact max over the integer lattice square."""
    best = 0
    arg = None
    for x in range(a + 1):
        for y in range(a + 1):
            v = abs(delta_at(coef, x, y))
            if v > best:
                best, arg = v, (x, y)
    return best, arg


def max_abs_on_square_continuous(coef, a: int):
    """Max over the real square, using convexity: attained at a corner."""
    corners = [(0, 0), (a, 0), (0, a), (a, a)]
    best = 0
    arg = None
    for (x, y) in corners:
        v = abs(delta_at(coef, x, y))
        if v > best:
            best, arg = v, (x, y)
    return best, arg


def max_abs_on_square_dense(coef, a: int, steps: int = 60):
    """Dense sampling of the real square, to test the corner claim."""
    best = Fraction(0)
    arg = None
    for i in range(steps + 1):
        for j in range(steps + 1):
            x = Fraction(a * i, steps)
            y = Fraction(a * j, steps)
            v = abs(delta_at(coef, x, y))
            if v > best:
                best, arg = v, (x, y)
    return best, arg


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[3, 4, 5, 6, 7])
    ap.add_argument("--dense-steps", type=int, default=40)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        pts = [(x, y) for y in range(a + 1) for x in range(a + 1)]
        best_lat = 0
        best_cont = 0
        corner_ok = True
        for tri in itertools.combinations(pts, 3):
            coef = coeffs(*tri)
            vl, _ = max_abs_on_square_exact(coef, a)
            vc, _ = max_abs_on_square_continuous(coef, a)
            best_lat = max(best_lat, vl)
            best_cont = max(best_cont, vc)
            # spot-check the corner claim on a few triples
            if corner_ok and tri[0] == (0, 0) and tri[1] == (a, 0):
                vd, _ = max_abs_on_square_dense(coef, a, args.dense_steps)
                if vd > vc:
                    corner_ok = False
        formula = a * a * ((a * a) // 2)
        cont_formula = Fraction(a ** 4, 2) + (Fraction(1, 2) if a % 2 else 0)
        report.append({
            "a": a,
            "lattice_max": best_lat,
            "lattice_formula": formula,
            "lattice_match": best_lat == formula,
            "continuous_max": str(best_cont),
            "continuous_formula": str(cont_formula),
            "continuous_match": Fraction(best_cont) == cont_formula,
            "corner_reduction_ok": corner_ok,
        })
        print(f"a={a}: lattice={best_lat} (formula {formula}, "
              f"{'OK' if best_lat == formula else 'MISMATCH'})  "
              f"continuous={best_cont} (formula {cont_formula}, "
              f"{'OK' if Fraction(best_cont) == cont_formula else 'MISMATCH'})  "
              f"corner_reduction={'OK' if corner_ok else 'FAIL'}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
