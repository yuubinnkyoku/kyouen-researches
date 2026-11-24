#!/usr/bin/env python3
"""Independent Python enumeration of all s=2-safe sets (caps).

Algorithm (deliberately different from the C engine):
  - the current position S keeps an explicit list of its bisecant lines
    (all lines through pairs of points of S; for a cap these are exactly the
    lines carrying 2 points of S);
  - the set of forbidden points is recomputed from scratch at every node as
    the union of the bisecant-line point sets;
  - children are found by iterating the bits of the allowed-point mask with
    increasing point index, so every safe set is produced exactly once.

Counts, per-size maximal counts and a per-size 64-bit checksum
(sum of splitmix64(mask) mod 2^64) are written to JSON.  With --dump the masks
are also written to a binary file (uint64 count, then count uint64 masks,
for sizes 0..maxsize) for the independent Python Grundy DP.

Usage:
  python count_caps_py.py <board> <tag> [--dump <file>]
"""

import json
import os
import struct
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
M64 = (1 << 64) - 1


def read_board(path):
    with open(path, "r", encoding="utf-8") as f:
        toks = f.read().split()
    it = iter(toks)
    n = int(next(it))
    b = int(next(it))
    lines = []
    for _ in range(b):
        k = int(next(it))
        lines.append(tuple(int(next(it)) for _ in range(k)))
    return n, lines


def splitmix64(x):
    x = (x + 0x9E3779B97F4A7C15) & M64
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & M64
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & M64
    return (x ^ (x >> 31)) & M64


def enumerate_caps(n, lines, store=False):
    b = len(lines)
    line_masks = []
    for L in lines:
        m = 0
        for p in L:
            m |= 1 << p
        line_masks.append(m)
    pair_line = [[-1] * n for _ in range(n)]
    for li, L in enumerate(lines):
        for i in range(len(L)):
            p = L[i]
            row = pair_line[p]
            for j in range(i + 1, len(L)):
                row[L[j]] = li
                pair_line[L[j]][p] = li

    full = (1 << n) - 1
    counts = [0] * (n + 1)
    maximal = [0] * (n + 1)
    chk = [0] * (n + 1)
    mchk = [0] * (n + 1)
    buckets = [[] for _ in range(n + 1)]
    sat = []  # bisecant line indices of the current position

    sys.setrecursionlimit(10000)

    def dfs(start, S, sz):
        counts[sz] += 1
        chk[sz] = (chk[sz] + splitmix64(S)) & M64
        if store:
            buckets[sz].append(S)
        U = 0
        for l in sat:
            U |= line_masks[l]
        forbidden = S | U
        if forbidden == full:
            maximal[sz] += 1
            mchk[sz] = (mchk[sz] + splitmix64(S)) & M64
        cand = full & ~forbidden & ~((1 << start) - 1)
        while cand:
            bit = cand & -cand
            cand ^= bit
            p = bit.bit_length() - 1
            row = pair_line[p]
            before = len(sat)
            t = S
            while t:
                qb = t & -t
                t ^= qb
                sat.append(row[qb.bit_length() - 1])
            dfs(p + 1, S | bit, sz + 1)
            del sat[before:]

    t0 = time.time()
    dfs(0, 0, 0)
    elapsed = time.time() - t0
    return counts, maximal, chk, line_masks, elapsed, buckets, mchk


def main():
    if len(sys.argv) < 3:
        print("usage: count_caps_py.py <board> <tag> [--dump file]")
        return 2
    board = sys.argv[1]
    tag = sys.argv[2]
    dump = None
    if len(sys.argv) >= 5 and sys.argv[3] == "--dump":
        dump = sys.argv[4]
    n, lines = read_board(board)
    counts, maximal, chk, line_masks, elapsed, buckets, mchk = enumerate_caps(
        n, lines, store=(dump is not None))
    max_size = max(i for i, c in enumerate(counts) if c)
    total = sum(counts)
    out = {
        "tag": tag,
        "n": n,
        "b": len(lines),
        "safe": total,
        "max_size": max_size,
        "counts": counts[:max_size + 1],
        "maximal": maximal[:max_size + 1],
        "checksums": chk[:max_size + 1],
        "maximal_checksums": mchk[:max_size + 1],
        "seconds": round(elapsed, 3),
    }
    path = os.path.join(HERE, tag + "_py_enum.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    if dump:
        from array import array
        with open(dump, "wb") as f:
            for sz in range(max_size + 1):
                f.write(struct.pack("<Q", counts[sz]))
                array("Q", buckets[sz]).tofile(f)
        print("wrote", dump)
    return 0


if __name__ == "__main__":
    sys.exit(main())
