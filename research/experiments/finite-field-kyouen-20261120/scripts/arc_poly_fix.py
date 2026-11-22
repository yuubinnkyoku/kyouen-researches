"""Correctly derive the arc-count polynomials, respecting parity.

BUGS FOUND:
  1. The #5 coefficients recorded earlier were mis-transcribed
     (q^4, q^5, q^6, q^7, q^8 were wrong).
  2. The #6 polynomial was interpolated from q=3,5,7,...,27 (all ODD) but
     then verified against ALL q including even ones -- and it failed from
     q=16 on.  That is expected: the N_xy split is parity-dependent, so
     the odd-q polynomial is only valid for odd q.

CORRECT APPROACH:
  - #4 and #5 have NO parity dependence (their closed forms do not use
    N_xy), so a single polynomial works for all q.
  - #6 DOES depend on parity, so we need two polynomials: one for odd q,
    one for even q.

For even q we need 13 points but only have q = 4, 8, 16 (and 2 is
degenerate).  So the even-q #6 polynomial is NOT determinable from
available data.

Run:  python arc_poly_fix.py
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arc_k6_pure import arcs6  # noqa: E402


def closed(q: int, k: int):
    n = q * q + 1
    b = q * (q * q + 1)
    s = q + 1
    if k == 4:
        return comb(n, 4) - b * comb(s, 4)
    if k == 5:
        return comb(n, 5) - b * comb(s, 5) - b * comb(s, 4) * (n - s)
    if k == 6:
        val, _ = arcs6(q)
        return int(val)
    return None


def interpolate(xs, ys):
    m = len(xs)
    A = [[Fraction(x) ** j for j in range(m)] for x in xs]
    B = [Fraction(y) for y in ys]
    for c in range(m):
        piv = None
        for r in range(c, m):
            if A[r][c] != 0:
                piv = r
                break
        if piv is None:
            return None
        A[c], A[piv] = A[piv], A[c]
        B[c], B[piv] = B[piv], B[c]
        inv = 1 / A[c][c]
        A[c] = [v * inv for v in A[c]]
        B[c] *= inv
        for r in range(m):
            if r == c or A[r][c] == 0:
                continue
            f = A[r][c]
            A[r] = [A[r][k] - f * A[c][k] for k in range(m)]
            B[r] -= f * B[c]
    return B


def ev(coef, q):
    return sum(c * Fraction(q) ** i for i, c in enumerate(coef))


def poly_div(a, b):
    a = list(a)
    b = list(b)
    while len(b) > 1 and b[-1] == 0:
        b.pop()
    q = [Fraction(0)] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b):
        while len(a) > 1 and a[-1] == 0:
            a.pop()
        if len(a) < len(b):
            break
        d = len(a) - len(b)
        c = a[-1] / b[-1]
        q[d] = c
        for i in range(len(b)):
            a[d + i] -= c * b[i]
        while len(a) > 1 and a[-1] == 0:
            a.pop()
    if any(x != 0 for x in a):
        return None
    while len(q) > 1 and q[-1] == 0:
        q.pop()
    return q


CANDS = [
    ("q", [Fraction(0), Fraction(1)]),
    ("(q-1)", [Fraction(-1), Fraction(1)]),
    ("(q+1)", [Fraction(1), Fraction(1)]),
    ("(q-2)", [Fraction(-2), Fraction(1)]),
    ("(q-3)", [Fraction(-3), Fraction(1)]),
    ("(q^2+1)", [Fraction(1), Fraction(0), Fraction(1)]),
    ("(q^2-q+1)", [Fraction(1), Fraction(-1), Fraction(1)]),
    ("(q^2+q+1)", [Fraction(1), Fraction(1), Fraction(1)]),
    ("(q^2-1)", [Fraction(-1), Fraction(0), Fraction(1)]),
]


def main() -> None:
    results = {}

    # --- k=4,5: no parity dependence, single polynomial ---
    for k in (4, 5):
        deg = 2 * k
        xs = list(range(3, 3 + deg + 1))
        ys = [closed(q, k) for q in xs]
        coef = interpolate(xs, ys)
        while len(coef) > 1 and coef[-1] == 0:
            coef.pop()
        bad = [q for q in range(3, 60) if ev(coef, q) != closed(q, k)]
        print(f"=== k={k}: degree {len(coef)-1}, "
              f"verified q=3..59: {'ALL OK' if not bad else f'FAIL {bad[:3]}'}")
        print("  coefficients:")
        for i, c in enumerate(coef):
            if c != 0:
                print(f"    q^{i}: {c}")
        cur = list(coef)
        factors = []
        for name, f in CANDS:
            while True:
                qq = poly_div(cur, f)
                if qq is None:
                    break
                factors.append(name)
                cur = qq
        print(f"  factors: {factors}")
        print(f"  remainder degree {len(cur)-1}: {[str(x) for x in cur]}")
        print()
        results[k] = {"coeffs": [str(c) for c in coef],
                      "factors": factors,
                      "remainder": [str(x) for x in cur],
                      "parity": "none"}

    # --- k=6: parity dependent ---
    deg = 12
    odd_xs = [3 + 2 * i for i in range(deg + 1)]
    odd_ys = [closed(q, 6) for q in odd_xs]
    odd_coef = interpolate(odd_xs, odd_ys)
    while len(odd_coef) > 1 and odd_coef[-1] == 0:
        odd_coef.pop()
    bad_odd = [q for q in range(3, 60, 2) if ev(odd_coef, q) != closed(q, 6)]
    print(f"=== k=6 (ODD q): degree {len(odd_coef)-1}, "
          f"verified odd q=3..59: {'ALL OK' if not bad_odd else f'FAIL {bad_odd[:3]}'}")
    print("  coefficients:")
    for i, c in enumerate(odd_coef):
        if c != 0:
            print(f"    q^{i}: {c}")
    cur = list(odd_coef)
    factors = []
    for name, f in CANDS:
        while True:
            qq = poly_div(cur, f)
            if qq is None:
                break
            factors.append(name)
            cur = qq
    print(f"  factors: {factors}")
    print(f"  remainder degree {len(cur)-1}: {[str(x) for x in cur]}")
    print()
    results[6] = {"coeffs": [str(c) for c in odd_coef],
                  "factors": factors,
                  "remainder": [str(x) for x in cur],
                  "parity": "odd only"}

    print("=== k=6 (EVEN q): NOT determinable ===")
    print("  even q available: 4, 8, 16 (3 points); degree 12 needs 13.")
    print("  The odd-q polynomial does NOT apply to even q.")

    out = Path(__file__).resolve().parent.parent / "output" / "arc_poly_fix.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
