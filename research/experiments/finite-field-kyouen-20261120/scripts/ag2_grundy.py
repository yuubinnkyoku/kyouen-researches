"""AG(2,q) cocircular game: exact Grundy for q = 3, 5 and structural results for q = 7.

The AG(2,q) board is F_q^2 with the rule "four points concyclic or collinear",
decided by det[[x,y,x^2+y^2,1]] = 0 over F_q.

For q = 3 (9 points) and q = 5 (25 points) the full safe-set enumeration is
feasible.  For q = 7 (49 points) it is not, so we compute:

  * the exact safe-layer counts L_k for k <= 5, using the same disjoint-event
    argument as for the inversive plane (two distinct circles meet in at most
    2 points, so two "4-on-a-circle" events need >= 6 points),
  * a greedy/local-search lower bound and a counting upper bound on K.

Note: in AG(2,q) the "blocks" are circles AND lines.  Two distinct circles meet
in at most 2 points; a circle and a line meet in at most 2 points; two lines
meet in at most 1 point.  So the same bound applies: two bad events need
>= 4+4-2 = 6 points.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
from collections import Counter
from math import comb
from pathlib import Path

from ff_structure import circles_and_lines


def build(q: int):
    pts, circles, lines = circles_and_lines(q)
    blocks = [sorted(b) for b in circles] + [sorted(b) for b in lines]
    n = len(pts)
    through: list[list[int]] = [[] for _ in range(n)]
    for bi, b in enumerate(blocks):
        for i in b:
            through[i].append(bi)
    return pts, blocks, through


def disjoint_layer(q: int, k: int) -> int:
    """Exact safe-layer count for k <= 5.

    L_k = C(n,k) - sum over blocks B of #{k-sets with >=4 points on B},
    valid when the bad events are pairwise disjoint (k <= 5).
    """
    pts, circles, lines = circles_and_lines(q)
    n = len(pts)
    total = comb(n, k)
    if k < 4:
        return total
    bad = 0
    for block in itertools.chain(circles, lines):
        s = len(block)
        if s < 4:
            continue
        per = sum(comb(s, j) * comb(n - s, k - j) for j in range(4, min(k, s) + 1))
        bad += per
    return total - bad


def counting_upper_bound(q: int) -> int:
    pts, circles, lines = circles_and_lines(q)
    b = len(circles) + len(lines)
    k = 3
    while comb(k + 1, 3) <= b:
        k += 1
    return k


def greedy_lower(q: int, rng: random.Random, trials: int) -> int:
    pts, blocks, through = build(q)
    n = len(pts)

    def can_add(i: int, pmask: int) -> bool:
        for bi in through[i]:
            cnt = 0
            for j in blocks[bi]:
                if pmask >> j & 1:
                    cnt += 1
                    if cnt >= 3:
                        return False
        return True

    best = 0
    for _ in range(trials):
        order = list(range(n))
        rng.shuffle(order)
        pmask = 0
        size = 0
        for i in order:
            if can_add(i, pmask):
                pmask |= 1 << i
                size += 1
        best = max(best, size)
    return best


def full_grundy(q: int) -> dict:
    pts, blocks, through = build(q)
    n = len(pts)

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

    layer = {k: len(v) for k, v in sorted(by_size.items())}
    first = Counter(g[1 << i] for i in range(n))
    return {
        "q": q,
        "points": n,
        "blocks": len(blocks),
        "safe_sets": sum(layer.values()),
        "layer_sizes": layer,
        "max_safe_size": max(layer),
        "empty_grundy": g[0],
        "grundy_distribution": dict(sorted(Counter(g.values()).items())),
        "max_grundy": max(Counter(g.values())),
        "first_move_grundy": dict(sorted(first.items())),
        "winning_first_moves": sum(c for v, c in first.items() if v == 0),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7])
    ap.add_argument("--trials", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20261120)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    rows = []
    for q in args.q:
        pts, circles, lines = circles_and_lines(q)
        row = {
            "q": q,
            "points": len(pts),
            "circles": len(circles),
            "lines": len(lines),
        }
        if q <= 5:
            row.update(full_grundy(q))
            print(f"q={q}: FULL safe={row['safe_sets']} K={row['max_safe_size']} "
                  f"g0={row['empty_grundy']} maxg={row['max_grundy']} "
                  f"wins={row['winning_first_moves']}/{row['points']}", flush=True)
        else:
            layers = {k: disjoint_layer(q, k) for k in range(0, 6)}
            row["layer_counts_k_le_5_exact"] = layers
            row["K_lower_greedy"] = greedy_lower(q, rng, args.trials)
            row["K_upper_counting"] = counting_upper_bound(q)
            print(f"q={q}: layers(k<=5)={layers} "
                  f"K in [{row['K_lower_greedy']}, {row['K_upper_counting']}]", flush=True)
        rows.append(row)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
