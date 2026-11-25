"""k=7: the circle counts by (a,w) have closed forms.

MEASURED (q=5, s=6, |T|=4, circles W != C):

    a=0 w=0: 30
    a=1 w=0:  8
    a=1 w=1: 16
    a=2 w=0:  5
    a=2 w=1: 40
    a=2 w=2: 30

CLOSED FORMS (all verified):

    a=2 total = C(s,2)*q
    a=1 total = s*(q-1)
    a=0 total = b - 1 - C(s,2)*q - s*(q-1)

    (2,2) = C(4,2)*q          = 6q
    (2,1) = 4*(s-4)*q         = 4(q-3)q
    (2,0) = C(s-4,2)*q        = C(q-3,2)q
    (1,1) = 4*(q-1)
    (1,0) = (s-4)*(q-1)       = (q-3)(q-1)

Check q=5:
    (2,2) = 6*5 = 30      MATCHES
    (2,1) = 4*2*5 = 40    MATCHES
    (2,0) = C(2,2)*5 = 5  MATCHES
    (1,1) = 4*4 = 16      MATCHES
    (1,0) = 2*4 = 8       MATCHES
    a=0 = 130-1-75-24 = 30 MATCHES

DERIVATION.

a=2: W meets C in 2 points {p,p'}.  Choose {p,p'} (C(s,2) ways), then W is
a circle through them other than C (q ways).  So C(s,2)*q.  []
  w = |{p,p'} cap T|: both in T (C(4,2)=6), one in T (4*(s-4)), neither
  (C(s-4,2)).  Each times q.

a=1: W meets C in exactly 1 point p.  The tangent circles at p number q-1
(proved earlier), and there are s points p.  So s*(q-1).  []
  w = [p in T]: 4*(q-1) or (s-4)*(q-1).

a=0: the rest.

So the w marginal is fully closed:

    w=2: C(4,2)*q*C(q-1,3)
    w=1: [4*(s-4)*q + 4*(q-1)]*C(q-1,3) + ... (careful: different |W\\C|)

Let me be careful: for a=2, |W \\ C| = s-2 = q-1, so triples = C(q-1,3).
For a=1, |W \\ C| = s-1 = q, so triples = C(q,3).
For a=0, |W \\ C| = s = q+1, so triples = C(q+1,3).

    w=2: (2,2) * C(q-1,3) = 6q*C(q-1,3)
    w=1: (2,1)*C(q-1,3) + (1,1)*C(q,3) = 4(q-3)q*C(q-1,3) + 4(q-1)*C(q,3)
    w=0: (2,0)*C(q-1,3) + (1,0)*C(q,3) + (0,0)*C(q+1,3)

Check q=5:
    w=2: 30*C(4,3) = 30*4 = 120   MATCHES
    w=1: 40*4 + 16*C(6,3) = 160 + 16*20 = 160+320 = 480
         but measured 320.  MISMATCH.

Hmm.  Let me recheck: for a=1, |W \\ C| = s-1 = 5 = q, so C(5,3) = 10, not
C(6,3)=20.  I used q=5 so C(q,3) = C(5,3) = 10.
    w=1: 40*4 + 16*10 = 160 + 160 = 320   MATCHES

    w=0: 5*4 + 8*10 + 30*C(6,3) = 20 + 80 + 30*20 = 20+80+600 = 700  MATCHES

ALL MATCH.

Run:  python arc_k7_w_closed.py
"""

from __future__ import annotations

from math import comb


def w_marginal(q: int):
    s = q + 1
    n = q * q + 1
    b = q * (q * q + 1)
    c22 = comb(4, 2) * q
    c21 = 4 * (s - 4) * q
    c20 = comb(s - 4, 2) * q
    c11 = 4 * (q - 1)
    c10 = (s - 4) * (q - 1)
    c00 = b - 1 - (c22 + c21 + c20) - (c11 + c10)
    w2 = c22 * comb(q - 1, 3)
    w1 = c21 * comb(q - 1, 3) + c11 * comb(q, 3)
    w0 = c20 * comb(q - 1, 3) + c10 * comb(q, 3) + c00 * comb(q + 1, 3)
    return {0: w0, 1: w1, 2: w2}, {"c22": c22, "c21": c21, "c20": c20,
                                   "c11": c11, "c10": c10, "c00": c00}


def main() -> None:
    print("=== w marginal closed form ===")
    print("  w=2: C(4,2)*q*C(q-1,3)")
    print("  w=1: 4(q-3)q*C(q-1,3) + 4(q-1)*C(q,3)")
    print("  w=0: C(q-3,2)q*C(q-1,3) + (q-3)(q-1)*C(q,3)")
    print("       + (b-1-C(s,2)q-s(q-1))*C(q+1,3)")
    print()
    for q in (5, 7):
        wm, cc = w_marginal(q)
        n = q * q + 1
        s = q + 1
        print(f"q={q}: n={n}, s={s}, C(n-s,3)={comb(n-s,3)}")
        print(f"  circle counts: {cc}")
        print(f"  w marginal: {wm}, total {sum(wm.values())}")
        print(f"  total matches C(n-s,3): "
              f"{sum(wm.values()) == comb(n-s,3)}")
        print()

    print("=== measured (q=5) ===")
    print("  w marginal: {0: 700, 1: 320, 2: 120}")
    wm, _ = w_marginal(5)
    print(f"  formula:    {wm}")
    print(f"  match: {wm == {0: 700, 1: 320, 2: 120}}")


if __name__ == "__main__":
    main()
