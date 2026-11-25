"""k=7: the a=2 split in closed form.

MEASURED (q=5, a=2, 300 triples):

    extra-pair counts (1,1,2), extra overlaps (0,0,0), |all extra| = 4 -> 180
    extra-pair counts (1,2,2), extra overlaps (0,0,0), |all extra| = 5 -> 120

So the two orbits are distinguished by the number of EXTRA pairs (beyond
the common pair W cap C) in the three involutions.

Let me derive the counts.

SETUP.  a=2 means W meets C in {p,p'}.  The three involutions all contain
the pair {p,p'}.  Each involution also has some extra pairs.

For a fixed W with |W cap C| = 2, the triples on W are the 3-subsets of
W \\ C (q-1 points).  For each such triple {x,y,z}, the three pencils give
three involutions.

The number of extra pairs depends on how the pencils' 2-secant circles
(other than W) meet C.

Let me count directly: for a fixed W, how many of its C(q-1,3) triples give
each type?

Run:  python arc_k7_a2_count.py --q 5
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

        # for each W with |W cap C| = 2, count triples by type
        per_W = Counter()
        for k, BB in enumerate(blocks):
            if k == ci:
                continue
            cap = Bset & set(BB)
            if len(cap) != 2:
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
                extras = [frozenset(inv - {tuple(sorted(cap))}) for inv in invs]
                per_W[tuple(sorted(len(e) for e in extras))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "per_W": {str(k): v for k, v in sorted(per_W.items())},
               "total": sum(per_W.values())}
        rows.append(row)
        print(f"q={q}: a=2, per-W triple types", flush=True)
        for k, v in sorted(per_W.items()):
            print(f"    {k}: {v}", flush=True)
        print(f"  total {sum(per_W.values())}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
