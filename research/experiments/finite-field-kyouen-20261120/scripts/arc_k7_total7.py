"""k=7: the complete arc count at q=7, assembled from the structure.

At q=7, C(50,7) = 99,884,400 seven-subsets.  Exhaustive enumeration is
feasible but slow.  Instead, assemble the count from the verified pieces:

    #7-arcs = C(n,7) - (6,) - sum over profiles of #sets with that profile

    (6,) = b*C(s,6)*(n-s)
    #sets with profile P = (tuples with P) / (#4-circles in P) * b*C(s,4)

and the tuples come from the (w,u) distribution over (C,T,{x,y,z}).

At q=7 the (w,u) distribution is measured by arc_k7_wu.py.

Run:  python arc_k7_total7.py --q 7
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field, build_inversive_plane  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[7])
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
        circ_of_triple = {}
        for k, BB in enumerate(blocks):
            for tri in itertools.combinations(BB, 3):
                circ_of_triple[tri] = k

        outside = [p for p in range(n) if p not in Bset]

        wu = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = circ_of_triple.get(tuple(sorted(xyz)))
            WcapC = Bset & set(blocks[W]) if W is not None else set()
            w = len(WcapC)
            union = set()
            for xy in itertools.combinations(xyz, 2):
                for kk in circ_through_pair.get(tuple(sorted(xy)), []):
                    if kk == ci:
                        continue
                    if len(Bset & set(blocks[kk])) == 2:
                        union.add(kk)
            u = len(union - ({W} if W is not None else set()))
            wu[(w, u)] += 1

        # assemble
        scale = b * comb(s, 4)
        prof_tuples = Counter()
        for (w, u), cnt in wu.items():
            n4 = 1 + u + (1 if w == 1 else 0)
            n5 = 1 if w == 2 else 0
            prof = tuple([5] * n5 + [4] * n4)
            prof_tuples[prof] += cnt

        bad = Fraction(0)
        detail = {}
        for prof, cnt in prof_tuples.items():
            n4 = sum(1 for t in prof if t == 4)
            sets = Fraction(cnt, n4) * scale
            bad += sets
            detail[str(prof)] = int(sets)
        six = b * comb(s, 6) * (n - s)
        bad += six
        arcs = comb(n, 7) - bad

        row = {"q": q, "n": n, "b": b, "s": s,
               "wu": {f"{a},{c}": v for (a, c), v in sorted(wu.items())},
               "profile_sets": detail, "six_term": six,
               "bad": int(bad), "arcs": int(arcs),
               "C(n,7)": comb(n, 7),
               "consistent": int(bad) + int(arcs) == comb(n, 7)}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (w,u) classes: {len(wu)}", flush=True)
        print(f"  profile set counts: {detail}", flush=True)
        print(f"  (6,) = {six}", flush=True)
        print(f"  bad = {int(bad)}, C(n,7) = {comb(n,7)}, "
              f"arcs = {int(arcs)}", flush=True)
        print(f"  consistent: {row['consistent']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
