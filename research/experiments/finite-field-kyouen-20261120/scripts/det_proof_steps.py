"""Proof of the continuous relaxation bound, step by step.

CLAIM.  For three distinct lattice points p1,p2,p3 in [0,a]^2 and any real
(x,y) in [0,a]^2,

    |Delta(x,y)| <= a^4/2 + [a odd]/2.

Structure found numerically (det_extremal_triples.py):
  * The maximum is attained ONLY by the two "corner right triangles"
        (0,0),(a,0),(0,a)   and   (0,0),(a,0),(a,a),
    whose circumcircle has centre (a/2, a/2) and radius a/sqrt(2).
  * At the centre, Delta = -gamma*R^2 with gamma = -a^2, R^2 = a^2/2,
    giving |Delta| = a^4/2.
  * For odd a the centre (a/2,a/2) is NOT a lattice point, so the lattice
    maximum is strictly smaller; the observed lattice max is a^4/2 - 1/2.

This script verifies the key algebraic facts that a proof would need:

  (F1) For the corner triangle, gamma = -a^2 and R^2 = a^2/2, so
       |Delta(centre)| = a^4/2.
  (F2) For ANY triple, |gamma| <= a^2.
  (F3) For ANY triple, the maximum of |power| over the square is <= a^2/2.
  (F4) Hence |Delta| <= |gamma| * max|power| <= a^2 * a^2/2 = a^4/2.

If (F2) and (F3) hold, the continuous bound follows immediately.
This script tests (F2) and (F3) exhaustively for small a.
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


def max_abs_power(coef, a: int):
    """max over the real square of |Delta/gamma| = |power|, for gamma != 0."""
    alpha, beta, gamma, delta = coef
    if gamma == 0:
        return None
    cx = Fraction(-alpha, 2 * gamma)
    cy = Fraction(-beta, 2 * gamma)
    R2 = cx * cx + cy * cy - Fraction(delta, gamma)
    best = Fraction(0)
    # corners
    for (x, y) in [(0, 0), (a, 0), (0, a), (a, a)]:
        v = abs((x - cx) ** 2 + (y - cy) ** 2 - R2)
        best = max(best, v)
    # clamped centre
    px = min(max(cx, Fraction(0)), Fraction(a))
    py = min(max(cy, Fraction(0)), Fraction(a))
    v = abs((px - cx) ** 2 + (py - cy) ** 2 - R2)
    best = max(best, v)
    return best


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[2, 3, 4, 5, 6, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        pts = [(x, y) for y in range(a + 1) for x in range(a + 1)]
        max_gamma = 0
        max_power = Fraction(0)
        max_prod = Fraction(0)
        worst_gamma_triple = None
        worst_power_triple = None
        for tri in itertools.combinations(pts, 3):
            coef = coeffs(*tri)
            g = abs(coef[2])
            if g > max_gamma:
                max_gamma, worst_gamma_triple = g, tri
            pw = max_abs_power(coef, a)
            if pw is not None:
                if pw > max_power:
                    max_power, worst_power_triple = pw, tri
                max_prod = max(max_prod, g * pw)
        bound_gamma = a * a
        bound_power = Fraction(a * a, 2)
        report.append({
            "a": a,
            "max_abs_gamma": max_gamma,
            "bound_gamma_a2": bound_gamma,
            "F2_holds": max_gamma <= bound_gamma,
            "max_abs_power": str(max_power),
            "bound_power_a2_2": str(bound_power),
            "F3_holds": max_power <= bound_power,
            "max_gamma_times_power": str(max_prod),
            "product_bound_a4_2": str(Fraction(a ** 4, 2)),
            "F4_holds": max_prod <= Fraction(a ** 4, 2),
            "worst_gamma_triple": list(worst_gamma_triple) if worst_gamma_triple else None,
            "worst_power_triple": list(worst_power_triple) if worst_power_triple else None,
        })
        print(f"a={a}: max|gamma|={max_gamma} (<=a^2={bound_gamma}: {max_gamma <= bound_gamma})  "
              f"max|power|={max_power} (<=a^2/2={bound_power}: {max_power <= bound_power})  "
              f"max|gamma|*|power|={max_prod} (<=a^4/2={Fraction(a**4,2)}: "
              f"{max_prod <= Fraction(a**4,2)})", flush=True)
        print(f"   worst gamma triple: {worst_gamma_triple}", flush=True)
        print(f"   worst power triple: {worst_power_triple}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
