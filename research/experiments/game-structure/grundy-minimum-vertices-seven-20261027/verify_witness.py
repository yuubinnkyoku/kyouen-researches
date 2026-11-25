#!/usr/bin/env python3
"""Independent occupied-independent-set recursion for exact minimum-order witnesses."""
from functools import lru_cache
from itertools import combinations

P3 = [(0, 1), (1, 2)]
G4 = [(0, 4), (0, 5), (0, 6), (1, 2), (1, 4), (1, 5), (2, 3)]
G6 = [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4),
      (3, 5), (4, 6), (7, 8), (7, 9)]
WITNESSES = [(0, []), (1, []), (3, P3), (4, P3),
             (7, G4), (8, G4), (10, G6), (11, G6)]


def occupied_game(n, edges):
    adj = [0] * n
    for a, b in edges:
        adj[a] |= 1 << b
        adj[b] |= 1 << a

    @lru_cache(None)
    def g(chosen):
        children = set()
        for v in range(n):
            if (chosen >> v) & 1 or adj[v] & chosen:
                continue
            children.add(g(chosen | (1 << v)))
        k = 0
        while k in children:
            k += 1
        return k

    first = [g(1 << v) for v in range(n)]
    return g(0), first, g.cache_info().currsize


def alpha(n, edges):
    return max((len(s) for k in range(n + 1)
                for s in combinations(range(n), k)
                if all(not (a in s and b in s) for a, b in edges)), default=0)


def main():
    for expected, (n, edges) in enumerate(WITNESSES):
        value, children, states = occupied_game(n, edges)
        assert value == expected, (n, expected, value, children)
        if expected:
            assert set(range(expected)).issubset(children)
        print(f"g={expected}: n={n}, edges={len(edges)}, "
              f"alpha={alpha(n, edges)}, first={children}, states={states}")

    hist = {}
    for bits in range(8):
        edges = [p for i, p in enumerate(combinations(range(3), 2))
                 if (bits >> i) & 1]
        value = occupied_game(3, edges)[0]
        hist[value] = hist.get(value, 0) + 1
        assert value <= 2
    assert hist == {0: 3, 1: 2, 2: 3}, hist
    print("n=3 all 8 labelled graphs:", hist)


if __name__ == "__main__":
    main()
