#!/usr/bin/env python3
"""Exact finite algebra audit for the three-parallel-line q=6 bound 19.

Only the standard library is used.  All concurrency computations are rational.
The universal reduction and its proof are in proof.md.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import gcd
import json


def pair_profile(points):
    return Counter(x + y for x, y in combinations(points, 2))


def cross_energy(a, b):
    pa, pb = pair_profile(a), pair_profile(b)
    return sum(n * pb[s] for s, n in pa.items())


def normalized(row):
    g = gcd(*row)
    if g == 0:
        return (0, 0, 0)
    result = tuple(x // g for x in row)
    if next(x for x in result if x) < 0:
        result = tuple(-x for x in result)
    return result


def audit_ap_concurrency():
    # B=C={0,1,2,3,4}.  Each matched chord pair yields a circle.
    # (s,delta,p) = (b1+b2, c1*c2-b1*b2, b1*b2).
    chords = list(combinations(range(5), 2))
    triples = sorted((sum(b), c[0] * c[1] - b[0] * b[1], b[0] * b[1])
                     for b in chords for c in chords if sum(b) == sum(c))
    assert len(triples) == 16 and len(set(triples)) == 16
    counts = Counter()
    rank_one_cases = []
    for ids in combinations(range(16), 4):
        s0, delta0, p0 = triples[ids[0]]
        rows = [(-(triples[j][0] - s0), triples[j][1] - delta0,
                 triples[j][2] - p0) for j in ids[1:]]
        # Each row is A*a+B*u+C=0, with u=(x_A-x_B)/(x_C-x_B).
        nonzero = [normalized(r) for r in rows if r != (0, 0, 0)]
        assert nonzero
        if len(set(nonzero)) == 1:
            # Four circle equations differ only by the condition a=k.
            A, B, C = nonzero[0]
            assert A == 1 and B == 0 and C in (0, -1, -2, -3, -4)
            k = -C
            assert all(delta == 0 and p == k * (s - k)
                       for s, delta, p in (triples[j] for j in ids))
            # Substituting a=k leaves d^2*u*(u-1)=0, impossible
            # because d>0 and the three lines are distinct.
            counts['rank_one_only_u_zero_or_one'] += 1
            rank_one_cases.append({'ids': list(ids), 'a': k})
            continue
        solved = False
        for i, j in combinations(range(3), 2):
            A, B, C = rows[i]
            D, E, F = rows[j]
            det = A * E - B * D
            if not det:
                continue
            a = Fraction(-C * E + B * F, det)
            u = Fraction(-A * F + C * D, det)
            if not all(A * a + B * u + C == 0 for A, B, C in rows):
                counts['inconsistent'] += 1
            elif u in (0, 1):
                counts['rank_two_u_zero_or_one'] += 1
            else:
                # Circle equation is d^2*u*(u-1)+a^2-s*a+delta*u+p=0.
                d_squared = -(a*a-s0*a+delta0*u+p0) / (u*(u-1))
                assert d_squared <= 0, (ids, a, u, d_squared)
                counts['rank_two_d_squared_negative' if d_squared < 0
                       else 'rank_two_d_squared_zero'] += 1
            solved = True
            break
        if not solved:
            counts['inconsistent_parallel'] += 1
    assert sum(counts.values()) == 1820
    assert counts == {
        'inconsistent': 1318,
        'inconsistent_parallel': 210,
        'rank_two_u_zero_or_one': 226,
        'rank_two_d_squared_negative': 37,
        'rank_two_d_squared_zero': 24,
        'rank_one_only_u_zero_or_one': 5,
    }, counts
    return counts, rank_one_cases


def audit_finite_energy():
    samples = list(combinations(range(10), 5))
    ap = lambda x: len({x[i+1]-x[i] for i in range(4)}) == 1
    hist = Counter()
    for a in samples:
        for b in samples:
            e = cross_energy(a, b)
            assert e <= 16
            assert e != 15
            if e == 16:
                assert a == b and ap(a)
            if not (a == b and ap(a)):
                assert e <= 14
            hist[e] += 1
    assert hist[16] == 8
    return len(samples) ** 2, hist


def main():
    counts, rank_one = audit_ap_concurrency()
    n, hist = audit_finite_energy()
    result = {
        'classification': 'exact symbolic finite reduction (1820 4-tuples)',
        'circle_candidates': 16,
        'four_circle_subsets': 1820,
        'concurrency_categories': dict(sorted(counts.items())),
        'rank_one_cases': rank_one,
        'finite_energy_pairs': n,
        'finite_energy_histogram': {str(k): v for k, v in sorted(hist.items())},
        'finite_energy_e15': hist[15],
        'finite_energy_e16': hist[16],
        'assertions_passed': True,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
