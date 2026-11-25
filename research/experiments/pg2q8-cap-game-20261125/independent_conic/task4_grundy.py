"""Task 4: independent Grundy values of the conic k-caps (k = 3..8) in the
s=2 cap game on PG(2,8).

Game (standard normal play): position = a cap S (a set of points meeting every
line in at most 2 points).  A move adds one point while keeping the set a cap.
The player unable to move loses;  Grundy(S) = mex{ Grundy(S + p) }.

For each k = 3..8 one representative conic k-cap is taken (the k smallest
points of C; task 3 showed all k-subsets of C are a single PGL(2,8) orbit) and
the whole upset  { S : base subset of S, S a cap }  is enumerated by memoised
DFS, recording the upset profile and every maximal (terminal) extension size.

Run:  python task4_grundy.py
Writes results_grundy.json next to this file.
"""

from __future__ import annotations

import itertools
import json
import os
import random
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pg8

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.join(HERE, os.pardir, "output", "board_pg2q8.txt")


class CapGame:
    def __init__(self, board):
        self.board = board
        self.FULL = board.FULL
        self.LINE = board.line_mask_of_pair
        self.npoints = board.npoints
        self.memo = {}
        self.calls = 0

    def allowed_mask(self, mask):
        """Points p not in mask such that mask+p is still a cap."""
        pts = []
        m = mask
        while m:
            b = m & -m
            pts.append(b.bit_length() - 1)
            m ^= b
        forb = 0
        n = len(pts)
        for i in range(n):
            Li = self.LINE[pts[i]]
            for j in range(i + 1, n):
                forb |= Li[pts[j]]
        return self.FULL & ~forb & ~mask

    def grundy(self, mask):
        self.calls += 1
        g = self.memo.get(mask)
        if g is not None:
            return g
        A = self.allowed_mask(mask)
        if A == 0:
            self.memo[mask] = 0
            return 0
        seen = set()
        m = A
        while m:
            b = m & -m
            seen.add(self.grundy(mask | b))
            m ^= b
        g = 0
        while g in seen:
            g += 1
        self.memo[mask] = g
        return g

    def upset(self, base):
        """All caps containing base (uses the same allowed-move generator)."""
        seen = {base}
        stack = [base]
        while stack:
            S = stack.pop()
            m = self.allowed_mask(S)
            while m:
                b = m & -m
                T = S | b
                if T not in seen:
                    seen.add(T)
                    stack.append(T)
                m ^= b
        return seen

    def terminal_from(self, base):
        """Maximal extensions of base reached by the upset + their Grundy."""
        out = Counter()
        stack = [base]
        seen = {base}
        while stack:
            S = stack.pop()
            A = self.allowed_mask(S)
            if A == 0:
                out[S.bit_count()] += 1
                continue
            m = A
            while m:
                b = m & -m
                T = S | b
                if T not in seen:
                    seen.add(T)
                    stack.append(T)
                m ^= b
        return out

    # ---------- slow but obviously-correct reference implementation ----------
    def allowed_naive(self, mask):
        board = self.board
        S = [i for i in range(self.npoints) if (mask >> i) & 1]
        out = []
        for p in range(self.npoints):
            if (mask >> p) & 1:
                continue
            good = True
            for a, b in itertools.combinations(S, 2):
                if (board.line_of_pair[a][b] == board.line_of_pair[a][p]
                        == board.line_of_pair[b][p]):
                    good = False
                    break
            if good:
                out.append(p)
        return out


def bits(mask):
    out = []
    m = mask
    while m:
        b = m & -m
        out.append(b.bit_length() - 1)
        m ^= b
    return out


