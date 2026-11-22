"""k=7: the (5,) profile in closed form.

(5,) = 7-sets with exactly ONE circle carrying >= 4 points, and it carries 5.

Structure: a circle C with 5 points of S, plus 2 points {x,y} outside C,
such that NO other circle carries 4 of S.

A second circle C' carries 4 of S iff it carries 2 of the 5 points of C
and both x,y (since C' meets C in <= 2 points, it can carry at most 2 of
the 5; to reach 4 it needs both x and y).

So the condition is: NO circle through x and y meets the 5-set in exactly
2 points.

The circles through x,y form a pencil of q+1 circles.  Each meets C in
0, 1 or 2 points.  Let n2 = number of 2-secant circles in that pencil.
The condition is: none of those n2 circles meets the 5 chosen points in
exactly 2.

Let me measure this directly: for each (C, 5-subset T5, {x,y}), count the
number of pencil circles through x,y meeting T5 in exactly 2 points, and
check that (5,) corresponds to count 0.

Run:  python arc_k7_five_profile.py --q 5 7
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

        circ_through_pair = {}
        for k, BB in enumerate(blocks):
            for pair in itertools.combinations(BB, 2):
                circ_through_pair.setdefault(pair, []).append(k)

        outside = [p for p in range(n) if p not in Bset]

        # for each (T5, {x,y}), count pencil circles through x,y meeting T5
        # in exactly 2 points
        hist = Counter()
        for T5 in itertools.combinations(B, 5):
            T5set = set(T5)
            for xy in itertools.combinations(outside, 2):
                cnt = 0
                for kk in circ_through_pair.get(tuple(sorted(xy)), []):
                    if kk == ci:
                        continue
                    if len(T5set & set(blocks[kk])) == 2:
                        cnt += 1
                hist[cnt] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "hist": dict(sorted(hist.items())),
               "total": sum(hist.values()),
               "naive": comb(s, 5) * comb(n - s, 2)}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  #pencil circles meeting T5 in 2 points -> count", flush=True)
        for k, v in sorted(hist.items()):
            print(f"    {k}: {v}", flush=True)
        print(f"  total {sum(hist.values())} vs C(s,5)*C(n-s,2) = "
              f"{comb(s,5)*comb(n-s,2)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
