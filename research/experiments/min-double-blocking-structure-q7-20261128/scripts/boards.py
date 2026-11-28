#!/usr/bin/env python3
"""GF(q) board construction + independent verification for AG(2,q)/PG(2,q).

Boards are point sets with all lines; each line is a set of point indices.
Used by the SAT encoder and the classifier; independent of the C enumerator
so that published board files can be cross-checked.

Field encodings (all polynomial basis, shift = multiply by x, reduce):
  GF(2^2): x^2 = x + 1        GF(2^3): x^3 = x + 1
  GF(3^2): x^2 = x + 1 (mod x^2 + 2x + 2, irreducible over GF(3))
Prime fields: integers mod q.
Point labelling: AG index = y*q + x; PG index = x*q + y (affine part),
then (x,1,0) for x in range(q), then (1,0,0).
"""
import sys
from itertools import product

def field(q):
    """Return (add, mul, neg, one) as functions on range(q)."""
    if q in (2, 3, 5, 7):
        return ((lambda a, b: (a + b) % q), (lambda a, b: (a * b) % q),
                (lambda a: (-a) % q), 1)
    if q == 4:
        def add(a, b): return a ^ b
        def mul(a, b):
            r = 0
            while b:
                if b & 1: r = add(r, a)
                b >>= 1
                a <<= 1
                if a & 4: a = (a & 0b11) ^ 0b11  # x^2 = x + 1
            return r
        return (add, mul, (lambda a: a), 1)
    if q == 8:
        def add(a, b): return a ^ b
        def mul(a, b):
            r = 0
            while b:
                if b & 1: r ^= a
                b >>= 1
                a <<= 1
                if a & 8: a = (a & 0b111) ^ 0b011  # x^3 -> x + 1
            return r
        return (add, mul, (lambda a: a), 1)
    if q == 9:
        def digits(a): return [a % 3, a // 3]
        def add(a, b):
            da, db = digits(a), digits(b)
            return (da[0] + db[0]) % 3 + 3 * ((da[1] + db[1]) % 3)
        def mul(a, b):
            da, db = digits(a), digits(b)
            c = [0, 0, 0]
            for i in range(2):
                for j in range(2):
                    c[i + j] = (c[i + j] + da[i] * db[j]) % 3
            # reduce x^2 = x + 1 (from x^2 + 2x + 2 = 0)
            hi = c[2]
            c[2] = 0
            c[0] = (c[0] + hi) % 3
            c[1] = (c[1] + hi) % 3
            return c[0] + 3 * c[1]
        def neg_(a):
            da = digits(a)
            return ((3 - da[0]) % 3) + 3 * ((3 - da[1]) % 3)
        return (add, mul, neg_, 1)
    raise ValueError(q)

def affine_plane(q):
    """AG(2,q): points (x,y), lines: verticals + y = m x + b."""
    add, mul, neg, one = field(q)
    pts = [(x, y) for y in range(q) for x in range(q)]
    lines = []
    for xv in range(q):
        lines.append(frozenset(i for i, (x, y) in enumerate(pts) if x == xv))
    for m in range(q):
        for b in range(q):
            s = set()
            for x in range(q):
                y = add(mul(m, x), b)
                s.add(pts.index((x, y)))
            lines.append(frozenset(s))
    return pts, [frozenset(l) for l in lines]

def projective_plane(q):
    """PG(2,q) via homogeneous coords; pts: (x,y,1) [x-outer], (x,1,0), (1,0,0)."""
    add, mul, neg, one = field(q)
    pts = []
    for x in range(q):
        for y in range(q):
            pts.append((x, y, 1))
    for x in range(q):
        pts.append((x, 1, 0))
    pts.append((1, 0, 0))
    lines = set()
    for a in range(q):
        for b in range(q):
            for c in range(q):
                if (a, b, c) == (0, 0, 0):
                    continue
                if a == 0 and b == 0 and c != 1: continue
                if a == 0 and b != 1 and c == 0: continue
                if a != 1 and b == 0 and c == 0: continue
                s = frozenset(i for i, (x, y, z) in enumerate(pts)
                              if add(add(mul(a, x), mul(b, y)), mul(c, z)) == 0)
                lines.add(s)
    return pts, sorted(lines, key=sorted)

def check_design(pts, lines, k_expected, affine=False):
    n = len(pts)
    sizes = set(len(l) for l in lines)
    assert sizes == {k_expected}, sizes
    from itertools import combinations
    cnt = {}
    for l in lines:
        for a, b in combinations(sorted(l), 2):
            cnt[(a, b)] = cnt.get((a, b), 0) + 1
    assert all(c == 1 for c in cnt.values())
    if affine:
        q = k_expected
        assert len(cnt) == (q + 1) * q * (q * (q - 1) // 2), (len(cnt), q)
    else:
        assert len(cnt) == n * (n - 1) // 2
    return True
