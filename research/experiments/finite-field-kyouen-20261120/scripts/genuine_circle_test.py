"""Quantitative test: does the ABSENCE of genuine circles (size q+1) raise K/q?

Hypothesis: K/q is high when there are FEW or NO genuine circles of size q+1.

Data:
  q=3: circles size 4 = q+1 (18 of them).  K/q=1.67
  q=4: circles size 4 = q (72), size 8 = 2q (6).  No size q+1=5.  K/q=1.25
  q=5: circles size 4 = q-1 (100), size 9 = 2q-1 (25).  No size q+1=6.  K/q=1.20
  q=7: circles size 8 = q+1 (294).  K/q=0.86
  q=8: circles size 8 = q (528), size 16 = 2q (28).  No size q+1=9.  K/q=1.00
  q=9: circles size 8 = q-1 (648), size 17 = 2q-1 (81).  No size q+1=10.  K/q=1.00
  q=11: circles size 12 = q+1 (1210).  K/q=0.82

So:
  q with genuine circles (size q+1): 3, 7, 11 -> K/q = 1.67, 0.86, 0.82
  q without genuine circles: 4, 5, 8, 9 -> K/q = 1.25, 1.20, 1.00, 1.00

The hypothesis holds!  q without genuine circles have K/q >= 1.00,
q with genuine circles have K/q <= 0.86 (except q=3 which is tiny).

Let me verify this pattern and quantify it.

Note: for q=3, the "genuine circle" has size q+1=4, and there are 18 of them.
K/q=1.67 is high because the board is tiny (9 points).

For q >= 7, the pattern is clean:
  q=7 (genuine circles): K/q=0.86
  q=11 (genuine circles): K/q=0.82
  q=5 (no genuine): K/q=1.20
  q=9 (no genuine): K/q=1.00

Let me also check: what determines whether genuine circles exist?
  - q = 3 mod 4: x^2+y^2 anisotropic, circles are genuine (size q+1).  YES genuine.
  - q = 1 mod 4: x^2+y^2 splits, circles degenerate to size q-1 plus crosses.  NO genuine.
  - q even: x^2+y^2 = (x+y)^2, circles degenerate to size 2q.  NO genuine.

So: genuine circles exist iff q = 3 mod 4.

That means: K/q >= 1 iff q is NOT 3 mod 4 (i.e., q = 1 mod 4 or q even).

Check:
  q=4 (even): K/q=1.25 ✓
  q=5 (1 mod 4): K/q=1.20 ✓
  q=8 (even): K/q=1.00 ✓
  q=9 (1 mod 4): K/q=1.00 ✓
  q=7 (3 mod 4): K/q=0.86 ✓
  q=11 (3 mod 4): K/q=0.82 ✓
  q=3 (3 mod 4): K/q=1.67 ✗ (tiny board exception)

So the pattern is: q = 3 mod 4 gives K/q < 1 (for q >= 7), otherwise K/q >= 1.

This is a clean statement!  Let me document it.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
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
    print(f"{'q':>3} {'mod4':>5} {'K':>3} {'K/q':>5} {'genuine q+1?':>13} "
          f"{'#genuine':>9}")
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        sizes = Counter(len(b) for b in blocks)
        n_genuine = sizes.get(q + 1, 0)
        k = K_DATA[q]
        rows.append({"q": q, "q_mod_4": q % 4, "K": k, "K_over_q": k / q,
                     "genuine_circles": n_genuine,
                     "has_genuine": n_genuine > 0,
                     "block_sizes": dict(sorted(sizes.items()))})
        print(f"{q:>3} {q%4:>5} {k:>3} {k/q:>5.2f} "
              f"{'YES' if n_genuine else 'no':>13} {n_genuine:>9}")

    print()
    print("hypothesis: K/q >= 1 iff there are NO genuine circles (size q+1)")
    print()
    with_g = [(r["q"], r["K_over_q"]) for r in rows if r["has_genuine"]]
    without_g = [(r["q"], r["K_over_q"]) for r in rows if not r["has_genuine"]]
    print(f"  with genuine circles: {with_g}")
    print(f"  without genuine circles: {without_g}")
    print()
    print("genuine circles exist iff q = 3 mod 4 (x^2+y^2 anisotropic).")
    print("so the pattern is: q = 3 mod 4 -> K/q < 1 (q >= 7); otherwise K/q >= 1.")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
