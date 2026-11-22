"""k=8: the u3 closed form.

    u3 = #{C' : |C' cap T| = 1, |C' cap X| = 3}

From the |C' cap T| decomposition:

    #{C' : |C' cap T| = 1} = 4(q-1) + 4(s-4)q

Two sub-families:
  (a) tangent at a point of T: 4(q-1) circles
  (b) mixed 2-secants (one point in T, one in C-T): 4(s-4)q circles

For each, we need |C' cap X| = 3.

MEASURED at q=5: sum u3 = 74,400, sum u4 = 1,800, sum u3+u4 = 76,200.

u4 is known (concyclicity).  So sum u3 = 76,200 - 1,800 = 74,400.

Let me derive the aggregate sum(u3+u4) = #{|cap T|=1, |cap X|>=3}.

STRUCTURE.  Fix C' with |C' cap T| = 1.  Then T contains exactly one of
C' cap C.  Two cases:
  (a) |C' cap C| = 1 (tangent): T must contain that point, so
      T = {a} + 3 more from C-{a}: C(s-1,3) choices.
  (b) |C' cap C| = 2: T contains exactly one of the two, so
      T = {one of 2} + 3 more from C - (C' cap C): 2*C(s-2,3) choices.

And |C' cap X| = |Y cap X| where Y = C' - C.

Let me verify this decomposition numerically.

Run:  python arc_k8_u3_formula.py --q 5
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

        # for each C' with |C' cap C| in {1,2}, compute |Y| and the number
        # of T with |C' cap T| = 1, and the number of X with |Y cap X| >= 3
        by_capC = Counter()
        total = 0
        for kk in range(b):
            if kk == ci:
                continue
            capC = len(Bset & set(blocks[kk]))
            if capC not in (1, 2):
                continue
            Y = [p for p in blocks[kk] if p not in Bset]
            y = len(Y)
            # number of T (4-subsets of C) with |C' cap T| = 1
            if capC == 1:
                nT = comb(s - 1, 3)
            else:
                nT = 2 * comb(s - 2, 3)
            # number of X with |Y cap X| >= 3
            nX = 0
            for X in itertools.combinations(outside, 4):
                if len(set(Y) & set(X)) >= 3:
                    nX += 1
            by_capC[(capC, y)] += 1
            total += nT * nX

        row = {"q": q, "n": n, "b": b, "s": s,
               "by_capC": {str(k): v for k, v in sorted(by_capC.items())},
               "predicted_sum_u3u4": total}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  (|C' cap C|, |Y|) -> count: "
              f"{dict(sorted(by_capC.items()))}", flush=True)
        print(f"  predicted sum(u3+u4) = {total}", flush=True)
        print(f"  measured             = 76200", flush=True)
        print(f"  match: {total == 76200}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
