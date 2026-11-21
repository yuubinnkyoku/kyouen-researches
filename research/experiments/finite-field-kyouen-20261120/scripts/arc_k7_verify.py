"""k=7: verifying the profile division by multiplicity.

MEASURED over (C, T, {x,y,z}) tuples with |T| = 4:

    (4,4,4,4)        1248000
    (4,4,4,4,4)       390000
    (4,4,4)           288600
    (5,4,4)           171600
    (5,4)              62400
    (4,4)              31200
    (4,4,4,4,4,4)      31200

Each 7-set with profile P is counted once per (4-circle, 4-subset) pair,
i.e. |P| times (the number of entries in P).  So

    #7-sets with profile P = tuples(P) / |P|

Check against the direct census:

    (4,4)          31200 / 2 =  15600   measured  15600  OK
    (4,4,4)       288600 / 3 =  96200   measured  96200  OK
    (4,4,4,4)    1248000 / 4 = 312000   measured 312000  OK
    (4,4,4,4,4)   390000 / 5 =  78000   measured  78000  OK
    (4,4,4,4,4,4)  31200 / 6 =   5200   measured   5200  OK
    (5,4)          62400 / 1 =  62400   measured  62400  OK  (only one 4-circle)
    (5,4,4)       171600 / 2 =  85800   measured  85800  OK

ALL MATCH.  So the k=7 profile counts reduce to counting tuples, and the
tuple counts are what the pencil machinery computes.

Run:  python arc_k7_verify.py
"""

from __future__ import annotations

MEASURED = {
    (4, 4): 15600,
    (4, 4, 4): 96200,
    (4, 4, 4, 4): 312000,
    (4, 4, 4, 4, 4): 78000,
    (4, 4, 4, 4, 4, 4): 5200,
    (5, 4): 62400,
    (5, 4, 4): 85800,
    (6,): 2600,
}

TUPLES = {
    (4, 4, 4, 4): 1248000,
    (4, 4, 4, 4, 4): 390000,
    (4, 4, 4): 288600,
    (5, 4, 4): 171600,
    (5, 4): 62400,
    (4, 4): 31200,
    (4, 4, 4, 4, 4, 4): 31200,
}


def main() -> None:
    print("=== profile = tuples / (number of 4-circles) ===")
    print("  The tuple loop fixes a 4-subset T of a circle C, so a 7-set is")
    print("  counted once per (4-circle, 4-subset) pair.  For a profile P")
    print("  the number of 4-circles is the count of entries equal to 4.")
    print()
    print(f"{'profile':>20} {'tuples':>10} {'#4-circ':>8} {'tuples/#':>12} "
          f"{'measured':>10} {'ok':>4}")
    all_ok = True
    for prof, tc in sorted(TUPLES.items(), key=lambda x: -x[1]):
        m = sum(1 for t in prof if t == 4)
        val = tc // m
        meas = MEASURED.get(prof)
        ok = (val == meas)
        all_ok = all_ok and ok
        print(f"{str(prof):>20} {tc:>10} {m:>8} {val:>12} {meas:>10} "
              f"{str(ok):>4}")
    print(f"  all match: {all_ok}")

    print()
    print("=== (6,) is separate ===")
    print("  (6,) = b*C(s,6)*C(n-s,1) = 130*1*20 = 2600  (measured 2600)")

    print()
    print("=== total check ===")
    tot = sum(MEASURED.values())
    print(f"  sum of measured profiles = {tot}")
    print(f"  C(26,7) = 657800, arcs = 0, so bad = 657800")
    print(f"  match: {tot == 657800}")

    print()
    print("=== which profiles are closed? ===")
    print("  (6,)   : closed  b*C(s,6)*C(n-s,1)")
    print("  (5,4)  : closed  b*sum N_xy*H(n2,n1,1,5)")
    print("  (5,4,4): closed  b*sum N_xy*H(n2,n1,2,5)")
    print("  (4,*)  : need the tuple counts, which involve THREE outside")
    print("           points and hence a richer structure than the pencil")


if __name__ == "__main__":
    main()
