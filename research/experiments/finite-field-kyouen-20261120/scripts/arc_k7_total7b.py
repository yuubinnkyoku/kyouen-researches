"""k=7: the arc count at q=7 using the CORRECTED formula.

The corrected profile formula is

    #4-circles = 1 + v + [|W cap T| = 1]
    #5-circles = [|W cap T| = 2]

with v = #{C' != C : |C' cap T| = 2 and |C' cap {x,y,z}| = 2}.

The multiplicity theorem still holds: a 7-set with profile P is counted
once per (4-circle, 4-subset) pair, i.e. #4-circles(P) times.

So:
    #7-sets with profile P = (tuples with P) / #4-circles(P) * b*C(s,4)

Let me assemble and check integrality + consistency.

Run:  python arc_k7_total7b.py --q 7
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
        circ_of_triple = {}
        for k, BB in enumerate(blocks):
            for tri in itertools.combinations(BB, 3):
                circ_of_triple[tri] = k

        outside = [p for p in range(n) if p not in Bset]

        prof_tuples = Counter()
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            for xyz in itertools.combinations(outside, 3):
                xyzset = set(xyz)
                W = circ_of_triple.get(tuple(sorted(xyz)))
                wT = len(Tset & set(blocks[W])) if W is not None else 0
                v = 0
                for kk in range(b):
                    if kk == ci:
                        continue
                    if len(Tset & set(blocks[kk])) != 2:
                        continue
                    if len(xyzset & set(blocks[kk])) == 2:
                        v += 1
                n4 = 1 + v + (1 if wT == 1 else 0)
                n5 = 1 if wT == 2 else 0
                prof = tuple([5] * n5 + [4] * n4)
                prof_tuples[prof] += 1

        scale = b * comb(s, 4)
        bad = Fraction(0)
        detail = {}
        nonint = []
        for prof, cnt in prof_tuples.items():
            n4 = sum(1 for t in prof if t == 4)
            sets = Fraction(cnt, n4) * scale
            if sets.denominator != 1:
                nonint.append((str(prof), cnt, n4, str(sets)))
            bad += sets
            detail[str(prof)] = str(sets)
        six = b * comb(s, 6) * (n - s)
        bad += six
        arcs = comb(n, 7) - bad

        row = {"q": q, "n": n, "b": b, "s": s,
               "num_profiles": len(prof_tuples),
               "profile_sets": detail, "six_term": six,
               "bad": str(bad), "arcs": str(arcs),
               "C(n,7)": comb(n, 7),
               "bad_integer": bad.denominator == 1,
               "arcs_integer": arcs.denominator == 1,
               "non_integer_profiles": nonint[:5],
               "consistent": bad + arcs == comb(n, 7)}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}, profiles {len(prof_tuples)}",
              flush=True)
        print(f"  bad = {bad}  (integer: {bad.denominator == 1})", flush=True)
        print(f"  arcs = {arcs}  (integer: {arcs.denominator == 1})",
              flush=True)
        print(f"  C(n,7) = {comb(n,7)}", flush=True)
        print(f"  consistent: {row['consistent']}", flush=True)
        if nonint:
            print(f"  NON-INTEGER profiles: {nonint[:3]}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
