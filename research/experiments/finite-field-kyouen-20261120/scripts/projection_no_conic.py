"""The projection of the q=9 extremal arc is an 8-arc not lying on a conic.

K1252 improves the arc upper bound to q by feeding Segre's theorem "every q-arc
of PG(2,q) is contained in a conic" into a cone/Bezout argument, and records that
the same route cannot continue to q-1 because that would need every (q-1)-arc to
lie on a conic.  This script makes that limitation concrete: it projects the
known extremal 9-arc of M(9) (unique up to PGammaL(2,81)) from one of its points
onto a plane and checks that the resulting 8-arc of PG(2,9) is not contained in
any conic.

Run:  python projection_no_conic.py --q 9 --arc 6,18,45,20,17,61,77,0,22
"""

from __future__ import annotations

import argparse
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from inversive_fast import build_circles  # noqa: E402
from arc_lift_verify import Lift  # noqa: E402


def projective_basis(F, vecs):
    """Greedy basis of the span of the given vectors."""
    basis = []
    for v in vecs:
        m = [list(b) for b in basis] + [list(v)]
        # rank check
        r = 0
        mm = [row[:] for row in m]
        ncols = len(v)
        for c in range(ncols):
            piv = next((i for i in range(r, len(mm)) if not F.is_zero(mm[i][c])), None)
            if piv is None:
                continue
            mm[r], mm[piv] = mm[piv], mm[r]
            inv = F.div(F.pow(v[0], 0), mm[r][c])
            mm[r] = [F.mul(inv, x) for x in mm[r]]
            for i in range(len(mm)):
                if i != r and not F.is_zero(mm[i][c]):
                    f = mm[i][c]
                    mm[i] = [F.sub(mm[i][k], F.mul(f, mm[r][k])) for k in range(ncols)]
            r += 1
        if r == len(basis) + 1:
            basis.append(v)
    return basis


def coordinates_in(F, vec, basis):
    """Solve vec = sum c_i basis_i (basis vectors are a basis of the span)."""
    k = len(basis)
    ncols = len(vec)
    m = [[basis[j][i] for j in range(k)] + [vec[i]] for i in range(ncols)]
    # solve least squares by Gaussian elimination on the augmented matrix
    r = 0
    pivots = []
    for c in range(k):
        piv = next((i for i in range(r, ncols) if not F.is_zero(m[i][c])), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = F.div(F.pow(vec[0], 0), m[r][c])
        m[r] = [F.mul(inv, x) for x in m[r]]
        for i in range(ncols):
            if i != r and not F.is_zero(m[i][c]):
                f = m[i][c]
                m[i] = [F.sub(m[i][k], F.mul(f, m[r][k])) for k in range(k + 1)]
        pivots.append(c)
        r += 1
    sol = [None] * k
    for i, c in enumerate(pivots):
        sol[c] = m[i][k]
    return sol


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--arc", type=str, required=True)
    args = ap.parse_args()
    q = args.q
    arc = [int(x) for x in args.arc.split(",")]

    lift = Lift(q)
    F = lift.F
    one = lift.one
    zero = lift.zero
    points, blocks = build_circles(q, check_orbit_size=True)
    vecs = {i: lift.coords(points[i]) for i in arc}

    P = arc[0]
    pv = vecs[P]
    # choose a functional y with y.pv != 0
    yi = next(c for c in range(4) if not F.is_zero(pv[c]))

    def dot(u, v):
        acc = zero
        for a, b in zip(u, v):
            acc = F.add(acc, F.mul(a, b))
        return acc

    y = tuple(one if c == yi else zero for c in range(4))
    proj = {}
    for i in arc[1:]:
        a = vecs[i]
        s = dot(y, pv)
        t = dot(y, a)
        proj[i] = tuple(F.sub(F.mul(s, a[c]), F.mul(t, pv[c])) for c in range(4))
    # the projections span a 3-space (the plane pi = ker y)
    basis = projective_basis(F, list(proj.values()))
    print(f"q={q}: projected points span dimension {len(basis)} (expect 3)")
    coords = []
    for i in arc[1:]:
        sol = coordinates_in(F, proj[i], basis)
        if sol is None or any(c is None for c in sol):
            print("  coordinate extraction failed")
            return
        coords.append(tuple(sol))
    n = len(coords)
    print(f"  {n} projected points in PG(2,{q})")

    def det3(a, b, c):
        t1 = F.mul(a[0], F.sub(F.mul(b[1], c[2]), F.mul(b[2], c[1])))
        t2 = F.mul(a[1], F.sub(F.mul(b[0], c[2]), F.mul(b[2], c[0])))
        t3 = F.mul(a[2], F.sub(F.mul(b[0], c[1]), F.mul(b[1], c[0])))
        return F.add(F.sub(t1, t2), t3)

    collinear = 0
    for tri in combinations(range(n), 3):
        if F.is_zero(det3(coords[tri[0]], coords[tri[1]], coords[tri[2]])):
            collinear += 1
    print(f"  collinear triples: {collinear} (0 = it is an arc)")

    # conic coefficients (a,b,c,d,e,f) for aX^2+bY^2+cZ^2+dXY+eXZ+fYZ
    def quad_vec(p):
        x, yv, z = p
        return [F.mul(x, x), F.mul(yv, yv), F.mul(z, z), F.mul(x, yv), F.mul(x, z), F.mul(yv, z)]

    # the conic is determined by 5 points; check whether any conic carries all n
    # (solve the 5x6 system for the first five, then test the rest)
    rows = [quad_vec(p) for p in coords[:5]]
    m = [r[:] for r in rows]
    r = 0
    pivots = []
    for c in range(6):
        piv = next((i for i in range(r, len(m)) if not F.is_zero(m[i][c])), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = F.div(one, m[r][c])
        m[r] = [F.mul(inv, x) for x in m[r]]
        for i in range(len(m)):
            if i != r and not F.is_zero(m[i][c]):
                f = m[i][c]
                m[i] = [F.sub(m[i][k], F.mul(f, m[r][k])) for k in range(6)]
        pivots.append(c)
        r += 1
    free = [c for c in range(6) if c not in pivots]
    print(f"  conic pencil through the first five points has dimension {len(free)}")
    carried = False
    for fv in free:
        vec = [zero] * 6
        vec[fv] = one
        for i, c in enumerate(pivots):
            vec[c] = F.neg(m[i][fv])
        ok = all(F.is_zero(sum((F.mul(vec[t], term) for t, term in enumerate(quad_vec(p))), zero))
                 for p in coords)
        if ok:
            carried = True
            break
    print(f"  an 8-arc lying on a conic: {carried}  "
          f"({'contradicts the expectation' if carried else 'as expected: not contained in a conic'})")


if __name__ == "__main__":
    main()
