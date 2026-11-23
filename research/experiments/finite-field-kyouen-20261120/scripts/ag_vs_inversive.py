"""Compare the AG(2,q) circle family with the finite circles of M(q).

K1058's AG(2,q) board and the inversive board M(q) are treated in the literature
as related (M(q) = AG(2,q) plus a point at infinity, lines becoming circles), so
a safe set of the AG board should be safe in M(q).  A verification of the AG(2,13)
13-safe-set showed it is NOT M(13)-safe, so the two families of blocks must
differ.  This script compares them as sets of point sets.

Run:  python ag_vs_inversive.py --q 13
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402
from inversive_fast import build_circles  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[7, 9, 13])
    args = ap.parse_args()

    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        n_ag = len(pts)
        ag_circles = {frozenset(b) for b in blocks if len(b) != q}
        ag_lines = {frozenset(b) for b in blocks if len(b) == q}

        points, circles = build_circles(q, check_orbit_size=True)
        finite = [i for i in range(len(points)) if points[i] is not None]
        assert len(finite) == n_ag, (len(finite), n_ag)
        # the inversive circles with q+1 finite points (no infinity) vs those
        # through infinity (which are the lines plus infinity)
        m_finite = set()
        m_inf = set()
        for c in circles:
            if len(finite) in c:            # index of infinity is the last point
                continue
            m_finite.add(frozenset(c))
        print(f"q={q}: AG: {len(ag_circles)} distinct circles, {len(ag_lines)} distinct lines")
        print(f"      M: {len(m_finite)} circles avoiding infinity, {len(circles)} circles total")
        print(f"      AG circles that are M circles: {len(ag_circles & m_finite)}")
        print(f"      M circles not among AG circles: {len(m_finite - ag_circles)}")
        print(f"      AG circles not among M circles: {len(ag_circles - m_finite)}")
        # do the AG lines match the M circles through infinity (minus infinity)?
        inftylines = set()
        inf = len(points) - 1
        for c in circles:
            if inf in c:
                inftylines.add(frozenset(set(c) - {inf}))
        print(f"      AG lines matching (M circle through infinity) minus infinity: "
              f"{len(ag_lines & inftylines)} of {len(ag_lines)}")


if __name__ == "__main__":
    main()
