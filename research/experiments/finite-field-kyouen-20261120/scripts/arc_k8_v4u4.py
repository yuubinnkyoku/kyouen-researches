"""k=8: the v4 and u4 closed forms (the rare classes).

    v4 = #{C' : |C' cap T| = 2, |C' cap X| = 4}
    u4 = #{C' : |C' cap T| = 1, |C' cap X| = 4}

Both require |C' cap X| = 4, i.e. C' contains all 4 points of X.  Since 4
points determine at most one circle, there is AT MOST ONE such C' -- the
circle D through X, if X is concyclic.

So:
    v4 = 1 iff X is concyclic AND |D cap T| = 2
    u4 = 1 iff X is concyclic AND |D cap T| = 1

And z4 = 1 iff X concyclic AND |D cap T| = 0 (already established).

So v4, u4, z4 are MUTUALLY EXCLUSIVE and together they are 1 iff X is
concyclic (and D != C).

Let me verify this at q=5.

Run:  python arc_k8_v4u4.py --q 5
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

        circ_of_triple = {}
        for k, BB in enumerate(blocks):
            for tri in itertools.combinations(BB, 3):
                circ_of_triple[tri] = k

        # (is_concyclic, |D cap T|) -> count, and the v4/u4/z4 values
        hist = Counter()
        v4u4z4 = Counter()
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            for X in itertools.combinations(outside, 4):
                cj = circ_of_triple.get(tuple(sorted(X[:3])))
                is_concyc = (cj is not None
                             and all(p in blocks[cj] for p in X))
                if not is_concyc:
                    hist[("not concyc", -1)] += 1
                    v4u4z4[(0, 0, 0)] += 1
                    continue
                capT = len(Tset & set(blocks[cj]))
                hist[("concyc", capT)] += 1
                v4 = 1 if capT == 2 else 0
                u4 = 1 if capT == 1 else 0
                z4 = 1 if capT == 0 else 0
                v4u4z4[(v4, u4, z4)] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "hist": {str(k): v for k, v in sorted(hist.items())},
               "v4u4z4": {str(k): v for k, v in sorted(v4u4z4.items())}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print("  (concyclicity, |D cap T|) -> count:", flush=True)
        for k, v in sorted(hist.items()):
            print(f"    {k}: {v}", flush=True)
        print("  (v4, u4, z4) -> count:", flush=True)
        for k, v in sorted(v4u4z4.items()):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