def main():
    t0 = time.time()
    print("=" * 78)
    print("TASK 4 - Grundy values of the conic k-caps in the s=2 cap game")
    print("=" * 78)
    board = pg8.Board(BOARD)
    info = pg8.find_conic_through(pg8.BASE_5CAP)
    C = sorted(info["zero_set"])
    print("conic C:", C)
    game = CapGame(board)

    results = {}
    for k in range(3, 9):
        base = C[:k]
        mask = 0
        for p in base:
            mask |= 1 << p
        assert board.is_cap(base)
        g = game.grundy(mask)
        up = game.upset(mask)
        prof = Counter(S.bit_count() for S in up)
        term = game.terminal_from(mask)
        maxsizes = sorted(term)
        even = all(s % 2 == 0 for s in maxsizes)
        print(f"\n---- k = {k}: base = {base}  (conic k-cap) -------------------")
        print(f"  Grundy(base)                 : {g}")
        print(f"  |upset| (caps containing base): {len(up)}")
        print(f"  upset profile (size: count)  : {dict(sorted(prof.items()))}")
        print(f"  maximal extension sizes      : {maxsizes}")
        print(f"  #maximal extensions by size  : {dict(sorted(term.items()))}")
        print(f"  all maximal sizes even       : {even}")
        print(f"  k mod 2                      : {k % 2}   "
              f"(10-k) mod 2: {(10 - k) % 2}")
        results[k] = {
            "base": base,
            "grundy": g,
            "upset_size": len(up),
            "upset_profile": {str(s): c for s, c in sorted(prof.items())},
            "maximal_sizes": maxsizes,
            "maximal_counts": {str(s): c for s, c in sorted(term.items())},
            "all_maximal_even": even,
        }

    # ---------------- cross-check against a naive implementation ----------
    print("\n-- cross-check: naive move generator vs bitmask generator -----")
    rnd = random.Random(20261125)
    sample = list(game.memo.keys())
    bad = 0
    for mask in rnd.sample(sample, min(300, len(sample))):
        if set(bits(game.allowed_mask(mask))) != set(game.allowed_naive(mask)):
            bad += 1
    print(f"  sampled {min(300, len(sample))} memoised positions "
          f"(size 3..10): mismatches = {bad}")

    # independent naive Grundy for the two smallest upsets (k = 7, 8)
    print("\n-- independent naive Grundy recomputation (frozenset game tree) --")
    naive_ok = True
    for k in (8, 7):
        base = frozenset(C[:k])
        memo = {}

        def ng(S):
            if S in memo:
                return memo[S]
            S_l = list(S)
            moves = []
            for p in range(73):
                if p in S:
                    continue
                if board.is_cap(S_l + [p]):
                    moves.append(p)
            if not moves:
                memo[S] = 0
                return 0
            vals = {ng(S | {p}) for p in moves}
            g = 0
            while g in vals:
                g += 1
            memo[S] = g
            return g

        gn = ng(base)
        print(f"  k={k}: naive Grundy = {gn}; bitmask DP = {results[k]['grundy']}; "
              f"positions explored = {len(memo)}")
        naive_ok = naive_ok and (gn == results[k]["grundy"])

    # ---------------- Grundy is constant on the k-subset orbit ------------
    print("\n-- extra representatives (orbit-invariance spot check) --------")
    extra_ok = True
    for k in range(3, 9):
        subsets = list(itertools.combinations(C, k))
        picks = [subsets[0]] + rnd.sample(subsets, min(3, len(subsets)))
        vals = []
        for sub in picks:
            m = 0
            for p in sub:
                m |= 1 << p
            vals.append(game.grundy(m))
        same = all(v == results[k]["grundy"] for v in vals)
        extra_ok = extra_ok and same
        print(f"  k={k}: Grundy on {[list(p) for p in picks]} -> {vals} "
              f"{'OK' if same else 'MISMATCH'}")

    print(f"\n  DP memo size (all bases): {len(game.memo)}; "
          f"grundy() calls: {game.calls}; elapsed {time.time()-t0:.1f}s")

    with open(os.path.join(HERE, "results_grundy.json"), "w", encoding="utf-8") as fh:
        json.dump({"conic": C, "results": results,
                   "memo_positions": len(game.memo)}, fh, indent=1)
    print("  wrote results_grundy.json")

    ok = (
        all(results[k]["all_maximal_even"] for k in range(3, 9))
        and all(results[k]["grundy"] == k % 2 for k in range(3, 9))
        and bad == 0
        and naive_ok
        and extra_ok
    )
    print("\nTASK 4:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
