"""Forbidden quads of AG(2,q) generated from circles and lines, not from 4-subsets.

A 4-subset is forbidden iff it lies on one circle or one line.  Enumerating the
q^2(q-1) circles and q(q+1) lines and taking their 4-subsets is far cheaper than
scanning all C(q^2,4) 4-subsets, and it is exact: every forbidden quad lies on
at least one such circle or line.

Circles are the board traces of x^2+y^2+Dx+Ey+F=0.  Over F_q with -1 a square
(q = 1 mod 4) these degenerate into line pairs, which is reported explicitly.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path


def circles_and_lines(q: int):
    """Return (circles, lines) as lists of frozensets of points in F_q^2."""
    pts = [(x, y) for y in range(q) for x in range(q)]
    index = {p: i for i, p in enumerate(pts)}

    circles = set()
    for D in range(q):
        for E in range(q):
            for F in range(q):
                s = frozenset(
                    index[(x, y)]
                    for (x, y) in pts
                    if (x * x + y * y + D * x + E * y + F) % q == 0
                )
                if len(s) >= 3:
                    circles.add(s)

    lines = set()
    for (x0, y0) in pts:
        for (dx, dy) in [(1, 0)] + [(a, 1) for a in range(q)]:
            s = frozenset(
                index[((x0 + t * dx) % q, (y0 + t * dy) % q)] for t in range(q)
            )
            lines.add(s)

    return pts, circles, lines


def forbidden_quads_fast(q: int):
    pts, circles, lines = circles_and_lines(q)
    quads = set()
    for block in itertools.chain(circles, lines):
        if len(block) >= 4:
            for quad in itertools.combinations(sorted(block), 4):
                quads.add(quad)
    return pts, circles, lines, sorted(quads)


def main() -> None:
    rows = []
    for q in (3, 5, 7, 11, 13, 17, 19):
        pts, circles, lines, quads = forbidden_quads_fast(q)
        csizes = Counter(len(c) for c in circles)
        rows.append(
            {
                "q": q,
                "q_mod_4": q % 4,
                "points": len(pts),
                "circles": len(circles),
                "circle_sizes": dict(sorted(csizes.items())),
                "lines": len(lines),
                "forbidden_quads": len(quads),
            }
        )
        print(
            f"q={q:3d} (mod4={q % 4}): circles={len(circles):6d} sizes={dict(sorted(csizes.items()))} "
            f"lines={len(lines):5d} quads={len(quads):9d}",
            flush=True,
        )

    Path("output").mkdir(exist_ok=True)
    Path("output/ff_structure.json").write_text(
        json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
