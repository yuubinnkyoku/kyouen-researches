"""Algebraic route: use the circle equation structure.

A circle in AG(2,q) is the zero set of
    f(x,y) = x^2 + y^2 + D x + E y + F = 0.

For a safe set S, no circle contains 4 points of S.  Equivalently, for every
choice of (D,E,F), the equation f=0 has at most 3 solutions in S.

KEY ALGEBRAIC IDEA: consider the "evaluation map"
    S -> F_q^3,  p -> (x_p, y_p, x_p^2+y_p^2)
Then a circle through 4 points of S corresponds to 4 points of S lying on a
common affine plane in F_q^3 (the plane x^2+y^2 = -Dx-Ey-F, i.e. the graph of
a linear function on (x,y)).

Wait: the condition f(p)=0 for all 4 points means the 4 points
(x_p, y_p, x_p^2+y_p^2) lie on the plane Z = -D X - E Y - F in F_q^3.

So: S is safe iff no 4 points of the lifted set
    S' = {(x, y, x^2+y^2) : (x,y) in S}  subset F_q^3
lie on a common affine plane of the form Z = aX + bY + c.

But ANY 4 points in F_q^3 lie on a plane iff they are affinely dependent.
The planes of the form Z = aX+bY+c are exactly the "non-vertical" planes.

So the condition is: no 4 points of S' lie on a non-vertical plane.

Now, 4 points of S' lie on a non-vertical plane iff the 4x4 determinant
    det[[x_i, y_i, x_i^2+y_i^2, 1]] = 0
which is exactly our original condition.  So this is just a restatement.

BUT: the lifted set S' lies on the paraboloid Z = X^2+Y^2.  This is a
2-dimensional algebraic surface.  The condition "no 4 points on a plane" is
a "cap" condition on the paraboloid.

KNOWN RESULT: caps on the paraboloid (no 4 coplanar) correspond to
"no 4 concyclic or collinear" in the plane.  The maximum size of such a set
in F_q^2 is exactly K.

This is a known problem in finite geometry!  Let me look for the known bounds.

Actually, the condition "no 4 points of the paraboloid coplanar" is equivalent
to "the set is a cap in the sense of no 4 on a plane".  For the paraboloid
over F_q, this is related to "arcs" in the inversive plane.

Let me instead try a DIRECT algebraic bound using the polynomial method.

POLYNOMIAL METHOD: Let S be a safe set of size k.  Consider the polynomial
    P(X,Y) = prod_{p in S} (X - x_p)
of degree k in X.  Hmm, that does not capture the circle condition.

Better: consider the space of polynomials of degree <= d vanishing on S.
If k is large, there are many such polynomials, and we can find one of a
special form that gives a circle through 4 points.

Specifically: the space of polynomials of degree <= 2 in (X,Y) has dimension 6
(1, X, Y, X^2, XY, Y^2).  The circles are the degree-2 polynomials with
X^2 and Y^2 having equal coefficients and XY coefficient 0: a 3-dimensional
subspace (D, E, F).

A circle through 4 points of S exists iff the evaluation map
    V = span{1, X, Y, X^2+Y^2}  (dimension 4)
restricted to S has a kernel of dimension >= 1 when we look for a nonzero
element vanishing on 4 points.

Hmm, let me think again.  The circle condition for 4 points is
    det[[x_i, y_i, x_i^2+y_i^2, 1]] = 0.
This is a 4x4 determinant.  For a set S of size k, we want NO 4-subset to
have this determinant zero.

Consider the vectors v_p = (x_p, y_p, x_p^2+y_p^2, 1) in F_q^4.  The condition
is that no 4 of these vectors are linearly dependent.

So S is safe iff the k vectors {v_p} are in "general position" (no 4 dependent)
in F_q^4.

NOW: this is a classical problem!  A set of vectors in F_q^4 with no 4 linearly
dependent is related to "caps" and to MDS codes.

KEY: if no 4 are dependent, then in particular no 3 are dependent (since 3
dependent + any 4th would be 4 dependent... no, that is not right: 3 dependent
means they span a 2-space, and adding a 4th gives 4 vectors in a 3-space, which
are dependent.  So yes: no 4 dependent implies no 3 dependent).

Wait, that is important!  If 3 vectors are dependent, then those 3 plus any
other vector are 4 vectors in a space of dimension <= 3, hence dependent.
So "no 4 dependent" implies "no 3 dependent".

But "no 3 dependent" means the vectors are in general position in the sense
that any 3 are independent.  In F_q^4, a set of vectors with any 3 independent
is exactly a "cap" / an MDS code of length k and dimension... 

Actually: a set of k vectors in F_q^4 with any 3 linearly independent
corresponds to a [k, 3] MDS code?  Let me think: the vectors v_p are columns of
a 4 x k matrix.  Any 3 columns independent means the matrix is a generator
matrix of an MDS code with d = k-3+1... 

Hmm, let me be careful.  A 4 x k matrix M with any 3 columns independent.
The code C = {M^T a : a in F_q^4} is a [k, 4] code.  Any 3 columns independent
means the minimum distance is >= 4 (since a codeword of weight <= 3 would mean
3 columns dependent).  So C is a [k, 4, >=4] code.

Singleton bound: d <= k - 4 + 1 = k - 3.  So d >= 4 requires k >= 7.
And for MDS (d = k-3), we need k <= q+1 (for q prime power, MDS codes of
dimension 4 exist up to length q+1).

So: a safe set of size k gives a [k, 4, >=4] code over F_q.  The Singleton
bound gives k >= 7 for d >= 4, which is a LOWER bound on k, not upper.

Hmm, that does not give an upper bound.  Let me reconsider.

Actually the constraint is stronger: the vectors v_p = (x, y, x^2+y^2, 1) lie on
the "paraboloid" in F_q^4, i.e. the 3rd coordinate is determined by the first
two.  So the set is not an arbitrary code.

Let me use this: the map p -> (x_p, y_p) is injective (points are distinct).
So the first two coordinates already determine the point.

The condition "no 4 dependent" for vectors (x,y,x^2+y^2,1):
4 vectors dependent iff det = 0 iff the 4 points are concyclic or collinear.

So the algebraic restatement is exact but does not immediately give a bound.

Let me try the polynomial method properly.

POLYNOMIAL METHOD: Suppose S is safe with |S| = k.  Consider the space of
polynomials of the form
    Q(X,Y) = A(X,Y)(X^2+Y^2) + B(X,Y)
where deg A <= d-2, deg B <= d-1.  Hmm.

Let me instead look up the known result: the maximum size of a set in F_q^2 with
no 4 concyclic or collinear.  This is the "no-four-on-a-circle" problem over
finite fields.  Let me search my memory: for the inversive plane of order q,
a set with no 4 concyclic is called a "3-arc" or "cap" in the inversive plane.
The maximum size of a cap in the inversive plane of order q is known to be
q+1 for q odd (I think), achieved by a circle minus... no.

Actually: in the inversive plane of order q, a set meeting every circle in at
most 3 points.  Since every 3 points determine a circle, a set of size k has
C(k,3) triples, each on a distinct circle.  The circles number q(q^2+1).
So C(k,3) <= q(q^2+1), giving k = O(q).

The known exact value: I recall that the maximum size of a "3-arc" in the
inversive plane of order q is q+1 for q even and q+1 or q+2 for q odd.
Hmm, but our computed K for the inversive plane is 5,5,6,6,7,9,9,10 for
q=3,4,5,7,8,9,11,13.  That is much less than q+1 for large q (q=13 gives 10 < 14).

So the "3-arc" maximum is NOT q+1.  Let me reconsider: a 3-arc in the inversive
plane is a set with no 4 concyclic, which is exactly our safe set.  And the
maximum is what we computed.

Let me just document the algebraic reformulation and note that it does not
immediately give a better bound, but connects to coding theory (MDS codes).
"""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    print("ALGEBRAIC REFORMULATION")
    print("=" * 60)
    print()
    print("Lift each point p=(x,y) to v_p = (x, y, x^2+y^2, 1) in F_q^4.")
    print("Then 4 points are concyclic or collinear")
    print("  <=> det[v_p1, v_p2, v_p3, v_p4] = 0")
    print("  <=> the 4 vectors are linearly dependent.")
    print()
    print("So S is safe  <=>  no 4 of the vectors {v_p} are dependent.")
    print()
    print("CONSEQUENCE: no 3 are dependent either")
    print("  (3 dependent + any 4th => 4 dependent).")
    print()
    print("So the 4 x k matrix with columns v_p has any 3 columns independent.")
    print("This is a parity-check matrix of a [k, k-4, >=4] code over F_q.")
    print()
    print("Singleton bound: d <= k - 4 + 1, so d >= 4 needs k >= 7.")
    print("That is a LOWER bound on k, not an upper bound.")
    print()
    print("The extra structure (3rd coordinate = x^2+y^2) is what limits k.")
    print()
    print("=" * 60)
    print("KNOWN CONNECTION: '3-arcs' in the inversive plane")
    print()
    print("A set meeting every circle in at most 3 points is called a 3-arc")
    print("(or cap) in the inversive plane.  Our K is exactly the max 3-arc size.")
    print()
    print(f"{'q':>3} {'our K (inversive)':>18} {'q+1':>5}")
    INV = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 10}
    rows = []
    for q, k in sorted(INV.items()):
        rows.append({"q": q, "K": k, "q_plus_1": q + 1})
        print(f"{q:>3} {k:>18} {q+1:>5}")
    print()
    print("our K is well below q+1 for q >= 9, so the max 3-arc is NOT q+1.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
