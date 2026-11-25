"""Why is the inversive K bounded by a constant?

Observed: K ~ 9 for all q from 3 to 29.

Let me look for a proof that K = O(1).

SETUP.  Inversive plane of order q: v = q^2+1 points, b = q(q^2+1) circles,
each circle has s = q+1 points, lambda_2 = q+1 (circles through a pair),
lambda_3 = 1 (circles through a triple).

A safe set S meets every circle in at most 3 points.

KEY IDEA: use the "circle through a pair" structure more carefully.

For a pair {a,b} in S, the pencil has q+1 circles.  Each circle through a,b
can contain at most 1 more point of S (since 3 is the limit).  So at most q+1
points of S can be "covered" by the pencil.  That gives k-2 <= q+1, i.e.
k <= q+3.  Linear, not constant.

To get a constant bound we need a DIFFERENT argument.

IDEA: count TRIPLES more carefully.

Each triple of S lies on exactly one circle.  The circle has q+1 points, of
which 3 are in S.  So the circle has q-2 points outside S.

Now consider a FIXED point p in S.  The circles through p that contain 2 other
points of S number C(k-1,2).  Each such circle has q+1 points, so q-2 points
outside S.

Hmm, that does not immediately bound k.

IDEA 2: use the fact that two circles meet in at most 2 points.

Take two disjoint pairs {a,b} and {c,d} in S.  The circle through a,b,c and the
circle through a,b,d are distinct (they share a,b but differ in the third
point).  Both are in the pencil through a,b.

Now consider the circle through a,c,d and the circle through b,c,d.  These are
in the pencils through a,c and b,c respectively.

Hmm.

IDEA 3: Let me look at the actual structure of maximum safe sets.

For q=29, K=8.  Let me examine the witness and see its structure.

Actually, let me test a specific conjecture: is K bounded by the maximum number
of points on a circle minus something?  No, circles have q+1 points which grows.

Let me look at the DATA differently: what is the maximum size of a set with no
4 concyclic in the inversive plane?  This is the "3-arc" problem.

Known result (from literature): for the inversive plane of order q, the maximum
size of a 3-arc is at most q+1 (trivially, since a circle has q+1 points and
... no, that's not a bound).

Hmm.  Let me think about the "arc" literature again.

Actually, in the inversive plane, a set with no 4 concyclic is called a
"3-arc" or "cap".  The maximum size is known to be:
  - q+1 for q even?  No, our data shows K=7 for q=8, much less than 9.

Let me just try to find a proof of K = O(1) or K = O(sqrt(q)) etc.

COUNTING ARGUMENT: Let S be safe with |S| = k.  Consider the C(k,3) circles
determined by triples of S.  Each such circle contains exactly 3 points of S.

Now, each circle has q+1 points.  Consider the "incidence" between S and the
circles: each point of S is on r = q(q+1) circles.

Hmm, let me try: count pairs (circle C, point p in S∩C) where C is a
"triple circle" (contains 3 points of S).  Each triple circle contributes 3.
So 3*C(k,3) incidences.

On the other hand, each point p in S is on how many triple circles?  The
triple circles through p correspond to pairs {a,b} of S\{p}, and each pair
gives a distinct circle.  So C(k-1,2) triple circles through p.

So 3*C(k,3) = k*C(k-1,2).  Check: 3*k(k-1)(k-2)/6 = k(k-1)(k-2)/2.  And
k*C(k-1,2) = k(k-1)(k-2)/2.  Consistent.  No new info.

Let me try the SECOND moment: count pairs of triple circles that share 2 points.

Two triple circles sharing 2 points {a,b} of S: they are both in the pencil
through a,b, and each contains a third point of S.  The number of such pairs
is C(k,2) * C(k-2, 2) (choose the pair {a,b}, then choose 2 of the k-2 other
points to be the third points of the two circles).

Each pair of triple circles shares at most 2 points (two circles meet in at
most 2 points).  So the count is consistent.

Hmm.

Let me try a completely different approach: look for a SMALL "blocking set".

For a safe set S, every point p outside S must be blocked: adding p would
create a 4-point circle.  So for every p outside S, there is a circle through
p containing 3 points of S.

The number of points outside S is q^2+1-k.  Each triple of S blocks at most
(q+1-3) = q-2 points (the other points on its circle).

So: q^2+1-k <= C(k,3) * (q-2).

For k ~ 9 and q large: LHS ~ q^2, RHS ~ 84*q.  So q^2 <= 84q, i.e. q <= 84.
That gives an upper bound on q for which K=9 is possible, not a bound on k.

Hmm, but this is interesting: it says that for q > 84, a safe set of size 9
cannot block all points.  So K must grow for large q!

Wait, that contradicts the "K is constant" observation.  Let me redo.

Each triple of S determines a circle with q+1 points, of which 3 are in S, so
q-2 are outside S.  These are the points blocked by that triple.

Total blocked points (with multiplicity) = C(k,3)*(q-2).

For S to be maximal, every point outside S must be blocked at least once:
q^2+1-k <= C(k,3)*(q-2).

For k=9: C(9,3)=84, so RHS = 84(q-2).  LHS = q^2+1-9 = q^2-8.
q^2-8 <= 84q-168 => q^2-84q+160 <= 0 => q <= 82 (approximately).

So for q > 82, a maximal safe set of size 9 is impossible!

That means K must GROW for large q.  The "K is constant" observation is only
valid for q <= 82 or so.

This is a genuine theoretical prediction!  Let me verify the inequality and
document it.

Actually wait, I need to be careful: the blocking argument requires S to be
MAXIMAL, not just safe.  K is the maximum safe size, and a maximum safe set is
maximal.  So the argument applies to maximum safe sets.

So: K(q) satisfies q^2+1-K <= C(K,3)*(q-2).

For K=9: q <= 82.
For K=10: C(10,3)=120, q^2 <= 120q => q <= 120.
For K=11: C(11,3)=165, q <= 165.

So K grows like sqrt(q)?  Let me solve: q^2 <= C(K,3)*q => q <= C(K,3) =>
C(K,3) >= q => K^3/6 >= q => K >= (6q)^(1/3).

So K >= (6q)^{1/3} for maximal sets.  That is a LOWER bound on K.

And the upper bound from lambda_2 is K <= q+3.

So (6q)^{1/3} <= K <= q+3.

For q=29: (174)^{1/3} = 5.6.  K=8 >= 5.6.  OK.
For q=1000: (6000)^{1/3} = 18.2.  So K >= 19 for q=1000.

So K DOES grow, like q^{1/3}!

This is a genuine theoretical result: K = Omega(q^{1/3}).

And the observed K ~ 9 for q <= 29 is consistent with q^{1/3} growth
(29^{1/3} = 3.07, times 6^{1/3}=1.82 gives 5.6).

Let me verify this bound carefully and document it.
"""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path


