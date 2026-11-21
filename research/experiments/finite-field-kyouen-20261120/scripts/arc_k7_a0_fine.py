"""k=7: the a=0 ambiguity — what distinguishes the pairs?

MEASURED (q=5, a=0, 600 triples, 6 types):

    ((2,2,3),(2,4,4),6) -> dist1 (240) and dist2 (120)
    ((2,3,3),(4,4,6),6) -> dist3 (120) and dist4 (60)

So two invariant classes each split into two types.

The invariants used are (n2-triple, point-overlap vector, |union points|).
All have |union points| = 6 = s, i.e. the three involutions together cover
ALL of C.

The difference must be in the FINE structure of how the pairs interleave.
Let me look at the actual pair sets for the two sub-types of
((2,2,3),(2,4,4),6).

Run:  python arc_k7_a0_fine.py --q 5
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

from arc_on_quadric import build  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, ovoid, circles = build(q)
        n = len(ovoid)
        b = len(circles)
        s = q + 1
        circ_through_pair = {}
        for ci, B in enumerate(circles):
            for pair in itertools.combinations(B, 2):
                circ_through_pair.setdefault(pair, []).append(ci)

        ci = 0
        B = circles[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]

        joint = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = None
            for cj, BB in enumerate(circles):
                if cj == ci:
                    continue
                if all(p in BB for p in xyz):
                    W = cj
                    break
            WcapC = Bset & set(circles[W]) if W is not None else set()
            if len(WcapC) != 0:
                continue
            invs = []
            n2s = []
            for xy in itertools.combinations(xyz, 2):
                pairs = set()
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    cap = Bset & set(circles[cj])
                    if len(cap) == 2:
                        pairs.add(tuple(sorted(cap)))
                invs.append(frozenset(pairs))
                n2s.append(len(pairs))
            if tuple(sorted(n2s)) != (2, 2, 3):
                continue
            covered = [set(p for pr in inv for p in pr) for inv in invs]
            ov = (len(covered[0] & covered[1]), len(covered[0] & covered[2]),
                  len(covered[1] & covered[2]))
            if tuple(sorted(ov)) != (2, 4, 4):
                continue

            # canonical form of the pair sets
            pts = sorted(B)
            lab = {p: i for i, p in enumerate(pts)}
            canon = tuple(sorted(
                tuple(sorted(tuple(sorted((lab[a], lab[b]))) for a, b in inv))
                for inv in invs))

            dist = Counter()
            for T in itertools.combinations(B, 4):
                Tset = set(T)
                u = set()
                for inv in invs:
                    for pr in inv:
                        if pr[0] in Tset and pr[1] in Tset:
                            u.add(pr)
                dist[(0, len(u))] += 1
            joint[(canon, tuple(sorted(dist.items())))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: a=0, n2=(2,2,3), overlap=(2,4,4)", flush=True)
        print(f"  distinct canonical configurations: {len(joint)}", flush=True)
        for k, v in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
