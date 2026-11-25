#!/usr/bin/env python3
"""Finite exact certificate for singular p=677 and p<1000 census.

The all-dimensional deductions use the exponential identity in K0561 and
p-adic lifting proved in the accompanying README, not finite extrapolation.
"""
from collections import Counter
from math import comb, factorial, isqrt

COEFF = {32: 1, 24: -30, 20: 140, 18: 135, 16: -1215,
         14: 2205, 12: -1977, 10: 780, 8: 250,
         6: -495, 4: 255, 2: -49}
P = 677
STEP = P - 1
LIMIT = 10**18
EXPECTED_SINGULAR = [(61, 13, 28), (73, 59, 13),
                     (127, 1, 0), (139, 2, 0), (677, 1, 0)]
EXPECTED_ROOTS = [0, 1, 2, 3, 4, 383]
EXPECTED_SLOPES = {0: 527, 1: 0, 2: 636, 3: 344, 4: 136, 383: 281}


def exp_mod(d, mod):
    return sum(c * pow(a, d, mod) for a, c in COEFF.items()) * pow(120, -1, mod) % mod


def stirling_mod(end, mod):
    """Independent Stirling-number recurrence; no modular exponentiation."""
    weights = [factorial(k) * sum(c * comb(a, k) for a, c in COEFF.items() if a >= k)
               % mod for k in range(33)]
    row = [1] + [0] * 32
    inv = pow(120, -1, mod)
    for _ in range(end + 1):
        yield sum(w * s for w, s in zip(weights, row)) * inv % mod
        row = [0] + [(row[k - 1] + k * row[k]) % mod for k in range(1, 33)]


def primes():
    return [p for p in range(37, 1000)
            if all(p % a for a in range(2, isqrt(p) + 1))]


def census():
    singular = []
    root_count = Counter()
    for p in primes():
        span = p - 1
        mod = p**2
        vals = list(stirling_mod(2 * span - 1, mod))
        assert all(exp_mod(d, mod) == value for d, value in enumerate(vals)), p
        roots = [j for j in range(span) if vals[j] % p == 0]
        root_count[len(roots)] += 1
        for j in roots:
            assert (vals[j + span] - vals[j]) % p == 0
            if (vals[j + span] - vals[j]) % mod == 0:
                singular.append((p, j, vals[j] // p % p))
    assert singular == EXPECTED_SINGULAR, singular
    assert root_count == Counter({5: 55, 6: 47, 7: 35, 8: 14, 9: 2, 10: 4}), root_count
    print('157 primes 32<p<1000: singular', singular)
    print('root counts:', sorted(root_count.items()))


def lift_simple(j, slope, last_t):
    k = 0
    roots = {1: 0}
    for t in range(1, last_t):
        mod = P**(t + 1)
        f = exp_mod(j + STEP * k, mod)
        assert f % P**t == 0
        digit = -(f // P**t) * pow(slope, -1, P) % P
        k += P**(t - 1) * digit
        assert exp_mod(j + STEP * k, mod) == 0
        roots[t + 1] = k
    return roots


def lift_singular(k, last_t):
    roots = {3: k}
    for t in range(3, last_t):
        mod = P**(t + 1)
        f = exp_mod(1 + STEP * k, mod)
        assert f % P**t == 0
        derivative = 468 * (2 * k - 327) % P
        assert derivative
        digit = -(f // P**t) * pow(derivative, -1, P) % P
        k += P**(t - 2) * digit
        assert exp_mod(1 + STEP * k, mod) == 0
        roots[t + 1] = k
    return roots


def progression(j, k, step):
    first = j + STEP * k
    if first < 5:
        first += step
    if first > LIMIT:
        return None
    return first, step, 1 + (LIMIT - first) // step


def main():
    census()
    mod = P**3
    vals = list(stirling_mod(2 * STEP + 4, mod))
    assert all(exp_mod(d, mod) == v for d, v in enumerate(vals))
    roots = [j for j in range(STEP) if vals[j] % P == 0]
    assert roots == EXPECTED_ROOTS
    slopes = {j: ((vals[j + STEP] - vals[j]) // P) % P for j in roots}
    assert slopes == EXPECTED_SLOPES
    assert all({(j + h) % STEP for j in roots} != set(roots)
               for h in range(1, STEP))
    a = ((vals[1 + STEP] - vals[1]) // P**2) % P
    b = ((vals[1 + 2 * STEP] - 2 * vals[1 + STEP] + vals[1]) // P**2) % P
    assert (a, b) == (434, 259)
    assert all(exp_mod(1 + STEP * k, mod) == P**2 * (468 * k * (k - 327) % P)
               for k in range(P))
    assert all(exp_mod(1 + STEP * k, P**2) == 0 for k in range(P))
    simple = {j: lift_simple(j, slopes[j], 10) for j in roots if j != 1}
    singular = [lift_singular(0, 10), lift_singular(327, 10)]
    assert simple[383][2] == 86
    assert [r[4] for r in singular] == [0, 372677]

    def rows(t):
        result = []
        for j, lifts in simple.items():
            if (r := progression(j, lifts[t], STEP * P**(t - 1))) is not None:
                result.append(('simple', j, *r))
        if t >= 3:
            for i, lifts in enumerate(singular):
                if (r := progression(1, lifts[t], STEP * P**(t - 2))) is not None:
                    result.append((f'singular{i}', 1, *r))
        return result

    at7 = rows(7)
    assert at7 == [
        ('singular0', 1, 96136883502038133, 96136883502038132, 10),
        ('singular1', 1, 40599894136591609, 96136883502038132, 10)]
    assert not rows(8)
    for _, _, first, step, count in at7:
        assert first + step * (count - 1) <= LIMIT < first + step * count
        assert exp_mod(first, P**7) == 0
        assert exp_mod(first, P**8) != 0
    print('p=677 roots:', roots, 'slopes:', slopes)
    print('H(k)=468*k*(k-327) mod 677; 2 simple singular branches')
    print('v_677 maximum on [5,10^18] = 7, 20 maximizers:')
    print(*at7, sep='\n')
    print('PASS: census, two independent modular algorithms, 677-adic lifts')


if __name__ == '__main__':
    main()
