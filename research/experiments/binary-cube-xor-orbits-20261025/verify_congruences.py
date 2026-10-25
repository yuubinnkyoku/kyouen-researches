#!/usr/bin/env python3
"""Exact arithmetic checks of K0567, independent of the rooted rank verifier."""

C3 = {8: 1, 6: -3, 4: 3, 2: -1}
C4 = {16: 1, 12: -12, 10: 30, 8: -35, 6: 27, 4: -16, 2: 5}
C5 = {32: 1, 24: -30, 20: 140, 18: 135, 16: -1215,
      14: 2205, 12: -1977, 10: 780, 8: 250,
      6: -495, 4: 255, 2: -49}


def exact(coefficients, denominator, d):
    numerator = sum(coefficient * base**d
                    for base, coefficient in coefficients.items())
    assert numerator % denominator == 0
    return numerator // denominator


def v2(x):
    assert x > 0
    return (x & -x).bit_length() - 1



def rank_mod_101(rows, dimension):
    """Row rank over F_101; exact for 0/1 cube differences in d<=5."""
    matrix = [[x % 101 for x in row] for row in rows]
    rank = 0
    for column in range(dimension):
        pivot = next((i for i in range(rank, len(matrix))
                      if matrix[i][column] != 0), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][column], -1, 101)
        for j in range(column, dimension):
            matrix[rank][j] = matrix[rank][j] * inv % 101
        for i in range(rank + 1, len(matrix)):
            factor = matrix[i][column]
            if factor:
                for j in range(column, dimension):
                    matrix[i][j] = (matrix[i][j] - factor * matrix[rank][j]) % 101
        rank += 1
        if rank == len(matrix):
            break
    return rank


def count_four_sections_direct(d):
    """Exhaustive geometric test, independent of the E4 closed formula."""
    from itertools import combinations

    vertices = [tuple((i >> j) & 1 for j in range(d))
                for i in range(1 << d)]
    count = 0
    for indices in combinations(range(1 << d), 4):
        origin = vertices[indices[0]]
        directions = [
            tuple(vertices[x][j] - origin[j] for j in range(d))
            for x in indices[1:]
        ]
        rank = rank_mod_101(directions, d)
        if rank == d:
            continue
        if all(rank_mod_101(
            directions + [tuple(vertices[x][j] - origin[j]
                                for j in range(d))], d) > rank
               for x in range(1 << d) if x not in indices):
            count += 1
    return count



