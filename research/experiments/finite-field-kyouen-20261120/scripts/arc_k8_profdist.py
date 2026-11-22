"""k=8: the profile distribution.

The profile is (n4, n5, n6) where
    n4 = 1 + v2 + u3 + z4
    n5 = v3 + u4
    n6 = v4

To get the DISTRIBUTION (not just the sums) we need the joint distribution
of (v2, v3, v4, u3, u4, z4).

MEASURED at q=5: 13 profiles.  Let me look at their structure.

From the earlier run (arc_k8_assemble.py at q=5):
    (8,0,0): 26640 tuples
    (5,1,0): 16200
    (7,0,0):  9450
    (6,1,0):  6480
    (4,1,0):  5280
    (9,0,0):  3510
    (6,0,0):  2760
    (2,2,0):   960
    (10,0,0):   525
    (3,2,0):   360
    (2,0,1):   240
    (3,0,1):   210
    (12,0,0):    60

KEY OBSERVATION: n6 = v4 is 0 except for (2,0,1) and (3,0,1) where it is 1.
And n5 = v3 + u4 is 0, 1 or 2.

Since v4, u4, z4 are mutually exclusive and rare, the profile is mostly
determined by (v2, u3) with occasional corrections.

Let me measure the joint distribution of (v2, u3) and see how v3, v4, u4, z4
perturb it.

Run:  python arc_k8_profdist.py --q 5
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

        prof = Counter()
        v2u3 = Counter()
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
                prof[(n4, n5, n6)] += 1
                v2u3[(v2, u3)] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "profiles": {str(k): v for k, v in
                            sorted(prof.items(), key=lambda x: -x[1])},
               "v2u3": {str(k): v for k, v in
                        sorted(v2u3.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  profiles ({len(prof)}):", flush=True)
        for k, v in sorted(prof.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)
        print(f"  (v2,u3) classes: {len(v2u3)}", flush=True)
        for k, v in sorted(v2u3.items(), key=lambda x: -x[1])[:15]:
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
