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
    verify_six_point_sharpness_period()
    verify_six_point_mod32()
    print("K0567: exact checks and q=6 parity-period bases passed (d<=64)")


if __name__ == "__main__":
    main()
