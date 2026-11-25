"""k=7: a finer invariant for the a=0 layer.

The a=0 layer has 6 orbits.  The invariants tried so far:
  - n2-triple (pairs per involution): 4 classes
  - point-overlap vector: still 4 classes
  - circle kind (HIGH/LOW): does not separate

NEW IDEA.  For the three involutions on C, classify each point of C by HOW
MANY of the three involutions cover it (0, 1, 2 or 3).  That gives a
"coverage profile" which is finer than the pairwise overlap vector.

Let me measure it.

Run:  python arc_k7_a0_coverage.py --q 5
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
                # coverage multiplicity per point of C
                cov = Counter()
                for inv in invs:
                    for pr in inv:
                        for p in pr:
                            cov[p] += 1
                prof = tuple(sorted(Counter(cov.values()).items()))
                n2s = tuple(sorted(len(i) for i in invs))
                joint[(n2s, prof)] += 1

        row = {"q": q, "joint": {str(k): v for k, v in
                                 sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: a=0, (n2-triple, coverage profile) -> triples",
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
