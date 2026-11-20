"""Quantify the relation between circle degeneration and K.

For AG(2,q), the block structure depends on q mod 4:

  q = 3 mod 4:  circles of size q+1 (q^2(q-1) of them), lines of size q
  q = 1 mod 4:  degenerate circles of size q-1 (q^2 of them),
                crosses of size 2q-1 (q^2 of them),
                lines of size q
  q even:       circles degenerate as (x+y)^2, different structure

Let us define a "constraint strength" measure and correlate it with K.

Natural measures:
  (a) average block size: larger blocks are stronger constraints
  (b) number of blocks per point (degree): more blocks = stronger
  (c) the "triple budget" b / C(k,3): how much slack the counting bound has

Let us compute these for each q and compare with K.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402

# known K values (lower bounds marked)
K_DATA = {
    3: (5, True), 4: (5, True), 5: (6, True), 7: (6, True), 8: (8, True),
    9: (9, True), 11: (9, True), 13: (13, False), 16: (12, False),
    17: (17, False), 19: (13, False),
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=sorted(K_DATA))
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'mod4':>5} {'pts':>5} {'blocks':>7} {'avg size':>9} "
          f"{'deg':>5} {'K':>4} {'exact':>6} {'K/q':>6}")
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        n = len(pts)
        sizes = Counter(len(b) for b in blocks)
        total_inc = sum(len(b) for b in blocks)
        avg_size = Fraction(total_inc, len(blocks))
        degs = Counter(len(t) for t in through)
        deg = next(iter(degs)) if len(degs) == 1 else None
        k, exact = K_DATA.get(q, (None, None))
        rows.append({
            "q": q, "q_mod_4": q % 4, "points": n, "blocks": len(blocks),
            "block_sizes": dict(sorted(sizes.items())),
            "avg_block_size": str(avg_size),
            "degree": deg, "degree_uniform": len(degs) == 1,
            "K": k, "K_exact": exact,
            "K_over_q": (k / q) if k else None,
        })
        print(f"{q:>3} {q % 4:>5} {n:>5} {len(blocks):>7} {float(avg_size):>9.2f} "
              f"{deg if deg else 'var':>5} {k if k else '-':>4} "
              f"{'Y' if exact else 'n':>6} {k/q if k else 0:>6.2f}")

    print()
    print("block size distributions:")
    for r in rows:
        print(f"  q={r['q']:>2} (mod4={r['q_mod_4']}): {r['block_sizes']}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
