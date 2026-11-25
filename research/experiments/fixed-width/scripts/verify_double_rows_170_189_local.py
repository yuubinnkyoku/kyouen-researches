#!/usr/bin/env python3
"""Independent arithmetic checks for the 170..189 extension; not a full mask audit."""
from math import isqrt

p = 19
qr = {z * z % p for z in range(p)}
max_admissible = max(
    sum((n - (2 * y + c) ** 2) % p in qr for y in range(p))
    for c in range(p) for n in range(p)
)
assert max_admissible == 11

for w in (176, 183):
    freq = [0] * p
    for y in range(0, w, 7):
        freq[y % p] += 1
    assert max(freq) == 2
    assert (25 + max(freq) - 1) // max(freq) == 13 > max_admissible

Y = []
for y in range(106):
    delta = 11050 - (2 * y - 105) ** 2
    if delta <= 0:
        continue
    z = isqrt(delta)
    if z * z != delta or z % 2 == 0:
        continue
    x1, x2 = (-1 - z) // 2, (-1 + z) // 2
    assert x1 != x2
    for x in (x1, x2):
        assert x * x + y * y + x - 105 * y - 6 == 0
    Y.append(y)
assert len(Y) == 24
for w in range(170, 190):
    assert all(0 <= y < w for y in Y)
print('PASS mod19 maximum=11; g7 cases 176,183 require >=13 residues')
print('PASS 24-row circle witness for every 170<=w<=189:', Y)
