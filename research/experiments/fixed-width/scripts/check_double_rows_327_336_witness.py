#!/usr/bin/env python3
"""Independent exact-integer witness check for 327 <= w <= 336."""
from math import isqrt

rows = []
for y in range(336):
    d = 1 - 4 * (y * y - 235 * y - 6)
    if d <= 0:
        continue
    r = isqrt(d)
    if r * r != d or r % 2 == 0:
        continue
    x1, x2 = (-1-r)//2, (-1+r)//2
    assert x1 != x2
    assert x1*x1 + y*y + x1 - 235*y - 6 == 0
    assert x2*x2 + y*y + x2 - 235*y - 6 == 0
    rows.append(y)
assert len(rows) == 32 and rows[-1] == 235
for w in range(327, 337):
    assert sum(y < w for y in rows) == 32
    print(f"WITNESS {w} 32")
print('ROWS', ','.join(map(str, rows)))
