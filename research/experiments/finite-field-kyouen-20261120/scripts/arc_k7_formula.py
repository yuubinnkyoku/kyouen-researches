"""k=7: the CORRECT decomposition is exact.

VERIFIED (q=5): each (w, |union without W|) pair maps to EXACTLY ONE
profile.  The mapping is:

    w=2, u=0  ->  (5,4)              u+2 = 2 four-circles? no: 1 four + 1 five
    w=2, u=1  ->  (5,4,4)
    w=1, u=1  ->  (4,4,4)
    w=1, u=2  ->  (4,4,4,4)
    w=1, u=3  ->  (4,4,4,4,4)
    w=0, u=1  ->  (4,4)
    w=0, u=2  ->  (4,4,4)
    w=0, u=3  ->  (4,4,4,4)
    w=0, u=4  ->  (4,4,4,4,4)
    w=0, u=5  ->  (4,4,4,4,4,4)

PATTERN.  The profile is:
    - a 5 if w = 2, else nothing
    - a 4 for C itself
    - a 4 for each circle in the union (excluding W)
    - a 4 for W if w = 2?  No: W carries 2 of T + 3 of xyz = 5 points, so
      W contributes a 5, not a 4.

So:
    #4s = 1 (for C) + u
    #5s = 1 if w = 2 else 0

Check:
    w=2, u=0: #4=1, #5=1 -> (5,4)        MATCHES
    w=2, u=1: #4=2, #5=1 -> (5,4,4)      MATCHES
    w=1, u=1: #4=2, #5=0 -> (4,4)        but measured (4,4,4)!
Hmm, w=1, u=1 gives (4,4,4) which has THREE 4s, but 1+1 = 2.

So the formula is off.  Let me recount: for w=1, W carries 1 of T and 3 of
xyz = 4 points of S.  So W IS a 4-circle!  It was excluded from the union
but it still counts.

Corrected:
    #4s = 1 (for C) + u + (1 if w = 1 else 0)
    #5s = 1 if w = 2 else 0

Check:
    w=1, u=1: #4 = 1+1+1 = 3 -> (4,4,4)   MATCHES
    w=1, u=2: #4 = 1+2+1 = 4 -> (4,4,4,4) MATCHES
    w=1, u=3: #4 = 1+3+1 = 5 -> (4,4,4,4,4) MATCHES
    w=0, u=1: #4 = 1+1+0 = 2 -> (4,4)     MATCHES
    w=0, u=2: #4 = 1+2 = 3 -> (4,4,4)     MATCHES
    w=0, u=3: #4 = 1+3 = 4 -> (4,4,4,4)   MATCHES
    w=0, u=4: #4 = 1+4 = 5 -> (4,4,4,4,4) MATCHES
    w=0, u=5: #4 = 1+5 = 6 -> (4,4,4,4,4,4) MATCHES
    w=2, u=0: #4 = 1+0 = 1, #5 = 1 -> (5,4) MATCHES
    w=2, u=1: #4 = 1+1 = 2, #5 = 1 -> (5,4,4) MATCHES

ALL MATCH.  So:

    #4-circles = 1 + u + [w = 1]
    #5-circles = [w = 2]

Run:  python arc_k7_formula.py
"""

from __future__ import annotations

DATA = {
    (0, 3): (4, 4, 4, 4),
    (1, 2): (4, 4, 4, 4),
    (0, 4): (4, 4, 4, 4, 4),
    (0, 2): (4, 4, 4),
    (2, 1): (5, 4, 4),
    (1, 3): (4, 4, 4, 4, 4),
    (1, 1): (4, 4, 4),
    (2, 0): (5, 4),
    (0, 1): (4, 4),
    (0, 5): (4, 4, 4, 4, 4, 4),
}


def predict(w: int, u: int):
    n4 = 1 + u + (1 if w == 1 else 0)
    n5 = 1 if w == 2 else 0
    prof = tuple([5] * n5 + [4] * n4)
    return prof


def main() -> None:
    print("=== profile = (5 if w==2) + (4 repeated 1+u+[w==1]) ===")
    print(f"{'w':>3} {'u':>3} {'predicted':>22} {'measured':>22} {'ok':>4}")
    all_ok = True
    for (w, u), meas in sorted(DATA.items()):
        pred = predict(w, u)
        ok = pred == meas
        all_ok = all_ok and ok
        print(f"{w:>3} {u:>3} {str(pred):>22} {str(meas):>22} {str(ok):>4}")
    print(f"  all match: {all_ok}")

    print()
    print("=== the rule ===")
    print("  W = the unique circle through x,y,z")
    print("  w = |T cap W|  (0, 1 or 2)")
    print("  u = |union of pencil circles meeting T in 2 points, minus W|")
    print()
    print("  #4-circles = 1 (for C) + u + [w == 1]")
    print("  #5-circles = [w == 2]")
    print()
    print("  Why [w==1] adds a 4: W carries 1 of T and all 3 of {x,y,z},")
    print("  so W carries 4 points of S -- it IS a 4-circle.")
    print("  Why [w==2] gives a 5: W carries 2 of T and 3 of {x,y,z} = 5.")


if __name__ == "__main__":
    main()
