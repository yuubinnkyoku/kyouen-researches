"""k=7: the a=0 layer's u-distribution per triple, grouped by |U|.

The orbit is determined by the involution triple.  The u-distribution over
T is determined by the involution triple too (9 distributions = 9 orbits).

For a=0, u(T) = number of involution pairs fully inside T.  Let U be the
union of the three pair-sets.  In case A (no shared pair) |U| = sum(n2).

MEASURED coverage classes: |U| = 6, 7, 8, 9 with 20, 360, 180, 40 triples.
Orbits: 20, (240+120), (120+60), 40.

So |U| = 7 splits into 240+120 and |U| = 8 splits into 120+60.

Let me measure the u-distribution per triple and see what distinguishes them.

Run:  python arc_k7_a0_udist.py --q 5
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

        circ_through_pair = {}
        for k, BB in enumerate(blocks):
            for pair in itertools.combinations(BB, 2):
                circ_through_pair.setdefault(pair, []).append(k)

        joint = Counter()
        for k, BB in enumerate(blocks):
            if k == ci:
                continue
            if len(Bset & set(BB)) != 0:
                continue
            Wout = [p for p in BB if p not in Bset]
            if len(Wout) < 3:
                continue
            for xyz in itertools.combinations(Wout, 3):
                invs = []
                for xy in itertools.combinations(xyz, 2):
                    pairs = set()
                    for kk in circ_through_pair.get(tuple(sorted(xy)), []):
                        if kk == ci:
                            continue
                        c2 = Bset & set(blocks[kk])
                        if len(c2) == 2:
                            pairs.add(tuple(sorted(c2)))
                    invs.append(frozenset(pairs))
                U = set()
                for inv in invs:
                    U |= inv
                # u-distribution over T
                dist = Counter()
                for T in itertools.combinations(B, 4):
                    Tset = set(T)
                    u = sum(1 for pr in U if pr[0] in Tset and pr[1] in Tset)
                    dist[u] += 1
                joint[(len(U), tuple(sorted(dist.items())))] += 1

        row = {"q": q, "joint": {str(k): v for k, v in
                                 sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: a=0, (|U|, u-distribution over T) -> triples",
              flush=True)
        print(f"  distinct classes: {len(joint)}", flush=True)
        for k, v in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
