"""k=7: the 9 realised orbits' triple counts in closed form.

MEASURED (q=5): the 9 realised orbits have triple counts

    240, 180, 240, 120, 60, 120, 120, 20, 40   (total 1140)

and each has a distinct (w,u)-distribution.  Let me pair them up:

    orbit 0  : 240  <- dist (0,1):1 (0,2):2 (0,3):11 (0,4):1
    orbit 20 : 240  <- dist (0,3):2 (0,4):3 (1,1):3 (1,2):6 (1,3):1
    orbit 16 : 180  <- dist (0,4):1 (1,2):8 (2,1):2 (2,2):4
    orbit 22 : 120  <- dist (0,5):1 (1,2):4 (1,3):4 (2,1):1 (2,2):5
    orbit 28 : 120  <- dist (0,2):5 (0,3):8 (0,4):2
    orbit 31 : 120  <- dist (0,2):1 (0,3):11 (0,4):2 (0,5):1
    orbit 27 :  60  <- dist (0,2):2 (0,3):8 (0,4):5
    orbit 36 :  40  <- dist (0,3):6 (0,4):9
    orbit 32 :  20  <- dist (0,2):9 (0,3):6

Now: the triple count for a realised orbit should be expressible via the
circle structure.  Recall the triple count decomposes by a = |W cap C|:

    a=0: 600,  a=1: 240,  a=2: 300

and the a-classes correspond to:
    a=0 -> Case A, 6 types
    a=1 -> Case A, 1 type
    a=2 -> Case B, 2 types

Let me verify the orbit triple counts against the a-decomposition.

Run:  python arc_k7_orbit_a.py --q 5
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

        orbit_a = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = None
            for k, BB in enumerate(blocks):
                if k == ci:
                    continue
                if all(p in BB for p in xyz):
                    W = k
                    break
            WcapC = Bset & set(blocks[W]) if W is not None else set()
            a = len(WcapC)
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
                for aa, bb in inv:
                    ia, ib = c_to_p1[aa], c_to_p1[bb]
                    pm[ia] = ib
                    pm[ib] = ia
                perms3.append(tuple(pm))
            ids = [inv_index.get(p) for p in perms3]
            if all(i is not None for i in ids):
                oid = orbit_of.get(tuple(sorted(ids)))
                if oid is not None:
                    orbit_a[(oid, a)] += 1

        row = {"q": q, "orbit_a": {f"{o},{a}": v for (o, a), v in
                                   sorted(orbit_a.items())}}
        rows.append(row)
        print(f"q={q}: (orbit, a) -> triples", flush=True)
        for (o, a), v in sorted(orbit_a.items()):
            print(f"    orbit {o}, a={a}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
