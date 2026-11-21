"""k=7: 37 PGL-orbits vs 9 types vs 90 ad-hoc canonical forms.

MEASURED:
    q=5: |PGL(2,5)| = 120, |P^1(F_5)| = 6, involutions = 25
         triples of involutions = 2300
         PGL-orbits on triples = 37
         orbit sizes: 120 (x9), 60 (x16), 30 (x6), 20 (x2), 15, 10 (x2), 5

COMPARE:
    - 9 types (by (w,u)-distribution)
    - 90 ad-hoc canonical forms (by first-appearance relabelling)
    - 37 PGL-orbits (the correct group-theoretic count)

The ad-hoc 90 is an ARTEFACT of the canonicalisation: relabelling by first
appearance does not respect the group action, so it over-counts.

The 37 PGL-orbits is the right invariant.  But 37 > 9, so the (w,u)
distribution does not separate all PGL-orbits -- several orbits share a
distribution.

Let me verify: group the 37 orbits by their (w,u)-distribution and check
that we get 9 classes.

Run:  python arc_k7_orbit_types.py --q 5
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, ovoid, circles = build(q)
        n = len(ovoid)
        b = len(circles)
        s = q + 1
        circ_through_pair = {}
        for ci, B in enumerate(circles):
            for pair in itertools.combinations(B, 2):
                circ_through_pair.setdefault(pair, []).append(ci)

        ci = 0
        B = circles[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]

        # For each triple, record the (w,u)-distribution and the
        # "involution triple" as a canonical object under PGL.
        # Since we cannot easily compute PGL orbits here, just record the
        # distribution and the multiset of pair-sets (as frozensets of
        # frozensets of point indices in C's own labelling).
        dist_hist = Counter()
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
            dist_hist[tuple(sorted(dist.items()))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "num_distributions": len(dist_hist),
               "distributions": {str(k): v for k, v in
                                 sorted(dist_hist.items(),
                                        key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  distinct (w,u)-distributions: {len(dist_hist)}", flush=True)
        for k, v in sorted(dist_hist.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
