"""A weighted counting bound using block sizes.

The triple bound is C(k,3) <= b (number of blocks).  It ignores block sizes.

But a block of size s can host at most C(s,3) triples of S (if |S cap B| = 3,
it hosts exactly 1 triple; the C(s,3) is the number of triples of B, not of S).

Hmm, that is not the right direction.  Let me think again.

For a safe set S, each triple of S lies on exactly one block.  So
    C(k,3) = #{(B, triple) : triple of S on B} = #blocks containing 3 points of S.

The blocks containing 3 points of S are a subset of all blocks.  So C(k,3) <= b.

Now, can we use sizes?  A block of size s contains C(s,3) triples of the BOARD.
The triples of S that lie on B are at most 1 (since |S cap B| <= 3).

So: sum over blocks B of (number of triples of S on B) = C(k,3).
And each term is 0 or 1.

Alternatively: sum over blocks B of C(|S cap B|, 3) = C(k,3) (each triple on
exactly one block, and C(3,3)=1).

Now consider the "pair" version:
    sum over blocks B of C(|S cap B|, 2) = lambda_2 * C(k,2)
Since |S cap B| <= 3, C(|S cap B|,2) <= 3, giving lambda_2 C(k,2) <= 3b.
That is the pair bound (weaker than lambda_2 + 2).

Let me try a WEIGHTED version: weight each block by 1/C(s,3) or similar.

Hmm.  Let me think about what quantity would capture the size effect.

KEY IDEA: consider the number of triples of the BOARD that lie on some block.
    T = #{(B, triple of B)} = sum over B of C(|B|, 3).
For a safe set S, all C(k,3) triples of S are among these T triples (each on
exactly one block).  So C(k,3) <= T.  But T is huge (much bigger than b), so
this is weaker than C(k,3) <= b.

Hmm, that is the wrong direction.

Let me think about the "complement": triples of S that are NOT on any block.
For a safe set, every triple IS on a block (trivially, since 3 points determine
a circle or line).  So there are no such triples.

OK so the triple bound is the natural one.

Let me try a different weighting: count (block, pair of S) incidences, but weight
by the block size.

    sum over B of |B| * C(|S cap B|, 2) = ?

Each pair {a,b} of S lies on lambda_2 blocks.  For each such block B, the
contribution is |B|.  So
    sum over B of |B| * C(|S cap B|, 2) = sum over pairs {a,b} of S of
        sum over blocks B through a,b of |B|.

Let mu_2 = sum over blocks through a pair of |B|.  Then
    mu_2 * C(k,2) = sum over B of |B| * C(|S cap B|, 2).

Since |S cap B| <= 3, C(|S cap B|,2) <= 3, so
    mu_2 * C(k,2) <= 3 * sum over B of |B| = 3 * (total incidences).

For AG(2,q): total incidences = sum over B of |B|.
    = q(q+1)*q + (number of circles)*(circle size)
For q=7: 56*7 + 294*8 = 392 + 2352 = 2744.
mu_2 = sum over blocks through a pair of |B|.  For q=7: 1 line (size 7) + 6 circles (size 8) = 7 + 48 = 55.
So 55 * C(k,2) <= 3 * 2744 = 8232.
C(k,2) <= 149.7, k <= 17.8, so k <= 17.
Weaker than q+3=10.

Hmm.

Let me try yet another weighting.  What if we weight by 1/(s-2) or similar?

Actually, let me revisit the lambda_2 bound proof and see if the size enters.

The lambda_2 bound: fix p,q in S.  The pencil through p,q has lambda_2 blocks.
Each r in S\\{p,q} needs a distinct block.  So k-2 <= lambda_2.

The size of the blocks in the pencil does not enter!  That is why the bound is
q+3 regardless of sizes.

To use sizes, we would need to show that some blocks in the pencil CANNOT
contain a third point of S.  That would happen if the block is "too small" or
if its other points are already excluded.

Hmm, for a block B through p,q of size s, the number of other points is s-2.
If S has k points and k-2 of them must be on distinct blocks, then...

Actually here is an idea: the blocks through p,q are DISJOINT outside {p,q}
(two circles through p,q meet only in p,q).  So the union of the pencil has
1 + sum over B of (|B|-2) points.  If S\\{p,q} is contained in this union, then
    k-2 <= sum over B of (|B|-2) = (total size of pencil) - 2*lambda_2.

For AG(2,q): the pencil through p,q has 1 line (size q) and q circles (size q+1).
Sum of (|B|-2) = (q-2) + q*(q-1) = q-2 + q^2-q = q^2-2.
So k-2 <= q^2-2, i.e., k <= q^2.  Very weak.

So the size-based bound via the pencil is weak.

CONCLUSION: the block size effect is real (empirically) but does not translate
into a better bound via these counting arguments.  The lambda_2 bound q+3
remains the best.

Let me document this analysis.
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        n = len(pts)
        b = len(blocks)
        total_inc = sum(len(x) for x in blocks)
        # mu_2 = sum over blocks through a pair of |B|
        # compute for one pair
        pair = (blocks[0][0], blocks[0][1])
        mu2 = sum(len(blocks[bi]) for bi in range(b)
                  if pair[0] in blocks[bi] and pair[1] in blocks[bi])
        # bound: mu2 * C(k,2) <= 3 * total_inc
        rhs = Fraction(3 * total_inc, mu2)
        k = 2
        while Fraction(k * (k + 1), 2) <= rhs:
            k += 1
        # pencil size bound: k-2 <= sum over pencil of (|B|-2)
        pencil = [bi for bi in range(b) if pair[0] in blocks[bi] and pair[1] in blocks[bi]]
        pencil_sum = sum(len(blocks[bi]) - 2 for bi in pencil)
        rows.append({"q": q, "blocks": b, "total_incidences": total_inc,
                     "mu2": mu2, "weighted_bound": k,
                     "pencil_size_sum": pencil_sum,
                     "pencil_bound": pencil_sum + 2})
        print(f"q={q}: b={b}, total_inc={total_inc}, mu2={mu2}", flush=True)
        print(f"   weighted pair bound: K <= {k}", flush=True)
        print(f"   pencil size bound: K <= {pencil_sum + 2}", flush=True)
        print(f"   lambda_2 bound: K <= {q+3}", flush=True)

    print()
    print("all size-based bounds are weaker than lambda_2 + 2 = q+3.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
