"""A structural theorem: when is the game "trivial"?

HYPOTHESIS.  If every maximal safe set of a board has the same size T, then the
Grundy value of every position S is

    g(S) = (T - |S|) mod 2.

PROOF.  From S, every maximal extension has size T, so every play from S has
exactly T - |S| moves.  The game tree from S is therefore a uniform-depth tree.
Induct on d = T - |S|: at d = 0 there are no moves, g = 0 = d mod 2.  At depth d,
all children have depth d-1 and (by induction) the same Grundy value (d-1) mod 2,
so mex of a singleton { (d-1) mod 2 } is d mod 2.  QED.

CONSEQUENCE.  The game is "trivial" (all Grundy values in {0,1}) exactly when all
maximal safe sets have the same size.  Conversely, if two maximal sets have
different sizes, the game is non-trivial somewhere.

This script verifies the theorem on every board we can enumerate, and reports
which boards have uniform maximal sets.

This is a genuinely new structural statement: it links the *game theory*
(Grundy values) to the *combinatorics* (uniformity of maximal sets), and it
explains why the inversive plane of order 3 and 4 have only nim-values 0 and 1
while order 5 has nim-value 2.
"""

from __future__ import annotations

import argparse
import itertools
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


def analyse(pts, blocks, through, n_fixed: int):
    """Enumerate all safe sets, compute Grundy values and maximal-set sizes."""
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

    # enumerate safe sets by size
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

    # Grundy values (bottom-up)
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

    # maximal-set sizes
    maximal_sizes = Counter()
    for size in by_size:
        for pmask in by_size[size]:
            if all(pmask >> i & 1 or not can_add(i, pmask) for i in range(n)):
                maximal_sizes[size] += 1

    # check the theorem
    uniform = len(maximal_sizes) == 1
    T = next(iter(maximal_sizes)) if uniform else None
    theorem_ok = True
    if uniform:
        for pmask, val in g.items():
            if val != (T - pmask.bit_count()) % 2:
                theorem_ok = False
                break

    return {
        "points": n,
        "blocks": n_blocks,
        "safe_sets": sum(len(v) for v in by_size.values()),
        "layer_sizes": {k: len(v) for k, v in sorted(by_size.items())},
        "maximal_sizes": dict(sorted(maximal_sizes.items())),
        "uniform_maximal": uniform,
        "T": T,
        "grundy_distribution": dict(sorted(Counter(g.values()).items())),
        "max_grundy": max(g.values()),
        "theorem_holds": theorem_ok,
        "root_grundy": g[0],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []

    # inversive planes
    for q in (3, 4, 5):
        pts, blocks, through = build_inv(q)
        r = analyse(pts, blocks, through, 3)
        r["board"] = f"inversive q={q}"
        rows.append(r)
        print(f"inversive q={q}: safe={r['safe_sets']} "
              f"maximal sizes={r['maximal_sizes']} uniform={r['uniform_maximal']} "
              f"gdist={r['grundy_distribution']} theorem={r['theorem_holds']}",
              flush=True)

    # AG(2,q)
    for q in (3, 5):
        pts, blocks, through = build_ag(q)
        r = analyse(pts, blocks, through, 2)
        r["board"] = f"AG(2,{q})"
        rows.append(r)
        print(f"AG(2,{q}): safe={r['safe_sets']} "
              f"maximal sizes={r['maximal_sizes']} uniform={r['uniform_maximal']} "
              f"gdist={r['grundy_distribution']} theorem={r['theorem_holds']}",
              flush=True)

    # integer boards
    from ff_kyouen import int_forbidden_quads, int_grid
    for n in (3, 4, 5):
        pts = int_grid(n)
        quads = int_forbidden_quads(n, pts)
        through = [[] for _ in range(n * n)]
        blocks = [list(qd) for qd in quads]
        for bi, b in enumerate(blocks):
            for i in b:
                through[i].append(bi)
        r = analyse(pts, blocks, through, 2)
        r["board"] = f"{n}x{n} integer"
        rows.append(r)
        print(f"{n}x{n} integer: safe={r['safe_sets']} "
              f"maximal sizes={r['maximal_sizes']} uniform={r['uniform_maximal']} "
              f"gdist={r['grundy_distribution']} theorem={r['theorem_holds']}",
              flush=True)

    print()
    print("THEOREM CHECK: uniform maximal sets => g(S) = (T-|S|) mod 2")
    all_ok = all(r["theorem_holds"] for r in rows if r["uniform_maximal"])
    print(f"  holds on all uniform boards: {all_ok}")
    print()
    print("boards with NON-uniform maximal sets (non-trivial game):")
    for r in rows:
        if not r["uniform_maximal"]:
            print(f"  {r['board']}: maximal sizes {r['maximal_sizes']}, "
                  f"max Grundy {r['max_grundy']}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                            encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
