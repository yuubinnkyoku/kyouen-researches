"""Structural probe: how the finite-field circle family depends on q mod 4.

Over F_q the rule "four points concyclic or collinear" is
    det[[x_i, y_i, x_i^2+y_i^2, 1]] = 0.
The quadratic part is the form Q(x,y) = x^2 + y^2.

* If -1 is a non-square mod q (q = 3 mod 4), Q is anisotropic: every circle is
  a genuine conic with q+1 points, the faithful analogue of the Euclidean case.
* If -1 is a square mod q (q = 1 mod 4), Q splits as (x+iy)(x-iy): every
  "circle" degenerates into a pair of lines and the game is a different one.

This script reports, for each q, the circle size distribution, the number of
forbidden quads, and the isotropy of Q, so the dichotomy is machine-checked
rather than asserted.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from ff_kyouen import PrimeField, ag2_points, circle_census, forbidden_quads


def is_minus_one_square(p: int) -> bool:
    return any((i * i) % p == p - 1 for i in range(p))


def line_census(p: int, points: list[tuple[int, int]]) -> dict:
    """Affine lines of AG(2,p): p(p+1) of them, each with exactly p points."""
    lines = set()
    for (x0, y0) in points:
        for (dx, dy) in [(1, 0)] + [(a, 1) for a in range(p)]:
            pts = frozenset(
                ((x0 + t * dx) % p, (y0 + t * dy) % p) for t in range(p)
            )
            lines.add(pts)
    return {"distinct_lines": len(lines), "line_size": p}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, nargs="+", default=[3, 5, 7, 11, 13])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for q in args.q:
        pts = ag2_points(q)
        quads = forbidden_quads(q, pts)
        census = circle_census(q, pts)
        lines = line_census(q, pts)
        row = {
            "q": q,
            "q_mod_4": q % 4,
            "minus_one_is_square": is_minus_one_square(q),
            "quadratic_form_anisotropic": not is_minus_one_square(q),
            "points": q * q,
            "forbidden_quads": len(quads),
            "distinct_circles": census["distinct_circles"],
            "circle_size_distribution": census["circle_size_distribution"],
            "max_circle_size": census["max_circle_size"],
            "distinct_lines": lines["distinct_lines"],
        }
        rows.append(row)
        print(
            f"q={q:3d} (mod4={q % 4}) -1 square={row['minus_one_is_square']!s:5s} "
            f"quads={len(quads):8d} circles={census['distinct_circles']:6d} "
            f"sizes={census['circle_size_distribution']}"
        )

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
