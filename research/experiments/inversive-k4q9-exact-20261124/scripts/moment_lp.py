"""Exact optimum of the 3-moment (Delsarte/Farkas) bound for s-arcs.

An s-arc S (|S| = n) of the inversive plane has circle-intersection numbers
t_r (r = 0..s) satisfying the four moment equations

    (M1) sum_r t_r        = q(q^2+1)
    (M2) sum_r r t_r      = n q(q+1)
    (M3) sum_r C(r,2) t_r = C(n,2)(q+1)
    (M4) sum_r C(r,3) t_r = C(n,3)

with t_r >= 0.  K1291's Farkas argument is the dual view: a multiplier P with
P(r) >= 0 on 0..s and Y_P(n,q) < 0 rules out n.  By LP duality this method
gives its best bound at n exactly when the primal system above is infeasible,
so the boundary of the method is decided by the exact rational feasibility of

    { t >= 0 : A t = b(n,q) },   A[r][j] = (1, r, C(r,2), C(r,3))[j].

By Caratheodory (A has rank 4) the system is feasible iff b lies in the cone
spanned by at most 4 columns, so feasibility is decided by enumerating all
4-column subsets and solving exactly over Fraction.  No floating point and no
LP library is involved.

Usage:
    python moment_lp.py --s 4 --q 4 5 7 8 9 11 13 [--out output/moment_lp.json]
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path


def C(n: int, k: int) -> int:
    if k < 0 or n < k:
        return 0
    out = 1
    for i in range(k):
        out = out * (n - i) // (i + 1)
    return out


def column(r: int) -> tuple[int, int, int, int]:
    return (1, r, C(r, 2), C(r, 3))


def rhs(n: int, q: int) -> tuple[int, int, int, int]:
    return (q * (q * q + 1), n * q * (q + 1), C(n, 2) * (q + 1), C(n, 3))


def solve_exact(mat: list[list[Fraction]], vec: list[Fraction]) -> list[Fraction] | None:
    """Solve a square rational system; None if singular."""
    k = len(mat)
    a = [row[:] + [vec[i]] for i, row in enumerate(mat)]
    for col in range(k):
        piv = next((i for i in range(col, k) if a[i][col] != 0), None)
        if piv is None:
            return None
        a[col], a[piv] = a[piv], a[col]
        pv = a[col][col]
        a[col] = [v / pv for v in a[col]]
        for i in range(k):
            if i != col and a[i][col] != 0:
                f = a[i][col]
                a[i] = [a[i][j] - f * a[col][j] for j in range(k + 1)]
    return [a[i][k] for i in range(k)]


def feasible(s: int, n: int, q: int) -> tuple[bool, list[Fraction] | None]:
    b = [Fraction(v) for v in rhs(n, q)]
    for combo in itertools.combinations(range(s + 1), 4):
        mat = [[Fraction(column(r)[i]) for r in combo] for i in range(4)]
        sol = solve_exact(mat, b)
        if sol is None or any(v < 0 for v in sol):
            continue
        # exact re-check that the solution reproduces b
        if all(sum(sol[j] * column(combo[j])[i] for j in range(4)) == b[i]
               for i in range(4)):
            return True, sol
    return False, None


def moment_bound(s: int, q: int, hi: int) -> dict:
    n = hi
    while n > 0 and not feasible(s, n, q)[0]:
        n -= 1
    return {"s": s, "q": q, "moment_bound": n,
            "theorem_bound": (s - 2) * (q + 1) + 2}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--s", type=int, nargs="+", required=True)
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    rows = []
    for s in args.s:
        for q in args.q:
            if s > q + 1:
                continue
            hi = min(q * q + 1, (s - 2) * (q + 1) + 3)
            row = moment_bound(s, q, hi)
            rows.append(row)
            print(json.dumps(row), flush=True)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
