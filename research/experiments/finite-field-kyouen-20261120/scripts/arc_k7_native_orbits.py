"""k=7: orbit multiplicities using the NATIVE P^1(F_{q^2}) model.

The ovoid model's circle C is an abstract set of s points; mapping it to
P^1(F_q) by sorted order does not preserve the Mobius structure, so the
induced permutations are not the right involutions.

The NATIVE model (inversive_all_q.build_inversive_plane) has
points = P^1(F_{q^2}) and circles = images of P^1(F_q) under PGL(2,F_{q^2}).
There, a circle IS a copy of P^1(F_q) with the correct structure, so the
involutions can be read off directly.

Run:  python arc_k7_native_orbits.py --q 5
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from inversive_all_q import build_inversive_plane  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        points, circles = build_inversive_plane(q)
        idx = {p: i for i, p in enumerate(points)}
        blocks = [tuple(sorted(idx[p] for p in c)) for c in circles]
        n = len(points)
        b = len(blocks)
        s = q + 1
        circ_through_pair = {}
        for ci, B in enumerate(blocks):
            for pair in itertools.combinations(B, 2):
                circ_through_pair.setdefault(pair, []).append(ci)

        ci = 0
        B = blocks[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]

        # For each triple, compute the three involutions as permutations of
        # C's OWN points (indices into B), then canonicalise by the
        # multiset of pair-sets.  This is the honest object; the PGL orbit
        # question needs the actual group action, which we handle by
        # grouping on the full pair-set structure.
        dist_hist = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = None
            for cj, BB in enumerate(blocks):
                if cj == ci:
                    continue
                if all(p in BB for p in xyz):
                    W = cj
                    break
            WcapC = Bset & set(blocks[W]) if W is not None else set()
            invs = []
            for xy in itertools.combinations(xyz, 2):
                pairs = set()
                for cj in circ_through_pair.get(tuple(sorted(xy)), []):
                    if cj == ci:
                        continue
                    cap = Bset & set(blocks[cj])
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
