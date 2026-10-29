#!/usr/bin/env python3
"""Named-vertex Node Kayles audit: odd singleton, even higher supports."""
from functools import lru_cache
from itertools import combinations
import random

def named_grundy(k, leaf_counts, support_counts):
    assert len(leaf_counts) == k and all(t > 0 and t % 2 for t in leaf_counts)
    assert all(len(s) >= 2 and len(set(s)) == len(s) and
               all(0 <= i < k for i in s) and r > 0 and r % 2 == 0
               for s, r in support_counts.items())
    adj = [0] * k
    for i in range(k):
        for j in range(i + 1, k):
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    for i, t in enumerate(leaf_counts):
        for _ in range(t):
            v = len(adj)
            adj.append(1 << i)
            adj[i] |= 1 << v
    for support, count in support_counts.items():
        mask = sum(1 << i for i in support)
        for _ in range(count):
            v = len(adj)
            adj.append(mask)
            for i in support:
                adj[i] |= 1 << v
    n = len(adj)

    @lru_cache(maxsize=None)
    def sg(active):
        isolated = 0
        bits = active
        while bits:
            bit = bits & -bits
            v = bit.bit_length() - 1
            if adj[v] & active == 0:
                isolated |= bit
            bits -= bit
        if isolated:
            return (isolated.bit_count() & 1) ^ sg(active ^ isolated)
        if not active:
            return 0
        values = set()
        bits = active
        while bits:
            bit = bits & -bits
            v = bit.bit_length() - 1
            bits -= bit
            values.add(sg(active & ~(adj[v] | bit)))
        g = 0
        while g in values:
            g += 1
        return g
    return sg((1 << n) - 1), sg.cache_info().currsize, n

def check(k, leaves, supports):
    got, states, n = named_grundy(k, leaves, supports)
    if got != (k & 1):
        raise AssertionError((k, leaves, supports, got))
    return states, n

def main():
    total = max_vertices = max_states = 0
    exhaustive = 0
    for k in range(5):
        supports = [s for size in range(2, k+1)
                    for s in combinations(range(k), size)]
        for mask in range(1 << len(supports)):
            selected = {s: 2 for b, s in enumerate(supports) if mask >> b & 1}
            states, n = check(k, [1] * k, selected)
            exhaustive += 1
            total += 1
            max_vertices, max_states = max(max_vertices, n), max(max_states, states)
    rng = random.Random(20261029)
    randomized = 0
    for k in range(1, 9):
        all_supports = [s for size in range(2, k+1)
                        for s in combinations(range(k), size)]
        for _ in range(30):
            selected = rng.sample(all_supports, min(len(all_supports), rng.randrange(8)))
            counts = {s: rng.choice((2, 4, 6)) for s in selected}
            leaves = [rng.choice((1, 3, 5)) for _ in range(k)]
            states, n = check(k, leaves, counts)
            randomized += 1
            total += 1
            max_vertices, max_states = max(max_vertices, n), max(max_states, states)
    assert (exhaustive, randomized) == (2068, 240)
    print(f"PASS exhaustive={exhaustive} randomized={randomized} total={total} "
          f"max_vertices={max_vertices} max_memo_states={max_states}")

if __name__ == "__main__":
    main()
