"""k=7: the correct Mobius bijection from a circle to P^1(F_q).

The previous attempt failed because the ovoid model's circle C was mapped
to P^1(F_q) by sorted order, which does not preserve the Mobius structure.

THE RIGHT WAY.  In the NATIVE model, a circle is by construction the image
of P^1(F_q) under a Mobius map.  So we can recover the bijection directly:
for a circle C = g(P^1(F_q)), the map g^{-1} restricted to C gives the
bijection to P^1(F_q).

But even simpler: in the native model, the points of P^1(F_{q^2}) are field
elements (or infinity), and F_q is a subfield.  A circle through the three
"anchor" points 0, 1, infinity is exactly P^1(F_q).  So for THAT circle the
bijection is the identity!

So: use the circle C = P^1(F_q) itself (the one through 0, 1, infinity).
Then C's points ARE P^1(F_q) with the correct structure, and the
involutions can be read off directly.

Run:  python arc_k7_identity_circle.py --q 5
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--q", type=int, nargs="+", default=[5])
    args = ap.parse_args()

    rows = []
    for q in args.q:
        F, sub = build_field(q)
        points, circles = build_inversive_plane(q)
        idx = {p: i for i, p in enumerate(points)}
        blocks = [tuple(sorted(idx[p] for p in c)) for c in circles]
        n = len(points)
        b = len(blocks)
        s = q + 1

        # find the circle P^1(F_q) = F_q u {infinity}
        base = set(sub) | {None}
        ci = None
        for k, B in enumerate(blocks):
            if set(points[i] for i in B) == base:
                ci = k
                break
        if ci is None:
            print(f"q={q}: P^1(F_q) not found as a circle", flush=True)
            continue
        B = blocks[ci]
        Bset = set(B)
        # the bijection: point index -> P^1(F_q) index
        p1 = list(sub) + [None]
        p1_idx = {repr(x): i for i, x in enumerate(p1)}
        c_to_p1 = {idx[p]: p1_idx[repr(p)] for p in base}

        circ_through_pair = {}
        for k, BB in enumerate(blocks):
            for pair in itertools.combinations(BB, 2):
                circ_through_pair.setdefault(pair, []).append(k)

        outside = [p for p in range(n) if p not in Bset]

        dist_hist = Counter()
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

        row = {"q": q, "n": n, "b": b, "s": s, "circle_index": ci,
               "num_distributions": len(dist_hist),
               "distributions": {str(k): v for k, v in
                                 sorted(dist_hist.items(),
                                        key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}, C = P^1(F_q) at index {ci}",
              flush=True)
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
