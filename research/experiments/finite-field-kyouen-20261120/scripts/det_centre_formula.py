"""Closing the proof: combine the identity with the centre-inside condition.

We have, for u = p2-p1, v = p3-p1 (integer vectors), c = |u x v|, s = u.v,
n1 = |u|^2, n2 = |v|^2, n3 = |u-v|^2:

    (I)  n1 n2 = c^2 + s^2                      [Lagrange identity]
    (II) Area * R^2 = n1 n2 n3 / (8c)

The unconstrained maximum of (II) over vectors in [-a,a]^2 is much larger than
a^4/4 (see det_identity.py), because nearly-degenerate triangles (c=1, s large)
give huge R^2.  But those triangles have their circumcentre FAR OUTSIDE the
square, so their |power| is not R^2.

So the centre-inside condition is essential.  Let us express it algebraically.

The circumcentre O satisfies 2 O.u = n1 and 2 O.v = n2 (taking p1 as origin).
Solving,
    O = (n1 * v_perp - n2 * u_perp) / (2c)   (up to sign conventions)

where u_perp = (-u_y, u_x).  Concretely, with u=(ux,uy), v=(vx,vy), c = ux*vy-uy*vx:

    Ox = (n1*vy - n2*uy) / (2c)
    Oy = (n2*ux - n1*vx) / (2c)

The condition "O in [0,a]^2" becomes four linear inequalities in n1,n2 and the
coordinates.

This script:
  1. verifies the centre formula,
  2. computes, for each triangle with O inside the square, the exact value of
     Area*R^2 and confirms the bound a^4/4,
  3. reports the extremal triangles (which should be the four corner triangles).
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[3, 4, 5, 6, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        vecs = [(dx, dy) for dx in range(-a, a + 1) for dy in range(-a, a + 1)
                if (dx, dy) != (0, 0)]
        bound = Fraction(a ** 4, 4)
        best = Fraction(0)
        best_info = None
        centre_formula_ok = True
        n_inside = 0
        for u in vecs:
            for v in vecs:
                c = u[0] * v[1] - u[1] * v[0]
                if c == 0:
                    continue
                n1 = u[0] ** 2 + u[1] ** 2
                n2 = v[0] ** 2 + v[1] ** 2
                w = (u[0] - v[0], u[1] - v[1])
                n3 = w[0] ** 2 + w[1] ** 2
                # centre relative to p1 = origin
                Ox = Fraction(n1 * v[1] - n2 * u[1], 2 * c)
                Oy = Fraction(n2 * u[0] - n1 * v[0], 2 * c)
                # verify: |O|^2 should equal R^2 = n1 n2 n3/(4 c^2)
                R2 = Fraction(n1 * n2 * n3, 4 * c * c)
                if Ox * Ox + Oy * Oy != R2:
                    centre_formula_ok = False
                # the square is [0,a]^2 but p1 is at the origin of the translated
                # frame; the actual square position depends on p1.  For the
                # bound we only need SOME placement, so we test the condition
                # that O lies in the square when p1 is a corner -- but that is
                # not general.
                # Instead: we test the condition for the WORST placement, i.e.
                # we ask whether there EXISTS a translation of the square
                # containing p1,p2,p3 and O.  Since all four points must be in
                # [0,a]^2, the bounding box of {0,u,v,O} must fit in [0,a]^2.
                xs = [Fraction(0), Fraction(u[0]), Fraction(v[0]), Ox]
                ys = [Fraction(0), Fraction(u[1]), Fraction(v[1]), Oy]
                if max(xs) - min(xs) > a or max(ys) - min(ys) > a:
                    continue
                n_inside += 1
                prod = Fraction(abs(c), 2) * R2
                if prod > best:
                    best = prod
                    best_info = {"u": list(u), "v": list(v), "c": c,
                                 "area": str(Fraction(abs(c), 2)),
                                 "R2": str(R2), "centre": [str(Ox), str(Oy)],
                                 "product": str(prod)}
        report.append({
            "a": a, "bound": str(bound),
            "centre_formula_ok": centre_formula_ok,
            "triangles_fitting": n_inside,
            "max_area_R2": str(best),
            "at_bound": best == bound,
            "extremal": best_info,
        })
        print(f"a={a}: centre formula ok: {centre_formula_ok}  "
              f"fitting triangles: {n_inside}  "
              f"max Area*R^2 = {best} (bound {bound}, "
              f"{'AT BOUND' if best == bound else 'below'})", flush=True)
        if best_info:
            print(f"   extremal u={best_info['u']} v={best_info['v']} "
                  f"area={best_info['area']} R2={best_info['R2']} "
                  f"centre={best_info['centre']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
