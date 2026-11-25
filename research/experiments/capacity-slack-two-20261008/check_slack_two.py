#!/usr/bin/env python3
"""Finite independent mex regression for the proved capacity-slack-two formula.

Runs with only the Python standard library. Enumerates every safe sorted state
with capacity slack 2 for 3<=w<=9, 2<=h<w, 2<=m<=8 and 2<=r<h*m,
and computes Grundy directly from all legal successor states.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement


def verify(max_w=9, max_m=8):
    counts = Counter()
    for w in range(3, max_w + 1):
        for h in range(2, w):
            n = w - h
            for m in range(2, max_m + 1):
                states = [tuple(reversed(y)) for y in
                          combinations_with_replacement(range(m + 1), w)]
                for r in range(2, h * m):
                    @lru_cache(None)
                    def grundy(x):
                        options = set()
                        for i, val in enumerate(x):
                            # Equal-height columns yield the same sorted child.
                            if val == m or (i and x[i-1] == val):
                                continue
                            y = list(x)
                            y[i] += 1
                            y.sort(reverse=True)
                            y = tuple(y)
                            if sum(y[:h]) <= r:
                                options.add(grundy(y))
                        mex = 0
                        while mex in options:
                            mex += 1
                        return mex

                    for x in states:
                        if sum(x[:h]) != r - 2:
                            continue
                        b = x[h-1]
                        R = n*b - sum(x[h:])
                        c = sum(t == b for t in x[:h])
                        delta = sum(m-t for t in x[:h-1])
                        gamma = x[h-2] - b
                        trigger = c == 1 and (gamma == 1 or delta == 1)
                        predicted = (R + (n % 2) * int(trigger)) % 2
                        actual = grundy(x)
                        assert actual == predicted, (
                            w, h, m, r, x, actual, predicted
                        )
                        counts["total"] += 1
                        if n % 2:
                            counts["odd_n"] += 1
                        if trigger:
                            counts["trigger"] += 1
    print("PASS", dict(counts))


if __name__ == "__main__":
    verify()
