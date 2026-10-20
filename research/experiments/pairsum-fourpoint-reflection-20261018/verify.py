#!/usr/bin/env python3
"""Exact rational reconstruction audit for four-element pair-sum multisets."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement
import json


def pair_sums(xs):
    return tuple(sorted(xs[i] + xs[j] for i in range(4) for j in range(i + 1, 4)))


def reconstruct(sums):
    """Return all real four-multisets compatible with a valid six-pair-sum input."""
    total = sum(sums, Fraction(0)) / 3
    remaining = Counter(Fraction(s) - total / 2 for s in sums)
    abc = []
    while remaining:
        a = min(remaining)
        assert remaining[a] > 0 and remaining[-a] > 0
        remaining[a] -= 1
        if remaining[a] == 0:
            del remaining[a]
        remaining[-a] -= 1
        if remaining[-a] == 0:
            del remaining[-a]
        abc.append(a)
    assert len(abc) == 3
    a, b, c = abc
    z = ((a+b+c)/2, (a-b-c)/2, (-a+b-c)/2, (-a-b+c)/2)
    x = tuple(sorted(v + total / 4 for v in z))
    y = tuple(sorted(total / 2 - v for v in x))
    assert pair_sums(x) == tuple(sorted(sums))
    assert pair_sums(y) == tuple(sorted(sums))
    return {x, y}


def run():
    checks = []
    for mode, points in [
        ("distinct", combinations(range(-8, 9), 4)),
        ("with_repetitions", combinations_with_replacement(range(-5, 8), 4)),
    ]:
        count = one = two = odd_total = 0
        for xs in points:
            xs = tuple(Fraction(x) for x in xs)
            result = reconstruct(pair_sums(xs))
            assert xs in result
            assert len(result) in (1, 2)
            is_symmetric = tuple(sorted(sum(xs)/2-x for x in xs)) == xs
            assert (len(result) == 1) == is_symmetric
            if sum(xs).denominator == 1 and sum(xs).numerator % 2:
                assert len([ys for ys in result if all(y.denominator == 1 for y in ys)]) == 1
                odd_total += 1
            one += len(result) == 1
            two += len(result) == 2
            count += 1
        checks.append(dict(mode=mode, checked=count, one_real_preimage=one,
                           two_real_preimages=two, odd_total=odd_total))
    a = (Fraction(0), Fraction(3), Fraction(15), Fraction(16))
    b = (Fraction(1), Fraction(2), Fraction(14), Fraction(17))
    assert reconstruct(pair_sums(a)) == {a, b}
    print(json.dumps({"method": "rational_reconstruction", "checks": checks,
                      "witness": [list(map(int, a)), list(map(int, b))]}, ensure_ascii=False))

if __name__ == "__main__":
    run()
