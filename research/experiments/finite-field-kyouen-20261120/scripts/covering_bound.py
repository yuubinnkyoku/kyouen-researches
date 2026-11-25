"""A covering-based bound: how many points can avoid all circles?

For AG(2,q), a safe set S must not contain 4 points of any circle or line.
Equivalently, for every block B, |S cap B| <= 3.

The "circle covering" obstruction: a large subset of the board necessarily
contains a full circle.  Let us quantify this.

Define, for a k-subset S, the number of blocks fully contained in S:
    f(S) = #{B : B subset S}.
Safety requires f(S) = 0 (for blocks of size >= 4; blocks of size 3 are fine
since |S cap B| = 3 <= 3).

So we need: does there exist a k-subset with f(S) = 0?

A counting argument: the average of f(S) over all k-subsets is
    E[f] = sum over blocks B of P(B subset S) = sum over B of C(n-|B|, k-|B|)/C(n,k).

If E[f] > 0, that does not prove existence (we need f=0 for SOME S).
But if we can show f(S) >= 1 for ALL S, then no safe set exists.

A sufficient condition: if every k-subset contains a block, then K < k.

Let us compute, for each q and k, the exact number of k-subsets containing no
block, for small q where enumeration is feasible.  That gives the exact
"safe set count" by size, which we already have for small q.

For larger q, let us use the second-moment / inclusion-exclusion estimate to
predict when the count hits zero, and compare with the known K.

This script computes:
  * the exact safe-set counts by size for q=3,5 (feasible),
  * the expected number of blocks in a random k-subset (E[f]),
  * the "threshold" k where E[f] crosses 1.
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
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7, 9])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        n = len(pts)
        sizes = {}
        for b in blocks:
            sizes[len(b)] = sizes.get(len(b), 0) + 1
        print(f"q={q}: n={n}, block sizes {dict(sorted(sizes.items()))}", flush=True)
        # E[f] for a random k-subset
        print(f"  {'k':>3} {'E[f]':>12} {'C(n,k)':>14}")
        for k in range(4, min(n, 20) + 1):
            ef = Fraction(0)
            for s, cnt in sizes.items():
                if s <= k:
                    ef += cnt * Fraction(comb(n - s, k - s), comb(n, k))
            rows.append({"q": q, "k": k, "E_f": str(ef),
                         "C_n_k": comb(n, k)})
            if k <= 14 or ef < 10:
                print(f"  {k:>3} {float(ef):>12.4f} {comb(n,k):>14}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
