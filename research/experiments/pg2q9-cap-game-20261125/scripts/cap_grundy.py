"""Grundy value of a cap in PG(2,9) by a full DP over its upset.

The upset of a small cap (all caps containing it) is small: 31,681 positions for
a 3-cap, 1,868 for a 4-cap.  Since PGL(3,9) is transitive on 3-caps and on
4-caps, the value computed here is the value of every cap of that size.

Usage:
    python cap_grundy.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def load(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    n, b = map(int, lines[0].split())
    return n, [tuple(map(int, l.split()[1:])) for l in lines[1:]]


def solve(n, blocks, S):
    pc = [[] for _ in range(n)]
    for c, B in enumerate(blocks):
        for p in B:
            pc[p].append(c)
    used = [False] * n
    counts = [0] * len(blocks)
    for p in S:
        used[p] = True
        for c in pc[p]:
            counts[c] += 1
    order = []

    def rec(mask: int, size: int, start: int) -> None:
        order.append(mask)
        for p in range(start, n):
            if used[p]:
                continue
            if all(counts[c] < 2 for c in pc[p]):
                used[p] = True
                for c in pc[p]:
                    counts[c] += 1
                rec(mask | (1 << p), size + 1, p + 1)
                for c in pc[p]:
                    counts[c] -= 1
                used[p] = False

    rec(sum(1 << p for p in S), len(S), 0)
    g = {}
    for mask in sorted(order, key=lambda m: -m.bit_count()):
        ch = set()
        for p in range(n):
            if (mask >> p) & 1:
                continue
            nm = mask | (1 << p)
            if nm in g:
                ch.add(g[nm])
        v = 0
        while v in ch:
            v += 1
        g[mask] = v
    by_size = Counter(m.bit_count() for m in order)
    return g[sum(1 << p for p in S)], dict(sorted(by_size.items())), len(order)


def main() -> None:
    n, blocks = load(OUT / "board_pg2q9.txt")
    res = {}
    for k, S in [(3, [0, 1, 10]), (4, [0, 1, 10, 20])]:
        G, sizes, total = solve(n, blocks, S)
        res[str(k)] = {"cap": S, "grundy": G, "upset_sizes": sizes,
                       "upset_positions": total}
        print(k, G, sizes, total)
    (OUT / "small_cap_grundy.json").write_text(json.dumps(res, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
