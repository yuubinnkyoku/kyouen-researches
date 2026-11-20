"""Re-analyse the K growth rate with the CORRECTED values.

Corrected series:
  inversive: q=3:5, 4:5, 5:6, 7:6, 8:7, 9:9, 11:9, 13:8, 17:9, 19:9
  AG:        q=3:5, 4:5, 5:6, 7:6, 8:8, 9:9, 11:9, 13:13, 16:16

The old (buggy) inversive series was 5,5,6,6,7,9,9,10,12,13,14 which looked
like steady growth.  The corrected series is 5,5,6,6,7,9,9,8,9,9 which is
NON-MONOTONE (q=13 gives 8, less than q=11's 9).

Let me re-examine:
  * Is K monotone in q?  NO for inversive (9 at q=11, 8 at q=13).
  * What is the growth rate?
  * Does K/q decrease?

This is a genuinely different picture from before.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


INV = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 8, 17: 9, 19: 9}
AG = {3: 5, 4: 5, 5: 6, 7: 6, 8: 8, 9: 9, 11: 9, 13: 13, 16: 16}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    print("CORRECTED inversive series:")
    print(f"{'q':>3} {'K':>3} {'K/q':>6} {'monotone?':>10}")
    prev = None
    rows = []
    for q in sorted(INV):
        k = INV[q]
        mono = "" if prev is None else ("up" if k > prev else ("same" if k == prev else "DOWN"))
        rows.append({"board": "inv", "q": q, "K": k, "K_over_q": k / q,
                     "trend": mono})
        print(f"{q:>3} {k:>3} {k/q:>6.2f} {mono:>10}")
        prev = k

    print()
    print("CORRECTED AG series:")
    print(f"{'q':>3} {'K':>3} {'K/q':>6} {'monotone?':>10}")
    prev = None
    for q in sorted(AG):
        k = AG[q]
        mono = "" if prev is None else ("up" if k > prev else ("same" if k == prev else "DOWN"))
        rows.append({"board": "ag", "q": q, "K": k, "K_over_q": k / q,
                     "trend": mono})
        print(f"{q:>3} {k:>3} {k/q:>6.2f} {mono:>10}")
        prev = k

    print()
    print("KEY OBSERVATIONS:")
    print("  * inversive K is NOT monotone: q=11 gives 9, q=13 gives 8.")
    print("  * AG K IS monotone (5,5,6,6,8,9,9,13,16).")
    print("  * inversive K/q decreases: 1.67 -> 0.47")
    print("  * AG K/q stays near 1.0 for q >= 8")

    # fit inversive K ~ c*q^alpha on q >= 7 (avoid small-board effects)
    qs = [q for q in sorted(INV) if q >= 7]
    ks = [INV[q] for q in qs]
    xs = [math.log(q) for q in qs]
    ys = [math.log(k) for k in ks]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    den = sum((x - mx) ** 2 for x in xs)
    alpha = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0
    c = math.exp(my - alpha * mx)
    print()
    print(f"inversive (q>=7): K ~ {c:.3f} * q^{alpha:.3f}")
    print(f"  => K grows like q^{alpha:.2f}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps({
            "rows": rows,
            "inversive_fit_q_ge_7": {"c": c, "alpha": alpha},
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