def verify_six_point_sharpness_period():
    """Independent Stirling reconstruction from K0565's exact support counts.

    The finite test is *not* the proof of the infinite periodicity:
    that follows from the integer exponential representation modulo 16.
    """
    from math import factorial

    support = {4: 75, 5: 75, 6: 2877, 7: 44437,
               8: 480895, 9: 3220820}
    expected = {6: 206528, 7: 47884928,
                8: 9324142464, 9: 1405033324800}
    stirling = [[0] * 10 for _ in range(10)]
    stirling[0][0] = 1
    for d in range(1, 10):
        for k in range(1, d + 1):
            stirling[d][k] = stirling[d - 1][k - 1] + k * stirling[d - 1][k]
    for d in range(6, 10):
        a = sum(h * factorial(k) * stirling[d][k]
                for k, h in support.items() if k <= d)
        assert a % 360 == 0
        assert ((1 << d) * a) % 720 == 0
        e = (1 << d) * a // 720
        assert e == expected[d]
        assert a % 16 == (8 if d % 4 in (0, 1) else 0)
        assert (e // (1 << (d - 1))) % 2 == (d % 4 in (0, 1))

    # Every possible exponential base in the q=6 rooted formula:
    # a congruence on four residues, not an extrapolation from d<=64.
    for base in range(33):
        for d in range(4, 8):
            assert (pow(base, d + 4, 16) - pow(base, d, 16)) % 16 == 0




def verify_six_point_mod32():
    """Prove-checkable q=6 mod-32 pattern, with two independent arithmetic routes.

    Full generality follows from 10! divisible by 256 and
    (j**4-1)**2 divisible by 256 for odd j, not from the d<=512 loop.
    """
    from math import comb, factorial

    support = {4: 75, 5: 75, 6: 2877, 7: 44437,
               8: 480895, 9: 3220820}
    exact_known = {6: 206528, 7: 47884928,
                   8: 9324142464, 9: 1405033324800}

    def via_stirling(d):
        values = [1] + [0] * 9
        for _ in range(d):
            following = [0] * 10
            for k in range(1, 10):
                following[k] = (values[k - 1] + k * values[k]) % 256
            values = following
        return sum(h * factorial(k) * values[k]
                   for k, h in support.items()) % 256

    def via_inclusion_exclusion(d):
        return sum(h * sum((-1) ** (k - j) * comb(k, j)
                           * pow(j, d, 256) for j in range(k + 1))
                   for k, h in support.items()) % 256

    # Even bases vanish for d>=8. Odd bases have square-zero 4th-power
    # increments mod 256, yielding exact affine dependence on floor(d/4).
    assert factorial(10) % 256 == 0
    for j in range(10):
        if j % 2:
            assert (pow(j, 4, 256) - 1) % 16 == 0
        else:
            assert pow(j, 8, 256) == 0

    for d in range(6, 513):
        a = via_stirling(d)
        assert a == via_inclusion_exclusion(d), d
        if d in exact_known:
            assert a == (720 * exact_known[d] // (1 << d)) % 256, d
        if d < 8:
            continue
        n, r = divmod(d, 4)
        expected_a = [144 * n + 120, 112 * n - 120,
                      16 * (n - 2), -16 * (n - 2)][r] % 256
        assert a == expected_a, d
        assert a % 8 == 0
        b = (5 * (a // 8)) % 32  # inverse of 45 modulo 32
        expected_b = [26 * n + 11, 6 * n + 21,
                      10 * (n - 2), -10 * (n - 2)][r] % 32
        assert b == expected_b, d
        if r in (2, 3):
            if (n - 2) % 16:
                assert v2(b) == 1 + v2(abs(n - 2)), d
            else:
                assert b == 0, d



def verify_five_point_lifting():
    """Modular recurrence and independent power checks for the all-t q=5 lemma.

    The infinite theorem is proved by LTE, not by this finite audit.
    """
    coefficients = {base // 2: coefficient for base, coefficient in C5.items()}
    expected_roots = {
        1: (0, 3), 2: (3, 4), 3: (3, 12), 4: (12, 19),
        5: (19, 44), 6: (19, 108), 7: (147, 236),
        8: (147, 492), 9: (492, 659), 10: (492, 1683),
    }

    def via_powers(d, t):
        modulus = 1 << (t + 3)
        numerator = sum(c * pow(b, d, modulus)
                        for b, c in coefficients.items()) % modulus
        assert numerator % 8 == 0
        return (numerator // 8 * pow(15, -1, 1 << t)) % (1 << t)

    for t, expected in expected_roots.items():
        period = 1 << (t + 1)
        start = max(5, t + 4)
        modulus = 1 << (t + 3)
        inv15 = pow(15, -1, 1 << t)
        powers = {base: 1 for base in coefficients}
        residues = []
        for d in range(start + 2 * period):
            numerator = sum(c * powers[b] for b, c in coefficients.items()) % modulus
            residues.append((numerator // 8 * inv15) % (1 << t)
                            if d >= 5 else None)
            if d >= 5:
                assert numerator % 8 == 0
            for b in powers:
                powers[b] = powers[b] * b % modulus
        for d in range(start, start + 2 * period):
            assert residues[d] == via_powers(d, t)
        assert all(residues[d] == residues[d + period]
                   for d in range(start, start + period))
        assert residues[start] != residues[start + period // 2]
        roots = sorted(d % period for d in range(start, start + period)
                       if residues[d] == 0)
        assert roots == list(expected), (t, roots)

    for k in range(2, 12):
        t = k + 3
        for d in list(range(k + 3, k + 20)) + [100, 1000]:
            if d < k + 3:
                continue
            diff = (via_powers(d + (1 << k), t) - via_powers(d, t)) % (1 << t)
            assert diff and v2(diff) == k - 1, (k, d)

    for d in range(5, 81):
        value = exact(C5, 120, d)
        assert value % (1 << d) == 0
        for t in range(1, 11):
            assert (value >> d) % (1 << t) == via_powers(d, t)



def verify_six_point_odd_prime_periods():
    """All-d odd-prime congruences for six-point cube sections.

    The all-d argument uses Euler periods modulo p^(t+v_p(720))
    and the factorial cutoff; the finite residue check only shortens
    the proven periods. Stirling and inclusion-exclusion are independent
    arithmetic reconstructions from the same certified h_{6,k}.
    """
    from math import comb, factorial

    support = {4: 75, 5: 75, 6: 2877, 7: 44437,
               8: 480895, 9: 3220820}
    exact_known = {6: 206528, 7: 47884928,
                   8: 9324142464, 9: 1405033324800}

    def via_stirling(d, modulus):
        row = [1] + [0] * 9
        for _ in range(d):
            row = [0] + [(row[k - 1] + k * row[k]) % modulus
                         for k in range(1, 10)]
        return sum(h * factorial(k) * row[k]
                   for k, h in support.items()
                   if factorial(k) % modulus) % modulus

    def via_inclusion(d, modulus):
        return sum(
            h * sum((-1) ** (k - j) * comb(k, j)
                    * pow(j, d, modulus) for j in range(k + 1))
            for k, h in support.items()
            if factorial(k) % modulus
        ) % modulus

    # (p, exponent, claimed least period, Euler period, residues d=6,...)
    cases = [
        (3, 1, 6, 18, [2, 2, 0, 0, 1, 0]),
        (3, 2, 18, 54,
         [5, 5, 3, 6, 7, 6, 8, 5, 6, 3, 1, 0,
          2, 5, 0, 0, 4, 3]),
        (5, 1, 20, 20,
         [3, 3, 4, 0, 1, 1, 3, 0, 4, 4, 2, 0,
          2, 2, 1, 0, 0, 0, 0, 0]),
    ]
    for p, t, period, euler_period, expected in cases:
        v = 2 if p == 3 else 1  # v_p(6!)
        modulus = p ** (v + t)
        residue_modulus = p ** t
        cutoff = 8 if p == 3 else 9
        assert factorial(cutoff + 1) % modulus == 0
        assert period <= euler_period and euler_period % period == 0

        # Establish the all-d Euler period for A_d modulo p^(v+t).
        for base in range(cutoff + 1):
            if base % p:
                assert pow(base, euler_period, modulus) == 1
            else:
                assert pow(base, 6, modulus) == 0

        def section_residue(d):
            a = via_inclusion(d, modulus)
            assert a % (p ** v) == 0
            return (pow(2, d, residue_modulus) *
                    (a // (p ** v)) *
                    pow(720 // (p ** v), -1, residue_modulus)
                    ) % residue_modulus

        # One full Euler period is enough to prove the shorter period.
        for d in range(6, 6 + euler_period):
            assert section_residue(d + period) == section_residue(d)
        residues = [section_residue(d) for d in range(6, 6 + period)]
        assert residues == expected, (p, t, residues)
        for candidate in range(1, period):
            if period % candidate == 0:
                assert any(residues[i] != residues[(i + candidate) % period]
                           for i in range(period))

        for d in range(6, 201):
            assert via_stirling(d, modulus) == via_inclusion(d, modulus)
            assert section_residue(d + period) == section_residue(d)
            if d in exact_known:
                assert section_residue(d) == exact_known[d] % residue_modulus


def main():
    for d in range(3, 65):
        value = exact(C3, 6, d)
        assert v2(value) == d + (d % 2 == 0)
    for d in range(3, 65):
        value = exact(C4, 24, d)
        assert v2(value) == d - (1 if d % 2 else 2)
        assert v2(exact({4: 1, 2: -1}, 2, d)) == d - 1
    for d in range(3, 6):
        assert count_four_sections_direct(d) == exact(C4, 24, d)
    for d in range(5, 65):
        value = exact(C5, 120, d)
        assert value % (1 << d) == 0
        assert (value // (1 << d)) % 2 == (d % 4 in (1, 2))
    assert exact(C3, 6, 3) == 8
    assert exact(C3, 6, 4) == 160
    assert exact(C5, 120, 5) == 2592
    assert exact(C5, 120, 6) == 256704
    # Existing exact finite counts, illustrating the even-q orbit bound.
    for d, q, count in [(4, 6, 40), (5, 6, 1200), (4, 8, 20)]:
        assert count % (1 << max(0, d - v2(q))) == 0
    verify_five_point_lifting()
    verify_six_point_sharpness_period()
    verify_six_point_mod32()
    verify_six_point_odd_prime_periods()
    print("K0567: exact checks and q=6 parity-period bases passed (d<=64)")


if __name__ == "__main__":
    main()
