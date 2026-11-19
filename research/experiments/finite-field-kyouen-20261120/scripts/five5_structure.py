"""D4 orbit decomposition of the 5x5 winning first moves.

Known: on the 5x5 board the winning first moves are exactly
    W = {(2,0),(1,1),(3,1),(0,2),(2,2),(4,2),(1,3),(3,3),(2,4)}
      = {(x,y) : x+y even and |x-2|+|y-2| <= 2}
and the 16 losing first moves all have Grundy value 3.

This script:
  1. recomputes the Grundy table from scratch (independent of the other scripts),
  2. decomposes both W and its complement into D4 orbits,
  3. reports, for each orbit, the Grundy value and the number of forbidden
     quadruples through each point,
  4. checks whether the parity/distance description is exact.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path


def det4_int(rows) -> int:
    total = 0
    for i in range(4):
        minor = [rows[j][:3] for j in range(4) if j != i]
        (a, b, c), (d, e, f), (g, h, i2) = minor
        total += (1 if i % 2 == 0 else -1) * (
            a * (e * i2 - f * h) - b * (d * i2 - f * g) + c * (d * h - e * g)
        )
    return total


def forbidden_quads(n: int):
    pts = [(x, y) for y in range(n) for x in range(n)]
    sq = [x * x + y * y for (x, y) in pts]
    quads = []
    for quad in itertools.combinations(range(n * n), 4):
        rows = [(pts[i][0], pts[i][1], sq[i], 1) for i in quad]
        if det4_int(rows) == 0:
            quads.append(quad)
    return pts, quads


def grundy_table(n: int):
    pts, quads = forbidden_quads(n)
    others: list[list[tuple[int, ...]]] = [[] for _ in range(n * n)]
    for quad in quads:
        for pos, i in enumerate(quad):
            others[i].append(tuple(quad[:pos] + quad[pos + 1:]))

    def can_add(i: int, pmask: int) -> bool:
        return not any(
            (pmask >> a) & 1 and (pmask >> b) & 1 and (pmask >> c) & 1
            for (a, b, c) in others[i]
        )

    by_size: dict[int, list[int]] = {}
    stack = [(0, 0)]
    while stack:
        start, pmask = stack.pop()
        by_size.setdefault(pmask.bit_count(), []).append(pmask)
        for i in range(start, n * n):
            if pmask >> i & 1:
                continue
            if can_add(i, pmask):
                stack.append((i + 1, pmask | (1 << i)))

    g: dict[int, int] = {}
    for size in sorted(by_size, reverse=True):
        for pmask in by_size[size]:
            reach = set()
            for i in range(n * n):
                if pmask >> i & 1:
                    continue
                if can_add(i, pmask):
                    reach.add(g[pmask | (1 << i)])
            m = 0
            while m in reach:
                m += 1
            g[pmask] = m
    return pts, quads, g, others


def d4_orbit(p, n: int):
    x, y = p
    a = n - 1
    imgs = {
        (x, y), (a - x, y), (x, a - y), (a - x, a - y),
        (y, x), (a - y, x), (y, a - x), (a - y, a - x),
    }
    return frozenset(imgs)


def main() -> None:
    n = 5
    pts, quads, g, others = grundy_table(n)
    idx = {p: i for i, p in enumerate(pts)}

    first = {p: g[1 << idx[p]] for p in pts}
    win = {p for p, v in first.items() if v == 0}
    lose = {p for p, v in first.items() if v != 0}

    print(f"n={n}: forbidden quads={len(quads)}")
    print(f"winning first moves ({len(win)}): {sorted(win)}")
    print(f"losing first moves ({len(lose)}): {sorted(lose)}")
    print(f"losing Grundy values: {sorted(set(first[p] for p in lose))}")

    # parity/distance description
    pred = {(x, y) for y in range(n) for x in range(n)
            if (x + y) % 2 == 0 and abs(x - 2) + abs(y - 2) <= 2}
    print(f"\nparity+distance prediction matches W: {pred == win}")
    if pred != win:
        print(f"  pred - W = {sorted(pred - win)}")
        print(f"  W - pred = {sorted(win - pred)}")

    # D4 orbits
    seen = set()
    orbits = []
    for p in pts:
        if p in seen:
            continue
        orb = d4_orbit(p, n)
        seen |= orb
        orbits.append(orb)

    print(f"\nD4 orbits ({len(orbits)}):")
    rows = []
    for orb in sorted(orbits, key=lambda o: (len(o), sorted(o)[0])):
        vals = {first[p] for p in orb}
        nquads = {len(others[idx[p]]) for p in orb}
        kind = "WIN" if vals == {0} else ("LOSE" if 0 not in vals else "MIXED")
        rows.append({
            "orbit": sorted(orb),
            "size": len(orb),
            "grundy_values": sorted(vals),
            "quads_per_point": sorted(nquads),
            "kind": kind,
        })
        print(f"  size={len(orb)} {sorted(orb)} g={sorted(vals)} "
              f"quads/pt={sorted(nquads)} -> {kind}")

    # how many forbidden quads does each point participate in
    print("\nforbidden quads per point:")
    for p in sorted(pts):
        print(f"  {p}: {len(others[idx[p]])} quads, g({{p}})={first[p]}")

    out = {
        "n": n,
        "forbidden_quads": len(quads),
        "winning_first_moves": sorted(win),
        "losing_first_moves": sorted(lose),
        "losing_grundy_values": sorted(set(first[p] for p in lose)),
        "parity_distance_matches": pred == win,
        "d4_orbits": rows,
        "quads_per_point": {str(p): len(others[idx[p]]) for p in sorted(pts)},
    }
    Path("output").mkdir(exist_ok=True)
    Path("output/five5_structure.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("\nwrote output/five5_structure.json")


if __name__ == "__main__":
    main()
