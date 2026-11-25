#!/usr/bin/env python3
"""Branch-and-bound search for a 14-set in board_q7 with <=4 points per circle.

Uses the verified model: PGL(2,49) is 3-transitive on the 50 points, so WLOG a
14-set contains the three points 0, 7 and 49 (field 0, field 1, infinity).
We search only for such sets.
"""
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import explore

Q = 7
TARGET = 14
S = 4
FIXED = (0, 7, 49)


def main():
    board = explore.Board(explore.load_board(Q))
    v = board.v
    b = board.b
    blocks = board.blocks
    masks = board.masks
    pb = board.point_blocks
    assert len(blocks) == 350

    A = 0
    counts = [0] * b
    for p in FIXED:
        A |= 1 << p
        for bi in pb[p]:
            counts[bi] += 1
    U = ((1 << v) - 1) & ~A
    # propagate blocks already at capacity
    for bi, c in enumerate(counts):
        if c >= S:
            U &= ~masks[bi]
    # fixed points count
    base_sel = len(FIXED)

    sys.setrecursionlimit(10000)
    t0 = time.time()
    nodes = 0
    leaves = 0
    found = []

    # Precompute per-point block masks / point masks
    block_masks = masks

    def upper_bound_moments(sel, U, counts):
        """Return max m with 8*C(m,2)<=S2 and C(m,3)<=S3, where S2=sum C(r,2)."""
        S2 = 0
        S3 = 0
        for bi in range(b):
            r = S - counts[bi]
            if r >= 2:
                S2 += r * (r - 1) // 2
            if r >= 3:
                S3 += r * (r - 1) * (r - 2) // 6
        best = 0
        for m in range(1, U.bit_count() + 1):
            if 8 * (m * (m - 1) // 2) <= S2 and (m * (m - 1) * (m - 2) // 6) <= S3:
                best = m
            else:
                break
        return best

    def choose_point(U, counts):
        # score points by sum of squares of current block counts
        best_p = -1
        best_score = -1
        u = U
        while u:
            low = u & -u
            p = low.bit_length() - 1
            u ^= low
            sc = 0
            for bi in pb[p]:
                c = counts[bi]
                sc += c * c
                if c == S - 1:
                    sc += 8  # emphasise near-saturation
            if sc > best_score:
                best_score = sc
                best_p = p
        return best_p

    def dfs(A, U, sel, counts):
        nonlocal nodes, leaves
        nodes += 1
        if nodes % 1000000 == 0:
            print(f"  nodes={nodes} sel={sel} avail={U.bit_count()} elapsed={time.time()-t0:.1f}s", flush=True)
        if sel == TARGET:
            found.append(A)
            return True
        if sel + U.bit_count() < TARGET:
            return False
        ub = upper_bound_moments(sel, U, counts)
        if sel + ub < TARGET:
            return False
        p = choose_point(U, counts)
        if p < 0:
            return False
        # branch 1: include p
        if (U >> p) & 1:
            A2 = A | (1 << p)
            U2 = U & ~(1 << p)
            counts2 = counts[:]
            touched = []
            ok = True
            for bi in pb[p]:
                counts2[bi] += 1
                if counts2[bi] > S:
                    ok = False
                    break
                if counts2[bi] == S:
                    touched.append(bi)
            if ok:
                for bi in touched:
                    U2 &= ~block_masks[bi]
                if dfs(A2, U2, sel + 1, counts2):
                    return True
        # branch 2: exclude p
        U3 = U & ~(1 << p)
        if dfs(A, U3, sel, counts):
            return True
        return False

    res = dfs(A, U, base_sel, counts)
    print("result:", res, "nodes:", nodes, "leaves:", leaves, "seconds:", time.time() - t0)
    if found:
        mask = found[0]
        witness = [i for i in range(v) if (mask >> i) & 1]
        print("witness:", witness, "size", len(witness))
        print("verify:", explore.check_set(board, witness, S))


if __name__ == "__main__":
    main()
