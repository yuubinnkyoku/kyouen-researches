#!/usr/bin/env python3
"""Exact rational-circle enumeration and full q=6 game on a 12-point lattice set."""
from fractions import Fraction
from itertools import combinations
from collections import Counter
import json

ROWS = {0: (-2, 0, 1, 3), 1: (-2, -1, 2, 3), 3: (-3, 0, 1, 4)}
POINTS = tuple((x, y) for y, xs in ROWS.items() for x in xs)

def circle_key(p, q, r):
    x1, y1 = p
    x2, y2 = q
    x3, y3 = r
    u, v, w, z = x2 - x1, y2 - y1, x3 - x1, y3 - y1
    det = u * z - v * w
    if det == 0:
        return None
    e = -(x2*x2+y2*y2-x1*x1-y1*y1)
    f = -(x3*x3+y3*y3-x1*x1-y1*y1)
    a = Fraction(e*z-v*f, det)
    b = Fraction(u*f-e*w, det)
    c = -x1*x1-y1*y1-a*x1-b*y1
    return a, b, c

def circles():
    found = {}
    for i, j, k in combinations(range(12), 3):
        key = circle_key(POINTS[i], POINTS[j], POINTS[k])
        if key is None:
            continue
        a, b, c = key
        mask = sum(1 << t for t, (x, y) in enumerate(POINTS)
                   if x*x+y*y+a*x+b*y+c == 0)
        found[key] = mask
    return found

def game(forbidden):
    safe = [all((mask & f) != f for f in forbidden) for mask in range(1 << 12)]
    grundy = [-1] * (1 << 12)
    maximal = Counter()
    for mask in range((1 << 12)-1, -1, -1):
        if not safe[mask]:
            continue
        children = [mask | (1 << i) for i in range(12)
                    if not (mask >> i & 1) and safe[mask | (1 << i)]]
        if not children:
            maximal[mask.bit_count()] += 1
        values = {grundy[child] for child in children}
        g = 0
        while g in values:
            g += 1
        grundy[mask] = g
    return {"safe_positions": sum(safe), "empty_grundy": grundy[0],
            "grundy_distribution": dict(sorted(Counter(g for g in grundy if g >= 0).items())),
            "maximal_size_distribution": dict(sorted(maximal.items())),
            "winning_first_moves": sum(grundy[1 << i] == 0 for i in range(12))}

def main():
    cs = circles()
    full = sorted(((key, mask) for key, mask in cs.items() if mask.bit_count() >= 6),
                  key=lambda item: item[0])
    assert len(full) == 3, full
    # Circle C: x^2-x+y^2-y-6=0; all three circles have A=-1.
    assert {key for key, _ in full} == {(-1, -7, 0), (-1, -3, 0), (-1, -1, -6)}
    assert all(mask.bit_count() == 6 for _, mask in full)
    data = {"points": POINTS, "circles": [
        {"coefficients_A_B_C": [str(v) for v in key],
         "points": [POINTS[i] for i in range(12) if mask >> i & 1]}
        for key, mask in full], "game": game([mask for _, mask in full])}
    assert data['game']['safe_positions'] == 3915
    assert data['game']['empty_grundy'] == 0
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
