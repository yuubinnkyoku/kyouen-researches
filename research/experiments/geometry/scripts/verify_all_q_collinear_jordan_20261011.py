#!/usr/bin/env python3
"""Exact all-q, all-dimensional collinear tuple count via Mobius inversion.

Independent verification enumerates maximal integer lines from point pairs.
Only standard-library integers are used.
"""
from __future__ import annotations
from collections import defaultdict
from itertools import product
from math import comb, factorial, gcd, prod


def mobius_upto(n: int) -> list[int]:
    mu = [1] * (n + 1)
    if n >= 0:
        mu[0] = 0
    prime = []
    composite = [False] * (n + 1)
    for i in range(2, n + 1):
        if not composite[i]:
            prime.append(i)
            mu[i] = -1
        for p in prime:
            if i * p > n:
                break
            composite[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            mu[i * p] = -mu[i]
    return mu


def collinear_mobius(sides: tuple[int, ...], q: int) -> int:
    """Number of unordered collinear q-subsets in the integer box.

    Valid for any dimension >=1, sides >=1 and q>=2.
    """
    if not sides or min(sides) < 1 or q < 2:
        raise ValueError("dimension>=1, sides>=1, q>=2 required")
    nmax = max(sides) - 1
    if q - 1 > nmax:
        return 0
    mu = mobius_upto(nmax)
    weight = [0] * (nmax + 1)
    # W_q(s) = sum_{t|s} mu(s/t) * binom(t-1,q-2).
    for t in range(q - 1, nmax + 1):
        b = comb(t - 1, q - 2)
        for g in range(1, nmax // t + 1):
            weight[t * g] += mu[g] * b
    volume = prod(sides)
    doubled = 0
    for s in range(q - 1, nmax + 1):
        if not weight[s]:
            continue
        product_sum = 1
        for n in sides:
            ell = (n - 1) // s
            product_sum *= n * (2 * ell + 1) - s * ell * (ell + 1)
        doubled += weight[s] * (product_sum - volume)
    assert doubled % 2 == 0
    return doubled // 2


def collinear_direct(sides: tuple[int, ...], q: int) -> int:
    """Independent algorithm: enumerate all maximal lines using point pairs."""
    pts = list(product(*(range(n) for n in sides)))
    ptset = set(pts)
    d = len(sides)
    lines = set()
    for i, a in enumerate(pts):
        for b in pts[i + 1:]:
            delta = tuple(y - x for x, y in zip(a, b))
            g = gcd(*delta)
            direction = tuple(x // g for x in delta)
            if next(x for x in direction if x) < 0:
                direction = tuple(-x for x in direction)
            first = a
            while tuple(first[j] - direction[j] for j in range(d)) in ptset:
                first = tuple(first[j] - direction[j] for j in range(d))
            lines.add((direction, first))
    answer = 0
    for direction, first in lines:
        length = 0
        cur = first
        while cur in ptset:
            length += 1
            cur = tuple(cur[j] + direction[j] for j in range(d))
        if length >= q:
            answer += comb(length, q)
    return answer


def jordan_totient(n: int, k: int) -> int:
    """Independent multiplicative formula for Jordan J_k, k>=1."""
    value = n**k
    p = 2
    m = n
    while p*p <= m:
        if m % p == 0:
            value = (value // p**k) * (p**k-1)
            while m % p == 0:
                m //= p
        p += 1
    if m > 1:
        value = (value // m**k) * (m**k-1)
    return value


def falling_coefficients(q: int) -> list[int]:
    """Coefficients of (x-1)...(x-(q-2)), increasing degree."""
    coefficients = [1]
    for a in range(1, q-1):
        following = [0] * (len(coefficients)+1)
        for k, v in enumerate(coefficients):
            following[k] -= a*v
            following[k+1] += v
        coefficients = following
    return coefficients


def check_jordan_weights() -> None:
    """Separate number-theoretic check of the polynomial identity."""
    mu = mobius_upto(500)
    for q in range(3, 12):
        coefficients = falling_coefficients(q)
        for s in range(2, 501):
            via_divisors = sum(
                mu[s//t]*comb(t-1, q-2)
                for t in range(q-1, s+1) if s % t == 0
            )
            via_jordan_numerator = sum(
                coefficients[k]*jordan_totient(s, k)
                for k in range(1, len(coefficients))
            )
            assert via_jordan_numerator % factorial(q-2) == 0
            via_jordan = via_jordan_numerator // factorial(q-2)
            assert via_divisors == via_jordan, (q, s, via_divisors, via_jordan)


def verify() -> None:
    count = 0
    for d in range(1, 5):
        # Exhaust all boxes with side lengths 1..4 (4D <= 256 points).
        for sides in product(range(1, 5), repeat=d):
            for q in range(2, min(max(sides) + 2, 7)):
                a = collinear_mobius(sides, q)
                b = collinear_direct(sides, q)
                assert a == b, (sides, q, a, b)
                count += 1
    # Stronger independent regression for a square and a non-cubic 3D box.
    for sides in ((5, 6), (4, 5, 3), (3, 3, 3)):
        for q in range(2, max(sides) + 2):
            assert collinear_mobius(sides, q) == collinear_direct(sides, q), (sides, q)
            count += 1
    # q=2 identity: every pair of distinct points is collinear.
    for sides in ((11, 11), (10, 7, 5), (3, 3, 3, 3, 3)):
        v = prod(sides)
        assert collinear_mobius(sides, 2) == comb(v, 2)
        count += 1
    assert collinear_mobius((11, 11), 4) == 10428
    assert collinear_mobius((11, 11), 8) == 4180
    assert collinear_mobius((3, 3, 3), 3) == 49
    assert collinear_mobius((4, 4, 4), 4) == 76
    check_jordan_weights()
    print(f"PASS: {count} independent (box,q) checks, plus 4 known exact values; 4491 Jordan checks")
    for sides, q in [((11, 11), 4), ((11, 11), 5), ((11, 11), 6), ((11, 11), 8), ((100, 100), 4), ((100, 100), 5), ((3, 3, 3), 3), ((4, 4, 4), 4)]:
        print(f"{sides}, q={q}: {collinear_mobius(sides,q)}")


if __name__ == '__main__':
    verify()
