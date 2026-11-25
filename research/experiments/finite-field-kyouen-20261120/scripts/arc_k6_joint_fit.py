"""CLOSED FORMS FOR THE JOINT INTERSECTION TABLE.

MEASURED (T = 4-subset of circle C, {x,y} outside C, C' through x,y, C' != C):

    q=5 (circle size 6, n=26):
        (|C' cap C|, |T cap C'|) -> count
        (0,0): 450   (1,0):  80   (1,1): 160
        (2,0):  30   (2,1): 240   (2,2): 180

    q=7 (circle size 8, n=50):
        (0,0): 2940  (1,0): 504   (1,1): 504
        (2,0):  630  (2,1): 1680  (2,2): 630

Let me fit each entry.

Let s = q+1 (circle size), n = q^2+1, and let P = C(n-s, 2) = number of
pairs {x,y} outside C.  Note P*(q+1) = total.

(2,2): C' meets C in 2 points BOTH in T.  Choose the 2 points of T:
C(4,2) = 6.  Then C' is a circle through those 2 points, C' != C: q choices.
Then {x,y} = 2 points of C' outside C: C(q-1, 2).
    (2,2) = 6 * q * C(q-1,2)
    q=5: 6*5*6 = 180  MATCHES
    q=7: 6*7*C(6,2) = 6*7*15 = 630  MATCHES

(2,1): C' meets C in 2 points, exactly 1 in T.  Choose 1 of T (4) and 1 of
C\T (q+1-4 = q-3): 4*(q-3) pairs.  Then q circles through them, C' != C,
and C(q-1,2) pairs {x,y}.
    (2,1) = 4*(q-3) * q * C(q-1,2)
    q=5: 4*2*5*6 = 240  MATCHES
    q=7: 4*4*7*15 = 1680  MATCHES

(2,0): C' meets C in 2 points, none in T.  Choose 2 of C\T: C(q-3,2).
    (2,0) = C(q-3,2) * q * C(q-1,2)
    q=5: C(2,2)*5*6 = 30  MATCHES
    q=7: C(4,2)*7*15 = 6*7*15 = 630  MATCHES

(1,1): C' meets C in exactly 1 point, which is in T.  Choose p in T (4).
C' through p, meeting C only at p (tangent).  For each such C', {x,y} are
2 points of C' outside C: C(q-1,2).  How many tangent circles through p?
    q=5: 160 / (4 * C(4,2)) = 160/24 = 6.67  -- not integral
Let me instead fit: (1,1) = 4 * X * C(q-1,2) with X = number of tangent
circles at p.
    q=5: 160 = 4*X*6 -> X = 6.67  NO
So the tangent count is not uniform, or my model is off.

Let me just fit each entry as a polynomial in q.

Run:  python arc_k6_joint_fit.py
"""

from __future__ import annotations

from math import comb

DATA = {
    5: {(0, 0): 450, (1, 0): 80, (1, 1): 160,
        (2, 0): 30, (2, 1): 240, (2, 2): 180},
    7: {(0, 0): 2940, (1, 0): 504, (1, 1): 504,
        (2, 0): 630, (2, 1): 1680, (2, 2): 630},
}


def main() -> None:
    print("=== fitting each (capC, capT) entry ===")
    for key in [(2, 2), (2, 1), (2, 0), (1, 1), (1, 0), (0, 0)]:
        print(f"\n{key}:")
        for q in sorted(DATA):
            v = DATA[q][key]
            print(f"  q={q}: {v}")
        # candidate formulas
        cands = {
            "C(4,2)*q*C(q-1,2)": lambda q: comb(4, 2) * q * comb(q - 1, 2),
            "4*(q-3)*q*C(q-1,2)": lambda q: 4 * (q - 3) * q * comb(q - 1, 2),
            "C(q-3,2)*q*C(q-1,2)": lambda q: comb(q - 3, 2) * q * comb(q - 1, 2),
            "4*q*C(q-1,2)": lambda q: 4 * q * comb(q - 1, 2),
            "4*(q-3)*C(q-1,2)": lambda q: 4 * (q - 3) * comb(q - 1, 2),
            "C(q-3,2)*C(q-1,2)": lambda q: comb(q - 3, 2) * comb(q - 1, 2),
            "q*C(q-1,2)": lambda q: q * comb(q - 1, 2),
            "C(q-1,2)": lambda q: comb(q - 1, 2),
        }
        for name, f in cands.items():
            ok = all(f(q) == DATA[q][key] for q in DATA)
            if ok:
                print(f"  MATCH: {name}")
        # print values for inspection
        for name, f in cands.items():
            vals = [f(q) for q in sorted(DATA)]
            obs = [DATA[q][key] for q in sorted(DATA)]
            if vals != obs:
                print(f"    {name}: {vals} vs {obs}")

    print()
    print("=== totals ===")
    for q in sorted(DATA):
        tot = sum(DATA[q].values())
        print(f"q={q}: total {tot}, C(n-q-1,2)*(q+1) = "
              f"{comb(q*q+1-q-1,2)*(q+1)}")


if __name__ == "__main__":
    main()
