"""Upper bound for AG(2,q) when q = 3 mod 4: use the CIRCLE structure.

For q = 3 mod 4, -1 is a non-square, so x^2+y^2 is anisotropic and every circle
is a genuine conic with q+1 points.  There are q^2(q-1) circles and q(q+1) lines.

The cross trick does not apply.  But there is another structure: the circles
through a fixed point.

For a point P, the circles through P: how many?  Each circle through P is
determined by two other points, but different pairs can give the same circle.
The number of circles through P equals the number of circles in the "pencil"
at P, which for the inversive plane is q(q-1)... let me just compute it.

Better idea: use the fact that the circles through two points form a pencil of
size q-1 (for q odd).  Then:

  For a safe set S with |S| = k, consider the pairs {p,q} in S.  Each pair lies
  on exactly q-1 circles (plus 1 line).  Each such circle holds at most 3 points
  of S, so at most one more point of S.

  Count triples: each triple of S lies on exactly one circle (if non-collinear)
  or one line (if collinear).  So the number of triples is at most the number
  of blocks: C(k,3) <= q^3+q.  That is the standard bound.

Let us look for a "2-point" structure analogous to the cross.

For q = 3 mod 4, consider the sets
    D_P = {points Q : Q is at "distance" 0 from P}  -- just {P}
Not useful.

Alternative: consider the "circle through P with centre at P"?  No.

Let me look at the actual block structure for q=7 and q=11 and see if there is
a family of large blocks we have missed.

For q=7: sizes {7: 56, 8: 294}.  Lines are size 7, circles size 8.
For q=11: sizes {11: 132, 12: 1210}.

No large blocks.  So the cross trick has no analogue.

DIFFERENT APPROACH: use the LINE structure with a sharper argument.

Every safe set meets every line in at most 3 points.  AG(2,q) has q+1 parallel
classes of q lines each.  Within one parallel class, the q lines partition the
q^2 points.  So the sum of |S cap L| over the q lines of one parallel class
equals k.  Since each is at most 3:
    k <= 3q.
That is the line bound, weak.

But we can use TWO parallel classes.  Two lines from different classes meet in
exactly one point.  Let the classes be A (lines a_1..a_q) and B (lines b_1..b_q).
Let x_ij = 1 if the intersection point a_i cap b_j is in S.
Then
    sum_j x_ij = |S cap a_i| <= 3
    sum_i x_ij = |S cap b_j| <= 3
    sum_ij x_ij = k
So k <= 3q (from either direction).  Still weak.

Hmm.  Let me think about what makes K small for q = 3 mod 4.

Observed: q=7 K=6, q=11 K=9, q=19 K>=13.  So K/q = 0.86, 0.82, 0.68.

The circles have q+1 points and there are q^2(q-1) of them.  Each point is on
how many circles?  Let me compute: total incidences = q^2(q-1)(q+1) = q^2(q^2-1).
Divided by q^2 points: q^2-1 circles per point.  Plus q+1 lines.  So degree
= q^2-1 + q+1 = q^2+q.

For q=7: degree = 56.  Matches the earlier computation.

So each point is on q^2+q blocks.  A safe set of size k has each point on
q^2+q blocks, and each block holds at most 3 points of S.  Counting incidences:
    k(q^2+q) = sum over blocks of |S cap B| <= 3 * (#blocks) = 3(q^3+q)
    k <= 3(q^3+q)/(q^2+q) = 3(q^2+1)/(q+1) ~ 3q.
Weak again.

Let me try the "pair" counting with the circle pencil:
    sum over blocks of C(|S cap B|, 2) = (number of blocks through a pair) * C(k,2)
    = (q-1 + 1) * C(k,2) = q * C(k,2)
Since |S cap B| <= 3, C(|S cap B|,2) <= 3:
    q * C(k,2) <= 3(q^3+q)
    C(k,2) <= 3(q^3+q)/q = 3(q^2+1)
    k <= sqrt(6) q ~ 2.45q
Weak.

So all elementary counting gives O(q).  The observed K/q ~ 0.7-0.9 is consistent
with O(q) but the constant is not pinned down.

CONCLUSION: for q = 3 mod 4, the best elementary bound is the triple bound
C(k,3) <= q^3+q, giving k ~ 6^{1/3} q ~ 1.82q.  The observed K/q ~ 0.7-0.9 is
below this, but no sharper bound is available from these arguments.

This script verifies the degree and the bounds.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 7, 11, 19])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'pts':>5} {'blocks':>7} {'deg':>6} {'triple':>7} "
          f"{'pair':>6} {'incid':>6} {'K':>4}")
    K_DATA = {3: 5, 7: 6, 11: 9, 19: 13}
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        n = len(pts)
        degs = Counter(len(t) for t in through)
        deg = next(iter(degs)) if len(degs) == 1 else None
        b = len(blocks)
        # triple bound
        kt = 3
        while comb(kt + 1, 3) <= b:
            kt += 1
        # pair bound: q*C(k,2) <= 3b
        kp = 2
        while q * comb(kp + 1, 2) <= 3 * b:
            kp += 1
        # incidence bound: deg*k <= 3b
        ki = 3
        while deg and deg * (ki + 1) <= 3 * b:
            ki += 1
        rows.append({"q": q, "points": n, "blocks": b, "degree": deg,
                     "triple_bound": kt, "pair_bound": kp,
                     "incidence_bound": ki if deg else None,
                     "K": K_DATA.get(q)})
        print(f"{q:>3} {n:>5} {b:>7} {deg if deg else 'var':>6} {kt:>7} "
              f"{kp:>6} {ki if deg else '-':>6} {K_DATA.get(q, '-'):>4}")

    print()
    print("all elementary bounds are O(q); the triple bound is the sharpest")
    print("for q = 3 mod 4, giving k ~ 6^(1/3) q ~ 1.82 q.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
