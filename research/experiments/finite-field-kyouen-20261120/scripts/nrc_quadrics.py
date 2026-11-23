"""Which quadrics contain the normal rational curve?  (odd-q side of K <= q)

For odd q every (q+1)-arc of PG(3,q) is a normal rational curve (Segre 1955), and
"K(q) <= q" is equivalent to claiming that no (q+1)-arc lies on the elliptic
quadric Q^-(3,q).  This script enumerates every quadric through the standard
normal rational curve

    N = {(1,t,t^2,t^3) : t in F_q} u {(0,0,0,1)}

and classifies each non-degenerate member by its number of F_q-points:
hyperbolic quadrics have (q+1)^2 points, elliptic ones q^2+1, and the degenerate
members have other counts (their counts are also reported).  If no member is
elliptic then no (q+1)-arc lies on Q^-, hence K(q) <= q.

Run:  python nrc_quadrics.py --q 5 7 9 11 13
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_prime_power import FiniteField, factorize, find_irreducible  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    apps = ap.parse_args()

    for q in apps.q:
        p, e = factorize(q)[0]
        F = FiniteField(p, e, find_irreducible(p, e))
        elems = list(F.elements())
        one = F.pow(elems[0], 0)
        zero = F.sub(one, one)
        mul = F.mul
        add = F.add

        pairs = [(i, j) for i in range(4) for j in range(i, 4)]
        pts = []
        for t in elems:
            t2 = mul(t, t)
            t3 = mul(t2, t)
            pts.append((one, t, t2, t3))
        pts.append((zero, zero, zero, one))

        rows = [[mul(pt[i], pt[j]) for (i, j) in pairs] for pt in pts]

        # homogeneous solution space of  (coefficients) . (monomials of each point) = 0
        m = [r[:] for r in rows]
        ncols = len(pairs)
        r = 0
        pivots = []
        for c in range(ncols):
            piv = next((i for i in range(r, len(m)) if not F.is_zero(m[i][c])), None)
            if piv is None:
                continue
            m[r], m[piv] = m[piv], m[r]
            inv = F.div(one, m[r][c])
            m[r] = [mul(inv, x) for x in m[r]]
            for i in range(len(m)):
                if i != r and not F.is_zero(m[i][c]):
                    f = m[i][c]
                    m[i] = [F.sub(m[i][k], mul(f, m[r][k])) for k in range(ncols)]
            pivots.append(c)
            r += 1
            if r == len(m):
                break
        free = [c for c in range(ncols) if c not in pivots]
        basis = []
        for fv in free:
            vec = [zero] * ncols
            vec[fv] = one
            for i, c in enumerate(pivots):
                vec[c] = F.neg(m[i][fv])
            basis.append(vec)

        # enumerate all projective points of the solution space
        projectives = []
        for combo in itertools.product(elems, repeat=len(basis)):
            if all(F.is_zero(x) for x in combo):
                continue
            vec = [zero] * ncols
            for coef, bv in zip(combo, basis):
                for k in range(ncols):
                    vec[k] = add(vec[k], mul(coef, bv[k]))
            # normalise: first nonzero coefficient to one
            inv = None
            for x in vec:
                if not F.is_zero(x):
                    inv = F.div(one, x)
                    break
            vec = tuple(mul(inv, x) for x in vec)
            projectives.append(vec)
        projectives = sorted(set(projectives))
        print(f"q={q}: solution space dim {len(basis)} (projective dim {len(basis)-1}), "
              f"{len(projectives)} quadrics through the normal rational curve")

        # points of PG(3,q)
        pg = []
        for a, b, c, d in itertools.product(elems, repeat=4):
            if F.is_zero(a) and F.is_zero(b) and F.is_zero(c) and F.is_zero(d):
                continue
            pg.append((a, b, c, d))

        def val(vec, pt):
            acc = zero
            for coef, (i, j) in zip(vec, pairs):
                if not F.is_zero(coef):
                    acc = add(acc, mul(coef, mul(pt[i], pt[j])))
            return acc

        counts = {}
        elliptic = 0
        for vec in projectives:
            raw = sum(1 for pt in pg if F.is_zero(val(vec, pt)))
            cnt = raw // (q - 1)      # pg lists every projective point q-1 times
            counts[cnt] = counts.get(cnt, 0) + 1
            if cnt == q * q + 1:
                elliptic += 1
        print(f"  projective point-count histogram: {counts}")
        print(f"  (hyperbolic = (q+1)^2 = "
              f"{(q + 1) * (q + 1)}, elliptic = q^2+1 = {q * q + 1})")
        print(f"  {'ELLIPTIC MEMBERS EXIST: ' + str(elliptic) if elliptic else 'no elliptic member'}",
              flush=True)


if __name__ == "__main__":
    main()
