#!/usr/bin/env python3
"""Complete independent Grundy computation for PG(2,5), s=3, in pure Python.

Starting from the empty position, recursively expand every legal move with
memoisation.  Because every subset of a safe position is safe, this reaches
exactly the set of all safe positions (7,906,892 of them).  Per-size and
per-Grundy counts, maximal-position counts and the root value are accumulated
during the single traversal.

This is a third implementation, independent of both C programs: Python ints,
explicit line-count test, recursive mex.  It is slower (~5 min) but directly
computes the full GSIZE table.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.abspath(os.path.join(
    HERE, "..", "..", "projective-blocking-kyouen-20261125",
    "output", "board_pg2q5.txt"))
N = 31
FULL = (1 << N) - 1

lmask = []
point_lines = [[] for _ in range(N)]


def load():
    with open(BOARD, encoding="utf-8") as f:
        tok = f.read().split()
    it = iter(tok)
    n = int(next(it)); b = int(next(it))
    assert n == N and b == 31, (n, b)
    for _ in range(b):
        ln = int(next(it))
        pts = [int(next(it)) for _ in range(ln)]
        m = 0
        for p in pts:
            m |= 1 << p
            point_lines[p].append(len(lmask))
        lmask.append(m)


load()

memo = {}
gsize = [[0] * 64 for _ in range(N + 1)]
maximal = [0] * (N + 1)


def legal(mask, p):
    for c in point_lines[p]:
        if (mask & lmask[c]).bit_count() >= 3:
            return False
    return True


sys.setrecursionlimit(10000)


def g(mask):
    """Return (grundy | misere_win << 8) for mask, memoised.

    misere_win = 1 iff the player to move wins under the convention that a
    player with no move wins (same convention as the C engines).
    """
    e = memo.get(mask)
    if e is not None:
        return e
    seen = 0
    nmoves = 0
    win = 0
    rest = FULL ^ mask
    while rest:
        bit = rest & -rest
        p = bit.bit_length() - 1
        if legal(mask, p):
            child = g(mask | bit)
            seen |= 1 << (child & 255)
            nmoves += 1
            if not ((child >> 8) & 1):
                win = 1
        rest ^= bit
    if nmoves == 0:
        v = 0
        win = 1
        maximal[mask.bit_count()] += 1
    else:
        v = 0
        while (seen >> v) & 1:
            v += 1
    e = v | (win << 8)
    memo[mask] = e
    gsize[mask.bit_count()][v] += 1
    return e


def main():
    t0 = time.time()
    root_e = g(0)
    root = root_e & 255
    root_win = (root_e >> 8) & 1
    elapsed = time.time() - t0

    total = sum(sum(row) for row in gsize)
    print(f"# python full DP: {total} positions, {len(memo)} memo entries, "
          f"{elapsed:.1f}s", file=sys.stderr)
    print("POINTS 31")
    print("CIRCLES 31")
    print(f"SAFE {total}")
    print(f"ROOT {root} {root_win}")
    for s in range(N + 1):
        if sum(gsize[s]) == 0 and s > 0:
            continue
        print(f"SIZE {s} {sum(gsize[s])} {maximal[s]} {gsize[s][0]}")
    for v in range(64):
        c = sum(gsize[s][v] for s in range(N + 1))
        if c:
            print(f"GRUNDY {v} {c}")
    for s in range(N + 1):
        for v in range(64):
            if gsize[s][v]:
                print(f"GSIZE {s} {v} {gsize[s][v]}")

    out = {
        "total": total,
        "root": root,
        "root_misere_win": root_win,
        "elapsed_seconds": round(elapsed, 1),
        "memo_entries": len(memo),
        "sizes": {str(s): sum(gsize[s]) for s in range(N + 1) if sum(gsize[s])},
        "maximal": {str(s): maximal[s] for s in range(N + 1) if maximal[s]},
        "gsize": {f"{s},{v}": gsize[s][v]
                  for s in range(N + 1) for v in range(64) if gsize[s][v]},
    }
    with open(os.path.join(HERE, "out", "python_full_dp.json"), "w",
              encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
