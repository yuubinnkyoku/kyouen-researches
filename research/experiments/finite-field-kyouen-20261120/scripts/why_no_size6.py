"""Why is there no safe set of size 6 on AG(2,3)?

AG(2,3): 9 points, 30 blocks (12 lines of size 3, 18 circles of size 4).
K = 5 (verified).  The bound q+3 = 6 is not attained.

Let me enumerate ALL 6-subsets of the 9 points and check which are safe.
There are C(9,6) = 84 subsets.  For each, check whether it contains a block
with 4 points (impossible since max block size is 4, so a block with all 4
points of the subset).

Actually a block has size 3 or 4.  A 6-subset is unsafe iff it contains a
block of size 4 entirely (circles), or... wait, a line has size 3, so a
6-subset always contains a line?  Let me check: a 6-subset of a 3x3 grid.

In AG(2,3), the 12 lines are the 3 rows, 3 columns, and 6 diagonals (3 in each
of 2 directions).  A 6-subset contains a line iff some line is fully inside.

Let me just enumerate and report which 6-subsets are safe (should be none).
And for the unsafe ones, report which block is violated.
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=3)
    ap.add_argument("--size", type=int, default=6)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    pts, blocks, through, nc, nl = build_ag(args.q)
    n = len(pts)
    print(f"AG(2,{args.q}): {n} points, {len(blocks)} blocks "
          f"(circles {nc}, lines {nl})", flush=True)
    sizes = Counter(len(b) for b in blocks)
    print(f"  block sizes: {dict(sorted(sizes.items()))}", flush=True)

    safe = 0
    violation_kinds = Counter()
    for S in itertools.combinations(range(n), args.size):
        Sset = set(S)
        bad = []
        for b in blocks:
            if len(set(b) & Sset) >= 4:
                bad.append(len(b))
        if not bad:
            safe += 1
        else:
            violation_kinds[min(bad)] += 1

    print(f"  {args.size}-subsets: {len(list(itertools.combinations(range(n), args.size)))}",
          flush=True)
    print(f"  safe: {safe}", flush=True)
    print(f"  violation block sizes (min per subset): {dict(sorted(violation_kinds.items()))}",
          flush=True)

    out = {"q": args.q, "size": args.size, "safe": safe,
           "violation_kinds": dict(sorted(violation_kinds.items()))}
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(out, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
