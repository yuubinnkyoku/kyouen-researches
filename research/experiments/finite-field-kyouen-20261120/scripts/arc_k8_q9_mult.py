"""k=8 at q=9: is the multiplicity theorem the problem?

The profile formula is exact at q=9 (500/500 verified).  So the gap must
be in the multiplicity division or in the assembly.

The multiplicity theorem says:
    #8-sets with profile P = tuples(P) / (#4-circles in P) * b

Let me test this DIRECTLY at q=9: for a sample of 8-sets, compute their
profile and check that the tuple loop counts each set exactly n4 times.

Actually, the cleanest test: compute the number of 8-sets with a given
profile by EXHAUSTIVE enumeration at q=9 -- but C(82,8) = 3.6e10 is too
big.

ALTERNATIVE: test the identity
    b * (tuples for fixed C) = sum over S of #4-circles(S)
at q=9.  If this fails, the multiplicity scaling is wrong.

Run:  python arc_k8_q9_mult.py --q 9
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field, build_inversive_plane  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[9])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, sub = build_field(q)
        points, circles = build_inversive_plane(q)
        idx = {p: i for i, p in enumerate(points)}
        blocks = [tuple(sorted(idx[p] for p in c)) for c in circles]
        n = len(points)
        b = len(blocks)
        s = q + 1
        base = set(sub) | {None}
        ci = None
        for k, B in enumerate(blocks):
            if set(points[i] for i in B) == base:
                ci = k
                break
        B = blocks[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]

        # LHS: b * (number of (T, X) tuples for the fixed C)
        lhs = b * comb(s, 4) * comb(n - s, 4)

        # RHS: sum over 8-sets of #4-circles -- too big to enumerate.
        # Instead: sum over circles D of #{8-sets whose 4-circle set
        # includes D}.  That is sum over D of #{S : D subset S, |S|=8}
        # = b * C(n-s, 4) ... but that counts S once per 4-circle, which
        # is exactly the RHS.
        #
        # So RHS = sum over D of C(n-s,4) = b * C(n-s,4).
        # And LHS = b * C(s,4) * C(n-s,4).
        #
        # These differ by the factor C(s,4)!  So the tuple loop counts
        # each (S, D) pair C(s,4) times, not once.

        rhs = b * comb(n - s, 4)
        row = {"q": q, "n": n, "b": b, "s": s,
               "lhs": lhs, "rhs": rhs,
               "ratio": lhs // rhs if rhs else None,
               "C(s,4)": comb(s, 4)}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  LHS = b*C(s,4)*C(n-s,4) = {lhs}", flush=True)
        print(f"  RHS = b*C(n-s,4)        = {rhs}", flush=True)
        print(f"  ratio = {lhs//rhs}  (C(s,4) = {comb(s,4)})", flush=True)
        print(f"  ratio == C(s,4): {lhs//rhs == comb(s,4)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
