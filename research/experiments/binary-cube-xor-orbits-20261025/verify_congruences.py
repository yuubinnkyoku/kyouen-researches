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



def verify_six_point_mod81_sylow3():
    """Exact q=6 Sylow-3 fixed-set census and 3-adic classes through 3^4."""
    from fractions import Fraction
    from math import comb, factorial

    def row_action(x, permutation):
        bits = [0] + [(x >> i) & 1 for i in range(5)]
        return sum((bits[permutation[i]] ^ bits[permutation[0]]) << (i - 1)
                   for i in range(1, 6))

    identity = tuple(range(32))
    cycle_a = tuple(row_action(x, (1, 2, 0, 3, 4, 5)) for x in range(32))
    cycle_b = tuple(row_action(x, (0, 1, 2, 4, 5, 3)) for x in range(32))

    def compose(a, b):
        return tuple(a[b[x]] for x in range(32))

    def power(g, n):
        value = identity
        for _ in range(n):
            value = compose(value, g)
        return value

    group = {compose(power(cycle_a, i), power(cycle_b, j))
             for i in range(3) for j in range(3)}
    assert len(group) == 9
    subgroup_generators = (cycle_a, cycle_b,
                           compose(cycle_a, cycle_b),
                           compose(cycle_a, power(cycle_b, 2)))
    subgroups = [{identity, g, compose(g, g)} for g in subgroup_generators]
    assert all(len(h) == 3 for h in subgroups)
    assert len({frozenset(h) for h in subgroups}) == 4

    def orbits(h):
        seen, answer = set(), []
        for x in range(32):
            if x not in seen:
                orbit = tuple(sorted({g[x] for g in h}))
                seen.update(orbit)
                answer.append(orbit)
        return answer

    def admissible(columns, rational=False):
        k = len(columns)
        a = [[Fraction((col >> i) & 1) if rational else (col >> i) & 1
              for col in columns] for i in range(5)]
        row_masks = [sum(((col >> i) & 1) << j
                         for j, col in enumerate(columns)) for i in range(5)]
        if 0 in row_masks or len(set(row_masks)) != 5:
            return False
        rank = 0
        for j in range(k):
            if rank == 5:
                break
            pivot = next((i for i in range(rank, 5) if a[i][j]), None)
            if pivot is None:
                continue
            a[rank], a[pivot] = a[pivot], a[rank]
            scale = (1 / a[rank][j] if rational else pow(a[rank][j], -1, 1009))
            a[rank] = [v * scale if rational else v * scale % 1009
                       for v in a[rank]]
            for i in range(5):
                if i != rank and a[i][j]:
                    f = a[i][j]
                    a[i] = [a[i][z] - f * a[rank][z] if rational else
                            (a[i][z] - f * a[rank][z]) % 1009
                            for z in range(k)]
            rank += 1
        found = 0
        for mask in range(1 << rank):
            if all((sum(a[i][j] for i in range(rank) if mask >> i & 1)
                    if rational else
                    sum(a[i][j] for i in range(rank) if mask >> i & 1) % 1009)
                   in (0, 1) for j in range(k)):
                found += 1
                if found > 6:
                    return False
        return found == 6

    fixed = []
    checked = []
    for subgroup in subgroups + [group]:
        orbit_list = orbits(subgroup)
        totals, valid = [0] * 15, [0] * 15

        def visit(i, columns):
            k = len(columns)
            if k > 14:
                return
            if i == len(orbit_list):
                if 4 <= k <= 14:
                    totals[k] += 1
                    is_valid = admissible(columns)
                    if 10 <= k <= 14:
                        assert is_valid == admissible(columns, rational=True)
                    valid[k] += is_valid
                return
            visit(i + 1, columns)
            visit(i + 1, columns + orbit_list[i])

        visit(0, ())
        fixed.append(valid)
        checked.append(totals)
    assert [checked[i][10] for i in range(5)] == [2472, 2472, 240, 240, 12]
    assert [checked[i][11] for i in range(5)] == [3144, 3144, 120, 120, 6]
    assert [fixed[i][10:15] for i in range(5)] == [
        [1059, 1615, 2357, 3188, 3849],
        [1059, 1615, 2357, 3188, 3849],
        [147, 82, 185, 383, 198],
        [147, 82, 185, 383, 198],
        [9, 4, 5, 14, 9],
    ]

    h_known = {4: 75, 5: 75, 6: 2877, 7: 44437,
               8: 480895, 9: 3220820}
    h = {k: (sum(fixed[i][k] for i in range(4)) - 3 * fixed[4][k]) % 9
         for k in range(4, 15)}
    assert all(h[k] == h_known[k] % 9 for k in h_known)
    assert [h[k] for k in range(10, 15)] == [0, 7, 2, 8, 3]
    h.update(h_known)

    def via_inclusion(d, modulus):
        return sum(h[k] * sum((-1) ** (k - j) * comb(k, j) *
                              pow(j, d, modulus) for j in range(k + 1))
                   for k in h if factorial(k) % modulus) % modulus

    def via_stirling(d, modulus):
        row = [1] + [0] * 14
        for _ in range(d):
            row = [0] + [(row[k - 1] + k * row[k]) % modulus
                         for k in range(1, 15)]
        return sum(h[k] * factorial(k) * row[k] for k in h) % modulus

    def section_residue(d, modulus):
        a = via_inclusion(d, 9 * modulus)
        assert a == via_stirling(d, 9 * modulus)
        assert a % 9 == 0
        return (pow(2, d, modulus) * (a // 9) *
                pow(80, -1, modulus)) % modulus

    # 3^6 divides 15!, so the unknown h[k>=15] disappear modulo 729.
    # Euler's theorem proves a period 486 for E mod81 for all d>=6.
    vals = {m: [section_residue(d, m) for d in range(6, 6 + 2 * 486)]
            for m in (27, 81)}
    exact = {6: 206528, 7: 47884928, 8: 9324142464,
             9: 1405033324800}
    for m in (27, 81):
        assert all(vals[m][d - 6] == v % m for d, v in exact.items())
        period = 54 if m == 27 else 162
        assert all(vals[m][i] == vals[m][i + period] for i in range(486))
        # All proper divisors of 54 divide 18 or 27;
        # all proper divisors of 162 divide 54 or 81.
        forbidden = (18, 27) if m == 27 else (54, 81)
        assert all(vals[m][0] != vals[m][j] for j in forbidden)
        roots = sorted(d % period for d in range(6, 6 + period)
                       if vals[m][d - 6] == 0)
        assert roots == ([35, 38, 39] if m == 27 else [93, 143, 146])
    assert (vals[27][4], vals[27][5]) == (16, 6)
    assert (vals[81][4], vals[81][5]) == (43, 6)
    print('q=6 Sylow-3: h[10..14] mod9 = (0,7,2,8,3)')
    print('q=6: least periods mod27=54, mod81=162')
    print('q=6: v3(E)>=4 iff d mod162 in {93,143,146}, d>=6')



def verify_six_point_mod25_sylow5():
    """C5 fixed-set census for q=6 mod25, with rational/modular checks."""
    from fractions import Fraction
    from itertools import combinations
    from math import comb, factorial

    permutation = (1, 2, 3, 4, 0, 5)

    def action(x):
        bits = [0] + [(x >> i) & 1 for i in range(5)]
        return sum((bits[permutation[i]] ^ bits[permutation[0]]) << (i - 1)
                   for i in range(1, 6))

    orbits, seen = [], set()
    for x in range(32):
        if x in seen:
            continue
        orbit, y = [], x
        while y not in orbit:
            orbit.append(y)
            y = action(y)
        assert y == x
        orbits.append(tuple(orbit))
        seen.update(orbit)
    assert sorted(map(len, orbits)) == [1, 1, 5, 5, 5, 5, 5, 5]

    def valid(columns, prime=None):
        k = len(columns)
        rows = [[Fraction((col >> i) & 1) if prime is None
                 else (col >> i) & 1 for col in columns] for i in range(5)]
        rank = 0
        for j in range(k):
            pivot = next((i for i in range(rank, 5) if rows[i][j]), None)
            if pivot is None:
                continue
            rows[rank], rows[pivot] = rows[pivot], rows[rank]
            inv = 1 / rows[rank][j] if prime is None else pow(rows[rank][j], -1, prime)
            rows[rank] = [v * inv if prime is None else v * inv % prime
                          for v in rows[rank]]
            for i in range(5):
                if i != rank and rows[i][j]:
                    factor = rows[i][j]
                    rows[i] = [rows[i][z] - factor * rows[rank][z]
                               if prime is None else
                               (rows[i][z] - factor * rows[rank][z]) % prime
                               for z in range(k)]
            rank += 1
            if rank == 5:
                break
        if rank != 5:
            return False
        return sum(all((sum(rows[i][j] for i in range(5) if mask >> i & 1)
                        if prime is None else
                        sum(rows[i][j] for i in range(5) if mask >> i & 1) % prime)
                       in (0, 1) for j in range(k)) for mask in range(32)) == 6

    fixed = {k: 0 for k in range(4, 15)}
    checked = {k: 0 for k in range(4, 15)}
    for n in range(len(orbits) + 1):
        for chosen in combinations(orbits, n):
            columns = tuple(x for orbit in chosen for x in orbit)
            k = len(columns)
            if k not in fixed:
                continue
            checked[k] += 1
            exact = valid(columns)
            assert exact == valid(columns, prime=1009)
            fixed[k] += exact
    assert {k: v for k, v in checked.items() if v} == {
        5: 6, 6: 12, 7: 6, 10: 15, 11: 30, 12: 15}
    assert {k: v for k, v in fixed.items() if v} == {
        6: 2, 7: 2, 10: 7, 11: 20, 12: 13}

    known = {4: 75, 5: 75, 6: 2877, 7: 44437,
             8: 480895, 9: 3220820}
    assert all(fixed[k] % 5 == v % 5 for k, v in known.items())
    h = dict(known)
    h.update({k: fixed[k] % 5 for k in range(10, 15)})

    def via_stirling(d):
        row = [1] + [0] * 14
        for _ in range(d):
            row = [0] + [(row[k - 1] + k * row[k]) % 125
                         for k in range(1, 15)]
        return sum(v * factorial(k) * row[k] for k, v in h.items()) % 125

    def via_inclusion(d):
        return sum(v * sum((-1) ** (k - j) * comb(k, j) * pow(j, d, 125)
                           for j in range(k + 1)) for k, v in h.items()) % 125

    def residue(d):
        a = via_stirling(d)
        assert a == via_inclusion(d)
        assert a % 5 == 0
        return pow(2, d, 25) * (a // 5) * pow(144, -1, 25) % 25

    # 5^3 divides 15!: all unknown h[k>=15] vanish modulo 125.
    # Euler's theorem proves period 100 for E mod25 at all d>=6.
    assert factorial(15) % 125 == 0
    for j in range(15):
        if j % 5:
            assert pow(j, 100, 125) == 1
        else:
            assert pow(j, 6, 125) == 0
    values = [residue(d) for d in range(6, 206)]
    assert all(values[i] == values[i + 100] for i in range(100))
    # Every proper divisor of 100 divides 50 or 20.
    assert values[0] != residue(56) and values[0] != residue(26)
    roots = sorted(d % 100 for d in range(6, 106) if residue(d) == 0)
    assert roots == [2, 3, 5, 9, 25, 29, 45, 49, 64, 65, 69, 85, 89]
    for d, exact in {6: 206528, 7: 47884928, 8: 9324142464,
                     9: 1405033324800}.items():
        assert residue(d) == exact % 25
    assert (residue(10), residue(11)) == (21, 11)
    print('q=6 Sylow-5: fixed[10..14] = (7,20,13,0,0)')
    print('q=6: least period mod25=100; 13 zero classes; E10=21,E11=11 mod25')



def verify_five_point_three_adic():
    """Exact checks of theorem 11; proof for all t is in proof.md.

    Compare modular pow with a sequential recurrence and the original
    unnormalized exact formula. The two modular algorithms share only
    K0561's independently established coefficients.
    """
    half = {a // 2: c for a, c in C5.items()}
    roots_known = {
        2: (2, 3, 4, 5),
        3: (2, 3, 4, 5),
        4: (2, 4, 5, 39),
        5: (4, 93, 110, 113),
        6: (113, 328, 417, 434),
    }

    def normalized_mod(d, modulus):
        assert d >= 5
        m = 120 * modulus
        numerator = sum(c * pow(a, d, m) for a, c in half.items()) % m
        assert numerator % 120 == 0
        return numerator // 120

    def via_recurrence(modulus, limit):
        m = 120 * modulus
        powers = {a: 1 for a in half}
        values = []
        for d in range(limit):
            numerator = sum(c * powers[a] for a, c in half.items()) % m
            if d >= 5:
                assert numerator % 120 == 0
                values.append(numerator // 120)
            else:
                values.append(None)
            for a in powers:
                powers[a] = powers[a] * a % m
        return values

    known = {5: 2592, 6: 256704, 7: 18778368,
             8: 1133185536, 9: 58832008704, 10: 2724496524288}
    for d in range(5, 26):
        e = exact(C5, 120, d)
        assert e % (1 << d) == 0
        assert e // (1 << d) == sum(c * a**d for a, c in half.items()) // 120
        if d in known:
            assert e == known[d]

    lambdas = {a: ((a**6 - 1) // 9) % 9 for a in half if a % 3}
    assert lambdas == {16: 1, 10: 6, 8: 3, 7: 4,
                       5: 8, 4: 5, 2: 7, 1: 0}
    slope_numerators = tuple(
        sum(c * pow(a, r, 9) * lambdas[a]
            for a, c in half.items() if a % 3) % 9 for r in range(6))
    assert slope_numerators == (0, 0, 6, 6, 3, 3)
    assert all(normalized_mod(d, 3) == 0 for d in range(5, 30))

    for t in range(2, 8):
        modulus, period = 3**t, 2 * 3**(t - 1)
        start = max(5, t + 2)
        values = via_recurrence(3**(t + 1), start + 3 * period + 5)
        for d in range(start, start + 2 * period):
            assert values[d] == normalized_mod(d, 3**(t + 1))
            assert (values[d + period] - values[d]) % modulus == 0
            eps = (0, 0, 2, 2, 1, 1)[d % 6]
            assert (values[d + period] - values[d]) % (3**(t + 1)) == (
                3**t * eps) % (3**(t + 1))
        roots = tuple(sorted(d % period for d in range(start, start + period)
                             if values[d] % modulus == 0))
        assert len(roots) == 4
        if t in roots_known:
            assert roots == roots_known[t], (t, roots)
            for d in range(5, start):
                assert (normalized_mod(d, modulus) == 0) == (d % period in roots)
        # Maximal proper divisors cannot be periods.
        d0 = next(d for d in range(start, start + 6) if d % 6 == 0)
        assert normalized_mod(d0, modulus) != normalized_mod(
            d0 + period // 2, modulus)
        if t == 2:
            assert normalized_mod(d0, modulus) != normalized_mod(
                d0 + period // 3, modulus)
        else:
            d2 = next(d for d in range(start, start + 6) if d % 6 == 2)
            assert normalized_mod(d2, modulus) != normalized_mod(
                d2 + period // 3, modulus)
    print('q=5: exact 3-adic periods and four lifting branches verified to t=7')


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
    verify_five_point_three_adic()
    verify_six_point_sharpness_period()
    verify_six_point_mod32()
    verify_six_point_odd_prime_periods()
    verify_six_point_mod81_sylow3()
    verify_six_point_mod25_sylow5()
    print("K0567: exact checks and q=6 parity-period bases passed (d<=64)")


if __name__ == "__main__":
    main()
