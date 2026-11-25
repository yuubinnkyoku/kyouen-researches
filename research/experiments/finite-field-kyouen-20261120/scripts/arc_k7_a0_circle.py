"""k=7: the a=0 layer's 6-way split.

MEASURED (q=5, a=0, 600 triples, 6 orbits):

    240, 120, 120, 60, 40, 20

For a=0, W is disjoint from C, so w = 0 always.  The type is determined by
the u-distribution, which depends on the three involutions.

KEY IDEA.  For a=0, W contributes nothing to the involutions (W meets C in
0 points, so W is not a 2-secant circle of any pencil).  So the three
involutions come ENTIRELY from other circles.

The triples on W are the 3-subsets of W \\ C, which has s = q+1 points.
So each a=0 circle W contributes C(q+1, 3) triples.

Check q=5: C(6,3) = 20 triples per W, and there are 30 a=0 circles:
30 * 20 = 600.  MATCHES.

So the a=0 layer's 600 triples come from 30 circles x 20 triples each.

NOW: is the type a property of the CIRCLE W (as it was for a=2)?

Let me check.

Run:  python arc_k7_a0_circle.py --q 5
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

        # for each a=0 circle W, compute the u-distribution over its triples
        per_W = Counter()
        for k, BB in enumerate(blocks):
            if k == ci:
                continue
            cap = Bset & set(BB)
            if len(cap) != 0:
                continue
            Wout = [p for p in BB if p not in Bset]
            if len(Wout) < 3:
                continue
            dist = Counter()
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
                u = set()
                for inv in invs:
                    u |= inv
                dist[len(u)] += 1
            per_W[tuple(sorted(dist.items()))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "per_W": {str(k): v for k, v in
                         sorted(per_W.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: a=0 circles, u-distribution over their triples",
              flush=True)
        print(f"  distinct per-W distributions: {len(per_W)}", flush=True)
        for k, v in sorted(per_W.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v} circles", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
