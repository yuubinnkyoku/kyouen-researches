"""k=7: the a=2 layer's 2-way split (180 vs 120) in closed form.

MEASURED (q=5): a=2 has 300 triples split into two orbits of 180 and 120.

For a=2, W meets C in exactly 2 points {p,p'} = W cap C.  The triples with
W(x,y,z) = W are the 3-subsets of W \\ C, which has s-2 = q-1 points.  So
each such W contributes C(q-1,3) triples.

Check q=5: C(4,3) = 4 triples per W.  With 75 circles of type a=2, that is
300.  MATCHES.

So the a=2 layer's 300 triples come from 75 circles x 4 triples each.

NOW: the split into 180 and 120 must come from a property of W (or of the
triples on W) that takes two values.

The (w,u)-distribution for a=2 depends on w = |T cap W|, which varies over
T.  But the ORBIT depends on the three involutions, which for a=2 all
contain the pair W cap C.

So the orbit is determined by the OTHER pairs of the three involutions.
Let me measure: for a=2, what distinguishes the 180-orbit from the
120-orbit?

Run:  python arc_k7_a2_split.py --q 5
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
        outside = [p for p in range(n) if p not in Bset]

        # for a=2 triples, record the structure of the three involutions
        # beyond the common pair
        joint = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = None
            for k, BB in enumerate(blocks):
                if k == ci:
                    continue
                if all(p in BB for p in xyz):
                    W = k
                    break
            WcapC = Bset & set(blocks[W]) if W is not None else set()
            if len(WcapC) != 2:
                continue
            invs = []
            for xy in itertools.combinations(xyz, 2):
                pairs = set()
                for k in circ_through_pair.get(tuple(sorted(xy)), []):
                    if k == ci:
                        continue
                    cap = Bset & set(blocks[k])
                    if len(cap) == 2:
                        pairs.add(tuple(sorted(cap)))
                invs.append(frozenset(pairs))
            # the common pair is WcapC; the other pairs are the extras
            extras = []
            for inv in invs:
                extras.append(frozenset(inv - {tuple(sorted(WcapC))}))
            # how many extra pairs in total, and their overlap structure
            all_extra = set()
            for e in extras:
                all_extra |= e
            ov = (len(extras[0] & extras[1]), len(extras[0] & extras[2]),
                  len(extras[1] & extras[2]))
            joint[(tuple(sorted(len(e) for e in extras)),
                   tuple(sorted(ov)), len(all_extra))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: a=2 layer", flush=True)
        print(f"  (extra-pair counts, extra overlaps, |all extra|) -> triples",
              flush=True)
        for k, v in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
