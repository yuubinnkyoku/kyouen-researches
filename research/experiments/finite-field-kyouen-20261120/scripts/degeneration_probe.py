"""Does circle degeneration (q = 1 mod 4) increase K?

Hypothesis from the q=13 analysis: when q = 1 mod 4, x^2+y^2 factors and the
circles degenerate into smaller blocks (size q-1) plus large "cross" blocks
(size 2q-1).  The smaller blocks are weaker constraints, so K may be larger.

Test: compare K for q = 1 mod 4 (5, 9, 13, 17) against q = 3 mod 4 (3, 7, 11, 19)
at comparable board sizes.

Known data:
  q=3  (3 mod 4): K=5
  q=5  (1 mod 4): K=6
  q=7  (3 mod 4): K=6
  q=9  (1 mod 4): K=9
  q=11 (3 mod 4): K=9
  q=13 (1 mod 4): K>=13
  q=17 (1 mod 4): ?
  q=19 (3 mod 4): ?

The pairs (5,7), (9,11), (13,17?) are close in size.  Let's compute K for
q=17 and q=19 to extend the comparison.

This script reports the block structure and runs the symmetry-broken search.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[17, 19])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        sizes = Counter(len(b) for b in blocks)
        print(f"q={q} (mod4={q % 4}): {len(pts)} points, {len(blocks)} blocks, "
              f"sizes={dict(sorted(sizes.items()))}", flush=True)
        rows.append({
            "q": q,
            "q_mod_4": q % 4,
            "points": len(pts),
            "blocks": len(blocks),
            "block_sizes": dict(sorted(sizes.items())),
        })

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
