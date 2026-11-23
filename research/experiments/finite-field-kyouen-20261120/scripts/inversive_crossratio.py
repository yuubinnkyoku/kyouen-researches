"""Verify the cross-ratio characterisation of concyclicity in the inversive plane.

Claim: four distinct points z1,z2,z3,z4 of P^1(F_{q^2}) lie on a common circle of
the inversive plane of order q  <=>  their cross-ratio lies in P^1(F_q).

Proof sketch: circles are exactly the PGL(2,F_{q^2})-images of the base circle
P^1(F_q), and a Moebius map with z1,z2,z3 |-> 0,1,infinity sends any circle
through z1,z2,z3 onto the unique circle through 0,1,infinity, namely P^1(F_q).
Hence z4 is on that circle iff the image of z4 -- the cross-ratio -- is in
P^1(F_q).  The point is that the coefficients of that Moebius map lie in
F_{q^2}, so no rationality is lost.

This script checks the claim exhaustively for small q against the circle
incidence structure, so that later arguments may use the reformulation:

    an arc is a set S in P^1(F_{q^2}) such that no four points of S have
    F_q-rational cross-ratio.

Run:  python inversive_crossratio.py --q 3 4 5 7
"""

from __future__ import annotations

import argparse
import itertools
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from inversive_fast import make_inverse_table  # noqa: E402


def cross_ratio(F, inv_tab, z1, z2, z3, z4):
    """Image of z4 under the unique Moebius map with z1->0, z2->1, z3->infinity.

    Implemented with homogeneous 2x2 determinants so that the point at
    infinity needs no separate treatment.
    """
    def det(a, b, c, d):
        return F.sub(F.mul(a, d), F.mul(b, c))

    one = F.pow(z1, 0) if z1 is not None else F.pow(z2, 0)
    zero = F.sub(one, one)

    def lift(z):
        return (z, one) if z is not None else (one, zero)

    a1, b1 = lift(z1)
    a2, b2 = lift(z2)
    a3, b3 = lift(z3)
    a4, b4 = lift(z4)
    # m_i = 2x2 matrix annihilating z_i and z_3 respectively:
    #   row = ( -z_i , 1 ) for the linear form  X - z_i Y  ... but we need the
    # composite map M = [[a,b],[c,d]] with M(z1)=0, M(z2)=1, M(z3)=infinity,
    # built from the two linear forms L1 = (z1, -1) (vanishing at z1) and
    # L3 = (-1, z3)??  Easier: use the standard formula
    #     (z, z1, z2, z3) = ((z - z1)(z2 - z3)) / ((z - z3)(z2 - z1))
    # in homogeneous determinant form:
    d1 = det(a4, b4, a1, b1)   # z - z1
    d3 = det(a4, b4, a3, b3)   # z - z3
    e2 = det(a2, b2, a3, b3)   # z2 - z3
    e1 = det(a2, b2, a1, b1)   # z2 - z1
    num = F.mul(d1, e2)
    den = F.mul(d3, e1)
    if F.is_zero(den):
        return None if not F.is_zero(num) else "undefined"
    return F.mul(num, inv_tab[den])


def is_in_base_field(F, sub, x) -> bool:
    if x is None:
        return True
    return x in set(sub)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7])
    args = ap.parse_args()

    for q in args.q:
        F, sub = build_field(q)
        inv_tab = make_inverse_table(F)
        from inversive_fast import build_circles
        points, blocks = build_circles(q, check_orbit_size=True)
        idx_of = {i: p for i, p in enumerate(points)}
        quad_circle = {}
        for ci, B in enumerate(blocks):
            for quad in itertools.combinations(B, 4):
                quad_circle[quad] = ci

        mism = []
        n_quad = 0
        n_conc = 0
        for quad in itertools.combinations(range(len(points)), 4):
            n_quad += 1
            concyclic = quad in quad_circle
            n_conc += concyclic
            z = [idx_of[i] for i in quad]
            cr = cross_ratio(F, inv_tab, z[0], z[1], z[2], z[3])
            rational = is_in_base_field(F, sub, cr)
            if concyclic != rational:
                mism.append((quad, concyclic, cr))
        print(f"q={q}: 4-subsets={n_quad} concyclic={n_conc} "
              f"mismatches={len(mism)}", flush=True)
        if mism:
            for m in mism[:5]:
                print("   MISMATCH", m, flush=True)
            raise SystemExit(f"cross-ratio characterisation FAILED at q={q}")


if __name__ == "__main__":
    main()
