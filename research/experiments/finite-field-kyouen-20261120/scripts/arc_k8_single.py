"""k=8: the general single-circle profile (j,) formula.

A (j,) profile means: exactly ONE circle carries >= 4 points of S, and it
carries j of them.  The other 8-j points are outside that circle.

For k=8 with |T| = 4 on the base circle C:
  - the "big" circle can be C itself (j = 4, the 4 points of T) -- but then
    the other 4 points are outside C, and we need NO other 4-circle.
  - or the big circle can be another circle D carrying j >= 5 points.

The (j,) profiles with j >= 5 arise when D carries j points of S and no
other circle carries 4.

MEASURED at q=7 (s=8): (5,)=1411200, (6,)=411600, (7,)=2800.
MEASURED at q=5 (s=6): (6,)=2600, (5,)=0.

At q=9 (s=10) we need (5,), (6,), (7,), (8,).

KEY: (8,) = b*C(s,8) is exact (all 8 on one circle, no other 4-circle
possible since the other points are outside).
(7,) = b*C(s,7)*(n-s) is exact (7 on one circle + 1 outside; the outside
point cannot create a 4-circle with only 1 point).

For (6,): 6 on one circle + 2 outside.  A second 4-circle needs 2 of the
6 plus both outside points.  So (6,) = b*C(s,6)*C(n-s,2) - (cases where a
pencil circle through the 2 outside points meets the 6 in exactly 2).

For (5,): 5 on one circle + 3 outside.  A second 4-circle needs 2 of the 5
plus 2 of the 3 outside.

Let me measure the (6,) and (5,) values at q=9 by direct enumeration of
the single-circle profiles, to get the numbers we need.

Run:  python arc_k8_single.py --q 9
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
    ap.add_argument("--q", type=int, nargs="+", default=[9])
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

        # count single-circle profiles by direct enumeration over
        # (circle D, j-subset of D, (8-j)-subset of outside D)
        # This is expensive; do it for j >= 5 only and use the
        # "no other 4-circle" test.
        single = Counter()
        # For each circle D, choose j points of D and 8-j outside D
        for dk in range(b):
            D = blocks[dk]
            Dset = set(D)
            outD = [p for p in range(n) if p not in Dset]
            for j in range(5, 9):
                if j > len(D) or 8 - j > len(outD):
                    continue
                for Tj in itertools.combinations(D, j):
                    Tjset = set(Tj)
                    for Y in itertools.combinations(outD, 8 - j):
                        Sset = Tjset | set(Y)
                        # check no other 4-circle
                        ok = True
                        for quad in itertools.combinations(sorted(Sset), 4):
                            cj = circ_of_triple.get(tuple(sorted(quad[:3])))
                            if cj is None:
                                continue
                            if cj == dk:
                                continue
                            if all(p in blocks[cj] for p in quad):
                                ok = False
                                break
                        if ok:
                            single[j] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "single": dict(sorted(single.items()))}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  single-circle profiles: {dict(sorted(single.items()))}",
              flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
