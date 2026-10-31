#!/usr/bin/env python3
"""Two-center shared independent vertices: symbolic induction and named graph audit.

No external packages.  The named-graph oracle never calls the symbolic formulas.
"""
from collections import Counter
from functools import lru_cache
from itertools import product
from random import Random


def mex(values):
    present = set(values)
    value = 0
    while value in present:
        value += 1
    return value


@lru_cache(None)
def private(z, o, e):
    """Independent recurrence for a clique with only private leaves."""
    if z + o + e == 0:
        return 0
    p = o & 1
    moves = []
    if z or e:
        moves.append(p)
    if o:
        moves.extend((p ^ 1, private(z, o - 1, e)))
    if e:
        moves.append(private(z, o, e - 1) ^ 1)
    return mex(moves)


def closed(a, b, c, z, o, e):
    """Proposed all-size closed formula, c>0; a,b are private leaf counts."""
    assert c >= 1
    pa, pb = a & 1, b & 1
    odd = o & 1
    if c & 1:
        # The already-proved single-shared-vertex formula.
        if z:
            if pa != pb:
                return 2 if odd else 3
            if pa == 0:
                return 3 if odd else 2
            return 0 if not o else (3 if odd else 2)
        if pa != pb:
            return 3 if odd else 2
        if pa == 0:
            if not e:
                return 0 if odd else 1
            return 2 if odd else 3
        if not o:
            return 3 if not e else 0
        return 2 if odd else 3
    # New even-positive shared class.
    if z:
        if pa != pb:
            return 3 if odd else 2
        if pa:
            return 2 if odd else 3
        if not o:
            return 1
        return 2 if odd else 3
    if pa != pb:
        return 2 if odd else 3
    if pa:
        if not e:
            return odd
        return 3 if odd else 2
    if not o and e:
        return 1
    return 3 if odd else 2


def formula_children(a, b, c, z, o, e):
    """Every possible move type, using the closed form for smaller o+e."""
    p = (a + b + c + o) & 1
    values = [(b + o) & 1, (a + o) & 1,
              private(z, o, e) ^ ((a + b + c - 1) & 1)]
    if z or e:
        values.append(p)
    if o:
        values.append(p ^ 1)
    if a:
        bc = b + c  # strictly positive
        values.append(private(z, o + (bc & 1), e + (1 - (bc & 1)))
                      ^ ((a - 1) & 1))
    if b:
        ac = a + c
        values.append(private(z, o + (ac & 1), e + (1 - (ac & 1)))
                      ^ ((b - 1) & 1))
    if o:
        values.append(closed(a, b, c, z, o - 1, e))
    if e:
        values.append(closed(a, b, c, z, o, e - 1) ^ 1)
    return values


def named_graph(a, b, c, others, isolates=0):
    """Direct vertex-labelled Node Kayles, independent of every class recurrence."""
    t = (a, b) + tuple(others)
    k = len(t)
    n = k + sum(t) + c + isolates
    adj = [1 << i for i in range(n)]
    for i in range(k):
        for j in range(i + 1, k):
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    v = k
    for i, count in enumerate(t):
        for _ in range(count):
            adj[i] |= 1 << v
            adj[v] |= 1 << i
            v += 1
    for _ in range(c):
        for i in (0, 1):
            adj[i] |= 1 << v
            adj[v] |= 1 << i
        v += 1
    assert v + isolates == n

    @lru_cache(None)
    def g(mask):
        moves = []
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            remaining -= bit
            i = bit.bit_length() - 1
            moves.append(g(mask & ~adj[i]))
        return mex(moves)

    return g((1 << n) - 1), g.cache_info().currsize


def main():
    representatives = 0
    for a, b, c, z, o, e in product(range(4), range(4), (1, 2),
                                     range(2), range(6), range(4)):
        expected = closed(a, b, c, z, o, e)
        observed = mex(formula_children(a, b, c, z, o, e))
        assert expected == observed, (a, b, c, z, o, e, expected, observed)
        representatives += 1

    # The new even-shared table is invariant under the remaining magnitudes.
    parity_classes = 0
    for c in (1, 2, 3, 4, 5, 6):
        for a, b, z, o, e in product(range(6), range(6), range(3),
                                     range(9), range(5)):
            assert closed(a, b, c, z, o, e) == closed(a, b, 1 if c & 1 else 2,
                                                    z, o, e)
            parity_classes += 1

    cases = states = 0
    histogram = Counter()
    for a, b, c, z, o, e in product(range(4), range(4), range(1, 5),
                                     range(3), range(3), range(3)):
        others = (0,) * z + (1,) * o + (2,) * e
        if 2 + len(others) + a + b + sum(others) + c > 17:
            continue
        for isolates in (0, 1):
            observed, visited = named_graph(a, b, c, others, isolates)
            expected = closed(a, b, c, z, o, e) ^ isolates
            assert observed == expected, (a, b, c, z, o, e, isolates,
                                          observed, expected)
            cases += 1
            states += visited
            histogram[observed] += 1

    rng = Random(20261030)
    random_cases = 0
    for _ in range(500):
        a, b, c = rng.randrange(6), rng.randrange(6), rng.randrange(1, 7)
        others = tuple(rng.randrange(7) for _ in range(rng.randrange(5)))
        if 2 + len(others) + a + b + sum(others) + c > 19:
            continue
        z = others.count(0)
        o = sum(t > 0 and t & 1 for t in others)
        e = sum(t > 0 and not t & 1 for t in others)
        observed, visited = named_graph(a, b, c, others)
        expected = closed(a, b, c, z, o, e)
        assert observed == expected, (a, b, c, others, observed, expected)
        random_cases += 1
        states += visited

    assert closed(0, 0, 1, 0, 0, 0) == 1
    assert closed(0, 0, 2, 0, 0, 0) == 2
    assert closed(1, 1, 1, 0, 0, 0) == 3
    assert closed(1, 1, 2, 0, 0, 0) == 0
    print('induction_representatives=', representatives)
    print('parity_formula_checks=', parity_classes)
    print('named_graph_cases=', cases)
    print('random_named_graph_cases=', random_cases)
    print('named_graph_states_sum=', states)
    print('named_graph_root_histogram=', dict(sorted(histogram.items())))
    print('c=1,2 with a=b=0:', [closed(0,0,c,0,0,0) for c in (1,2)])
    print('c=1,2 with a=b=1:', [closed(1,1,c,0,0,0) for c in (1,2)])
    print('all checks passed')


if __name__ == '__main__':
    main()
