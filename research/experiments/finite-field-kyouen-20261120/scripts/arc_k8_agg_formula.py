"""Derive the closed form of sum(v2+v3+v4) and sum(u3+u4).

MEASURED at q=5:
    sum v2 = 324,000
    sum v3 =  28,800
    sum v4 =     450
    sum u3 =  74,400
    sum u4 =   1,800
    sum z4 =   7,425
    tuples =  72,675

The aggregate sum(v2+v3+v4) counts triples (T, X, C') with
|C' cap T| = 2 and |C' cap X| >= 2.

STRUCTURE.  Fix C' with |C' cap C| = 2, say C' cap C = {a,b}.
  - T must contain a and b: T = {a,b} + 2 more from C, so C(s-2,2) choices.
  - C' has some points outside C; call them Y = C' - C.
  - |C' cap X| = |Y cap X|.
  - X is a 4-subset of the outside (n-s points).
  - Need |Y cap X| >= 2.

So
  sum(v2+v3+v4) = sum over C' with |C' cap C|=2 of
                    C(s-2,2) * #{X : |Y cap X| >= 2}

Let me verify this decomposition numerically at q=5.

Run:  python arc_k8_agg_formula.py --q 5
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
        nout = len(outside)

        # for each C' with |C' cap C| = 2, compute |Y| = |C' - C| and
        # count X with |Y cap X| >= 2
        hist = Counter()
        total = 0
        for kk in range(b):
            if kk == ci:
                continue
            capC = len(Bset & set(blocks[kk]))
            if capC != 2:
                continue
            Y = [p for p in blocks[kk] if p not in Bset]
            y = len(Y)
            # count 4-subsets X of outside with |Y cap X| >= 2
            cnt = 0
            for X in itertools.combinations(outside, 4):
                if len(set(Y) & set(X)) >= 2:
                    cnt += 1
            hist[y] += 1
            total += cnt

        predicted = comb(s - 2, 2) * total
        row = {"q": q, "n": n, "b": b, "s": s, "nout": nout,
               "Y_size_hist": dict(sorted(hist.items())),
               "sum_over_Cprime": total,
               "C(s-2,2)": comb(s - 2, 2),
               "predicted_sum_v2v3v4": predicted}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}, outside={nout}", flush=True)
        print(f"  |Y| histogram for C' with |C' cap C|=2: "
              f"{dict(sorted(hist.items()))}", flush=True)
        print(f"  sum over C' of #{{X : |Y cap X|>=2}} = {total}", flush=True)
        print(f"  C(s-2,2) = {comb(s-2,2)}", flush=True)
        print(f"  predicted sum(v2+v3+v4) = {predicted}", flush=True)
        print(f"  measured                = 353250", flush=True)
        print(f"  match: {predicted == 353250}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
