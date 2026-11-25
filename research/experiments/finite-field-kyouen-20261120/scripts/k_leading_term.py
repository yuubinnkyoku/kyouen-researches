"""K(q): a structural upper bound from the arc-count ladder.

We know K exactly for q <= 9.  The bounds are

    Omega(q^(1/3))  <=  K  <=  q + 2

The data: K = 6, 6, 7, 9 for q = 5, 7, 8, 9.

NEW IDEA.  Instead of bounding K directly, bound the SIZE at which the
arc count becomes zero.  The arc count #k-arcs is a polynomial in q of
degree 2k (since n ~ q^2 and we choose k points).  It becomes zero when
the leading coefficient vanishes or when a lower-order term dominates.

For k=7 the count is

    #7-arcs = C(n,7) - (bad 7-sets)

and C(n,7) ~ n^7/7! ~ q^14/5040.  The bad count is dominated by the
(4,4,4) profile which is ~ b*C(s,4)*... ~ q * q^4 * ... .

Let me compute the LEADING TERM of #k-arcs for k = 4..7 as a polynomial
in q, and see where it changes sign.  That predicts the threshold q where
k-arcs start to exist.

Run:  python k_leading_term.py
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from arc_k6_pure import arcs6  # noqa: E402


def count(q: int, k: int):
    n = q * q + 1
    b = q * (q * q + 1)
    s = q + 1
    if k <= 3:
        return comb(n, k)
    if k == 4:
        return comb(n, 4) - b * comb(s, 4)
    if k == 5:
        return comb(n, 5) - b * comb(s, 5) - b * comb(s, 4) * (n - s)
    if k == 6:
        val, _ = arcs6(q)
        return int(val)
    return None


SEVEN = {5: 0, 7: 0, 8: 1048320, 9: 17003520}


def poly_fit(xs, ys, deg):
    """Exact rational polynomial fit (Vandermonde)."""
    m = deg + 1
    A = [[Fraction(x) ** j for j in range(m)] for x in xs[:m]]
    B = [Fraction(y) for y in ys[:m]]
    # Gaussian elimination
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


def main() -> None:
    rows = []
    print("=== arc counts by k and q ===")
    print(f"{'q':>3} {'#4':>12} {'#5':>14} {'#6':>14} {'#7':>14}")
    data = {}
    for q in (5, 7, 8, 9):
        vals = {4: count(q, 4), 5: count(q, 5), 6: count(q, 6),
                7: SEVEN.get(q)}
        data[q] = vals
        print(f"{q:>3} {vals[4]:>12} {vals[5]:>14} {vals[6]:>14} "
              f"{vals[7]!s:>14}")

    print()
    print("=== leading coefficient of #k-arcs as a polynomial in q ===")
    print("  (degree 2k, fitted from q=5,7,8,9 plus extrapolated)")
    for k in (4, 5, 6):
        xs = [5, 7, 8, 9]
        ys = [data[q][k] for q in xs]
        deg = 2 * k
        if deg + 1 > len(xs):
            print(f"  k={k}: need {deg+1} points, have {len(xs)} -- skip")
            continue
        coef = poly_fit(xs, ys, deg)
        if coef is None:
            print(f"  k={k}: fit failed")
            continue
        print(f"  k={k}: leading coeff = {coef[-1]}")

    print()
    print("=== zero-crossing of #k-arcs ===")
    print("  #k-arcs > 0 iff K >= k.  The smallest q with #k-arcs > 0 is")
    print("  the smallest q with K >= k.")
    for k in (4, 5, 6, 7):
        qs = [q for q in sorted(data) if data[q].get(k) and data[q][k] > 0]
        print(f"  k={k}: smallest q with count>0 among tested = "
              f"{min(qs) if qs else 'none'}")

    out = Path(__file__).resolve().parent.parent / "output" / "k_leading_term.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({str(q): {str(k): v for k, v in d.items()}
                               for q, d in data.items()},
                              indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
