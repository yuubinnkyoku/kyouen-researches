"""THE (n2, j) TABLE IS HYPERGEOMETRIC: k=6 CLOSES.

VERIFIED.  For an involution iota on C with n2 pairs and n1 = q+1-2*n2
fixed points, the number of 4-subsets T containing exactly j pairs is

    H(n2, n1, j) = sum_a C(n2,j) * C(n2-j,a) * 2^a * C(n1, 4-2j-a)

and the measured counts are exactly

    #{({x,y}, T) : n2, j} = N_xy(n2) * H(n2, n1, j)

where N_xy(n2) = number of {x,y} whose pencil has n2 2-secant circles.

Check (q=5, n2=2, n1=2):
    H = (4, 10, 1) for j = 0,1,2
    N_xy(2) = 120
    120*(4,10,1) = (480, 1200, 120)   MATCHES

Check (q=5, n2=3, n1=0):
    H = (0, 12, 3)
    N_xy(3) = 70
    70*(0,12,3) = (0, 840, 210)       MATCHES

Check (q=7, n2=3, n1=2):
    H = (28, 39, 3)
    N_xy(3) = 504
    504*(28,39,3) = (14112, 19656, 1512)  MATCHES

Check (q=7, n2=4, n1=0):
    H = (16, 48, 6)
    N_xy(4) = 357
    357*(16,48,6) = (5712, 17136, 2142)   MATCHES

ALL FOUR MATCH EXACTLY.

SO THE k=6 ARC COUNT IS:

    #6-arcs = C(n,6) - b*C(q+1,6) - b*C(q+1,5)*(n-q-1)
              - b * sum over n2 of N_xy(n2) * [H(n2,n1,0) + H(n2,n1,1)/2
                                                + H(n2,n1,2)/3]

Wait -- careful.  The (4,*) profiles are counted per (C,T,{x,y}), and each
6-set with profile (4,4) is counted twice etc.  Let me redo.

For a fixed (C, T) and {x,y}, j is determined.  The 6-set S = T u {x,y}
has profile determined by j.  Summing over all (C,T,{x,y}) counts each
6-set with profile (4,*) exactly (j+1) times.

So:
    #{(C,T,{x,y}) with j} = b * C(q+1,4) * N_xy_total * P(j | ...)
and the contribution to bad 6-sets is
    sum_j #{...j} / (j+1).

Using the hypergeometric structure:
    #{... with n2, j} = b * N_xy(n2) * H(n2, n1, j)

so
    (4,*) contribution = b * sum_{n2} N_xy(n2) * [H(n2,n1,0)
                                                  + H(n2,n1,1)/2
                                                  + H(n2,n1,2)/3]

Let me verify this numerically.

Run:  python arc_k6_closed.py --q 5 7
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


def H(n2, n1, j, k=4):
    """#k-subsets of (n2 pairs + n1 singles) containing exactly j pairs."""
    total = 0
    for a in range(0, n2 - j + 1):
        used = 2 * j + a
        if used > k:
            break
        rest = k - used
        if rest < 0 or rest > n1:
            continue
        total += (comb(n2, j) * comb(n2 - j, a) * (2 ** a)
                  * comb(n1, rest))
    return total


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

        # measure N_xy(n2)
        N_xy = Counter()
        for xy in itertools.combinations(outside, 2):
            pencil = circ_through_pair.get(tuple(sorted(xy)), [])
            n2 = 0
            for cj in pencil:
                if cj == ci:
                    continue
                if len(Bset & set(circles[cj])) == 2:
                    n2 += 1
            N_xy[n2] += 1

        # closed-form (4,*) contribution
        contrib = 0
        detail = []
        for n2, cnt in sorted(N_xy.items()):
            n1 = q + 1 - 2 * n2
            h0, h1, h2 = H(n2, n1, 0), H(n2, n1, 1), H(n2, n1, 2)
            c = b * cnt * (h0 + h1 / 2 + h2 / 3)
            contrib += c
            detail.append({"n2": n2, "n1": n1, "N_xy": cnt,
                           "H": [h0, h1, h2], "contribution": c})

        term6 = b * comb(q + 1, 6)
        term5 = b * comb(q + 1, 5) * (n - q - 1)
        bad = term6 + term5 + contrib
        arcs = comb(n, 6) - bad

        # exhaustive
        circ_of_quad = {}
        for cj, BB in enumerate(circles):
            for quad in itertools.combinations(BB, 4):
                circ_of_quad[quad] = cj
        ex = 0
        for S in itertools.combinations(range(n), 6):
            if not any(quad in circ_of_quad
                       for quad in itertools.combinations(S, 4)):
                ex += 1

        row = {"q": q, "n": n, "b": b, "N_xy": dict(N_xy),
               "detail": detail, "term6": term6, "term5": term5,
               "contrib4": contrib, "bad": bad, "arcs": arcs,
               "exhaustive": ex, "match": abs(arcs - ex) < 1e-6}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}", flush=True)
        print(f"  N_xy = {dict(sorted(N_xy.items()))}", flush=True)
        for d in detail:
            print(f"    n2={d['n2']} n1={d['n1']} N_xy={d['N_xy']} "
                  f"H={d['H']} -> {d['contribution']}", flush=True)
        print(f"  (6,)={term6} (5,)={term5} (4,*)={contrib}", flush=True)
        print(f"  arcs={arcs} (exhaustive {ex}) match={row['match']}",
              flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
