"""Random sampling of graphs, looking for full graph arcs S = {(a, f(a))}.

A full graph has q points.  If one exists for a given q then K(q) >= q, which
would be far above the current lower bounds (about 0.65q, K1251).  The test for
one sample is b = q(q^2+1) popcounts against the circle bitmasks, so hundred
thousands of samples are cheap.

Run:  python graph_random_search.py --q 11 13 16 17 19 --samples 20000
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from inversive_fast import build_circles  # noqa: E402
from arc_lift_verify import Lift  # noqa: E402


def build(q: int):
    lift = Lift(q)
    F, sub = build_field(q)
    points, blocks = build_circles(q, check_orbit_size=True)
    coord_index = {}
    for i, z in enumerate(points):
        if z is None:
            continue
        v = lift.coords(z)
        coord_index[(v[1], v[2])] = i
    sub_list = list(sub)
    table = [[coord_index[(a, b)] for b in sub_list] for a in sub_list]
    return sub_list, table, blocks


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--samples", type=int, default=20000)
    ap.add_argument("--maxdeg", type=int, default=0,
                    help="0 = arbitrary functions, d>0 = degree-d polynomials over F_q")
    args = ap.parse_args()

    for q in args.q:
        sub_list, table, blocks = build(q)
        m = len(sub_list)
        cmasks = []
        for B in blocks:
            mask = 0
            for p in B:
                mask |= 1 << p
            cmasks.append(mask)
        rng = random.Random(4242 + q)
        found = 0
        first = None
        for _ in range(args.samples):
            f = [rng.randrange(m) for _ in range(m)]
            S = 0
            ok = True
            for i in range(m):
                p = table[i][f[i]]
                if (S >> p) & 1:
                    ok = False
                    break
                S |= 1 << p
            if not ok:
                continue
            bad = False
            for mask in cmasks:
                if bin(S & mask).count("1") >= 4:
                    bad = True
                    break
            if not bad:
                found += 1
                if first is None:
                    first = f
        print(f"q={q}: full graph arcs found in {found}/{args.samples} samples",
              flush=True)
        if first is not None:
            print(f"    example f = {first}", flush=True)


if __name__ == "__main__":
    main()
