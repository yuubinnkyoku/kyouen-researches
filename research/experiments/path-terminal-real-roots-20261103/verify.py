#!/usr/bin/env python3
"""Independent finite audit of path real-rootedness and weighted tilings.

The unbounded theorem follows from proof.md, not these finite checks.
"""
from functools import lru_cache
from itertools import combinations, product
from math import comb, lcm, prod
from random import Random

def add_scaled(dst, src, scale, shift=0):
    while len(dst) < len(src) + shift:
        dst.append(0)
    for i, v in enumerate(src):
        dst[i + shift] += scale * v

def weighted_tilings(singletons, blocks):
    length = len(singletons)
    @lru_cache(None)
    def suffix(i):
        if i == length:
            return (1,)
        out = []
        add_scaled(out, suffix(i + 1), singletons[i])
        for size in (2, 3):
            if (i, size) in blocks:
                add_scaled(out, suffix(i + size), blocks[(i, size)], 1)
        return tuple(out)
    return list(suffix(0))

def path_tilings(n, r):
    length = n - 1
    a = [r] * length
    if length == 1:
        a[0] = r + 2
    else:
        a[0] = a[-1] = r + 1
    return weighted_tilings(tuple(a), {
        (i, size): 1 for size in (2, 3)
        for i in range(length - size + 1)
    })

def deletion_enumeration(n, r):
    """Enumerate all X directly from K0602, without using tilings."""
    counts = {}
    for x in range(1 << n):
        if any((x >> i) & 1
               and (i == 0 or (x >> (i - 1)) & 1)
               and (i == n - 1 or (x >> (i + 1)) & 1)
               for i in range(n)):
            continue
        edges = sum(not ((x >> i) & 1) and not ((x >> (i + 1)) & 1)
                    for i in range(n - 1))
        k = n - 1 - x.bit_count() - edges
        assert k >= 0
        counts[k] = counts.get(k, 0) + r ** edges
    return [counts.get(k, 0) for k in range(max(counts) + 1)]

def closed_formula(n, r):
    out = []
    for k in range((n - 1) // 2 + 1):
        total = 0
        for a, b in product((0, 1), repeat=2):
            for j in range(k + 1):
                R = n - a - b - k - j
                if R >= k + 1:
                    total += comb(k, j) * comb(R - 1, k) * r ** (R - k - 1)
        out.append(total)
    return out

def interval_claw_free(length):
    intervals = [(i, i + size - 1) for size in (2, 3)
                 for i in range(length - size + 1)]
    def hit(a, b):
        return a[0] <= b[1] and b[0] <= a[1]
    for center in intervals:
        neighbors = [v for v in intervals if v != center and hit(center, v)]
        for x, y, z in combinations(neighbors, 3):
            if not hit(x, y) and not hit(x, z) and not hit(y, z):
                return False
    return True

def weighted_interval_independence(singletons, blocks):
    """Enumerate independent intervals using integer-cleared rational weights."""
    intervals = sorted(blocks)
    denominators = [prod(singletons[i:i + size]) for i, size in intervals]
    M = lcm(*denominators) if denominators else 1
    A = prod(singletons)
    counts = {}
    for mask in range(1 << len(intervals)):
        occupied = 0
        weight = 1
        k = 0
        for j, (i, size) in enumerate(intervals):
            if not (mask >> j) & 1:
                continue
            bits = ((1 << size) - 1) << i
            if occupied & bits:
                break
            occupied |= bits
            weight *= M * blocks[(i, size)] // denominators[j]
            k += 1
        else:
            counts[k] = counts.get(k, 0) + weight
    ans = []
    for k in range(max(counts) + 1):
        numerator = A * counts.get(k, 0)
        assert numerator % (M ** k) == 0
        ans.append(numerator // M ** k)
    return ans

def newton_holds(a):
    h = len(a) - 1
    return all(a[k] ** 2 * k * (h - k) >=
               a[k - 1] * a[k + 1] * (k + 1) * (h - k + 1)
               for k in range(1, h))

def main():
    rng = Random(20261103)
    counts = dict(path_three_way=0, path_large=0, claw_free=0,
                  weighted_tiling=0, newton=0)
    for n in range(2, 18):
        for r in (1, 2, 3, 5):
            a = deletion_enumeration(n, r)
            b = path_tilings(n, r)
            c = closed_formula(n, r)
            assert a == b == c, (n, r, a, b, c)
            counts["path_three_way"] += 1
    for n in (18, 19, 20, 21, 40, 41, 100, 101, 200):
        for r in (1, 2, 3, 1000003):
            assert path_tilings(n, r) == closed_formula(n, r), (n, r)
            counts["path_large"] += 1
    for length in range(1, 65):
        assert interval_claw_free(length), length
        counts["claw_free"] += 1
    for length in range(1, 10):
        for _ in range(35):
            singles = tuple(rng.randint(1, 6) for _ in range(length))
            blocks = {(i, size): rng.randint(1, 5)
                      for size in (2, 3)
                      for i in range(length - size + 1)}
            assert weighted_tilings(singles, blocks) == weighted_interval_independence(singles, blocks)
            counts["weighted_tiling"] += 1
    for n in range(2, 151):
        for r in (1, 2, 3, 7, 1000003):
            a = path_tilings(n, r)
            assert all(x > 0 for x in a)
            assert newton_holds(a), (n, r)
            counts["newton"] += 1
    print("PASS", counts, "total", sum(counts.values()))

if __name__ == "__main__":
    main()
