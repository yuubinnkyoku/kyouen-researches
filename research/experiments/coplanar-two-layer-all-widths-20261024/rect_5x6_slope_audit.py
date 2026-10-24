"""Exhaustive oriented 3+2 audit; integer normalized slopes and bitmasks."""
from collections import Counter
from itertools import combinations
from math import gcd


def audit(k, m):
    pts = [(y, z) for y in range(k) for z in range(m)]

    def slope(a, b):
        dy, dz = b[0] - a[0], b[1] - a[1]
        g = gcd(abs(dy), abs(dz))
        dy, dz = dy // g, dz // g
        return (-dy, -dz) if dy < 0 or (dy == 0 and dz < 0) else (dy, dz)

    directions = sorted({slope(a, b) for a, b in combinations(pts, 2)})
    ids = {d: i for i, d in enumerate(directions)}

    def bit(a, b):
        return 1 << ids[slope(a, b)]

    triangles = Counter()
    for a, b, c in combinations(pts, 3):
        ab, ac, bc = bit(a, b), bit(a, c), bit(b, c)
        if ab != ac:  # no collinear triple in the three-stone layer
            triangles[ab | ac | bc] += 1

    safe = terminal = 0
    for d, e in combinations(pts, 2):
        pairbit = bit(d, e)
        options = []
        for f in pts:
            if f == d or f == e:
                continue
            df, ef = bit(d, f), bit(e, f)
            if df != pairbit:
                options.append(df | ef)
        for mask, frequency in triangles.items():
            if mask & pairbit:
                continue  # parallel pair of edges makes four coplanar points
            safe += frequency
            if all(mask & option for option in options):
                terminal += frequency
    return safe, terminal


if __name__ == "__main__":
    expected = {(5, 5): (475400, 0),
                (5, 6): (1278380, 0),
                (6, 6): (3408680, 0)}
    for (k, m), values in expected.items():
        got = audit(k, m)
        assert got == values, (k, m, got, values)
        print(f"{k}x{m}: oriented_safe={got[0]} oriented_terminal={got[1]}")
