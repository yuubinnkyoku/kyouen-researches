"""k=7: how the a=0 HIGH/LOW circle split maps to the 6 orbits.

MEASURED (q=5, a=0):
    20 circles (HIGH, u=7/9) and 10 circles (LOW, u=6/8)
    6 orbits with triple counts 240, 120, 120, 60, 40, 20

Each a=0 circle contributes C(s,3) = 20 triples (q=5).
So 20 circles x 20 = 400 triples from HIGH, 10 x 20 = 200 from LOW.
Total 600.  MATCHES.

Now: which orbits come from HIGH circles and which from LOW?

Let me measure the orbit of each triple, tagged by its circle's kind.

Run:  python arc_k7_a0_orbit_kind.py --q 5
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

        # classify each a=0 circle as HIGH or LOW
        kind_of = {}
        for k, BB in enumerate(blocks):
            if k == ci:
                continue
            if len(Bset & set(BB)) != 0:
                continue
            Wout = [p for p in BB if p not in Bset]
            if len(Wout) < 3:
                continue
            xyz = tuple(Wout[:3])
            invs = []
            for xy in itertools.combinations(xyz, 2):
                pairs = set()
                for kk in circ_through_pair.get(tuple(sorted(xy)), []):
                    if kk == ci:
                        continue
                    c2 = Bset & set(blocks[kk])
                    if len(c2) == 2:
                        pairs.add(tuple(sorted(c2)))
                invs.append(frozenset(pairs))
            u = set()
            for inv in invs:
                u |= inv
            kind_of[k] = "HIGH" if len(u) == q + 2 else "LOW"

        # for each a=0 triple, find its circle and orbit
        joint = Counter()
        for k, BB in enumerate(blocks):
            if k == ci:
                continue
            if len(Bset & set(BB)) != 0:
                continue
            Wout = [p for p in BB if p not in Bset]
            if len(Wout) < 3:
                continue
            kind = kind_of[k]
            for xyz in itertools.combinations(Wout, 3):
                invs = []
                for xy in itertools.combinations(xyz, 2):
                    pairs = set()
                    for kk in circ_through_pair.get(tuple(sorted(xy)), []):
                        if kk == ci:
                            continue
                        c2 = Bset & set(blocks[kk])
                        if len(c2) == 2:
                            pairs.add(tuple(sorted(c2)))
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
                        joint[(kind, oid)] += 1

        row = {"q": q, "joint": {f"{k},{o}": v for (k, o), v in
                                 sorted(joint.items())}}
        rows.append(row)
        print(f"q={q}: (circle kind, orbit) -> triples", flush=True)
        for (kind, oid), v in sorted(joint.items()):
            print(f"    {kind}, orbit {oid}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
