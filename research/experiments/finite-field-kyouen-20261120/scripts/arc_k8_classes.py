"""k=8: closed forms for the six profile classes.

The classes are (from the k=8 profile formula):

    v2 = #{C' : |C' cap T| = 2, |C' cap X| = 2}
    v3 = #{C' : |C' cap T| = 2, |C' cap X| = 3}
    v4 = #{C' : |C' cap T| = 2, |C' cap X| = 4}
    u3 = #{C' : |C' cap T| = 1, |C' cap X| = 3}
    u4 = #{C' : |C' cap T| = 1, |C' cap X| = 4}
    z4 = #{C' : |C' cap T| = 0, |C' cap X| = 4}

where T is a 4-subset of the base circle C and X is a 4-subset of the
points outside C.

KEY STRUCTURE.  A circle C' != C meets C in 0, 1 or 2 points.  So
|C' cap T| <= 2 automatically.  The count of C' with |C' cap T| = 2 is
exactly the number of 2-secants of C through a pair of T -- but each such
C' is determined by the pair, and different pairs can share a circle.

Let me just MEASURE the distributions of (v2,v3,v4,u3,u4,z4) at q=5 and
q=7 and look for closed forms.

Run:  python arc_k8_classes.py --q 5 7
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

        # marginal distributions of each class
        marg = {name: Counter() for name in
                ("v2", "v3", "v4", "u3", "u4", "z4")}
        joint = Counter()
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
                marg["v2"][v2] += 1
                marg["v3"][v3] += 1
                marg["v4"][v4] += 1
                marg["u3"][u3] += 1
                marg["u4"][u4] += 1
                marg["z4"][z4] += 1
                joint[(v2, v3, v4, u3, u4, z4)] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "marginals": {k: dict(sorted(v.items()))
                             for k, v in marg.items()},
               "joint_classes": len(joint)}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        for name in ("v2", "v3", "v4", "u3", "u4", "z4"):
            print(f"  {name}: {dict(sorted(marg[name].items()))}", flush=True)
        print(f"  joint classes: {len(joint)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
