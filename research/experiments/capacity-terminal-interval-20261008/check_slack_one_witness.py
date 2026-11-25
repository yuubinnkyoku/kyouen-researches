#!/usr/bin/env python3
"""Independent complete-range check of constructive nonbinary slack-one witnesses.

For every safe sorted capacity position with odd n=w-h and B(x)>A(x),
construct a descendant of slack one by modifying only the top h columns.
The Grundy value is independently computed from the legal-move recursion.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement


def verify():
    counts = Counter()
    for w in range(3, 9):
        for h in range(2, w):
            n = w - h
            if n % 2 == 0:
                continue
            for m in range(2, 8):
                for r in range(1, h * m):
                    @lru_cache(None)
                    def grundy(x):
                        values = set()
                        for i, v in enumerate(x):
                            if v == m:
                                continue
                            y = list(x)
                            y[i] += 1
                            y = tuple(sorted(y, reverse=True))
                            if sum(y[:h]) <= r:
                                values.add(grundy(y))
                        g = 0
                        while g in values:
                            g += 1
                        return g

                    for asc in combinations_with_replacement(range(m + 1), w):
                        x = tuple(reversed(asc))
                        sigma = r - sum(x[:h])
                        if sigma < 0:
                            continue
                        b = x[h - 1]
                        a = max(b, r - (h - 1) * m)
                        # B(x)>A(x) iff the next threshold a+1 is attainable.
                        if a + 1 > m or sum(max(v, a + 1) for v in x[:h]) > r:
                            continue

                        # First make h-1 upper columns >a, column h exactly a.
                        y = [max(v, a + 1) for v in x[:h - 1]]
                        y += [a]
                        y += list(x[h:])
                        # Fill only the upper h-1 columns to top sum r-1.
                        for i in range(h - 1):
                            increase = min(m - y[i], r - 1 - sum(y[:h]))
                            y[i] += increase
                        y = tuple(y)

                        assert y == tuple(sorted(y, reverse=True))
                        assert all(u <= v for u, v in zip(x, y))
                        assert sum(y[:h]) == r - 1
                        assert sum(y) - sum(x) == sigma - 1
                        assert a < y[h - 2] < m and y[h - 1] == a
                        # Evaluate g without using the K0358 closed formula.
                        actual = grundy(y)
                        residual = n * a - sum(x[h:])
                        predicted = 2 + (residual % 2)
                        assert actual == predicted, (w, h, m, r, x, y, actual, predicted)
                        counts["witnesses"] += 1
                        counts["g2" if actual == 2 else "g3"] += 1
    return counts


if __name__ == "__main__":
    print("PASS", dict(verify()))
