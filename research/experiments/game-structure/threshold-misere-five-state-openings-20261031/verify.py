#!/usr/bin/env python3
"""Independent finite checks of the threshold Node Kayles five-state formula."""
from functools import lru_cache
from itertools import product
import random

# E, A, B, C (the old C/F quotient), D.
OUTPUT = ((0, 1), (1, 0), (0, 1), (2, 2), (3, 3))
I_TRANS = (1, 2, 1, 4, 3)
D_TRANS = (1, 1, 3, 3, 4)

def build(word):
    adj = []
    for letter in word:
        n = len(adj)
        if letter == 'I':
            adj.append(0)
        else:
            for j in range(n):
                adj[j] |= 1 << n
            adj.append((1 << n) - 1)
    return tuple(adj)

def direct(adj):
    """Compute root and every child by closed-neighborhood deletion."""
    n = len(adj)
    @lru_cache(None)
    def rec(mask, terminal):
        if not mask:
            return terminal
        children = {rec(mask & ~(adj[v] | (1 << v)), terminal)
                    for v in range(n) if mask >> v & 1}
        value = 0
        while value in children:
            value += 1
        return value
    full = (1 << n) - 1
    root = (rec(full, 0), rec(full, 1))
    children = [(rec(full & ~(adj[v] | (1 << v)), 0),
                 rec(full & ~(adj[v] | (1 << v)), 1)) for v in range(n)]
    return root, children

def independent_set_recursion(adj):
    """Second representation: grow chosen independent sets, not remaining masks."""
    n = len(adj)
    @lru_cache(None)
    def rec(chosen, terminal):
        allowed = [v for v in range(n) if not (chosen >> v & 1)
                   and not (adj[v] & chosen)]
        if not allowed:
            return terminal
        values = {rec(chosen | (1 << v), terminal) for v in allowed}
        value = 0
        while value in values:
            value += 1
        return value
    return rec(0, 0), rec(0, 1)

def predicted(word):
    n = len(word)
    suffix = [0] * (n + 1)
    for j in range(n - 1, -1, -1):
        suffix[j] = suffix[j + 1] ^ (word[j] == 'I')
    state = 0
    children = []
    for j, letter in enumerate(word):
        p = suffix[j + 1]
        value = p if letter == 'D' else OUTPUT[state][0] ^ p
        children.append((value, 1 if value == 0 else 0 if value == 1 else value))
        state = (I_TRANS if letter == 'I' else D_TRANS)[state]
    return state, children

def check(word, independent=False):
    adj = build(word)
    root, children = direct(adj)
    state, expected_children = predicted(word)
    assert root == OUTPUT[state], (word, root, state)
    assert children == expected_children, (word, children, expected_children)
    if independent:
        assert independent_set_recursion(adj) == root, word
    assert all(not (g == 0 and h == 0) for g, h in children)
    return state

def main():
    counts = [0] * 5
    exhaustive = 0
    for n in range(14):
        for suffix in product('ID', repeat=max(0, n - 1)):
            word = '' if n == 0 else 'I' + ''.join(suffix)
            counts[check(word, independent=n <= 8)] += 1
            exhaustive += 1
    rng = random.Random(20261031)
    for _ in range(120):
        n = rng.randrange(14, 18)
        word = 'I' + ''.join(rng.choice('ID') for _ in range(n - 1))
        check(word)
    assert len(set(OUTPUT)) == 4
    assert OUTPUT[D_TRANS[0]] != OUTPUT[D_TRANS[2]]
    assert counts == [1, 609, 376, 3719, 3487]
    print('exhaustive=', exhaustive, 'random=', 120,
          'five_state_counts=', counts, 'max_g=', max(x[0] for x in OUTPUT))
    print('all checks passed')

if __name__ == '__main__':
    main()
