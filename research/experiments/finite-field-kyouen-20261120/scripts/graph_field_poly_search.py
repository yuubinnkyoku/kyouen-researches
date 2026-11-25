"""Enumerate polynomial graphs over F_q and test them as arcs.

Unlike graph_poly_search.py this uses the real field arithmetic: the graph of
f(a) = c_d a^d + ... + c_0 with coefficients in F_q, tested against the circle
list.  Any hit is a genuine construction with q points, i.e. K(q) >= q.

Run:  python graph_field_poly_search.py --q 5 7 9 11 13 --maxdeg 2
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from inversive_fast import build_circles  # noqa: E402
from arc_lift_verify import Lift  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--maxdeg", type=int, default=2)
    args = ap.parse_args()

    for q in args.q:
        lift = Lift(q)
        F, sub = build_field(q)
        points, blocks = build_circles(q, check_orbit_size=True)
        one = F.pow(sub[0], 0)
        zero = F.sub(one, one)
        coord_index = {}
        for i, z in enumerate(points):
            if z is None:
                continue
            v = lift.coords(z)
            coord_index[(v[1], v[2])] = i
        sub_list = list(sub)
        cmasks = []
        for B in blocks:
            mask = 0
            for p in B:
                mask |= 1 << p
            cmasks.append(mask)

        def graph_is_arc(coeffs) -> bool:
            S = 0
            for a in sub_list:
                b = zero
                for c in reversed(coeffs):
                    b = F.add(F.mul(b, a), c)
                key = (a, b)
                if key not in coord_index:
                    return False
                p = coord_index[key]
                if (S >> p) & 1:
                    return False
                S |= 1 << p
            for mask in cmasks:
                if bin(S & mask).count("1") >= 4:
                    return False
            return True

        hits = []
        m = len(sub_list)
        for deg in range(1, args.maxdeg + 1):
            for coeffs in itertools.product(sub_list, repeat=deg + 1):
                if graph_is_arc(coeffs):
                    hits.append((deg, coeffs))
                    if len(hits) <= 3:
                        print(f"  q={q} hit: degree {deg} coeffs {coeffs}", flush=True)
        print(f"q={q}: {len(hits)} polynomial graph arcs of degree <= {args.maxdeg} "
              f"(K(q) would be at least {q} if any)", flush=True)


if __name__ == "__main__":
    main()
