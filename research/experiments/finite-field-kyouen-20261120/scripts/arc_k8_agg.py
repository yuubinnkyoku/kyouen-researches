"""k=8: the v2, v3, u3 closed forms via the pencil structure.

The three remaining classes:

    v2 = #{C' : |C' cap T| = 2, |C' cap X| = 2}
    v3 = #{C' : |C' cap T| = 2, |C' cap X| = 3}
    u3 = #{C' : |C' cap T| = 1, |C' cap X| = 3}

KEY: circles with |C' cap T| = 2 are exactly the 6q circles in the six
pencils through pairs of T (excluding C).  Circles with |C' cap T| = 1
are the 4(q-1) tangent-at-T circles plus the 4(s-4)q mixed 2-secants.

For each such C', we need |C' cap X|.  X is a 4-subset of the outside.

So:
    v2 + v3 + v4 = #{C' : |C' cap T| = 2 and |C' cap X| >= 2}
    u3 + u4      = #{C' : |C' cap T| = 1 and |C' cap X| >= 3}

And v4, u4 are already known (concyclicity).

So:
    v2 + v3 = #{|cap T|=2, |cap X|>=2} - v4
    u3      = #{|cap T|=1, |cap X|>=3} - u4

Let me measure these aggregates and look for closed forms.

Run:  python arc_k8_agg.py --q 5
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

        # aggregate over all (T, X)
        agg = Counter()
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
                agg["v2"] += v2
                agg["v3"] += v3
                agg["v4"] += v4
                agg["u3"] += u3
                agg["u4"] += u4
                agg["z4"] += z4
                agg["tuples"] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "sums": dict(sorted(agg.items()))}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  tuples = {agg['tuples']}", flush=True)
        for name in ("v2", "v3", "v4", "u3", "u4", "z4"):
            print(f"  sum {name} = {agg[name]}", flush=True)
        print(f"  sum v2+v3+v4 = {agg['v2']+agg['v3']+agg['v4']}", flush=True)
        print(f"  sum u3+u4 = {agg['u3']+agg['u4']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
