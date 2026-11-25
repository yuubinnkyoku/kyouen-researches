"""k=7: the w marginal in closed form.

MEASURED (q=5, per (C,T) with |T|=4, over C(n-s,3)=1140 triples):

    w=0: 700,  w=1: 320,  w=2: 120

DERIVATION.  W is the circle through x,y,z.  w = |T cap W|.

For fixed T (4 points of C), count triples {x,y,z} outside C by w.

A triple determines W uniquely.  Conversely, for a circle W, the triples
{x,y,z} with W(x,y,z) = W are the 3-subsets of W that are not contained in
a smaller circle -- but any 3 points of W determine W, so the triples are
exactly the 3-subsets of W that lie outside C... no: x,y,z must be OUTSIDE
C, so they are 3-subsets of W \\ C.

So:
    #{triples with W(x,y,z) = W} = C(|W \\ C|, 3)

and w = |T cap W|.

Now classify W by a = |W cap C| (0, 1 or 2):

  a = 0:  W disjoint from C.  |W \\ C| = s = q+1.  w = 0.
  a = 1:  W meets C in 1 point p.  |W \\ C| = s-1 = q.  w = [p in T].
  a = 2:  W meets C in 2 points p,p'.  |W \\ C| = s-2 = q-1.
          w = #{p,p'} cap T.

So:
    w=2 count = sum over W with a=2 and both points in T of C(q-1,3)
    w=1 count = sum over W with a=2 and exactly one point in T of C(q-1,3)
              + sum over W with a=1 and the point in T of C(q,3)
    w=0 count = the rest

Let me verify with the known circle counts.

Run:  python arc_k7_w_formula.py --q 5
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

        ci = 0
        B = circles[ci]
        Bset = set(B)
        T = tuple(B[:4])
        Tset = set(T)

        # count circles W by (a, w)
        by_aw = Counter()
        for cj, W in enumerate(circles):
            if cj == ci:
                continue
            cap = Bset & set(W)
            a = len(cap)
            w = len(Tset & set(W))
            by_aw[(a, w)] += 1

        # predicted w marginal
        pred = Counter()
        for (a, w), cnt in by_aw.items():
            outside_count = s - a
            if outside_count >= 3:
                pred[w] += cnt * comb(outside_count, 3)

        row = {"q": q, "n": n, "b": b, "s": s,
               "circles_by_a_w": {f"{a},{w}": v for (a, w), v in
                                  sorted(by_aw.items())},
               "predicted_w": dict(sorted(pred.items()))}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  circles by (|W cap C|, w):", flush=True)
        for (a, w), cnt in sorted(by_aw.items()):
            print(f"    a={a} w={w}: {cnt}", flush=True)
        print(f"  predicted w marginal: {dict(sorted(pred.items()))}",
              flush=True)
        print(f"  measured: {{0: 700, 1: 320, 2: 120}}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
