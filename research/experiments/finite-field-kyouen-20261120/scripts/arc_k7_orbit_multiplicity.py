"""k=7: the 37 PGL-orbits and their multiplicities.

The correct invariant is the PGL(2,q)-orbit on triples of involutions.
At q=5 there are 37 orbits.  Now compute, for each orbit:
  - its size
  - how many triples {x,y,z} of the actual geometry fall in it
  - its (w,u)-distribution

Then the k=7 arc count follows.

Run:  python arc_k7_orbit_multiplicity.py --q 5
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arc_on_quadric import build  # noqa: E402
from inversive_prime_power import FiniteField, factorize  # noqa: E402


def pgl_perms(q: int):
    fac = factorize(q)
    p, e = fac[0]
    F = FiniteField(p, e)
    pts = list(F.elements()) + [None]
    idx = {repr(x): i for i, x in enumerate(pts)}
    n = len(pts)

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

    perms = set()
    for m in mats:
        perms.add(tuple(idx[repr(apply(m, z))] for z in pts))
    return F, pts, idx, sorted(perms), n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, pts, idx, perms, n = pgl_perms(q)
        ident = tuple(range(n))
        invols = []
        for pm in perms:
            sq = tuple(pm[pm[i]] for i in range(n))
            if sq == ident and pm != ident:
                invols.append(pm)
        invols = sorted(set(invols))
        inv_index = {inv: i for i, inv in enumerate(invols)}

        # orbits on triples of involutions
        triples = list(itertools.combinations(range(len(invols)), 3))
        seen = set()
        orbit_of = {}
        orbits = []
        for t in triples:
            if t in seen:
                continue
            orb = set()
            for pm in perms:
                pinv = [0] * n
                for j in range(n):
                    pinv[pm[j]] = j
                conj = []
                for i in t:
                    inv = invols[i]
                    c = tuple(pm[inv[pinv[j]]] for j in range(n))
                    conj.append(inv_index[c])
                orb.add(tuple(sorted(conj)))
            seen |= orb
            oid = len(orbits)
            for o in orb:
                orbit_of[o] = oid
            orbits.append(sorted(orb))

        # now the geometry: for each triple {x,y,z} outside C, compute the
        # three involutions and find the orbit
        Fq, ovoid, circles = build(q)
        nn = len(ovoid)
        b = len(circles)
        s = q + 1
        circ_through_pair = {}
        for ci, B in enumerate(circles):
            for pair in itertools.combinations(B, 2):
                circ_through_pair.setdefault(pair, []).append(ci)

        ci = 0
        B = circles[ci]
        Bset = set(B)
        outside = [p for p in range(nn) if p not in Bset]

        # map C's points to P^1 indices.  The ovoid model's C is a set of s
        # points; we need a bijection to P^1(F_q).  Any bijection works as
        # long as it is consistent, because the orbit is computed from the
        # induced permutations.  Use the sorted order.
        cpts = sorted(B)
        c_to_p1 = {p: i for i, p in enumerate(cpts)}

        # The induced permutations must be involutions of P^1.  Verify and
        # fall back to a direct orbit computation if the labelling does not
        # produce valid involutions.
        def to_perm(inv):
            pm = list(range(n))
            for a, bb in inv:
                ia, ib = c_to_p1[a], c_to_p1[bb]
                pm[ia] = ib
                pm[ib] = ia
            return tuple(pm)

        orbit_count = Counter()
        orbit_dist = {}
        unmatched = 0
        for xyz in itertools.combinations(outside, 3):
            W = None
            for cj, BB in enumerate(circles):
                if cj == ci:
                    continue
                if all(p in BB for p in xyz):
                    W = cj
                    break
            WcapC = Bset & set(circles[W]) if W is not None else set()
            invs = []
            for xy in itertools.combinations(xyz, 2):
                pairs = set()
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    cap = Bset & set(circles[cj])
                    if len(cap) == 2:
                        pairs.add(tuple(sorted(cap)))
                invs.append(frozenset(pairs))
            perms3 = [to_perm(inv) for inv in invs]
            ids = []
            ok = True
            for p in perms3:
                if p in inv_index:
                    ids.append(inv_index[p])
                else:
                    ok = False
                    break
            if ok:
                key = tuple(sorted(ids))
                oid = orbit_of.get(key)
                orbit_count[oid] += 1
            else:
                unmatched += 1
                oid = None

            dist = Counter()
            for T in itertools.combinations(B, 4):
                Tset = set(T)
                w = len(Tset & WcapC)
                u = set()
                for inv in invs:
                    for pr in inv:
                        if pr[0] in Tset and pr[1] in Tset:
                            u.add(pr)
                dist[(w, len(u))] += 1
            if oid is not None:
                orbit_dist.setdefault(oid, tuple(sorted(dist.items())))

        row = {"q": q, "num_orbits": len(orbits),
               "orbit_sizes": [len(o) for o in orbits],
               "triples_per_orbit": {str(k): v for k, v in
                                     sorted(orbit_count.items())},
               "unmatched": unmatched,
               "orbit_distributions": {str(k): str(v) for k, v in
                                       sorted(orbit_dist.items())}}
        rows.append(row)
        print(f"q={q}: {len(orbits)} orbits", flush=True)
        print(f"  orbit sizes: {[len(o) for o in orbits]}", flush=True)
        print(f"  triples per orbit: {dict(sorted(orbit_count.items()))}",
              flush=True)
        print(f"  total triples: {sum(orbit_count.values())}, "
              f"unmatched {unmatched}", flush=True)
        print(f"  orbits actually realised: {len(orbit_count)}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
