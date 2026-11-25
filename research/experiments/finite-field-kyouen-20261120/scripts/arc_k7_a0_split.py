"""k=7: the a=0 circle split (20 vs 10) in closed form.

MEASURED (q=5): the 30 a=0 circles split into
    20 circles: u=7 (18 triples), u=9 (2 triples)
    10 circles: u=6 (2 triples), u=8 (18 triples)

So 20 + 10 = 30 = b - 1 - C(s,2)*q - s*(q-1) = 130-1-75-24.

Let me find the closed form for the 20/10 split.

Candidates:
    20 = ?  10 = ?
    C(s,2)*q = 75, s*(q-1) = 24, b-1 = 129
    20 = 4*5 = (q-1)*q?  = 20  YES
    10 = 2*5 = 2*q?  = 10  YES
    check: 20+10 = 30, and (q-1)*q + 2*q = q*(q+1) = 30  YES!

So the split is q*(q-1) and 2*q, summing to q*(q+1).

Let me verify this is consistent with the a=0 circle count formula:
    a=0 circles = b - 1 - C(s,2)*q - s*(q-1)
                = q(q^2+1) - 1 - q(q+1)q/2 - (q+1)(q-1)

For q=5: 130 - 1 - 75 - 24 = 30.
And q*(q+1) = 30.  So the a=0 count equals q(q+1)!

Let me verify: q(q^2+1) - 1 - q^2(q+1)/2 - (q^2-1)
            = q^3 + q - 1 - (q^3+q^2)/2 - q^2 + 1
            = q^3 + q - (q^3+q^2)/2 - q^2
            = (2q^3 + 2q - q^3 - q^2 - 2q^2)/2
            = (q^3 - 3q^2 + 2q)/2
            = q(q^2 - 3q + 2)/2
            = q(q-1)(q-2)/2

For q=5: 5*4*3/2 = 30.  YES.

So a=0 circles = q(q-1)(q-2)/2, NOT q(q+1).  Let me recheck the 20/10 split.

Run:  python arc_k7_a0_split.py --q 5 7
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

        circ_through_pair = {}
        for k, BB in enumerate(blocks):
            for pair in itertools.combinations(BB, 2):
                circ_through_pair.setdefault(pair, []).append(k)

        per_W = Counter()
        for k, BB in enumerate(blocks):
            if k == ci:
                continue
            if len(Bset & set(BB)) != 0:
                continue
            Wout = [p for p in BB if p not in Bset]
            if len(Wout) < 3:
                continue
            dist = Counter()
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
                u = set()
                for inv in invs:
                    u |= inv
                dist[len(u)] += 1
            per_W[tuple(sorted(dist.items()))] += 1

        a0 = b - 1 - comb(s, 2) * q - s * (q - 1)
        row = {"q": q, "n": n, "b": b, "s": s,
               "a0_circles": a0,
               "a0_formula": q * (q - 1) * (q - 2) // 2,
               "per_W": {str(k): v for k, v in
                         sorted(per_W.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: a=0 circles = {a0} "
              f"(formula q(q-1)(q-2)/2 = {q*(q-1)*(q-2)//2})", flush=True)
        print(f"  distinct per-W distributions: {len(per_W)}", flush=True)
        for k, v in sorted(per_W.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v} circles", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
