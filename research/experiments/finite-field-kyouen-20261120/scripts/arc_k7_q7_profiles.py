"""k=7: determining the correct divisor per profile.

q=5 assembly vs exhaustive:

    profile        tuples   asm sets   exh sets   exh/asm
    (4,4,4,4)        9600     312000     312000      1.00
    (4,4,4,4,4)      3000      78000      78000      1.00
    (4,4,4)          2220      96200      96200      1.00
    (5,4,4)          1320      57200      85800      1.50
    (5,4)             480      31200      62400      2.00
    (4,4)             240      15600      15600      1.00
    (4,4,4,4,4,4)     240       5200       5200      1.00

So the divisor used (count of t >= 4) is right for profiles WITHOUT a 5,
but wrong for profiles WITH a 5.

Required divisor = tuples * b / exh_sets:
    (5,4):   480*130/62400 = 1.0
    (5,4,4): 1320*130/85800 = 2.0

So for (5,4) the divisor is 1, for (5,4,4) it is 2.

WHY?  A 7-set with profile (5,4) has ONE 5-circle and ONE 4-circle.
The tuple loop fixes C = P^1(F_q) and T = C cap S.  For S to be counted,
C must be one of S's circles with >= 4 points.

If C is the 5-circle: T = C cap S has 5 points, but the loop uses |T| = 4.
So the 5-circle case is NOT enumerated by the loop (which fixes |T| = 4).

If C is the 4-circle: T = C cap S has 4 points, and the loop counts it once.

So S with profile (5,4) is counted ONCE (via its 4-circle), not twice.
Hence divisor = 1, not 2.

For (5,4,4): S has one 5-circle and two 4-circles.  Counted twice (via each
4-circle).  Divisor = 2.  MATCHES.

For (4,4,4,4): four 4-circles, counted 4 times.  Divisor = 4.  MATCHES.

SO THE CORRECT DIVISOR IS:

    divisor = #{t in P : t == 4}

i.e. the count of 4s ONLY -- which is what the ORIGINAL code used!

Then why did the original give 1,414,000 arcs at q=7?

Because at q=7 the profile (6,) and (7,) cases exist and are NOT generated
by the formula.  Let me check the q=7 exhaustive profile histogram.

Run:  python arc_k7_q7_profiles.py --q 7
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
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
        coq = {}
        for k, BB in enumerate(blocks):
            for quad in itertools.combinations(BB, 4):
                coq[quad] = k

        hist = Counter()
        for S in itertools.combinations(range(n), 7):
            Sset = set(S)
            hits = {}
            for quad in itertools.combinations(S, 4):
                cj = coq.get(quad)
                if cj is None:
                    continue
                hits[cj] = len(Sset & set(blocks[cj]))
            hist[tuple(sorted(hits.values(), reverse=True))] += 1

        row = {"q": q, "n": n, "profiles": {str(k): v for k, v in
                                            sorted(hist.items(),
                                                   key=lambda x: -x[1])},
               "total": sum(hist.values())}
        rows.append(row)
        print(f"q={q}: exhaustive profile histogram", flush=True)
        for p, c in sorted(hist.items(), key=lambda x: -x[1]):
            print(f"    {p}: {c}", flush=True)
        print(f"  total: {sum(hist.values())}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
