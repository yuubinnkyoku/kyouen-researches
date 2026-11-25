"""Multi-pair interference: can three pencils give a better bound?

Fix three points p,q,r in S.  Consider the three pencils:
    P(p,q): lambda_2 blocks through p and q,
    P(p,r): lambda_2 blocks through p and r,
    P(q,r): lambda_2 blocks through q and r.

For each s in S\\{p,q,r}, the triples {p,q,s}, {p,r,s}, {q,r,s} determine three
blocks, one in each pencil.  Different s give different blocks in each pencil.

So each pencil needs at least k-3 blocks (beyond the block B(p,q,r) which is in
all three pencils).

Now, can the SAME block serve two different pencils?  A block in P(p,q) and
P(p,r) must contain p,q,r -- that is B(p,q,r).  So apart from B(p,q,r), the
three pencils are DISJOINT.

Therefore the three pencils together contain at least
    1 + 3(k-3) = 3k - 8
distinct blocks.

But each pencil has only lambda_2 blocks, so the three pencils have at most
3*lambda_2 blocks in total.  Hence
    3k - 8 <= 3*lambda_2
    k <= lambda_2 + 8/3

That is WORSE than k <= lambda_2 + 2 (since 8/3 > 2).  Hmm.

Wait, I need to be careful.  The three pencils are disjoint apart from
B(p,q,r), so the union has size 3*lambda_2 - 2 (subtracting the double-counted
B(p,q,r) three times, adding back once: 3*lambda_2 - 3 + 1 = 3*lambda_2 - 2).

And the union must contain B(p,q,r) plus 3(k-3) distinct blocks from the s's.
So
    1 + 3(k-3) <= 3*lambda_2 - 2
    3k - 8 <= 3*lambda_2 - 2
    3k <= 3*lambda_2 + 6
    k <= lambda_2 + 2

Same bound!  No improvement.

Let me try FOUR points p,q,r,t.  The six pencils P(p,q), P(p,r), ..., P(r,t).
For each s in S\\{p,q,r,t}, the 6 triples {p,q,s}, ..., {r,t,s} give 6 blocks,
one in each pencil, all distinct (a block in two pencils would need to contain
3 of the 4 points, i.e. be B of a triple of the 4).

The pencils pairwise intersect in the blocks B(x,y,z) for triples of the 4
points.  There are C(4,3) = 4 such blocks.  Each is in 3 of the 6 pencils.

Inclusion-exclusion: |union| = 6*lambda_2 - (sum of pairwise intersections)
+ (triple intersections) - ...
Pairwise intersections: each pair of pencils shares exactly one block (the
B of the 3 points they have in common).  C(6,2) = 15 pairs, but only 4 distinct
blocks are shared, each shared by 3 pencils, contributing C(3,2) = 3 pairs each.
So 4*3 = 12 pairs have a shared block, and 3 pairs (the ones with only 2 points
in common... wait, two pencils P(a,b) and P(c,d) share a block only if the
block contains all of a,b,c,d, impossible for a block with <= 3 points of S
unless {a,b} = {c,d}).

Hmm, P(p,q) and P(p,r) share blocks containing p,q,r -- exactly one, B(p,q,r).
P(p,q) and P(r,t) share blocks containing p,q,r,t -- impossible (4 points).
So the pairwise intersections are exactly the 4 blocks B(x,y,z), each shared by
the 3 pencils among {x,y,z}.

|union| = 6*lambda_2 - 4*3 + (triple intersections) - ...
Triple intersections: three pencils sharing a block.  P(p,q), P(p,r), P(p,s)
share B(p,q,r)? No, B(p,q,r) is in P(p,q), P(p,r), P(q,r) -- three pencils.
So each B(x,y,z) is in exactly 3 pencils, contributing 1 to the triple
intersection count.  There are 4 such blocks.  Higher intersections: 0.

|union| = 6*lambda_2 - 12 + 4 = 6*lambda_2 - 8.

The union must contain the 4 blocks B(x,y,z) plus 6(k-4) blocks from the s's.
So
    4 + 6(k-4) <= 6*lambda_2 - 8
    6k - 20 <= 6*lambda_2 - 8
    6k <= 6*lambda_2 + 12
    k <= lambda_2 + 2

SAME BOUND AGAIN.  It seems the bound lambda_2 + 2 is stable under this
generalisation.  That suggests it might be essentially tight for this method.

Let me verify the pattern: with m points, the bound is always lambda_2 + 2.
That would mean the method cannot be improved.

This script documents the computation.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import comb
from pathlib import Path


def multi_pair_bound(m: int, lam2: int) -> Fraction:
    """Bound from m fixed points.

    Pencils: C(m,2).  Blocks B(x,y,z) for triples of the m points: C(m,3),
    each in 3 pencils.
    |union| = C(m,2)*lam2 - 3*C(m,3) + C(m,3)   (pairwise - triple, higher = 0)
            = C(m,2)*lam2 - 2*C(m,3)
    Required: C(m,3) + C(m,2)*(k-m) <= |union|
    """
    pencils = comb(m, 2)
    triples = comb(m, 3)
    union = pencils * lam2 - 2 * triples
    # C(m,3) + C(m,2)*(k-m) <= union
    # C(m,2)*k <= union - C(m,3) + C(m,2)*m
    lhs_coef = pencils
    rhs = union - triples + pencils * m
    return Fraction(rhs, lhs_coef)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    print("bound from m fixed points, as a function of lambda_2:")
    print(f"{'m':>3} {'pencils':>8} {'triples':>8} {'bound':>20}")
    for m in range(3, 9):
        pencils = comb(m, 2)
        triples = comb(m, 3)
        b = multi_pair_bound(m, 0)  # the constant part
        # bound = lam2 + constant
        const = b  # since multi_pair_bound(m, lam2) = lam2 + const
        rows.append({"m": m, "pencils": pencils, "triples": triples,
                     "bound": f"lambda_2 + {const}"})
        print(f"{m:>3} {pencils:>8} {triples:>8} {'lambda_2 + ' + str(const):>20}")

    print()
    print("the bound is lambda_2 + 2 for every m >= 3.")
    print("so the multi-pair generalisation does NOT improve the bound.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
