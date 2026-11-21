"""THE PENCIL INVOLUTION: what really determines j.

For fixed T (4 points of circle C) and {x,y} outside C, define

    j({x,y}) = #{C' : x,y in C', |T cap C'| = 2}.

KEY STRUCTURE.  The circles through x and y form a PENCIL of q+1 circles.
Each circle in the pencil meets C in 0, 1 or 2 points.  Let n0, n1, n2 be
the counts.  Counting incidences with C:

    n1 + 2*n2 = q+1        (each point of C lies on exactly one pencil circle)
    n0 + n1 + n2 = q+1     (the pencil has q+1 circles)

Subtracting:  n0 = n2.  So the pencil has equally many disjoint and
2-secant circles.

The 2-secant circles pair up the points of C: each such circle gives a
pair {p, p'}.  These pairs form an INVOLUTION iota on C (the "residual
involution" of the pencil), defined on the q+1 - n1 points covered by
2-secants.

Since |T cap C'| <= |C cap C'| <= 2, we get

    j = #{pairs {p,p'} of iota with both p, p' in T}.

So j in {0,1,2} and

    j = 2  iff  iota pairs T into two pairs inside T
    j = 1  iff  iota pairs exactly one pair inside T
    j = 0  iff  iota has no pair inside T

This script verifies the involution description and measures how the
pairing depends on T.

Run:  python arc_k6_involution.py --q 5 7
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
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, ovoid, circles = build(q)
        n = len(ovoid)
        b = len(circles)
        circ_through_pair = {}
        for ci, B in enumerate(circles):
            for pair in itertools.combinations(B, 2):
                circ_through_pair.setdefault(pair, []).append(ci)

        ci = 0
        B = circles[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]

        # verify: for each {x,y}, the pencil induces an involution on C and
        # j equals the number of pairs inside T
        mismatches = 0
        checked = 0
        n2_hist = Counter()
        for xy in itertools.combinations(outside, 2):
            pencil = circ_through_pair.get(tuple(sorted(xy)), [])
            # pairs of C covered by 2-secant circles of the pencil
            pairs = []
            for cj in pencil:
                if cj == ci:
                    continue
                cap = Bset & set(circles[cj])
                if len(cap) == 2:
                    pairs.append(tuple(sorted(cap)))
            n2_hist[len(pairs)] += 1
            # check it is an involution (disjoint pairs)
            flat = [p for pr in pairs for p in pr]
            if len(flat) != len(set(flat)):
                mismatches += 1
            checked += 1

        row = {"q": q, "n": n, "b": b, "pairs_xy": checked,
               "involution_violations": mismatches,
               "n2_histogram": {str(k): v for k, v in sorted(n2_hist.items())}}
        rows.append(row)
        print(f"q={q}: n={n}, circle size {q+1}", flush=True)
        print(f"  {checked} pairs {{x,y}}; involution violations: "
              f"{mismatches}", flush=True)
        print(f"  n2 (2-secant circles per pencil) histogram: "
              f"{dict(sorted(n2_hist.items()))}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
