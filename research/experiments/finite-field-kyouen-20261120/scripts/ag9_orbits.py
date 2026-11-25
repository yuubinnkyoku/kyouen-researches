"""Orbit structure of AGL(2,9) acting on pairs of points, for symmetry breaking.

AGL(2,q) = translations + GL(2,q).  It acts transitively on points, and the
stabiliser of a point is GL(2,q) acting on the other q^2-1 points.

For symmetry breaking in a search for a safe set of size k, we can:
  1. fix the first point to index 0 (transitivity),
  2. fix the second point to a representative of each orbit of GL(2,q) on the
     remaining points.

The GL(2,q)-orbits on nonzero vectors are classified by the "ratio" of the
quadratic form: for q odd, GL(2,q) has two orbits on nonzero vectors, namely
the squares and the non-squares of the norm Q(v) = v_x^2 + v_y^2 (up to scalar).
Actually GL(2,q) preserves Q only up to scalar, so the invariant is the class of
Q(v) in F_q^*/(F_q^*)^2, i.e. whether Q(v) is a square or not.

So there are at most 2 orbits.  This is a big saving: instead of trying all 80
second points, we try 2.

This script computes the actual orbits by brute force (applying GL(2,q)) for
q=9, and verifies the count.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import defaultdict
from pathlib import Path

from inversive_prime_power import FiniteField, find_irreducible


def build_f9():
    return FiniteField(3, 2, find_irreducible(3, 2))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=9)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    q = args.q
    if q != 9:
        raise SystemExit("this script is specialised to q=9")
    F = build_f9()
    els = F.elements()
    # points of AG(2,9)
    pts = [(x, y) for x in els for y in els]
    idx = {p: i for i, p in enumerate(pts)}

    # GL(2,9): 2x2 invertible matrices over F_9
    def det2(a, b, c, d):
        return F.sub(F.mul(a, d), F.mul(b, c))

    mats = []
    for a in els:
        for b in els:
            for c in els:
                for d in els:
                    if not F.is_zero(det2(a, b, c, d)):
                        mats.append((a, b, c, d))
    print(f"|GL(2,9)| = {len(mats)}", flush=True)

    def apply(m, v):
        a, b, c, d = m
        x, y = v
        return (F.add(F.mul(a, x), F.mul(b, y)),
                F.add(F.mul(c, x), F.mul(d, y)))

    # orbits on nonzero vectors
    seen = set()
    orbits = []
    for v in pts:
        if v == (F.zero, F.zero) or v in seen:
            continue
        orb = set()
        for m in mats:
            orb.add(apply(m, v))
        seen |= orb
        orbits.append(sorted(orb))

    print(f"GL(2,9) orbits on nonzero vectors: {len(orbits)}", flush=True)
    for i, orb in enumerate(orbits):
        print(f"  orbit {i}: size {len(orb)}, representative {orb[0]}", flush=True)

    # classify by whether Q(v) is a square
    def Q(v):
        return F.add(F.mul(v[0], v[0]), F.mul(v[1], v[1]))

    for i, orb in enumerate(orbits):
        sq = {F.is_square(Q(v)) for v in orb}
        print(f"  orbit {i}: Q values square? {sq}", flush=True)

    out = {
        "q": q,
        "gl_order": len(mats),
        "num_orbits": len(orbits),
        "orbits": [{"size": len(o), "rep": list(o[0])} for o in orbits],
    }
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
