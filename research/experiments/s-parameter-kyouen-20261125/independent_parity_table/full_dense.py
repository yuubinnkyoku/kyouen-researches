"""Dense full DP: mark safe sets in a bytearray, then descend masks numerically.

Because adding a point always increases the integer mask, iterating masks in
decreasing numeric order guarantees children are evaluated first.  This needs
only two bytearrays of size 2^n, so it handles W_24 (n=24, 7.9M safe sets).
"""
import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kyouen_lib as K

ROOT = HERE.parent.parent
OUT = HERE / "out"


def full_dense(n, blocks, s):
    nb = len(blocks)
    pc = [[] for _ in range(n)]
    for c, B in enumerate(blocks):
        for p in B:
            pc[p].append(c)
    counts = [0] * nb
    safe = bytearray(1 << n)
    t0 = time.time()

    def rec(mask, start):
        safe[mask] = 1
        for p in range(start, n):
            ok = True
            for c in pc[p]:
                if counts[c] >= s:
                    ok = False
                    break
            if ok:
                for c in pc[p]:
                    counts[c] += 1
                rec(mask | (1 << p), p + 1)
                for c in pc[p]:
                    counts[c] -= 1

    rec(0, 0)
    t_enum = time.time() - t0
    g = bytearray([255]) * (1 << n)
    maximal = Counter()
    gdist = Counter()
    t1 = time.time()
    full = (1 << n) - 1
    for mask in range(full, -1, -1):
        if not safe[mask]:
            continue
        seen = 0
        is_max = True
        for p in range(n):
            if (mask >> p) & 1:
                continue
            nm = mask | (1 << p)
            if safe[nm]:
                is_max = False
                seen |= 1 << g[nm]
        if is_max:
            maximal[mask.bit_count()] += 1
        m = 0
        while (seen >> m) & 1:
            m += 1
        g[mask] = m
        gdist[m] += 1
    t_dp = time.time() - t1
    sizes = Counter()
    for mask in range(1 << n):
        if safe[mask]:
            sizes[mask.bit_count()] += 1
    return {
        "key": "W24_s7",
        "n": n,
        "s": s,
        "positions": sum(sizes.values()),
        "size_counts": dict(sorted(sizes.items())),
        "maximal_by_size": dict(sorted(maximal.items())),
        "grundy_dist": dict(sorted(gdist.items())),
        "root_grundy": g[0],
        "max_size": max(sizes),
        "enum_seconds": round(t_enum, 2),
        "dp_seconds": round(t_dp, 2),
        "seconds": round(time.time() - t0, 2),
    }


def main():
    board = ROOT / "design-kyouen-witt-20261125/output/board_w24.txt"
    n, blocks = K.load_board(board)
    s = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    print("board", K.validate_board(n, blocks), flush=True)
    res = full_dense(n, blocks, s)
    res["board_file"] = str(board).replace("\\", "/")
    print(json.dumps({k: res[k] for k in
                      ("positions", "maximal_by_size", "grundy_dist",
                       "root_grundy", "enum_seconds", "dp_seconds")},
                     indent=1), flush=True)
    (OUT / f"full_dense_W24_s{s}.json").write_text(json.dumps(res, indent=1),
                                                   encoding="utf-8")


if __name__ == "__main__":
    main()
