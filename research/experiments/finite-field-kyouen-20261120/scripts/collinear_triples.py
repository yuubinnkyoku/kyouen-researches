"""Quantify: how many collinear triples does each block type contain?

Hypothesis: genuine circles (size q+1) contain NO collinear triples (a line
meets a circle in at most 2 points), so all their C(q+1,3) triples are
"genuinely concyclic" and each triple is uniquely determined.

Degenerate blocks (size q-1, grid-like) contain MANY collinear triples, so
their constraint is weaker: a triple on a degenerate block might also be on a
line, so the "triple -> block" map is not injective in the same way.

Let me count, for each block, the number of its triples that are collinear.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag2_prime_power import build_ag  # noqa: E402


def is_collinear(p1, p2, p3, q):
    """Check collinearity over F_q using the cross product."""
    # points are ((x,), (y,)) for prime q
    x1, y1 = p1[0][0], p1[1][0]
    x2, y2 = p2[0][0], p2[1][0]
    x3, y3 = p3[0][0], p3[1][0]
    cr = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
    return cr % q == 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[5, 7])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        pts, blocks, through, nc, nl = build_ag(q)
        sizes = Counter(len(b) for b in blocks)
        print(f"q={q}: sizes {dict(sorted(sizes.items()))}", flush=True)
        for sz in sorted(sizes):
            # sample a few blocks of this size
            sample = [b for b in blocks if len(b) == sz][:5]
            coll_counts = []
            for b in sample:
                bp = [pts[i] for i in b]
                cnt = 0
                tot = 0
                for tri in itertools.combinations(bp, 3):
                    tot += 1
                    if is_collinear(*tri, q):
                        cnt += 1
                coll_counts.append((cnt, tot))
            print(f"  size {sz} ({sizes[sz]} blocks): collinear triples in "
                  f"sample = {coll_counts}", flush=True)
            rows.append({"q": q, "size": sz, "count": sizes[sz],
                         "collinear_sample": coll_counts})

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
