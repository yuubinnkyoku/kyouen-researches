#!/usr/bin/env python3
"""Exact two-coordinate SG kernel for odd-width finite pair-cap games.

The universal proof is in proof.md. No geometry or long-board assumption is
used here; transferring this kernel to a 3D prism requires K0340's hypotheses.
"""


def mex(values):
    result = 0
    while result in values:
        result += 1
    return result


def pair_table(m, r):
    if not isinstance(m, int) or not isinstance(r, int) or m < 0 or r < 0:
        raise ValueError('nonnegative integer m and r are required')
    cap = min(m, r)
    values = {}
    # Both successors increase a+b, so descending rows and columns are a
    # topological order. Keys are sorted largest/second-largest occupancies.
    for a in range(cap, -1, -1):
        for b in range(min(a, r-a), -1, -1):
            options = set()
            if a < cap and a+b < r:
                options.add(values[a+1, b])
            if b < a and a+b < r:
                options.add(values[a, b+1] ^ 1)
            values[a, b] = mex(options)
    return values


def grundy(x, m, r, table=None):
    if len(x) < 3 or len(x) % 2 != 1:
        raise ValueError('an odd number of at least three columns is required')
    if any(not isinstance(v, int) or not 0 <= v <= m for v in x):
        raise ValueError('occupancies must be integers between zero and m')
    a, b = sorted(x, reverse=True)[:2]
    if a+b > r:
        raise ValueError('pair-unsafe occupancy')
    if table is None:
        table = pair_table(m, r)
    return table[a, b] ^ ((sum(x)-a) % 2)


def capped_gap_formula(y, budget):
    if len(y) < 2 or len(y) % 2:
        raise ValueError('an even number of at least two gaps is required')
    if budget < 0 or any(v < 0 for v in y):
        raise ValueError('nonnegative gaps and diagonal budget are required')
    t, parity = min(y), sum(y) % 2
    if budget < t:
        return (parity+budget) % 2
    return 2*(t % 2)+parity


def root_grundy(w, m, r):
    if w < 3 or w % 2 != 1 or m < 0 or r < 0:
        raise ValueError('odd w>=3 and nonnegative m,r are required')
    if r % 2:
        return min(m, (r+1)//2) % 2
    return m % 2 if m < r else 0
