"""k=8: the CORRECT assembly divisor.

THE BUG.  The tuple loop fixes C and uses T with |T| = 4.  So S is
generated via C only when |C cap S| = 4.  But:
  - if |C cap S| = 5, the loop generates S C(5,4) = 5 times (one per
    4-subset T of C cap S), and X = S - T is outside C only when
    T = C cap S -- which has size 5, not 4.  So actually the loop CANNOT
    generate S via C at all when |C cap S| = 5.
  - Wait: X must be a 4-subset of the outside.  If |C cap S| = 5, then
    S has 5 points on C and 3 outside.  So X (4 points outside C) cannot
    be S - T for any T.  So S is NOT generated via C.

So the loop generates S via C iff |C cap S| = 4, and then exactly once.

Summing over all C: S is generated once per circle C with |C cap S| = 4.
That is the number of circles carrying EXACTLY 4 points of S -- call it
e4(S), NOT n4(S) (which counts circles carrying >= 4).

So the correct divisor is e4(S), not n4(S)!

And the profile formula gives n4 = 1 + v2 + u3 + z4 which counts circles
carrying >= 4.  So n4 >= e4, and dividing by n4 UNDERCOUNTS.

That matches the observed direction (bad undercounted, arcs overcounted).

Let me verify: the correct divisor is e4 = n4 - n5 - n6.

Run:  python arc_k8_e4.py --q 5 7
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

        asm_n4 = Fraction(0)
        asm_e4 = Fraction(0)
        zero_e4 = 0
        for (n4, n5, n6), cnt in prof_tuples.items():
            asm_n4 += Fraction(cnt * b, n4)
            e4 = n4 - n5 - n6
            if e4 > 0:
                asm_e4 += Fraction(cnt * b, e4)
            else:
                zero_e4 += cnt

        row = {"q": q, "n": n, "b": b, "s": s,
               "profiles": len(prof_tuples),
               "asm_n4": str(asm_n4), "asm_e4": str(asm_e4),
               "zero_e4_tuples": zero_e4,
               "C_n_8": comb(n, 8)}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}, profiles={len(prof_tuples)}",
              flush=True)
        print(f"  divisor n4  -> {asm_n4}", flush=True)
        print(f"  divisor e4  -> {asm_e4}", flush=True)
        print(f"  tuples with e4=0: {zero_e4}", flush=True)
        print(f"  C(n,8) = {comb(n,8)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
