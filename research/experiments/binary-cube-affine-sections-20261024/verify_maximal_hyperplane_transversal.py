"""Exhaustive transversal audit for all maximal hypercube hyperplanes.

A flat is represented by the bit mask of its vertices.  For d<=7,
all (t-1)-point candidate transversals are checked, where t=1+bit_length(d).
"""
from itertools import combinations


def flats(d):
    n = 1 << d
    out = []
    for i in range(d):
        for b in (0, 1):
            out.append(sum(1 << x for x in range(n) if ((x >> i) & 1) == b))
    for i, j in combinations(range(d), 2):
        for b in (0, 1):
            out.append(sum(1 << x for x in range(n)
                           if (((x >> i) ^ (x >> j)) & 1) == b))
    assert len(set(out)) == d * (d + 1)
    assert all(m.bit_count() == n // 2 for m in out)
    return out


def witness(d):
    t = 1 + d.bit_length()
    return [0] + [sum(1 << j for j in range(d) if (j + 1) >> b & 1)
                  for b in range(t - 1)]


def check(d, exhaustive):
    family = flats(d)
    t = 1 + d.bit_length()
    chosen = witness(d)
    assert len(chosen) == len(set(chosen)) == t
    mask = sum(1 << x for x in chosen)
    assert all(mask & f for f in family)
    count = 0
    if exhaustive:
        # A smaller hitting set could be enlarged to t-1 points.
        for subset in combinations(range(1 << d), t - 1):
            candidate = sum(1 << x for x in subset)
            assert any((candidate & f) == 0 for f in family), (d, subset)
            count += 1
    print(f"d={d} flats={len(family)} t={t} K={2**d-t} "
          f"excluded_smaller={count} witness={chosen}")


if __name__ == "__main__":
    for dimension in range(1, 13):
        check(dimension, dimension <= 7)
