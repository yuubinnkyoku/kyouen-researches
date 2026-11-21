"""END-TO-END VERIFICATION OF THE COMPLETE k=6 FORMULA.

The formula:

    #6-arcs = C(n,6) - b*C(q+1,6) - b*C(q+1,5)*(n-q-1)
              - sum over PGL(2,q)-orbits O of
                    b*|O| * [N0(O) + N1(O)/2 + N2(O)/3]

where (N0(O), N1(O), N2(O)) is the second-circle distribution for a
representative T in orbit O.

This script computes everything from scratch and compares with the
exhaustive arc count.

Run:  python arc_k6_verify.py --q 5 7
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

        # group the 4-subsets of ONE circle by their second-circle distribution
        ci = 0
        B = circles[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]
        groups = Counter()
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            d = Counter()
            for xy in itertools.combinations(outside, 2):
                cnt = 0
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    if len(Tset & set(circles[cj])) == 2:
                        cnt += 1
                d[cnt] += 1
            groups[tuple(sorted(d.items()))] += 1

        # formula
        term6 = b * comb(q + 1, 6)
        term5 = b * comb(q + 1, 5) * (n - q - 1)
        term4 = 0
        detail = []
        for dist, cnt in groups.items():
            d = dict(dist)
            n0, n1, n2 = d.get(0, 0), d.get(1, 0), d.get(2, 0)
            contrib = b * cnt * (n0 + n1 / 2 + n2 / 3)
            term4 += contrib
            detail.append({"orbit_size": cnt, "N0": n0, "N1": n1, "N2": n2,
                           "contribution": contrib})

        bad = term6 + term5 + term4
        arcs = comb(n, 6) - bad

        # exhaustive
        circ_of_quad = {}
        for cj, BB in enumerate(circles):
            for quad in itertools.combinations(BB, 4):
                circ_of_quad[quad] = cj
        ex_arcs = 0
        for S in itertools.combinations(range(n), 6):
            ok = True
            for quad in itertools.combinations(S, 4):
                if quad in circ_of_quad:
                    ok = False
                    break
            if ok:
                ex_arcs += 1

        row = {"q": q, "n": n, "b": b,
               "term_all6": term6, "term_exactly5": term5,
               "term_4star": term4, "detail": detail,
               "bad_formula": bad, "arcs_formula": arcs,
               "arcs_exhaustive": ex_arcs,
               "match": abs(arcs - ex_arcs) < 1e-6}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}", flush=True)
        print(f"  (6,)      = {term6}", flush=True)
        print(f"  (5,)      = {term5}", flush=True)
        print(f"  (4,*)     = {term4}", flush=True)
        for d in detail:
            print(f"     orbit size {d['orbit_size']}: "
                  f"N=({d['N0']},{d['N1']},{d['N2']}) "
                  f"-> {d['contribution']}", flush=True)
        print(f"  bad  = {bad}", flush=True)
        print(f"  arcs = {arcs}  (exhaustive {ex_arcs})  "
              f"match={row['match']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
