"""k=8: re-derive the assembly from first principles.

The assembly must count, for each 8-set S, whether it has a 4-circle.

DIRECT APPROACH (no multiplicity tricks):
    #8-arcs = C(n,8) - #{S : S has a 4-circle}

And #{S : S has a 4-circle} can be computed by summing over 4-circles D:
    #{S : D subset S} = C(n-4, 4)
but that overcounts S with multiple 4-circles.

INCLUSION-EXCLUSION over 4-circles is infeasible (154,980 of them at q=9).

ALTERNATIVE: count by the profile.  For each profile P, the number of
8-sets with profile P is what we want.  The tuple loop gives us
tuples(P) = sum over (T,X) with profile P of 1.

For a FIXED C, the map (T, X) -> S = T u X is:
  - surjective onto {S : |C cap S| >= 4}
  - for S with |C cap S| = j, the preimage has size C(j,4)

So:
    tuples(P) = sum over S with profile P of C(|C cap S|, 4)

Summing over all C (multiplying by b):
    b * tuples(P) = sum over S with profile P of sum over 4-circles D of S
                    of C(|D cap S|, 4)

But |D cap S| = 4 for a 4-circle D (by definition of 4-circle: it carries
exactly 4 points of S... no, a 4-circle carries >= 4).

AH -- that is the issue.  A "4-circle" in the profile is a circle carrying
>= 4 points of S.  So |D cap S| can be 4, 5, 6, ...

So C(|D cap S|, 4) is C(4,4)=1 for a 4-point circle, C(5,4)=5 for a
5-point circle, C(6,4)=15 for a 6-point circle.

Therefore:
    b * tuples(P) = sum over S with profile P of
                      [n4(P)*1 + n5(P)*5 + n6(P)*15]

NOT n4(P) alone!

So the correct divisor is NOT n4(P) but the weighted sum
    w(P) = n4(P) + 5*n5(P) + 15*n6(P)

Let me verify this at q=5 and q=7.

Run:  python arc_k8_weighted.py --q 5 7
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field, build_inversive_plane  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
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

        prof_tuples = Counter()
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            for X in itertools.combinations(outside, 4):
                Xset = set(X)
                v2 = v3 = v4 = u3 = u4 = z4 = 0
                for kk in range(b):
                    if kk == ci:
                        continue
                    ct = len(Tset & set(blocks[kk]))
                    cx = len(Xset & set(blocks[kk]))
                    if ct == 2:
                        if cx == 2:
                            v2 += 1
                        elif cx == 3:
                            v3 += 1
                        elif cx == 4:
                            v4 += 1
                    elif ct == 1:
                        if cx == 3:
                            u3 += 1
                        elif cx == 4:
                            u4 += 1
                    elif ct == 0:
                        if cx == 4:
                            z4 += 1
                n4 = 1 + v2 + u3 + z4
                n5 = v3 + u4
                n6 = v4
                prof_tuples[(n4, n5, n6)] += 1

        # assembly with divisor n4
        asm = Fraction(0)
        # assembly with weighted divisor n4 + 5*n5 + 15*n6
        wtd = Fraction(0)
        for (n4, n5, n6), cnt in prof_tuples.items():
            asm += Fraction(cnt * b, n4)
            w = n4 + 5 * n5 + 15 * n6
            wtd += Fraction(cnt * b, w)

        row = {"q": q, "n": n, "b": b, "s": s,
               "profiles": len(prof_tuples),
               "asm": str(asm), "wtd": str(wtd),
               "asm_int": int(asm) if asm.denominator == 1 else None,
               "wtd_int": int(wtd) if wtd.denominator == 1 else None,
               "C_n_8": comb(n, 8)}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}, profiles={len(prof_tuples)}",
              flush=True)
        print(f"  divisor n4        -> {asm}", flush=True)
        print(f"  divisor n4+5n5+15n6 -> {wtd}", flush=True)
        print(f"  C(n,8) = {comb(n,8)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
