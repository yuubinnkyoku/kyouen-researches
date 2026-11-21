"""k=7: sum_j is the number of pencil circles, and (3,2) is exactly W.

MEASURED (q=5, over 1140 triples):

    ((2,2),(2,2),(2,2))              464
    ((2,2),(2,2))                    324
    ((2,2),(2,2),(2,2),(2,2))        152
    ((2,2),(3,2))                     88
    ((2,2),)                          64
    ((3,2),)                          32
    ((2,2),(2,2),(2,2),(2,2),(2,2))   16

KEY OBSERVATIONS.

(1) Every circle in the list has |C' cap T| = 2 (by construction) and
    |C' cap xyz| in {2, 3}.

(2) A circle with |C' cap xyz| = 3 is the circle through all three of
    x,y,z, i.e. W.  So the (3,2) entries are exactly W, and they occur
    iff w = 2.

(3) sum_j = (number of entries) since each entry is one (pair, circle)
    incidence.  But a circle through all 3 points is counted in all 3
    pairs, so it contributes 3 to sum_j while appearing once in the list.

Let me verify: for the profile ((3,2),) with 32 triples, sum_j should be 3
(W counted in all three pencils).  And for ((2,2),(3,2)) with 88 triples,
sum_j = 1 + 3 = 4.

Check against the (case, w, sum_j) table:
    B w=2 sum_j=3: 32   <- ((3,2),) 32   MATCHES
    B w=2 sum_j=4: 88   <- ((2,2),(3,2)) 88  MATCHES

So the (3,2) circle is W and contributes 3 to sum_j.

(4) The remaining entries are all (2,2): circles through exactly 2 of
    {x,y,z} meeting T in 2 points.  Each contributes 1 to sum_j.

So:
    sum_j = (#(2,2) circles) + 3*[W is a (3,2) circle]

and the number of (2,2) circles is the "u" from before (when w<=1) or
u+3 (when w=2, since W is counted 3 times).

Let me verify the whole table.

Run:  python arc_k7_sumj_verify.py
"""

from __future__ import annotations

DATA = {
    ((2, 2), (2, 2), (2, 2)): 464,
    ((2, 2), (2, 2)): 324,
    ((2, 2), (2, 2), (2, 2), (2, 2)): 152,
    ((2, 2), (3, 2)): 88,
    ((2, 2),): 64,
    ((3, 2),): 32,
    ((2, 2), (2, 2), (2, 2), (2, 2), (2, 2)): 16,
}

# (case, w, sum_j) -> count
CASE_TABLE = {
    ("A", 0, 1): 16, ("A", 0, 2): 100, ("A", 0, 3): 416,
    ("A", 0, 4): 140, ("A", 0, 5): 8,
    ("A", 1, 1): 48, ("A", 1, 2): 96, ("A", 1, 3): 16,
    ("B", 0, 4): 12, ("B", 0, 5): 8,
    ("B", 1, 2): 128, ("B", 1, 3): 32,
    ("B", 2, 3): 32, ("B", 2, 4): 88,
}


def main() -> None:
    print("=== sum_j from the pencil-circle profile ===")
    print("  sum_j = #(2,2) + 3*[a (3,2) circle is present]")
    print()
    print(f"{'profile':>44} {'count':>6} {'#(2,2)':>7} {'has(3,2)':>9} "
          f"{'sum_j':>6}")
    derived = {}
    for prof, cnt in sorted(DATA.items(), key=lambda x: -x[1]):
        n22 = sum(1 for e in prof if e == (2, 2))
        has32 = any(e == (3, 2) for e in prof)
        sj = n22 + (3 if has32 else 0)
        derived[sj] = derived.get(sj, 0) + cnt
        print(f"{str(prof):>44} {cnt:>6} {n22:>7} {str(has32):>9} "
              f"{sj:>6}")

    print()
    print("=== derived sum_j marginal ===")
    print(f"  {dict(sorted(derived.items()))}")

    print()
    print("=== measured sum_j marginal (all cases) ===")
    meas = {}
    for (case, w, sj), cnt in CASE_TABLE.items():
        meas[sj] = meas.get(sj, 0) + cnt
    print(f"  {dict(sorted(meas.items()))}")
    print(f"  match: {derived == meas}")

    print()
    print("=== the (3,2) circle is W, and it appears iff w = 2 ===")
    b_w2 = sum(v for k, v in CASE_TABLE.items() if k[0] == "B" and k[1] == 2)
    has32 = sum(v for prof, v in DATA.items() if any(e == (3, 2) for e in prof))
    print(f"  triples with w=2: {b_w2}")
    print(f"  triples with a (3,2) circle: {has32}")
    print(f"  match: {b_w2 == has32}")


if __name__ == "__main__":
    main()
