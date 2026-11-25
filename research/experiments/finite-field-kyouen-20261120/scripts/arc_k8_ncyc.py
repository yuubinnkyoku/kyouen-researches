"""k=8: the number of concyclic 4-subsets among the outside points.

This is the last missing piece: v4+u4+z4 sums to the concyclicity
indicator, so we need

    N_cyc = #{X : X is a 4-subset of the outside, X concyclic}

MEASURED at q=5: 645 out of C(20,4) = 4,845.

STRUCTURE.  The outside has m = n - s points.  A 4-subset is concyclic
iff it lies on a circle.  Circles meeting the outside in >= 4 points
contribute C(|C' cap outside|, 4) each.

Let me measure the distribution of |C' cap outside| and derive N_cyc.

Run:  python arc_k8_ncyc.py --q 5
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from math import comb
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
        outset = set(outside)

        # distribution of |C' cap outside|
        hist = Counter()
        for kk in range(b):
            if kk == ci:
                continue
            hist[len(outset & set(blocks[kk]))] += 1

        # direct count of concyclic X
        circ_of_triple = {}
        for k, BB in enumerate(blocks):
            for tri in itertools.combinations(BB, 3):
                circ_of_triple[tri] = k
        ncyc = 0
        for X in itertools.combinations(outside, 4):
            cj = circ_of_triple.get(tuple(sorted(X[:3])))
            if cj is not None and all(p in blocks[cj] for p in X):
                ncyc += 1

        # predicted from the histogram: sum over circles of C(|cap outside|,4)
        # but each concyclic X lies on exactly ONE circle, so no overcount
        predicted = sum(cnt * comb(y, 4) for y, cnt in hist.items())

        row = {"q": q, "n": n, "b": b, "s": s,
               "outside": len(outside),
               "hist": dict(sorted(hist.items())),
               "ncyc_direct": ncyc,
               "ncyc_predicted": predicted,
               "match": ncyc == predicted}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}, outside={len(outside)}",
              flush=True)
        print(f"  |C' cap outside| histogram: "
              f"{dict(sorted(hist.items()))}", flush=True)
        print(f"  N_cyc direct    = {ncyc}", flush=True)
        print(f"  N_cyc predicted = {predicted}", flush=True)
        print(f"  match: {ncyc == predicted}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
