#!/usr/bin/env python3
"""Exact independent checks for N=2q, q>=7, and a q=6 counterexample."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from math import comb


def types(q):
    return [
        ("I", q, q, 0), ("II", q, q, 1), ("III", q, q, 2),
        ("IV", q+1, q, 1), ("V", q+1, q, 2),
        ("VI", q+1, q+1, 2), ("VII", q+2, q, 2),
    ]


def compressed(q, a, b, c):
    x, y, z = a-c, b-c, 2*q-a-b+c
    @lru_cache(None)
    def rec(i, j, t, e):
        children = []
        if i < x and i+t+1 < q: children.append(rec(i+1, j, t, e))
        if j < y and j+t+1 < q: children.append(rec(i, j+1, t, e))
        if t < c and i+t+1 < q and j+t+1 < q:
            children.append(rec(i, j, t+1, e))
        if e < z: children.append(rec(i, j, t, e+1))
        if not children: return (0, 1)
        gs = {v[0] for v in children}
        hs = {v[1] for v in children}
        return (next(k for k in range(6) if k not in gs),
                next(k for k in range(6) if k not in hs))
    return rec, (x, y, c, z)


def direct_all(q, rec, sizes):
    x, y, c, z = sizes
    n = x+y+c+z
    A = ((1 << x)-1) | (((1 << c)-1) << (x+y))
    B = (((1 << y)-1) << x) | (((1 << c)-1) << (x+y))
    groups = [(1 << x)-1, ((1 << y)-1) << x,
              ((1 << c)-1) << (x+y), ((1 << z)-1) << (x+y+c)]
    @lru_cache(None)
    def brute(mask):
        children = []
        for k in range(n):
            bit = 1 << k
            if mask & bit: continue
            new = mask | bit
            if (new & A).bit_count() < q and (new & B).bit_count() < q:
                children.append(brute(new))
        if not children: return (0, 1)
        gs = {v[0] for v in children}
        hs = {v[1] for v in children}
        return (next(k for k in range(6) if k not in gs),
                next(k for k in range(6) if k not in hs))
    checked = 0
    for mask in range(1 << n):
        if (mask & A).bit_count() >= q or (mask & B).bit_count() >= q:
            continue
        state = tuple((mask & g).bit_count() for g in groups)
        assert brute(mask) == rec(*state), (q, sizes, mask)
        checked += 1
    return checked


def point_stream(center, radius):
    cx, cy = center
    for k in range(1, 100):
        t = F(k, k+2)
        yield (cx+radius*(1-t*t)/(1+t*t), cy+radius*2*t/(1+t*t))
        yield (cx+radius*(1-t*t)/(1+t*t), cy-radius*2*t/(1+t*t))


def on_circle(p, center, r):
    return (p[0]-center[0])**2+(p[1]-center[1])**2 == r*r


def carriers(points, q):
    found = set()
    for a, b, c in combinations(points, 3):
        dx1, dy1 = b[0]-a[0], b[1]-a[1]
        dx2, dy2 = c[0]-a[0], c[1]-a[1]
        det = dx1*dy2-dx2*dy1
        if det == 0:
            covered = frozenset(i for i, p in enumerate(points)
                if (p[0]-a[0])*dy1 == (p[1]-a[1])*dx1)
        else:
            r1 = -(b[0]**2+b[1]**2-a[0]**2-a[1]**2)
            r2 = -(c[0]**2+c[1]**2-a[0]**2-a[1]**2)
            d = (r1*dy2-r2*dy1)/det
            e = (dx1*r2-dx2*r1)/det
            f = -(a[0]**2+a[1]**2+d*a[0]+e*a[1])
            covered = frozenset(i for i, p in enumerate(points)
                if p[0]**2+p[1]**2+d*p[0]+e*p[1]+f == 0)
        if len(covered) >= q: found.add(covered)
    return found


def geometric_two(q, a, b, c):
    c1 = (F(0), F(0))
    c2 = (F(12 if c == 0 else 10 if c == 1 else 6), F(0))
    common = [] if c == 0 else [(F(5), F(0))] if c == 1 else [
        (F(3), F(4)), (F(3), F(-4))]
    pts = list(common)
    for center, other, size in [(c1, c2, a), (c2, c1, b)]:
        count = 0
        for p in point_stream(center, F(5)):
            if p in pts or on_circle(p, other, F(5)): continue
            pts.append(p)
            count += 1
            if count == size-c: break
        assert count == size-c
    for k in range(2*q-len(pts)):
        pts.append((F(100+k), F(200+3*k)))
    expected = {frozenset(i for i, p in enumerate(pts)
        if on_circle(p, center, F(5))) for center in (c1, c2)}
    assert len(pts) == 2*q and carriers(pts, q) == expected


def geometric_three_q6():
    circles = [((F(0), F(0)), F(5)),
               ((F(6), F(0)), F(5)),
               ((F(2), F(-5)), F(2))]
    pts = [(F(3), F(-4)), (F(3), F(4)),
           (F(0), F(-5)), (F(100, 29), F(-105, 29)),
           (F(2), F(-3)), (F(162, 41), F(-187, 41)),
           (F(4), F(3)), (F(4), F(-3)),
           (F(10), F(3)), (F(10), F(-3)),
           (F(18, 5), F(-19, 5)), (F(18, 5), F(-31, 5))]
    expected = {frozenset(i for i, p in enumerate(pts)
        if on_circle(p, center, r)) for center, r in circles}
    assert len(pts) == 12 and len(expected) == 3
    assert all(len(s) == 6 for s in expected)
    assert carriers(pts, 6) == expected


def terminal_formula(q, name):
    if name == "I": return {2*q-2: q*q}
    if name == "II": return {2*q-2: (q-1)**2, 2*q-1: 1}
    if name == "III": return {2*q-2: (q-2)**2, 2*q-1: 2}
    if name == "IV": return {2*q-3: comb(q, 2)*(q-1), 2*q-2: q}
    if name == "V": return {2*q-3: (q-2)*comb(q-1, 2), 2*q-2: 2*q-1}
    if name == "VI": return {2*q-4: comb(q-1, 2)**2,
                              2*q-3: 2*(q-1)**2, 2*q-2: 1}
    return {2*q-4: (q-2)*comb(q, 3), 2*q-3: q*q}


def check_terminals(q, name, a, b, c):
    x, y, z = a-c, b-c, 2*q-a-b+c
    got = {}
    for t in range(c+1):
        for i in range(x+1):
            for j in range(y+1):
                if i+t >= q or j+t >= q: continue
                if i < x and i+t < q-1: continue
                if j < y and j+t < q-1: continue
                if t < c and i+t < q-1 and j+t < q-1: continue
                k = z+i+j+t
                got[k] = got.get(k, 0)+comb(c, t)*comb(x, i)*comb(y, j)
    assert got == terminal_formula(q, name), (q, name, got)


def main():
    total = 0
    for q in (7, 8):
        for name, a, b, c in types(q):
            rec, sizes = compressed(q, a, b, c)
            count = direct_all(q, rec, sizes)
            geometric_two(q, a, b, c)
            print("full", q, name, "root", rec(0, 0, 0, 0), "safe", count)
            total += count
    assert total == 557748, total
    for q in range(7, 51):
        for name, a, b, c in types(q):
            check_terminals(q, name, a, b, c)
    for q in (9, 10, 20, 50):
        for name, a, b, c in types(q):
            rec, _ = compressed(q, a, b, c)
            print("compressed", q, name, rec(0, 0, 0, 0))
    geometric_three_q6()
    print("PASS: 557748 independent full states; 308 terminal formulas; "
          "14 geometric two-carrier boards; one q=6 three-carrier board")


if __name__ == "__main__":
    main()
