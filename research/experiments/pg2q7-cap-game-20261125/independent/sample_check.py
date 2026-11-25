#!/usr/bin/env python3
"""Direct recursive re-evaluation of sampled positions.

Reads the SAMPLE lines emitted by cap_engine and re-solves each sampled
position from the game definition alone (no bit-mask U shortcut): a move is
legal iff every line through the new point contains at most one old point.
Grundy = mex of children, misere win = terminal or some child is a loss.

This is a third code path for the Grundy values (C DP, Python bucket DP,
direct recursion).  Root (empty position) is skipped because it would amount
to a full recomputation; it is already covered by the two full DPs.

Usage: python sample_check.py <board> <engine-result.txt> <tag>
"""

import json
import os
import sys

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


def main():
    if len(sys.argv) < 4:
        print("usage: sample_check.py <board> <engine-result.txt> <tag>")
        return 2
    board, result, tag = sys.argv[1], sys.argv[2], sys.argv[3]
    n, lines = read_board(board)
    line_masks = []
    for L in lines:
        m = 0
        for p in L:
            m |= 1 << p
        line_masks.append(m)
    point_lines = [[] for _ in range(n)]
    for li, L in enumerate(lines):
        for p in L:
            point_lines[p].append(li)

    samples = []
    with open(result, "r", encoding="utf-8") as f:
        for line in f:
            t = line.split()
            if t and t[0] == "SAMPLE":
                sz = int(t[1])
                mask = int(t[2])
                samples.append((sz, mask, int(t[3]), int(t[4])))
    samples = [s for s in samples if s[0] >= 4]

    memo = {}
    sys.setrecursionlimit(10000)

    def solve(S):
        if S in memo:
            return memo[S]
        moves = []
        for p in range(n):
            bit = 1 << p
            if S & bit:
                continue
            ok = True
            for li in point_lines[p]:
                if (S & line_masks[li]).bit_count() >= 2:
                    ok = False
                    break
            if ok:
                moves.append(bit)
        if not moves:
            memo[S] = (0, True)  # terminal: misere win, no move loses normally
            return memo[S]
        seen = set()
        win = False
        for bit in moves:
            gg, ww = solve(S | bit)
            seen.add(gg)
            if not ww:
                win = True
        gg = 0
        while gg in seen:
            gg += 1
        memo[S] = (gg, win)
        return memo[S]

    bad = []
    by_size = {}
    for sz, mask, want_g, want_w in samples:
        gg, ww = solve(mask)
        got_w = 1 if ww else 0
        by_size[sz] = by_size.get(sz, 0) + 1
        if (gg, got_w) != (want_g, want_w):
            bad.append({"size": sz, "mask": mask,
                        "engine": [want_g, want_w],
                        "recursive": [gg, got_w]})
    out = {
        "tag": tag,
        "samples_checked": len(samples),
        "by_size": by_size,
        "mismatches": bad,
        "memo_states": len(memo),
        "pass": not bad,
    }
    path = os.path.join(HERE, tag + "_sample_check.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
