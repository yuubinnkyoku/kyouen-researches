"""Full Grundy computation on the inversive plane of order q, for small q.

For q = 3 (10 points) and q = 4 (17 points) the full safe-set enumeration is
feasible, so we can compute the complete Grundy table and the game outcome.

q = 5 (26 points) is also feasible (done in inversive_plane.py); q = 7 (50
points) is not.

This script uses the general prime-power construction so that q = 4 works.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from inversive_bfs import build_field, circles_bfs, projective_line


def build(q: int):
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


def solve(q: int) -> dict:
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
    min_maximal = None
    for size in sorted(by_size):
        for pmask in by_size[size]:
            if all(pmask >> i & 1 or not can_add(i, pmask) for i in range(n)):
                min_maximal = size
                break
        if min_maximal is not None:
            break

    gdist = Counter(g.values())
    first = Counter(g[1 << i] for i in range(n))
    return {
        "q": q,
        "points": n,
        "circles": len(blocks),
        "circle_size": len(blocks[0]),
        "safe_sets": sum(layer.values()),
        "layer_sizes": layer,
        "max_safe_size": max(layer),
        "min_maximal_size": min_maximal,
        "empty_grundy": g[0],
        "empty_outcome": "P(second-player-win)" if g[0] == 0 else "N(first-player-win)",
        "grundy_distribution": dict(sorted(gdist.items())),
        "max_grundy": max(gdist),
        "first_move_grundy": dict(sorted(first.items())),
        "winning_first_moves": sum(c for v, c in first.items() if v == 0),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 4])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        r = solve(q)
        rows.append(r)
        print(f"q={q}: points={r['points']} circles={r['circles']} "
              f"safe={r['safe_sets']} K={r['max_safe_size']} s={r['min_maximal_size']} "
              f"g(empty)={r['empty_grundy']} ({r['empty_outcome']})", flush=True)
        print(f"   layers={r['layer_sizes']}", flush=True)
        print(f"   gdist={r['grundy_distribution']} maxg={r['max_grundy']} "
              f"first={r['first_move_grundy']} wins={r['winning_first_moves']}/{r['points']}",
              flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
