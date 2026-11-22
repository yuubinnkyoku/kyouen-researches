"""K(q): the leading term of #k-arcs, derived symbolically.

The closed forms are

    #4 = C(n,4) - b*C(s,4)
    #5 = C(n,5) - b*C(s,5) - b*C(s,4)*(n-s)

with n = q^2+1, b = q(q^2+1), s = q+1.

Let me expand these symbolically (exact rational arithmetic on polynomials
in q) and read off the leading coefficient.  If the leading coefficient is
POSITIVE, then #k-arcs > 0 for large q, so K >= k for large q.  If it is
NEGATIVE, #k-arcs < 0 for large q, which is impossible -- meaning the
closed form must break down (it is only valid while the profile
classification is complete).

Run:  python k_leading_symbolic.py
"""

from __future__ import annotations

import json
from fractions import Fraction
from math import comb
from pathlib import Path


def poly_mul(a, b):
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def poly_add(a, b):
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i, x in enumerate(a):
        out[i] += x
    for i, y in enumerate(b):
        out[i] += y
    return out


def poly_scale(a, c):
    return [x * c for x in a]


def poly_pow(a, e):
    out = [Fraction(1)]
    for _ in range(e):
        out = poly_mul(out, a)
    return out


def binom_poly(a, k):
    """C(a, k) as a polynomial, where a is a polynomial."""
    out = [Fraction(1)]
    for i in range(k):
        out = poly_mul(out, poly_add(a, [Fraction(-i)]))
    return poly_scale(out, Fraction(1, comb(k, k) if False else 1) / _fact(k))


def _fact(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def main() -> None:
    # n = q^2 + 1
    n = [Fraction(1), Fraction(0), Fraction(1)]      # 1 + q^2
    # s = q + 1
    s = [Fraction(1), Fraction(1)]
    # b = q(q^2+1) = q + q^3
    b = [Fraction(0), Fraction(1), Fraction(0), Fraction(1)]

    rows = []
    print("=== leading terms of the closed forms ===")
    for k in (4, 5):
        Cn = binom_poly(n, k)
        term = poly_scale(poly_mul(b, binom_poly(s, k)), Fraction(-1))
        if k == 5:
            extra = poly_scale(
                poly_mul(poly_mul(b, binom_poly(s, 4)),
                         poly_add(n, [Fraction(-1), Fraction(1)])),
                Fraction(-1))
            # (n - s) = (q^2+1) - (q+1) = q^2 - q
            extra = poly_scale(
                poly_mul(poly_mul(b, binom_poly(s, 4)),
                         [Fraction(0), Fraction(-1), Fraction(1)]),
                Fraction(-1))
            term = poly_add(term, extra)
        total = poly_add(Cn, term)
        # trim
        while len(total) > 1 and total[-1] == 0:
            total.pop()
        deg = len(total) - 1
        lead = total[-1]
        rows.append({"k": k, "degree": deg, "leading": str(lead),
                     "coeffs": [str(c) for c in total]})
        print(f"  k={k}: degree {deg}, leading coeff {lead}")
        print(f"       full: {[str(c) for c in total]}")

    print()
    print("=== interpretation ===")
    print("  A positive leading coefficient means #k-arcs > 0 for large q,")
    print("  so K >= k for large q.  A negative one would be impossible.")

    out = Path(__file__).resolve().parent.parent / "output" / "k_leading_symbolic.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
