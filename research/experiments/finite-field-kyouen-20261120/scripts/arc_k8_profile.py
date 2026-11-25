"""k=8: the profile formula, derived from the k=7 structure.

For k=7 the profile formula was

    #4-circles = 1 + v + [|W cap T| = 1]
    #5-circles = [|W cap T| = 2]

with v = #{C' != C : |C' cap T| = 2 and |C' cap {x,y,z}| = 2}.

For k=8, S = T u {w,x,y,z} with |T| = 4, T in C, and 4 points outside C.
A circle C' != C meets C in <= 2 points, so

    |C' cap S| = |C' cap T| + |C' cap {w,x,y,z}| <= 2 + 4 = 6.

So the profile values are 4, 5, 6.

The classification:
  - C itself: |C cap S| = 4 (the 4 points of T)
  - C' with |C' cap T| = 2 and |C' cap {w,x,y,z}| = 2  -> 4 points
  - C' with |C' cap T| = 2 and |C' cap {w,x,y,z}| = 3  -> 5 points
  - C' with |C' cap T| = 2 and |C' cap {w,x,y,z}| = 4  -> 6 points
  - C' with |C' cap T| = 1 and |C' cap {w,x,y,z}| = 3  -> 4 points
  - C' with |C' cap T| = 1 and |C' cap {w,x,y,z}| = 4  -> 5 points
  - C' with |C' cap T| = 0 and |C' cap {w,x,y,z}| = 4  -> 4 points

Let me define:
  v2 = #{C' : |C' cap T| = 2, |C' cap X| = 2}   (X = {w,x,y,z})
  v3 = #{C' : |C' cap T| = 2, |C' cap X| = 3}
  v4 = #{C' : |C' cap T| = 2, |C' cap X| = 4}
  u3 = #{C' : |C' cap T| = 1, |C' cap X| = 3}
  u4 = #{C' : |C' cap T| = 1, |C' cap X| = 4}
  z4 = #{C' : |C' cap T| = 0, |C' cap X| = 4}

Then
  #4-circles = 1 + v2 + u3 + z4
  #5-circles = v3 + u4
  #6-circles = v4

Let me VERIFY this at q=5 and q=7 (small enough to enumerate).

Run:  python arc_k8_profile.py --q 5 7
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
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    ap.add_argument("--limit", type=int, default=20000)
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
        circ_of_triple = {}
        for k, BB in enumerate(blocks):
            for tri in itertools.combinations(BB, 3):
                circ_of_triple[tri] = k
        outside = [p for p in range(n) if p not in Bset]

        mismatch = Counter()
        checked = 0
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            for X in itertools.combinations(outside, 4):
                Xset = set(X)
                Sset = Tset | Xset
                # actual profile
                hits = {}
                for quad in itertools.combinations(sorted(Sset), 4):
                    cj = circ_of_triple.get(tuple(sorted(quad[:3])))
                    if cj is None:
                        continue
                    if all(p in blocks[cj] for p in quad):
                        hits[cj] = len(Sset & set(blocks[cj]))
                actual = tuple(sorted(hits.values(), reverse=True))
                # formula
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
                pred = tuple([6] * n6 + [5] * n5 + [4] * n4)
                checked += 1
                if actual != pred:
                    mismatch[(actual, pred)] += 1
                if checked >= args.limit:
                    break
            if checked >= args.limit:
                break

        row = {"q": q, "checked": checked,
               "mismatches": sum(mismatch.values()),
               "examples": {str(k): v for k, v in
                            sorted(mismatch.items(), key=lambda x: -x[1])[:3]}}
        rows.append(row)
        print(f"q={q}: checked {checked}, mismatches {sum(mismatch.values())}",
              flush=True)
        for (a, p), v in sorted(mismatch.items(), key=lambda x: -x[1])[:3]:
            print(f"    actual {a} vs predicted {p}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
