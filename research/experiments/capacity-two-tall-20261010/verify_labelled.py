#!/usr/bin/env python3
"""Independent labelled-state audit for the two-tall capacity family."""
from functools import lru_cache
from itertools import product


def check(r, s, k):
    capacities = (r, s) + (1,) * k
    def safe(x):
        return sum(sorted(x, reverse=True)[:2]) <= r
    @lru_cache(None)
    def grundy(x):
        next_values = set()
        for i, ci in enumerate(capacities):
            if x[i] < ci:
                y = x[:i] + (x[i]+1,) + x[i+1:]
                if safe(y):
                    next_values.add(grundy(y))
        g = 0
        while g in next_values:
            g += 1
        return g
    def formula(x):
        a, b = x[:2]
        t = sum(x[2:])
        if a == r and b == t == 0:
            return 0
        if s == r and b == r and a == t == 0:
            return 0
        if k % 2 and a == r-1 and b == t == 0:
            return 2
        if k % 2 and s == r and b == r-1 and a == t == 0:
            return 2
        return (r+k-sum(x)) % 2
    count = 0
    terminals = set()
    maxg = 0
    for x in product(*(range(c+1) for c in capacities)):
        if not safe(x):
            continue
        g = grundy(x)
        want = formula(x)
        assert g == want, (r,s,k,x,g,want)
        count += 1
        maxg = max(maxg,g)
        if not any(x[i] < capacities[i] and safe(x[:i]+(x[i]+1,)+x[i+1:]) for i in range(len(x))):
            terminals.add(sum(x))
    assert terminals == {r, r+k}, (r,s,k,terminals)
    return count,maxg

if __name__ == '__main__':
    tests = states = 0
    counts = {}
    for r in range(2,10):
        for s in range(1,r+1):
            for k in range(1,9):
                c,g = check(r,s,k)
                tests += 1
                states += c
                counts[g] = counts.get(g,0)+1
    print('parameter_triples=',tests,'labelled_safe_states=',states,'max_grundy_histogram=',counts)
