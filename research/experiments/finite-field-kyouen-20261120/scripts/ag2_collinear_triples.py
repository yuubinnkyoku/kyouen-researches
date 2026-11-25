"""The strongest elementary bound: use the LINE structure alone.

Every safe set meets every line in at most 3 points.  AG(2,q) has q(q+1) lines,
each of size q, and every point is on q+1 lines.

Double counting pairs (point, line through it):
    sum over lines of |S cap L| = (q+1) k
Since |S cap L| <= 3:
    (q+1) k <= 3 q(q+1)  ->  k <= 3q.

That is weak (k <= 3q).

But we can do better using PAIRS of lines.  Two lines meet in at most 1 point.
For a safe set S, consider the "line profile" (a_L) = |S cap L|.  We have
    sum_L a_L = (q+1)k
    sum_L C(a_L,2) = sum over pairs {p,q} in S of (number of lines through both)
                   = 1 * C(k,2)      (two points determine exactly one line)
    sum_L C(a_L,3) = sum over triples of collinear triples in S
                   <= C(k,3)         (each collinear triple on exactly one line)

Since a_L <= 3, C(a_L,3) <= 1 and C(a_L,2) <= 3.

The third identity is the interesting one: it says the number of collinear
triples in S equals sum_L C(a_L,3) <= #lines = q(q+1).

So a safe set of size k has at most q(q+1) collinear triples.  If we can lower
bound the number of collinear triples in ANY k-subset of AG(2,q), we get a bound.

This is a known problem: the minimum number of collinear triples in a k-subset
of AG(2,q).  For k small relative to q, a random k-set has about
C(k,3)/q collinear triples (since a random triple is collinear with probability
~1/q).  Setting C(k,3)/q <= q(q+1) gives k^3/6 <= q^2(q+1), i.e. k <= (6q^3)^{1/3}
= q * 6^{1/3} ~ 1.82 q.  That is weaker than the cross bound but applies to all q.

Let us compute the exact minimum number of collinear triples for small q by
exhaustive search over k-subsets, to see how strong this bound really is.
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
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5])
    ap.add_argument("--k", type=int, nargs="+", default=[4, 5, 6])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        n = len(pts)
        # lines only: blocks of size q
        lines = [b for b in blocks if len(b) == q]
        line_set = [frozenset(b) for b in lines]
        for k in args.k:
            if comb(n, k) > 3_000_000:
                print(f"q={q} k={k}: too many subsets ({comb(n,k)}), skipped",
                      flush=True)
                continue
            min_triples = None
            max_triples = 0
            for S in itertools.combinations(range(n), k):
                Sset = set(S)
                triples = 0
                for L in line_set:
                    c = len(L & Sset)
                    if c >= 3:
                        triples += comb(c, 3)
                if min_triples is None or triples < min_triples:
                    min_triples = triples
                if triples > max_triples:
                    max_triples = triples
            report.append({
                "q": q, "k": k,
                "min_collinear_triples": min_triples,
                "max_collinear_triples": max_triples,
                "num_lines": len(lines),
            })
            print(f"q={q} k={k}: collinear triples range "
                  f"[{min_triples}, {max_triples}] over all C({n},{k}) subsets "
                  f"(#lines={len(lines)})", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