def min_k_for_maximal(q: int) -> int:
    """Smallest k such that q^2+1-k <= C(k,3)*(q-2)."""
    k = 3
    while True:
        lhs = q * q + 1 - k
        rhs = comb(k, 3) * (q - 2)
        if lhs <= rhs:
            return k
        k += 1
        if k > q + 3:
            return -1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    INV = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 8, 17: 9, 19: 9,
           23: 10, 29: 8}

    print("BLOCKING BOUND: a maximal safe set of size k needs")
    print("  q^2+1-k <= C(k,3)*(q-2)")
    print()
    print(f"{'q':>4} {'min k for maximal':>18} {'observed K':>11} {'ok?':>5}")
    rows = []
    for q in sorted(INV):
        mk = min_k_for_maximal(q)
        k = INV[q]
        ok = k >= mk
        rows.append({"q": q, "min_k": mk, "observed_K": k, "ok": ok})
        print(f"{q:>4} {mk:>18} {k:>11} {str(ok):>5}")

    print()
    print("asymptotic: C(k,3) >= q  =>  k >= (6q)^(1/3)")
    print()
    print(f"{'q':>6} {'(6q)^(1/3)':>12}")
    for q in (29, 100, 1000, 10000, 1000000):
        print(f"{q:>6} {(6*q)**(1/3):>12.2f}")

    print()
    print("=> K = Omega(q^(1/3)).  The observed K~9 for q<=29 is consistent")
    print("   with this growth; K must grow for large q.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
