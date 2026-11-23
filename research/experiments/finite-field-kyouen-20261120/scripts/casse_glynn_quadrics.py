"""Do Casse-Glynn (q+1)-arcs lie on the elliptic quadric?  (even-q side of K <= q)

For q = 2^m (m >= 3) every (q+1)-arc of PG(3,q) is projectively equivalent to a
Frobenius-twisted normal rational curve (Casse-Glynn 1982):

    A_e = {[1 : t : t^sigma : t^(sigma+1)] : t in F_q} u {[0:0:0:1]},
    sigma = 2^e, gcd(e, m) = 1, 1 <= e <= m-1.

"K(q) <= q" is the statement that no (q+1)-arc lies on the elliptic quadric
Q^-(3,q).  This script enumerates every quadric through A_e and classifies the
members by their number of F_q-points: in PG(3,q) a non-degenerate quadric is
hyperbolic with (q+1)^2 points or elliptic (an ovoid) with q^2+1 points, cones
give 1 + q(q+1) and pairs of planes give 2(q^2+q+1) - (q+1).

Run:  python casse_glynn_quadrics.py --q 8 16
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
    args = ap.parse_args()

    for q in args.q:
        p, m = factorize(q)[0]
        assert p == 2, "this script is for q = 2^m"
        F = FiniteField(p, m, find_irreducible(p, m))
        elems = list(F.elements())
        one = F.pow(elems[0], 0)
        zero = F.sub(one, one)
        mul, add = F.mul, F.add

        pairs = [(i, j) for i in range(4) for j in range(i, 4)]
        pg = [pt for pt in itertools.product(elems, repeat=4)
              if not all(F.is_zero(x) for x in pt)]
        n_proj = len(pg) // (q - 1)

        es = [e for e in range(1, m) if __import__("math").gcd(e, m) == 1]
        for e in es:
            sigma = 2 ** e
            pts = []
            for t in elems:
                pts.append((one, t, F.pow(t, sigma), F.pow(t, sigma + 1)))
            pts.append((zero, zero, zero, one))

            rows = [[mul(pt[i], pt[j]) for (i, j) in pairs] for pt in pts]
            mm = [r[:] for r in rows]
            ncols = len(pairs)
            r = 0
            pivots = []
            for c in range(ncols):
                piv = next((i for i in range(r, len(mm)) if not F.is_zero(mm[i][c])), None)
                if piv is None:
                    continue
                mm[r], mm[piv] = mm[piv], mm[r]
                inv = F.div(one, mm[r][c])
                mm[r] = [mul(inv, x) for x in mm[r]]
                for i in range(len(mm)):
                    if i != r and not F.is_zero(mm[i][c]):
                        f = mm[i][c]
                        mm[i] = [F.sub(mm[i][k], mul(f, mm[r][k])) for k in range(ncols)]
                pivots.append(c)
                r += 1
                if r == len(mm):
                    break
            free = [c for c in range(ncols) if c not in pivots]
            basis = []
            for fv in free:
                vec = [zero] * ncols
                vec[fv] = one
                for i, c in enumerate(pivots):
                    vec[c] = F.neg(mm[i][fv])
                basis.append(vec)

            projectives = set()
            for combo in itertools.product(elems, repeat=len(basis)):
                if all(F.is_zero(x) for x in combo):
                    continue
                vec = [zero] * ncols
                for coef, bv in zip(combo, basis):
                    for k in range(ncols):
                        vec[k] = add(vec[k], mul(coef, bv[k]))
                inv = None
                for x in vec:
                    if not F.is_zero(x):
                        inv = F.div(one, x)
                        break
                projectives.add(tuple(mul(inv, x) for x in vec))
            projectives = sorted(projectives)

            def val(vec, pt):
                acc = zero
                for coef, (i, j) in zip(vec, pairs):
                    if not F.is_zero(coef):
                        acc = add(acc, mul(coef, mul(pt[i], pt[j])))
                return acc

            hist = {}
            elliptic = 0
            for vec in projectives:
                raw = sum(1 for pt in pg if F.is_zero(val(vec, pt)))
                cnt = raw // (q - 1)
                hist[cnt] = hist.get(cnt, 0) + 1
                if cnt == q * q + 1:
                    elliptic += 1
            if not e:
                continue
            print(f"q={q} (m={m}), e={e}, sigma={sigma}: "
                  f"{len(pts)}-point arc, {len(projectives)} quadrics through it, "
                  f"point-count histogram {hist}", flush=True)
            print(f"   hyperbolic=(q+1)^2={(q+1)*(q+1)}, elliptic=q^2+1={q*q+1}, "
                  f"cone=1+q(q+1)={1+q*(q+1)}")
            print(f"   ELLIPTIC MEMBERS: {elliptic}", flush=True)


if __name__ == "__main__":
    main()
