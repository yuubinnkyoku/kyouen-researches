"""k=8: the z4 closed form.

z4 = #{C' : |C' cap T| = 0 and |C' cap X| = 4}

Since C' meets C in <= 2 points, |C' cap T| = 0 means C' meets C in 0
points OR in points outside T.  But T is a 4-subset of C, so C' can meet
C in 2 points that are NOT in T.

Hmm, so z4 is NOT simply "X is concyclic".  Let me re-read the definition:

    z4 = #{C' != C : |C' cap T| = 0 and |C' cap X| = 4}

C' contains all 4 points of X.  Since 4 points determine at most one
circle, there is AT MOST ONE such C' -- namely the circle through X, if
X is concyclic.

So z4 = 1 if X is concyclic (and that circle is != C and meets T in 0
points), else 0.

But wait: if X is concyclic with circle D, then D contains all of X.  Does
D meet T?  D could meet C in 0, 1 or 2 points.  If it meets C in 2 points
and both are in T, then |D cap T| = 2, not 0, so D would be counted in v2
(or v3/v4) instead.

So z4 = 1 iff X is concyclic AND the circle through X meets C in at most
1 point of T.

MEASURED at q=5: z4 = 1 in 7,425 of 72,675 tuples (10.2%).

Let me verify: how many 4-subsets X of the outside points are concyclic?
The outside has n-s = 20 points at q=5.  The number of concyclic 4-subsets
of the outside is the number of 4-arcs... no, the number of 4-subsets that
lie on a circle.

Let me just measure it.

Run:  python arc_k8_z4.py --q 5
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
        base = set(sub) | {None}
        ci = None
        for k, B in enumerate(blocks):
            if set(points[i] for i in B) == base:
                ci = k
                break
        B = blocks[ci]
        Bset = set(B)
        outside = [p for p in range(n) if p not in Bset]

        circ_of_triple = {}
        for k, BB in enumerate(blocks):
            for tri in itertools.combinations(BB, 3):
                circ_of_triple[tri] = k

        # how many 4-subsets of outside are concyclic?
        concyc = 0
        totalX = 0
        for X in itertools.combinations(outside, 4):
            totalX += 1
            cj = circ_of_triple.get(tuple(sorted(X[:3])))
            if cj is not None and all(p in blocks[cj] for p in X):
                concyc += 1

        # z4 distribution and its relation to concyclicity
        z4_hist = Counter()
        z4_given_concyc = Counter()
        for T in itertools.combinations(B, 4):
            Tset = set(T)
            for X in itertools.combinations(outside, 4):
                Xset = set(X)
                cj = circ_of_triple.get(tuple(sorted(X[:3])))
                is_concyc = (cj is not None
                             and all(p in blocks[cj] for p in X))
                z4 = 0
                if is_concyc and cj != ci:
                    if len(Tset & set(blocks[cj])) == 0:
                        z4 = 1
                z4_hist[z4] += 1
                z4_given_concyc[(is_concyc, z4)] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "outside": len(outside),
               "concyclic_X": concyc, "total_X": totalX,
               "z4_hist": dict(sorted(z4_hist.items())),
               "z4_given_concyc": {str(k): v for k, v in
                                   sorted(z4_given_concyc.items())}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}, outside={len(outside)}",
              flush=True)
        print(f"  concyclic X: {concyc} / {totalX}", flush=True)
        print(f"  z4 histogram: {dict(sorted(z4_hist.items()))}", flush=True)
        print(f"  (is_concyclic, z4) -> count:", flush=True)
        for k, v in sorted(z4_given_concyc.items()):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
