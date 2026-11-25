"""Find the lines on members of the char-2 pencil  s(X0X3+X1X2) + r0(X0X1+X2^2) + r1(X1^2+X2X3).

For q even a non-degenerate quadric of PG(3,q) is hyperbolic exactly when it
contains a line, so a proof that every member with s != 0 is hyperbolic can be
given by exhibiting lines.  This script enumerates the lines of PG(3,q) and
prints those contained in a given member, to reveal the pattern.

Run:  python cg_line_hunt.py --q 8
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
    ap.add_argument("--q", type=int, required=True)
    args = ap.parse_args()
    q = args.q
    p, m = factorize(q)[0]
    assert p == 2
    F = FiniteField(p, m, find_irreducible(p, m))
    elems = list(F.elements())
    one = F.pow(elems[0], 0)
    zero = F.sub(one, one)
    mul, add = F.mul, F.add

    # projective points
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

    def Q(vec, pt):
        s = vec[0]                                  # coefficient of X0X3+X1X2
        r0 = vec[1]                                 # coefficient of X0X1+X2^2
        r1 = vec[2]                                 # coefficient of X1^2+X2X3
        x0, x1, x2, x3 = pt
        acc = zero
        acc = add(acc, mul(s, add(mul(x0, x3), mul(x1, x2))))
        acc = add(acc, mul(r0, add(mul(x0, x1), mul(x2, x2))))
        acc = add(acc, mul(r1, add(mul(x1, x1), mul(x2, x3))))
        return acc

    # all lines: pairs of distinct points with all q+1 points on the line
    def normalise(v):
        if all(F.is_zero(x) for x in v):
            return None
        inv = None
        for x in v:
            if not F.is_zero(x):
                inv = F.div(one, x)
                break
        return tuple(mul(inv, x) for x in v)

    def line_points(a, b):
        out = []
        for lam in elems:
            out.append(normalise(tuple(add(a[i], mul(lam, b[i])) for i in range(4))))
        out.append(normalise(b))
        return out

    lines = set()
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            lp = line_points(pts[i], pts[j])
            if len(set(lp)) == q + 1:
                lines.add(tuple(sorted(index[v] for v in lp)))
    print(f"q={q}: {len(pts)} points, {len(lines)} lines")

    # test a few members
    for (s, r0, r1) in [(one, zero, zero), (one, one, zero), (one, zero, one), (one, one, one)]:
        vec = (s, r0, r1)
        on = [pt for pt in pts if F.is_zero(Q(vec, pt))]
        on_lines = [ln for ln in lines if all(F.is_zero(Q(vec, pts[i])) for i in ln)]
        print(f"  member s={s} r0={r0} r1={r1}: {len(on)} points, "
              f"{len(on_lines)} lines on it")
        for ln in on_lines[:4]:
            print("     line:", [pts[i] for i in ln])


if __name__ == "__main__":
    main()
