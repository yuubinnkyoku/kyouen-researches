"""Independent integer checks for the three-row six-point-circle early-width formula.
Run: python research/experiments/fixed-width/scripts/q36_early_width_20261022.py
"""
from collections import defaultdict
from math import isqrt


def rho(n):
    """Count positive ordered chords via divisor formula, removing zero chords."""
    d1 = d3 = 0
    for d in range(1, isqrt(n) + 1):
        if n % d:
            continue
        for z in (d,) if d*d == n else (d, n//d):
            if z % 4 == 1:
                d1 += 1
            elif z % 4 == 3:
                d3 += 1
    diagonal = n % 2 == 0 and isqrt(n//2)**2 == n//2
    return d1 - d3 - int(diagonal)


def predicted(h, m):
    k = m - 2*h - 1
    return sum((k+1-l)*rho(l*(4*h+l)) for l in range(1, k+1))


def direct_chords(h, m):
    total = 0
    for middle in range(1, m):
        for top in range(1, m):
            if (middle-top) % 2:
                continue
            square = 2*middle*middle - 8*h*h - top*top
            if square <= 0:
                continue
            bottom = isqrt(square)
            if bottom and bottom < m and bottom*bottom == square and (bottom-middle)%2 == 0:
                total += m - max(top, middle, bottom)
    return total


def direct_geometry(h, m):
    """Determine circles from pairs on rows 0,h; independently test row 2h."""
    pairs = defaultdict(dict)
    for x in range(m):
        for y in range(x+1, m):
            pairs[x+y][x*y] = (x, y)
    total = 0
    for by_product in pairs.values():
        products = set(by_product)
        for p0 in products:
            for p1 in products:
                p2 = 2*p1-p0+2*h*h
                total += p2 in products
    return total


def run():
    checked = 0
    for h in range(1, 101):
        max_k = isqrt(8*h*h)-2*h
        for k in range(max_k+1):
            m = 2*h+k+1
            assert predicted(h,m) == direct_chords(h,m), (h,m)
            checked += 1
    geometric = 0
    for h in range(1, 19):
        for k in range(isqrt(8*h*h)-2*h+1):
            m = 2*h+k+1
            assert direct_geometry(h,m) == predicted(h,m), (h,m)
            geometric += 1
    assert rho(128) == 0
    assert predicted(7,19) == 8
    assert direct_chords(3,12) == 20 and predicted(3,12) == 22
    print(f"PASS {checked} independent chord widths; {geometric} direct-circle widths")
    print("diagonal exclusion: rho(128)=0; outside-range counterexample: h=3,m=12: 20 != 22")


if __name__ == "__main__":
    run()
