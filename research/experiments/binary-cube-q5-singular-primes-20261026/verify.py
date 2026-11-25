#!/usr/bin/env python3
"""Exact certificate for q=5 p=127,139 singular p-adic branches.

Uses K0561's proved exponential formula. Checks its arithmetic by an
independent Stirling-number recurrence. No geometric enumeration is claimed.
"""
from math import comb, factorial

COEFF = {32: 1, 24: -30, 20: 140, 18: 135, 16: -1215,
         14: 2205, 12: -1977, 10: 780, 8: 250,
         6: -495, 4: 255, 2: -49}
DATA = {
    127: {'roots': [0, 1, 2, 3, 4], 'singular': 1,
          'quadratic_coefficient': 112, 'second_root': 7},
    139: {'roots': [0, 1, 2, 3, 4, 27], 'singular': 2,
          'quadratic_coefficient': 104, 'second_root': 36},
}
LIMIT = 10**18


def exp_mod(d, mod):
    return (sum(c * pow(a, d, mod) for a, c in COEFF.items())
            * pow(120, -1, mod)) % mod


def stirling_mod(end, mod):
    weights = [sum(c * comb(a, k) for a, c in COEFF.items() if a >= k)
               * factorial(k) % mod for k in range(33)]
    row = [1] + [0] * 32
    inv = pow(120, -1, mod)
    for _ in range(end + 1):
        yield sum(weights[k] * row[k] for k in range(33)) * inv % mod
        row = [0] + [(row[k-1] + k * row[k]) % mod
                     for k in range(1, 33)]


def simple_lift(p, j, slope, last_t):
    """Return k mod p^(t-1) at each t for a simple zero."""
    k, roots = 0, {1: 0}
    for t in range(1, last_t):
        v = exp_mod(j + (p-1)*k, p**(t+1))
        assert v % p**t == 0
        k += p**(t-1) * (-(v//p**t) * pow(slope, -1, p) % p)
        assert exp_mod(j + (p-1)*k, p**(t+1)) == 0
        roots[t+1] = k
    return roots


def singular_lift(p, j, c, r, last_t):
    """Two k mod p^(t-2) roots for t>=3, via Hensel on E/p^2."""
    roots = {3: [0, r]}
    for t in range(3, last_t):
        nxt = []
        for k in roots[t]:
            v = exp_mod(j+(p-1)*k, p**(t+1))
            assert v % p**t == 0
            slope = c*(2*(k % p)-r) % p
            assert slope
            k += p**(t-2) * (-(v//p**t)*pow(slope, -1, p) % p)
            assert exp_mod(j+(p-1)*k, p**(t+1)) == 0
            nxt.append(k)
        assert nxt[0] == 0
        assert nxt[0] != nxt[1]
        roots[t+1] = nxt
    return roots


def count_progressions(p, simple, singular, t):
    P = p-1
    rows = []
    for j, lifts in simple.items():
        period = P*p**(t-1)
        start = j+P*lifts[t]
        if start < 5:
            start += period
        if start <= LIMIT:
            rows.append((j, start, period, 1+(LIMIT-start)//period))
    if t == 1:
        period = P
        roots = [0]
    elif t == 2:
        period = P
        roots = [0]  # every k; already reduced modulo p-1
    else:
        period = P*p**(t-2)
        roots = singular[t]
    j = DATA[p]['singular']
    for k in roots:
        start = j+P*k
        if start < 5:
            start += period
        if start <= LIMIT:
            rows.append((j, start, period, 1+(LIMIT-start)//period))
    return rows


def main():
    for p, expected in DATA.items():
        P, mod = p-1, p**3
        vals = list(stirling_mod(2*P+4, mod))
        assert all(v == exp_mod(d, mod) for d, v in enumerate(vals))
        assert all(vals[j] == 0 for j in range(5))
        roots = [j for j in range(P) if vals[j] % p == 0]
        assert roots == expected['roots'], (p, roots)
        slopes = {j: ((vals[j+P]-vals[j]) % p**2)//p
                  for j in range(P)}
        singular = expected['singular']
        assert [j for j in roots if slopes[j] == 0] == [singular]
        assert sum(c*a**singular for a,c in COEFF.items()) == 0
        assert vals[singular] == 0
        assert vals[singular+P] % p**2 == 0
        assert vals[singular+2*P] % p**2 == 0
        c, r = expected['quadratic_coefficient'], expected['second_root']
        # E(j+Pk)/p^2 mod p = c*k*(k-r), by binomial expansion.
        assert [(vals[singular+P*k]//p**2) % p for k in (0,1,2)] == [
            c*k*(k-r) % p for k in (0,1,2)]
        # Direct binomial coefficients in (1+p*u_a)^k, not interpolation.
        u = {a: (pow(a,P)-1)//p for a in COEFF}
        b1 = sum(c0*pow(a,singular)*u[a] for a,c0 in COEFF.items())//120
        b2 = sum(c0*pow(a,singular)*u[a]**2 for a,c0 in COEFF.items())//120
        assert b1 % p == 0
        assert b1//p % p == c*(1-r) % p
        assert b2 % p == 2*c % p
        assert [k for k in range(p) if exp_mod(singular+P*k, mod) == 0] == [0, r]
        assert all({(j+h)%P for j in roots} != set(roots) for h in range(1,P))
        last_t = 13
        simple = {j: simple_lift(p,j,slopes[j],last_t)
                  for j in roots if j != singular}
        special = singular_lift(p,singular,c,r,last_t)
        assert all(all(k == 0 for k in simple[j].values())
                   for j in simple if j <= 4)
        # Directly inspect all k modulo p at the p^2 stage.
        for j in range(P):
            for k in range(p):
                predicted = (j == singular or
                             (j in simple and k == simple[j][2]))
                assert (exp_mod(j+P*k,p**2) == 0) == predicted
        counts = {t: count_progressions(p,simple,special,t)
                  for t in range(1,last_t+1)}
        max_t = max(t for t, rows in counts.items() if rows)
        assert max_t < last_t and not counts[max_t+1]
        assert all(counts[t] for t in range(1,max_t+1))
        print('p=',p,'roots mod p=',roots,'singular j=',singular)
        print('singular polynomial mod p:',c,'* k * (k-',r,')')
        print('simple slopes:',{j:slopes[j] for j in simple})
        print('singular lifts t=3..6:',{t:special[t] for t in range(3,7)})
        print('max v_p on 5<=d<=1e18:',max_t)
        print('maximizers as progressions (j, first, period, count):',counts[max_t])
        print('maximizer count:',sum(row[3] for row in counts[max_t]))
    print('PASS: exact modular checks and two arithmetic routes')


if __name__ == '__main__':
    main()
