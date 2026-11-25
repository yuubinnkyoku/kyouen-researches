"""Factor the #5 and #6 remainders more aggressively.

#5 remainder (after pulling out q^3 (q-1)):
    R5 = -1/24 + q/12 - q^2/24 + q^4/120 - q^5/30 + q^6/120
    = (1/120)(-5 + 10q - 5q^2 + q^4 - 4q^5 + q^6)

#6 remainder (after pulling out q^2 (q-1)^2 (q+1) (q^2+1)):
    R6 = -1/48 + 37q/144 - 21q^2/80 + 19q^3/180 - 7q^4/360 + q^5/720
    = (1/720)(-15 + 185q - 189q^2 + 76q^3 - 14q^4 + q^5)

Let me try to factor the integer polynomials

    P5 = q^6 - 4q^5 + q^4 - 5q^2 + 10q - 5
    P6 = q^5 - 14q^4 + 76q^3 - 189q^2 + 185q - 15

over the rationals by testing small integer roots and quadratic factors.

Run:  python arc_factor2.py
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


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


def ev(coef, x):
    return sum(c * Fraction(x) ** i for i, c in enumerate(coef))


def main() -> None:
    P5 = [Fraction(-5), Fraction(10), Fraction(-5), Fraction(0),
          Fraction(1), Fraction(-4), Fraction(1)]
    P6 = [Fraction(-15), Fraction(185), Fraction(-189), Fraction(76),
          Fraction(-14), Fraction(1)]

    print("=== P5 = q^6 - 4q^5 + q^4 - 5q^2 + 10q - 5 ===")
    print("  rational roots (integer divisors of 5):")
    for r in (1, -1, 5, -5):
        print(f"    P5({r}) = {ev(P5, r)}")

    print()
    print("=== P6 = q^5 - 14q^4 + 76q^3 - 189q^2 + 185q - 15 ===")
    print("  rational roots (integer divisors of 15):")
    for r in (1, -1, 3, -3, 5, -5, 15, -15):
        print(f"    P6({r}) = {ev(P6, r)}")

    print()
    print("=== try quadratic factors q^2 + aq + b for P5 ===")
    found5 = []
    for a in range(-6, 7):
        for b in range(-6, 7):
            f = [Fraction(b), Fraction(a), Fraction(1)]
            if poly_div(P5, f) is not None:
                found5.append((a, b, poly_div(P5, f)))
    if found5:
        for a, b, q in found5:
            print(f"  q^2 + {a}q + {b}  ->  quotient {[str(x) for x in q]}")
    else:
        print("  none")

    print()
    print("=== try quadratic factors for P6 ===")
    found6 = []
    for a in range(-20, 21):
        for b in range(-20, 21):
            f = [Fraction(b), Fraction(a), Fraction(1)]
            if poly_div(P6, f) is not None:
                found6.append((a, b, poly_div(P6, f)))
    if found6:
        for a, b, q in found6:
            print(f"  q^2 + {a}q + {b}  ->  quotient {[str(x) for x in q]}")
    else:
        print("  none")

    print()
    print("=== numeric roots (to spot irrational structure) ===")
    import cmath
    for name, P in (("P5", P5), ("P6", P6)):
        # companion-matrix eigenvalues via numpy-free power iteration is
        # overkill; use numpy if available
        try:
            import numpy as np
            roots = np.roots([float(c) for c in reversed(P)])
            print(f"  {name} roots:")
            for r in roots:
                print(f"    {r:.6f}")
        except ImportError:
            print(f"  {name}: numpy unavailable")

    out = Path(__file__).resolve().parent.parent / "output" / "arc_factor2.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"P5_quadratic_factors": [[a, b] for a, b, _ in found5],
                               "P6_quadratic_factors": [[a, b] for a, b, _ in found6]},
                              indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
