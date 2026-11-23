"""Look for algebraic structure in the maximum arcs found by arc_maxsearch.

The randomised search produces sets of size about 0.65q on the elliptic quadric.
Any *structured* family would give a proof of a lower bound instead of a
measurement, so it is worth asking what the witnesses look like:

  * affine shape     : z = a + b*u, does the set have distinct a or b?
  * algebraic curve  : do the points lie on a curve of low degree?
  * automorphisms    : is the set invariant (or almost invariant) under one of
                       the generators z -> z+1, z -> lambda z, z -> 1/z?
  * multiplicative   : are the ratios of the elements a coset / subgroup?
  * closure          : is the set maximal?  does it contain infinity?

Run:  python arc_structure_probe.py --q 13 17 23
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field  # noqa: E402
from arc_lift_verify import Lift  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "output"
FILES = ["arc_maxsearch.json", "arc_maxsearch_long.json", "arc_maxsearch_big.json",
         "arc_maxsearch_q49.json", "arc_maxsearch_q49b.json"]


def load_witness(q: int):
    best = None
    for name in FILES:
        p = OUT / name
        if not p.exists():
            continue
        for rec in json.loads(p.read_text(encoding="utf-8")):
            if rec.get("q") == q and "arc" in rec:
                if best is None or len(rec["arc"]) > len(best):
                    best = rec["arc"]
    return best


def fits_curve(F, pts, degree):
    """Is there a polynomial of total degree <= degree through all (a,b) points?"""
    monos = [(i, j) for i in range(degree + 1) for j in range(degree + 1 - i)]
    one = F.pow(pts[0][0], 0)
    zero = F.sub(one, one)
    rows = []
    for a, b in pts:
        row = []
        for i, j in monos:
            term = F.mul(F.pow(a, i), F.pow(b, j))
            row.append(term)
        rows.append(row)
    # Gaussian elimination on len(pts) x len(monos); consistent iff rank(rows) == rank(rows|0)
    m = [r[:] for r in rows]
    ncol = len(monos)
    rk = 0
    for col in range(ncol):
        piv = next((r for r in range(rk, len(m)) if not F.is_zero(m[r][col])), None)
        if piv is None:
            continue
        m[rk], m[piv] = m[piv], m[rk]
        inv = F.div(one, m[rk][col])
        m[rk] = [F.mul(inv, x) for x in m[rk]]
        for r in range(len(m)):
            if r != rk and not F.is_zero(m[r][col]):
                f = m[r][col]
                m[r] = [F.sub(m[r][c], F.mul(f, m[rk][c])) for c in range(ncol)]
        rk += 1
        if rk == len(m):
            break
    # a nonzero solution exists iff rank < number of monomials
    return rk < ncol, rk, ncol


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", required=True)
    args = ap.parse_args()

    for q in args.q:
        arc = load_witness(q)
        if arc is None:
            print(f"q={q}: no witness found", flush=True)
            continue
        lift = Lift(q)
        F = lift.F
        points = list(F.elements()) + [None]
        has_inf = any(points[i] is None for i in arc)
        affine = [p for p in (points[i] for i in arc) if p is not None]
        coords = []
        for z in affine:
            v = lift.coords(z)
            coords.append((v[1], v[2]))       # (a, b)
        distinct_a = len({a for a, b in coords})
        distinct_b = len({b for a, b in coords})
        print(f"q={q}: k={len(arc)} infinity={has_inf} affine={len(affine)} "
              f"distinct_a={distinct_a} distinct_b={distinct_b}", flush=True)

        # curve fits
        for deg in (1, 2, 3):
            ok, rk, ncol = fits_curve(F, coords, deg)
            print(f"   degree<={deg} curve through all affine points: {ok} "
                  f"(rank {rk}/{ncol})", flush=True)

        # automorphism invariance
        elems = list(F.elements())
        sub = set(lift.sub)
        lam = next((x for x in elems if x not in sub and not F.is_zero(x)), None)
        S = {p for p in (points[i] for i in arc)}
        for name, fn in [
            ("z->z+1", lambda z: None if z is None else F.add(z, lift.one)),
            ("z->lam*z", lambda z: None if z is None else F.mul(lam, z)),
            ("z->1/z", lambda z: None if z is None else
             (None if F.is_zero(z) else F.mul(lift.one, F.div(lift.one, z)))),
        ]:
            try:
                img = {fn(z) for z in S}
                same = len(img & S)
                print(f"   {name}: image size {len(img)}, points kept {same}/{len(S)}",
                      flush=True)
            except ZeroDivisionError:
                print(f"   {name}: degenerate", flush=True)

        # multiplicative structure: do the ratios form a subgroup?
        one = lift.one
        if affine and all(not F.is_zero(z) for z in affine):
            base = affine[0]
            inv_base = F.div(one, base)
            ratios = {F.mul(z, inv_base) for z in affine}
            closed = all(F.mul(x, y) in ratios for x in ratios for y in ratios)
            print(f"   ratios z/z0 ({len(ratios)} elements) closed under multiplication: {closed}",
                  flush=True)
            # additive structure: differences closed?
            diffs = {F.sub(z, base) for z in affine}
            print(f"   differences z-z0: {len(diffs)} distinct of {len(affine)}", flush=True)
        else:
            print("   multiplicative probe skipped (0 in the set)", flush=True)


if __name__ == "__main__":
    main()
