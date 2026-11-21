"""k=7: the circle-based decomposition of the triple count.

VERIFIED: the triple count decomposes exactly by a = |W cap C|:

    a=0: 600,  a=1: 240,  a=2: 300,  total 1140 = C(n-s,3)

And the circle counts by a are known in closed form (from the k=7 w
analysis):

    a=2: C(s,2)*q
    a=1: s*(q-1)
    a=0: b - 1 - C(s,2)*q - s*(q-1)

Check q=5: a=2: 15*5 = 75 circles, each with C(s-2,3) = C(4,3) = 4 triples
-> 300.  a=1: 6*4 = 24 circles, each with C(5,3) = 10 triples -> 240.
a=0: 130-1-75-24 = 30 circles, each with C(6,3) = 20 triples -> 600.
ALL MATCH.

So the triple count is fully closed.  The remaining question is how the
TYPE distributes within each a-class.

Let me measure the type distribution conditioned on a.

Run:  python arc_k7_by_a.py --q 5
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

        by_a = Counter()
        for xyz in itertools.combinations(outside, 3):
            W = None
            for cj, BB in enumerate(circles):
                if cj == ci:
                    continue
                if all(p in BB for p in xyz):
                    W = cj
                    break
            WcapC = Bset & set(circles[W]) if W is not None else set()
            a = len(WcapC)
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
            by_a[(a, tuple(sorted(dist.items())))] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "by_a": {str(k): v for k, v in
                        sorted(by_a.items(), key=lambda x: -x[1])}}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (a, distribution) -> count", flush=True)
        for k, v in sorted(by_a.items(), key=lambda x: -x[1]):
            print(f"    {k}: {v}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
