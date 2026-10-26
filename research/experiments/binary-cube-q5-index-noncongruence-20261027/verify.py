#!/usr/bin/env python3
"""Finite independent checks; the theorem for all moduli is proved in README."""
from math import lcm

BASES = (2, 3, 5, 7)
MODULI = (2, 3, 4, 5, 8)
LIMIT = 5_000_000


def sieve(n):
    prime = bytearray(b"\x01") * (n + 1)
    prime[0:2] = b"\x00\x00"
    for d in range(2, int(n**0.5) + 1):
        if prime[d]:
            prime[d*d:n+1:d] = b"\x00" * ((n-d*d)//d+1)
    return prime


def factor(n):
    result = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            result.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        result.append(n)
    return result


def order(a, p, factors):
    k = p-1
    for q in factors:
        while k % q == 0 and pow(a, k//q, p) == 1:
            k //= q
    return k


def main():
    prime = sieve(LIMIT)
    first_yes = {m: None for m in MODULI}
    first_no = {m: None for m in MODULI}
    count = 0
    for p in range(841, LIMIT + 1, 840):
        if not prime[p]:
            continue
        count += 1
        factors = factor(p-1)
        common_period = lcm(*(order(a, p, factors) for a in BASES))
        index = (p-1)//common_period
        for m in MODULI:
            via_order = (index % m == 0)
            via_power = ((p-1) % m == 0 and
                         all(pow(a, (p-1)//m, p) == 1 for a in BASES))
            assert via_order == via_power, (p, m, index)
            if via_order and first_yes[m] is None:
                first_yes[m] = (p, index)
            if not via_order and first_no[m] is None:
                first_no[m] = (p, index)
    assert first_yes[2] == (2521, 2) and first_no[2] is None
    assert first_yes[3] == (4762801, 6) and first_no[3] == (2521, 2)
    assert first_yes[4] == (152041, 4) and first_no[4] == (2521, 2)
    assert first_yes[5] == (4082401, 10) and first_no[5] == (2521, 2)
    assert first_yes[8] == (750121, 8) and first_no[8] == (2521, 2)
    print('840 progression primes <=', LIMIT, ':', count)
    for m in MODULI:
        print('m=', m, 'first_yes=', first_yes[m], 'first_no=', first_no[m])
    print('PASS: direct m-th powers and multiplicative orders agree')


if __name__ == '__main__':
    main()
