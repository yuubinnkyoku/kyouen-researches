"""Structural analysis of the circle determinant for the D(n) upper bound.

Goal: understand why the corner family (0,0), (a,0), (t,t), (0,a) maximises
|Delta|, and reduce the general bound to a tractable statement.

Key reformulation.  Fix three points p1,p2,p3.  Expanding the 4x4 determinant
along the last row r = (x, y, x^2+y^2, 1) gives

    Delta(x,y) = alpha*x + beta*y + gamma*(x^2+y^2) + delta

with coefficients that are 3x3 minors of the first three points.  So Delta is
an affine function of (x, y, x^2+y^2): it is (up to a constant) the power of
the point (x,y) with respect to the circle through p1,p2,p3.

Consequences used here:
  * For fixed p1,p2,p3, maximising |Delta| over the integer square [0,a]^2 is a
    separable quadratic problem, so the maximum is attained on the boundary.
  * Enumerating triples and taking the max over the square reproduces D(n)
    without enumerating 4-subsets, which is much cheaper and lets us reach
    larger n.

This script verifies the coefficient formula against the direct determinant,
then computes D(n) for larger n than the 4-subset enumeration can reach.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


def det2(m) -> int:
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def det3(m) -> int:
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def det4_int(rows) -> int:
    total = 0
    for i in range(4):
        minor = [rows[j][:3] for j in range(4) if j != i]
        total += (1 if i % 2 == 0 else -1) * det3(minor)
    return total


def coeffs_for_triple(p1, p2, p3):
    """(alpha, beta, gamma, delta) with Delta(x,y) = a x + b y + c(x^2+y^2) + d.

    Expanding the 4x4 determinant along the last row r = (x, y, x^2+y^2, 1):
    the coefficient of r_j is (-1)^{3+j} times the 3x3 minor obtained by
    deleting row 4 and column j from the 4x4 matrix.  That minor is the
    determinant of the 3x3 matrix formed by the first three rows with column j
    deleted -- a 3x3 determinant, not 2x2.
    """
    # Full 4-column rows for the three fixed points.
    rows3 = [(p1[0], p1[1], p1[0] ** 2 + p1[1] ** 2, 1),
             (p2[0], p2[1], p2[0] ** 2 + p2[1] ** 2, 1),
             (p3[0], p3[1], p3[0] ** 2 + p3[1] ** 2, 1)]
    coef = []
    for j in range(4):
        # delete column j from the three fixed rows -> 3x3 minor
        minor = [[rows3[r][c] for c in range(4) if c != j] for r in range(3)]
        m = det3(minor)
        # last row is index 3; cofactor sign is (-1)^(3+j)
        coef.append((1 if (3 + j) % 2 == 0 else -1) * m)
    return coef


def max_over_square(coef, a: int):
    alpha, beta, gamma, delta = coef
    best = -1
    arg = None
    for x in range(a + 1):
        for y in range(a + 1):
            v = abs(alpha * x + beta * y + gamma * (x * x + y * y) + delta)
            if v > best:
                best, arg = v, (x, y)
    return best, arg


def verify_coeffs(n: int) -> bool:
    """Check the coefficient formula against the direct 4x4 determinant."""
    pts = [(x, y) for y in range(n) for x in range(n)]
    for tri in itertools.combinations(pts, 3):
        coef = coeffs_for_triple(*tri)
        for p4 in pts:
            if p4 in tri:
                continue
            alpha, beta, gamma, delta = coef
            x, y = p4
            pred = alpha * x + beta * y + gamma * (x * x + y * y) + delta
            rows = [(p[0], p[1], p[0] ** 2 + p[1] ** 2, 1) for p in tri] + \
                   [(x, y, x * x + y * y, 1)]
            # the expansion is exact up to the global sign convention of the
            # cofactor expansion; |Delta| is what matters for D(n)
            if abs(pred) != abs(det4_int(rows)):
                return False
    return True


def D_via_triples(n: int):
    a = n - 1
    pts = [(x, y) for y in range(n) for x in range(n)]
    best = 0
    info = None
    for tri in itertools.combinations(pts, 3):
        coef = coeffs_for_triple(*tri)
        v, arg = max_over_square(coef, a)
        if v > best:
            best, info = v, {"triple": tri, "argmax4": arg}
    return best, info


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-n", type=int, default=4)
    ap.add_argument("--n", type=int, nargs="+", default=[3, 4, 5, 6, 7, 8, 9, 10])
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    ok = verify_coeffs(args.verify_n)
    print(f"coefficient formula verified on n={args.verify_n}: {ok}", flush=True)

    report = []
    for n in args.n:
        a = n - 1
        best, info = D_via_triples(n)
        formula = a * a * ((a * a) // 2)
        report.append(
            {
                "n": n,
                "a": a,
                "D_via_triples": best,
                "formula": formula,
                "match": best == formula,
                "extremal": info,
            }
        )
        print(f"n={n:3d}: D={best:12d}  formula={formula:12d}  "
              f"{'MATCH' if best == formula else 'MISMATCH'}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
