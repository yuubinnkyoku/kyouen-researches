"""Proof attempt: Area * R^2 <= a^4/4 for the circumcircle of three lattice points.

Numerical finding (det_centre_inside_sharp.py): for a = 3..8, the maximum of
Area * R^2 over all triples whose circumcentre lies in [0,a]^2 is EXACTLY a^4/4,
attained by the four "corner right triangles" (three corners of the square).

This suggests a clean proof strategy:

  STEP 1.  For any triangle with vertices in [0,a]^2, Area <= a^2/2.
  STEP 2.  If the circumcentre O is in [0,a]^2, then R^2 <= a^2/2.
  STEP 3.  Hence Area * R^2 <= (a^2/2)(a^2/2) = a^4/4.

STEP 1 is trivial (the triangle is inside the square).

STEP 2 is the crux.  Is it true that a circle with centre in [0,a]^2 passing
through three lattice points of [0,a]^2 has R^2 <= a^2/2?

NO -- counterexample: the circle through (0,0), (a,0), (a/2, a/2) has centre
(a/2, 0) and R = a/2, so R^2 = a^2/4 <= a^2/2.  OK.
But the circle through (0,0), (a,0), (0,a) has centre (a/2,a/2) and
R^2 = a^2/2.  Also OK.

What about a circle through (0,0), (a,0), (a,a)?  Centre (a/2, a/2), R^2 = a^2/2.
What about (0,0), (a,a), (0,a)?  Same.

Is there a circle with centre in the square and R^2 > a^2/2 passing through three
lattice points of the square?  Let us test exhaustively.

If STEP 2 holds, the proof is complete and elementary.
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
    ap.add_argument("--a", type=int, nargs="+", default=[2, 3, 4, 5, 6, 7, 8])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        pts = [(x, y) for y in range(a + 1) for x in range(a + 1)]
        bound_R2 = Fraction(a * a, 2)
        max_R2 = Fraction(0)
        max_R2_info = None
        violations = 0
        for tri in itertools.combinations(pts, 3):
            coef = coeffs(*tri)
            if coef[2] == 0:
                continue
            cd = circle_data(coef)
            if cd is None:
                continue
            cx, cy, R2 = cd
            if not (0 <= cx <= a and 0 <= cy <= a):
                continue
            if R2 > bound_R2:
                violations += 1
                if violations <= 3:
                    print(f"  STEP2 VIOLATION a={a} tri={tri} R2={R2} > {bound_R2}",
                          flush=True)
            if R2 > max_R2:
                max_R2 = R2
                max_R2_info = {"triple": list(tri), "R2": str(R2),
                               "centre": [str(cx), str(cy)]}
        report.append({
            "a": a,
            "bound_R2_a2_2": str(bound_R2),
            "max_R2_centre_inside": str(max_R2),
            "STEP2_holds": violations == 0,
            "violations": violations,
            "extremal": max_R2_info,
        })
        print(f"a={a}: STEP2 (R^2 <= a^2/2 for centre inside): "
              f"{'HOLDS' if violations == 0 else 'FAILS'}  "
              f"max R^2 = {max_R2} (bound {bound_R2})", flush=True)
        if max_R2_info:
            print(f"   extremal {max_R2_info['triple']} centre={max_R2_info['centre']}",
                  flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
