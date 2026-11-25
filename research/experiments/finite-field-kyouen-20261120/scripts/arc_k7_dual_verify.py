"""k=7: aggregating the dual (per-triple) distributions.

MEASURED (q=5): 9 distinct (case, (w,u)-distribution-over-T) types, with
multiplicities 240, 240, 180, 120, 120, 120, 60, 40, 20 (total 1140).

Each type contributes its distribution times its multiplicity to the
overall (w,u) count.  Let me verify that the aggregation reproduces the
measured (w,u) distribution:

    (0,1):16  (0,2):100  (0,3):416  (0,4):152  (0,5):16
    (1,1):48  (1,2):224  (1,3):48
    (2,0):32  (2,1):88

Run:  python arc_k7_dual_verify.py
"""

from __future__ import annotations

from collections import Counter

# (case, ((w,u), count)..., ) -> multiplicity
TYPES = {
    ("A", (((0, 1), 1), ((0, 2), 2), ((0, 3), 11), ((0, 4), 1))): 240,
    ("A", (((0, 3), 2), ((0, 4), 3), ((1, 1), 3), ((1, 2), 6),
           ((1, 3), 1))): 240,
    ("B", (((0, 4), 1), ((1, 2), 8), ((2, 1), 2), ((2, 2), 4))): 180,
    ("A", (((0, 2), 1), ((0, 3), 11), ((0, 4), 2), ((0, 5), 1))): 120,
    ("B", (((0, 5), 1), ((1, 2), 4), ((1, 3), 4), ((2, 1), 1),
           ((2, 2), 5))): 120,
    ("A", (((0, 2), 5), ((0, 3), 8), ((0, 4), 2))): 120,
    ("A", (((0, 2), 2), ((0, 3), 8), ((0, 4), 5))): 60,
    ("A", (((0, 3), 6), ((0, 4), 9))): 40,
    ("A", (((0, 2), 9), ((0, 3), 6))): 20,
}

MEASURED = {
    (0, 1): 16, (0, 2): 100, (0, 3): 416, (0, 4): 152, (0, 5): 16,
    (1, 1): 48, (1, 2): 224, (1, 3): 48,
    (2, 0): 32, (2, 1): 88,
}


def main() -> None:
    print("=== aggregating the 9 dual types ===")
    print("  NOTE: the dual view fixes the TRIPLE and varies T over all")
    print("  C(s,4)=15 subsets of C.  The primal view fixes T and varies the")
    print("  triple.  So the dual counts are (triple, T) pairs; dividing by")
    print("  C(s,4) converts to the primal (T, triple) count.")
    print()
    agg = Counter()
    for (case, dist), mult in TYPES.items():
        for wu, cnt in dist:
            agg[wu] += cnt * mult

    # convert: divide by C(s,4) = 15.
    # The dual view counts involution pairs inside T.  For w = 2 the
    # common pair W cap C IS an involution pair (it lies in all three
    # involutions), so the dual count includes it ONCE.  The primal u
    # EXCLUDES W, so subtract 1 when w = 2.
    agg_primal = {}
    for k, v in agg.items():
        w, u = k
        uu = u - 1 if w == 2 else u
        agg_primal[(w, uu)] = agg_primal.get((w, uu), 0) + v // 15

    print(f"{'w':>3} {'u':>3} {'dual':>8} {'/15':>8} {'measured':>10} "
          f"{'ok':>4}")
    all_ok = True
    for key in sorted(set(agg_primal) | set(MEASURED)):
        a = agg_primal.get(key, 0)
        m = MEASURED.get(key, 0)
        ok = a == m
        all_ok = all_ok and ok
        print(f"{key[0]:>3} {key[1]:>3} {agg.get(key,0):>8} {a:>8} {m:>10} "
              f"{str(ok):>4}")
    print(f"  all match: {all_ok}")

    print()
    print("=== totals ===")
    print(f"  sum of multiplicities: {sum(TYPES.values())}")
    print(f"  sum of aggregated (w,u): {sum(agg.values())}")
    print(f"  each type's distribution sums to C(s,4) = 15: "
          f"{all(sum(c for _, c in d) == 15 for (_, d) in TYPES)}")

    print()
    print("=== per-type distribution sums ===")
    for (case, dist), mult in sorted(TYPES.items(), key=lambda x: -x[1]):
        tot = sum(c for _, c in dist)
        print(f"  {case} mult={mult}: distribution sums to {tot}")


if __name__ == "__main__":
    main()
