"""Structure of the extremal triples for the continuous relaxation.

We want to prove: for any three lattice points in [0,a]^2 and any real (x,y) in
[0,a]^2,

    |Delta(x,y)| <= a^4/2 + [a odd]/2.

The maximum over the square is attained at a corner (gamma > 0) or at a corner
or the clamped centre (gamma < 0).  This script characterises WHICH triples
attain the maximum, to guide a proof.

Key quantities for a triple:
  * gamma (the coefficient of x^2+y^2),
  * the centre (cx,cy) and R^2,
  * the value at each corner,
  * the value at the clamped centre.

We look for the structural pattern of the extremal triple.
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


def delta_at(coef, x, y):
    alpha, beta, gamma, delta = coef
    return alpha * x + beta * y + gamma * (x * x + y * y) + delta


def continuous_max(coef, a: int):
    alpha, beta, gamma, delta = coef
    corners = [(0, 0), (a, 0), (0, a), (a, a)]
    best = max(abs(delta_at(coef, x, y)) for (x, y) in corners)
    arg = None
    for (x, y) in corners:
        if abs(delta_at(coef, x, y)) == best:
            arg = (x, y)
            break
    if gamma < 0:
        cx = Fraction(-alpha, 2 * gamma)
        cy = Fraction(-beta, 2 * gamma)
        cx = min(max(cx, Fraction(0)), Fraction(a))
        cy = min(max(cy, Fraction(0)), Fraction(a))
        v = abs(delta_at(coef, cx, cy))
        if v > best:
            best, arg = v, (cx, cy)
    return best, arg


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, nargs="+", default=[3, 5, 7])
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = []
    for a in args.a:
        pts = [(x, y) for y in range(a + 1) for x in range(a + 1)]
        scored = []
        for tri in itertools.combinations(pts, 3):
            coef = coeffs(*tri)
            v, arg = continuous_max(coef, a)
            scored.append((v, tri, coef, arg))
        scored.sort(key=lambda t: -t[0])
        target = Fraction(a ** 4, 2) + (Fraction(1, 2) if a % 2 else 0)
        print(f"\na={a}: continuous max = {scored[0][0]} (formula {target})")
        print(f"  number of triples attaining the max: "
              f"{sum(1 for s in scored if s[0] == scored[0][0])}")
        for v, tri, coef, arg in scored[: args.top]:
            alpha, beta, gamma, delta = coef
            print(f"  value={v} triple={tri}")
            print(f"     gamma={gamma} argmax={arg}")
            if gamma != 0:
                cx = Fraction(-alpha, 2 * gamma)
                cy = Fraction(-beta, 2 * gamma)
                print(f"     centre=({cx},{cy})")
        report.append({
            "a": a,
            "continuous_max": str(scored[0][0]),
            "formula": str(target),
            "num_attaining": sum(1 for s in scored if s[0] == scored[0][0]),
            "top": [
                {"value": str(v), "triple": list(tri), "gamma": coef[2],
                 "argmax": [str(x) for x in arg]}
                for v, tri, coef, arg in scored[: args.top]
            ],
        })

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
