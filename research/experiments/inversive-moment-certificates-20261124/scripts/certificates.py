"""Exact verification of the moment-polynomial certificates.

All arithmetic is exact (Python integers / Fraction).  No SAT, no floating
point, no external dependencies.

Checked:
  (1) P_s(r) = -(r-(s-3))(r-(s-2))(r-s) >= 0 for every integer 0 <= r <= s,
      for s = 4 .. S_MAX.
  (2) coefficients of P_s in the basis {1, r, C(r,2), C(r,3)} equal
      (s(s-3)(s-2), -(s-3)(3s-4), 2(3s-8), -6).
  (3) for 5 <= s <= q-1, q = 9..Q_MAX: Y((s-2)q+1, q) = -q*W(s,q) < 0,
      with W(s,q) = q(s-1)(s-4) - s(s-2)(s-3) - 2.
  (4) s = 4: Y(2q+2, q) = -4(q^2-5q-2) < 0 for 6 <= q <= Q_MAX.
  (5) blocking: Q(r) = (r-1)(r-3)(r-4) >= 0 for integer r >= 1,
      and y.b at m = 2q-1 equals -2(q-8)(q-1) < 0 for 9 <= q <= Q_MAX.

Usage:
    python certificates.py [--smax 80] [--qmax 120]
"""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"


def cubic_coeffs(p: tuple[int, int, int]) -> tuple[int, int, int, int]:
    """Return (c3,c2,c1,c0) of the monic polynomial with roots p (times -1).

    We need -(r-a)(r-b)(r-c), so the returned c3 is -1.
    """
    a, b, c = p
    # (r-a)(r-b)(r-c) = r^3 - (a+b+c)r^2 + (ab+bc+ca)r - abc
    return (-1, a + b + c, -(a * b + b * c + c * a), a * b * c)


def to_basis(c3: int, c2: int, c1: int, c0: int) -> tuple[int, int, int, int]:
    """Coefficients (a0,a1,a2,a3) with p(r)=a0+a1 r+a2 C(r,2)+a3 C(r,3)."""
    a3 = 6 * c3
    a2 = 2 * c2 + a3
    a1 = c1 + c2 + c3
    a0 = c0
    return a0, a1, a2, a3


def Y_s(n: int, q: int, y: tuple[int, int, int, int]) -> int:
    a0, a1, a2, a3 = y
    return (a0 * q * (q * q + 1) + a1 * n * q * (q + 1)
            + a2 * comb(n, 2) * (q + 1) + a3 * comb(n, 3))


def verify_poly_nonneg(s: int) -> bool:
    a, b, c = s - 3, s - 2, s
    for r in range(0, s + 1):
        v = -(r - a) * (r - b) * (r - c)
        if v < 0:
            return False
    return True


def W(s: int, q: int) -> int:
    return q * (s - 1) * (s - 4) - s * (s - 2) * (s - 3) - 2


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smax", type=int, default=80)
    ap.add_argument("--qmax", type=int, default=120)
    args = ap.parse_args()
    rows = []
    # (1) nonnegativity and (2) coefficients
    for s in range(4, args.smax + 1):
        assert verify_poly_nonneg(s), s
        c = cubic_coeffs((s - 3, s - 2, s))
        y = to_basis(*c)
        assert y == (s * (s - 3) * (s - 2), -(s - 3) * (3 * s - 4),
                     2 * (3 * s - 8), -6), (s, y)
        rows.append({"s": s, "coeffs": y})
    # (3) general bound
    checks = 0
    for q in range(9, args.qmax + 1):
        for s in range(5, q):
            y = (s * (s - 3) * (s - 2), -(s - 3) * (3 * s - 4),
                 2 * (3 * s - 8), -6)
            yy = Y_s((s - 2) * q + 1, q, y)
            assert yy == -q * W(s, q), (q, s, yy, -q * W(s, q))
            assert yy < 0, (q, s, yy)
            checks += 1
    # (4) s = 4
    s4 = 0
    y4 = (8, -8, 8, -6)
    for q in range(6, args.qmax + 1):
        yy = Y_s(2 * q + 2, q, y4)
        assert yy == -4 * (q * q - 5 * q - 2), (q, yy)
        assert yy < 0, q
        s4 += 1
    # (5) blocking
    yb = (-12, 12, -10, 6)  # coefficients of (r-1)(r-3)(r-4)
    for r in range(1, args.qmax + 2):
        v = (r - 1) * (r - 3) * (r - 4)
        if v < 0:
            raise AssertionError(r)
    blk = 0
    for q in range(9, args.qmax + 1):
        m = 2 * q - 1
        yy = (yb[0] * q * (q * q + 1) + yb[1] * m * q * (q + 1)
              + yb[2] * comb(m, 2) * (q + 1) + yb[3] * comb(m, 3))
        assert yy == -2 * (q - 8) * (q - 1), (q, yy)
        assert yy < 0, q
        blk += 1
    result = {
        "experiment": "inversive-moment-certificates-20261124",
        "s_max": args.smax,
        "q_max": args.qmax,
        "nonneg_and_coeffs_checked": len(rows),
        "theorem_B_checks": checks,
        "theorem_A_checks": s4,
        "theorem_C_checks": blk,
        "status": "all exact checks passed",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "certificates.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
