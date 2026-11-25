"""Quantify the trade-off between |gamma| and |power|.

We have |Delta| = |gamma| * |power| and |gamma| = 2*Area <= a^2.
The naive bound |power| <= a^2/2 is FALSE; instead |power| grows as |gamma| shrinks.

This script measures the exact trade-off.  For each triple it computes
    g = |gamma|,  p = max |power| over the square,
and looks for a relation of the form

    g * p <= a^4/2      (what we want to prove)

or a sharper structural statement such as

    p <= (a^4/2) / g    i.e.  p <= a^4/(2g).

Since g = 2*Area, this is  p <= a^4/(4*Area).

Geometric meaning: the power of a point w.r.t. a circle of radius R is at most
about (distance to centre)^2 + R^2.  For a circle through three lattice points
with small area, R is large, so the power can be large -- but the product with
the area stays bounded.

This script tabulates (g, p, g*p) and checks the product bound, and also tests
the sharper conjecture  p <= a^4/(4*Area)  (equivalently g*p <= a^4/2).
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path


def det3(m) -> int:
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def coeffs(p1, p2, p3):
    rows3 = [(p1[0], p1[1], p1[0] ** 2 + p1[1] ** 2, 1),
             (p2[0], p2[1], p2[0] ** 2 + p2[1] ** 2, 1),
             (p3[0], p3[1], p3[0] ** 2 + p3[1] ** 2, 1)]
    out = []
    for j in range(4):
        minor = [[rows3[r][c] for c in range(4) if c != j] for r in range(3)]
        out.append((1 if (3 + j) % 2 == 0 else -1) * det3(minor))
    return out


def max_abs_power(coef, a: int):
    alpha, beta, gamma, delta = coef
    if gamma == 0:
        return None
    cx = Fraction(-alpha, 2 * gamma)
    cy = Fraction(-beta, 2 * gamma)
    R2 = cx * cx + cy * cy - Fraction(delta, gamma)
    best = Fraction(0)
    for (x, y) in [(0, 0), (a, 0), (0, a), (a, a)]:
        v = abs((x - cx) ** 2 + (y - cy) ** 2 - R2)
        best = max(best, v)
    px = min(max(cx, Fraction(0)), Fraction(a))
    py = min(max(cy, Fraction(0)), Fraction(a))
    v = abs((px - cx) ** 2 + (py - cy) ** 2 - R2)
    return max(best, v)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[3, 4, 5, 6])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        pts = [(x, y) for y in range(a + 1) for x in range(a + 1)]
        rows = []
        for tri in itertools.combinations(pts, 3):
            coef = coeffs(*tri)
            g = abs(coef[2])
            if g == 0:
                continue
            p = max_abs_power(coef, a)
            rows.append((g, p, g * p, tri))
        rows.sort(key=lambda r: -r[2])
        bound = Fraction(a ** 4, 2)
        worst = rows[0]
        violations = sum(1 for r in rows if r[2] > bound)
        # group by g and report max p for each g
        by_g = {}
        for g, p, gp, tri in rows:
            if g not in by_g or p > by_g[g][0]:
                by_g[g] = (p, tri)
        report.append({
            "a": a,
            "triples": len(rows),
            "product_bound": str(bound),
            "violations": violations,
            "worst_product": str(worst[2]),
            "worst_triple": list(worst[3]),
            "worst_gamma": worst[0],
            "worst_power": str(worst[1]),
            "max_p_by_gamma": {
                str(g): {"max_power": str(v[0]), "triple": list(v[1])}
                for g, v in sorted(by_g.items())
            },
        })
        print(f"a={a}: {len(rows)} triples, product bound {bound}, "
              f"violations {violations}", flush=True)
        print(f"   worst: gamma={worst[0]} power={worst[1]} product={worst[2]} "
              f"triple={worst[3]}", flush=True)
        print(f"   max power by |gamma|:", flush=True)
        for g, v in sorted(by_g.items())[:8]:
            print(f"      |gamma|={g:3d}: max|power|={v[0]}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
