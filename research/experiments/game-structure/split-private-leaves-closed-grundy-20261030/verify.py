#!/usr/bin/env python3
"""Independent exact checks for the private-leaf split-graph Grundy formula.

Run with Python 3 standard library only.  No dependency on the repository.
"""
from collections import Counter
from functools import lru_cache
from itertools import product


def closed_form(t, isolated=0):
    z = sum(x == 0 for x in t)
    o = sum(x % 2 == 1 for x in t)
    e = sum(x > 0 and x % 2 == 0 for x in t)
    if z:
        base = 1 if o == 0 else (2 if o % 2 else 3)
    elif o:
        base = (o % 2) if e == 0 else (3 if o % 2 else 2)
    else:
        base = 0 if e == 0 else (2 if e == 1 else 1)
    return base ^ (isolated % 2)


@lru_cache(None)
def class_recurrence(z, o, e):
    if z + o + e == 0:
        return 0
    p = o & 1
    options = set()
    if z + e:
        options.add(p)
    if o:
        options.add(p ^ 1)
        options.add(class_recurrence(z, o - 1, e))
    if e:
        options.add(class_recurrence(z, o, e - 1) ^ 1)
    return next(i for i in range(5) if i not in options)


def named_graph_grundy(t, isolated=0):
    k = len(t)
    n = k + sum(t) + isolated
    neighbors = [0] * n
    for i in range(k):
        for j in range(i):
            neighbors[i] |= 1 << j
            neighbors[j] |= 1 << i
    v = k
    for i, count in enumerate(t):
        for _ in range(count):
            neighbors[i] |= 1 << v
            neighbors[v] |= 1 << i
            v += 1

    @lru_cache(None)
    def solve(mask):
        if mask == 0:
            return 0
        vals = set()
        x = mask
        while x:
            bit = x & -x
            i = bit.bit_length() - 1
            vals.add(solve(mask & ~(bit | neighbors[i])))
            x ^= bit
        return next(i for i in range(6) if i not in vals)

    return solve((1 << n) - 1), solve.cache_info().currsize


def main():
    cases = 0
    states = 0
    hist = Counter()
    # All named graphs with <=5 clique vertices, 0..4 private
    # leaves per center, <=15 vertices, and 0..1 isolates.
    for k in range(6):
        for t in product(range(5), repeat=k):
            for isolated in (0, 1):
                if k + sum(t) + isolated > 15:
                    continue
                expected = closed_form(t, isolated)
                actual, nstates = named_graph_grundy(t, isolated)
                assert actual == expected, (t, isolated, actual, expected)
                cases += 1
                states += nstates
                hist[actual] += 1

    count_triples = 0
    for k in range(151):
        for z in range(k + 1):
            for o in range(k - z + 1):
                e = k - z - o
                t = (0,) * z + (1,) * o + (2,) * e
                assert class_recurrence(z, o, e) == closed_form(t)
                count_triples += 1
    print('named_graph_cases=', cases)
    print('named_graph_memo_states_sum=', states)
    print('named_graph_root_histogram=', dict(sorted(hist.items())))
    print('class_recurrence_triples=', count_triples)
    print('example t=(1,2):', named_graph_grundy((1, 2))[0])
    print('all checks passed')


if __name__ == '__main__':
    main()
