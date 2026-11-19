"""The real trade-off: Area * R^2 <= a^4/4 holds even though R^2 can exceed a^2/2.

STEP2 (R^2 <= a^2/2) is FALSE: e.g. a=5, triangle (0,0),(3,1),(4,2) has centre
(0,5) inside the square and R^2 = 25 > 25/2.

But that triangle has Area = 1/2 (it is nearly degenerate: (0,0),(3,1),(4,2)
are almost collinear).  So Area * R^2 = 25/2, well below a^4/4 = 625/4.

The correct statement must couple Area and R^2.  Let us find the exact relation.

Parametrise by the two edge vectors u = p2-p1, v = p3-p1 (integer vectors).
Then
    Area = |u x v| / 2
    R^2  = (|u|^2 |v|^2 |u-v|^2) / (4 (u x v)^2)

so
    Area * R^2 = (|u|^2 |v|^2 |u-v|^2) / (8 |u x v|).

Let c = |u x v| (a positive integer), and let n1=|u|^2, n2=|v|^2, n3=|u-v|^2.
Then
    Area * R^2 = n1 n2 n3 / (8c).

We want this <= a^4/4, i.e.

    n1 n2 n3 <= 2 a^4 c.

Now, u and v have coordinates in [-a,a], so n1,n2 <= 2a^2 and n3 <= 8a^2.
The product n1 n2 n3 <= 2a^2 * 2a^2 * 8a^2 = 32 a^6, which is too weak.

But there is a classical identity: for a triangle with sides x,y,z and area A,
    x^2 y^2 z^2 = 16 A^2 R^2
which is just the circumradius formula rearranged.  Not helpful directly.

The useful constraint: c = |u x v| is an integer >= 1, and n1 n2 - c^2 = (u.v)^2.
So n1 n2 = c^2 + (u.v)^2.  This couples the side lengths to the area!

Let s = u.v.  Then n1 n2 = c^2 + s^2.  Also n3 = n1 + n2 - 2s.

So
    Area * R^2 = (c^2 + s^2)(n1 + n2 - 2s) / (8c).

This script verifies the identity and explores the resulting bound.
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
        identity_ok = True
        for u in vecs:
            for v in vecs:
                c = u[0] * v[1] - u[1] * v[0]
                if c == 0:
                    continue
                c = abs(c)
                n1 = u[0] ** 2 + u[1] ** 2
                n2 = v[0] ** 2 + v[1] ** 2
                s = u[0] * v[0] + u[1] * v[1]
                w = (u[0] - v[0], u[1] - v[1])
                n3 = w[0] ** 2 + w[1] ** 2
                # identity check: n1*n2 = c^2 + s^2
                if n1 * n2 != c * c + s * s:
                    identity_ok = False
                # Area*R^2 = n1 n2 n3 / (8c)
                prod = Fraction(n1 * n2 * n3, 8 * c)
                if prod > best:
                    best = prod
                    best_info = {"u": list(u), "v": list(v), "c": c,
                                 "n1": n1, "n2": n2, "n3": n3, "s": s,
                                 "product": str(prod)}
        report.append({
            "a": a, "bound": str(bound),
            "identity_n1n2_eq_c2_plus_s2": identity_ok,
            "max_area_R2": str(best),
            "at_bound": best == bound,
            "extremal": best_info,
        })
        print(f"a={a}: identity n1*n2 = c^2+s^2: {identity_ok}  "
              f"max Area*R^2 = {best} (bound {bound}, "
              f"{'AT BOUND' if best == bound else 'below'})", flush=True)
        if best_info:
            print(f"   extremal u={best_info['u']} v={best_info['v']} "
                  f"c={best_info['c']} n1={best_info['n1']} n2={best_info['n2']} "
                  f"n3={best_info['n3']} s={best_info['s']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
