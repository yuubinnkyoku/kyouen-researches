"""A different route: use the BLOCK SIZE distribution, not pencils.

The pencil argument gives K <= lambda_2 + 2 = q+3.  It is invariant under
multi-pair generalisation.  Let us try a completely different principle.

IDEA: count (block, 3-subset of S) incidences in two ways, but weight blocks
by their size.

For a block B of size s, the number of 3-subsets of S inside B is C(|S cap B|,3)
which is 0 or 1 (since |S cap B| <= 3).  So
    #{(B, triple) : triple of S on B} = #full blocks = C(k,3).
That is the triple bound, saturated.

Now weight by s:  sum over full blocks B of s(B) = sum over triples of s(B(triple)).
Since s(B) <= q+1 (max block size), we get
    sum over full blocks of s(B) <= C(k,3) * (q+1).
Not useful.

DIFFERENT IDEA: use the fact that a block of size s contains C(s,2) pairs, and
each pair of S is in lambda_2 blocks.

Count (block, pair of S) incidences:
    sum over blocks of C(|S cap B|, 2) = lambda_2 * C(k,2).
Since |S cap B| <= 3, C(|S cap B|,2) <= 3, so
    lambda_2 * C(k,2) <= 3 * b.
With lambda_2 = q+1, b = q^3+q:
    (q+1) * k(k-1)/2 <= 3(q^3+q) = 3q(q^2+1)
    k(k-1) <= 6q(q^2+1)/(q+1) = 6q(q-1+2/(q+1)) ~ 6q^2
    k <= sqrt(6) q ~ 2.45q.
Weaker than q+3.

Hmm.  Let me think about what makes the pencil argument sharp.

The pencil argument: fix p,q.  The k-2 points r each need a distinct block
through p,q.  There are lambda_2 such blocks.  So k-2 <= lambda_2.

This is sharp when EVERY block through p,q is used.  For that, we need
k-2 = lambda_2, i.e. k = q+3.

Is k = q+3 achievable?  For q=3: k=6, but K=5.  For q=5: k=8, K=6.
So no.  The bound is not achieved.

WHY not?  Because if all lambda_2 blocks through p,q are used, then for EVERY
pair p,q in S, all lambda_2 blocks through them contain a third point of S.
That is a very strong condition.

Let me count: if all pairs are "saturated", then the number of (pair, block)
incidences where the block contains a third point is lambda_2 * C(k,2).
But each full block contributes C(3,2) = 3 such incidences.
So 3 * C(k,3) = lambda_2 * C(k,2), i.e.
    3 * (k-2)/3 = lambda_2
    k - 2 = lambda_2
    k = lambda_2 + 2.
Consistent.  So saturation requires k = lambda_2 + 2 exactly.

Now, is k = lambda_2 + 2 = q+3 achievable?  Let me test computationally for
small q whether a safe set of size q+3 exists.

q=3: size 6?  K=5, so no.
q=5: size 8?  K=6, so no.
q=7: size 10?  K=6, so no.

So the bound is never achieved for small q.  There must be an additional
obstruction.  Let me look for it.

If k = q+3 and all pairs are saturated, then:
  - every block through any pair of S contains a third point of S,
  - so every block meeting S in >= 2 points meets it in exactly 3.

Consider a block B with |S cap B| = 3, say S cap B = {a,b,c}.  The pairs
{a,b}, {a,c}, {b,c} are all in B.  Each of these pairs has lambda_2 blocks
through it, all saturated.

Now take d in S \ {a,b,c}.  The pair {a,d} has lambda_2 blocks through it, all
containing a third point of S.  One of them is B(a,d,x) for some x.

Hmm, this is getting complex.  Let me just test computationally whether
k = q+3 is achievable for q=3,5,7 by direct search (we know it is not, since
K < q+3).  The question is WHY.

Let me look at the structure of the maximum safe sets and see what prevents
them from reaching q+3.
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
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    K_DATA = {3: 5, 5: 6, 7: 6}
    rows = []
    print(f"{'q':>3} {'K':>3} {'q+3':>4} {'gap':>4} {'b':>6} {'C(K,3)':>8} "
          f"{'full blocks':>12}")
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        k = K_DATA[q]
        b = len(blocks)
        rows.append({"q": q, "K": k, "q_plus_3": q + 3, "gap": q + 3 - k,
                     "blocks": b, "C_K_3": comb(k, 3)})
        print(f"{q:>3} {k:>3} {q+3:>4} {q+3-k:>4} {b:>6} {comb(k,3):>8} "
              f"{comb(k,3):>12}")

    print()
    print("the gap q+3-K is 1, 2, 4 for q=3,5,7.")
    print("the bound is never achieved; there is an additional obstruction.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
