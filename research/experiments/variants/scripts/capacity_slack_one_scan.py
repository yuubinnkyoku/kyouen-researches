#!/usr/bin/env python3
"""Finite exhaustive Grundy scan for the K0352 capacity game."""

from functools import lru_cache
from itertools import combinations_with_replacement
from collections import Counter


def states(w, m, h, r):
    for asc in combinations_with_replacement(range(m + 1), w):
        x = tuple(reversed(asc))
        if sum(x[:h]) <= r:
            yield x


def children(x, m, h, r):
    for i, a in enumerate(x):
        if a == m:
            continue
        y = list(x)
        y[i] += 1
        y = tuple(sorted(y, reverse=True))
        if sum(y[:h]) <= r:
            yield y


def mex(vals):
    vals = set(vals)
    g = 0
    while g in vals:
        g += 1
    return g


def recursive_solver(w, m, h, r):
    @lru_cache(None)
    def grundy(x):
        return mex(grundy(y) for y in children(x, m, h, r))
    return grundy


def bottom_up_solver(w, m, h, r):
    xs = sorted(states(w, m, h, r), key=sum, reverse=True)
    g = {}
    for x in xs:
        g[x] = mex(g[y] for y in children(x, m, h, r))
    return g


def main():
    dist = Counter()
    slack_one = 0
    checked = 0
    mismatch = 0

    for h in range(2, 6):
        for w in range(h + 1, h + 6):
            for m in range(2, 8):
                for r in range(1, h * m):
                    rec = recursive_solver(w, m, h, r)
                    tab = bottom_up_solver(w, m, h, r)
                    for x, gv in tab.items():
                        checked += 1
                        if rec(x) != gv:
                            mismatch += 1
                        if r - sum(x[:h]) == 1:
                            slack_one += 1
                            dist[gv] += 1

    print("all_safe_states_checked", checked)
    print("crosscheck_mismatches", mismatch)
    print("slack_one_states", slack_one)
    print("distribution", dict(sorted(dist.items())))
    print("max_slack_one_grundy", max(dist))


if __name__ == "__main__":
    main()
