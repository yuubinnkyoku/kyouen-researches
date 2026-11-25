"""Re-derive and verify ALL arc-count polynomials from scratch.

A transcription error was found in the #5 polynomial.  This script
re-derives every polynomial directly from the closed forms by exact
interpolation, verifies against the closed forms at many points, and
factors them correctly.

Run:  python arc_poly_verify.py
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
    for k in (4, 5, 6):
        deg = 2 * k
        xs = list(range(3, 3 + deg + 1))
        ys = [closed(q, k) for q in xs]
        coef = interpolate(xs, ys)
        # trim
        while len(coef) > 1 and coef[-1] == 0:
            coef.pop()
        print(f"=== k={k}: degree {len(coef)-1} ===")
        print("  coefficients:")
        for i, c in enumerate(coef):
            if c != 0:
                print(f"    q^{i}: {c}")

        # verify at many points
        bad = []
        for q in range(3, 40):
            if ev(coef, q) != closed(q, k):
                bad.append(q)
        print(f"  verified q=3..39: {'ALL OK' if not bad else f'FAIL at {bad}'}")

        # factor
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
                      "verified_upto": 39 if not bad else bad[0] - 1}

    out = Path(__file__).resolve().parent.parent / "output" / "arc_poly_verify.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
