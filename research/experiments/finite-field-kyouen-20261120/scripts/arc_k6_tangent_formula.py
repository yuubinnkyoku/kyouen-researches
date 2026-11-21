"""CLOSED FORM FOR THE TANGENT CASE: |C' cap C| = 1.

MEASURED:
    tangent circles through each point of C:  q-1   (4 at q=5, 6 at q=7)
    (xy, C') with C' tangent, by |T cap C'|:
        q=5:  (1,0)=80,  (1,1)=160
        q=7:  (1,0)=504, (1,1)=504

DERIVATION.

(1) TANGENT COUNT.  Through a point p of C there are q(q+1) circles.  The
ones meeting C in 2 points: for each of the q other points p' of C, there
are q circles through p,p' other than C, so q*q = q^2.  Hence the tangent
ones number q(q+1) - q^2 = q.  But the measurement says q-1.

The discrepancy: the circle through p and {x,y} where x,y are outside C --
we are counting only circles that contain at least 2 points outside C.
A tangent circle at p has q points outside C (it meets C only at p), so it
does contain outside points.  So the count should be q.

Measured q-1 = 4 at q=5.  So one of the q tangent circles has fewer than 2
outside points?  No -- all have q outside points.

Resolution: the measurement loops over pairs {x,y} OUTSIDE C and circles
through them.  A tangent circle at p contains q outside points, hence
C(q,2) pairs.  So it IS counted.  The count of tangent circles per p is
q-1, meaning my derivation over-counted by 1: the "circle through p,p'"
count of q includes C itself only when p'=... let me recount.

Circles through p: q(q+1).  Circles through p meeting C in >= 2 points:
for each p' != p in C (q choices), the circles through p and p' number
q+1, one of which is C.  So circles through p meeting C in exactly 2
points = q * q = q^2 (excluding C).  Plus C itself.  Total through p
meeting C in >=2 points = q^2 + 1.  Remaining = q(q+1) - q^2 - 1 = q - 1.
MATCHES.  []

(2) THE (1,1) COUNT.  C' tangent at p in T.  Choose p in T: 4 ways.
Choose a tangent circle at p: q-1 ways.  Choose {x,y} outside C on C':
C(q,2) ways (C' has q points outside C).
    (1,1) = 4 * (q-1) * C(q,2)
    q=5: 4*4*10 = 160  MATCHES
    q=7: 4*6*21 = 504  MATCHES

(3) THE (1,0) COUNT.  C' tangent at p NOT in T, i.e. p in C \ T (q-3 ways).
    (1,0) = (q-3) * (q-1) * C(q,2)
    q=5: 2*4*10 = 80   MATCHES
    q=7: 4*6*21 = 504  MATCHES

BOTH MATCH.  So the tangent case is fully closed.

Run:  python arc_k6_tangent_formula.py
"""

from __future__ import annotations

from math import comb

DATA = {
    5: {(1, 0): 80, (1, 1): 160},
    7: {(1, 0): 504, (1, 1): 504},
}


def main() -> None:
    print("=== tangent case closed forms ===")
    print("  (1,1) = 4*(q-1)*C(q,2)")
    print("  (1,0) = (q-3)*(q-1)*C(q,2)")
    print()
    print(f"{'q':>3} {'(1,1) obs':>10} {'formula':>10} {'ok':>4} "
          f"{'(1,0) obs':>10} {'formula':>10} {'ok':>4}")
    all_ok = True
    for q in sorted(DATA):
        f11 = 4 * (q - 1) * comb(q, 2)
        f10 = (q - 3) * (q - 1) * comb(q, 2)
        o11 = DATA[q][(1, 1)]
        o10 = DATA[q][(1, 0)]
        ok = (f11 == o11) and (f10 == o10)
        all_ok = all_ok and ok
        print(f"{q:>3} {o11:>10} {f11:>10} {str(f11==o11):>4} "
              f"{o10:>10} {f10:>10} {str(f10==o10):>4}")
    print(f"  all ok: {all_ok}")

    print()
    print("=== the (0,0) entry: C' disjoint from C ===")
    print("  Measured: q=5 -> 450, q=7 -> 2940")
    print("  Total is C(n-q-1,2)*(q+1); the capC=2 and capC=1 parts are known,")
    print("  so (0,0) = total - (2,*) - (1,*)")
    print()
    print(f"{'q':>3} {'total':>10} {'(2,*)':>10} {'(1,*)':>10} "
          f"{'(0,0)':>10} {'observed':>10}")
    OBS00 = {5: 450, 7: 2940}
    for q in sorted(DATA):
        n = q * q + 1
        total = comb(n - q - 1, 2) * (q + 1)
        c2 = q * comb(q - 1, 2) * comb(q + 1, 2)
        c1 = (q - 1) * (q - 1) * comb(q, 2)   # (q-3)+4 = q-1 tangent points
        c0 = total - c2 - c1
        print(f"{q:>3} {total:>10} {c2:>10} {c1:>10} {c0:>10} "
              f"{OBS00[q]:>10}  {'OK' if c0 == OBS00[q] else 'MISMATCH'}")

    print()
    print("=== COMPLETE k=6 JOINT TABLE ===")
    print("  (2,2) = C(4,2)*q*C(q-1,2)")
    print("  (2,1) = 4*(q-3)*q*C(q-1,2)")
    print("  (2,0) = C(q-3,2)*q*C(q-1,2)")
    print("  (1,1) = 4*(q-1)*C(q,2)")
    print("  (1,0) = (q-3)*(q-1)*C(q,2)")
    print("  (0,0) = total - (2,*) - (1,*)")


if __name__ == "__main__":
    main()
