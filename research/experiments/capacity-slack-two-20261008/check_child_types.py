#!/usr/bin/env python3
"""Independent mex audit of all slack-one-child nimber sets at slack two.

Odd residual column counts only; 3<=w<=8, 2<=h<w, 2<=m<=7.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement


def verify():
    stats = Counter()
    for w in range(3, 9):
        for h in range(2, w):
            n = w - h
            if n % 2 == 0:
                continue
            for m in range(2, 8):
                for r in range(2, h*m):
                    @lru_cache(None)
                    def nimber(x):
                        child_values = set()
                        for i, v in enumerate(x):
                            if v == m or (i and x[i-1] == v):
                                continue
                            y = list(x)
                            y[i] += 1
                            y = tuple(sorted(y, reverse=True))
                            if sum(y[:h]) <= r:
                                child_values.add(nimber(y))
                        mex = 0
                        while mex in child_values:
                            mex += 1
                        return mex

                    for ascending in combinations_with_replacement(range(m+1), w):
                        x = ascending[::-1]
                        if sum(x[:h]) != r-2:
                            continue
                        b = x[h-1]
                        R = n*b - sum(x[h:])
                        p = R % 2
                        c = sum(v == b for v in x[:h])
                        delta = sum(m-v for v in x[:h-1])
                        children = set()
                        for i, v in enumerate(x):
                            if v == m or (i and x[i-1] == v):
                                continue
                            y = list(x)
                            y[i] += 1
                            y = tuple(sorted(y, reverse=True))
                            if sum(y[:h]) == r-1:
                                children.add(nimber(y))
                        if c >= 3:
                            expected = {1-p}
                            category = "c>=3"
                        elif c == 2:
                            expected = {2+p}
                            if delta > m-b:
                                expected.add(1-p)
                            category = "c=2"
                        elif x[h-2] == b+1:
                            expected = {p}
                            if delta >= 2:
                                expected.add(2+p)
                            category = "gamma=1"
                        elif delta == 0:
                            expected = {1-p}
                            category = "gamma>=2, delta=0"
                        elif delta == 1:
                            expected = {p,3-p}
                            category = "gamma>=2, delta=1"
                        else:
                            expected = {2+p,3-p}
                            category = "gamma>=2, delta>=2"
                        assert children == expected, (
                            w, h, m, r, x, children, expected
                        )
                        stats[category] += 1
    print("PASS", dict(stats), "total", sum(stats.values()))


if __name__ == "__main__":
    verify()
