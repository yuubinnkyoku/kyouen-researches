"""CLOSED FORMS FOR THE ARC COUNTS AT SMALL k.

The arc-count series shows a striking pattern:

    k <= 3 :  #arcs = C(n, k)          (ratio exactly 1)
    k = 4  :  #arcs = C(n,4) - b        where b = #circles

Let me verify the k=4 formula and derive it.

WHY k <= 3 IS TRIVIAL.  A 4-subset is "bad" iff it is concyclic.  Any
3-subset is an arc, because 3 points are always concyclic but a 4th is
needed to violate the condition.  So #arcs = C(n,k) for k <= 3.  []

WHY k = 4 HAS THE FORM C(n,4) - b.  A 4-subset is bad iff it is concyclic,
and the concyclic 4-subsets are exactly the 4-subsets of the circles.
Each circle has q+1 points, so it contributes C(q+1,4) four-subsets, and
distinct circles share at most 2 points, so no 4-subset lies on two
circles.  Hence

    #bad 4-subsets = b * C(q+1, 4),   b = q(q^2+1).

Check q=5: b = 5*26 = 130, C(6,4) = 15, so 130*15 = 1950, and
C(26,4) - 1950 = 14950 - 1950 = 13000.  MATCHES.

Check q=7: b = 7*50 = 350, C(8,4) = 70, so 350*70 = 24500, and
C(50,4) - 24500 = 230300 - 24500 = 205800.  MATCHES.

Check q=8: b = 8*65 = 520, C(9,4) = 126, so 520*126 = 65520, and
C(65,4) - 65520 = 677040 - 65520 = 611520.  MATCHES.

So the k=4 count has the closed form

    #4-arcs = C(n,4) - b*C(q+1,4),   n = q^2+1,  b = q(q^2+1).

This script verifies all of it.

Run:  python arc_small_k.py
"""

from __future__ import annotations

from math import comb

SERIES = {
    3: {0: 1, 1: 10, 2: 45, 3: 120, 4: 180, 5: 72},
    4: {0: 1, 1: 17, 2: 136, 3: 680, 4: 2040, 5: 2040},
    5: {0: 1, 1: 26, 2: 325, 3: 2600, 4: 13000, 5: 26000, 6: 5200},
    7: {0: 1, 1: 50, 2: 1225, 3: 19600, 4: 205800, 5: 1070160,
        6: 1254400},
    8: {0: 1, 1: 65, 2: 2080, 3: 43680, 4: 611520, 5: 4525248,
        6: 9434880, 7: 1048320},
}


def main() -> None:
    print("=== k <= 3: #arcs = C(n,k) ===")
    print(f"{'q':>3} {'n':>5} {'k':>2} {'#arcs':>10} {'C(n,k)':>10} {'ok':>4}")
    all_ok = True
    for q in sorted(SERIES):
        n = q * q + 1
        for k in (0, 1, 2, 3):
            c = SERIES[q].get(k)
            if c is None:
                continue
            ok = c == comb(n, k)
            all_ok = all_ok and ok
            print(f"{q:>3} {n:>5} {k:>2} {c:>10} {comb(n,k):>10} "
                  f"{str(ok):>4}")
    print(f"  all ok: {all_ok}")

    print()
    print("=== k = 4: #arcs = C(n,4) - b*C(q+1,4),  b = q(q^2+1) ===")
    print(f"{'q':>3} {'n':>5} {'b':>6} {'#arcs':>10} {'formula':>10} {'ok':>4}")
    all_ok4 = True
    for q in sorted(SERIES):
        n = q * q + 1
        b = q * (q * q + 1)
        c = SERIES[q].get(4)
        if c is None:
            continue
        pred = comb(n, 4) - b * comb(q + 1, 4)
        ok = c == pred
        all_ok4 = all_ok4 and ok
        print(f"{q:>3} {n:>5} {b:>6} {c:>10} {pred:>10} {str(ok):>4}")
    print(f"  all ok: {all_ok4}")

    print()
    print("=== k = 5: is there a closed form? ===")
    print("  #bad 5-subsets = those containing a concyclic 4-subset.")
    print("  Inclusion-exclusion over circles is needed; two circles share")
    print("  at most 2 points, so a 5-subset can lie on at most one circle")
    print("  OR contain two disjoint concyclic 4-subsets.")
    print()
    print(f"{'q':>3} {'#5-arcs':>10} {'C(n,5)':>12} {'bad':>10} "
          f"{'b*C(q+1,5)':>12} {'extra':>10}")
    for q in sorted(SERIES):
        n = q * q + 1
        b = q * (q * q + 1)
        c = SERIES[q].get(5)
        if c is None:
            continue
        bad = comb(n, 5) - c
        simple = b * comb(q + 1, 5)
        print(f"{q:>3} {c:>10} {comb(n,5):>12} {bad:>10} {simple:>12} "
              f"{bad - simple:>10}")

    print()
    print("The 'extra' column counts 5-subsets that contain a concyclic")
    print("4-subset but are not contained in a single circle.")

    print()
    print("=== summary ===")
    print("  k <= 3 :  #arcs = C(n,k)                       (proved)")
    print("  k = 4  :  #arcs = C(n,4) - b*C(q+1,4)          (proved)")
    print("  k >= 5 :  no closed form found")


if __name__ == "__main__":
    main()
