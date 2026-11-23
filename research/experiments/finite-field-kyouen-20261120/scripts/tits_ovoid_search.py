"""Search for the Tits ovoid of PG(3,8) among candidate coordinate forms.

The Tits ovoid exists only for q = 2^m with m odd (m = 2e+1 >= 3), so q = 8 is the
smallest case.  Following the standard shape O = {(1, f(x,y), x, y)} u {P_inf},
this script tests candidate polynomials f against the ovoid axioms
(q^2+1 = 65 points, at most 2 on any line), and reports the ones that work.

Run:  python tits_ovoid_search.py --q 8
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
    ap.add_argument("--q", type=int, default=8)
    ap.add_argument("--max-degree", type=int, default=3)
    args = ap.parse_args()
    q = args.q
    p, m = factorize(q)[0]
    assert p == 2 and m >= 3
    F = FiniteField(p, m, find_irreducible(p, m))
    elems = list(F.elements())
    one = F.pow(elems[0], 0)
    zero = F.sub(one, one)
    mul, add = F.mul, F.add

    # projective points of PG(3,q) as normalised tuples
    seen = set()
    pts = []
    for v in itertools.product(elems, repeat=4):
        if all(F.is_zero(x) for x in v):
            continue
        inv = None
        for x in v:
            if not F.is_zero(x):
                inv = F.div(one, x)
                break
        nv = tuple(mul(inv, x) for x in v)
        if nv in seen:
            continue
        seen.add(nv)
        pts.append(nv)
    index = {v: i for i, v in enumerate(pts)}

    # monomials x^a y^b with deg <= max_degree, excluding x^0 y^0
    monos = [(a, b) for a in range(args.max_degree + 1)
             for b in range(args.max_degree + 1) if 1 <= a + b <= args.max_degree]

    def monomial_value(a, b, x, y):
        return mul(F.pow(x, a), F.pow(y, b))

    lines = []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            lp = set()
            for lam in elems:
                lp.add(tuple(add(pts[i][k], mul(lam, pts[j][k])) for k in range(4)))
            lp.add(pts[j])
            norm = set()
            for v in lp:
                if all(F.is_zero(x) for x in v):
                    continue
                inv = None
                for x in v:
                    if not F.is_zero(x):
                        inv = F.div(one, x)
                        break
                norm.add(tuple(mul(inv, x) for x in v))
            if len(norm) == q + 1:
                lines.append(norm)
    print(f"q={q}: {len(pts)} points, {len(lines)} lines")

    def is_ovoid(point_set):
        if len(point_set) != q * q + 1:
            return False
        for ln in lines:
            if len(ln & point_set) > 2:
                return False
        return True

    # candidates: a single monomial plus xy, and the "twisted" forms
    candidates = []
    for (a, b) in monos:
        candidates.append({(a, b): one, (1, 1): one})
    # also pure polynomials of the form x^a y^b + x^c y^d
    for m1, m2 in itertools.combinations(monos, 2):
        candidates.append({m1: one, m2: one})

    found = []
    for coeffs in candidates:
        O = set()
        ok = True
        for x in elems:
            for y in elems:
                f = zero
                for (a, b), c in coeffs.items():
                    f = add(f, mul(c, monomial_value(a, b, x, y)))
                v = (one, f, x, y)
                if v in O:
                    ok = False
                    break
                O.add(v)
            if not ok:
                break
        if not ok:
            continue
        for inf in [(zero, zero, zero, one), (zero, zero, one, zero), (zero, one, zero, zero)]:
            cand = O | {inf}
            if is_ovoid(cand):
                found.append((dict(coeffs), inf))
                print("OVOID FOUND:", {k: v for k, v in coeffs.items()}, "plus", inf)
                break
    print(f"candidates tested: {len(candidates)}, ovoids found: {len(found)}")
    for coeffs, inf in found:
        print("   ", coeffs, "+", inf)


if __name__ == "__main__":
    main()
