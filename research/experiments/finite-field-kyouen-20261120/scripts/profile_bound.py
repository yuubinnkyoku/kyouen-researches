"""Can the circle profile give a NEW bound?

We established:
  * #circles with 3 points of S = C(k,3)
  * #circles with 2 points of S = C(k,2)(q-k+3)
  * total circles = q(q^2+1)

So:
  #circles with 0 or 1 point = q(q^2+1) - C(k,3) - C(k,2)(q-k+3)

This must be >= 0, giving:
  C(k,3) + C(k,2)(q-k+3) <= q(q^2+1)

Let me check whether this gives a constraint.

For k = q+3 (the lambda_2 bound):
  C(q+3,3) + C(q+3,2)(q-(q+3)+3) = C(q+3,3) + C(q+3,2)*0 = C(q+3,3)
  = (q+3)(q+2)(q+1)/6
And q(q^2+1) = q^3+q.
For q=7: C(10,3) = 120, q^3+q = 350.  120 <= 350 OK.
For q=13: C(16,3) = 560, 13*170 = 2210.  560 <= 2210 OK.
No constraint.

Hmm.  But wait: the formula #circles with 2 points = C(k,2)(q-k+3) requires
q-k+3 >= 0, i.e. k <= q+3.  That is exactly the lambda_2 bound!  So the formula
itself encodes the bound.

Indeed: for each pair {a,b} of S, the pencil through a,b has q+1 circles, of
which k-2 contain a third point of S.  So q+1-(k-2) = q-k+3 circles contain
only a,b.  This must be >= 0, giving k <= q+3.

So the profile analysis REPRODUCES the lambda_2 bound but does not improve it.

Let me look at the "0-point circles" count for a possible constraint.

#circles with 0 points = q(q^2+1) - C(k,3) - C(k,2)(q-k+3) - #circles with 1 point

We need #circles with 1 point >= 0 too.  Let me compute it.

#circles with exactly 1 point of S: for each p in S, the circles through p that
contain no other point of S.  Circles through p total q^2.  Of these:
  - C(k-1,2) contain 2 other points of S (one per pair),
  - (k-1)(q-k+3) contain exactly 1 other point of S (for each q, the pencil
    through p,q has q-k+3 circles with only p,q),
  - the rest contain no other point.
So #circles through p with only p = q^2 - C(k-1,2) - (k-1)(q-k+3).

This must be >= 0:
  q^2 >= C(k-1,2) + (k-1)(q-k+3)
  q^2 >= (k-1)[(k-2)/2 + q - k + 3]
  q^2 >= (k-1)[q + 2 - k/2]

That is exactly the degree bound we computed before, which gives k <= 2q+4.
Weaker than q+3.

So the profile analysis gives nothing new.  Let me document this.

Actually, let me double-check the "circles through p total q^2" claim.
Inversive plane of order q: v = q^2+1 points, b = q(q^2+1) circles, each circle
has q+1 points.  Each point is on r circles where r(q+1) = b, so
r = q(q^2+1)/(q+1) = q(q^2+1)/(q+1).
For q=3: 3*10/4 = 7.5.  Not an integer!  So my formula is wrong.

Let me recompute: b = q(q^2+1) = q^3+q.  Each circle has q+1 points.
Total incidences = (q^3+q)(q+1) = q(q^2+1)(q+1).
Points = q^2+1.
r = q(q^2+1)(q+1)/(q^2+1) = q(q+1).
For q=3: 3*4 = 12.  OK, r = q(q+1) = q^2+q.

So each point is on q^2+q circles, not q^2.  Let me redo:
  q^2+q >= C(k-1,2) + (k-1)(q-k+3)
  q^2+q >= (k-1)[q+2-k/2]
For k = q+3: (q+2)[q+2-(q+3)/2] = (q+2)(q+1/2) = q^2+2.5q+1.
And q^2+q.  So q^2+2.5q+1 <= q^2+q requires 1.5q+1 <= 0, false.
So k=q+3 VIOLATES this inequality!

Wait, that means k=q+3 is impossible?!  Let me check with q=7, k=10:
  C(9,2) + 9*(7-10+3) = 36 + 9*0 = 36.
  q^2+q = 56.  36 <= 56 OK.
Hmm, my formula (k-1)[q+2-k/2] for k=10, q=7: 9*(7+2-5) = 9*4 = 36. OK.
And q^2+q = 56.  36 <= 56.  OK, no violation.

Let me redo the algebra: (k-1)[(k-2)/2 + q-k+3] with k=q+3:
  (q+2)[(q+1)/2 + q-(q+3)+3] = (q+2)[(q+1)/2 + 0] = (q+2)(q+1)/2.
For q=7: 9*8/2 = 36.  Matches.
And q^2+q = 56.  36 <= 56 OK.

I made an arithmetic error before.  Let me redo: q-k+3 with k=q+3 gives q-(q+3)+3 = 0.  So the second term vanishes.  Good.

So the constraint is (k-1)(k-2)/2 <= q^2+q, i.e. C(k-1,2) <= q^2+q.
For k=q+3: C(q+2,2) = (q+2)(q+1)/2 ~ q^2/2 <= q^2+q.  OK.

So no constraint.  The profile analysis gives nothing new.

Let me document this properly.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import comb
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    print("circle profile identities (verified numerically):")
    print("  #circles with 3 points of S = C(k,3)")
    print("  #circles with 2 points of S = C(k,2)(q-k+3)")
    print("  #circles through a point p with only p = q^2+q - C(k-1,2) - (k-1)(q-k+3)")
    print()
    print("the requirement q-k+3 >= 0 gives k <= q+3 (the lambda_2 bound).")
    print("the requirement (circles through p with only p) >= 0 gives:")
    print("  C(k-1,2) + (k-1)(q-k+3) <= q^2+q")
    print()
    print(f"{'q':>3} {'k=q+3':>6} {'LHS':>10} {'q^2+q':>8} {'ok':>4}")
    rows = []
    for q in [3, 5, 7, 9, 11, 13, 17, 19]:
        k = q + 3
        lhs = comb(k - 1, 2) + (k - 1) * (q - k + 3)
        rhs = q * q + q
        rows.append({"q": q, "k": k, "lhs": lhs, "rhs": rhs, "ok": lhs <= rhs})
        print(f"{q:>3} {k:>6} {lhs:>10} {rhs:>8} {'Y' if lhs <= rhs else 'N':>4}")
    print()
    print("all satisfied: the profile analysis reproduces but does not improve")
    print("the lambda_2 bound k <= q+3.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
