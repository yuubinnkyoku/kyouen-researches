#!/usr/bin/env python3
"""Independent brute-force audit of sharp extremal terminal spectra.

The exhaustive oracle enumerates labelled occupancy vectors and checks
all legal single-column increments.  It does NOT use the T(b) formula.
"""
from itertools import combinations_with_replacement, product
from collections import Counter


def terminal_sizes(c, h, r):
    sizes = set()
    for x in product(*(range(z+1) for z in c)):
        if sum(sorted(x, reverse=True)[:h]) > r:
            continue
        maximal = True
        for i, ci in enumerate(c):
            if x[i] == ci:
                continue
            y = list(x)
            y[i] += 1
            if sum(sorted(y, reverse=True)[:h]) <= r:
                maximal = False
                break
        if maximal:
            sizes.add(sum(x))
    assert sizes
    return sizes


def sharp(w, h, r, M):
    # r >= h*M means the whole box is safe for every capacity vector.
    delta = max(0, min(M, r//h) - max(0, r-(h-1)*M))
    return ((w-h)*delta,
            max(0,w-h-1)*delta,
            1 + (delta if w>h else 0))


def stats(sizes):
    return (max(sizes)-min(sizes),
            max(sizes)-min(sizes)+1-len(sizes),
            len(sizes))


def run():
    cases=0; vectors=0; terminals=0
    for w in range(1, 6):
        for M in range(0, 5):
            for h in range(1, w+1):
                for r in range(0, h*M+3):
                    expected = sharp(w,h,r,M)
                    uniform = stats(terminal_sizes((M,)*w,h,r))
                    assert uniform == expected, (w,h,r,M,expected,uniform)
                    cases += 1
                    for c in combinations_with_replacement(range(M+1), w):
                        actual = stats(terminal_sizes(c,h,r))
                        assert all(a<=b for a,b in zip(actual,expected)), (w,h,r,M,c,actual,expected)
                        vectors += 1
                        terminals += actual[2]
    print('PASS: independent brute force')
    print(f'parameter sets (w,h,r,M): {cases}')
    print(f'capacity instances: {vectors}')
    print(f'number of distinct terminal-size observations summed: {terminals}')
    print('uniform capacity attains each bound, no capacity vector exceeds it')
    for w,h,r,M in [(5,2,5,5),(6,3,10,4),(5,2,5,3),(4,3,7,2)]:
        sizes=terminal_sizes((M,)*w,h,r)
        print(f'example w={w} h={h} r={r} M={M}: sizes={sorted(sizes)}, stats={stats(sizes)}')


if __name__=='__main__':
    run()
