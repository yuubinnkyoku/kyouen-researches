"""Correlate K/q with structural invariants of AG(2,q).

Data (exact K):
  q=3: K=5, K/q=1.67
  q=4: K=5, K/q=1.25
  q=5: K=6, K/q=1.20
  q=7: K=6, K/q=0.86
  q=8: K=8, K/q=1.00
  q=9: K=9, K/q=1.00
  q=11: K=9, K/q=0.82

Structural invariants to test:
  (a) number of blocks b = q^3+q
  (b) degree d = q^2+q
  (c) average block size
  (d) number of "large" blocks (size > q+1)
  (e) the ratio b / C(q^2, 3)  -- how much of the triple space is covered
  (f) the "cross" presence (q = 1 mod 4)

Let me compute these and look for correlation with K/q.
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

K_DATA = {3: 5, 4: 5, 5: 6, 7: 6, 8: 8, 9: 9, 11: 9}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=sorted(K_DATA))
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    print(f"{'q':>3} {'mod4':>5} {'K':>3} {'K/q':>5} {'b':>7} {'avg':>6} "
          f"{'maxblk':>7} {'b/C(n,3)':>10}")
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        n = len(pts)
        b = len(blocks)
        sizes = Counter(len(x) for x in blocks)
        avg = Fraction(sum(len(x) for x in blocks), b)
        maxblk = max(sizes)
        cover = Fraction(b, comb(n, 3))
        k = K_DATA[q]
        rows.append({
            "q": q, "q_mod_4": q % 4, "K": k, "K_over_q": k / q,
            "blocks": b, "avg_block_size": str(avg), "max_block": maxblk,
            "block_sizes": dict(sorted(sizes.items())),
            "b_over_C_n_3": str(cover),
        })
        print(f"{q:>3} {q%4:>5} {k:>3} {k/q:>5.2f} {b:>7} {float(avg):>6.2f} "
              f"{maxblk:>7} {float(cover):>10.5f}")

    print()
    print("block size distributions:")
    for r in rows:
        print(f"  q={r['q']:>2}: {r['block_sizes']}")

    print()
    print("K/q vs max block size:")
    for r in rows:
        print(f"  q={r['q']:>2}: K/q={r['K_over_q']:.2f}, max block={r['max_block']}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
