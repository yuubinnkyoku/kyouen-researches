"""Extract explicit multiplier certificates for the 3-moment bound.

For an s-arc of size n in M(q), any multiplier

    P(r) = a0 + a1 r + a2 C(r,2) + a3 C(r,3)

with P(r) >= 0 for every achievable r = 0..s gives

    Y_P(n,q) = a0 q(q^2+1) + a1 n q(q+1) + a2 C(n,2)(q+1) + a3 C(n,3) >= 0,

because Y_P = sum_r P(r) t_r and t_r >= 0.  So Y_P < 0 rules out n.

This script, for each (s,q), finds the largest n the method cannot rule out
(exact rational LP, `moment_lp.py`) and then emits an explicit certificate for
n+1: the coefficient vector a and the check that P >= 0 on 0..s and Y_P < 0.
The certificate is checked again with independent Fraction arithmetic.

Usage:
    python moment_certificate.py --s 5 6 7 8 --q 9 11 13 16 [--out ...]
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(HERE))
from moment_lp import C, column, feasible, moment_bound, rhs, solve_exact  # noqa: E402


def certificate(s: int, n: int, q: int) -> list[Fraction] | None:
    """Find a = (a0..a3) with P >= 0 on 0..s and Y_P(n,q) = -1."""
    b = [Fraction(v) for v in rhs(n, q)]
    for combo in itertools.combinations(range(s + 1), 3):
        mat = [[Fraction(v) for v in column(r)] for r in combo]
        mat = mat + [[Fraction(v) for v in b]]  # 3 rows P(r)=0, then Y=-1
        sol = solve_exact(mat, [Fraction(0)] * 3 + [Fraction(-1)])
        if sol is None:
            continue
        # independent re-check: P(r) >= 0 on 0..s and Y < 0
        ok = all(sum(sol[j] * Fraction(column(r)[j]) for j in range(4)) >= 0
                 for r in range(s + 1))
        y = sum(sol[j] * Fraction(b[j]) for j in range(4))
        if ok and y == -1:
            return sol
    return None


def run(s: int, q: int) -> dict:
    hi = min(q * q + 1, (s - 2) * (q + 1) + 3)
    n = hi
    while n > 0 and not feasible(s, n, q)[0]:
        n -= 1
    bound = n
    cert = certificate(s, n + 1, q) if n + 1 <= q * q + 1 else None
    return {"s": s, "q": q, "lp_bound": bound,
            "theorem_bound": (s - 2) * (q + 1) + 2,
            "closed_form_K1291": (s - 2) * q if s <= q - 1 else None,
            "certificate_n": n + 1,
            "certificate": [str(v) for v in cert] if cert else None,
            "certificate_ok": cert is not None}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--s", type=int, nargs="+", required=True)
    ap.add_argument("--q", type=int, nargs="+", required=True)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    rows = []
    for s in args.s:
        for q in args.q:
            if not (3 <= s <= q + 1):
                continue
            row = run(s, q)
            rows.append(row)
            print(json.dumps(row), flush=True)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rows, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
