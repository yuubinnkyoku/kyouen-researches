#!/usr/bin/env python3
"""Third implementation of the 25-double-row modular obstruction, widths 129..133.

No coefficient bounds; only necessary modular conditions. Integer masks are unbounded.
"""
from functools import lru_cache
from math import gcd

MODS = (9, 11, 7, 19, 23, 49, 31, 37, 41, 43, 47, 53)


def maximal(candidates):
    ordered = sorted(set(candidates), key=lambda x: (-x.bit_count(), x))
    out = []
    for a in ordered:
        if not any((a & b) == a for b in out):
            out.append(a)
    return out


@lru_cache(maxsize=None)
def local(length, p, target):
    squares = {x * x % p for x in range(p)}
    out = []
    for c in range(p):
        shift = [((2 * k + c) ** 2) % p for k in range(length)]
        for n in range(p):
            mask = sum(1 << k for k in range(length) if (n - shift[k]) % p in squares)
            if mask.bit_count() >= target and (mask & 1) and (mask >> (length - 1) & 1):
                out.append(mask)
    return maximal(out)


def main():
    for w in range(129, 134):
        for g in range(1, (w - 1) // 24 + 1):
            if (w - 1) % g:
                continue
            length = (w - 1) // g + 1
            states = [(1 << length) - 1]
            for p in MODS:
                if gcd(g, p) != 1:
                    continue
                masks = local(length, p, 25)
                states = maximal(a & b for a in states for b in masks if (a & b).bit_count() >= 25)
                print('CASE', w, 25, g, p, len(masks), len(states))
                if not states:
                    break
            assert not states, (w, g)
        print('WIDTH', w, 'EXCLUDED_25')
    print('PASS')


if __name__ == '__main__':
    main()
