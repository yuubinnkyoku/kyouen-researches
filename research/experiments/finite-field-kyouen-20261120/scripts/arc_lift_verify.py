"""Lift the inversive plane to the elliptic quadric and read the game as an MDS code.

The model
---------
Let F = F_{q^2} = F_q + F_q*u.  Every point of the inversive plane is an element
z of F or the point at infinity.  Write z = a + b*u with a, b in F_q and let

    N(z) = z * z^q = a^2 + alpha*a*b + beta*b^2,   alpha = u + u^q, beta = u^(q+1)

(alpha, beta in F_q).  Then

    lift(z) = (1 : a : b : N(z))  in PG(3,q),      lift(infinity) = (0:0:0:1)

lies on the quadric  X0*X3 = X1^2 + alpha*X1*X2 + beta*X2^2, and the circle
through three points is exactly the plane spanned by their lifts.  Hence

    four points are concyclic  <=>  their four lifts are linearly dependent.

Consequently an arc of size k is a 4 x k matrix over F_q, all of whose columns
lie on Q^-(3,q) and every four of which are independent.  For such a matrix the
generated code C has min distance k-3, because a nonzero codeword has weight
k - |{i : y.p_i = 0}| and a plane meets the quadric in a conic, so it can contain
at most three columns.  Singleton forces equality, so

    arcs of size k  <->  MDS codes [k, 4, k-3] over F_q whose columns can all be
                         placed on the elliptic quadric (equivalently: MDS codes
                         [k, k-4, 5] with a quadric-point parity check matrix).

This file checks the model exhaustively for small q and re-verifies every arc
witness found by arc_maxsearch by linear algebra alone -- no circle list is
used, so this is an independent check of the witnesses.

Run:  python arc_lift_verify.py --check-model 3 4 5 7
      python arc_lift_verify.py --check-witnesses
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "output"


class Lift:
    def __init__(self, q: int):
        self.q = q
        self.F, self.sub = build_field(q)
        F = self.F
        self.one = F.pow(self.sub[0], 0)
        self.zero = F.sub(self.one, self.one)
        sub = set(self.sub)
        u = next(x for x in F.elements() if x not in sub)
        uq = F.pow(u, q)
        self.u = u
        self.alpha = F.add(u, uq)                       # u + u^q  in F_q
        self.beta = F.pow(u, q + 1)                     # u^(q+1)  in F_q
        self.dinv = F.div(self.one, F.sub(u, uq))       # 1/(u - u^q)

    def coords(self, z):
        F, one, zero = self.F, self.one, self.zero
        if z is None:
            return (zero, zero, zero, one)
        zq = F.pow(z, self.q)
        b = F.mul(F.sub(z, zq), self.dinv)
        a = F.sub(z, F.mul(b, self.u))
        n = F.pow(z, self.q + 1)
        return (one, a, b, n)

    def quadric_residual(self, v):
        """X0*X3 - (X1^2 + alpha*X1*X2 + beta*X2^2); zero iff on the quadric."""
        F = self.F
        x0, x1, x2, x3 = v
        lhs = F.mul(x0, x3)
        rhs = F.add(F.mul(x1, x1), F.add(F.mul(F.mul(self.alpha, x1), x2),
                                        F.mul(self.beta, F.mul(x2, x2))))
        return F.sub(lhs, rhs)

    def det4(self, rows) -> bool:
        """True iff the four vectors are linearly independent."""
        F = self.F
        m = [list(r) for r in rows]
        for col in range(4):
            piv = next((r for r in range(col, 4) if not F.is_zero(m[r][col])), None)
            if piv is None:
                return False
            m[col], m[piv] = m[piv], m[col]
            inv = F.div(self.one, m[col][col])
            m[col] = [F.mul(inv, x) for x in m[col]]
            for r in range(col + 1, 4):
                f = m[r][col]
                if not F.is_zero(f):
                    m[r] = [F.sub(m[r][c], F.mul(f, m[col][c])) for c in range(4)]
        return True


def point_list(q: int):
    """Same point order as inversive_fast.build_circles: F elements, then infinity."""
    F, _ = build_field(q)
    return list(F.elements()) + [None]


def check_model(q: int) -> dict:
    """Exhaustively compare 'lift is dependent' with 'concyclic' for all 4-sets."""
    from inversive_fast import build_circles

    lift = Lift(q)
    points, blocks = build_circles(q, check_orbit_size=True)
    vecs = [lift.coords(z) for z in points]

    bad_quadric = [i for i, v in enumerate(vecs) if not lift.F.is_zero(lift.quadric_residual(v))]
    quad4 = {}
    for B in blocks:
        for quad in itertools.combinations(B, 4):
            quad4[quad] = True

    mism = 0
    n_conc = 0
    n_dep = 0
    for quad in itertools.combinations(range(len(points)), 4):
        indep = lift.det4([vecs[i] for i in quad])
        conc = quad in quad4
        n_conc += conc
        n_dep += not indep
        if conc == indep:      # concyclic must mean dependent
            mism += 1
            if mism <= 3:
                print(f"   MISMATCH q={q} quad={quad} concyclic={conc} independent={indep}")
    return {"q": q, "points": len(points), "concyclic_4sets": n_conc,
            "dependent_4sets": n_dep, "mismatches": mism,
            "off_quadric": len(bad_quadric),
            "ok": mism == 0 and not bad_quadric and n_conc == n_dep}


def verify_witness(q: int, arc: list, lift: Lift) -> dict:
    points = point_list(q)
    vecs = [lift.coords(points[i]) for i in arc]
    off = sum(1 for v in vecs if not lift.F.is_zero(lift.quadric_residual(v)))
    bad = 0
    for quad in itertools.combinations(range(len(arc)), 4):
        if not lift.det4([vecs[i] for i in quad]):
            bad += 1
    k = len(arc)
    return {"q": q, "k": k, "off_quadric": off, "dependent_4sets": bad,
            "mds_ok": bad == 0 and off == 0,
            "mds_params": f"[{k},4,{k - 3}]", "dual": f"[{k},{k - 4},5]",
            "q_plus_1": q + 1, "k_over_q": round(k / q, 4)}


def rank(F, rows) -> int:
    m = [list(r) for r in rows]
    n_col = len(m[0]) if m else 0
    rk = 0
    for col in range(n_col):
        piv = next((r for r in range(rk, len(m)) if not F.is_zero(m[r][col])), None)
        if piv is None:
            continue
        m[rk], m[piv] = m[piv], m[rk]
        inv = F.div(F.pow(m[rk][col], 0), m[rk][col])
        m[rk] = [F.mul(inv, x) for x in m[rk]]
        for r in range(len(m)):
            if r != rk and not F.is_zero(m[r][col]):
                f = m[r][col]
                m[r] = [F.sub(m[r][c], F.mul(f, m[rk][c])) for c in range(n_col)]
        rk += 1
    return rk


def projection_arc_check(q: int, arc: list, lift: Lift) -> dict:
    """For each P of the arc, project the others from P onto a plane.

    Claim (K1250, projection corollary): the projections form an arc of PG(2,q),
    i.e. no three are collinear.  This is what bounds K by (max arc of PG(2,q))+1.
    """
    F = lift.F
    points = point_list(q)
    vecs = [lift.coords(points[i]) for i in arc]
    k = len(vecs)
    worst = k
    failures = 0
    for i in range(k):
        p = vecs[i]
        # pick a coordinate functional y with y.p != 0, then pi = ker(y)
        yi = next(c for c in range(4) if not F.is_zero(p[c]))
        proj = []
        for j in range(k):
            if j == i:
                continue
            a = vecs[j]
            s = p[yi]                       # y.p
            t = a[yi]                       # y.a
            # (y.p)*a - (y.a)*p  lies in ker(y) and on the span of p, a
            proj.append(tuple(F.sub(F.mul(s, a[c]), F.mul(t, p[c])) for c in range(4)))
        bad = 0
        for tri in itertools.combinations(range(len(proj)), 3):
            if rank(F, [proj[x] for x in tri]) < 3:
                bad += 1
        if bad:
            failures += 1
            worst = min(worst, k - 1)
    return {"q": q, "k": k, "projection_arc": failures == 0,
            "bad_projections": failures, "projected_size": k - 1}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-model", type=int, nargs="*", default=[])
    ap.add_argument("--check-witnesses", action="store_true")
    ap.add_argument("--check-projection", action="store_true",
                    help="verify that projecting from any arc point gives an arc of PG(2,q)")
    ap.add_argument("--files", nargs="*", default=[
        "arc_maxsearch.json", "arc_maxsearch_long.json", "arc_maxsearch_big.json",
        "arc_maxsearch_q49.json", "arc_maxsearch_q49b.json"])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    ok_all = True
    for q in args.check_model:
        r = check_model(q)
        rows.append({"model": r})
        ok_all &= r["ok"]
        print(f"q={q}: points={r['points']} concyclic={r['concyclic_4sets']} "
              f"dependent={r['dependent_4sets']} mismatches={r['mismatches']} "
              f"off_quadric={r['off_quadric']} -> {'OK' if r['ok'] else 'FAIL'}", flush=True)

    if args.check_witnesses:
        seen = {}
        for name in args.files:
            path = OUT / name
            if not path.exists():
                print(f"skip missing {name}", flush=True)
                continue
            for rec in json.loads(path.read_text(encoding="utf-8")):
                if "arc" not in rec:
                    continue
                q = rec["q"]
                # keep the largest witness per q
                if q in seen and seen[q][0]["k"] >= len(rec["arc"]):
                    continue
                lift = Lift(q)
                seen[q] = (verify_witness(q, rec["arc"], lift), rec["arc"])
        for q in sorted(seen):
            r, arc = seen[q]
            rows.append({"witness": r})
            ok_all &= r["mds_ok"]
            print(f"q={r['q']:>2}: k={r['k']:>2} MDS {r['mds_params']:>12} "
                  f"dual {r['dual']:>10} q+1={r['q_plus_1']:>2} k/q={r['k_over_q']:.3f} "
                  f"dep4={r['dependent_4sets']} off={r['off_quadric']} "
                  f"-> {'OK' if r['mds_ok'] else 'FAIL'}", flush=True)
            if args.check_projection:
                pj = projection_arc_check(q, arc, Lift(q))
                rows.append({"projection": pj})
                ok_all &= pj["projection_arc"]
                print(f"      projection from each of {pj['k']} points gives "
                      f"{pj['projected_size']} points with no 3 collinear: "
                      f"{'OK' if pj['projection_arc'] else 'FAIL'}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        print(f"wrote {args.out}")

    if not ok_all:
        raise SystemExit("lift/MDS verification FAILED")


if __name__ == "__main__":
    main()
