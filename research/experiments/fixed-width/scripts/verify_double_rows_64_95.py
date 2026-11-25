#!/usr/bin/env python3
"""Certified modular exclusions for exact double-hit row counts T(64)..T(95).
Inductive base T(63)=16 is K0369. All calculations use exact integers.
"""
from functools import lru_cache
from math import gcd, isqrt

MODS = (9, 11, 7, 49, 19, 23, 31, 37, 41, 43, 47, 53)

def maximal(masks):
    kept = []
    for mask in sorted(set(masks), key=int.bit_count, reverse=True):
        if not any(mask & other == mask for other in kept):
            kept.append(mask)
    return kept

@lru_cache(None)
def local_masks(length, modulus, target):
    squares = {x*x % modulus for x in range(modulus)}
    masks = []
    for c in range(modulus):
        shifts = [((2*k+c)**2) % modulus for k in range(length)]
        for n in range(modulus):
            mask = sum(1 << k for k, z in enumerate(shifts)
                       if (n-z) % modulus in squares)
            if mask.bit_count() >= target and mask & 1 and mask >> (length-1) & 1:
                masks.append(mask)
    return maximal(masks)

def excludes(width, divisor, target):
    length = (width-1)//divisor+1
    states = [(1 << length)-1]
    for modulus in MODS:
        if gcd(modulus, divisor) != 1:
            continue
        local = local_masks(length, modulus, target)
        states = maximal(a & b for a in states for b in local
                         if (a & b).bit_count() >= target)
        print('CASE', width, target, divisor, modulus, len(local), len(states))
        if not states:
            return True
    return False

def witness_rows(width, c, d):
    rows = []
    for y in range(width):
        delta = 1 - 4*(y*y+c*y+d)
        if delta <= 0:
            continue
        s = isqrt(delta)
        if s*s == delta and s % 2:
            xs = ((-1-s)//2, (-1+s)//2)
            assert xs[0] != xs[1]
            assert all(x*x+y*y+x+c*y+d == 0 for x in xs)
            rows.append(y)
    return rows

assert len(witness_rows(63, -47, 0)) == 16
previous = 16
for width in range(64, 96):
    witness = witness_rows(width, -47, 0) if width <= 82 else witness_rows(width, -105, -6)
    assert len(witness) >= previous
    if len(witness) == previous + 1:
        previous += 1  # T(w) <= T(w-1)+1
        print('WIDTH', width, 'EXACT', previous, 'WITNESS_STEP')
        continue
    assert len(witness) == previous
    target = previous + 1
    divisors = [g for g in range(1, (width-1)//(target-1)+1)
                if (width-1) % g == 0]
    assert all(excludes(width, g, target) for g in divisors)
    print('WIDTH', width, 'EXACT', previous, 'EXCLUDED', divisors)
print('PASS T(64..95)')
