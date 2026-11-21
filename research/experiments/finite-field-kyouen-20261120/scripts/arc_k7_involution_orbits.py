"""k=7: are the configurations PGL(2,q)-orbits on triples of involutions?

The 90 "canonical configurations" found earlier came from an ad-hoc
canonicalisation (relabel C's points by first appearance).  That is NOT a
group action, so 90 may be an artefact.

THE RIGHT QUESTION.  The three involutions iota(x,y), iota(x,z), iota(y,z)
are elements of PGL(2,q) of order 2 acting on C = P^1(F_q).  The (w,u)
distribution depends only on the TRIPLE OF INVOLUTIONS up to the action of
the group preserving C, i.e. PGL(2,q).

So the number of distinct distributions should equal the number of
PGL(2,q)-orbits on triples of involutions (of the relevant kind).

Let me compute those orbits directly.

An involution of P^1(F_q) is a fixed-point-free-or-not element of order 2
in PGL(2,q).  The involutions arising from pencils are the ones with
exactly 2 fixed points or 0 fixed points depending on q.

Let me enumerate all triples of involutions and compute PGL(2,q)-orbits.

Run:  python arc_k7_involution_orbits.py --q 5
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_prime_power import FiniteField, factorize  # noqa: E402


def pgl(q: int):
    """PGL(2,q) as a set of normalised matrices, plus its action on P^1."""
    fac = factorize(q)
    p, e = fac[0]
    F = FiniteField(p, e)
    pts = list(F.elements()) + [None]
    idx = {repr(x): i for i, x in enumerate(pts)}

    mats = set()
    for a in F.elements():
        for b in F.elements():
            for c in F.elements():
                for d in F.elements():
                    det = F.sub(F.mul(a, d), F.mul(b, c))
                    if F.is_zero(det):
                        continue
                    inv = F.inv(det)
                    mats.add(tuple(F.mul(x, inv) for x in (a, b, c, d)))

    def apply(m, z):
        a, b, c, d = m
        if z is None:
            return None if F.is_zero(c) else F.div(a, c)
        num = F.add(F.mul(a, z), b)
        den = F.add(F.mul(c, z), d)
        return None if F.is_zero(den) else F.div(num, den)

    def perm(m):
        return tuple(idx[repr(apply(m, z))] for z in pts)

    perms = {perm(m) for m in mats}
    return F, pts, idx, perms


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, pts, idx, perms = pgl(q)
        n = len(pts)

        # involutions: permutations of order 2
        invols = []
        for pm in perms:
            sq = tuple(pm[pm[i]] for i in range(n))
            if sq == tuple(range(n)) and pm != tuple(range(n)):
                invols.append(pm)
        invols = sorted(set(invols))

        print(f"q={q}: |PGL| = {len(perms)}, |P^1| = {n}, "
              f"involutions = {len(invols)}", flush=True)

        # orbits on triples of involutions (unordered, with repetition
        # allowed? the three pencils are distinct, so ordered distinct)
        triples = list(itertools.combinations(range(len(invols)), 3))
        seen = set()
        orbits = []
        for t in triples:
            if t in seen:
                continue
            orb = set()
            for pm in perms:
                # conjugate each involution by pm
                conj = []
                for i in t:
                    inv = invols[i]
                    # pm o inv o pm^{-1}
                    pinv = [0] * n
                    for j in range(n):
                        pinv[pm[j]] = j
                    c = tuple(pm[inv[pinv[j]]] for j in range(n))
                    conj.append(c)
                # map back to indices
                ids = tuple(sorted(invols.index(c) for c in conj))
                orb.add(ids)
            seen |= orb
            orbits.append(len(orb))

        row = {"q": q, "pgl_order": len(perms), "p1_size": n,
               "involutions": len(invols),
               "triples": len(triples),
               "num_orbits": len(orbits),
               "orbit_sizes": sorted(orbits, reverse=True)}
        rows.append(row)
        print(f"  triples of involutions: {len(triples)}", flush=True)
        print(f"  PGL-orbits: {len(orbits)}", flush=True)
        print(f"  orbit sizes: {sorted(orbits, reverse=True)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
