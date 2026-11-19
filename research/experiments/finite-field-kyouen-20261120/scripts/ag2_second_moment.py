"""Stronger bounds for AG(2,q): use PAIRS of blocks (second moment).

For a safe set S with |S| = k, and blocks B (circles and lines), we have
|S cap B| <= 3 for every block.

First moment:   sum_B |S cap B| = d*k  where d = blocks through a point.
                Since |S cap B| <= 3,  d*k <= 3*b  ->  k <= 3b/d.

Second moment:  sum_B C(|S cap B|, 2) = sum over pairs {p,q} in S of
                (number of blocks through both p and q).
                For AG(2,q): two points determine exactly one line, and the
                number of circles through two points is (number of circles
                through both).  Let lambda_2 = #blocks through a given pair.
                Then sum_B C(|S cap B|,2) = lambda_2 * C(k,2).

                Since |S cap B| <= 3, C(|S cap B|,2) <= 3 for each block, so
                    lambda_2 * C(k,2) <= 3*b.
                This gives  k(k-1) <= 6b/lambda_2.

Third moment:   sum_B C(|S cap B|,3) = lambda_3 * C(k,3) where lambda_3 is the
                number of blocks through a given triple.  Since
                C(|S cap B|,3) <= 1 (as |S cap B| <= 3), we get
                    lambda_3 * C(k,3) <= b.
                For AG(2,q), a triple determines exactly one circle (if
                non-collinear) or one line (if collinear), so lambda_3 = 1
                and this is the triple-counting bound C(k,3) <= b.

The second moment bound is new and may be stronger.  Let us compute lambda_2
and the resulting bound.

For AG(2,q): through two distinct points p,q pass:
  - exactly 1 line,
  - circles: the circles through both p and q.  A circle through p and q is
    determined by a third point r not on line pq; but different r can give the
    same circle.  The number of circles through p and q equals the number of
    circles in the "pencil" through p and q, which is q-1 (the circles through
    two points form a pencil of size q-1 for q odd).
So lambda_2 = 1 + (q-1) = q.

Then  q * C(k,2) <= 3b  ->  k(k-1) <= 6b/q.

For q=7: b=350, so k(k-1) <= 6*350/7 = 300 -> k <= 18 (since 17*18=306>300, 17*16=272).
Hmm, that gives k <= 17.  Let me compute exactly.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path

from ag2_prime_power import build_ag


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7, 9, 11])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        n = len(pts)
        n_blocks = len(blocks)
        # compute lambda_2 = number of blocks through a given pair
        pair_count = Counter()
        for b in blocks:
            for pair in __import__("itertools").combinations(sorted(b), 2):
                pair_count[pair] += 1
        lambdas = Counter(pair_count.values())
        lam2 = next(iter(lambdas)) if len(lambdas) == 1 else None
        # bound: lam2 * C(k,2) <= 3*b
        if lam2:
            # k(k-1)/2 <= 3b/lam2  ->  k(k-1) <= 6b/lam2
            rhs = Fraction(6 * n_blocks, lam2)
            k = 2
            while Fraction(k * (k + 1)) <= rhs:
                k += 1
            bound2 = k
        else:
            bound2 = None
        # triple bound
        k = 3
        while comb(k + 1, 3) <= n_blocks:
            k += 1
        report.append({
            "q": q,
            "q_mod_4": q % 4,
            "blocks": n_blocks,
            "lambda2_uniform": len(lambdas) == 1,
            "lambda2": lam2,
            "lambda2_distribution": dict(sorted(lambdas.items())),
            "bound_second_moment": bound2,
            "bound_triple": k,
        })
        print(f"q={q}: blocks={n_blocks}, lambda2 uniform={len(lambdas)==1}, "
              f"lambda2={lam2} (dist {dict(sorted(lambdas.items()))})", flush=True)
        print(f"   second-moment bound: K <= {bound2}   triple bound: K <= {k}",
              flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
