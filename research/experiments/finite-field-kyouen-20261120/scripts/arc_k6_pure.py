"""THE COMPLETE k=6 CLOSED FORM: pure formula, no enumeration.

All ingredients are now closed:

    n = q^2+1,  b = q(q^2+1),  s = q+1

    N_xy(n2):
        q odd :  (q^2-1)*C(q,2)/2  pairs with n2 = (q+1)/2 - 1
                 the rest          with n2 = (q+1)/2
        q even:  C(q,2)            pairs with n2 = 0
                 the rest          with n2 = q/2

    H(n2, n1, j) = sum_a C(n2,j)*C(n2-j,a)*2^a*C(n1, 4-2j-a),
                   n1 = q+1-2*n2

    #6-arcs = C(n,6) - b*C(s,6) - b*C(s,5)*(n-s)
              - b * sum_{n2} N_xy(n2) * [H(n2,n1,0) + H(n2,n1,1)/2
                                         + H(n2,n1,2)/3]

This script evaluates the formula for q = 5, 7, 8 and compares with the
exhaustive counts.

Run:  python arc_k6_pure.py --q 5 7 8
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from math import comb
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arc_on_quadric import build  # noqa: E402


def H(n2, n1, j, k=4):
    total = 0
    for a in range(0, n2 - j + 1):
        used = 2 * j + a
        if used > k:
            break
        rest = k - used
        if rest < 0 or rest > n1:
            continue
        total += comb(n2, j) * comb(n2 - j, a) * (2 ** a) * comb(n1, rest)
    return total


def N_xy(q):
    """Closed-form N_xy(n2) as a dict."""
    n = q * q + 1
    s = q + 1
    total_pairs = comb(n - s, 2)
    if q % 2 == 1:
        special = (q * q - 1) * comb(q, 2) // 2
        n2a = (q + 1) // 2 - 1
        n2b = (q + 1) // 2
        return {n2a: special, n2b: total_pairs - special}
    else:
        special = comb(q, 2)
        n2a = 0
        n2b = q // 2
        return {n2a: special, n2b: total_pairs - special}


def arcs6(q):
    n = q * q + 1
    b = q * (q * q + 1)
    s = q + 1
    term6 = b * comb(s, 6)
    term5 = b * comb(s, 5) * (n - s)
    contrib = Fraction(0)
    for n2, cnt in N_xy(q).items():
        n1 = s - 2 * n2
        h0, h1, h2 = H(n2, n1, 0), H(n2, n1, 1), H(n2, n1, 2)
        contrib += b * cnt * (h0 + Fraction(h1, 2) + Fraction(h2, 3))
    bad = term6 + term5 + contrib
    return comb(n, 6) - bad, {"term6": term6, "term5": term5,
                              "contrib": contrib, "N_xy": N_xy(q)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7, 8])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        val, detail = arcs6(q)
        # exhaustive
        F, ovoid, circles = build(q)
        n = len(ovoid)
        circ_of_quad = {}
        for cj, BB in enumerate(circles):
            for quad in itertools.combinations(BB, 4):
                circ_of_quad[quad] = cj
        ex = 0
        for S in itertools.combinations(range(n), 6):
            if not any(quad in circ_of_quad
                       for quad in itertools.combinations(S, 4)):
                ex += 1
        ok = abs(val - ex) < 1e-6
        row = {"q": q, "n": n, "formula": val, "exhaustive": ex,
               "match": ok, **detail}
        rows.append(row)
        print(f"q={q}: n={n}", flush=True)
        print(f"  N_xy = {detail['N_xy']}", flush=True)
        print(f"  (6,)={detail['term6']} (5,)={detail['term5']} "
              f"(4,*)={detail['contrib']}", flush=True)
        print(f"  formula = {val}, exhaustive = {ex}, match = {ok}",
              flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
