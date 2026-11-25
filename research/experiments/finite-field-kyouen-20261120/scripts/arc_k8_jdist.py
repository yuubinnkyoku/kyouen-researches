"""k=8 at q=7: test the corrected divisor n4 * C(j,4).

The tuple loop fixes T (a 4-subset of C).  For a set S with
|C cap S| = j >= 4, the loop sees S once for each 4-subset T of C cap S,
i.e. C(j,4) times, and for each such T it counts S once per 4-circle D.

So S appears C(j,4) * n4(S) times.  The correct divisor is
C(j,4) * n4(S), not n4(S).

The assembly divides by n4 only, so S with j > 4 is OVERcounted by C(j,4).

Let me measure the actual j-distribution and compute the corrected sum.

Run:  python arc_k8_jdist.py --q 7
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
    ap.add_argument("--q", type=int, nargs="+", default=[7])
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

        # for each (T, X) tuple, record j = |C cap S| and n4
        jhist = Counter()
        # sum of tuples*b/n4 (as the assembly does)
        asm = Fraction(0)
        # sum of tuples*b/(n4*C(j,4)) (corrected)
        corr = Fraction(0)
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            for X in itertools.combinations(outside, 4):
                Xset = set(X)
                Sset = Tset | Xset
                j = len(Bset & Sset)
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
                jhist[j] += 1
                asm += Fraction(b, n4)
                corr += Fraction(b, n4 * comb(j, 4))

        row = {"q": q, "n": n, "b": b, "s": s,
               "jhist": dict(sorted(jhist.items())),
               "asm": str(asm), "corr": str(corr),
               "asm_int": int(asm) if asm.denominator == 1 else None,
               "corr_int": int(corr) if corr.denominator == 1 else None}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  j = |C cap S| histogram: {dict(sorted(jhist.items()))}",
              flush=True)
        print(f"  assembly sum (div n4)        = {asm}", flush=True)
        print(f"  corrected sum (div n4*C(j,4)) = {corr}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
