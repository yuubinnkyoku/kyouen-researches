"""CLOSED FORMS FOR THE (n2, j) TABLE.

MEASURED (over all {x,y} and all 4-subsets T of C):

    q=5 (circle size 6):
        n2=2: j=0 -> 480,  j=1 -> 1200, j=2 -> 120
        n2=3: j=0 ->   0,  j=1 ->  840, j=2 -> 210
    q=7 (circle size 8):
        n2=3: j=0 -> 14112, j=1 -> 19656, j=2 -> 1512
        n2=4: j=0 ->  5712, j=1 -> 17136, j=2 -> 2142

STRUCTURE.  iota is an involution on C with n2 pairs (2*n2 points) and
n1 = q+1-2*n2 fixed points.  T is a 4-subset of C.

j = #{pairs of iota fully inside T}.

Given the involution (n2 pairs + n1 fixed points) and a uniformly random
4-subset T, the count of T with exactly j pairs inside is a hypergeometric
quantity:

    choose j of the n2 pairs (both points) : C(n2, j)
    choose the remaining 4-2j points from the n1 fixed points : C(n1, 4-2j)

    #T with that j = C(n2,j) * C(n1, 4-2j)

Check q=5, n2=2 (n1 = 6-4 = 2):
    j=0: C(2,0)*C(2,4) = 0        but measured 480/120 = 4 per {x,y}
Hmm, 480/120 = 4.  And C(2,0)*C(2,4) = 0.  So the formula is wrong.

Wait: n1 = q+1-2*n2 = 6-4 = 2.  C(2,4) = 0, so j=0 impossible.  But
measured j=0 occurs 480 times over 120 {x,y} = 4 per {x,y}.  Contradiction.

Resolution: T need not avoid the pairs -- T can contain ONE point of a
pair.  Then that pair contributes 0 to j but uses up a slot.  So the
count is:

    choose j pairs fully in T          : C(n2, j)
    choose a of the remaining pairs with exactly 1 point in T
    choose the rest from fixed points

Let me just fit numerically.

Run:  python arc_k6_n2j_fit.py
"""

from __future__ import annotations

import itertools
from math import comb

DATA = {
    5: {(2, 0): 480, (2, 1): 1200, (2, 2): 120,
        (3, 0): 0, (3, 1): 840, (3, 2): 210},
    7: {(3, 0): 14112, (3, 1): 19656, (3, 2): 1512,
        (4, 0): 5712, (4, 1): 17136, (4, 2): 2142},
}


def count_T(n2, n1, j, k=4):
    """#k-subsets T of a set with n2 pairs + n1 singles having exactly j pairs."""
    total = 0
    # choose j pairs fully in T
    for jj in range(j, j + 1):
        # a pairs with exactly one point in T
        for a in range(0, n2 - jj + 1):
            used = 2 * jj + a
            if used > k:
                break
            rest = k - used
            if rest > n1:
                continue
            total += (comb(n2, jj) * comb(n2 - jj, a)
                      * (2 ** a) * comb(n1, rest))
    return total


def main() -> None:
    print("=== testing the hypergeometric model ===")
    print("  #T with exactly j pairs = sum over a of")
    print("     C(n2,j) * C(n2-j,a) * 2^a * C(n1, 4-2j-a)")
    print()
    for q in sorted(DATA):
        s = q + 1
        print(f"q={q} (circle size {s}):")
        for n2 in sorted({a for (a, c) in DATA[q]}):
            n1 = s - 2 * n2
            print(f"  n2={n2}, n1={n1}")
            for j in (0, 1, 2):
                obs = DATA[q].get((n2, j), 0)
                pred = count_T(n2, n1, j)
                print(f"    j={j}: observed {obs}, model {pred}, "
                      f"ratio {obs/pred if pred else 'inf'}")
        # total per n2
        for n2 in sorted({a for (a, c) in DATA[q]}):
            tot = sum(DATA[q].get((n2, j), 0) for j in (0, 1, 2))
            print(f"  n2={n2}: total over T = {tot}, C(q+1,4) = "
                  f"{comb(q+1,4)}")

    print()
    print("=== per-{x,y} normalisation ===")
    for q in sorted(DATA):
        s = q + 1
        print(f"q={q}:")
        for n2 in sorted({a for (a, c) in DATA[q]}):
            tot = sum(DATA[q].get((n2, j), 0) for j in (0, 1, 2))
            # number of {x,y} with this n2
            n_xy = {5: {2: 120, 3: 70}, 7: {3: 504, 4: 357}}[q][n2]
            print(f"  n2={n2}: {tot} / {n_xy} = {tot/n_xy} per {{x,y}} "
                  f"(C(q+1,4)={comb(s,4)})")


if __name__ == "__main__":
    main()
