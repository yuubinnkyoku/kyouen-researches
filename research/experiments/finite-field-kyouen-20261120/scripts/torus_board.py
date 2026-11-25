"""The torus board: the integer grid with periodic boundary conditions.

The standard board is the n x n grid with the Euclidean circle rule.  A natural
variant that keeps the integer coordinates but changes the topology is the
torus Z_n x Z_n.  Two questions arise:

(Q1) What is the right notion of "circle" on a torus?  The Euclidean circle
     x^2+y^2+Dx+Ey+F=0 is not well defined modulo n, because the quadratic
     form is not a function on Z_n (it depends on the representative).

(Q2) If we nevertheless use the same determinant with coordinates taken in
     {0,...,n-1} and reduced mod n, what game do we get, and how does it
     compare with the planar board?

This script answers (Q2) concretely: it builds the "torus rule" by declaring a
4-subset forbidden iff the determinant vanishes mod n, computes the game, and
compares with the planar board of the same size.  It also reports how many
planar forbidden quads survive and how many new ones appear, which measures how
far the torus rule is from the planar rule.

Note: the torus rule is NOT claimed to be the "correct" toroidal analogue of
the Euclidean circle.  It is one concrete, well-defined variant, reported as
such.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path


def det4_mod(rows, m: int) -> int:
    total = 0
    for i in range(4):
        minor = [rows[j][:3] for j in range(4) if j != i]
        (a, b, c), (d, e, f), (g, h, i2) = minor
        total += (1 if i % 2 == 0 else -1) * (
            a * (e * i2 - f * h) - b * (d * i2 - f * g) + c * (d * h - e * g)
        )
    return total % m


def det4_int(rows) -> int:
    total = 0
    for i in range(4):
        minor = [rows[j][:3] for j in range(4) if j != i]
        (a, b, c), (d, e, f), (g, h, i2) = minor
        total += (1 if i % 2 == 0 else -1) * (
            a * (e * i2 - f * h) - b * (d * i2 - f * g) + c * (d * h - e * g)
        )
    return total


def quads_planar(n: int):
    pts = [(x, y) for y in range(n) for x in range(n)]
    sq = [x * x + y * y for (x, y) in pts]
    out = set()
    for quad in itertools.combinations(range(n * n), 4):
        rows = [(pts[i][0], pts[i][1], sq[i], 1) for i in quad]
        if det4_int(rows) == 0:
            out.add(quad)
    return pts, out


def quads_torus(n: int):
    pts = [(x, y) for y in range(n) for x in range(n)]
    sq = [(x * x + y * y) % n for (x, y) in pts]
    out = set()
    for quad in itertools.combinations(range(n * n), 4):
        rows = [(pts[i][0], pts[i][1], sq[i], 1) for i in quad]
        if det4_mod(rows, n) == 0:
            out.add(quad)
    return pts, out


def solve(n_points: int, quads) -> dict:
    others: list[list[tuple[int, ...]]] = [[] for _ in range(n_points)]
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
        for i in range(start, n_points):
            if pmask >> i & 1:
                continue
            if can_add(i, pmask):
                stack.append((i + 1, pmask | (1 << i)))

    g: dict[int, int] = {}
    for size in sorted(by_size, reverse=True):
        for pmask in by_size[size]:
            reach = set()
            for i in range(n_points):
                if pmask >> i & 1:
                    continue
                if can_add(i, pmask):
                    reach.add(g[pmask | (1 << i)])
            m = 0
            while m in reach:
                m += 1
            g[pmask] = m

    layer = {k: len(v) for k, v in sorted(by_size.items())}
    first = Counter(g[1 << i] for i in range(n_points))
    return {
        "safe_sets": sum(layer.values()),
        "layer_sizes": layer,
        "max_safe_size": max(layer),
        "empty_grundy": g[0],
        "grundy_distribution": dict(sorted(Counter(g.values()).items())),
        "first_move_grundy": dict(sorted(first.items())),
        "winning_first_moves": sum(c for v, c in first.items() if v == 0),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="+", default=[3, 4, 5])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for n in args.n:
        pts_p, qp = quads_planar(n)
        pts_t, qt = quads_torus(n)
        assert pts_p == pts_t
        common = qp & qt
        only_planar = qp - qt
        only_torus = qt - qp
        gp = solve(n * n, qp)
        gt = solve(n * n, qt)
        row = {
            "n": n,
            "planar_quads": len(qp),
            "torus_quads": len(qt),
            "common": len(common),
            "only_planar": len(only_planar),
            "only_torus": len(only_torus),
            "planar": gp,
            "torus": gt,
        }
        rows.append(row)
        print(f"n={n}: planar quads={len(qp)} torus quads={len(qt)} "
              f"common={len(common)} only_planar={len(only_planar)} "
              f"only_torus={len(only_torus)}", flush=True)
        print(f"   planar: safe={gp['safe_sets']} K={gp['max_safe_size']} "
              f"g0={gp['empty_grundy']} wins={gp['winning_first_moves']}/{n*n}", flush=True)
        print(f"   torus : safe={gt['safe_sets']} K={gt['max_safe_size']} "
              f"g0={gt['empty_grundy']} wins={gt['winning_first_moves']}/{n*n}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
