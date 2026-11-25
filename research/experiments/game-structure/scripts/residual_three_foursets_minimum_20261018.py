#!/usr/bin/env python3
"""Independent small incidence-type classification of root nimbers for 2 or 3 size-4 forbidden sets."""
from collections import Counter
from functools import lru_cache
from itertools import product


def types(k):
    for c in product(range(5), repeat=(1 << k) - 1):
        edges = [sum(c[t - 1] for t in range(1, 1 << k) if t & (1 << i)) for i in range(k)]
        if any(x != 4 for x in edges):
            continue
        if any(not any(c[t - 1] and (t & (1 << i)) and not (t & (1 << j))
                       for t in range(1, 1 << k))
               for i in range(k) for j in range(k) if i != j):
            continue
        yield c


def root_nimber(c, k):
    edges = [0] * k
    n = 0
    for t in range(1, 1 << k):
        for _ in range(c[t - 1]):
            for i in range(k):
                if t & (1 << i):
                    edges[i] |= 1 << n
            n += 1
    @lru_cache(None)
    def g(s):
        options = set()
        for i in range(n):
            if not (s >> i) & 1:
                child = s | (1 << i)
                if all((child & e) != e for e in edges):
                    options.add(g(child))
        m = 0
        while m in options:
            m += 1
        return m
    return g(0)


def main():
    for k in (2, 3):
        histogram = Counter()
        for c in types(k):
            histogram[(sum(c), root_nimber(c, k))] += 1
        print('k=', k, 'total=', sum(histogram.values()), 'by_n_and_root=', sorted(histogram.items()))
        if k == 2:
            assert histogram == {(5, 0): 1, (6, 2): 1, (7, 1): 1, (8, 0): 1}
        if k == 3:
            assert sum(histogram.values()) == 68
            assert {n: sum(v for (n0, g), v in histogram.items() if n0 == n and g == 3)
                    for n in range(5, 13)} == {5: 0, 6: 0, 7: 0, 8: 6, 9: 0, 10: 3, 11: 0, 12: 0}

if __name__ == '__main__':
    main()
