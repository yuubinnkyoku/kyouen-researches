"""k=8: the exact 8-arc count at q=9 (the smallest case with K >= 8).

At q=9: n=82, b=738, s=10.  C(82,8) = 82!/(8!74!) ~ 1.6e10 -- too many
to enumerate directly.

APPROACH: use the same profile method as k=7.  An 8-set S has a profile
of circles carrying >= 4 points.  The key structural fact:

  For S = T u {x,y,z,w} with |T| = 4, T in C, and x,y,z,w outside C,
  a circle C' != C carries at most 2 of T, so
      |C' cap S| <= 2 + 4 = 6.

So the profile values are 4, 5, 6 (plus C itself with 4).

That means the k=8 profile formula is a natural extension of k=7's.

BUT: the number of (T, {x,y,z,w}) tuples is C(10,4)*C(72,4) = 210*1,028,790
= 216 million -- too slow in Python.

ALTERNATIVE: count 8-arcs by INCLUSION-EXCLUSION on the 4-circles.

    #8-arcs = C(n,8) - |union of "S contains a 4-circle"|

The 4-circles are b*C(s,4) = 738*210 = 154,980 sets of 4 points.  An 8-set
contains a 4-circle iff it contains one of these.  Inclusion-exclusion over
154,980 sets is infeasible directly, but the STRUCTURE (each 4-circle is
a subset of a unique circle) makes it tractable:

    #8-arcs = sum over 8-sets with no 4-circle

Let me instead count via the "which circles does S meet in >= 4 points"
decomposition, which is what the profile method does.

Given the cost, let me first check whether a cheaper invariant suffices:
compute the number of 8-sets that ARE arcs using a randomised/structured
search, or accept that k=8 at q=9 is out of reach and instead compute the
k=8 count at q=9 via the profile formula with an optimised loop.

Run:  python arc_k8_start.py --q 9
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from collections import Counter
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field, build_inversive_plane  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[9])
    ap.add_argument("--limit", type=int, default=200000)
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
        outside = [p for p in range(n) if p not in Bset]

        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  C(n,8) = {comb(n,8)}", flush=True)
        print(f"  tuples (T, 4 outside) = C(s,4)*C(n-s,4) = "
              f"{comb(s,4)*comb(n-s,4)}", flush=True)

        # sample the profile distribution to see the structure
        prof = Counter()
        cnt = 0
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            for quad in itertools.combinations(outside, 4):
                Sset = Tset | set(quad)
                hits = {}
                for sub4 in itertools.combinations(sorted(Sset), 4):
                    cj = circ_of_triple.get(tuple(sorted(sub4[:3])))
                    if cj is None:
                        continue
                    if all(p in blocks[cj] for p in sub4):
                        hits[cj] = len(Sset & set(blocks[cj]))
                prof[tuple(sorted(hits.values(), reverse=True))] += 1
                cnt += 1
                if cnt >= args.limit:
                    break
            if cnt >= args.limit:
                break

        row = {"q": q, "n": n, "b": b, "s": s,
               "sampled": cnt,
               "profiles": {str(k): v for k, v in
                            sorted(prof.items(), key=lambda x: -x[1])},
               "seconds": round(time.time() - t0, 1)}
        rows.append(row)
        print(f"  sampled {cnt} tuples in {row['seconds']}s", flush=True)
        print(f"  distinct profiles: {len(prof)}", flush=True)
        for k, v in sorted(prof.items(), key=lambda x: -x[1])[:10]:
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
