"""k=7: the 9 dual types' multiplicities in closed form.

MEASURED (q=5, total 1140 triples):

    A (0,1):1 (0,2):2 (0,3):11 (0,4):1                      240
    A (0,3):2 (0,4):3 (1,1):3 (1,2):6 (1,3):1               240
    B (0,4):1 (1,2):8 (2,1):2 (2,2):4                       180
    A (0,2):1 (0,3):11 (0,4):2 (0,5):1                      120
    B (0,5):1 (1,2):4 (1,3):4 (2,1):1 (2,2):5               120
    A (0,2):5 (0,3):8 (0,4):2                               120
    A (0,2):2 (0,3):8 (0,4):5                                60
    A (0,3):6 (0,4):9                                        40
    A (0,2):9 (0,3):6                                        20

The type is determined by the involution structure.  Let me characterise
each type by invariants that can be counted:

  - case A or B
  - the number of involution pairs (n2 for each of the 3 pencils)
  - how the pairs relate to W cap C

Let me measure the type by (case, sorted n2-triple, |W cap C|) and see
whether that determines the type.

Run:  python arc_k7_types.py --q 5
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

            # distribution over T
            dist = Counter()
            for T in itertools.combinations(B, 4):
                Tset = set(T)
                w = len(Tset & WcapC)
                union = set()
                for inv in invs:
                    for pr in inv:
                        if pr[0] in Tset and pr[1] in Tset:
                            union.add(pr)
                dist[(w, len(union))] += 1
            key = (case, tuple(sorted(n2s)), len(WcapC),
                   tuple(sorted(dist.items())))
            joint[key] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (case, n2-triple, |W cap C|, dist) -> count", flush=True)
        for k, v in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
