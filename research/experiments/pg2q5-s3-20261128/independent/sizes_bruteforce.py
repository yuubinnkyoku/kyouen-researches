#!/usr/bin/env python3
"""Brute-force SIZE counts for small k by iterating k-subsets directly.

This is yet another enumeration method (itertools.combinations over all
C(31,k) subsets, direct line test) used as a cross-check of the DFS-based
counts for k = 4..7.
"""
import itertools
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.abspath(os.path.join(
    HERE, "..", "..", "projective-blocking-kyouen-20261125",
    "output", "board_pg2q5.txt"))


def load():
    with open(BOARD, encoding="utf-8") as f:
        tok = f.read().split()
    it = iter(tok)
    n = int(next(it)); b = int(next(it))
    masks = []
    for _ in range(b):
        ln = int(next(it))
        m = 0
        for _ in range(ln):
            m |= 1 << int(next(it))
        masks.append(m)
    return n, masks


def main():
    n, lmask = load()
    assert n == 31
    expected = {4: 31000, 5: 158100, 6: 592100, 7: 1550000}
    for k in (4, 5, 6, 7):
        t0 = time.time()
        cnt = 0
        for comb in itertools.combinations(range(n), k):
            m = 0
            for p in comb:
                m |= 1 << p
            ok = True
            for L in lmask:
                if (m & L).bit_count() > 3:
                    ok = False
                    break
            if ok:
                cnt += 1
        print(f"k={k}: {cnt} (claimed {expected[k]}) "
              f"{'OK' if cnt == expected[k] else 'MISMATCH'} "
              f"{time.time()-t0:.1f}s", flush=True)
    print("done")


if __name__ == "__main__":
    main()
