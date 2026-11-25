#!/usr/bin/env python3
"""Check the finite modular ingredients of the 2-adic all-width theorem."""
from itertools import combinations

def v2(x):
    x = abs(x)
    return (x & -x).bit_length() - 1

def check(rows, k):
    if len(rows) < 2:
        return True
    t = min(v2(b-a) for a,b in combinations(rows,2))
    mod = 1 << (k if t >= k else 2*k-t)
    return len({x % mod for x in rows}) <= (1 if t >= k else 2)

for k in range(1,6):
    for w in range(4,13):
        max_rows = max(sum(1 for i in range(w) if mask & (1<<i))
                       for mask in range(1<<w)
                       if check([i for i in range(w) if mask & (1<<i)], k))
        r = w % 4
        delta = (0,1,2,1)[r]
        assert 2*max_rows <= (w+delta if k == 1 else w)
    print("PASS k=", k, "w=4..12")
