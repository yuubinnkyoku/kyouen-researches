#!/usr/bin/env python3
"""Independent named-vertex and support-mask mex verification for odd universal split graphs."""
from functools import lru_cache
from itertools import combinations
import random


def mex(vals):
    x = 0
    while x in vals:
        x += 1
    return x


def expected(counts, n):
    odd = sum(counts.get(1 << i, 0) % 2 for i in range(n))
    return 1 if odd == 0 else 2 if odd % 2 else 3


def quotient(counts, n):
    full = (1 << n) - 1

    @lru_cache(None)
    def parity(R):
        return sum(v for s, v in counts.items() if s & R) % 2

    @lru_cache(None)
    def h(R):
        if not R:
            return 0
        p = parity(R)
        children = set()
        for i in range(n):
            if R & (1 << i):
                children.add(p ^ parity(1 << i))
        for s, v in counts.items():
            if v == 0 or not (s & R):
                continue
            Q = R & ~s
            children.add(h(Q) ^ p ^ parity(Q) ^ 1)
        return mex(children)

    for R in range(1, full + 1):
        odd = sum(counts.get(1 << i, 0) % 2
                  for i in range(n) if R & (1 << i))
        target = 1 if odd == 0 else 2 if odd % 2 else 3
        assert h(R) == target, (n, counts, R, h(R), target)
    return h(full)


def named(counts, n, isolates=0):
    adj = [0] * n
    for i in range(n):
        adj[i] = ((1 << n) - 1) ^ (1 << i)
    for s, v in counts.items():
        for _ in range(v):
            j = len(adj)
            adj.append(s)
            for i in range(n):
                if s & (1 << i):
                    adj[i] |= 1 << j
    adj.extend([0] * isolates)
    close = [a | (1 << i) for i, a in enumerate(adj)]

    @lru_cache(None)
    def g(mask):
        if mask == 0:
            return 0
        iso = 0
        active = mask
        for i in range(len(adj)):
            if active & (1 << i) and not (adj[i] & active):
                active ^= 1 << i
                iso ^= 1
        if active != mask:
            return g(active) ^ iso
        vals = set()
        todo = active
        while todo:
            bit = todo & -todo
            i = bit.bit_length() - 1
            vals.add(g(active & ~close[i]))
            todo -= bit
        return mex(vals)

    return g((1 << len(adj)) - 1), g.cache_info().currsize


def check(counts, n, isolates=0):
    assert counts.get((1 << n) - 1, 0) % 2 == 1
    for s, v in counts.items():
        if s != (1 << n) - 1 and s.bit_count() >= 2:
            assert v % 2 == 0
    target = expected(counts, n)
    assert quotient(counts, n) == target
    got, states = named(counts, n, isolates)
    assert got == (target ^ (isolates & 1)), (
        n, counts, isolates, got, target)
    return states


def main():
    cases = 0
    maxstates = 0
    by_n = {}
    for n in range(2, 5):
        full = (1 << n) - 1
        middle = [s for s in range(1, full) if s.bit_count() >= 2]
        if n == 2:
            subsets = [()]
        elif n == 3:
            subsets = [
                tuple(middle[i] for i in range(len(middle))
                      if bits >> i & 1)
                for bits in range(1 << len(middle))]
        else:
            subsets = ([()] + [(s,) for s in middle]
                       + list(combinations(middle, 2)))
        countn = 0
        for odd_mask in range(1 << n):
            for extra in subsets:
                counts = {full: 1}
                for i in range(n):
                    counts[1 << i] = (odd_mask >> i) & 1
                for s in extra:
                    counts[s] = 2
                states = check(counts, n)
                maxstates = max(maxstates, states)
                cases += 1
                countn += 1
        by_n[n] = countn

    rng = random.Random(20261029)
    for n in (3, 4, 5, 6):
        full = (1 << n) - 1
        middle = [s for s in range(1, full) if s.bit_count() >= 2]
        for _ in range(70):
            counts = {full: rng.choice([1, 3, 5])}
            for i in range(n):
                counts[1 << i] = rng.choice([0, 1, 2, 3])
            for s in rng.sample(middle, min(len(middle), rng.randrange(4))):
                counts[s] = rng.choice([2, 4])
            iso = rng.randrange(3)
            states = check(counts, n, iso)
            maxstates = max(maxstates, states)
            cases += 1

    # Sharpness: one odd proper pair changes g=1 to g=2 (n=3).
    assert named({7: 1}, 3)[0] == 1
    assert named({7: 1, 3: 1}, 3)[0] == 2

    print(f'PASS named_and_quotient_cases={cases} '
          f'exhaustive_by_n={by_n} max_named_states={maxstates}')


if __name__ == '__main__':
    main()
