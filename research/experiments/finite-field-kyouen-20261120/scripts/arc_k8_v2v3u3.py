"""k=8: the v2, v3, u3 closed forms.

    v2 = #{C' : |C' cap T| = 2, |C' cap X| = 2}
    v3 = #{C' : |C' cap T| = 2, |C' cap X| = 3}
    u3 = #{C' : |C' cap T| = 1, |C' cap X| = 3}

KEY STRUCTURE.  A circle C' with |C' cap T| = 2 is a 2-secant of C through
a pair of T.  For each pair {a,b} of T, the pencil through a,b has q+1
circles; one of them is C itself, so q circles meet C in exactly {a,b}.

So the "2-secant" circles of T are the union over the 6 pairs of T of the
q circles in each pencil (excluding C).  Different pairs can share a circle
only if the circle meets C in 2 points, which determines the pair -- so
the 6 pencils are DISJOINT except for C.

Therefore there are exactly 6q circles with |C' cap T| = 2.

Similarly, circles with |C' cap T| = 1: for each point a of T, the circles
through a that meet C only at a -- these are the circles TANGENT to C at a.
There are q-1 such circles per point (the tangent pencil minus C).

So:
    #{C' : |C' cap T| = 2} = 6q
    #{C' : |C' cap T| = 1} = 4(q-1)

Let me verify these counts and then split by |C' cap X|.

Run:  python arc_k8_v2v3u3.py --q 5
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field, build_inversive_plane  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5])
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

        # verify the counts of circles by |C' cap T|
        T = tuple(B[:4])
        Tset = set(T)
        cnt_by_capT = Counter()
        for kk in range(b):
            if kk == ci:
                continue
            cnt_by_capT[len(Tset & set(blocks[kk]))] += 1

        # and by |C' cap X| for a fixed X
        X = tuple(outside[:4])
        Xset = set(X)
        cnt_by_capX = Counter()
        for kk in range(b):
            if kk == ci:
                continue
            cnt_by_capX[len(Xset & set(blocks[kk]))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "capT_counts": dict(sorted(cnt_by_capT.items())),
               "capX_counts": dict(sorted(cnt_by_capX.items())),
               "predicted_capT2": 6 * q,
               "predicted_capT1": 4 * (q - 1)}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  |C' cap T| distribution: "
              f"{dict(sorted(cnt_by_capT.items()))}", flush=True)
        print(f"  predicted |cap T|=2: {6*q}, "
              f"|=1: {4*(q-1)}", flush=True)
        print(f"  |C' cap X| distribution: "
              f"{dict(sorted(cnt_by_capX.items()))}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
