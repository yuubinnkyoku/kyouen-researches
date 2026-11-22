"""k=7: the a=0 layer CLOSES with (n2-triple, u-distribution).

MEASURED (q=5, a=0): the pair (n2-triple, u-distribution over T) gives
EXACTLY 6 classes, matching the 6 orbits:

    (7, ((1,1),(2,2),(3,11),(4,1)))   240   <- orbit 20
    (7, ((2,5),(3,8),(4,2)))          120   <- orbit 28
    (8, ((2,1),(3,11),(4,2),(5,1)))   120   <- orbit 31? (a=2) -- no, a=0
    (8, ((2,2),(3,8),(4,5)))           60   <- orbit 27
    (9, ((3,6),(4,9)))                 40   <- orbit 36
    (6, ((2,9),(3,6)))                 20   <- orbit 32

Wait: the a=0 orbits are 20, 22, 27, 28, 32, 36 with counts
240, 120, 60, 120, 20, 40.

Matching by count:
    240 -> orbit 20
    120 -> orbit 22 or 28
    120 -> orbit 28 or 22
     60 -> orbit 27
     40 -> orbit 36
     20 -> orbit 32

So the 6 classes ARE the 6 orbits.  The (n2-triple, u-distribution) pair
is a COMPLETE invariant for the a=0 layer.

Now: can we get the counts in closed form?

The classes are indexed by |U| (6, 7, 8, 9) and within |U|=7,8 there are
two sub-classes.  The sub-classes differ in the u-distribution.

Let me look for the closed form of the counts: 240, 120, 120, 60, 40, 20.

    240 = 20*12
    120 = 20*6
    120 = 20*6
     60 = 20*3
     40 = 20*2
     20 = 20*1

So all are multiples of 20 = C(s,3).  The multipliers are 12, 6, 6, 3, 2, 1.

And 12+6+6+3+2+1 = 30 = the number of a=0 circles!

So each a=0 circle contributes its 20 triples entirely to ONE class.
The classes are CIRCLE classes, with 12, 6, 6, 3, 2, 1 circles.

Check: 12+6+6+3+2+1 = 30.  YES.

So the a=0 layer's 6 orbits correspond to 6 kinds of CIRCLE, with
12, 6, 6, 3, 2, 1 circles each.

Run:  python arc_k7_a0_circle6.py --q 5
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

        # per-circle: the class (n2-triple, u-distribution)
        per_circle = Counter()
        for k, BB in enumerate(blocks):
            if k == ci:
                continue
            if len(Bset & set(BB)) != 0:
                continue
            Wout = [p for p in BB if p not in Bset]
            if len(Wout) < 3:
                continue
            classes = Counter()
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
                dist = Counter()
                for T in itertools.combinations(B, 4):
                    Tset = set(T)
                    u = sum(1 for pr in U if pr[0] in Tset and pr[1] in Tset)
                    dist[u] += 1
                classes[(len(U), tuple(sorted(dist.items())))] += 1
            per_circle[tuple(sorted(classes.items()))] += 1

        row = {"q": q, "per_circle": {str(k): v for k, v in
                                      sorted(per_circle.items(),
                                             key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: a=0 per-circle class distributions", flush=True)
        print(f"  distinct: {len(per_circle)}", flush=True)
        for k, v in sorted(per_circle.items(), key=lambda x: -x[1]):
            print(f"    {v} circles: {k}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
