"""k=7: the last discriminator between the two (A,(2,2,3),0,(2,4,4),6) types.

MEASURED: two types share (case A, n2=(2,2,3), |W cap C|=0, point-overlaps
(2,4,4), |union pts|=6):

    dist1 = (0,1):1 (0,2):2 (0,3):11 (0,4):1        240 triples
    dist2 = (0,2):5 (0,3):8 (0,4):2                  120 triples

Both have the same n2-triple and the same point-overlap vector.  The
difference must be in the FINE structure: which pairs the involutions
share at the point level.

Let me measure the exact triple of pair-sets (as a canonical form) and see
how many distinct configurations occur.

Run:  python arc_k7_fine.py --q 5
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
        circ_of_triple = {}
        for ci, B in enumerate(circles):
            for tri in itertools.combinations(B, 3):
                circ_of_triple[tri] = ci

        ci = 0
        B = circles[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]

        joint = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = circ_of_triple.get(tuple(sorted(xyz)))
            WcapC = Bset & set(circles[W]) if W is not None else set()
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
            common = (len(invs[0] & invs[1]), len(invs[0] & invs[2]),
                      len(invs[1] & invs[2]))
            case = "B" if common == (1, 1, 1) else "A"
            if case != "A" or tuple(sorted(n2s)) != (2, 2, 3):
                continue
            if len(WcapC) != 0:
                continue

            # canonical form: relabel C's points by first appearance
            pts = sorted(B)
            lab = {p: i for i, p in enumerate(pts)}
            canon = []
            for inv in invs:
                canon.append(tuple(sorted(tuple(sorted((lab[a], lab[b])))
                                          for a, b in inv)))
            canon = tuple(sorted(canon))

            dist = Counter()
            for T in itertools.combinations(B, 4):
                Tset = set(T)
                w = len(Tset & WcapC)
                u = set()
                for inv in invs:
                    for pr in inv:
                        if pr[0] in Tset and pr[1] in Tset:
                            u.add(pr)
                dist[(w, len(u))] += 1
            joint[(canon, tuple(sorted(dist.items())))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
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
