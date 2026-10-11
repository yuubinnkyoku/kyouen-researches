#!/usr/bin/env python3
"""Independent exact-integer check of 32 double-hit rows in 321..326."""
from math import isqrt
rows = []
for y in range(326):
    disc = 1 - 4 * (y*y - 235*y - 6)
    if disc <= 0:
        continue
    r = isqrt(disc)
    if r*r != disc or r % 2 == 0:
        continue
    a, b = (-1-r)//2, (-1+r)//2
    assert a != b
    assert all(x*x + y*y + x - 235*y - 6 == 0 for x in (a, b))
    rows.append(y)
assert len(rows) == 32 and max(rows) == 235
for w in range(321, 327):
    assert len([y for y in rows if y < w]) == 32
    print(f"WITNESS {w} 32")
print('ROWS', ','.join(map(str, rows)))
