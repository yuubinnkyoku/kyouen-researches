"""Attempt a proof of  Area * max|power| <= a^4/4.

Case analysis (verified in det_power_cases.py):

  Case C (centre):  the max is |power(O_clamped)| = R^2 when the centre lies in
                    the square.  Then Area * R^2 must be <= a^4/4.
  Case K (corner):  the max is |power(corner)|.

For Case C: R = xyz/(4A) where x,y,z are the side lengths.  Since all points are
in [0,a]^2, each side is at most a*sqrt(2), so xyz <= (a*sqrt(2))^3 = 2*sqrt(2)*a^3.
Hence

    R^2 = (xyz)^2/(16 A^2) <= 8 a^6/(16 A^2) = a^6/(2 A^2)

and

    A * R^2 <= a^6/(2A).

This is NOT bounded by a^4/4 unless A >= 2a^2, which is false (A <= a^2/2).
So the crude side-length bound is far too lossy: it gives A*R^2 <= a^6/(2A),
which for A = 1/2 is a^6, much larger than a^4/4.

The loss is because xyz is bounded independently of A, but for a SMALL area the
triangle must be nearly degenerate, so xyz cannot be maximal simultaneously.

KEY REFINEMENT: for a lattice triangle, A is a half-integer >= 1/2.  Moreover
the three side lengths satisfy a relation with A.  Let us parametrise by the
two vectors u = p2-p1, v = p3-p1 with integer coordinates.  Then

    A = |u x v| / 2,   x = |u|, y = |v|, z = |u-v|.

So A is determined by the integer cross product.  For fixed u, v the quantity
A*R^2 = A*(xyz)^2/(16A^2) = (xyz)^2/(16A) = (|u||v||u-v|)^2/(8|u x v|).

So we need:  (|u||v||u-v|)^2 / (8 |u x v|) <= a^4/4, i.e.

    (|u||v||u-v|)^2 <= 2 a^4 |u x v|.

This is a purely arithmetic inequality in the integer vectors u,v.  This script
tests it and looks for the extremal (u,v).
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path


def cross(u, v) -> int:
    return u[0] * v[1] - u[1] * v[0]


def norm2(u) -> int:
    return u[0] * u[0] + u[1] * u[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[3, 4, 5, 6, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        # vectors with coordinates in [-a, a]
        vecs = [(dx, dy) for dx in range(-a, a + 1) for dy in range(-a, a + 1)
                if (dx, dy) != (0, 0)]
        best = Fraction(0)
        best_info = None
        violations = 0
        bound = Fraction(a ** 4, 4)
        for u in vecs:
            for v in vecs:
                c = cross(u, v)
                if c == 0:
                    continue
                area = Fraction(abs(c), 2)
                # side lengths squared
                n1 = norm2(u)
                n2 = norm2(v)
                w = (u[0] - v[0], u[1] - v[1])
                n3 = norm2(w)
                # R^2 = (xyz)^2/(16 A^2); A = |c|/2 so 16A^2 = 4c^2
                # R^2 = (n1 n2 n3) / (4 c^2)   [since (xyz)^2 = n1*n2*n3]
                R2 = Fraction(n1 * n2 * n3, 4 * c * c)
                prod = area * R2
                if prod > bound:
                    violations += 1
                if prod > best:
                    best = prod
                    best_info = {"u": list(u), "v": list(v), "cross": c,
                                 "area": str(area), "R2": str(R2),
                                 "product": str(prod)}
        report.append({
            "a": a,
            "bound": str(bound),
            "violations": violations,
            "max_area_times_R2": str(best),
            "at_bound": best == bound,
            "extremal": best_info,
        })
        print(f"a={a}: bound {bound}, violations {violations}, "
              f"max Area*R^2 = {best} "
              f"({'AT BOUND' if best == bound else 'below'})", flush=True)
        if best_info:
            print(f"   extremal u={best_info['u']} v={best_info['v']} "
                  f"cross={best_info['cross']} area={best_info['area']} "
                  f"R2={best_info['R2']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
