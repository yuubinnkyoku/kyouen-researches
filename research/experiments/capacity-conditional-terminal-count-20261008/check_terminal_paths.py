#!/usr/bin/env python3
"""Independent complete-play enumeration vs terminal-generating-function coefficients.

All safe sorted input column counts are tested for 3<=w<=6,
2<=h<w, 1<=m<=4, 1<=r<h*m. The recursive method chooses a labelled
column and weighs it by the number of distinct unoccupied points; the
polynomial method independently counts its reachable terminal supersets.
"""
from collections import defaultdict, Counter
from functools import lru_cache
from itertools import combinations_with_replacement
from math import comb, factorial
import argparse


def gf_counts(x, h, m, r):
    w = len(x)
    b = x[h - 1]
    t0 = max(0, b, r - (h - 1) * m)
    result = {}
    for t in range(t0, m + 1):
        excess = r - h * t
        if excess < 0:
            break
        dp = {(0, 0): 1}
        for a in x:
            choices = [(k, comb(m - a, t + k - a))
                       for k in range(max(0, a - t), m - t + 1)]
            new = defaultdict(int)
            for (j, total), count in dp.items():
                for k, factor in choices:
                    if j + (k > 0) < h and total + k <= excess:
                        new[(j + (k > 0), total + k)] += count * factor
            dp = new
        number = sum(count for (j, total), count in dp.items()
                     if total == excess)
        if number:
            result[r + (w - h) * t] = number
    return result


def recursive_complete_plays(x, h, m, r):
    # Do not sort column labels inside this recursion. Different labelled
    # column choices and different unused points are distinguished.
    @lru_cache(None)
    def paths(state):
        result = defaultdict(int)
        any_move = False
        for i, v in enumerate(state):
            if v == m:
                continue
            child = list(state)
            child[i] += 1
            child = tuple(child)
            if sum(sorted(child, reverse=True)[:h]) > r:
                continue
            any_move = True
            for length, count in paths(child):
                result[length + 1] += (m - v) * count
        if not any_move:
            result[0] = 1
        return tuple(sorted(result.items()))
    return dict(paths(x))


def verify(max_w=6, max_m=4):
    total = 0
    entries = 0
    allpaths = 0
    by_width = Counter()
    for w in range(3, max_w + 1):
        for h in range(2, w):
            for m in range(1, max_m + 1):
                xs = [tuple(reversed(z)) for z in
                      combinations_with_replacement(range(m + 1), w)]
                for r in range(1, h * m):
                    for x in xs:
                        if sum(x[:h]) > r:
                            continue
                        boards_by_size = gf_counts(x, h, m, r)
                        independent_paths = recursive_complete_plays(x, h, m, r)
                        expected = {
                            T - sum(x): factorial(T - sum(x)) * board_count
                            for T, board_count in boards_by_size.items()
                        }
                        assert independent_paths == expected, (
                            w, h, m, r, x, boards_by_size,
                            independent_paths, expected
                        )
                        total += 1
                        entries += len(boards_by_size)
                        allpaths += sum(independent_paths.values())
                        by_width[w] += 1
    print("PASS positions=", total, "terminal-spectrum entries=", entries,
          "by_width=", dict(by_width), "total_paths=", allpaths)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-w", type=int, default=6)
    parser.add_argument("--max-m", type=int, default=4)
    args = parser.parse_args()
    verify(args.max_w, args.max_m)
