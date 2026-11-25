#!/usr/bin/env python3
"""Exact marked-hub probabilities for split graphs with private leaves."""
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product
from random import Random


def marked_hub_probability(t, neighborhoods, h):
    """Inclusion-exclusion of earlier eligible hubs, integrated over ordered ranks."""
    m, k = len(t), len(neighborhoods)
    target = neighborhoods[h]
    rest = tuple(i for i in range(k) if i != h)
    answer = Fraction()
    for s in range(k):
        for sub in combinations(rest, s):
            for order in permutations(sub):
                # chronological order: order[0], ..., order[-1], h
                ordered = order + (h,)
                n = len(ordered)
                terms = {(0,) * n: Fraction(1)}
                for j in range(m):
                    w = t[j] + 1
                    if j in target:
                        # x_h^w (both contributions coalesce)
                        new = {}
                        for a, v in terms.items():
                            b = list(a); b[-1] += w
                            new[tuple(b)] = new.get(tuple(b), Fraction()) + v
                        terms = new
                        continue
                    last = -1
                    for pos, hub in enumerate(order):
                        if j in neighborhoods[hub]:
                            last = pos
                    new = defaultdict(Fraction)
                    for a, v in terms.items():
                        if last >= 0:
                            b = list(a); b[last] += w
                            new[tuple(b)] += v / w
                        else:
                            new[a] += v / w
                        if t[j]:
                            b = list(a); b[-1] += w
                            new[tuple(b)] += v * t[j] / w
                    terms = new
                value = Fraction()
                for a, coeff in terms.items():
                    denom = 1
                    total = 0
                    for idx in range(n - 1, -1, -1):
                        total += a[idx] + 1
                        denom *= total
                    value += coeff / denom
                answer += (-1)**s * value
    return answer


def direct_distribution(t, neighborhoods):
    m, k = len(t), len(neighborhoods)
    n = m + sum(t) + k
    adj = [0] * n
    private = []
    pos = m
    for j, count in enumerate(t):
        for _ in range(count):
            private.append(pos)
            adj[j] |= 1 << pos
            adj[pos] |= 1 << j
            pos += 1
    hubs = list(range(pos, n))
    centers = private + hubs
    for a in centers:
        for b in centers:
            if a != b:
                adj[a] |= 1 << b
    for h, near in enumerate(neighborhoods):
        for j in near:
            adj[j] |= 1 << hubs[h]
            adj[hubs[h]] |= 1 << j
    @lru_cache(None)
    def rec(mask):
        if not mask:
            return (Fraction(1),) + (Fraction(0),) * k
        cnt = mask.bit_count()
        ans = [Fraction()] * (k + 1)
        remain = mask
        while remain:
            bit = remain & -remain
            v = bit.bit_length() - 1
            remain ^= bit
            if v in hubs:
                ans[1 + hubs.index(v)] += Fraction(1, cnt)
            else:
                nxt = rec(mask & ~(adj[v] | bit))
                for i, val in enumerate(nxt):
                    ans[i] += val / cnt
        return tuple(ans)
    return rec((1 << n) - 1)


def permutation_distribution(t, neighborhoods):
    """Independent all-priority-order simulation, without using the recursion."""
    m, k = len(t), len(neighborhoods)
    private = [(j, z) for j, count in enumerate(t) for z in range(count)]
    n = m + len(private) + k
    def adjacent(a, b):
        if a == b:
            return False
        if a >= m and b >= m:
            return True
        if a < m and b < m:
            return False
        j, center = (a, b) if a < m else (b, a)
        if center < m + len(private):
            return private[center - m][0] == j
        return j in neighborhoods[center - m - len(private)]
    counts = [0] * (k + 1)
    for order in permutations(range(n)):
        chosen = []
        special = 0
        for v in order:
            if all(not adjacent(v, u) for u in chosen):
                chosen.append(v)
                if v >= m + len(private):
                    special = 1 + v - m - len(private)
        counts[special] += 1
    return tuple(Fraction(x, sum(counts)) for x in counts)


def check():
    tested = 0
    permutation_tested = 0
    for m in range(1, 4):
        all_near = [frozenset(j for j in range(m) if bits & (1 << j)) for bits in range(1 << m)]
        for k in range(1, 4):
            for t in product(range(3), repeat=m):
                if m + sum(t) + k > 9:
                    continue
                for near in product(all_near, repeat=k):
                    expected = direct_distribution(t, near)
                    found = [marked_hub_probability(t, near, h) for h in range(k)]
                    assert tuple(found) == expected[1:], (t, near, found, expected)
                    assert expected[0] + sum(found) == 1
                    tested += 1
                    if m + sum(t) + k <= 7 and permutation_tested < 160 and tested % 17 == 0:
                        assert permutation_distribution(t, near) == expected
                        permutation_tested += 1
    print('all exhaustive small cases:', tested, 'all-priority-order independent:', permutation_tested)
    t = (0, 1, 2)
    near = (frozenset((0,1)),)
    print('one hub check',marked_hub_probability(t,near,0))
    t = (1,2,0)
    near = (frozenset((0,1)),frozenset((1,2)),frozenset((0,2)))
    print('three hub example', [str(marked_hub_probability(t,near,h)) for h in range(3)],'direct',tuple(map(str,direct_distribution(t,near))))
    rng=Random(20261030)
    for _ in range(250):
        m,k=4,3
        t=tuple(rng.randrange(3) for j in range(m))
        near=tuple(frozenset(j for j in range(m) if rng.randrange(2)) for h in range(k))
        expected=direct_distribution(t,near)
        assert tuple(marked_hub_probability(t,near,h) for h in range(k)) == expected[1:]
    print('random m=4,k=3 configurations: 250')

if __name__=='__main__':
    check()
