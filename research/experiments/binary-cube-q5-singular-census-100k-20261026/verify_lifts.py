#!/usr/bin/env python3
"""Exact p-adic branch and finite-range audit; no geometric census claim."""
from math import comb, factorial

COEFF = {32: 1, 24: -30, 20: 140, 18: 135, 16: -1215, 14: 2205,
         12: -1977, 10: 780, 8: 250, 6: -495, 4: 255, 2: -49}
LIMIT = 10**18
EXPECTED = {
    1021: (5, {2: ((0, 347, 693), (0, 607))}, 1020, 6, 1804),
    6691: (5, {2: ((0, 824, 916), (0, 3184))}, 6690, 5, 998),
    18311: (10, {2: ((0, 11537, 8638), (0, 4327)),
                 9157: ((111, 15856, 8638), (9155, 13482))}, 9155, 5, 35),
    26947: (7, {2: ((0, 20999, 8575), (0, 22729))}, 26946, 5, 3),
}


def exp_mod(d, mod):
    return sum(c * pow(a, d, mod) for a, c in COEFF.items()) * pow(120, -1, mod) % mod


def stirling_mod(d, mod):
    """Independent binomial/Stirling evaluation, valid for p>32."""
    bases = [pow(i, d, mod) for i in range(33)]
    answer = 0
    for k in range(33):
        stir = sum((-1)**(k-i) * comb(k, i) * bases[i] for i in range(k+1))
        stir = stir * pow(factorial(k), -1, mod) % mod
        weight = factorial(k) * sum(c * comb(a, k) for a, c in COEFF.items() if a >= k)
        answer += weight * stir
    return answer * pow(120, -1, mod) % mod


def prime_factors(n):
    ans = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            ans.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        ans.append(n)
    return ans


def roots_and_slopes(p):
    period = p-1
    a = list(COEFF)
    powers = [1]*len(a)
    roots = []
    for j in range(period):
        if sum(COEFF[x]*powers[i] for i, x in enumerate(a)) % p == 0:
            roots.append(j)
        powers = [powers[i]*x % p for i, x in enumerate(a)]
    slopes = {j: ((exp_mod(j+period, p*p)-exp_mod(j, p*p)) % (p*p))//p
              for j in roots}
    return roots, slopes


def singular_polynomial(p, j):
    period = p-1
    vals = [exp_mod(j+period*k, p**3)//(p*p) for k in range(3)]
    assert all(exp_mod(j+period*k, p*p) == 0 for k in range(3))
    c, a, b = vals[0] % p, (vals[1]-vals[0]) % p, (vals[2]-2*vals[1]+vals[0]) % p
    inv2 = pow(2, -1, p)
    h = lambda k: (c + a*k + b*k*(k-1)*inv2) % p
    derivative = lambda k: (a + b*(2*k-1)*inv2) % p
    roots = tuple(k for k in range(p) if h(k) == 0)
    for k in (0, 1, 2, 3, 5, 17, p-1):
        assert exp_mod(j+period*k, p**3)//(p*p) % p == h(k)
    assert all(derivative(k) for k in roots)
    return (c, a, b), roots, derivative


def progression(p, j, k, step):
    first = j+(p-1)*k
    if first < 5:
        first += step
    if first > LIMIT:
        return None
    return (first, step, 1+(LIMIT-first)//step)


def verify_prime(p):
    nroots, singular_expected, least, max_v, max_count = EXPECTED[p]
    roots, slopes = roots_and_slopes(p)
    singular = [j for j in roots if not slopes[j]]
    assert len(roots) == nroots and set(singular) == set(singular_expected)
    polynomials = {}
    for j in singular:
        coeff, r, deriv = singular_polynomial(p, j)
        assert (coeff, r) == singular_expected[j]
        polynomials[j] = (r, deriv)
    order = p-1
    for q in prime_factors(p-1):
        while order % q == 0 and all(pow(a, order//q, p) == 1 for a in COEFF):
            order //= q
    assert order == least
    assert any(pow(a, order, p*p) != 1 for a in COEFF)
    simple = {j: 0 for j in roots if j not in singular}
    branches = {(j, r): r for j in singular for r in polynomials[j][0]}
    t = 1
    while t <= max_v+1:
        progressions = []
        for j, k in simple.items():
            v = progression(p, j, k, (p-1)*p**(t-1))
            if v:
                progressions.append(('simple', j, *v))
        for j in singular:
            if t <= 2:
                v = progression(p, j, 0, p-1)
                if v:
                    progressions.append(('singular', j, *v))
            else:
                for (j0, r), k in branches.items():
                    if j0 == j:
                        v = progression(p, j, k, (p-1)*p**(t-2))
                        if v:
                            progressions.append(('singular', j, *v))
        if t == max_v:
            assert sum(row[-1] for row in progressions) == max_count
            for kind, j, first, step, count in progressions:
                for d in (first, first+step*(count-1)):
                    assert exp_mod(d, p**t) == stirling_mod(d, p**t) == 0
                    assert exp_mod(d, p**(t+1)) == stirling_mod(d, p**(t+1)) != 0
            print(f'p={p}: max v={t}, {max_count} dimensions, progressions={progressions}')
        if t == max_v+1:
            assert not progressions
            break
        for j, k in list(simple.items()):
            mod = p**(t+1)
            value = exp_mod(j+(p-1)*k, mod)
            assert value % p**t == 0
            digit = -(value//p**t)*pow(slopes[j], -1, p) % p
            simple[j] = k + digit*p**(t-1)
            assert exp_mod(j+(p-1)*simple[j], mod) == 0
        if t >= 3:
            for key, k in list(branches.items()):
                j = key[0]
                mod = p**(t+1)
                value = exp_mod(j+(p-1)*k, mod)
                assert value % p**t == 0
                digit = -(value//p**t)*pow(polynomials[j][1](k), -1, p) % p
                branches[key] = k + digit*p**(t-2)
                assert exp_mod(j+(p-1)*branches[key], mod) == 0
        t += 1
    for d in (5, 6, 7, 8, 11, 37, p-1, p+1, 10**12+12345, LIMIT):
        assert exp_mod(d, p**3) == stirling_mod(d, p**3)
    print(f'p={p}: roots={roots}, least period p^t: {least}*p^(t-1), PASS')


if __name__ == '__main__':
    for prime in EXPECTED:
        verify_prime(prime)
    print('PASS: exact lifts, full [5,10^18] maxima, independent Stirling arithmetic')
