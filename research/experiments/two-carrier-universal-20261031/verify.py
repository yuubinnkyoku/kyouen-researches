#!/usr/bin/env python3
"""Finite certificate and independent labelled-state checks for two-carrier q-point games."""
from functools import lru_cache
from itertools import product


def mex(values):
    seen = set(values)
    k = 0
    while k in seen:
        k += 1
    return k


def project(n):
    return n if n <= 5 else 4 + n % 2


def compressed(a, b, c):
    @lru_cache(None)
    def value(u, v, t):
        if min(u, v) < 0 or not 0 <= t <= c or u + a + 1 - t < 0 or v + b + 1 - t < 0:
            return None
        children = []
        if u and u + a + 1 - t > 0:
            children.append(value(u - 1, v, t))
        if v and v + b + 1 - t > 0:
            children.append(value(u, v - 1, t))
        if t and u and v:
            children.append(value(u - 1, v - 1, t - 1))
        assert all(child is not None for child in children)
        return (mex(child[0] for child in children), mex(child[1] for child in children)) if children else (0, 1)
    return value


def local_certificate():
    checks = 0
    values = set()
    for a, b, c in product(range(2), range(2), range(3)):
        f = compressed(a, b, c)
        for t, u, v in product(range(c + 1), range(8), range(8)):
            if u + a + 1 - t < 0 or v + b + 1 - t < 0:
                continue
            projected = f(project(u), project(v), t)
            children = []
            if u and u + a + 1 - t > 0:
                children.append(f(project(u - 1), project(v), t))
            if v and v + b + 1 - t > 0:
                children.append(f(project(u), project(v - 1), t))
            if t and u and v:
                children.append(f(project(u - 1), project(v - 1), t - 1))
            assert all(x is not None for x in children)
            right = (mex(x[0] for x in children), mex(x[1] for x in children)) if children else (0, 1)
            assert projected == right, (a, b, c, t, u, v, projected, right)
            values.add(projected)
            checks += 1
    print('finite_mex_identities', checks, 'possible_values', sorted(values))
    assert max(max(x) for x in values) <= 3


def independent_labelled(q, a, b, c, z):
    # All q-subsets of each carrier are forbidden. No compressed recursion here.
    A = tuple(range(q + a))
    B = tuple(range(c)) + tuple(range(q + a, q + a + q + b - c))
    n = len(A) + len(B) - c + z
    amask = sum(1 << i for i in A)
    bmask = sum(1 << i for i in B)

    @lru_cache(None)
    def rec(mask):
        children = []
        for i in range(n):
            bit = 1 << i
            if mask & bit:
                continue
            child = mask | bit
            if (child & amask).bit_count() >= q or (child & bmask).bit_count() >= q:
                continue
            children.append(rec(child))
        return (mex(x[0] for x in children), mex(x[1] for x in children)) if children else (0, 1)

    f = compressed(a, b, c)
    checked = 0
    for mask in range(1 << n):
        if (mask & amask).bit_count() >= q or (mask & bmask).bit_count() >= q:
            continue
        i = (mask & (amask & ~bmask)).bit_count()
        j = (mask & (bmask & ~amask)).bit_count()
        t = (mask & amask & bmask).bit_count()
        e = (mask & ~(amask | bmask)).bit_count()
        u, v = q - 1 - i - t, q - 1 - j - t
        expected = f(project(u), project(v), c - t)
        expected = (expected[0] ^ ((z - e) % 2), expected[1] ^ ((z - e) % 2))
        actual = rec(mask)
        assert actual == expected, (q, a, b, c, z, mask, actual, expected)
        checked += 1
    return checked


def roots():
    checks = 0
    for a, b, c, q in product(range(2), range(2), range(3), range(5, 21)):
        f = compressed(a, b, c)
        root = f(q - 1, q - 1, c)
        assert root == (c % 2, 1 - c % 2), (q, a, b, c, root)
        if q >= 6:
            expected = (1 - c % 2, c % 2)
            assert f(q - 2, q - 1, c) == expected
            assert f(q - 1, q - 2, c) == expected
            if c:
                assert f(q - 2, q - 2, c - 1) == expected
        checks += 1
    # Both lower thresholds are sharp in the abstract two-carrier game.
    assert compressed(0, 0, 2)(3, 3, 2) == (2, 2)  # q=4 root exception
    f = compressed(0, 0, 2)
    assert f(3, 4, 2) == (3, 3) and f(3, 3, 1) == (1, 0)  # q=5 unequal first-move values
    print('root_and_first_move_checks', checks, 'sharpness_q4_q5', True)


if __name__ == '__main__':
    local_certificate()
    roots()
    boards = positions = 0
    for q, a, b, c, z in product((5, 6, 7), range(2), range(2), range(3), range(2)):
        positions += independent_labelled(q, a, b, c, z)
        boards += 1
    print('independent_labelled_boards', boards, 'safe_positions', positions)
    print('PASS')
