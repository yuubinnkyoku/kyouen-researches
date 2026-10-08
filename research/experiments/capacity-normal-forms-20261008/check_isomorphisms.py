#!/usr/bin/env python3
"""Independent mex check of two full-game isomorphisms for capacity occupations.

Checks all safe sorted positions in 4<=w<=8, 2<=h<w, 2<=m<=5,
1<=r<h*m. The reductions themselves never use the Grundy recurrence.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement


@lru_cache(None)
def grundy(w, h, m, r, x):
    children = set()
    for i, v in enumerate(x):
        if v == m or (i > 0 and x[i - 1] == v):
            continue
        y = list(x)
        y[i] += 1
        y.sort(reverse=True)
        if sum(y[:h]) <= r:
            children.add(grundy(w, h, m, r, tuple(y)))
    g = 0
    while g in children:
        g += 1
    return g


def check():
    counts = Counter()
    for w in range(4, 9):
        for h in range(2, w):
            for m in range(2, 6):
                for r in range(1, h * m):
                    for asc in combinations_with_replacement(range(m + 1), w):
                        x = tuple(reversed(asc))
                        if sum(x[:h]) > r:
                            continue
                        g = grundy(w, h, m, r, x)
                        k = next((i for i, v in enumerate(x) if v < m), w)
                        if 0 < k < h:
                            y = x[k:]
                            reduced = grundy(w - k, h - k, m, r - k * m, y)
                            assert reduced == g, (w, h, m, r, x, g, reduced)
                            counts["saturated"] += 1
                            if k == h - 1:
                                residual_capacity = r - k * m
                                parity = ((w - k) * residual_capacity - sum(y)) % 2
                                assert parity == g, (w, h, m, r, x, g, parity)
                                counts["last_column"] += 1
                            if k == h - 2:
                                counts["pair_reduction"] += 1

                        a = x[-1]
                        if a:
                            y = tuple(v - a for v in x)
                            reduced = grundy(w, h, m - a, r - h * a, y)
                            assert reduced == g, (w, h, m, r, x, g, reduced)
                            counts["translation"] += 1

    print("PASS", dict(counts))
    print("memo", grundy.cache_info())


if __name__ == "__main__":
    check()
