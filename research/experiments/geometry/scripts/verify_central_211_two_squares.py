#!/usr/bin/env python3
"""Independent integer verification of the middle-chord three-row theorem.

The theorem itself is proved in reports/central-211-two-squares-density-20261011.md.
This program is a finite audit, not a proof of the density statement.
"""
import json
from itertools import permutations
from math import isqrt
from pathlib import Path


def two_square_pairs(n):
    if n < 0:
        return set()
    out = set()
    for a in range(-isqrt(n), isqrt(n) + 1):
        b2 = n - a * a
        b = isqrt(b2)
        if b * b == b2:
            out.add((a, b))
            out.add((a, -b))
    return out


def completions(d, h):
    """Gaussian-integer construction (not used by determinant oracle)."""
    out = set()
    for a, b in two_square_pairs(d*d - 4*h*h):
        assert (d+a+b) % 2 == 0 and (d+a-b) % 2 == 0
        out.add(((d+a+b)//2, (d+a-b)//2))
    return out


PERMS = tuple((p, (-1)**sum(p[i] > p[j] for i in range(4) for j in range(i+1,4)))
              for p in permutations(range(4)))


def determinant4(points):
    rows = [[x, y, x*x + y*y, 1] for x, y in points]
    return sum(sign * rows[0][p[0]] * rows[1][p[1]] *
               rows[2][p[2]] * rows[3][p[3]] for p, sign in PERMS)


def factorization(n):
    out = {}
    p = 2
    while p*p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            out[p] = e
        p += 1 if p == 2 else 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def r2_divisor_formula(n):
    if n < 0:
        return 0
    if n == 0:
        return 1
    f = factorization(n)
    if any(p % 4 == 3 and e % 2 for p, e in f.items()):
        return 0
    z = 4
    for p, e in f.items():
        if p % 4 == 1:
            z *= e + 1
    return z


def run():
    direct_cases = 0
    direct_candidate_points = 0
    direct_solutions = 0
    for h in range(1, 7):
        for d in range(1, 25):
            predicted = completions(d, h)
            direct = set()
            # From |2u-d| <= sqrt(2d^2-8h^2) < sqrt(2)d,
            # any possible u,v lies in [-d,2d].
            for u in range(-d, 2*d+1):
                for v in range(-d, 2*d+1):
                    direct_candidate_points += 1
                    if determinant4(((0, 0), (d, 0), (u, -h), (v, h))) == 0:
                        direct.add((u, v))
            assert predicted == direct, (d, h, predicted ^ direct)
            direct_cases += 1
            direct_solutions += len(direct)

    factor_cases = 0
    for h in range(1, 13):
        for d in range(1, 301):
            expected = r2_divisor_formula(d*d - 4*h*h)
            actual = len(two_square_pairs(d*d - 4*h*h))
            assert actual == expected, (d, h, actual, expected)
            factor_cases += 1

    density_counts = {}
    for h in (1, 2, 3):
        tally = 0
        density_counts[str(h)] = {}
        for d in range(1, 5001):
            tally += r2_divisor_formula(d*d - 4*h*h) > 0
            if d in (100, 1000, 5000):
                density_counts[str(h)][str(d)] = tally

    pell_cases = 0
    k, t = 1, 0
    for _ in range(25):
        for h in range(1, 11):
            d = 2*h*k
            a = b = 2*h*t
            assert a*a + b*b == d*d - 4*h*h
            u, v = (d+a+b)//2, (d+a-b)//2
            assert determinant4(((0, 0), (d, 0), (u, -h), (v, h))) == 0
            pell_cases += 1
        k, t = 3*k+4*t, 2*k+3*t

    result = {
        'direct_determinant_cases': direct_cases,
        'direct_determinant_candidate_pairs': direct_candidate_points,
        'direct_determinant_solutions': direct_solutions,
        'two_square_divisor_formula_cases': factor_cases,
        'pell_witness_cases': pell_cases,
        'admissible_d_counts': density_counts,
        'status': 'PASS',
        'scope': 'finite audits only; unbounded claims use the report proof',
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


if __name__ == '__main__':
    run()
