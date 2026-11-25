#!/usr/bin/env python3
"""Independent occupied-set recursion, without closed-neighborhood deletion."""
from functools import lru_cache

def solve(centers, supports):
    n = centers + len(supports)
    forbidden = []
    for i in range(centers):
        for j in range(i + 1, centers):
            forbidden.append((1 << i) | (1 << j))
    for j, support in enumerate(supports):
        for i in range(centers):
            if support & (1 << i):
                forbidden.append((1 << i) | (1 << (centers + j)))

    @lru_cache(None)
    def grundy(occupied):
        options = set()
        for v in range(n):
            bit = 1 << v
            if occupied & bit:
                continue
            extended = occupied | bit
            if any((extended & edge) == edge for edge in forbidden):
                continue
            options.add(grundy(extended))
        value = 0
        while value in options:
            value += 1
        return value

    return grundy(0), [grundy(1 << v) for v in range(n)], grundy.cache_info().currsize

def main():
    base = [1, 2, 4, 8, 3, 12]
    extended = base + [15, 15]
    a, b = solve(4, base), solve(4, extended)
    assert a[:2] == (1, [0] * 8 + [3, 3]), a
    assert b[:2] == (2, [0] * 4 + [3] * 6 + [1, 1]), b
    print("base:", a)
    print("extended:", b)
    print("independent occupied-set verification passed")

if __name__ == "__main__":
    main()
