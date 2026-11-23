"""Test the classic Tits-ovoid shapes  f = x^A + x y + y^B  over F_8.

For q = 2^{2e+1} the Tits ovoid is usually written with a handful of exponents
involving sigma = 2^{e+1}; q=8 is the smallest case, and the earlier candidate
search (degree <= 3) missed it.  Here we test all pairs (A,B) with A,B <= 7 for
the shape O = {(1, x^A + x y + y^B, x, y)} u {P_inf}.

Run:  python tits_ovoid_exponents.py --q 8
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
    args = ap.parse_args()
    q = args.q
    p, m = factorize(q)[0]
    F = FiniteField(p, m, find_irreducible(p, m))
    elems = list(F.elements())
    one = F.pow(elems[0], 0)
    zero = F.sub(one, one)
    mul, add = F.mul, F.add

    def normalise(v):
        if all(F.is_zero(x) for x in v):
            return None
        inv = None
        for x in v:
            if not F.is_zero(x):
                inv = F.div(one, x)
                break
        return tuple(mul(inv, x) for x in v)

    pts = []
    seen = set()
    for v in itertools.product(elems, repeat=4):
        nv = normalise(v)
        if nv is None or nv in seen:
            continue
        seen.add(nv)
        pts.append(nv)

    lines = set()
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            lp = set()
            for lam in elems:
                nv = normalise(tuple(add(pts[i][k], mul(lam, pts[j][k])) for k in range(4)))
                if nv is not None:
                    lp.add(nv)
            lp.add(pts[j])
            if len(lp) == q + 1:
                lines.add(frozenset(lp))
    lines = list(lines)
    print(f"q={q}: {len(pts)} points, {len(lines)} distinct lines")

    def is_ovoid(point_set):
        if len(point_set) != q * q + 1:
            return False
        return all(len(ln & point_set) <= 2 for ln in lines)

    for A in range(0, 8):
        for B in range(0, 8):
            O = set()
            ok = True
            for x in elems:
                for y in elems:
                    f = add(add(F.pow(x, A), mul(x, y)), F.pow(y, B))
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
                if is_ovoid(O | {inf}):
                    print(f"OVOID: f = x^{A} + xy + y^{B}, extra point {inf}")
                    break


if __name__ == "__main__":
    main()
