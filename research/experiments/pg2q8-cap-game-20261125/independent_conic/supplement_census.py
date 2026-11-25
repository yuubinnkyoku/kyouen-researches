"""Supplementary check S1: global cap census of PG(2,8) derived from the
per-base upset profiles of task 4, plus an independent hyperoval count,
compared with the parent experiment's published census.

The task-4 upsets are exact counts of caps containing a fixed conic k-cap.  For
k = 3,4,5 PGL(3,8) is transitive on k-caps (every 3-, 4- and 5-arc of PG(2,8)
is equivalent), so the counts give the total number n_j of j-caps by
    n_j = (# j-caps containing the base k-cap) * n_k / C(j,k).
The three bases k=3,4,5 give three independent estimates for each j >= 6, so
their agreement is a strong consistency check.

For k = 6,7,8 this normalisation is INVALID: PGL(3,8) is not transitive on
6-caps (a 6-subset of a conic is not equivalent to "5 conic points + nucleus",
e.g. {n} + 5 points of C is a 6-cap lying on no conic), so the number of
j-caps containing one special conic 6-cap cannot be rescaled by n_6/C(j,6).
This is why only the k=3,4,5 upsets are used below.

Run:  python supplement_census.py
"""

from __future__ import annotations

import json
import os
import random
import sys
from math import comb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pg8

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.join(HERE, os.pardir, "output", "board_pg2q8.txt")


def main():
    print("=" * 78)
    print("SUPPLEMENT S1 - PG(2,8) cap census and hyperoval count")
    print("=" * 78)
    board = pg8.Board(BOARD)
    LOP = board.line_of_pair
    rnd = random.Random(7)

    # --- direct brute force for sizes 3 and 4 ----------------------------
    print("\n-- brute force counts -----------------------------------------")
    n3 = comb(73, 3) - 73 * comb(9, 3)
    print(f"  n_3 = C(73,3) - 73*C(9,3) = {comb(73,3)} - {73*comb(9,3)} = {n3}")
    n4 = 0
    sample4 = []
    for a in range(73):
        for b in range(a + 1, 73):
            lab = LOP[a][b]
            for c in range(b + 1, 73):
                lac = LOP[a][c]
                if lac == lab:
                    continue
                lbc = LOP[b][c]
                for d in range(c + 1, 73):
                    if LOP[a][d] == lab or LOP[a][d] == lac or LOP[b][d] == lbc:
                        continue
                    n4 += 1
                    if len(sample4) < 400:
                        sample4.append((a, b, c, d))
                    elif rnd.random() < 0.01:
                        sample4[rnd.randrange(len(sample4))] = (a, b, c, d)
    print(f"  n_4 by enumerating all C(73,4) = {comb(73,4)} 4-subsets : {n4}")
    exts = set()
    for S in sample4[:300]:
        mask = 0
        for p in S:
            mask |= 1 << p
        forb = 0
        for i in range(4):
            for j in range(i + 1, 4):
                forb |= board.line_mask_of_pair[S[i]][S[j]]
        exts.add((board.FULL & ~forb & ~mask).bit_count())
    n5 = n4 * 30 // 5
    print(f"  #extensions of 300 random 4-caps (expect {{30}})          : {exts}")
    print(f"  n_5 = n_4*30/5                                          : {n5}")

    # --- derive n_j from the k = 3,4,5 upsets ---------------------------
    with open(os.path.join(HERE, "results_grundy.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    profiles = {}
    for k in range(3, 9):
        r = data["results"][str(k)]
        profiles[k] = (
            {int(s): c for s, c in r["upset_profile"].items()},
            {int(s): c for s, c in r["maximal_counts"].items()},
        )
    nk = {3: n3, 4: n4, 5: n5}
    print("\n-- n_j from the k=3,4,5 upsets (three independent estimates) -")
    for j in range(6, 11):
        vals = [profiles[k][0][j] * nk[k] / comb(j, k) for k in (3, 4, 5)]
        same = max(vals) - min(vals) < 1e-9
        nk[j] = round(vals[0])
        print(f"  n_{j:<2d} = " + "  ".join(f"{v:.0f}" for v in vals)
              + ("   consistent" if same else "   INCONSISTENT"))
    print("\n  (bases k=6,7,8 are NOT used: PGL(3,8) is not transitive on")
    print("   6-caps, so n_j = a_j*n_6/C(j,6) does not hold for them; the raw")
    print("   rescaling from the k=6 base is off by the constant factor 13/10.)")

    # --- maximal caps -----------------------------------------------------
    print("\n-- maximal caps of PG(2,8) -----------------------------------")
    max6 = [profiles[k][1][6] * nk[k] / comb(6, k) for k in (3, 4, 5)]
    max10 = [profiles[k][1][10] * nk[k] / comb(10, k) for k in (3, 4, 5)]
    print(f"  maximal 6-caps  (bases 3,4,5): " + "  ".join(f"{v:.0f}" for v in max6))
    print(f"  maximal 10-caps (bases 3,4,5): " + "  ".join(f"{v:.0f}" for v in max10))

    # --- independent hyperoval count: conic + nucleus ---------------------
    print("\n-- independent hyperoval count (conic + its nucleus) ----------")
    conics = {}
    for co in pg8.all_canonical_forms():
        zs = pg8.zero_set_fast(co)
        if len(zs) == 9 and board.is_cap(zs):
            conics[frozenset(zs)] = co
    print(f"  conics                                            : {len(conics)}")
    hyp = set()
    nuc_bad = 0
    for zs, co in conics.items():
        M = pg8.polar_matrix(co)
        rad = pg8.nullspace_basis(M, 3)
        assert len(rad) == 1
        nv = pg8.vcanon(tuple(rad[0]))
        npt = pg8.PIDX[nv]
        if npt in zs:
            nuc_bad += 1
        h = frozenset(zs | {npt})
        if len(h) != 10 or not board.is_cap(h):
            nuc_bad += 1
        hyp.add(h)
    print(f"  nucleus on its conic (must be 0)                   : {nuc_bad}")
    print(f"  distinct hyperovals  conic + nucleus               : {len(hyp)}")
    print(f"  each conic lies in exactly one hyperoval           : {len(hyp) == len(conics)}")
    print(f"  every conic is 1 of the C(9,6)=84 conic 6-subsets of its hyperoval")
    print(f"  => #conic-6-subsets = 32704*84 = {32704*84}")

    # --- total cap count --------------------------------------------------
    total = 1 + 73 + comb(73, 2) + sum(nk[j] for j in range(3, 11))
    print("\n-- total number of caps of PG(2,8) (all sizes 0..10) ---------")
    print("  1 (empty) + 73 (1-caps) + 2628 (2-caps) + sum_(3..10) n_j")
    print(f"  = {total}")
    print("  parent README census (PG(2,8))     : 19,550,350   ->",
          total == 19550350)
    print("  parent README maximal 6-caps       : 2,060,352    ->",
          {round(v) for v in max6} == {2060352})
    print("  parent README maximal 10-caps      : 32,704       ->",
          {round(v) for v in max10} == {32704})

    print("\n-- PG(2,8) caps by size --------------------------------------")
    for j in range(3, 11):
        print(f"  n_{j:<2d} = {nk[j]:,}")
    print(f"  (n_1 = 73, n_2 = 2,628, n_0 = 1; total {total:,})")

    ok = (
        exts == {30}
        and total == 19550350
        and {round(v) for v in max6} == {2060352}
        and {round(v) for v in max10} == {32704}
        and nuc_bad == 0
        and len(hyp) == 32704
        and len(hyp) == len(conics)
    )
    print("\nSUPPLEMENT S1:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
