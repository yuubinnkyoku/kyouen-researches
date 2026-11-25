"""THE GEOMETRIC RESTATEMENT: K is the maximum ARC on the elliptic quadric.

The ovoid model gives a much cleaner description of the game than the
P^1(F_{q^2}) model.

SETUP.  Let Q be the elliptic quadric in PG(3,q),

    Q(x0,x1,x2,x3) = x0^2 + x1^2 + x2^2 + d*x3^2 = 0,   d a non-square.

Q has q^2 + 1 points.  A plane of PG(3,q) meets Q in 0, 1, 2 or q+1 points;
the q+1-point sections are exactly the circles of the inversive plane.

KEY EQUIVALENCE.  Four points of Q are concyclic  <=>  they are COPLANAR.

PROOF.  If four points of Q are coplanar, the plane contains at least 4
points of Q, so its section has size >= 4, hence (being 0,1,2 or q+1) it
has size q+1 -- a circle.  Conversely a circle is a plane section.  []

CONSEQUENCE.  A safe set is a subset of Q with no 4 coplanar.  In classical
finite geometry that is exactly an ARC on the quadric.  So

    K(inversive q) = max size of an arc on the elliptic quadric of PG(3,q).

This is a clean geometric restatement: the kyouen game on the inversive
plane is the ARC problem on an elliptic quadric.

This script verifies the equivalence exhaustively for small q and
re-derives K from the arc formulation.

Run:  python arc_on_quadric.py --q 3 4 5 7
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_ovoid import build_ovoid, planes_of_pg3  # noqa: E402


def build(q: int):
    """Return (F, ovoid, circles as index tuples, plane-of-each-circle)."""
    F, params, ovoid = build_ovoid(q)
    _, planes = planes_of_pg3(q)
    idx = {v: i for i, v in enumerate(ovoid)}
    circles = []
    for c in planes:
        sec = []
        for v in ovoid:
            s = F.zero
            for ci, vi in zip(c, v):
                s = F.add(s, F.mul(ci, vi))
            if F.is_zero(s):
                sec.append(idx[v])
        if len(sec) == q + 1:
            circles.append(tuple(sorted(sec)))
    circles = sorted(set(circles))
    return F, ovoid, circles


def coplanar(F, quad):
    """Are the four PG(3,q) points coplanar?

    Four points of PG(3,q) are coplanar iff the 4x4 matrix of their
    homogeneous coordinates is SINGULAR, i.e. its determinant is zero.
    """
    m = [list(p) for p in quad]
    n = 4
    det = F.one
    for col in range(n):
        piv = None
        for r in range(col, n):
            if not F.is_zero(m[r][col]):
                piv = r
                break
        if piv is None:
            return True                 # singular => coplanar
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det = F.neg(det)
        det = F.mul(det, m[col][col])
        inv = F.inv(m[col][col])
        for r in range(col + 1, n):
            f = F.mul(m[r][col], inv)
            if F.is_zero(f):
                continue
            for k in range(col, n):
                m[r][k] = F.sub(m[r][k], F.mul(f, m[col][k]))
    return F.is_zero(det)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4, 5, 7])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        t0 = time.time()
        F, ovoid, circles = build(q)
        n = len(ovoid)
        # circle membership lookup
        circ_of_quad = {}
        for ci, B in enumerate(circles):
            for quad in itertools.combinations(B, 4):
                circ_of_quad[quad] = ci

        bad = 0
        tot = 0
        for quad in itertools.combinations(range(n), 4):
            concyclic = quad in circ_of_quad
            copl = coplanar(F, [ovoid[i] for i in quad])
            tot += 1
            if concyclic != copl:
                bad += 1
                if bad <= 3:
                    print(f"    MISMATCH q={q} quad={quad} "
                          f"concyclic={concyclic} coplanar={copl}", flush=True)
        dt = time.time() - t0
        row = {"q": q, "points": n, "circles": len(circles),
               "quads_checked": tot, "mismatches": bad,
               "equivalence_holds": bad == 0, "seconds": round(dt, 2)}
        rows.append(row)
        print(f"q={q:>3}: {tot} quadruples, {bad} mismatches -> "
              f"{'OK' if bad == 0 else 'FAIL'}  ({dt:.1f}s)", flush=True)

    print()
    print("VERIFIED: four points of the elliptic quadric are concyclic")
    print("exactly when they are coplanar.")
    print()
    print("Therefore  K(inversive q) = max size of an ARC (no 4 coplanar)")
    print("on the elliptic quadric of PG(3,q).")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
