#!/usr/bin/env python3
"""Exact integer audit for the 421-row gcd=2 witness (no dependencies)."""
from math import gcd, isqrt
from functools import reduce

# Unscaled circle: X^2 + Y^2 + X - 235 Y - 6 = 0.
# Scaled/translated: x = 2X+1, y = 2Y,
# x^2 + y^2 - 470 y - 25 = 0.
expected = [0, 1, 3, 4, 10, 15, 22, 25, 45, 49, 60, 70, 87,
            91, 102, 115, 120, 133, 144, 148, 165, 175, 186, 190, 210]
assert len(expected) == 25 and len(set(expected)) == 25

unscaled = []
for Y in range(211):
    delta = 25 + 940 * Y - 4 * Y * Y
    if delta > 0:
        d = isqrt(delta)
        if d * d == delta and d % 2 == 1:
            X1, X2 = (-1 + d) // 2, (-1 - d) // 2
            assert X1 != X2
            assert all(X * X + Y * Y + X - 235 * Y - 6 == 0 for X in (X1, X2))
            unscaled.append((Y, d, X1, X2))
assert [row[0] for row in unscaled] == expected

scaled = []
for y in range(421):
    x2 = 25 + 470 * y - y * y
    if x2 > 0:
        x = isqrt(x2)
        if x * x == x2:
            assert x > 0 and x * x + y * y - 470 * y - 25 == 0
            scaled.append((y, x))
assert [y for y, x in scaled] == [2 * Y for Y in expected]
assert reduce(gcd, (y - scaled[0][0] for y, _ in scaled)) == 2
assert scaled[0] == (0, 5) and scaled[-1] == (420, 145)
# Stronger than a finite check: odd y are impossible modulo 4,
# because x^2 = 25+470*y-y^2 == 2 (mod 4) for odd y.
assert all((25 + 470 * y - y * y) % 4 == 2 for y in range(1, 421, 2))

print('PASS unscaled 211 rows: exactly 25 double-hit rows; span=210; T(211)>=25')
print('PASS scaled 421 rows: exactly 25 double-hit rows; gcd=2; endpoints=0,420')
print('rows Y:', ','.join(map(str, expected)))
print('x roots at y=0,2,420: +/-5, +/-31, +/-145')
