"""k=7: END-TO-END VERIFICATION of the profile formula.

Rather than closing the (w, j-triple) distribution analytically, let me
verify that the k=7 profile formula reproduces the exhaustive counts, using
the measured (w, u) distribution as input.  That confirms the formula is
correct even though the distribution itself is not yet closed.

The formula:
    #4-circles = 1 + u + [w = 1]
    #5-circles = [w = 2]

so the profile is determined by (w, u), and the number of 7-sets with
profile P is (tuples with that profile) / (#4-circles in P).

Run:  python arc_k7_endtoend.py --q 5
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

        # (w,u) distribution and the formula-predicted profile
        wu = Counter()
        pred_prof = Counter()
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
            n4 = 1 + u + (1 if w == 1 else 0)
            n5 = 1 if w == 2 else 0
            prof = tuple([5] * n5 + [4] * n4)
            pred_prof[prof] += 1

        # convert tuple counts to set counts, then scale by b*C(s,4)
        # (the tuple loop fixes one circle C and one 4-subset T of it).
        # Use exact fractions: a profile with n4 four-circles is counted n4
        # times, and the division must be exact only after summing over all
        # (C,T) -- so accumulate as Fraction.
        from fractions import Fraction
        scale = b * comb(s, 4)
        pred_sets = Counter()
        for prof, cnt in pred_prof.items():
            n4 = sum(1 for t in prof if t == 4)
            pred_sets[prof] += Fraction(cnt, n4) * scale

        # exhaustive
        circ_of_quad = {}
        for cj, BB in enumerate(circles):
            for quad in itertools.combinations(BB, 4):
                circ_of_quad[quad] = cj
        ex = Counter()
        for S in itertools.combinations(range(n), 7):
            Sset = set(S)
            hits = {}
            for quad in itertools.combinations(S, 4):
                cj = circ_of_quad.get(quad)
                if cj is None:
                    continue
                hits[cj] = len(Sset & set(circles[cj]))
            if not hits:
                ex[("ARC",)] += 1
                continue
            ex[tuple(sorted(hits.values(), reverse=True))] += 1

        pred_int = {k: int(v) for k, v in pred_sets.items()}
        # (6,) is the separate "one circle carries all 6" term, handled by
        # b*C(s,6)*C(n-s,1); exclude it from the (w,u) comparison.
        ex_int = {k: v for k, v in ex.items()
                  if k != ("ARC",) and k != (6,)}
        row = {"q": q, "n": n, "b": b, "s": s,
               "wu": {f"{a},{c}": v for (a, c), v in sorted(wu.items())},
               "predicted": {str(k): v for k, v in sorted(pred_int.items())},
               "exhaustive": {str(k): v for k, v in sorted(ex_int.items())},
               "six_term": ex.get((6,), 0),
               "six_formula": b * comb(s, 6) * (n - s),
               "match": pred_int == ex_int}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (w,u) distribution: {dict(sorted(wu.items()))}", flush=True)
        print(f"  predicted profiles: "
              f"{ {k: int(v) for k, v in sorted(pred_sets.items())} }",
              flush=True)
        print(f"  exhaustive profiles: {dict(sorted(ex.items()))}", flush=True)
        print(f"  match (excluding the separate (6,) term): {row['match']}",
              flush=True)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
