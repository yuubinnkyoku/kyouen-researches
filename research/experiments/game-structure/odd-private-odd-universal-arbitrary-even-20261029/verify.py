#!/usr/bin/env python3
"""Independent finite checks; the unbounded result is proved in README.md."""
from functools import lru_cache
from itertools import product
from random import Random


def mex(vals):
    x = 0
    while x in vals:
        x += 1
    return x


def quotient(a, n):
    p, h = [0] * (1 << n), [0] * (1 << n)
    for r in range(1, 1 << n):
        p[r] = sum(v for s, v in a.items() if s & r) % 2
        options = {p[r] ^ p[1 << c] for c in range(n) if r >> c & 1}
        for s, v in a.items():
            if v and s & r:
                q = r & ~s
                options.add(h[q] ^ p[r] ^ p[q] ^ 1)
        h[r] = mex(options)
    return h, p


def named(a, n, isolated=0):
    count = n + sum(a.values()) + isolated
    edges = [0] * count
    for c in range(n):
        edges[c] = ((1 << n) - 1) ^ (1 << c)
    j = n
    for s, v in sorted(a.items()):
        for _ in range(v):
            edges[j] |= s
            for c in range(n):
                if s >> c & 1:
                    edges[c] |= 1 << j
            j += 1
    closed = [edges[i] | 1 << i for i in range(count)]

    @lru_cache(None)
    def g(mask):
        if not mask:
            return 0
        opts = set()
        remaining = mask
        while remaining:
            b = remaining & -remaining
            opts.add(g(mask & ~closed[b.bit_length() - 1]))
            remaining ^= b
        return mex(opts)

    return g((1 << count) - 1), g.cache_info().currsize


def main():
    rng = Random(20261029)
    total, independent, max_states = 0, 0, 0
    for n in range(1, 5):
        full = (1 << n) - 1
        supports = [s for s in range(1, full + 1) if s.bit_count() >= 2]
        for flags in product((0, 2), repeat=len(supports)):
            a = {1 << c: 1 for c in range(n)}
            a[full] = a.get(full, 0) + 1
            for s, v in zip(supports, flags):
                a[s] = a.get(s, 0) + v
            h, p = quotient(a, n)
            assert all(h[r] == (2 if r.bit_count() & 1 else 3)
                       and p[r] == ((r.bit_count() + 1) & 1)
                       for r in range(1, full + 1))
            total += 1
            if n <= 3 or (sum(flags) <= 6 and rng.randrange(3) == 0):
                actual, states = named(a, n)
                assert actual == h[full]
                independent += 1
                max_states = max(max_states, states)

    for n, trials in ((1, 10), (2, 25), (3, 35), (4, 45), (5, 30), (6, 20)):
        full = (1 << n) - 1
        for _ in range(trials):
            a = {1 << c: (rng.choice((1, 3)) if n <= 3 else 1)
                 for c in range(n)}
            a[full] = a.get(full, 0) + (rng.choice((1, 3)) if n <= 3 else 1)
            supports = [s for s in range(1, full + 1) if s.bit_count() >= 2]
            rng.shuffle(supports)
            for s in supports[:rng.randrange(min(3 if n >= 4 else 4, len(supports)) + 1)]:
                a[s] = a.get(s, 0) + (rng.choice((2, 4)) if n <= 3 else 2)
            isolated = rng.randrange(3)
            if n + sum(a.values()) + isolated > 18:
                continue
            h, _ = quotient(a, n)
            actual, states = named(a, n, isolated)
            assert actual == (h[full] ^ (isolated & 1)) == ((2 if n & 1 else 3) ^ (isolated & 1))
            independent += 1
            max_states = max(max_states, states)
    for multiplicity, expected in ((1, 3), (2, 2)):
        a = {1: 1, 2: 1, 4: 1, 7: 1, 3: multiplicity}
        h, _ = quotient(a, 3)
        actual, states = named(a, 3)
        assert h[7] == actual == expected
        independent += 1
        max_states = max(max_states, states)
    print(f'PASS exhaustive_even_type_patterns={total} independent_named_cases={independent} max_named_states={max_states}')


if __name__ == '__main__':
    main()
