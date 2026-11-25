#!/usr/bin/env python3
"""Exact independent audit for hereditary placement games of residual capacity <=3.

The recursion computes normal and misere mex from the entire safe-face family.
The separate formula reads only feasible pairs and triples.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations
from random import Random


def mex(values):
    values = set(values)
    i = 0
    while i in values:
        i += 1
    return i


def tau(g):
    return 1 if g == 0 else 0 if g == 1 else g


def exact_values(faces, n):
    @lru_cache(None)
    def solve(s):
        children = [solve(s | (1 << v)) for v in range(n)
                    if not (s >> v & 1) and (s | (1 << v)) in faces]
        if not children:
            return 0, 1
        return mex(g for g, h in children), mex(h for g, h in children)
    return solve


def rank3_formula(faces, n, s):
    legal = [v for v in range(n)
             if not (s >> v & 1) and (s | (1 << v)) in faces]
    child = []
    for x in legal:
        sx = s | (1 << x)
        second = [y for y in legal
                  if y != x and (sx | (1 << y)) in faces]
        if not second:
            child.append(0)
            continue
        second_grundy = []
        for y in second:
            sy = sx | (1 << y)
            can_third = any(z != x and z != y
                            and (sy | (1 << z)) in faces for z in legal)
            second_grundy.append(1 if can_third else 0)
        child.append(mex(second_grundy))
    if not child:
        return (0, 1), False, ()
    return ((mex(child), mex(tau(v) for v in child)),
            all(v == 2 for v in child), tuple(child))


def check(faces, n, stats):
    solve = exact_values(faces, n)
    for s in faces:
        remaining_capacity = max((f & ~s).bit_count()
                                 for f in faces if f & s == s)
        if remaining_capacity > 3:
            continue
        predicted, exceptional, children = rank3_formula(faces, n, s)
        actual = solve(s)
        assert predicted == actual, (n, s, predicted, actual)
        assert (actual[1] != tau(actual[0])) == exceptional, (
            n, s, actual, exceptional, children)
        stats["positions"] += 1
        if exceptional:
            assert actual == (0, 0)
            stats["exceptions"] += 1


def all_complexes(n):
    # All downward-closed families containing the empty face.
    # Counts are Dedekind numbers minus one (exclude empty family).
    order = sorted(range(1, 1 << n), key=lambda m: (m.bit_count(), m))
    faces = {0}

    def recurse(i):
        if i == len(order):
            yield frozenset(faces)
            return
        mask = order[i]
        yield from recurse(i + 1)
        if all(mask ^ (1 << j) in faces
               for j in range(n) if mask >> j & 1):
            faces.add(mask)
            yield from recurse(i + 1)
            faces.remove(mask)

    yield from recurse(0)


def graph_independent_faces(n, edge_bits):
    adj = [0] * n
    t = 0
    for i in range(n):
        for j in range(i):
            if edge_bits >> t & 1:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            t += 1
    return frozenset(s for s in range(1 << n)
                     if all(not (adj[i] & s)
                            for i in range(n) if s >> i & 1))


def random_complex(n, rng):
    maximal = [sum(1 << i for i in c)
               for r in range(1, 4)
               for c in combinations(range(n), r)
               if rng.randrange(4) == 0]
    return frozenset(s for s in range(1 << n)
                     if s == 0 or any(s & ~m == 0 for m in maximal))


def main():
    stats = Counter()
    for n in range(6):
        count = 0
        for faces in all_complexes(n):
            check(faces, n, stats)
            count += 1
        assert count == [1, 2, 5, 19, 167, 7580][n]
        stats["complexes"] += count
        print(f"complexes_n{n}={count}")
    assert stats["positions"] == 122043
    assert stats["exceptions"] == 0

    for edge_bits in range(1 << 15):
        check(graph_independent_faces(6, edge_bits), 6, stats)
    stats["graphs_n6"] = 1 << 15
    assert stats["positions"] == 680939
    assert stats["exceptions"] == 60

    rng = Random(20261031)
    for _ in range(2000):
        check(random_complex(7, rng), 7, stats)
    stats["random_n7"] = 2000
    assert stats["positions"] == 748841
    assert stats["exceptions"] == 61

    # Every pair is feasible; only 012 and 345 are feasible triples.
    faces = {s for s in range(1 << 6) if s.bit_count() <= 2}
    faces |= {0b000111, 0b111000}
    check(frozenset(faces), 6, stats)
    assert rank3_formula(faces, 6, 0) == (
        (0, 0), True, (2,) * 6)
    assert stats["positions"] == 748865
    assert stats["exceptions"] == 62
    print("PASS", dict(sorted(stats.items())))


if __name__ == "__main__":
    main()
