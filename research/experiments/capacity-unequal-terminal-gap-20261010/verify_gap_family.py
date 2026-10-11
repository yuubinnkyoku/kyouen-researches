#!/usr/bin/env python3
"""Direct-mex audit for top-two unequal-capacity family c=(r,1^k), limit r.

The recursive evaluator uses only the original legal-move definition, not the
closed form or the terminal classification. All safe states are visited.
"""
from functools import lru_cache
from itertools import product


def top_two(x):
    a = b = 0
    for v in x:
        if v >= a:
            a, b = v, a
        elif v > b:
            b = v
    return a + b


def predicted(r, k, x):
    ell, a = x[0], sum(x[1:])
    if a == 0 and ell == r:
        return 0
    if a == 0 and ell == r - 1 and k % 2 == 0:
        return 2
    return (r - 1 + k - sum(x)) % 2


def verify(r, k):
    capacities = (r,) + (1,) * k
    states = [x for x in product(*(range(c + 1) for c in capacities)) if top_two(x) <= r]
    @lru_cache(None)
    def grundy(x):
        children = set()
        for i, cap in enumerate(capacities):
            if x[i] < cap:
                y = x[:i] + (x[i] + 1,) + x[i+1:]
                if top_two(y) <= r:
                    children.add(grundy(y))
        g = 0
        while g in children:
            g += 1
        return g

    terminal_sizes = set()
    hist = {}
    for x in states:
        g = grundy(x)
        assert g == predicted(r, k, x), (r, k, x, g, predicted(r, k, x))
        hist[g] = hist.get(g, 0) + 1
        if not any(x[i] < capacities[i] and
                   top_two(x[:i] + (x[i]+1,) + x[i+1:]) <= r
                   for i in range(k+1)):
            terminal_sizes.add(sum(x))
    assert terminal_sizes == {r, r-1+k}, (r, k, terminal_sizes)
    assert len(states) == r*2**k+1, (r, k, len(states))
    return len(states), terminal_sizes, hist, grundy((0,)*(k+1))


def main():
    total = 0
    for r in range(2, 9):
        for k in range(1, 12):
            n, sizes, hist, root = verify(r, k)
            total += n
            print(f'r={r} k={k:2d} states={n:5d} terminals={sorted(sizes)} root={root} hist={dict(sorted(hist.items()))}')
    print(f'PASS: 77 parameter pairs, {total} safe states; all terminal sizes and all Grundy values agree')

if __name__ == '__main__':
    main()
