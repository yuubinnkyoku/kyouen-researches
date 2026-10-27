#!/usr/bin/env python3
"""Independent vertex-level recurrences for the split-graph witness and samples."""
from functools import lru_cache
from random import Random

WITNESS = (2, 8, 11, 11, 12, 14, 24, 26)


def graph(clique_size, signatures):
    n = clique_size + len(signatures)
    closed = [1 << i for i in range(n)]
    for i in range(clique_size):
        for j in range(i + 1, clique_size):
            closed[i] |= 1 << j
            closed[j] |= 1 << i
    for j, signature in enumerate(signatures):
        assert 0 <= signature < (1 << clique_size)
        for i in range(clique_size):
            if signature & (1 << i):
                closed[i] |= 1 << (clique_size + j)
                closed[clique_size + j] |= 1 << i
    return closed


def exact(closed):
    n = len(closed)
    full = (1 << n) - 1

    @lru_cache(None)
    def remaining(mask):
        values = {remaining(mask & ~closed[i]) for i in range(n)
                  if mask & (1 << i)}
        return next(x for x in range(n + 1) if x not in values)

    @lru_cache(None)
    def occupied(chosen):
        values = {occupied(chosen | (1 << i)) for i in range(n)
                  if not (chosen & closed[i])}
        return next(x for x in range(n + 1) if x not in values)

    a = remaining(full)
    b = occupied(0)
    children_a = tuple(remaining(full & ~closed[i]) for i in range(n))
    children_b = tuple(occupied(1 << i) for i in range(n))
    assert (a, children_a) == (b, children_b)
    return a, children_a


def main():
    value, children = exact(graph(5, WITNESS))
    assert value == 4
    assert children == (0, 1, 0, 1, 0, 2, 3, 0, 0, 3, 0, 3, 0)
    assert exact(graph(5, WITNESS + (0,)))[0] == 5

    rng = Random(20261027)
    for c in (4, 5):
        for _ in range(200):
            if c == 4:
                signatures = tuple(s for s in rng.sample(range(1, 16), 5)
                                   for _ in range(rng.randrange(3)))
            else:
                signatures = tuple(rng.randrange(1, 32)
                                   for _ in range(rng.randrange(8)))
            assert exact(graph(c, signatures))[0] <= 3
    print("independent recurrences: 13-vertex witness, isolated extension,"
          " 400 samples OK")


if __name__ == "__main__":
    main()
