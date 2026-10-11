#!/usr/bin/env python3
"""Independent, exact modular audit of F(9)=43 (nonprimitive double-hit rows).

Uses discriminants d - 4*a*i - 4*g*g*i*i (mod p), rather than the
completed-square c,n parametrization in the C++ verifier.
"""
from math import gcd, isqrt

MODULI = (9, 11, 7, 49, 19, 23, 43, 27)
W, K = 42, 9

def allowed_masks(g, h, p):
    squares = {x * x % p for x in range(p)}
    masks = set()
    for a in range(p):
        for d in range(p):
            mask = sum(1 << i for i in range(h)
                       if (d - 4*a*i - 4*g*g*i*i) % p in squares)
            if mask & 1 and mask.bit_count() >= K:
                masks.add(mask)
    return masks

def verify():
    trace = []
    for g in range(2, (W - 1)//(K-1) + 1):
        h = (W - 1)//g + 1
        states = {(1 << h) - 1}
        for p in MODULI:
            if gcd(g, p) != 1:
                continue
            masks = allowed_masks(g, h, p)
            states = {s & t for s in states for t in masks
                      if (s & t).bit_count() >= K}
            row = (g, p, len(states), max(map(int.bit_count, states), default=0))
            trace.append(row)
            print('CASE', *row)
            if not states:
                break
        assert not states, f'non-excluded gcd={g}'
    ys = [-23, -19, -17, -11, -5, 5, 11, 17, 19]
    assert len(ys) == K and ys[-1] - ys[0] == 42
    assert gcd(*(y - ys[0] for y in ys[1:])) == 2
    for y in ys:
        x2 = 650-y*y
        x = isqrt(x2)
        assert x > 0 and x*x == x2
        assert x*x + y*y == 650
    print('WITNESS y=', ys, 'x=', [isqrt(650-y*y) for y in ys])
    print('PASS F(9)=43', 'steps=', len(trace))
    return trace

if __name__ == '__main__':
    verify()
