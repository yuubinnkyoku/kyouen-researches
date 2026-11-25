"""The even-q #6-arcs polynomial, derived SYMBOLICALLY.

For even q the N_xy split is

    N_xy(0)  = C(q,2)          = q(q-1)/2
    N_xy(q/2) = q(q^2-1)/2

(verified at q = 2,4,8,16,32).

So the #6 closed form becomes

    #6 = C(n,6) - b*C(s,6) - b*C(s,5)*(n-s)
         - b*[ C(q,2) * (H(0,n1a,0) + H(0,n1a,1)/2 + H(0,n1a,2)/3)
             + q(q^2-1)/2 * (H(q/2,n1b,0) + H(q/2,n1b,1)/2 + H(q/2,n1b,2)/3) ]

with n1a = s - 0 = s and n1b = s - q.

Since n1a = s = q+1 and n1b = 1, and H(0, n1, j, k) is nonzero only for
j = 0, this is a POLYNOMIAL in q.  Let me expand it symbolically.

Run:  python arc6_even_symbolic.py
"""

from __future__ import annotations

import json
from fractions import Fraction
from math import comb
from pathlib import Path


def H(n2, n1, j, k):
    total = 0
    for a in range(0, n2 - j + 1):
        used = 2 * j + a
        if used > k:
            break
        rest = k - used
        if rest < 0 or rest > n1:
            continue
        total += comb(n2, j) * comb(n2 - j, a) * (2 ** a) * comb(n1, rest)
    return total


def closed6_even(q: int) -> Fraction:
    n = q * q + 1
    b = q * (q * q + 1)
    s = q + 1
    term6 = b * comb(s, 6)
    term5 = b * comb(s, 5) * (n - s)
    # N_xy(0) = C(q,2), n1 = s
    n1a = s
    ha = (H(0, n1a, 0, 4) + Fraction(H(0, n1a, 1, 4), 2)
          + Fraction(H(0, n1a, 2, 4), 3))
    # N_xy(q/2) = q(q^2-1)(q-2)/2, n1 = s - q = 1
    n1b = s - q
    hb = (H(q // 2, n1b, 0, 4) + Fraction(H(q // 2, n1b, 1, 4), 2)
          + Fraction(H(q // 2, n1b, 2, 4), 3))
    cnt_b = q * (q * q - 1) * (q - 2) // 2
    contrib = b * (comb(q, 2) * ha + cnt_b * hb)
    bad = term6 + term5 + contrib
    return Fraction(comb(n, 6)) - bad


def main() -> None:
    print("=== even-q #6-arcs (symbolic closed form) ===")
    vals = {}
    for q in (2, 4, 8, 16, 32, 64, 128):
        v = closed6_even(q)
        vals[q] = v
        print(f"  q={q}: {v}  integer={v.denominator == 1}")

    print()
    print("=== compare with arcs6 ===")
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from arc_k6_pure import arcs6
    for q in (2, 4, 8, 16, 32, 64):
        a, _ = arcs6(q)
        b = closed6_even(q)
        print(f"  q={q}: arcs6={Fraction(a)}, symbolic={b}, "
              f"match={Fraction(a) == b}")

    print()
    print("=== interpolate the even-q polynomial ===")
    # degree 12 needs 13 points; we have 7 (2,4,8,16,32,64,128)
    xs = [2, 4, 8, 16, 32, 64, 128]
    ys = [vals[q] for q in xs]
    m = len(xs)
    A = [[Fraction(x) ** j for j in range(m)] for x in xs]
    B = list(ys)
    for c in range(m):
        piv = None
        for r in range(c, m):
            if A[r][c] != 0:
                piv = r
                break
        if piv is None:
            print("  singular")
            return
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
    print(f"  degree {m-1} polynomial (only {m} points, NOT degree 12):")
    for i, c in enumerate(B):
        if c != 0:
            print(f"    q^{i}: {c}")
    print()
    print("  NOTE: with only 7 points we get a degree-6 fit, which is NOT")
    print("  the true polynomial.  The true degree is 12 and needs 13 points.")

    out = Path(__file__).resolve().parent.parent / "output" / "arc6_even_symbolic.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({str(q): str(v) for q, v in vals.items()},
                              indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
