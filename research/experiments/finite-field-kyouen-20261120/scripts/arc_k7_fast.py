"""k=7: a FAST (5,) computation, enabling q=9 and beyond.

The slow part of arc_k7_complete.py is the (5,) loop:

    for T5 in C(s,5): for xy in C(n-s,2): check all q+1 pencil circles

That is O(C(s,5) * C(n-s,2) * q).  At q=9: C(10,5)*C(72,2)*10 = 252*2556*10
= 6.4M -- actually fine.  The real cost is the TUPLE loop:

    for T in C(s,4): for xyz in C(n-s,3): for kk in range(b)

That is O(C(s,4) * C(n-s,3) * b).  At q=9: 210 * 59640 * 738 = 9.2 BILLION.
That is the bottleneck.

OPTIMISATION.  Instead of scanning all b circles for each (T,xyz), use the
pencil structure: v counts circles through 2 of {x,y,z} meeting T in 2
points.  For each of the 3 pairs, the pencil has q+1 circles; check those
only.  That is O(C(s,4) * C(n-s,3) * 3 * q) = 210*59640*30 = 376M.  Still
heavy but 25x better.

FURTHER: v depends only on (T, the 3 pencils).  Group by the pencil
triple.  But simpler: just implement the 3-pencil version and try q=9.

Run:  python arc_k7_fast.py --q 9
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field, build_inversive_plane  # noqa: E402
from arc_k7_five_closed import five_profile  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[9])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        t0 = time.time()
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
        tb = time.time() - t0
        print(f"q={q}: n={n}, b={b}, s={s}, build {tb:.1f}s", flush=True)

        # --- fast tuple loop: v via the 3 pencils only ---
        prof_tuples = Counter()
        t1 = time.time()
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            for xyz in itertools.combinations(outside, 3):
                xyzset = set(xyz)
                W = circ_of_triple.get(tuple(sorted(xyz)))
                wT = len(Tset & set(blocks[W])) if W is not None else 0
                v = 0
                seen = set()
                for xy in itertools.combinations(xyz, 2):
                    for kk in circ_through_pair.get(tuple(sorted(xy)), []):
                        if kk == ci or kk in seen:
                            continue
                        if len(Tset & set(blocks[kk])) != 2:
                            continue
                        if len(xyzset & set(blocks[kk])) == 2:
                            seen.add(kk)
                            v += 1
                n4 = 1 + v + (1 if wT == 1 else 0)
                n5 = 1 if wT == 2 else 0
                prof_tuples[tuple([5] * n5 + [4] * n4)] += 1
        t2 = time.time() - t1
        print(f"  tuple loop: {t2:.1f}s, {len(prof_tuples)} profiles",
              flush=True)

        bad = Fraction(0)
        detail = {}
        for prof, cnt in prof_tuples.items():
            n4 = sum(1 for t in prof if t == 4)
            sets = Fraction(cnt, n4) * b
            bad += sets
            detail[str(prof)] = int(sets)

        six = b * comb(s, 6) * (n - s) if s >= 6 else 0
        seven = b * comb(s, 7) if s >= 7 else 0
        five = five_profile(q)
        bad += six + seven + five
        arcs = comb(n, 7) - bad

        row = {"q": q, "n": n, "b": b, "s": s,
               "profile_sets": detail,
               "five": five, "six": six, "seven": seven,
               "bad": str(bad), "arcs": str(arcs),
               "C(n,7)": comb(n, 7),
               "bad_integer": bad.denominator == 1,
               "consistent": bad + arcs == comb(n, 7),
               "seconds": round(time.time() - t0, 1)}
        rows.append(row)
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
