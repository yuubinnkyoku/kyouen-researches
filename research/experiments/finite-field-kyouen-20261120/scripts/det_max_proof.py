"""Proof attempt: the exact maximum of |det[[x,y,x^2+y^2,1]]| on the n x n grid.

Claim.  For the n x n grid with a = n-1,

    D(n) := max |Delta| = a^2 * floor(a^2 / 2),

attained by the three corners (0,0), (a,0), (0,a) together with a diagonal
point (t,t), where

    Delta = -2 a^2 t (a - t).

This script does two things.

(1) It verifies the closed form for the extremal family exactly, for many a.
(2) It runs an exhaustive check of the claim for n <= 7 (already done in
    det_threshold.py) and a *randomised* check for larger n, where exhaustive
    enumeration of C(n^2,4) is infeasible.

The randomised part is evidence, not proof.  The proof obligation that remains
is: show that no other 4-point configuration exceeds the corner family.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
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


def corner_family_det(a: int, t: int) -> int:
    """Delta for (0,0), (a,0), (t,t), (0,a)."""
    rows = [(0, 0, 0, 1), (a, 0, a * a, 1), (t, t, 2 * t * t, 1), (0, a, a * a, 1)]
    return det4_int(rows)


def formula(a: int) -> int:
    return a * a * ((a * a) // 2)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-a", type=int, default=40)
    ap.add_argument("--random-n", type=int, nargs="+", default=[8, 10, 12, 16, 20])
    ap.add_argument("--samples", type=int, default=400000)
    ap.add_argument("--seed", type=int, default=20261120)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    report = {"corner_family": [], "random_search": []}

    # (1) exact check of the extremal family
    print("(1) corner family: Delta = -2 a^2 t (a-t), max over t equals a^2*floor(a^2/2)")
    ok_all = True
    for a in range(1, args.verify_a + 1):
        best = 0
        best_t = None
        for t in range(a + 1):
            v = abs(corner_family_det(a, t))
            if v > best:
                best, best_t = v, t
        f = formula(a)
        ok = best == f
        ok_all &= ok
        report["corner_family"].append(
            {"a": a, "max_over_t": best, "argmax_t": best_t, "formula": f, "match": ok}
        )
        if a <= 12 or not ok:
            print(f"   a={a:3d}: max|Delta|={best:12d} at t={best_t}  formula={f:12d} "
                  f"{'OK' if ok else 'MISMATCH'}", flush=True)
    print(f"   all a in 1..{args.verify_a}: {'MATCH' if ok_all else 'MISMATCH'}")

    # (2) randomised search for larger n
    print("\n(2) randomised search on larger boards (evidence, not proof)")
    rng = random.Random(args.seed)
    for n in args.random_n:
        a = n - 1
        pts = [(x, y) for y in range(n) for x in range(n)]
        sq = [x * x + y * y for (x, y) in pts]
        best = 0
        best_quad = None
        for _ in range(args.samples):
            quad = rng.sample(range(n * n), 4)
            rows = [(pts[i][0], pts[i][1], sq[i], 1) for i in quad]
            v = abs(det4_int(rows))
            if v > best:
                best, best_quad = v, tuple(pts[i] for i in quad)
        f = formula(a)
        report["random_search"].append(
            {
                "n": n,
                "a": a,
                "samples": args.samples,
                "best_found": best,
                "best_quad": best_quad,
                "formula": f,
                "exceeds_formula": best > f,
            }
        )
        print(f"   n={n:3d}: best found={best:14d}  formula={f:14d}  "
              f"{'EXCEEDS!' if best > f else 'within formula'}", flush=True)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
