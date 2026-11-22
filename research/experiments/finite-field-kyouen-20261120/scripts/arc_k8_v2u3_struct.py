"""k=8: the structure of the (v2, u3) joint distribution.

MEASURED at q=5: 28 classes, largest (5,2) with 10,560.

v2 counts circles with |C' cap T| = 2 and |C' cap X| = 2.
u3 counts circles with |C' cap T| = 1 and |C' cap X| = 3.

These are NOT independent: both depend on the configuration (T, X).

KEY IDEA.  v2 is determined by the 6 pencils through pairs of T: for each
pencil circle C', we ask whether |C' cap X| = 2.  u3 is determined by the
tangent circles at T and the mixed 2-secants.

Let me measure the conditional distribution: given v2, what is u3?

Run:  python arc_k8_v2u3_struct.py --q 5
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
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

        joint = Counter()
        cond = defaultdict(Counter)
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            for X in itertools.combinations(outside, 4):
                Xset = set(X)
                v2 = u3 = 0
                for kk in range(b):
                    if kk == ci:
                        continue
                    ct = len(Tset & set(blocks[kk]))
                    cx = len(Xset & set(blocks[kk]))
                    if ct == 2 and cx == 2:
                        v2 += 1
                    elif ct == 1 and cx == 3:
                        u3 += 1
                joint[(v2, u3)] += 1
                cond[v2][u3] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])},
               "cond": {str(k): dict(sorted(v.items()))
                        for k, v in sorted(cond.items())}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  joint (v2,u3) classes: {len(joint)}", flush=True)
        print("  conditional distribution of u3 given v2:", flush=True)
        for v2 in sorted(cond):
            tot = sum(cond[v2].values())
            print(f"    v2={v2} (n={tot}): "
                  f"{dict(sorted(cond[v2].items()))}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
