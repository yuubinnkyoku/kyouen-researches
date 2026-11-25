#!/usr/bin/env python3
"""Exact independent integer-determinant audit of 3-row chord enclosure bounds.

Run: python research/experiments/geometry/scripts/verify_enclosed_chord_bound.py
"""
from itertools import permutations


def determinant_4x4(rows):
    total = 0
    for perm in permutations(range(4)):
        inversions = sum(perm[i] > perm[j] for i in range(4) for j in range(i+1, 4))
        product = 1
        for i in range(4):
            product *= rows[i][perm[i]]
        total += (-1 if inversions % 2 else 1) * product
    return total


def circle_det(d, p, q, u, v):
    # Laplace expansion along (0,0)'s row, then explicit 3x3 determinant.
    a, b, c = d*d, d, 0
    e, f, g = u*u+p*p, u, -p
    h, i, j = v*v+q*q, v, q
    return a*(f*j-g*i)-b*(e*j-g*h)+c*(e*i-f*h)


def lifted(x, y):
    return (x*x+y*y, x, y, 1)


def run():
    checks = 0
    hits = 0
    full_det_checks = 0
    strict_hits = 0
    observed_max = {}
    for p in range(1, 7):
        for q in range(1, 7):
            max_bound = 1 + (p+q)*max(p,q)
            strict_bound = 1 + p*q
            observed_max[p,q] = 0
            for d in range(1, max_bound+6):
                for u in range(d+1):
                    for v in range(d+1):
                        checks += 1
                        det = circle_det(d,p,q,u,v)
                        condition = q*u*(d-u)+p*v*(d-v)-p*q*(p+q)
                        assert (det == 0) == (condition == 0)
                        # Explicit independent 4x4 Leibniz determinant on a deterministic sample
                        # and every actual hit, without relying on the reduced expression.
                        if condition == 0 or checks % 199 == 0:
                            full_det_checks += 1
                            rows = [lifted(0,0), lifted(d,0), lifted(u,-p), lifted(v,q)]
                            assert determinant_4x4(rows) == -det
                        if det == 0:
                            hits += 1
                            observed_max[p,q] = max(observed_max[p,q],d)
                            assert d <= max_bound, (p,q,d,u,v)
                            if 0 < u < d and 0 < v < d:
                                strict_hits += 1
                                assert d <= strict_bound, (p,q,d,u,v)
            # Bound is sharp, independently checked with explicit witness.
            if q >= p:
                d,u,v = max_bound,0,1
            else:
                d,u,v = max_bound,1,0
            assert circle_det(d,p,q,u,v) == 0
            assert observed_max[p,q] == max_bound
            # Strict enclosure bound is also sharp.
            d = strict_bound
            assert circle_det(d,p,q,1,1) == 0
    print('parameter_pairs=36 (1<=p,q<=6)')
    print(f'enclosed_candidates={checks}')
    print(f'cocircular_hits={hits}')
    print(f'strictly_enclosed_hits={strict_hits}')
    print(f'independent_full_4x4_determinant_checks={full_det_checks}')
    print('maximum_chord_length_for_each_pair=1+(p+q)*max(p,q): ALL MATCH')
    print('strictly_inside_bound=1+p*q: ALL MATCH')
    for p,q in [(1,1),(1,2),(2,2),(1,3),(3,4),(6,6)]:
        print(f'p={p},q={q}: max_d={observed_max[p,q]}, strict_max_d={1+p*q}')


if __name__ == '__main__':
    run()
