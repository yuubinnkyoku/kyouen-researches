"""Task 5: parity-theorem consequence.

If every maximal extension of a position S has even size (terminal sizes
6-caps and 10-caps, both even), the parity theorem gives
    Grundy(S) = (p - |S|) mod 2,   p = 0  (mod 2),
so for the conic k-caps:  Grundy = (10 - k) mod 2 = k mod 2.

This script (a) checks that consequence on the task-4 data and (b) verifies the
parity theorem itself on EVERY position reached by the task-4 DP: for each
position whose maximal extensions all have the same parity p it checks
Grundy(S) == (p - |S|) mod 2.

Run:  python task5_parity.py
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pg8
from task4_grundy import CapGame

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.join(HERE, os.pardir, "output", "board_pg2q8.txt")


def main():
    print("=" * 78)
    print("TASK 5 - parity-theorem consequence")
    print("=" * 78)
    board = pg8.Board(BOARD)
    info = pg8.find_conic_through(pg8.BASE_5CAP)
    C = sorted(info["zero_set"])
    with open(os.path.join(HERE, "results_grundy.json"), encoding="utf-8") as fh:
        data = json.load(fh)

    print("\n-- (a) consequence check on the six representatives --------------")
    print(f"  {'k':>2}  {'base':>26}  {'terminal sizes':>14}  {'all even':>8}  "
          f"{'Grundy':>6}  {'k mod 2':>7}  {'(10-k) mod 2':>12}  verdict")
    mismatch = []
    for k in range(3, 9):
        r = data["results"][str(k)]
        g = r["grundy"]
        term = r["maximal_sizes"]
        even = all(s % 2 == 0 for s in term)
        want = (10 - k) % 2
        ok = even and g == want and g == k % 2
        if not ok:
            mismatch.append(k)
        print(f"  {k:>2}  {str(r['base']):>26}  {str(term):>14}  {str(even):>8}  "
              f"{g:>6}  {k % 2:>7}  {want:>12}  {'OK' if ok else 'MISMATCH'}")

    # ---------------- (b) parity theorem on all DP positions -------------
    print("\n-- (b) parity theorem verified on every position of the task-4 DP -")
    game = CapGame(board)
    for k in range(3, 9):
        m = 0
        for p in C[:k]:
            m |= 1 << p
        game.grundy(m)
    memo = game.memo
    par = {}

    def parities(S):
        if S in par:
            return par[S]
        A = game.allowed_mask(S)
        if A == 0:
            r = {S.bit_count() % 2}
        else:
            r = set()
            mm = A
            while mm:
                b = mm & -mm
                r |= parities(S | b)
                mm ^= b
        par[S] = r
        return r

    uniform = 0
    mixed = 0
    bad = []
    for S in memo:
        r = parities(S)
        if len(r) == 1:
            uniform += 1
            p = next(iter(r))
            if memo[S] != (p - S.bit_count()) % 2:
                bad.append((S, memo[S], p))
        else:
            mixed += 1
    print(f"  positions in the DP memo                 : {len(memo)}")
    print(f"  positions with a single maximal parity p : {uniform}")
    print(f"  positions with both parities (p mixed)   : {mixed}")
    print(f"  parity-theorem violations among uniform  : {len(bad)}")
    if bad[:5]:
        print("   first violations:", bad[:5])

    # distribution of Grundy values by size, for information
    print("\n-- Grundy by position size (over the whole DP memo) --------------")
    from collections import Counter
    tab = {}
    for S, g in memo.items():
        tab.setdefault(S.bit_count(), Counter())[g] += 1
    for size in sorted(tab):
        print(f"  size {size:2d}: " + ", ".join(
            f"G={g}:{c}" for g, c in sorted(tab[size].items())))

    ok = (not mismatch) and (not bad)
    print("\nTASK 5:", "PASS" if ok else "FAIL",
          "" if ok else f"(mismatches: {mismatch}, parity violations: {bad[:3]})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
