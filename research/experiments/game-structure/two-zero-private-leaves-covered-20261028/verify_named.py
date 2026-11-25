#!/usr/bin/env python3
"""Independent literal-vertex closed-neighborhood recursion for split Node Kayles.

No clique-subset parity quotient or proposed formula is used in the recursion.
"""
from functools import lru_cache
from itertools import product
from random import Random


def literal_grundy(k, leaves, pairs):
    adjacency = [(1 << k) - 1 - (1 << i) for i in range(k)]
    n = k

    def add_vertex(neighbors):
        nonlocal n
        adjacency.append(sum(1 << i for i in neighbors))
        for i in neighbors:
            adjacency[i] |= 1 << n
        n += 1

    for i, count in enumerate(leaves):
        for _ in range(count):
            add_vertex((i,))
    for (i, j), count in zip(((i, j) for i in range(k) for j in range(i + 1, k)), pairs):
        for _ in range(count):
            add_vertex((i, j))

    @lru_cache(None)
    def grundy(mask):
        seen = set()
        pending = mask
        while pending:
            bit = pending & -pending
            pending -= bit
            i = bit.bit_length() - 1
            seen.add(grundy(mask & ~(adjacency[i] | bit)))
        value = 0
        while value in seen:
            value += 1
        return value

    return grundy((1 << n) - 1)


def formula(k, leaves, pairs):
    u = (sum(leaves) + sum(pairs)) & 1
    z = [x & 1 for x in leaves]
    for (i, j), count in zip(((i, j) for i in range(k) for j in range(i + 1, k)), pairs):
        z[i] ^= count & 1
        z[j] ^= count & 1
    return (1 ^ u ^ z[0]) if len(set(z)) == 1 else 2 + u


def admissible(k, leaves, pairs):
    if leaves.count(0) > 2:
        return False
    degree = list(leaves)
    for (i, j), count in zip(((i, j) for i in range(k) for j in range(i + 1, k)), pairs):
        degree[i] += count
        degree[j] += count
    return all(degree)


def check(k, leaves, pairs):
    actual = literal_grundy(k, leaves, pairs)
    expected = formula(k, leaves, pairs)
    assert actual == expected, (k, leaves, pairs, actual, expected)


def main():
    count = 0
    for leaves in product((0, 1, 2), repeat=3):
        for pairs in product((0, 1, 2), repeat=3):
            if admissible(3, leaves, pairs):
                check(3, leaves, pairs)
                count += 1
    assert count == 636
    print(f"PASS literal k=3 exhaustive: {count}")

    rng = Random(20261028)
    for k, target in ((4, 192), (5, 64), (6, 16)):
        checked = 0
        while checked < target:
            leaves = tuple(rng.randrange(3) for _ in range(k))
            if leaves.count(0) > 2:
                continue
            pairs = tuple(rng.choice((0, 0, 1, 2)) if k <= 4
                          else rng.choice((0, 0, 0, 1, 2))
                          for _ in range(k * (k - 1) // 2))
            if not admissible(k, leaves, pairs):
                continue
            check(k, leaves, pairs)
            checked += 1
        print(f"PASS literal k={k} samples: {checked}")

    # Three zero-private-leaf clique vertices are not covered by the theorem.
    for k, expected in ((4, 2), (5, 4)):
        leaves = (1, 0, 0, 0) + ((1,) if k == 5 else ())
        pairs = tuple(2 if i == 0 and 1 <= j <= 3 else 0
                      for i in range(k) for j in range(i + 1, k))
        actual = literal_grundy(k, leaves, pairs)
        forecast = formula(k, leaves, pairs)
        assert actual == expected and actual != forecast, (k, actual, forecast)
        print(f"PASS three-zero counterexample k={k}: g={actual}, formula={forecast}")


if __name__ == "__main__":
    main()
