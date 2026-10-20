#!/usr/bin/env python3
"""Independent finite audit of the 4-row 8-point circle inert-prime obstruction.

The theorem's infinite quantifiers are proved in the accompanying report,
not by this finite computation. No external packages.
"""
from math import gcd, isqrt


def is_two_squares(n):
    """Independent exhaustive sum-of-two-squares test."""
    for x in range(isqrt(n) + 1):
        y2 = n - x * x
        if isqrt(y2) ** 2 == y2:
            return True
    return False


def no_inert_prime(n):
    """Trial factorization, independent of is_two_squares."""
    assert n > 0
    p = 2
    while p * p <= n:
        if n % p == 0:
            if p % 4 == 3:
                return False
            while n % p == 0:
                n //= p
        p += 1 if p == 2 else 2
    return n == 1 or n % 4 != 3


def candidate(A, B):
    if A <= 3 * B or gcd(A, B) != 1:
        return False
    g = gcd(A, 3)
    P = A * A - B * B
    Q = (A * A - 9 * B * B) // (g * g)
    return no_inert_prime(P) and no_inert_prime(Q)


def slope_of_chords(a, b, c, d):
    s, v = (a + d) // 2, (c - b) // 2
    k = gcd(s, v)
    return s // k, v // k


def check_direct_chords(BMAX):
    found = []
    for a in range(1, BMAX + 1, 2):
        for b in range(a + 2, BMAX + 1, 2):
            c2 = 2 * b * b - a * a - 8
            if c2 <= b * b:
                continue
            c = isqrt(c2)
            if c * c != c2 or c % 2 != 1:
                continue
            d2 = 3 * b * b - 2 * a * a - 24
            if d2 <= c * c:
                continue
            d = isqrt(d2)
            if d * d != d2 or d % 2 != 1:
                continue
            A, B = slope_of_chords(a, b, c, d)
            g = gcd(A, 3)
            P, Q = A*A-B*B, (A*A-9*B*B)//(g*g)
            assert candidate(A, B), (a, b, c, d, A, B)
            assert all(is_two_squares(x) for x in (A-B, A+B, (A-3*B)//g, (A+3*B)//g))
            found.append((a, b, c, d, A, B))
    return found


def main():
    # Check the one-way implication to sums of two squares for every n in a finite range.
    for n in range(1, 1001):
        assert not no_inert_prime(n) or is_two_squares(n), n
    for H in (100, 200, 400):
        primitive = survivors = 0
        for B in range(1, H + 1):
            for A in range(3*B + 1, H + 1):
                if gcd(A, B) == 1:
                    primitive += 1
                    survivors += candidate(A, B)
        print(f'H={H}: primitive={primitive}, necessary-condition-survivors={survivors}')
    circles = check_direct_chords(3000)
    print(f'direct nonlocal chord patterns (a,b<=3000): {len(circles)}')
    for row in circles:
        print('  chords/slope:', *row)
    print('PASS: trial-factor and direct-square checks; all enumerated chord patterns')


if __name__ == '__main__':
    main()
