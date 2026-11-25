#!/usr/bin/env python3
"""Exact integer audit of compressed double-hit row windows on three circles.

No floating-point operations or external dependencies. Each row set is computed
independently from (a,b) two-square representations and circle discriminants.
"""
import json
from math import isqrt

N_VALUES = (55250, 143650, 320450)


def from_two_squares(n):
    """All possible y-offsets b for a^2+b^2=n, a>0 odd, b odd."""
    positives = []
    for b in range(1, isqrt(n) + 1, 2):
        a2 = n - b * b
        if a2 > 0 and (a := isqrt(a2)) ** 2 == a2 and a % 2:
            positives.append(b)
    return sorted([-b for b in positives] + positives)


def from_circle(n, m, d):
    """All double-hit rows by checking the x-discriminant, independently."""
    out = []
    for y in range(m + 1):
        delta = 1 - 4 * (y * y - m * y + d)
        if delta > 0 and (a := isqrt(delta)) ** 2 == delta and a % 2:
            x0, x1 = (-1 - a) // 2, (-1 + a) // 2
            assert x0 < x1
            assert x0 * x0 + y * y + x0 - m * y + d == 0
            assert x1 * x1 + y * y + x1 - m * y + d == 0
            out.append(y)
    return out


def main():
    records = []
    thresholds = {}
    for n in N_VALUES:
        bvals = from_two_squares(n)
        m = max(bvals)
        assert m % 2 == 1 and n % 4 == 2
        assert (1 + m * m - n) % 4 == 0
        d = (1 + m * m - n) // 4
        rows1 = [(b + m) // 2 for b in bvals]
        rows2 = from_circle(n, m, d)
        assert rows1 == rows2
        for k in range(25, len(rows1) + 1):
            width, start_index = min(
                (rows1[i + k - 1] - rows1[i] + 1, i)
                for i in range(len(rows1) - k + 1)
            )
            start, end = rows1[start_index], rows1[start_index + k - 1]
            assert end - start + 1 == width
            assert sum(start <= y <= end for y in rows2) == k
            if k not in thresholds or width < thresholds[k]["w"]:
                thresholds[k] = {"w": width, "N": n, "row_interval": [start, end]}
        records.append({"N": n, "m": m, "D": d, "rows": rows1, "count": len(rows1)})
    assert sorted(thresholds) == list(range(25, 49))
    assert thresholds[33] == {"w": 372, "N": 143650, "row_interval": [0, 371]}
    assert thresholds[37] == {"w": 491, "N": 320450, "row_interval": [0, 490]}
    print(json.dumps({"circles": records, "thresholds": thresholds}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
