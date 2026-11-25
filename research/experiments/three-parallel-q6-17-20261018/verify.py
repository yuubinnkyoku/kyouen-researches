#!/usr/bin/env python3
"""Exact finite certificates for 3 parallel lines, q=6, 18 candidates.

The universal reductions are mathematical and are in proof.md. This checker
only audits the finite integer cases after the reductions.
"""
from collections import Counter
from itertools import combinations
import json


def profile(a):
    return Counter(a[i] + a[j] for i, j in combinations(range(5), 2))


def H(a):
    return sum(n*n for n in profile(a).values())


def energy(a, b):
    p, q = profile(a), profile(b)
    return sum(n*q[s] for s, n in p.items())


def circles(a, b):
    # Each circle has two distinct points from each line; equal pair sums
    # are necessary and sufficient for those four points to be cocircular.
    aa = [(frozenset((i, j)), a[i]+a[j], a[i]*a[j])
          for i, j in combinations(range(5), 2)]
    bb = [(frozenset((i, j)), b[i]+b[j], b[i]*b[j])
          for i, j in combinations(range(5), 2)]
    return [(ia, ib, s, pb-pa, pa)
            for ia, s, pa in aa for ib, t, pb in bb if s == t]


def compatible(c1, c2):
    # A necessary condition for four distinct circles through the same
    # point on a third line: every pair shares exactly one base-line point.
    return len(c1[0] & c2[0]) + len(c1[1] & c2[1]) == 1


def compatible_quads(a, b):
    cc = circles(a, b)
    return [q for q in combinations(cc, 4)
            if all(compatible(x, y) for x, y in combinations(q, 2))]


def determinant(rows):
    (a, b, c), (d, e, f), (g, h, i) = rows
    return a*(e*i-f*h) - b*(d*i-f*g) + c*(d*h-e*g)


def diff_determinant(q):
    s0, delta0, p0 = q[0][2:]
    # For a circle: T - s*y + delta*u + p = 0, where
    # T=d^2*u*(u-1)+y^2. Subtract the first from the other three.
    rows = [(s0-s, delta-delta0, p0-p)
            for _, _, s, delta, p in q[1:]]
    return determinant(rows)


def main():
    # Normalize the AP with H=16 to {0,1,2,3,4}. From 9 common sums,
    # any H=14 partner is integral or half-integral in (-5/2,13/2).
    ap2 = (0, 2, 4, 6, 8)
    pools = [tuple(range(-4, 13, 2)), tuple(range(-3, 12, 2))]
    candidates = [x for pool in pools for x in combinations(pool, 5)]
    assert len(candidates) == 182
    found = [x for x in candidates if H(x) == 14 and energy(x, ap2) == 14]
    expected = [(-2, 2, 4, 6, 8), (0, 2, 4, 6, 10)]
    assert found == expected, found
    assert all(len(circles(x, ap2)) == 14 and not compatible_quads(x, ap2)
               for x in found)

    # H=16,H=16, E=14: two equal-step APs offset by half a step.
    a = (0, 2, 4, 6, 8)
    b = (1, 3, 5, 7, 9)
    assert H(a) == H(b) == 16 and energy(a, b) == 14
    q = compatible_quads(a, b)
    assert len(q) == 2
    determinants = sorted(diff_determinant(x) for x in q)
    assert determinants == [-320, 320], determinants

    # H=16,H=16, E=16: the same five-term AP on both lines.
    assert len(circles(a, a)) == 16
    assert not compatible_quads(a, a)

    # H=14,H=14, E=14: B=C (power-sum uniqueness for n=5).
    # All H=14 patterns have exactly two disjoint-pair collisions.
    # For a diagonal circle pair, the two base-line intersections total
    # 0 or 2; for two off-diagonal swapped circles, total 0.
    # Therefore any compatible family has at most one diagonal and at
    # most one of each of the two off-diagonal pairs, i.e. at most three.
    for gaps in [(1, 2, 1, 1), (1, 2, 1, 2), (1, 2, 1, 3)]:
        x = (0, gaps[0], gaps[0]+gaps[1],
             gaps[0]+gaps[1]+gaps[2], sum(gaps))
        assert H(x) == 14 and not compatible_quads(x, x)

    # Independent finite spot-audit of the universal identical-set lemma.
    identical_checks = 0
    for x in combinations(range(10), 5):
        if H(x) >= 14:
            assert not compatible_quads(x, x)
            identical_checks += 1

    result = {
        'normalization_H14_H16_candidate_sets': 182,
        'H14_H16_energy14_candidates': [list(x) for x in found],
        'H14_H16_compatible_four_circle_sets': 0,
        'H16_H16_energy14_compatible_four_circle_sets': len(q),
        'H16_H16_energy14_difference_determinants': determinants,
        'H16_H16_energy16_compatible_four_circle_sets': 0,
        'H14_H14_energy14_symbolic_proof': 'see proof.md',
        'identical_sets_H_ge_14_finite_audit': identical_checks,
        'status': 'all finite assertions passed',
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
