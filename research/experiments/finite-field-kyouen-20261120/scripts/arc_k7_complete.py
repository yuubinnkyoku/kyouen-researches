"""k=7: the COMPLETE arc count, verified end-to-end at q=5 and q=7.

All profiles are now determined:

    (7,) = b*C(s,7)
    (6,) = b*C(s,6)*(n-s)
    (5,) = b * #{T5,{x,y} : no pencil circle through x,y meets T5 in 2}
    others = (tuples with P) / (#4s in P) * b

where the tuples come from the corrected profile formula

    #4-circles = 1 + v + [|W cap T| = 1]
    #5-circles = [|W cap T| = 2]
    v = #{C' != C : |C' cap T| = 2 and |C' cap {x,y,z}| = 2}

Run:  python arc_k7_complete.py --q 5 7
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
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
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
        circ_through_pair = {}
        for k, BB in enumerate(blocks):
            for pair in itertools.combinations(BB, 2):
                circ_through_pair.setdefault(pair, []).append(k)

        outside = [p for p in range(n) if p not in Bset]

        # --- profiles from the tuple formula ---
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
                prof_tuples[tuple([5] * n5 + [4] * n4)] += 1

        bad = Fraction(0)
        detail = {}
        for prof, cnt in prof_tuples.items():
            n4 = sum(1 for t in prof if t == 4)
            sets = Fraction(cnt, n4) * b
            bad += sets
            detail[str(prof)] = int(sets)

        # --- the three single-circle profiles ---
        six = b * comb(s, 6) * (n - s) if s >= 6 else 0
        seven = b * comb(s, 7) if s >= 7 else 0
        five = 0
        if s >= 5:
            cnt0 = 0
            for T5 in itertools.combinations(B, 5):
                T5set = set(T5)
                for xy in itertools.combinations(outside, 2):
                    hit = False
                    for kk in circ_through_pair.get(tuple(sorted(xy)), []):
                        if kk == ci:
                            continue
                        if len(T5set & set(blocks[kk])) == 2:
                            hit = True
                            break
                    if not hit:
                        cnt0 += 1
            five = b * cnt0

        bad += six + seven + five
        arcs = comb(n, 7) - bad

        row = {"q": q, "n": n, "b": b, "s": s,
               "profile_sets": detail,
               "five": five, "six": six, "seven": seven,
               "bad": str(bad), "arcs": str(arcs),
               "C(n,7)": comb(n, 7),
               "bad_integer": bad.denominator == 1,
               "consistent": bad + arcs == comb(n, 7)}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  profiles: {detail}", flush=True)
        print(f"  (5,)={five}  (6,)={six}  (7,)={seven}", flush=True)
        print(f"  bad = {bad}  (integer: {bad.denominator == 1})", flush=True)
        print(f"  arcs = {arcs}", flush=True)
        print(f"  C(n,7) = {comb(n,7)}", flush=True)
        print(f"  consistent: {row['consistent']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
