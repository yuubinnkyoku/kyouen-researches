"""Exact max |det[[x,y,x^2+y^2,1]]| over 4-subsets of the n x n grid.

The determinant Delta is the integer that vanishes exactly when four grid
points are concyclic or collinear.  Its maximum absolute value D(n) is the
sharp modulus threshold below which reduction mod q can create spurious
forbidden quads (see transfer_test.py / transfer_threshold.py).

Observed values: D(2)=0, D(3)=8, D(4)=36, D(5)=128.
The extremal configuration is three corners (0,0), (a,0), (0,a) with a=n-1
plus a point (t,t) on the diagonal, for which

    Delta = -2 a^2 t (a-t),      |Delta| = 2 a^2 t (a-t),

maximised at t = a/2 (a even) or t = (a+-1)/2 (a odd), giving

    D(n) = a^2 * floor(a^2 / 2),   a = n-1.

This script checks that formula against exhaustive enumeration.
"""

from __future__ import annotations

import argparse
import itertools
import json
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


def max_abs_det(n: int) -> tuple[int, tuple | None]:
    pts = [(x, y) for y in range(n) for x in range(n)]
    sq = [x * x + y * y for (x, y) in pts]
    best = 0
    arg = None
    for quad in itertools.combinations(range(n * n), 4):
        rows = [(pts[i][0], pts[i][1], sq[i], 1) for i in quad]
        v = abs(det4_int(rows))
        if v > best:
            best = v
            arg = tuple(pts[i] for i in quad)
    return best, arg


def formula(n: int) -> int:
    a = n - 1
    return a * a * ((a * a) // 2)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="+", default=[2, 3, 4, 5, 6, 7, 8])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rows = []
    for n in args.n:
        D, arg = max_abs_det(n)
        f = formula(n)
        rows.append(
            {
                "n": n,
                "a": n - 1,
                "max_abs_determinant": D,
                "formula_a2_floor_a2_over_2": f,
                "formula_matches": D == f,
                "argmax_quad": arg,
            }
        )
        print(
            f"n={n}: D={D:9d}  formula={f:9d}  {'MATCH' if D == f else 'MISMATCH'}  "
            f"argmax={arg}",
            flush=True,
        )

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
