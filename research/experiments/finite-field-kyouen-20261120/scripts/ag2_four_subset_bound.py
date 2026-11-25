"""Higher-order structure: how many blocks pass through 4 points?

For a safe set S, no block carries 4 points of S.  The triple-counting bound
uses lambda_3 = 1 (each triple on exactly one block).  The second-moment bound
uses lambda_2 = q+1 and is weaker.

What about the "4-uniform" structure?  For a 4-subset T of points, let
mu(T) = number of blocks containing T.  For a safe set, mu(T) = 0 for all
4-subsets T of S.  That is the definition of safety, so it gives no bound
directly.

But we can use the COMPLEMENT: count 4-subsets that ARE on a block.  Let
    N4 = number of (block, 4-subset) incidences = sum_B C(|B|,4).
For a safe set S, every 4-subset of S is NOT on any block, so
    C(k,4) <= C(n,4) - (number of 4-subsets on at least one block).
That is a lower bound on the complement, not an upper bound on k.

Better: use the fact that the blocks COVER many 4-subsets.  If the blocks cover
a fraction f of all 4-subsets, then a safe set of size k has all its C(k,4)
4-subsets uncovered, so C(k,4) <= (1-f) C(n,4).  This gives an upper bound on k!

This is a genuine bound.  Let us compute f for AG(2,q).

For AG(2,q):
  - lines: q(q+1) blocks of size q, contributing q(q+1)*C(q,4) incidences
  - circles: q^2(q-1) blocks of size q+1 (for q = 3 mod 4), contributing
    q^2(q-1)*C(q+1,4)
  - but 4-subsets may be on multiple blocks, so the number of DISTINCT covered
    4-subsets is at most the incidence count.

So  #covered <= q(q+1)C(q,4) + q^2(q-1)C(q+1,4).
And  C(k,4) <= C(q^2,4) - #covered  is FALSE (we need the uncovered count to be
at least C(k,4), i.e. #uncovered >= C(k,4)).

Actually: all C(k,4) 4-subsets of S are uncovered, so
    C(k,4) <= #uncovered = C(n,4) - #covered.
Since #covered <= incidence count, #uncovered >= C(n,4) - incidence.
That gives a LOWER bound on #uncovered, hence an UPPER bound on C(k,4) only if
we knew #uncovered exactly.  With the inequality #uncovered >= C(n,4) - inc,
we get C(k,4) <= #uncovered which is not bounded above by that.

So this route needs the EXACT number of covered 4-subsets.  Let us compute it
for small q and see how strong the resulting bound is.
"""

from __future__ import annotations

import argparse
import itertools
import json
from math import comb
from pathlib import Path

from ag2_prime_power import build_ag


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        n = len(pts)
        # exact count of covered 4-subsets
        covered = set()
        for b in blocks:
            if len(b) >= 4:
                for quad in itertools.combinations(sorted(b), 4):
                    covered.add(quad)
        n_covered = len(covered)
        n_uncovered = comb(n, 4) - n_covered
        # bound: C(k,4) <= n_uncovered
        k = 4
        while comb(k + 1, 4) <= n_uncovered:
            k += 1
        report.append({
            "q": q,
            "points": n,
            "blocks": len(blocks),
            "C(n,4)": comb(n, 4),
            "covered_4subsets": n_covered,
            "uncovered_4subsets": n_uncovered,
            "fraction_covered": n_covered / comb(n, 4) if comb(n, 4) else None,
            "K_upper_from_4subsets": k,
        })
        print(f"q={q}: n={n}, C(n,4)={comb(n,4)}, covered={n_covered} "
              f"({100*n_covered/comb(n,4):.2f}%), uncovered={n_uncovered}", flush=True)
        print(f"   bound from 4-subsets: C(k,4) <= {n_uncovered} -> K <= {k}",
              flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
