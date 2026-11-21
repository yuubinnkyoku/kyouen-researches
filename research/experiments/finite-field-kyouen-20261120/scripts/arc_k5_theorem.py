"""THE k=5 CLOSED FORM: a clean theorem.

A k-subset of the ovoid is an ARC iff it contains no concyclic 4-subset.

For k = 5 the structure is especially simple.  A 5-set has 5 four-subsets,
and any two of them share exactly 3 points.  If two of them are concyclic,
the shared 3 points determine a unique circle, so both lie on the SAME
circle, and hence all 5 points are concyclic.

Therefore a 5-set is bad in exactly one of two disjoint ways:

  (A) all 5 points lie on one circle;
  (B) exactly 4 lie on a circle and the 5th does not.

Counting:

  (A)  b * C(q+1, 5)
  (B)  b * C(q+1, 4) * (n - (q+1))

with b = q(q^2+1) circles, n = q^2+1 points.  So

  #5-arcs = C(n,5) - b*C(q+1,5) - b*C(q+1,4)*(n-q-1).

This script verifies it against the exhaustive counts.

Run:  python arc_k5_theorem.py
"""

from __future__ import annotations

from math import comb

# exhaustive arc counts
SERIES = {
    3: {0: 1, 1: 10, 2: 45, 3: 120, 4: 180, 5: 72},
    4: {0: 1, 1: 17, 2: 136, 3: 680, 4: 2040, 5: 2040},
    5: {0: 1, 1: 26, 2: 325, 3: 2600, 4: 13000, 5: 26000, 6: 5200},
    7: {0: 1, 1: 50, 2: 1225, 3: 19600, 4: 205800, 5: 1070160,
        6: 1254400},
    8: {0: 1, 1: 65, 2: 2080, 3: 43680, 4: 611520, 5: 4525248,
        6: 9434880, 7: 1048320},
}


def formula5(q: int) -> int:
    n = q * q + 1
    b = q * (q * q + 1)
    all5 = b * comb(q + 1, 5)
    exactly4 = b * comb(q + 1, 4) * (n - (q + 1))
    return comb(n, 5) - all5 - exactly4


def main() -> None:
    print("=== k=5 closed form ===")
    print("  #5-arcs = C(n,5) - b*C(q+1,5) - b*C(q+1,4)*(n-q-1)")
    print()
    print(f"{'q':>3} {'n':>5} {'b':>6} {'(A) all5':>10} {'(B) exactly4':>13} "
          f"{'#5-arcs':>10} {'formula':>10} {'ok':>4}")
    all_ok = True
    for q in sorted(SERIES):
        n = q * q + 1
        b = q * (q * q + 1)
        c = SERIES[q].get(5)
        if c is None:
            continue
        A = b * comb(q + 1, 5)
        B = b * comb(q + 1, 4) * (n - (q + 1))
        pred = formula5(q)
        ok = c == pred
        all_ok = all_ok and ok
        print(f"{q:>3} {n:>5} {b:>6} {A:>10} {B:>13} {c:>10} {pred:>10} "
              f"{str(ok):>4}")
    print(f"  all ok: {all_ok}")

    print()
    print("=== the same idea at k=4 (already proved) ===")
    print("  #4-arcs = C(n,4) - b*C(q+1,4)")
    print()
    print(f"{'q':>3} {'#4-arcs':>10} {'formula':>10} {'ok':>4}")
    ok4 = True
    for q in sorted(SERIES):
        n = q * q + 1
        b = q * (q * q + 1)
        c = SERIES[q].get(4)
        if c is None:
            continue
        pred = comb(n, 4) - b * comb(q + 1, 4)
        ok = c == pred
        ok4 = ok4 and ok
        print(f"{q:>3} {c:>10} {pred:>10} {str(ok):>4}")
    print(f"  all ok: {ok4}")

    print()
    print("=== k=6: why the same argument fails ===")
    print("  A 6-set has 15 four-subsets.  Two of them can share 2 points,")
    print("  and then they may lie on DIFFERENT circles.  So 'bad' is no")
    print("  longer a disjoint union of simple cases.")
    print()
    print(f"{'q':>3} {'#6-arcs':>10} {'C(n,6)':>12} {'bad':>10}")
    for q in sorted(SERIES):
        n = q * q + 1
        c = SERIES[q].get(6)
        if c is None:
            continue
        print(f"{q:>3} {c:>10} {comb(n,6):>12} {comb(n,6)-c:>10}")

    print()
    print("SUMMARY")
    print("  k <= 3 :  #arcs = C(n,k)                              (proved)")
    print("  k = 4  :  #arcs = C(n,4) - b*C(q+1,4)                 (proved)")
    print("  k = 5  :  #arcs = C(n,5) - b*C(q+1,5)")
    print("                    - b*C(q+1,4)*(n-q-1)                (proved)")
    print("  k >= 6 :  open")


if __name__ == "__main__":
    main()
