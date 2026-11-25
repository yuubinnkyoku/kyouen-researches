"""Upper bounds for AG(2,q) when q = 3 mod 4 (no cross blocks).

For q = 3 mod 4, -1 is a non-square, so x^2+y^2 is anisotropic and the circle
equation does NOT factor into (s+a)(t+b).  There are no "cross" blocks.

But there is still structure.  Over F_q with q = 3 mod 4, the quadratic form
Q(x,y) = x^2+y^2 is anisotropic, so every circle is a genuine conic with q+1
points (verified earlier: q=3 gives 18 circles of size 4; q=7 gives 294 circles
of size 8; q=11 gives 1210 circles of size 12).

So the blocks are:
  * q(q+1) lines, each of size q,
  * q^2(q-1) circles, each of size q+1.

A safe set meets each block in at most 3 points.  Double counting triples:

    C(k,3) <= (#circles) + (#lines) = q^2(q-1) + q(q+1) = q^3 + q

giving k = O(q).  This is the bound already used.

Can we do better?  Ideas:

(A) Use PAIRS of blocks.  Two circles meet in at most 2 points; a circle and a
    line in at most 2; two lines in at most 1.  So for any two blocks B1, B2,
    |S cap (B1 u B2)| <= 3 + 3 - |B1 cap B2| >= 4.
    Summing over all pairs gives a bound involving the number of pairs and the
    total intersection sizes.  This is a "second moment" bound.

(B) Use the fact that each point lies on a fixed number of blocks.  For AG(2,q),
    each point lies on q+1 lines and on (number of circles through a point)
    circles.  Let d = total blocks through a point.  Then
        sum over blocks of |S cap B| = d*k.
    Since each |S cap B| <= 3, we get d*k <= 3*(#blocks), i.e.
        k <= 3*(#blocks)/d.
    For q=7: #blocks = 350, d = 91?  Let me compute.

This script computes the point-block incidence count d for several q and the
resulting bound k <= 3*#blocks/d, comparing with the triple-counting bound.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path

from ag2_prime_power import build_ag


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 7, 11])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        n = len(pts)
        n_blocks = len(blocks)
        degs = Counter(len(t) for t in through)
        d = next(iter(degs))
        # bound from incidence: d*k <= 3*n_blocks
        bound_inc = Fraction(3 * n_blocks, d)
        # bound from triple counting: C(k,3) <= n_blocks
        k = 3
        while comb(k + 1, 3) <= n_blocks:
            k += 1
        bound_triple = k
        report.append({
            "q": q,
            "q_mod_4": q % 4,
            "points": n,
            "blocks": n_blocks,
            "circles": nc,
            "lines": nl,
            "degree_uniform": len(degs) == 1,
            "degree": d,
            "bound_incidence": str(bound_inc),
            "K_upper_incidence": bound_inc.numerator // bound_inc.denominator,
            "bound_triple": bound_triple,
        })
        print(f"q={q} (mod4={q % 4}): {n} points, {n_blocks} blocks "
              f"(circles {nc}, lines {nl})", flush=True)
        print(f"   degree uniform: {len(degs) == 1}, d = {d}", flush=True)
        print(f"   incidence bound: d*k <= 3*blocks -> k <= {bound_inc} "
              f"-> K <= {bound_inc.numerator // bound_inc.denominator}", flush=True)
        print(f"   triple bound: C(k,3) <= blocks -> K <= {bound_triple}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
