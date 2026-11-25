"""k=8: the individual sums of v4, u4, z4.

We know v4 + u4 + z4 = [X concyclic], so

    sum v4 + sum u4 + sum z4 = N_cyc * C(s,4)

(because for each concyclic X, the sum over T of the indicator is
C(s,4) -- every T gives exactly one of the three).

Wait, that is not right: for a FIXED concyclic X with circle D,
  - if |D cap C| = 2, then T contains both points -> v4, or exactly one
    -> u4, or neither -> z4.
  - if |D cap C| = 1, then T contains it -> u4, else z4.
  - if |D cap C| = 0, then always z4.

So the split depends on |D cap C|, not just on concyclicity.

Let me measure the distribution of |D cap C| over concyclic X and derive
the three sums.

Run:  python arc_k8_v4u4z4_sums.py --q 5
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

    MEASURED = {5: {"v4": 450, "u4": 1800, "z4": 7425}}

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

        # for each concyclic X, record |D cap C| and the resulting
        # (v4,u4,z4) contributions summed over T
        hist = Counter()
        sums = Counter()
        for X in itertools.combinations(outside, 4):
            cj = circ_of_triple.get(tuple(sorted(X[:3])))
            if cj is None or not all(p in blocks[cj] for p in X):
                continue
            if cj == ci:
                continue
            capC = len(Bset & set(blocks[cj]))
            hist[capC] += 1
            # over all T (4-subsets of C):
            #   |D cap T| = 2 -> v4 ; = 1 -> u4 ; = 0 -> z4
            # D meets C in capC points; T is a 4-subset of C.
            # #T with |D cap T| = j = C(capC, j) * C(s-capC, 4-j)
            for j in (0, 1, 2):
                cnt = comb(capC, j) * comb(s - capC, 4 - j)
                if j == 2:
                    sums["v4"] += cnt
                elif j == 1:
                    sums["u4"] += cnt
                else:
                    sums["z4"] += cnt

        meas = MEASURED.get(q, {})
        row = {"q": q, "n": n, "b": b, "s": s,
               "capC_hist": dict(sorted(hist.items())),
               "sums": dict(sorted(sums.items())),
               "measured": meas,
               "match": all(sums[k] == meas.get(k) for k in ("v4", "u4", "z4"))}
        rows.append(row)
        print(f"q={q}: n={n}, b={b}, s={s}", flush=True)
        print(f"  |D cap C| histogram over concyclic X: "
              f"{dict(sorted(hist.items()))}", flush=True)
        print(f"  computed: v4={sums['v4']}, u4={sums['u4']}, "
              f"z4={sums['z4']}", flush=True)
        print(f"  measured: v4={meas.get('v4')}, u4={meas.get('u4')}, "
              f"z4={meas.get('z4')}", flush=True)
        print(f"  match: {row['match']}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
