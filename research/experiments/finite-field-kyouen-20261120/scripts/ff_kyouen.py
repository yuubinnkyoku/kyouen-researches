"""Finite-field analogue of the complete-call cocircular game.

Board: AG(2,q) = F_q^2 (q an odd prime power).
Forbidden: four distinct points that are concyclic or collinear, decided by
    det[[x_i, y_i, x_i^2+y_i^2, 1]] = 0   over F_q
which is the exact same polynomial as the integer-grid rule of K0001.

The script enumerates all safe sets incrementally, computes Grundy values by
mex, and reports structural invariants so that the finite-field board can be
compared with the integer n x n board.

Only odd q are handled: in characteristic 2 the quadratic form x^2+y^2
degenerates to (x+y)^2 and the "circle" family is no longer the Euclidean one.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path


# ---------------------------------------------------------------- field ops


class PrimeField:
    """F_p for an odd prime p, with exact integer representatives."""

    def __init__(self, p: int) -> None:
        if p < 3 or any(p % d == 0 for d in range(2, int(p**0.5) + 1)):
            raise ValueError(f"p={p} is not an odd prime")
        self.p = p

    def det4(self, rows: list[tuple[int, int, int, int]]) -> int:
        """4x4 determinant over F_p, expanded along the all-ones column."""
        total = 0
        for i in range(4):
            minor = [rows[j][:3] for j in range(4) if j != i]
            total += (1 if i % 2 == 0 else -1) * self.det3(minor)
        return total % self.p

    def det3(self, rows: list[tuple[int, int, int]]) -> int:
        (a, b, c), (d, e, f), (g, h, i) = rows
        return (a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)) % self.p


# ---------------------------------------------------------------- geometry


def ag2_points(p: int) -> list[tuple[int, int]]:
    return [(x, y) for y in range(p) for x in range(p)]


def forbidden_quads(p: int, points: list[tuple[int, int]]) -> list[tuple[int, ...]]:
    """All 4-subsets of points that are concyclic or collinear over F_p."""
    F = PrimeField(p)
    sq = {(x, y): (x * x + y * y) % p for (x, y) in points}
    quads = []
    for quad in itertools.combinations(range(len(points)), 4):
        rows = [(points[i][0], points[i][1], sq[points[i]], 1) for i in quad]
        if F.det4(rows) == 0:
            quads.append(quad)
    return quads


def circle_census(p: int, points: list[tuple[int, int]]) -> dict:
    """Count distinct circles (as point sets) and their size distribution.

    A circle is the board trace of one solution set of
    x^2+y^2+Dx+Ey+F=0.  All (D,E,F) in F_p^3 are enumerated and deduplicated.
    """
    seen: dict[frozenset, tuple[int, int, int]] = {}
    for D in range(p):
        for E in range(p):
            for F in range(p):
                pts = frozenset(
                    (x, y)
                    for (x, y) in points
                    if (x * x + y * y + D * x + E * y + F) % p == 0
                )
                if len(pts) >= 3 and pts not in seen:
                    seen[pts] = (D, E, F)
    sizes = Counter(len(s) for s in seen)
    return {
        "distinct_circles": len(seen),
        "circle_size_distribution": dict(sorted(sizes.items())),
        "max_circle_size": max(sizes) if sizes else 0,
    }


# ---------------------------------------------------------------- game


def build_quad_index(n: int, quads: list[tuple[int, ...]]):
    """For each point i, the list of the other-three-index tuples of quads at i."""
    others: list[list[tuple[int, ...]]] = [[] for _ in range(n)]
    for quad in quads:
        for pos, i in enumerate(quad):
            others[i].append(tuple(quad[:pos] + quad[pos + 1:]))
    return others


def enumerate_safe(n: int, others) -> dict[int, list[int]]:
    """All safe sets, grouped by size.  Each set is produced exactly once."""
    by_size: dict[int, list[int]] = {}
    stack = [(0, 0)]
    while stack:
        start, pmask = stack.pop()
        by_size.setdefault(pmask.bit_count(), []).append(pmask)
        for i in range(start, n):
            if pmask & (1 << i):
                continue
            if any(
                (pmask >> a) & 1 and (pmask >> b) & 1 and (pmask >> c) & 1
                for (a, b, c) in others[i]
            ):
                continue
            stack.append((i + 1, pmask | (1 << i)))
    return by_size


def solve(n: int, quads: list[tuple[int, ...]]) -> dict:
    others = build_quad_index(n, quads)
    by_size = enumerate_safe(n, others)

    g: dict[int, int] = {}
    for size in sorted(by_size, reverse=True):
        for pmask in by_size[size]:
            reach = set()
            for i in range(n):
                if pmask & (1 << i):
                    continue
                if any(
                    (pmask >> a) & 1 and (pmask >> b) & 1 and (pmask >> c) & 1
                    for (a, b, c) in others[i]
                ):
                    continue
                reach.add(g[pmask | (1 << i)])
            m = 0
            while m in reach:
                m += 1
            g[pmask] = m

    layer_sizes = {k: len(v) for k, v in sorted(by_size.items())}
    max_size = max(layer_sizes)

    min_maximal = None
    for size in sorted(by_size):
        for pmask in by_size[size]:
            if all(
                pmask & (1 << i)
                or any(
                    (pmask >> a) & 1 and (pmask >> b) & 1 and (pmask >> c) & 1
                    for (a, b, c) in others[i]
                )
                for i in range(n)
            ):
                min_maximal = size
                break
        if min_maximal is not None:
            break

    gdist = Counter(g.values())
    first_move_g = Counter(g[1 << i] for i in range(n))
    return {
        "points": n,
        "forbidden_quads": len(quads),
        "safe_sets": sum(layer_sizes.values()),
        "layer_sizes": layer_sizes,
        "max_safe_size": max_size,
        "min_maximal_size": min_maximal,
        "empty_grundy": g[0],
        "empty_outcome": "P(second-player-win)" if g[0] == 0 else "N(first-player-win)",
        "grundy_distribution": dict(sorted(gdist.items())),
        "max_grundy": max(gdist),
        "first_move_grundy_distribution": dict(sorted(first_move_g.items())),
        "first_moves_winning": sum(c for v, c in first_move_g.items() if v == 0),
    }


# ---------------------------------------------------------------- integer grid


def int_grid(n: int) -> list[tuple[int, int]]:
    return [(x, y) for y in range(n) for x in range(n)]


def int_forbidden_quads(n: int, points: list[tuple[int, int]]) -> list[tuple[int, ...]]:
    quads = []
    for quad in itertools.combinations(range(len(points)), 4):
        rows = [(points[i][0], points[i][1], points[i][0] ** 2 + points[i][1] ** 2, 1)
                for i in quad]
        if _int_det4(rows) == 0:
            quads.append(quad)
    return quads


def _int_det4(rows) -> int:
    total = 0
    for i in range(4):
        minor = [rows[j][:3] for j in range(4) if j != i]
        total += (1 if i % 2 == 0 else -1) * _int_det3(minor)
    return total


def _int_det3(rows) -> int:
    (a, b, c), (d, e, f), (g, h, i) = rows
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7])
    ap.add_argument("--int-n", type=int, nargs="+", default=[3, 4, 5])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    result: dict = {"finite_field": {}, "integer_grid": {}}

    for q in args.q:
        pts = ag2_points(q)
        quads = forbidden_quads(q, pts)
        census = circle_census(q, pts)
        game = solve(q * q, quads)
        result["finite_field"][f"AG(2,{q})"] = {**census, **game}
        print(f"AG(2,{q}): {game['safe_sets']} safe sets, K={game['max_safe_size']}, "
              f"s={game['min_maximal_size']}, g(empty)={game['empty_grundy']}, "
              f"quads={game['forbidden_quads']}, circles={census['distinct_circles']}, "
              f"maxcircle={census['max_circle_size']}")

    for n in args.int_n:
        pts = int_grid(n)
        quads = int_forbidden_quads(n, pts)
        game = solve(n * n, quads)
        result["integer_grid"][f"{n}x{n}"] = game
        print(f"{n}x{n}: {game['safe_sets']} safe sets, K={game['max_safe_size']}, "
              f"s={game['min_maximal_size']}, g(empty)={game['empty_grundy']}, "
              f"quads={game['forbidden_quads']}")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
