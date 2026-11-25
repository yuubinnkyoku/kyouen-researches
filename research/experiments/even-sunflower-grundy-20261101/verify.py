#!/usr/bin/env python3
"""Independent checks for even-r sunflower quota game formulae.

No external dependencies. All integer and exact finite enumeration.
"""
from functools import lru_cache
from itertools import product


def closed(c, b, f):
    p = (sum(b) + f) & 1
    m = min(b)
    if c == 0 or m == 0:
        return p, 1 - p
    if c >= m:
        return (2 + p, 2 + p) if m & 1 else (p, p)
    if c & 1:
        return 1 - p, p
    return (p, 2 + p) if m == c + 1 else (p, 1 - p)


def mex(values):
    i = 0
    while i in values:
        i += 1
    return i


def compressed(r, cmax, bmax, fmax):
    @lru_cache(None)
    def solve(c, b, f):
        children = [solve(c, b[:i] + (v - 1,) + b[i + 1:], f)
                    for i, v in enumerate(b) if v]
        if c and min(b):
            children.append(solve(c - 1, tuple(v - 1 for v in b), f))
        if f:
            children.append(solve(c, b, f - 1))
        if not children:
            return 0, 1
        return mex({v[0] for v in children}), mex({v[1] for v in children})

    tested = 0
    for c in range(cmax + 1):
        for b in product(range(bmax + 1), repeat=r):
            for f in range(fmax + 1):
                actual = solve(c, b, f)
                expect = closed(c, b, f)
                assert actual == expect, (r, c, b, f, actual, expect)
                tested += 1
    return tested


def pointwise(r, c, petals, quotas, free):
    n = c + sum(petals) + free
    masks = []
    for i in range(r):
        bits = (1 << c) - 1
        start = c + sum(petals[:i])
        bits |= ((1 << petals[i]) - 1) << start
        masks.append(bits)
    free_mask = ((1 << free) - 1) << (n - free)
    safe_count = 0

    @lru_cache(None)
    def solve(s):
        nonlocal safe_count
        occ = tuple((s & mask).bit_count() for mask in masks)
        if any(occ[i] > quotas[i] for i in range(r)):
            return None
        safe_count += 1
        children = []
        for i in range(n):
            if not (s >> i) & 1:
                child = solve(s | (1 << i))
                if child is not None:
                    children.append(child)
        actual = (mex({v[0] for v in children}),
                  mex({v[1] for v in children})) if children else (0, 1)
        j = (s & ((1 << c) - 1)).bit_count()
        b = tuple(quotas[i] - occ[i] for i in range(r))
        f = free - (s & free_mask).bit_count()
        expect = closed(c - j, b, f)
        assert actual == expect, (r, c, petals, quotas, free, s, actual, expect)
        return actual

    solve(0)
    return safe_count


def local_identity():
    # All 16 distinct (target, min-petal, core, optional) signatures.
    signatures = set()
    for c in range(1, 21):
        for m in range(1, 21):
            for p in (0, 1):
                v = (closed(c, (m, m), p),
                     closed(c, (m - 1, m - 1), 1 - p),
                     closed(c - 1, (m - 1, m - 1), p),
                     closed(c, (m, m), 1 - p))
                signatures.add(v)
                for optional in (False, True) if p == 0 else (True,):
                    children = [v[1], v[2]] + ([v[3]] if optional else [])
                    assert (mex({x[0] for x in children}),
                            mex({x[1] for x in children})) == v[0], (c, m, p, optional, v)
    assert len(signatures) == 16, len(signatures)
    return len(signatures)


def main():
    sig = local_identity()
    total = 0
    details = []
    for r, cm, bm, fm in ((2, 8, 12, 4), (4, 5, 5, 3),
                          (6, 4, 3, 2), (8, 2, 2, 1)):
        n = compressed(r, cm, bm, fm)
        total += n
        details.append((r, n))
    pointcases = 0
    states = 0
    for r in (2, 4, 6):
        for c in (0, 1, 2):
            for f in (0, 1):
                for pattern in (0, 1, 2):
                    quotas = tuple(1 + (i % 2 if pattern == 1 else 0)
                                   for i in range(r))
                    petals = tuple(quotas[i] +
                                   (1 if pattern == 2 and i == 0 else 0)
                                   for i in range(r))
                    n = c + sum(petals) + f
                    if n > 14:
                        continue
                    states += pointwise(r, c, petals, quotas, f)
                    pointcases += 1
    print(f'PASS signatures={sig}; compressed={total} {details}; '
          f'pointwise_boards={pointcases}; pointwise_states={states}')


if __name__ == '__main__':
    main()
