#!/usr/bin/env python3
"""Independent subset recursion vs closed vertex-cover-two formula."""
from collections import Counter
from functools import lru_cache


def star(leaves):
    return 2 if leaves > 0 and leaves % 2 == 0 else 1


def formula(a, b, c, joined, free=0):
    """a,b,c: adjacent only to x, only to y, to both; free: isolated."""
    moves = {b % 2 if joined else star(b),
             a % 2 if joined else star(a)}
    if a:
        moves.add(star(b + c) ^ ((a - 1) % 2))
    if b:
        moves.add(star(a + c) ^ ((b - 1) % 2))
    if c:
        moves.add((a + b + c - 1) % 2)
    mex = 0
    while mex in moves:
        mex += 1
    return mex ^ (free % 2)


def direct(a, b, c, joined, free=0):
    n = 2 + a + b + c + free
    adj = [0] * n

    def edge(u, v):
        adj[u] |= 1 << v
        adj[v] |= 1 << u

    if joined:
        edge(0, 1)
    for i in range(2, 2 + a):
        edge(0, i)
    for i in range(2 + a, 2 + a + b):
        edge(1, i)
    for i in range(2 + a + b, 2 + a + b + c):
        edge(0, i)
        edge(1, i)

    @lru_cache(None)
    def recurse(mask):
        options = set()
        m = mask
        while m:
            bit = m & -m
            v = bit.bit_length() - 1
            options.add(recurse(mask & ~(bit | adj[v])))
            m -= bit
        value = 0
        while value in options:
            value += 1
        return value

    return recurse((1 << n) - 1)


def main():
    small = Counter()
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for joined in range(2):
                    g = formula(a, b, c, joined)
                    assert g <= 3
                    small[g] += 1
    assert [small[i] for i in range(4)] == [16, 9, 11, 18]

    tested = 0
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for joined in range(2):
                    for free in range(2):
                        predicted = formula(a, b, c, joined, free)
                        actual = direct(a, b, c, joined, free)
                        assert predicted == actual, (a, b, c, joined, free, predicted, actual)
                        tested += 1
    assert tested == 256
    assert formula(1, 1, 1, 0) == direct(1, 1, 1, 0) == 3  # P5
    assert formula(2, 0, 0, 0, 0) == 3  # K1,2 plus isolated cover vertex
    print('reduced 54 states:', [small[i] for i in range(4)])
    print('independent full-subset recursions:', tested, 'cases matched')
    print('sharp witnesses: P5=3; K1,2 + isolated vertex=3')


if __name__ == '__main__':
    main()
