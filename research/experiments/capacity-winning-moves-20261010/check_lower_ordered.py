#!/usr/bin/env python3
"""Independent audit using labelled, unsorted columns and direct mex only."""
from functools import lru_cache
from itertools import product
from collections import Counter

stats = Counter()
for w in range(3, 7):
    for h in range(2, w):
        for m in range(1, 5):
            for r in range(1, h * m):
                def safe(x):
                    return sum(sorted(x, reverse=True)[:h]) <= r

                @lru_cache(None)
                def grundy(x):
                    values = set()
                    for i in range(w):
                        if x[i] == m:
                            continue
                        y = x[:i] + (x[i] + 1,) + x[i+1:]
                        if safe(y):
                            values.add(grundy(y))
                    z = 0
                    while z in values:
                        z += 1
                    return z

                for x in product(range(m + 1), repeat=w):
                    if not safe(x):
                        continue
                    g = grundy(x)
                    b = sorted(x, reverse=True)[h-1]
                    stats['positions'] += 1
                    for i, v in enumerate(x):
                        if v >= b:
                            continue
                        y = x[:i] + (v + 1,) + x[i+1:]
                        assert safe(y)
                        assert (grundy(y) == 0) == (g == 1), (w,h,m,r,x,i,g,grundy(y))
                        stats['lower_moves'] += 1
                        if g == 1:
                            stats['lower_winning'] += 1
print('PASS', dict(stats))
