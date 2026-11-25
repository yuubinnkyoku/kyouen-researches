"""AG(2,9): structure of 10-point sets, and a randomized search for a witness.

Facts used (all verified in ag9_board.py):

  * 819 blocks = 90 lines (9 pts) + 648 non-degenerate conics (8 pts)
    + 81 crosses (17 pts), where the cross at (s0,t0) is
    column s0 union row t0.
  * every point is on 91 blocks.

Because the crosses are blocks, a safe set S satisfies
    |S cap (col s0 union row t0)| = c[s0] + r[t0] - [S n (s0,t0)] <= 3
for all (s0,t0), where c[s] = |S cap col s| and r[t] = |S cap row t|.

This script
  1. derives the resulting classification of 10-point candidates,
  2. counts them exactly (DP over columns),
  3. runs a randomized greedy / repair search for an actual witness.
"""

from __future__ import annotations

import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ag9_board import build_split_board  # noqa: E402

N = 81
Q = 9


def make_board():
    blocks, kinds = build_split_board()
    through = [[] for _ in range(N)]
    for bi, b in enumerate(blocks):
        for p in b:
            through[p].append(bi)
    return blocks, kinds, through


# ---------------------------------------------------------------- counting


def count_candidates() -> int:
    """Number of 10-subsets of the 9x9 grid with <=2 per row, <=2 per column,
    and satisfying the cross constraint."""
    # DP over columns; state = tuple of row counts (each 0..2)
    from functools import lru_cache
    from itertools import combinations

    start = (0,) * Q

    @lru_cache(maxsize=None)
    def rec(col: int, state: tuple) -> tuple:
        """returns tuple over total points placed -> count"""
        if col == Q:
            out = [0] * 11
            out[0] = 1
            return tuple(out)
        sub = rec(col + 1, state)  # not used directly; we need per-choice
        out = [0] * 11
        # choose 0, 1 or 2 rows for this column
        for k in (0, 1, 2):
            for rows in combinations(range(Q), k):
                if any(state[r] >= 2 for r in rows):
                    continue
                ns = list(state)
                for r in rows:
                    ns[r] += 1
                ns = tuple(ns)
                # cross constraint: this column has k points; for each row t,
                # c[col] + r[t] - [point present] <= 3
                ok = True
                for t in range(Q):
                    present = 1 if t in rows else 0
                    if k + ns[t] - present > 3:
                        ok = False
                        break
                if not ok:
                    continue
                tail = rec(col + 1, ns)
                for tot in range(11 - k):
                    if tail[tot]:
                        out[tot + k] += tail[tot]
        return tuple(out)

    res = rec(0, start)
    return res[10]


# ---------------------------------------------------------------- search


def randomized_search(seed: int, target: int = 10, restarts: int = 20000):
    blocks, kinds, through = make_board()
    rng = random.Random(seed)
    best = 0
    best_set = None
    for _ in range(restarts):
        cnt = [0] * blocks.__len__()
        S: list[int] = []
        inS = [False] * N
        rowcnt = [0] * Q
        colcnt = [0] * Q
        while len(S) < target:
            cands = []
            for p in range(N):
                if inS[p]:
                    continue
                s, t = p // Q, p % Q
                if rowcnt[t] >= 2 or colcnt[s] >= 2:
                    continue
                ok = True
                for b in through[p]:
                    if cnt[b] >= 3:
                        ok = False
                        break
                if ok:
                    cands.append(p)
            if not cands:
                break
            p = rng.choice(cands)
            s, t = p // Q, p % Q
            S.append(p)
            inS[p] = True
            rowcnt[t] += 1
            colcnt[s] += 1
            for b in through[p]:
                cnt[b] += 1
        if len(S) > best:
            best = len(S)
            best_set = list(S)
            print(f"  restart: new best {best}", flush=True)
        if len(S) == target:
            return S, best
    return None, best


def verify(S, blocks) -> bool:
    for b in blocks:
        if len(set(b) & set(S)) >= 4:
            return False
    return True


def main() -> None:
    blocks, kinds, through = make_board()
    print(f"blocks: {len(blocks)}, kinds: {Counter(kinds)}")
    print(f"block sizes: {Counter(len(b) for b in blocks)}")

    # sanity: every point on 91 blocks
    assert all(len(through[p]) == 91 for p in range(N))

    print("\ncounting 10-candidates with <=2 per row/col and cross constraint ...")
    c = count_candidates()
    print(f"  candidates: {c:,}")

    print("\nrandomized greedy search ...")
    for seed in range(4):
        S, best = randomized_search(seed, target=10, restarts=3000)
        print(f"  seed {seed}: best {best}, found={S is not None}")
        if S is not None:
            print(f"  WITNESS: {sorted(S)}")
            print(f"  verified: {verify(S, blocks)}")
            return
    print("\nno witness from randomized greedy.")


if __name__ == "__main__":
    main()
