"""Sharpen the triviality theorem: what exactly does non-uniformity buy?

The theorem says: uniform maximal sets => g(S) = (T-|S|) mod 2, so all Grundy
values are 0 or 1.

Question: if maximal sets have sizes in {T1 < T2 < ...}, what can we say?

Observation: a position S is maximal iff no move is legal.  Its Grundy value is
0.  So every maximal set has g = 0, regardless of its size.

Now consider a position S with a move to a maximal set of size T1 and also a
move to a maximal set of size T2 > T1.  Then S has children with g = 0 (both),
so g(S) = mex{0} = 1.  Not interesting.

Better: consider S such that ALL its children are maximal.  Then g(S) = 1.

The interesting case: S with children of Grundy values 0 and 1, giving g(S) = 2.

When does a child have g = 1?  A child S' has g = 1 iff all its children are
maximal (g=0) and it has at least one child.

So g(S) = 2 requires: some child S' of S has all children maximal, and some
other child S'' is maximal (g=0), and no child has g=2.

Let me measure, for each board, the "Grundy depth": the maximum d such that some
position has g = d.  And correlate with the spread of maximal sizes.

Conjecture: max Grundy <= (number of distinct maximal sizes) - 1?  Let me test.

For inversive q=5: maximal sizes {5,6}, 2 distinct, max Grundy 2.  Fits (2-1=1? no, 2 > 1).
Hmm, does not fit.

Let me just measure and report.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def build_ag(q: int):
    from ag2_prime_power import build_ag as _b
    pts, blocks, through, nc, nl = _b(q)
    return pts, blocks, through


def build_inv(q: int):
    from inversive_bfs import build_field, circles_bfs, projective_line
    F, sub = build_field(q)
    pts = projective_line(F)
    circles = circles_bfs(F, sub, pts)
    idx = {p: i for i, p in enumerate(pts)}
    blocks = [sorted(idx[p] for p in c) for c in circles]
    n = len(pts)
    through: list[list[int]] = [[] for _ in range(n)]
    for bi, b in enumerate(blocks):
        for i in b:
            through[i].append(bi)
    return pts, blocks, through


def analyse(pts, blocks, through):
    n = len(pts)
    n_blocks = len(blocks)

    def can_add(i: int, pmask: int) -> bool:
        for bi in through[i]:
            cnt = 0
            for j in blocks[bi]:
                if pmask >> j & 1:
                    cnt += 1
                    if cnt >= 3:
                        return False
        return True

    by_size: dict[int, list[int]] = {}
    stack = [(0, 0)]
    while stack:
        start, pmask = stack.pop()
        by_size.setdefault(pmask.bit_count(), []).append(pmask)
        for i in range(start, n):
            if pmask >> i & 1:
                continue
            if can_add(i, pmask):
                stack.append((i + 1, pmask | (1 << i)))

    g: dict[int, int] = {}
    for size in sorted(by_size, reverse=True):
        for pmask in by_size[size]:
            reach = set()
            for i in range(n):
                if pmask >> i & 1:
                    continue
                if can_add(i, pmask):
                    reach.add(g[pmask | (1 << i)])
            m = 0
            while m in reach:
                m += 1
            g[pmask] = m

    maximal_sizes = Counter()
    for size in by_size:
        for pmask in by_size[size]:
            if all(pmask >> i & 1 or not can_add(i, pmask) for i in range(n)):
                maximal_sizes[size] += 1

    # for each Grundy value, the sizes of positions attaining it
    g_by_size = defaultdict(Counter)
    for pmask, val in g.items():
        g_by_size[val][pmask.bit_count()] += 1

    return {
        "points": n,
        "safe_sets": sum(len(v) for v in by_size.values()),
        "maximal_sizes": dict(sorted(maximal_sizes.items())),
        "num_maximal_sizes": len(maximal_sizes),
        "spread": (max(maximal_sizes) - min(maximal_sizes)) if maximal_sizes else 0,
        "grundy_distribution": dict(sorted(Counter(g.values()).items())),
        "max_grundy": max(g.values()),
        "g_by_size": {k: dict(sorted(v.items())) for k, v in sorted(g_by_size.items())},
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in (3, 4, 5):
        pts, blocks, through = build_inv(q)
        r = analyse(pts, blocks, through)
        r["board"] = f"inversive q={q}"
        rows.append(r)
    for q in (3, 5):
        pts, blocks, through = build_ag(q)
        r = analyse(pts, blocks, through)
        r["board"] = f"AG(2,{q})"
        rows.append(r)
    from ff_kyouen import int_forbidden_quads, int_grid
    for n in (3, 4, 5):
        pts = int_grid(n)
        quads = int_forbidden_quads(n, pts)
        through = [[] for _ in range(n * n)]
        blocks = [list(qd) for qd in quads]
        for bi, b in enumerate(blocks):
            for i in b:
                through[i].append(bi)
        r = analyse(pts, blocks, through)
        r["board"] = f"{n}x{n} integer"
        rows.append(r)

    print(f"{'board':>18} {'maximal sizes':>22} {'#sizes':>6} {'spread':>6} "
          f"{'maxG':>5}")
    for r in rows:
        print(f"{r['board']:>18} {str(r['maximal_sizes']):>22} "
              f"{r['num_maximal_sizes']:>6} {r['spread']:>6} {r['max_grundy']:>5}")

    print()
    print("Grundy value -> sizes of positions attaining it:")
    for r in rows:
        print(f"  {r['board']}:")
        for gv, sizes in r["g_by_size"].items():
            print(f"    g={gv}: sizes {sizes}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
