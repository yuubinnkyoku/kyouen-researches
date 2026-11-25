"""k=7: the three involutions are either disjoint or share ONE common pair.

MEASURED (q=5, over C(20,3)=1140 triples):

    pairwise common-pair counts (0,0,0): 840
    pairwise common-pair counts (1,1,1): 300

So the three involutions iota(x,y), iota(x,z), iota(y,z) are either
PAIRWISE DISJOINT, or they all share exactly ONE common pair (and nothing
else).

This is a very strong structure.  Let me exploit it.

CASE A (disjoint, 840 triples): the three involutions have no common pair.
    Then j1, j2, j3 count disjoint sets of pairs, so the j's are
    independent-ish and u = j1+j2+j3 (as proved).

CASE B (one common pair, 300 triples): all three involutions contain the
    same pair {p,p'}.  Then that pair contributes 1 to each j IF both p,p'
    are in T.

    - If {p,p'} ⊂ T: j1,j2,j3 all >= 1, and u = j1+j2+j3 - 3 (the common
      pair is counted 3 times but once in the union).
    - If not: the common pair contributes 0 to each j.

Hmm, but u = sum(j) - 3[w=2] was verified for ALL cases.  Let me re-derive.

Actually the earlier proof said: for w=2, W is in all three pencils.  The
common pair {p,p'} IS W ∩ C (since W meets C in 2 points, and W is in all
three pencils means W meets T in 2 points, so W ∩ C = {p,p'} ⊂ T).

So Case B with {p,p'} ⊂ T is exactly w=2.  And Case B with {p,p'} not
subset of T... but then W would not be in the pencils (a pencil circle
must meet T in 2 points).  Contradiction.

So Case B should be exactly w=2.  But Case B has 300 triples and w=2 has
120.  Mismatch.

Let me check: maybe the common pair is not W ∩ C but something else.

Let me measure the relationship between Case B and w.

Run:  python arc_k7_caseB.py --q 5
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
        T = tuple(B[:4])
        Tset = set(T)

        joint = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = circ_of_triple.get(tuple(sorted(xyz)))
            w = len(Tset & set(circles[W])) if W is not None else 0
            invs = []
            for xy in itertools.combinations(xyz, 2):
                pairs = set()
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    cap = Bset & set(circles[cj])
                    if len(cap) == 2:
                        pairs.add(tuple(sorted(cap)))
                invs.append(frozenset(pairs))
            common = (len(invs[0] & invs[1]), len(invs[0] & invs[2]),
                      len(invs[1] & invs[2]))
            case = "B" if common == (1, 1, 1) else "A"
            # is the common pair inside T?
            inT = None
            if case == "B":
                cp = next(iter(invs[0] & invs[1]))
                inT = all(p in Tset for p in cp)
            joint[(case, w, inT)] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "joint": {str(k): v for k, v in
                         sorted(joint.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (case, w, common-pair-in-T) -> count", flush=True)
        for k, v in sorted(joint.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
