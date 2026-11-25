"""k=8: the (6,) single-circle profile in closed form.

(6,) = #8-sets with exactly one circle carrying >= 4 points, and it
carries 6.

STRUCTURE.  The big circle D carries 6 points of S; the other 2 points
Y = {y1, y2} are outside D.  No other circle may carry 4 of S.

A second circle C' carrying 4 of S must carry 2 of the 6 points of D
(since C' meets D in <= 2 points) and both y1, y2.  So C' is a circle
through y1, y2 that meets D in exactly 2 of the 6 chosen points.

The pencil through y1, y2 has q+1 circles.  Let n2 = number of them that
meet D in exactly 2 points.  For each such circle C', the number of
6-subsets of D meeting C' in exactly 2 points is C(2,2)*C(s-2,4) if
|C' cap D| = 2.

So:
  (6,) = b * sum over {y1,y2} of
           [ C(s,6)*C(n-s,2) - #{(T6, {y1,y2}) : some C' meets T6 in 2} ]

This is an inclusion-exclusion.  Let me measure the structure directly:
for each (D, T6, Y) count how many pencil circles through Y meet T6 in 2.

Run:  python arc_k8_six_formula.py --q 7
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
    ap.add_argument("--q", type=int, nargs="+", default=[7])
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

        circ_through_pair = {}
        for k, BB in enumerate(blocks):
            for pair in itertools.combinations(BB, 2):
                circ_through_pair.setdefault(pair, []).append(k)

        # fix one circle D and enumerate
        D = blocks[0]
        Dset = set(D)
        outD = [p for p in range(n) if p not in Dset]

        hist = Counter()
        total_ok = 0
        for T6 in itertools.combinations(D, 6):
            T6set = set(T6)
            for Y in itertools.combinations(outD, 2):
                # count pencil circles through Y meeting T6 in exactly 2
                cnt = 0
                for ck in circ_through_pair.get(tuple(sorted(Y)), []):
                    if ck == 0:
                        continue
                    if len(T6set & set(blocks[ck])) == 2:
                        cnt += 1
                hist[cnt] += 1
                if cnt == 0:
                    total_ok += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "hist": dict(sorted(hist.items())),
               "ok_per_circle": total_ok,
               "predicted_6": b * total_ok}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  #pencil circles meeting T6 in 2 -> count:", flush=True)
        for k, v in sorted(hist.items()):
            print(f"    {k}: {v}", flush=True)
        print(f"  (6,) per circle = {total_ok}", flush=True)
        print(f"  predicted (6,) = b * {total_ok} = {b*total_ok}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
