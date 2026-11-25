#!/usr/bin/env python3
"""Independent exhaustive checks of the residual-capacity-four g/h classification."""
from functools import lru_cache
from itertools import combinations
from random import Random


def mex(vals):
    vals = set(vals)
    k = 0
    while k in vals:
        k += 1
    return k


def swap(k):
    return 1 - k if k < 2 else k


def all_complexes(n):
    # Downward-closed families, including the empty face and excluding the empty family.
    order = sorted(range(1, 1 << n), key=lambda s: (s.bit_count(), s))

    def walk(i, faces):
        if i == len(order):
            yield frozenset(faces)
            return
        s = order[i]
        yield from walk(i + 1, faces)
        if all((s ^ (1 << v)) in faces for v in range(n) if s >> v & 1):
            faces.add(s)
            yield from walk(i + 1, faces)
            faces.remove(s)

    yield from walk(0, {0})


def graph_complex(n, edge_bits):
    pairs = list(combinations(range(n), 2))
    adjacency = [0] * n
    for i, (u, v) in enumerate(pairs):
        if edge_bits >> i & 1:
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
    safe = {0}
    for s in range(1, 1 << n):
        v = (s & -s).bit_length() - 1
        rest = s ^ (1 << v)
        if rest in safe and not (adjacency[v] & rest):
            safe.add(s)
    return safe


def check_complex(n, safe):
    @lru_cache(None)
    def children(s):
        return tuple(s | (1 << v) for v in range(n)
                     if not (s >> v & 1) and (s | (1 << v)) in safe)

    @lru_cache(None)
    def exact(s):
        ch = children(s)
        return mex(exact(t)[0] for t in ch), (mex(exact(t)[1] for t in ch) if ch else 1)

    @lru_cache(None)
    def capacity(s):
        ch = children(s)
        return 1 + max(map(capacity, ch)) if ch else 0

    def type_from_local_sets(s):
        # s is a child of a root of capacity <=4, hence cap(s)<=3.
        moves = children(s)
        if not moves:
            return 'a', (0, 1)
        u = set()
        for t in moves:
            # A: some legal pair from s, ending after that pair.
            a = any(not children(z) for z in children(t))
            # B: some legal triple from s.
            b = any(children(z) for z in children(t))
            u.add(2 if a and b else 1 if a else 0)
        g, h = mex(u), mex(swap(v) for v in u)
        name = {(0, 1): 'a', (1, 0): 'b', (2, 2): 'c',
                (3, 3): 'd', (0, 0): 'e'}[(g, h)]
        return name, (g, h)

    count = failures = exception_00 = exception_11 = common = 0
    for s in safe:
        if capacity(s) > 4:
            continue
        count += 1
        ch = children(s)
        if not ch:
            assert exact(s) == (0, 1)
            continue
        named = [type_from_local_sets(t) for t in ch]
        types = {x[0] for x in named}
        g = mex(x[1][0] for x in named)
        h = mex(x[1][1] for x in named)
        actual = exact(s)
        assert (g, h) == actual, (n, s, (g, h), actual)
        predicted_swap = (('a' in types or 'b' in types)
                          and ('e' not in types or ('a' in types and 'b' in types)))
        assert predicted_swap == (h == swap(g)), (n, s, types, (g, h))
        normal_winners = {t for t, (_, p) in zip(ch, named) if p[0] == 0}
        misere_winners = {t for t, (_, p) in zip(ch, named) if p[1] == 0}
        assert normal_winners == {t for t in ch if exact(t)[0] == 0}
        assert misere_winners == {t for t in ch if exact(t)[1] == 0}
        if h != swap(g):
            failures += 1
        if (g, h) == (0, 0):
            exception_00 += 1
        if (g, h) == (1, 1):
            exception_11 += 1
        if normal_winners & misere_winners:
            common += 1
            assert n >= 7
    return count, failures, exception_00, exception_11, common


def main():
    totals = [0] * 5
    counts = {}
    for n in range(6):
        num = 0
        for safe in all_complexes(n):
            num += 1
            values = check_complex(n, safe)
            totals = [a + b for a, b in zip(totals, values)]
        counts[n] = num
    print('all complexes n<=5:', counts, 'state totals:', totals)
    totals = [0] * 5
    for bits in range(1 << 15):
        vals = check_complex(6, graph_complex(6, bits))
        totals = [a + b for a, b in zip(totals, vals)]
    print('all 32768 labeled 6-vertex graphs:', totals)
    # C6 + isolated point: the graph has maximum independent set size 4.
    edges = {(i, (i + 1) % 6) for i in range(6)}
    pairs = list(combinations(range(7), 2))
    bits = sum(1 << i for i, (u, v) in enumerate(pairs)
               if (u, v) in edges or (v, u) in edges)
    safe = graph_complex(7, bits)
    root = check_complex(7, safe)
    @lru_cache(None)
    def gh(s):
        children = [s | 1 << v for v in range(7) if not (s >> v & 1) and (s | 1 << v) in safe]
        return (mex(gh(t)[0] for t in children), mex(gh(t)[1] for t in children) if children else 1)
    print('C6 + isolated vertex: max_capacity=', max(s.bit_count() for s in safe),
          'root (g,h)=', gh(0), 'isolated child=', gh(1 << 6),
          'states:', root)
    assert gh(0) == (1, 1) and gh(1 << 6) == (0, 0)
    rng = Random(20261031)
    totals = [0] * 5
    for _ in range(1500):
        bits = rng.getrandbits(21)
        vals = check_complex(7, graph_complex(7, bits))
        totals = [a + b for a, b in zip(totals, vals)]
    print('1500 seeded 7-vertex graphs:', totals)
    print('PASS')


if __name__ == '__main__':
    main()
