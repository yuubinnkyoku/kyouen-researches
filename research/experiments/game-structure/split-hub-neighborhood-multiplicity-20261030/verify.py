#!/usr/bin/env python3
"""Exact rational check of neighborhood-type compression for random greedy Node Kayles."""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb
import random

ZERO = {}
ONE = {(0, 0): F(1)}


def add(a, b):
    z = dict(a)
    for e, v in b.items():
        z[e] = z.get(e, F(0)) + v
        if not z[e]:
            del z[e]
    return z


def mul(a, b):
    z = defaultdict(F)
    for (p, q), x in a.items():
        for (r, s), y in b.items():
            z[(p + r, q + s)] += x * y
    return {e: x for e, x in z.items() if x}


def power_one_minus(n, variable):
    return {(j, 0) if variable == 'v' else (0, j): F(comb(n, j) * (-1)**j)
            for j in range(n + 1)}


def integrate_u_y_to_v(poly):
    z = defaultdict(F)
    for (p, q), x in poly.items():
        z[(p + q + 1, 0)] += x / (q + 1)
        z[(p, q + 1)] -= x / (q + 1)
    return {e: x for e, x in z.items() if x}


def eval_y_zero(poly):
    return {(p, 0): x for (p, q), x in poly.items() if q == 0}


def integrate_v_zero_one(poly):
    assert all(q == 0 for p, q in poly)
    return sum((x / (p + 1) for (p, q), x in poly.items()), F(0))


def compressed_probs(t, neighborhoods, copies):
    """Probability some hub in each neighborhood-type clique is selected."""
    m, r = len(t), len(copies)
    assert len(neighborhoods) == r and all(c > 0 for c in copies)
    w = [x + 1 for x in t]
    fj = [add({e: x / w[j] for e, x in power_one_minus(w[j], 'u').items()},
              {e: t[j] * x / w[j] for e, x in power_one_minus(w[j], 'v').items()})
          for j in range(m)]
    ans = []
    for h in range(r):
        B = neighborhoods[h]
        others = [i for i in range(r) if i != h]
        Fsets = [ONE] + [ZERO] * ((1 << len(others)) - 1)
        unions = [B] + [0] * ((1 << len(others)) - 1)
        for mask in range(1, 1 << len(others)):
            unions[mask] = B
            for bit, i in enumerate(others):
                if mask & (1 << bit):
                    unions[mask] |= neighborhoods[i]
        for mask in range(1, 1 << len(others)):
            total = ZERO
            for bit, i in enumerate(others):
                if not mask & (1 << bit):
                    continue
                prev = mask ^ (1 << bit)
                term = mul(Fsets[prev], {e: x * copies[i] for e, x in power_one_minus(copies[i] - 1, 'u').items()})
                newly = neighborhoods[i] & ~unions[prev]
                for j in range(m):
                    if newly >> j & 1:
                        term = mul(term, fj[j])
                integ = integrate_u_y_to_v(term)
                total = add(total, {e: -x for e, x in integ.items()})
            Fsets[mask] = total
        total = ZERO
        for mask in range(1 << len(others)):
            term = eval_y_zero(Fsets[mask])
            for j in range(m):
                if not (unions[mask] >> j & 1):
                    term = mul(term, eval_y_zero(fj[j]))
            total = add(total, term)
        exponent = copies[h] - 1 + sum(w[j] for j in range(m) if B >> j & 1)
        total = mul(total, {e: x * copies[h] for e, x in power_one_minus(exponent, 'v').items()})
        ans.append(integrate_v_zero_one(total))
    return tuple(ans)


def direct_probs(t, neighborhoods, copies):
    m, r = len(t), len(copies)
    groups = []
    for j in range(m):
        groups.extend([-1] * t[j])
    for h, c in enumerate(copies):
        groups.extend([h] * c)
    n = m + len(groups)
    adj = [0] * n
    for p in range(m, n):
        for q in range(m, n):
            if p != q:
                adj[p] |= 1 << q
        h = groups[p - m]
        for j in range(m):
            if (h == -1 and sum(t[:j]) <= p - m < sum(t[:j + 1])) or (h >= 0 and (neighborhoods[h] >> j & 1)):
                adj[p] |= 1 << j
                adj[j] |= 1 << p

    @lru_cache(None)
    def solve(mask):
        if not mask:
            return (F(0),) * r
        total = [F(0)] * r
        size = mask.bit_count()
        for p in range(n):
            if not mask >> p & 1:
                continue
            if p >= m:
                h = groups[p - m]
                if h >= 0:
                    total[h] += F(1, size)
            else:
                tail = solve(mask & ~(adj[p] | (1 << p)))
                for h in range(r):
                    total[h] += tail[h] / size
        return tuple(total)

    return solve((1 << n) - 1)


def run():
    rng = random.Random(20261030)
    cases = []
    for m in range(1, 4):
        for r in range(1, 3):
            for As in product(range(1 << m), repeat=r):
                for cs in product((1, 2), repeat=r):
                    for ts in product((0, 1), repeat=m):
                        if m + sum(cs) + sum(ts) <= 8:
                            cases.append((ts, As, cs))
    rng.shuffle(cases)
    cases = cases[:280]
    for _ in range(90):
        m, r = rng.randint(1, 4), rng.randint(1, 3)
        As = tuple(rng.randrange(1 << m) for _ in range(r))
        cs = tuple(rng.randint(1, 3) for _ in range(r))
        ts = tuple(rng.randint(0, 2) for _ in range(m))
        if m + sum(cs) + sum(ts) <= 12:
            cases.append((ts, As, cs))
    for index, (ts, As, cs) in enumerate(cases):
        x = compressed_probs(ts, As, cs)
        y = direct_probs(ts, As, cs)
        assert x == y, (index, ts, As, cs, x, y)
        assert all(F(0) <= p <= F(1) for p in x) and sum(x) <= 1
    examples = [
        ((0, 0, 0), (0b011,), (7,)),
        ((1, 2, 0), (0b011, 0b110, 0b101), (2, 3, 1)),
        ((0, 1), (0b01, 0b10), (3, 4)),
    ]
    for t, a, c in examples:
        assert compressed_probs(t, a, c) == direct_probs(t, a, c)
    print('PASS', len(cases), 'random/exhaustive-sampled instances +', len(examples), 'targeted examples')
    for t, a, c in examples:
        print('example', t, a, c, compressed_probs(t, a, c))


if __name__ == '__main__':
    run()
