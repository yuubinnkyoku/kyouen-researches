"""#6-arcs as an explicit polynomial in q.

The k=6 closed form is

    #6-arcs = C(n,6) - b*C(s,6) - b*C(s,5)*(n-s)
              - b*sum_{n2} N_xy(n2)*[H(n2,n1,0) + H(n2,n1,1)/2 + H(n2,n1,2)/3]

with n = q^2+1, b = q(q^2+1), s = q+1, n1 = s-2*n2.

The N_xy split depends on the PARITY of q, so the polynomial is
parity-dependent.  Let me compute the polynomial separately for odd and
even q by evaluating at enough points and interpolating.

For odd q: use q = 5, 7, 9, 11, 13, ...  (need 2*6+1 = 13 points)
For even q: use q = 4, 8, 16, ...  (only 3 available, not enough)

So: derive the ODD-q polynomial (degree 12) from 13 odd q values, and
report the even-q case as open.

Run:  python arc6_polynomial.py
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arc_k6_pure import arcs6  # noqa: E402


def poly_fit(xs, ys):
    """Exact rational interpolation (Vandermonde, degree len(xs)-1)."""
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


def main() -> None:
    # odd q values
    odd_qs = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27]
    ys = []
    print("=== #6-arcs at odd q ===")
    for q in odd_qs:
        val, _ = arcs6(q)
        v = int(val)
        ys.append(v)
        print(f"  q={q:>3}: {v}")

    coef = poly_fit(odd_qs, ys)
    print()
    print("=== interpolated polynomial (odd q, degree 12) ===")
    if coef is None:
        print("  fit failed")
        return
    # trim
    while len(coef) > 1 and coef[-1] == 0:
        coef.pop()
    print(f"  degree {len(coef)-1}")
    print(f"  coefficients (c0..c{len(coef)-1}):")
    for i, c in enumerate(coef):
        if c != 0:
            print(f"    q^{i}: {c}")

    print()
    print("=== verification at the fitted points ===")
    ok = True
    for q, y in zip(odd_qs, ys):
        v = ev(coef, q)
        if v != y:
            ok = False
            print(f"  q={q}: poly={v} expected={y} MISMATCH")
    print(f"  all match: {ok}")

    print()
    print("=== extrapolation check at q=29, 31 ===")
    for q in (29, 31):
        val, _ = arcs6(q)
        v = int(val)
        p = ev(coef, q)
        print(f"  q={q}: closed form={v}, polynomial={p}, "
              f"match={p == v}")

    out = Path(__file__).resolve().parent.parent / "output" / "arc6_polynomial.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"odd_qs": odd_qs, "values": ys,
                               "coeffs": [str(c) for c in coef]},
                              indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
