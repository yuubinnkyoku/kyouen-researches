"""k=7: the a=2 split is per-CIRCLE: 45 vs 30 circles at q=5.

MEASURED (q=5, a=2 layer):

    45 circles W: ALL their C(q-1,3)=4 triples give extra-pairs (1,1,2)
    30 circles W: ALL their 4 triples give extra-pairs (1,2,2)

    45*4 = 180,  30*4 = 120,  total 300.  MATCHES.

So the type is a property of the CIRCLE W, not of the triple.  That is a
big simplification: the a=2 layer's split reduces to counting circles of
two kinds.

45 + 30 = 75 = C(s,2)*q = 15*5.  MATCHES the a=2 circle count.

NOW: what distinguishes the two kinds of circle?

For a=2, W meets C in {p,p'}.  The triples on W are 3-subsets of W \\ C.
For each such triple, the three pencils give involutions containing {p,p'}
plus extras.

The extras come from OTHER circles through pairs of the triple that meet C
in 2 points.  Those circles are determined by W and the pair.

Let me characterise the two kinds of W.

Run:  python arc_k7_a2_circle_kind.py --q 5
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

        # for each a=2 circle W, record its kind and some invariants
        kinds = Counter()
        for k, BB in enumerate(blocks):
            if k == ci:
                continue
            cap = Bset & set(BB)
            if len(cap) != 2:
                continue
            Wout = [p for p in BB if p not in Bset]
            if len(Wout) < 3:
                continue
            # determine the kind from the first triple
            xyz = tuple(Wout[:3])
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
            kind = tuple(sorted(len(e) for e in extras))
            # invariants: how many circles through pairs of Wout meet C in 2
            n_extra_circles = 0
            for xy in itertools.combinations(Wout, 2):
                for kk in circ_through_pair.get(tuple(sorted(xy)), []):
                    if kk in (ci, k):
                        continue
                    if len(Bset & set(blocks[kk])) == 2:
                        n_extra_circles += 1
            kinds[(kind, n_extra_circles)] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "kinds": {str(k): v for k, v in sorted(kinds.items())}}
        rows.append(row)
        print(f"q={q}: a=2 circle kinds", flush=True)
        for k, v in sorted(kinds.items()):
            print(f"    kind={k[0]}, extra-circles={k[1]}: {v} circles",
                  flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
