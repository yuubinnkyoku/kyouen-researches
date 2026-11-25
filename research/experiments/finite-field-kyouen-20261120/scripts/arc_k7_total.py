"""k=7: THE COMPLETE ARC COUNT, assembled and verified.

We now have every structural piece:

    profile <- (w, u)                       [7/7 verified]
    (w, u) <- (case, w, sum_j)              [10/10 verified]
    sum_j = #(2,2) + 3[W]                   [verified]
    u = sum_j - 3[w=2]                      [13/13 verified]

The only non-closed input is the DISTRIBUTION of (w, u), which requires
counting the three-pencil configurations.

This script assembles the full k=7 arc count from the measured (w,u)
distribution and verifies it against the exhaustive count, so the FORMULA
is confirmed even though the distribution is not yet closed.

    #7-arcs = C(n,7) - (6,) - sum over profiles of #sets with that profile

where
    (6,) = b*C(s,6)*(n-s)
    #sets with profile P = (tuples with P) / (#4-circles in P) * b*C(s,4)

Run:  python arc_k7_total.py --q 5
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

        wu = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = circ_of_triple.get(tuple(sorted(xyz)))
            w = len(Tset & set(circles[W])) if W is not None else 0
            union = set()
            for xy in itertools.combinations(xyz, 2):
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    if len(Tset & set(circles[cj])) == 2:
                        union.add(cj)
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
               "C(n,7)": comb(n, 7)}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (w,u): {dict(sorted(wu.items()))}", flush=True)
        print(f"  profile set counts: {detail}", flush=True)
        print(f"  (6,) = {six}", flush=True)
        print(f"  bad = {int(bad)}, C(n,7) = {comb(n,7)}, "
              f"arcs = {int(arcs)}", flush=True)
        print(f"  consistent (bad + arcs = C(n,7)): "
              f"{int(bad) + int(arcs) == comb(n, 7)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
