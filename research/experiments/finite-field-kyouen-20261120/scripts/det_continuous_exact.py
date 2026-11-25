"""Where is the maximum of |Delta| over the square?  A correction.

Earlier reasoning claimed the maximum is attained at a corner because Delta is
"separable convex".  That is WRONG in general:

    Delta(x,y) = alpha x + beta y + gamma(x^2+y^2) + delta

is convex in (x,y) when gamma > 0 and CONCAVE when gamma < 0.  For gamma < 0 the
maximum of |Delta| can be attained in the interior (near the circle centre).

This script:

  1. exhibits the failure explicitly,
  2. classifies triples by sign(gamma),
  3. computes the true continuous maximum by an exact method:
     - if gamma > 0: convex, max on the boundary (check the 4 edges as 1-D
       convex quadratics, hence at endpoints = corners),
     - if gamma < 0: concave, so |Delta| is maximised either at a corner or at
       the point where Delta = 0 (if the zero set crosses the square) or at the
       interior critical point (the centre),
  4. reports the resulting continuous maximum and compares with a^4/2.

The exact treatment of the concave case: Delta is a downward paraboloid with
vertex at the centre (cx,cy).  On the square, |Delta| is maximised either at a
corner (large |Delta|) or at the centre (Delta closest to 0 from the other
side).  We evaluate both and take the max.
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


def continuous_max(coef, a: int):
    """Exact max of |Delta| over the real square [0,a]^2.

    gamma > 0: convex -> max at a corner.
    gamma < 0: concave -> max at a corner or at the clamped centre.
    gamma = 0: affine -> max at a corner.
    """
    alpha, beta, gamma, delta = coef
    corners = [(0, 0), (a, 0), (0, a), (a, a)]
    best = max(abs(delta_at(coef, x, y)) for (x, y) in corners)
    arg = None
    for (x, y) in corners:
        if abs(delta_at(coef, x, y)) == best:
            arg = (x, y)
            break
    if gamma < 0:
        # vertex of the downward paraboloid
        cx = Fraction(-alpha, 2 * gamma)
        cy = Fraction(-beta, 2 * gamma)
        # clamp to the square
        cx = min(max(cx, Fraction(0)), Fraction(a))
        cy = min(max(cy, Fraction(0)), Fraction(a))
        v = abs(delta_at(coef, cx, cy))
        if v > best:
            best, arg = v, (cx, cy)
    return best, arg


def lattice_max(coef, a: int):
    best = 0
    arg = None
    for x in range(a + 1):
        for y in range(a + 1):
            v = abs(delta_at(coef, x, y))
            if v > best:
                best, arg = v, (x, y)
    return best, arg


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[3, 4, 5, 6, 7, 8])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        pts = [(x, y) for y in range(a + 1) for x in range(a + 1)]
        best_lat = 0
        best_cont = Fraction(0)
        sign_counts = {1: 0, -1: 0, 0: 0}
        for tri in itertools.combinations(pts, 3):
            coef = coeffs(*tri)
            g = coef[2]
            sign_counts[1 if g > 0 else (-1 if g < 0 else 0)] += 1
            vl, _ = lattice_max(coef, a)
            vc, _ = continuous_max(coef, a)
            best_lat = max(best_lat, vl)
            best_cont = max(best_cont, vc)
        formula = a * a * ((a * a) // 2)
        cont_formula = Fraction(a ** 4, 2) + (Fraction(1, 2) if a % 2 else 0)
        report.append({
            "a": a,
            "lattice_max": best_lat,
            "lattice_formula": formula,
            "lattice_match": best_lat == formula,
            "continuous_max": str(best_cont),
            "continuous_formula": str(cont_formula),
            "continuous_match": best_cont == cont_formula,
            "gamma_sign_counts": sign_counts,
        })
        print(f"a={a}: lattice={best_lat} ({'OK' if best_lat == formula else 'MISMATCH'})  "
              f"continuous={best_cont} "
              f"({'OK' if best_cont == cont_formula else 'MISMATCH'})  "
              f"gamma signs {sign_counts}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
