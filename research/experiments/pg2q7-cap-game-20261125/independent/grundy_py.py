#!/usr/bin/env python3
"""Independent Python Grundy / misere DP over all safe sets.

Reads a mask dump produced by count_caps_py.py --dump and a board file.
Processes sizes from the maximum downwards; the legal moves of S are the
points outside S that are not on a bisecant of S, i.e.
    cand = full & ~S & ~U,   U = union of lines with exactly 2 points of S.
Children (size+1) are already scored, so mex is immediate.  The misere win
flag is stored alongside: terminal => win (no move wins), otherwise win iff
some child is a misere loss.

Usage: python grundy_py.py <board> <dump> <tag>
"""

import json
import os
import struct
import sys
import time
from array import array

HERE = os.path.dirname(os.path.abspath(__file__))


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


def read_dump(path):
    buckets = []
    with open(path, "rb") as f:
        while True:
            raw = f.read(8)
            if not raw:
                break
            if len(raw) != 8:
                raise ValueError("truncated dump")
            cnt = struct.unpack("<Q", raw)[0]
            a = array("Q")
            a.fromfile(f, cnt)
            buckets.append(a)
    return buckets


def main():
    if len(sys.argv) < 4:
        print("usage: grundy_py.py <board> <dump> <tag>")
        return 2
    board, dump, tag = sys.argv[1], sys.argv[2], sys.argv[3]
    n, lines = read_board(board)
    line_masks = []
    for L in lines:
        m = 0
        for p in L:
            m |= 1 << p
        line_masks.append(m)
    full = (1 << n) - 1
    buckets = read_dump(dump)
    max_size = len(buckets) - 1
    counts = [len(a) for a in buckets]
    total = sum(counts)
    assert total == sum(counts)

    g = {}
    t0 = time.time()
    for sz in range(max_size, -1, -1):
        for S in buckets[sz]:
            U = 0
            for lm in line_masks:
                if (S & lm).bit_count() == 2:
                    U |= lm
                    if (S | U) == full:
                        break
            cand = full & ~S & ~U
            seen = 0
            win = 0
            c = cand
            while c:
                bit = c & -c
                c ^= bit
                v = g[S | bit]
                seen |= 1 << (v & 0x0F)
                if not (v & 0x80):
                    win = 1
            gg = 0
            while (seen >> gg) & 1:
                gg += 1
            if cand == 0:
                gg = 0
                win = 1
            g[S] = gg | (0x80 if win else 0)
    elapsed = time.time() - t0

    gdist = {}
    per_size = []
    win_total = loss_total = parity_mismatch = 0
    for sz in range(max_size + 1):
        gd = {}
        w = ls = 0
        for S in buckets[sz]:
            v = g[S]
            gg = v & 0x0F
            gd[gg] = gd.get(gg, 0) + 1
            gdist[gg] = gdist.get(gg, 0) + 1
            if v & 0x80:
                w += 1
            else:
                ls += 1
            if gg != (sz & 1):
                parity_mismatch += 1
        win_total += w
        loss_total += ls
        per_size.append({"size": sz, "count": len(buckets[sz]),
                         "grundy": {str(k): v for k, v in sorted(gd.items())},
                         "win": w, "loss": ls})
    root = g[0]
    out = {
        "tag": tag,
        "n": n,
        "b": len(lines),
        "safe": total,
        "max_size": max_size,
        "per_size": per_size,
        "grundy": {str(k): v for k, v in sorted(gdist.items())},
        "root_g": root & 0x0F,
        "root_win": 1 if root & 0x80 else 0,
        "win_total": win_total,
        "loss_total": loss_total,
        "parity_mismatch": parity_mismatch,
        "seconds": round(elapsed, 3),
    }
    path = os.path.join(HERE, tag + "_py_grundy.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
