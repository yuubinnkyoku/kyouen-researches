#!/usr/bin/env python3
"""Independent x-coordinate enumeration for the explicit 32-double-row circle."""
from math import isqrt

def main():
    # x^2+y^2+x-235*y-6=0. Its real x-span is bounded by [-119,118].
    rows = []
    for y in range(300):
        xs = [x for x in range(-120, 120) if x*x+y*y+x-235*y-6 == 0]
        assert len(xs) <= 2
        if len(xs) == 2:
            rows.append(y)
    expected = [0,1,3,4,10,15,22,25,45,49,60,70,87,91,102,115,
                120,133,144,148,165,175,186,190,210,213,220,225,231,232,234,235]
    assert rows == expected, (rows, expected)
    for w in range(257,301):
        assert len([y for y in rows if y < w]) == 32
    print('PASS: 32 two-point rows on every width 257..300')
    print('Rows:', ','.join(map(str,rows)))
if __name__ == '__main__': main()
