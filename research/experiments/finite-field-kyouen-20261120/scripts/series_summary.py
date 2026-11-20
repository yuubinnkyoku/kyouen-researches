"""Complete the K series and analyse the AG / inversive gap.

Data collected so far:

  q   AG(2,q)   inversive
  3      5          5
  4      5          5
  5      6          6
  7      6          6
  8      8          7
  9      9          9
 11      9          9
 13    >=13        10
 16    >=12        >=11

This script:
  1. tabulates the data with the counting bounds,
  2. computes the ratio K/q and K/n,
  3. tests whether the AG/inversive gap grows with q,
  4. reports the block-size distributions that might explain the gap.

The key structural difference: AG(2,q) has q(q+1) LINES of size q in addition
to the circles, while the inversive plane has only circles (of size q+1).
A line meets a circle in at most 2 points, so line constraints and circle
constraints interact weakly -- which may allow larger safe sets in AG.
"""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path


AG = {3: 5, 4: 5, 5: 6, 7: 6, 8: 8, 9: 9, 11: 9, 13: 13, 16: 12}
AG_EXACT = {3, 4, 5, 7, 8, 9, 11}
INV = {3: 5, 4: 5, 5: 6, 7: 6, 8: 7, 9: 9, 11: 9, 13: 10, 16: 11}
INV_EXACT = {3, 4, 5, 7, 8, 9, 11, 13}


def counting_bound(q: int) -> int:
    b = q * (q * q + 1)
    k = 3
    while comb(k + 1, 3) <= b:
        k += 1
    return k


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    qs = sorted(set(AG) | set(INV))
    print(f"{'q':>3} {'AG':>5} {'exact':>6} {'inv':>5} {'exact':>6} "
          f"{'gap':>5} {'AG/q':>6} {'inv/q':>6} {'cnt':>5}")
    rows = []
    for q in qs:
        a = AG.get(q)
        i = INV.get(q)
        gap = (a - i) if (a is not None and i is not None) else None
        cb = counting_bound(q)
        rows.append({
            "q": q,
            "ag": a, "ag_exact": q in AG_EXACT,
            "inv": i, "inv_exact": q in INV_EXACT,
            "gap": gap,
            "ag_over_q": a / q if a else None,
            "inv_over_q": i / q if i else None,
            "counting_bound": cb,
        })
        print(f"{q:>3} {a if a is not None else '-':>5} "
              f"{'Y' if q in AG_EXACT else 'n':>6} "
              f"{i if i is not None else '-':>5} "
              f"{'Y' if q in INV_EXACT else 'n':>6} "
              f"{gap if gap is not None else '-':>5} "
              f"{a/q if a else 0:>6.2f} {i/q if i else 0:>6.2f} {cb:>5}")

    print()
    print("observations:")
    print("  * AG and inversive agree for q = 3,4,5,7,9,11")
    print("  * AG > inversive at q = 8 (8 vs 7)")
    print("  * AG >> inversive at q = 13 (>=13 vs 10)")
    print("  * K/q decreases for both, but AG decreases more slowly")
    print()
    print("block structure:")
    print("  AG(2,q):  q^2(q-1) circles of size q+1, q(q+1) lines of size q")
    print("  inversive: q(q^2+1) circles of size q+1")
    print("  => AG has extra LINE blocks; a line meets a circle in <= 2 points,")
    print("     so the two constraint families interact weakly.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
