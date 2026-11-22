"""Factor the arc-count polynomials.

#4-arcs = (q^8 - q^7 - q^4 + q^3)/24.  Let me factor it.

    q^8 - q^7 - q^4 + q^3 = q^3 (q^5 - q^4 - q + 1)
                          = q^3 (q^4(q-1) - (q-1))
                          = q^3 (q-1)(q^4 - 1)
                          = q^3 (q-1)(q^2-1)(q^2+1)
                          = q^3 (q-1)^2 (q+1)(q^2+1)

So

    #4-arcs = q^3 (q-1)^2 (q+1)(q^2+1) / 24

Check at q=5: 125 * 16 * 6 * 26 / 24 = 13000.  YES.

That is a BEAUTIFUL factorization.  Let me factor #5 and #6 too.

Run:  python arc_factor.py
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def poly_div(a, b):
    """Divide polynomial a by b (exact), return quotient or None."""
    a = list(a)
    b = list(b)
    while len(b) > 1 and b[-1] == 0:
        b.pop()
    if len(b) == 1 and b[0] == 0:
        return None
    q = [Fraction(0)] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and any(x != 0 for x in a):
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


def factor_out(coef, candidates):
    """Repeatedly divide by candidate factors; return (factors, remainder)."""
    cur = list(coef)
    factors = []
    for name, f in candidates:
        while True:
            q = poly_div(cur, f)
            if q is None:
                break
            factors.append(name)
            cur = q
    return factors, cur


def main() -> None:
    # #4: (q^8 - q^7 - q^4 + q^3)/24
    c4 = [Fraction(0)] * 9
    c4[3] = Fraction(1)
    c4[4] = Fraction(-1)
    c4[7] = Fraction(-1)
    c4[8] = Fraction(1)

    # #5
    c5 = [Fraction(0)] * 11
    for i, v in {3: 5, 4: -15, 5: 15, 6: -5, 7: -1, 8: 5, 9: -5, 10: 1}.items():
        c5[i] = Fraction(v, 120)

    # #6 (odd q)
    c6 = [Fraction(0)] * 13
    for i, v in {2: Fraction(-1, 48), 3: Fraction(5, 18),
                 4: Fraction(-187, 360), 5: Fraction(53, 144),
                 6: Fraction(-5, 48), 7: Fraction(-37, 144),
                 8: Fraction(373, 720), 9: Fraction(-53, 144),
                 10: Fraction(1, 8), 11: Fraction(-1, 48),
                 12: Fraction(1, 720)}.items():
        c6[i] = v

    # candidate factors: q, (q-1), (q+1), (q^2+1), (q^2-q+1), (q^2+q+1)
    cands = [
        ("q", [Fraction(0), Fraction(1)]),
        ("(q-1)", [Fraction(-1), Fraction(1)]),
        ("(q+1)", [Fraction(1), Fraction(1)]),
        ("(q^2+1)", [Fraction(1), Fraction(0), Fraction(1)]),
        ("(q^2-q+1)", [Fraction(1), Fraction(-1), Fraction(1)]),
        ("(q^2+q+1)", [Fraction(1), Fraction(1), Fraction(1)]),
        ("(q^2-1)", [Fraction(-1), Fraction(0), Fraction(1)]),
    ]

    rows = []
    for name, coef in (("#4", c4), ("#5", c5), ("#6", c6)):
        factors, rem = factor_out(coef, cands)
        print(f"{name}:")
        print(f"  factors: {factors}")
        print(f"  remainder degree: {len(rem)-1}")
        print(f"  remainder: {[str(x) for x in rem]}")
        rows.append({"name": name, "factors": factors,
                     "remainder": [str(x) for x in rem]})
        print()

    print("=== #4 in factored form ===")
    print("  #4-arcs = q^3 (q-1)^2 (q+1) (q^2+1) / 24")
    print("  check q=5: 125*16*6*26/24 =", 125 * 16 * 6 * 26 // 24)

    out = Path(__file__).resolve().parent.parent / "output" / "arc_factor.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
