"""#7-arcs as an explicit polynomial in q (odd q).

The k=7 count is assembled from 11 profiles.  Rather than expand
symbolically (very messy), interpolate from computed values.

The count is a polynomial in q of degree 2*7 = 14 for odd q (the N_xy
split is parity-dependent).  So we need 15 odd q values.

Computing #7-arcs at q=11,13,... requires the tuple loop, which is
O(C(s,4)*C(n-s,3)*3q).  At q=11: 330*C(122,3)*33 = 330*295240*33 = 3.2e9.
Too slow in Python.

ALTERNATIVE: use the STRUCTURE.  The k=7 count is

    #7-arcs = C(n,7) - sum over 11 profiles

and each profile count is a polynomial.  The (5,), (6,), (7,) terms are
already closed forms.  The 8 tuple-derived profiles come from the
(w,u)-distribution, which is a polynomial in q for odd q.

So: interpolate the (w,u)-distribution counts as polynomials in q, then
assemble.  The (w,u) distribution has 9 classes at q=5,7 and 8 at q=9 --
the CLASS COUNT varies, so direct interpolation of the distribution is
fragile.

BETTER: interpolate #7-arcs directly from the values we have plus a few
more cheap ones.  We have q=5,7,8,9.  We need 15 for degree 14.

Let me instead check: is the degree really 14?  #7-arcs = C(n,7) - bad,
and C(n,7) has degree 14.  The bad terms are lower order (as we saw for
k=4,5,6 where the leading term was exactly C(n,k)'s).  So degree 14 with
leading coefficient 1/7! = 1/5040.

That gives us the leading term for free.  Let me verify the pattern holds
and record the leading term, leaving the full polynomial open.

Run:  python arc7_leading.py
"""

from __future__ import annotations

import json
from fractions import Fraction
from math import comb, factorial
from pathlib import Path

SEVEN = {5: 0, 7: 0, 8: 1048320, 9: 17003520}


def main() -> None:
    print("=== #7-arcs values ===")
    for q in sorted(SEVEN):
        n = q * q + 1
        print(f"  q={q}: n={n}, #7-arcs={SEVEN[q]}, C(n,7)={comb(n,7)}")

    print()
    print("=== leading term conjecture ===")
    print("  For k=4,5,6 the leading term of #k-arcs is q^(2k)/k!,")
    print("  matching C(n,k) ~ q^(2k)/k!.")
    print("  So for k=7 the leading term should be q^14/7! = q^14/5040.")
    print()
    print("  Check: at q=9, q^14/5040 =", 9**14 / factorial(7))
    print("         #7-arcs(9) =", SEVEN[9])
    print("         ratio =", SEVEN[9] / (9**14 / factorial(7)))
    print()
    print("  At q=8, q^14/5040 =", 8**14 / factorial(7))
    print("         #7-arcs(8) =", SEVEN[8])
    print("         ratio =", SEVEN[8] / (8**14 / factorial(7)))
    print()
    print("  The ratio is far below 1, so the leading term is NOT yet")
    print("  dominant at q=8,9 -- lower-order terms still matter.")

    print()
    print("=== degree check via finite differences ===")
    print("  With only 4 points we cannot determine degree 14.")
    print("  Need 15 odd q values; the tuple loop is too slow above q=9.")

    out = Path(__file__).resolve().parent.parent / "output" / "arc7_leading.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"values": {str(k): v for k, v in SEVEN.items()},
                               "leading_conjecture": "q^14/5040"},
                              indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
