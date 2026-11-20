"""A new route for q = 3 mod 4: use the CIRCLE SIZE and the pencil structure.

For q = 3 mod 4, every circle has exactly q+1 points and every line has q points.
The pencil through two points has lambda_2 = q+1 blocks (1 line + q circles).

The lambda_2 bound gives k <= q+3.  To improve, we need to use the fact that
the q circles in the pencil have size q+1, so each contains q-1 points besides
p and q.

KEY IDEA: in the pencil through p,q, the q circles each contain q-1 other points.
If S has k points, and each of the q circles must contain at most 1 more point
of S (since p,q are already 2), then the q circles can "absorb" at most q points
of S.  Plus the line can absorb at most 1 more point (line has q points, p,q
already there, so q-2 free, but at most 1 more point of S since 3 is the limit).

So the pencil through p,q can absorb at most q+1 points of S besides p,q.
That gives k-2 <= q+1, i.e. k <= q+3.  Same bound.

To improve, note that the q circles through p,q are NOT disjoint: two circles
through p,q meet exactly in {p,q}.  So a point r of S (other than p,q) lies on
exactly ONE circle through p,q (the one determined by p,q,r).  So the q circles
each get at most 1 point of S, and the line gets at most 1.

Hence k-2 <= q+1.  Same.

Hmm.  Let me think about the SECOND pencil.  Fix p,q,r in S.  The pencil through
p,q has q+1 blocks; one of them (the circle through p,q,r) contains r.
The pencil through p,r has q+1 blocks; one contains q.
The pencil through q,r has q+1 blocks; one contains p.

Now consider s in S\\{p,q,r}.  The triples {p,q,s}, {p,r,s}, {q,r,s} give three
blocks.  These are in the three pencils respectively.

Can we count how many DISTINCT blocks are used?  The three pencils are pairwise
disjoint except for the block B(p,q,r) which is in all three.

So the union of the three pencils has 3(q+1) - 2 blocks.
The blocks used by the s's: 3(k-3) blocks (3 per s), all distinct.
Plus B(p,q,r).

So 1 + 3(k-3) <= 3(q+1) - 2
    3k - 8 <= 3q + 1
    3k <= 3q + 9
    k <= q + 3
Same bound again.

OK so the pencil structure gives q+3 robustly.  Let me look for a DIFFERENT
structure.

IDEA: use the fact that circles have size q+1 and there are q^2(q-1) of them.
Consider the "circle through 3 points" map.  For a safe set S, the map
    triple -> circle
is injective.  The circles used are C(k,3) in number.

Now, each circle has q+1 points.  The circles used contain 3 points of S each.
Consider a point p in S.  The circles through p that are "used" (contain 3
points of S) number C(k-1,2) (one per pair of other points).

The circles through p total: q^2-1 (circles) + q+1 (lines) = q^2+q blocks.
Of these, C(k-1,2) are used.

For k = q+3: C(q+2,2) = (q+2)(q+1)/2 ~ q^2/2.  And the total is q^2+q.
So C(k-1,2) <= q^2+q is satisfied with room: q^2/2 < q^2+q.

No constraint.

Let me try yet another angle: the "circle intersection" structure.
Two circles meet in at most 2 points.  For a safe set S, consider the circles
used (C(k,3) of them).  Each pair of used circles shares at most 2 points of S,
but since each has exactly 3 points of S, two used circles share at most 2
points of S, i.e. they share at most 2 points total (if they share 2 points of
S, those are the only shared points).

Count pairs of used circles that share 2 points of S: each pair of points of S
determines lambda_2 blocks, of which the "used" ones are those containing a
third point of S.  For a pair {a,b}, the used blocks through it number k-2.
So the number of (pair of S, pair of used circles sharing it) is
    C(k,2) * C(k-2, 2).
Each pair of used circles shares at most 2 points of S, so
    C(k,2) * C(k-2,2) <= C(C(k,3), 2) * 2.
Let me check: LHS = k(k-1)/2 * (k-2)(k-3)/2 = k(k-1)(k-2)(k-3)/4.
RHS = 2 * C(C(k,3),2) = 2 * C(k,3)(C(k,3)-1)/2 = C(k,3)(C(k,3)-1).
For k=10: LHS = 10*9*8*7/4 = 1260.  RHS = 120*119 = 14280.  OK.
For k=20: LHS = 20*19*18*17/4 = 29070.  RHS = 1140*1139 = 1298460.  OK.
No constraint.

CONCLUSION: the elementary counting arguments all give O(q) bounds with
constants >= 1, and the observed K is ~0.7q to 1.0q.  Improving the constant
below 1 seems to require a genuinely different idea.

Let me document this analysis and the failed attempts.
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

    print("checking the 'pair of used circles' counting argument:")
    print(f"{'k':>4} {'LHS':>12} {'RHS':>14} {'ok':>4}")
    rows = []
    for k in range(4, 25):
        lhs = Fraction(k * (k - 1) * (k - 2) * (k - 3), 4)
        c3 = comb(k, 3)
        rhs = c3 * (c3 - 1)
        ok = lhs <= rhs
        rows.append({"k": k, "lhs": str(lhs), "rhs": rhs, "ok": ok})
        if k <= 12 or not ok:
            print(f"{k:>4} {float(lhs):>12.1f} {rhs:>14} {'Y' if ok else 'N':>4}")

    print()
    print("the inequality holds for all k >= 4, so it gives no constraint.")
    print()
    print("summary of failed routes for q = 3 mod 4:")
    print("  1. degree counting: no constraint (k <= 2q+4)")
    print("  2. multi-pencil: bound stays lambda_2 + 2")
    print("  3. covering: only works for q = 3")
    print("  4. pair-of-used-circles: no constraint")
    print()
    print("all elementary counting gives O(q) with constant >= 1;")
    print("observed K/q is 0.68-0.86 for q = 3 mod 4.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
