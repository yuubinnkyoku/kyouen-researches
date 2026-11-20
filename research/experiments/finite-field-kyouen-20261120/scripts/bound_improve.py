"""Can we improve K <= lambda_2 + 2 = q + 3?

The proof used: fix p,q in S.  For each r in S\\{p,q}, the triple {p,q,r} lies on
a block through p and q.  Different r give different blocks, so k-2 <= lambda_2.

The bound is loose because it only uses ONE pair {p,q}.  Let us use ALL pairs.

For each pair {p,q} in S, let B(p,q) be the set of blocks through p and q that
contain a third point of S.  We showed |B(p,q)| = k-2 (one for each r).

Now count pairs (block, pair) where the block contains the pair and a third
point of S:
    sum over blocks B with |S cap B| = 3 of C(3,2) = 3 * (#full blocks)
    = 3 * C(k,3)     (each triple is on exactly one block)
On the other hand, summing over pairs {p,q} of S:
    sum over pairs of |B(p,q)| = C(k,2) * (k-2) = 3*C(k,3).
Consistent, no new information.

Let us use the structure of the pencil more carefully.  For a pair {p,q}, the
lambda_2 blocks through them are partitioned into:
  - k-2 blocks that contain a third point of S (the "full" ones),
  - lambda_2 - (k-2) blocks that contain no other point of S.

For the latter blocks, they contain exactly p and q from S.  Now consider a
third point r in S.  The block through {p,q,r} is one of the full ones.

Hmm.  Let me try a different tack: use the fact that the full blocks through
DIFFERENT pairs must be consistent.

Consider three points p,q,r in S.  They determine a block B(p,q,r).  Now take
a fourth point s in S.  The triples {p,q,s}, {p,r,s}, {q,r,s} determine blocks
B(p,q,s), B(p,r,s), B(q,r,s).  These are all distinct from B(p,q,r) (different
triples).

Now, B(p,q,r) contains p,q,r.  B(p,q,s) contains p,q,s.  Both contain p and q.
So they are two distinct blocks through p and q.  Fine.

But consider: B(p,q,r) and B(p,q,s) both contain p,q.  Their union has
3+3-2 = 4 points of S.  That is allowed (they are different blocks).

Let me look for a counting argument on the "blocks through a point".

For a point p in S, the blocks through p that contain 2 other points of S
number C(k-1,2) (one per pair).  These are all distinct.

The blocks through p that contain exactly 1 other point of S: for each q,
the pencil through p,q has lambda_2 blocks, of which k-2 contain a third point
of S.  So lambda_2 - (k-2) blocks through p,q contain only p,q from S.

Total blocks through p containing exactly one other point of S:
    sum over q of (lambda_2 - (k-2)) = (k-1)(lambda_2 - k + 2).

Total blocks through p: deg(p) = q^2 + q for AG(2,q).

So:
    C(k-1,2) + (k-1)(lambda_2 - k + 2) <= deg(p)
    (k-1)[(k-2)/2 + lambda_2 - k + 2] <= q^2+q
    (k-1)[lambda_2 + 2 - k + (k-2)/2] <= q^2+q
    (k-1)[lambda_2 + 2 - k/2 - 1] <= q^2+q
    (k-1)[lambda_2 + 1 - k/2] <= q^2+q

With lambda_2 = q+1:
    (k-1)[q + 2 - k/2] <= q^2 + q

For k ~ q, the left side is ~ q * (q/2) = q^2/2 < q^2+q.  So this gives no
constraint for k ~ q.  It only bites when k is close to 2(q+2).

So this route gives k <= 2q + 4 roughly.  Weaker than q+3.

CONCLUSION: the bound q+3 seems hard to improve with these counting arguments.
The gap between q+3 and the observed K (~0.7q to 1.0q) may require a genuinely
different idea.

Let me instead check: is the bound q+3 TIGHT for some q?  If K = q+3 for some q,
the bound is sharp.  From the data, K/q is at most 1.20 (q=5, K=6, q+3=8).
So the bound is not tight anywhere yet.

Let me look at the problem from the "complement" side: what does a safe set of
size close to q+3 look like?  Maybe it is impossible for structural reasons
that we can identify.
"""

from __future__ import annotations

import argparse
import json
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7, 9, 11])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    K_DATA = {3: 5, 5: 6, 7: 6, 9: 9, 11: 9}
    rows = []
    print(f"{'q':>3} {'deg':>6} {'lam2':>5} {'K':>3} {'q+3':>4} {'K/(q+3)':>8} "
          f"{'deg-bound':>10}")
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        n = len(pts)
        deg = len(through[0])
        lam2 = q + 1
        k = K_DATA.get(q)
        # the degree-based bound: (k-1)[lam2 + 1 - k/2] <= deg
        # solve for the largest k satisfying it
        kd = 2
        while (kd) * (lam2 + 1 - (kd + 1) / 2) <= deg:
            kd += 1
        rows.append({"q": q, "degree": deg, "lambda2": lam2, "K": k,
                     "q_plus_3": q + 3,
                     "ratio": (k / (q + 3)) if k else None,
                     "degree_bound": kd})
        print(f"{q:>3} {deg:>6} {lam2:>5} {k if k else '-':>3} {q+3:>4} "
              f"{(k/(q+3) if k else 0):>8.2f} {kd:>10}")

    print()
    print("the degree-based bound is ~2q, weaker than q+3.")
    print("the bound q+3 is not tight for any computed q (K/(q+3) <= 0.75).")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
