#!/usr/bin/env python3
"""Third, pure-Python cap census (independent of the two C programs).

Carries the addable-point set as a Python integer bitmask down the recursion;
`blocked` is the union of all secants of the current cap.  Nothing is reused
from cap_census.c / cap_census_alt.c.

usage: python_census.py <board-file> [maxdepth]
prints the size distribution and the maximal-cap counts.
"""
import sys


def parse_board(path):
    with open(path, encoding="utf-8") as f:
        raw = [ln.split() for ln in f if ln.strip()]
    n, b = int(raw[0][0]), int(raw[0][1])
    lines = []
    for row in raw[1:]:
        vals = [int(t) for t in row]
        k = vals[0]
        assert len(vals[1:]) == k
        lines.append(vals[1:])
    assert len(lines) == b
    return n, lines


def census(n, lines, maxdepth):
    pair_line = {}
    line_mask = []
    for li, L in enumerate(lines):
        m = 0
        for p in L:
            m |= 1 << p
            for q in L:
                if p < q:
                    pair_line[(p, q)] = li
        line_mask.append(m)
    FULL = (1 << n) - 1
    cnt = [0] * (maxdepth + 1)
    mx = [0] * (maxdepth + 1)
    S = []

    def dfs(depth, start, blocked, Smask):
        cnt[depth] += 1
        cand = (~blocked) & FULL & ~Smask          # addable points
        if cand == 0:
            mx[depth] += 1
        if depth == maxdepth:
            return
        todo = cand & ~((1 << (start + 1)) - 1)    # only larger points
        while todo:
            lsb = todo & -todo
            p = lsb.bit_length() - 1
            todo ^= lsb
            nb = blocked
            for a in S:
                key = (a, p) if a < p else (p, a)
                nb |= line_mask[pair_line[key]]
            S.append(p)
            dfs(depth + 1, p, nb, Smask | lsb)
            S.pop()

    dfs(0, -1, 0, 0)
    return cnt, mx


def main():
    if len(sys.argv) < 2:
        print("usage: python_census.py <board-file> [maxdepth]")
        return 2
    path = sys.argv[1]
    maxdepth = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    n, lines = parse_board(path)
    cnt, mx = census(n, lines, maxdepth)
    total = sum(cnt)
    maxsize = max(k for k in range(maxdepth + 1) if cnt[k])
    print(f"BOARD {path}")
    print(f"N {n} B {len(lines)}")
    for k in range(maxsize + 1):
        print(f"SIZE {k} {cnt[k]} {mx[k]}")
    print(f"TOTAL {total}")
    print(f"MAXSIZE {maxsize}")
    print("MAXSIZES " + " ".join(f"{k}({mx[k]})" for k in range(maxsize + 1) if mx[k]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
