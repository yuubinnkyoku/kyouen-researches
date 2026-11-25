#!/usr/bin/env python3
"""Named-vertex closed-neighborhood recursion, independent of the clique-mask quotient."""
from functools import lru_cache
from itertools import combinations, product
from random import Random


def graph(k, missing, leaves, multiplicities):
    adj = [(1 << k) - 1 - (1 << i) for i in range(k)]
    for i, t in enumerate(leaves):
        for _ in range(t):
            p = len(adj)
            adj.append(1 << i)
            adj[i] |= 1 << p
    for (i, j), t in multiplicities.items():
        assert (i, j) not in missing and t > 0
        for _ in range(t):
            p = len(adj)
            adj.append((1 << i) | (1 << j))
            adj[i] |= 1 << p
            adj[j] |= 1 << p
    return adj


def direct(adj):
    @lru_cache(None)
    def g(mask):
        if not mask:
            return 0
        values = set()
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            i = bit.bit_length() - 1
            remaining ^= bit
            values.add(g(mask & ~(bit | adj[i])))
        result = 0
        while result in values:
            result += 1
        return result
    return g((1 << len(adj)) - 1)


def closed_form(k, leaves, mult):
    u = (sum(leaves) + sum(mult.values())) & 1
    z = [leaves[i] & 1 for i in range(k)]
    for (i, j), n in mult.items():
        z[i] ^= n & 1
        z[j] ^= n & 1
    return (1 ^ u ^ z[0]) if len(set(z)) == 1 else (2 + u)


def check(k, missing, leaves, mult):
    a = direct(graph(k, missing, leaves, mult))
    b = closed_form(k, leaves, mult)
    assert a == b, (k, missing, leaves, mult, a, b)


def main():
    count = 0
    for missing in [(), ((0, 1),)]:
        pairs = [p for p in combinations(range(3), 2) if p not in missing]
        for leaves in product(range(3), repeat=3):
            for multiplicities in product((1, 2), repeat=len(pairs)):
                check(3, missing, leaves, dict(zip(pairs, multiplicities)))
                count += 1
    print(f"DIRECT exhaustive k=3: {count} representatives PASS")
    rng = Random(20261028)
    for k in (4, 5, 6):
        trials = 80 if k == 4 else (24 if k == 5 else 8)
        for _ in range(trials):
            pairs = list(combinations(range(k), 2))
            rng.shuffle(pairs)
            missing = []
            used = set()
            for i, j in pairs:
                if i not in used and j not in used and rng.randrange(2):
                    missing.append((i, j))
                    used.update((i, j))
            missing = tuple(missing)
            available = [p for p in combinations(range(k), 2) if p not in missing]
            leaves = [rng.randrange(3 if k == 4 else 2) for _ in range(k)]
            mult = {p: rng.randrange(1, 3) if k == 4 else 1 for p in available}
            check(k, missing, leaves, mult)
            count += 1
        print(f"DIRECT k={k}: {trials} deterministic examples PASS")
    print(f"PASS independent named-vertex checks={count}")


if __name__ == '__main__':
    main()
