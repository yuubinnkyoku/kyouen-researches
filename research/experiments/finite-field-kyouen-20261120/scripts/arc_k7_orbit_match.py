"""k=7: the orbit correspondence, now with a CORRECT bijection.

Using C = P^1(F_q) (the circle through 0, 1, infinity), the points of C ARE
P^1(F_q) with the correct Mobius structure.  So the involutions induced by
the pencils are genuine elements of PGL(2,q), and we can match them to the
37 orbits.

Run:  python arc_k7_orbit_match.py --q 5
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_field, build_inversive_plane  # noqa: E402
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

    perms = sorted({tuple(idx[repr(apply(m, z))] for z in pts) for m in mats})
    return F, pts, idx, perms, n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        Fp, p1pts, p1idx, perms, n = pgl_perms(q)
        ident = tuple(range(n))
        invols = [pm for pm in perms
                  if tuple(pm[pm[i]] for i in range(n)) == ident and pm != ident]
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

        # geometry with C = P^1(F_q)
        F, sub = build_field(q)
        points, circles = build_inversive_plane(q)
        idx = {p: i for i, p in enumerate(points)}
        blocks = [tuple(sorted(idx[p] for p in c)) for c in circles]
        nn = len(points)
        base = set(sub) | {None}
        ci = None
        for k, B in enumerate(blocks):
            if set(points[i] for i in B) == base:
                ci = k
                break
        B = blocks[ci]
        Bset = set(B)
        p1 = list(sub) + [None]
        p1_idx = {repr(x): i for i, x in enumerate(p1)}
        c_to_p1 = {idx[p]: p1_idx[repr(p)] for p in base}

        circ_through_pair = {}
        for k, BB in enumerate(blocks):
            for pair in itertools.combinations(BB, 2):
                circ_through_pair.setdefault(pair, []).append(k)
        outside = [p for p in range(nn) if p not in Bset]

        orbit_count = Counter()
        orbit_dist = {}
        unmatched = 0
        for xyz in itertools.combinations(outside, 3):
            W = None
            for k, BB in enumerate(blocks):
                if k == ci:
                    continue
                if all(p in BB for p in xyz):
                    W = k
                    break
            WcapC = Bset & set(blocks[W]) if W is not None else set()
            invs = []
            for xy in itertools.combinations(xyz, 2):
                pairs = set()
                for k in circ_through_pair.get(tuple(sorted(xy)), []):
                    if k == ci:
                        continue
                    cap = Bset & set(blocks[k])
                    if len(cap) == 2:
                        pairs.add(tuple(sorted(cap)))
                invs.append(frozenset(pairs))
            perms3 = []
            for inv in invs:
                pm = list(range(n))
                for a, bb in inv:
                    ia, ib = c_to_p1[a], c_to_p1[bb]
                    pm[ia] = ib
                    pm[ib] = ia
                perms3.append(tuple(pm))
            ids = [inv_index.get(p) for p in perms3]
            if all(i is not None for i in ids):
                key = tuple(sorted(ids))
                oid = orbit_of.get(key)
                if oid is not None:
                    orbit_count[oid] += 1
                else:
                    unmatched += 1
                    oid = None
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
               "realised_orbits": len(orbit_count),
               "orbit_distributions": {str(k): str(v) for k, v in
                                       sorted(orbit_dist.items())}}
        rows.append(row)
        print(f"q={q}: {len(orbits)} orbits", flush=True)
        print(f"  triples per orbit: {dict(sorted(orbit_count.items()))}",
              flush=True)
        print(f"  total {sum(orbit_count.values())}, unmatched {unmatched}",
              flush=True)
        print(f"  realised orbits: {len(orbit_count)}", flush=True)
        print(f"  distinct distributions among realised: "
              f"{len(set(orbit_dist.values()))}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
