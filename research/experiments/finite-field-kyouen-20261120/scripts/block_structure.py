"""Why do genuine circles (size q+1) constrain K more than degenerate ones?

For q = 3 mod 4, circles are genuine conics of size q+1.
For q = 1 mod 4, circles degenerate into size q-1 (line pairs) plus crosses.

Key structural difference: a genuine circle of size q+1 has q+1 points, and
through any 3 of them passes exactly that circle.  A degenerate "circle" of
size q-1 is a pair of lines, so it contains many collinear triples.

Let me quantify: for a block B, how many triples of B are "collinear" (i.e.,
lie on a line) vs "genuinely concyclic"?

For a genuine circle (size q+1): no 3 points are collinear (a line meets a
circle in at most 2 points).  So all C(q+1,3) triples are genuinely concyclic.

For a degenerate circle (pair of two lines, size q-1): the two lines each have
(q+1)/2 points... wait, size q-1 total.  Let me think: a degenerate circle is
(s+a)(t+b) = 0, i.e., a column plus a row, which has 2q-1 points.  That is the
"cross", not size q-1.

Hmm, let me recheck.  For q=5: sizes {4: 100, 5: 30, 9: 25}.
  - size 4 = q-1: these are... let me check what they are.
  - size 5 = q: lines.
  - size 9 = 2q-1: crosses.

For q=9: sizes {8: 648, 9: 90, 17: 81}.
  - size 8 = q-1: ?
  - size 9 = q: lines.
  - size 17 = 2q-1: crosses.

So the size q-1 blocks are something else.  Let me investigate their structure.

A circle x^2+y^2+Dx+Ey+F=0 over F_q with -1 a square factors as
(x+iy+a)(x-iy+b) = 0, which is a pair of lines with slopes ±i.  Each line has
q points, they meet in 1 point, so the union has 2q-1 points.  That is the cross.

But the size q-1 blocks: what are they?  Maybe they are circles that are
"tangent" or have a different degeneration.

Let me just compute: for q=5, take a size-4 block and see its structure.
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
    ap.add_argument("--q", type=int, nargs="+", default=[5, 9])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        sizes = Counter(len(b) for b in blocks)
        print(f"q={q}: sizes {dict(sorted(sizes.items()))}", flush=True)
        # examine a block of size q-1
        small = [b for b in blocks if len(b) == q - 1]
        if small:
            b = small[0]
            print(f"  size q-1={q-1} block example: {[pts[i] for i in b]}",
                  flush=True)
            # check if it is a line (all collinear)?
            # compute if all points are collinear
            p0 = pts[b[0]]
            collinear = True
            for i in range(1, len(b)):
                for j in range(i + 1, len(b)):
                    p1, p2 = pts[b[i]], pts[b[j]]
                    # cross product
                    cr = ((p1[0][0] - p0[0][0]) * (p2[1][0] - p0[1][0])
                          - (p1[1][0] - p0[1][0]) * (p2[0][0] - p0[0][0]))
                    if cr % q != 0:
                        collinear = False
                        break
                if not collinear:
                    break
            print(f"    all collinear? {collinear}", flush=True)
            rows.append({"q": q, "size": q - 1, "collinear": collinear,
                         "example": [[list(p[0]), list(p[1])] for p in
                                     [pts[i] for i in b]]})

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
