#!/usr/bin/env python3
"""Exact 2+1+1 cocircular count by integer quadratic roots; parity audit."""
from itertools import combinations
from math import isqrt


def count_211(width: int, height: int) -> int:
    total = 0
    for a in range(height):  # the unique doubled row
        for b, c in combinations((r for r in range(height) if r != a), 2):
            da, dc = b - a, c - a
            for x0 in range(width):
                for x1 in range(x0 + 1, width):
                    s, d = x0 + x1, x1 - x0
                    for u in range(width):
                        # (v-x0)(v-x1) = R; require integral R.
                        numerator = dc * ((u - x0) * (u - x1) - da * (c - b))
                        if numerator % da:
                            continue
                        R = numerator // da
                        disc = d * d + 4 * R
                        if disc < 0:
                            continue
                        t = isqrt(disc)
                        if t * t != disc or (s - t) % 2:
                            continue
                        for v in {(s - t) // 2, (s + t) // 2}:
                            total += 0 <= v < width
    return total


def predicted_parity(width: int, height: int) -> int:
    if width % 2 == 0 or height % 2 == 0:
        return 0
    return min((width - 1) // 2, (height - 1) // 2) % 2


def main() -> None:
    print('width,height,c211,parity')
    for h in range(1, 12):
        for w in range(1, 12):
            count = count_211(w, h)
            parity = predicted_parity(w, h)
            assert count % 2 == parity, (w, h, count, parity)
            if (w, h) == (11, 11):
                assert count == 39557
            print(f'{w},{h},{count},{parity}')


if __name__ == '__main__':
    main()
