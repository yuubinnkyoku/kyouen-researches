#!/usr/bin/env python3
"""Independent audits of the six-state Node Kayles automaton for threshold graphs."""
from functools import lru_cache
import random

# Each state stores (Grundy number, set of child Grundy numbers).
STATES = ((0, ()), (1, (0,)), (0, (1,)), (2, (0, 1)),
          (3, (0, 1, 2)), (2, (0, 1, 3)))
ISOLATE = (1, 2, 1, 4, 5, 4)
DOMINATE = (1, 1, 3, 3, 4, 5)


def graph_from_word(word):
    # 0: add an isolated vertex; 1: add a dominating vertex.
    adj = []
    for operation in word:
        i = len(adj)
        if operation:
            for j in range(i):
                adj[j] |= 1 << i
            adj.append((1 << i) - 1)
        else:
            adj.append(0)
    return adj


def mex(values):
    i = 0
    while i in values:
        i += 1
    return i


def verify_word(word):
    state = 0
    for operation in word:
        state = (DOMINATE if operation else ISOLATE)[state]
    adj = graph_from_word(word)
    n = len(adj)
    full = (1 << n) - 1

    # Independent implementation A: remove closed neighborhoods from the live set.
    @lru_cache(None)
    def remove(live):
        if not live:
            return 0
        values = set()
        remaining = live
        while remaining:
            bit = remaining & -remaining
            remaining -= bit
            v = bit.bit_length() - 1
            values.add(remove(live & ~(adj[v] | bit)))
        return mex(values)

    # Independent implementation B: build independent sets of already chosen moves.
    @lru_cache(None)
    def choose(chosen):
        blocked = chosen
        remaining = chosen
        while remaining:
            bit = remaining & -remaining
            remaining -= bit
            blocked |= adj[bit.bit_length() - 1]
        values = set()
        available = full & ~blocked
        while available:
            bit = available & -available
            available -= bit
            values.add(choose(chosen | bit))
        return mex(values)

    children_a = set()
    children_b = set()
    for v in range(n):
        children_a.add(remove(full & ~(adj[v] | (1 << v))))
        children_b.add(choose(1 << v))
    expected = STATES[state]
    actual = (remove(full), tuple(sorted(children_a)))
    assert actual == expected, (word, actual, expected)
    assert choose(0) == expected[0], (word, 'occupied', choose(0), expected)
    assert children_a == children_b, (word, children_a, children_b)
    return state


def main():
    counts = [0] * len(STATES)
    exhaustive = 0
    # Fix the first operation to isolate: on the empty graph both operations coincide.
    for n in range(0, 14):
        for suffix in range(1 << max(0, n - 1)):
            word = () if n == 0 else (0,) + tuple((suffix >> i) & 1 for i in range(n - 1))
            counts[verify_word(word)] += 1
            exhaustive += 1
    rng = random.Random(20261027)
    random_count = 160
    for _ in range(random_count):
        n = rng.randrange(14, 20)
        word = (0,) + tuple(rng.randrange(2) for _ in range(n - 1))
        counts[verify_word(word)] += 1
    print('exhaustive_graphs=', exhaustive)
    print('random_graphs=', random_count)
    print('state_counts=', counts)
    print('max_grundy=', max(STATES[i][0] for i, count in enumerate(counts) if count))
    print('all checks passed')


if __name__ == '__main__':
    main()
