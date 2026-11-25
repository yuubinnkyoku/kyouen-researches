"""k=7: the profile structure.

For k=6 the bad sets split into exactly five profiles (6,), (5,), (4,),
(4,4), (4,4,4).  For k=7 the profiles are richer because three circles can
each carry 4 points.

BOUND.  If m circles each carry >= 4 points of a k-set S, and two circles
share at most 2 points, then

    |S| >= 4m - 2*C(m,2)

For k=7:  m=1 -> 4, m=2 -> 6, m=3 -> 6, m=4 -> 4.  So m can be up to 3
comfortably (and 4 in principle).

This script enumerates the actual profiles for q=5 (C(26,7) = 657800,
feasible) and reports the distribution.

Run:  python arc_k7_profiles.py --q 5
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
        circ_of_quad = {}
        for ci, B in enumerate(circles):
            for quad in itertools.combinations(B, 4):
                circ_of_quad[quad] = ci

        fam = Counter()
        arcs = 0
        for S in itertools.combinations(range(n), 7):
            Sset = set(S)
            hits = {}
            for quad in itertools.combinations(S, 4):
                ci = circ_of_quad.get(quad)
                if ci is None:
                    continue
                hits[ci] = len(Sset & set(circles[ci]))
            if not hits:
                arcs += 1
                continue
            fam[tuple(sorted(hits.values(), reverse=True))] += 1

        row = {"q": q, "n": n, "b": b, "C(n,7)": comb(n, 7),
               "arcs": arcs, "bad": sum(fam.values()),
               "profiles": {str(k): v for k, v in
                            sorted(fam.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, C(n,7)={comb(n,7)}", flush=True)
        print(f"  arcs = {arcs}, bad = {sum(fam.values())}", flush=True)
        print(f"  profiles:", flush=True)
        for prof, cnt in sorted(fam.items(), key=lambda x: -x[1]):
            print(f"    {prof}: {cnt}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
