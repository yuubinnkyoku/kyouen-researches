#!/usr/bin/env python3
"""Exact O(2^k)-state polynomial DP for marked-hub selection probabilities."""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb
from pathlib import Path
from random import Random
import runpy

ONE = {(0, 0): F(1)}


def plus(a, b, sign=1):
    z = defaultdict(F, a)
    for key, value in b.items():
        z[key] += sign * value
    return {key: value for key, value in z.items() if value}


def times(a, b):
    z = defaultdict(F)
    for (p, q), x in a.items():
        for (r, s), y in b.items():
            z[(p + r, q + s)] += x * y
    return {key: value for key, value in z.items() if value}


def integrate_y_to_x(a):
    z = defaultdict(F)
    for (p, q), value in a.items():
        z[(p + q + 1, 0)] += value / (q + 1)
        z[(p, q + 1)] -= value / (q + 1)
    return {key: value for key, value in z.items() if value}


@lru_cache(None)
def power(w, axis):
    return {((i, 0) if axis == 0 else (0, i)): F((-1)**i * comb(w, i))
            for i in range(w + 1)}


def probability(t, neighborhoods, h):
    m = len(t)
    target = set(neighborhoods[h])
    others = [set(a) for i, a in enumerate(neighborhoods) if i != h]
    k = len(others)
    f = []
    for count in t:
        w = count + 1
        f.append({key: val / w for key, val in plus(
            power(w, 1), {key: count * val for key, val in power(w, 0).items()}
        ).items()})
    covered = [target]
    for mask in range(1, 1 << k):
        bit = mask & -mask
        covered.append(covered[mask ^ bit] | others[bit.bit_length() - 1])
    dp = [ONE] + [{} for _ in range((1 << k) - 1)]
    for mask in range(1, 1 << k):
        bits = mask
        while bits:
            bit = bits & -bits
            bits ^= bit
            i = bit.bit_length() - 1
            prev = mask ^ bit
            factor = ONE
            for j in others[i] - covered[prev]:
                factor = times(factor, f[j])
            dp[mask] = plus(dp[mask], integrate_y_to_x(times(dp[prev], factor)), -1)
    answer = F()
    for mask, polynomial in enumerate(dp):
        term = {(p, 0): value for (p, q), value in polynomial.items() if q == 0}
        for j in range(m):
            if j in target:
                term = times(term, power(t[j] + 1, 0))
            elif j not in covered[mask]:
                term = times(term, {(p, 0): value for (p, q), value in f[j].items() if q == 0})
        answer += sum((value / (p + 1) for (p, q), value in term.items()), F())
    return answer


def check():
    old = runpy.run_path(str(Path(__file__).resolve().parents[1] /
                             'split-marked-hub-terminal-law-20261030' / 'verify.py'))
    direct = old['direct_distribution']
    permutations = old['permutation_distribution']
    factorial_formula = old['marked_hub_probability']
    tested = 0
    checked_permutations = 0
    for m in range(1, 4):
        choices = [frozenset(j for j in range(m) if mask >> j & 1)
                   for mask in range(1 << m)]
        for k in range(1, 4):
            for t in product(range(2), repeat=m):
                if m + sum(t) + k > 8:
                    continue
                for neighborhoods in product(choices, repeat=k):
                    expected = direct(t, neighborhoods)
                    found = tuple(probability(t, neighborhoods, h) for h in range(k))
                    assert found == expected[1:], (t, neighborhoods, found, expected)
                    tested += 1
                    if tested % 11 == 0 and checked_permutations < 100 and m + sum(t) + k <= 6:
                        assert permutations(t, neighborhoods) == expected
                        checked_permutations += 1
    t = (1, 2, 0)
    neighborhoods = (frozenset((0, 1)), frozenset((1, 2)), frozenset((0, 2)))
    assert tuple(probability(t, neighborhoods, h) for h in range(3)) == (F(7, 54), F(2, 15), F(5, 36))
    rng = Random(20261030)
    for _ in range(120):
        t = tuple(rng.randrange(3) for _ in range(4))
        neighborhoods = tuple(frozenset(j for j in range(4) if rng.randrange(2)) for _ in range(4))
        assert tuple(probability(t, neighborhoods, h) for h in range(4)) == direct(t, neighborhoods)[1:]
    for _ in range(80):
        t = tuple(rng.randrange(3) for _ in range(4))
        neighborhoods = tuple(frozenset(j for j in range(4) if rng.randrange(2)) for _ in range(4))
        assert probability(t, neighborhoods, 0) == factorial_formula(t, neighborhoods, 0)
    print('exhaustive:', tested, 'priority permutations:', checked_permutations)
    print('random m=4,k=4: 120; independent factorial formula: 80')
    print('example:', [str(probability((1, 2, 0), (
        frozenset((0, 1)), frozenset((1, 2)), frozenset((0, 2))), h)) for h in range(3)])


if __name__ == '__main__':
    check()
