"""k=7: the three missing profiles (5,), (6,), (7,) in closed form.

MEASURED (q=7):
    (5,) : 1,411,200
    (6,) :   411,600
    (7,) :     2,800

These are 7-sets with exactly ONE circle carrying >= 4 points, and that
circle carries 5, 6 or 7 points.

(7,): all 7 points on one circle.  Count = b * C(s,7).
      q=7: 350 * C(8,7) = 350*8 = 2,800.  MATCHES!

(6,): 6 points on one circle + 1 outside, and NO other 4-circle.
      Naive: b * C(s,6) * (n-s) = 350*28*42 = 411,600.  MATCHES!

(5,): 5 points on one circle + 2 outside, and NO other 4-circle.
      Naive: b * C(s,5) * C(n-s,2) = 350*56*861 = 16,875,600.
      Measured: 1,411,200.  So the naive count is 12x too big.

So (7,) and (6,) are the naive counts, but (5,) needs the "no other
4-circle" condition.

Let me verify (7,) and (6,) at q=5 too:
    q=5: (7,) = 130*C(6,7) = 0  (s=6 < 7)
         (6,) = 130*C(6,6)*20 = 2,600.  MATCHES the measured 2,600!

So at q=5 only (6,) exists, and it IS the naive count.  Good.

Now (5,): need to subtract the cases where the 2 outside points create
another 4-circle.

Run:  python arc_k7_missing.py --q 5 7
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
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
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
        coq = {}
        for k, BB in enumerate(blocks):
            for quad in itertools.combinations(BB, 4):
                coq[quad] = k

        # count 7-sets by profile, focusing on single-circle profiles
        single = Counter()
        for S in itertools.combinations(range(n), 7):
            Sset = set(S)
            hits = {}
            for quad in itertools.combinations(S, 4):
                cj = coq.get(quad)
                if cj is None:
                    continue
                hits[cj] = len(Sset & set(blocks[cj]))
            if len(hits) == 1:
                t = next(iter(hits.values()))
                single[t] += 1

        row = {"q": q, "n": n, "b": b, "s": s,
               "single_circle_profiles": dict(sorted(single.items())),
               "naive_7": b * comb(s, 7) if s >= 7 else 0,
               "naive_6": b * comb(s, 6) * (n - s) if s >= 6 else 0,
               "naive_5": b * comb(s, 5) * comb(n - s, 2) if s >= 5 else 0}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  single-circle profiles: "
              f"{dict(sorted(single.items()))}", flush=True)
        print(f"  naive (7,) = {row['naive_7']}", flush=True)
        print(f"  naive (6,) = {row['naive_6']}", flush=True)
        print(f"  naive (5,) = {row['naive_5']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
