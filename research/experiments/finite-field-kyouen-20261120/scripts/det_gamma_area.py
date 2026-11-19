"""Verify the relation between gamma and the triangle area.

Claim: gamma = +-2 * Area(p1,p2,p3) * (some fixed factor), and in particular
|gamma| <= a^2 for points in [0,a]^2.

The 3x3 minor that gives gamma is

    gamma = det[[x1,y1,1],[x2,y2,1],[x3,y3,1]]   (up to sign)

which is exactly twice the signed area of the triangle p1p2p3.  Let us verify
this directly: compute gamma from the 4x4 cofactor expansion and compare with
2*Area computed by the shoelace formula.

If gamma = +-2*Area, then since the triangle lies in [0,a]^2 its area is at most
a^2/2, giving |gamma| <= a^2.  That proves F2.
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


def gamma_of(p1, p2, p3) -> int:
    """The coefficient of x^2+y^2 in the 4x4 determinant expansion."""
    rows3 = [(p1[0], p1[1], p1[0] ** 2 + p1[1] ** 2, 1),
             (p2[0], p2[1], p2[0] ** 2 + p2[1] ** 2, 1),
             (p3[0], p3[1], p3[0] ** 2 + p3[1] ** 2, 1)]
    j = 2  # column of x^2+y^2
    minor = [[rows3[r][c] for c in range(4) if c != j] for r in range(3)]
    return (1 if (3 + j) % 2 == 0 else -1) * det3(minor)


def twice_area(p1, p2, p3) -> int:
    """Twice the signed area by the shoelace formula."""
    return ((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1]))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[2, 3, 4, 5, 6])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        pts = [(x, y) for y in range(a + 1) for x in range(a + 1)]
        mismatches = 0
        max_gamma = 0
        max_area2 = 0
        for tri in itertools.combinations(pts, 3):
            g = gamma_of(*tri)
            ar = twice_area(*tri)
            if g != ar:
                mismatches += 1
                if mismatches <= 3:
                    print(f"  MISMATCH a={a} tri={tri} gamma={g} 2*area={ar}", flush=True)
            max_gamma = max(max_gamma, abs(g))
            max_area2 = max(max_area2, abs(ar))
        bound = a * a
        report.append({
            "a": a,
            "mismatches": mismatches,
            "gamma_equals_twice_area": mismatches == 0,
            "max_abs_gamma": max_gamma,
            "max_abs_twice_area": max_area2,
            "bound_a2": bound,
            "F2_holds": max_gamma <= bound,
        })
        print(f"a={a}: gamma == 2*Area for all triples: {mismatches == 0}  "
              f"max|gamma|={max_gamma}  max|2*Area|={max_area2}  "
              f"<= a^2={bound}: {max_gamma <= bound}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
