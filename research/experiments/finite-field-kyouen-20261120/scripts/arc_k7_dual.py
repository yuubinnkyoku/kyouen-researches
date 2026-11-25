"""k=7: the (w,u) distribution via the TRIPLE's own circle structure.

The remaining open quantity is the joint law of (w, u) over triples
{x,y,z} outside C.

KEY REFRAME.  Instead of fixing T and varying {x,y,z}, fix the TRIPLE and
vary T.  The triple {x,y,z} determines:
    W = the circle through x,y,z
    the three pencils, hence the three involutions iota(x,y), iota(x,z),
    iota(y,z)

and then w = |T cap W| and u = (number of involution pairs inside T,
counted with the W correction) are both functions of T.

So for a FIXED triple, (w,u) is determined by how the 4-subset T sits
relative to W and the three involutions.  That is a small combinatorial
problem on C (a set of size s = q+1).

This is the right direction: the distribution of (w,u) over T for a fixed
triple is a hypergeometric-type count, and then we sum over triples.

Let me measure, for each triple TYPE (characterised by the involution
structure), the distribution of (w,u) over T.

Run:  python arc_k7_dual.py --q 5
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

        # For each triple, compute the involution structure and then the
        # (w,u) distribution over all 4-subsets T of C.
        type_hist = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = circ_of_triple.get(tuple(sorted(xyz)))
            WcapC = Bset & set(circles[W]) if W is not None else set()
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

            # distribution of (w,u) over T
            dist = Counter()
            for T in itertools.combinations(B, 4):
                Tset = set(T)
                w = len(Tset & WcapC)
                union = set()
                for inv in invs:
                    for pr in inv:
                        if pr[0] in Tset and pr[1] in Tset:
                            union.add(pr)
                u = len(union)
                dist[(w, u)] += 1
            type_hist[(case, tuple(sorted(dist.items())))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "types": {str(k): v for k, v in
                         sorted(type_hist.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  distinct (case, (w,u)-distribution-over-T) types: "
              f"{len(type_hist)}", flush=True)
        for k, v in sorted(type_hist.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
