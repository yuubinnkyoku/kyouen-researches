#!/usr/bin/env python3
"""Independent finite audits of the 4-residue sieve used in a 4-row 8-circle slope bound.

This checks finite inequalities, not the large-sieve theorem or its analytic asymptotic.
"""
import json
from fractions import Fraction
from math import gcd, isqrt


def primes_3mod4(n):
    sieve = bytearray(b'\x01') * (n + 1)
    sieve[:2] = b'\x00\x00'
    for d in range(2, isqrt(n) + 1):
        if sieve[d]:
            sieve[d * d::d] = b'\x00' * ((n - d * d) // d + 1)
    return [p for p in range(7, n + 1) if sieve[p] and p % 4 == 3]


def weight(p):
    return Fraction(4, p - 4)


def sieve_G(Q, B=None):
    """G_B(Q) = sum_{q<=Q,(q,B)=1} mu(q)^2 prod_{p|q} 4/(p-4)."""
    values = [Fraction(0)] * (Q + 1)
    values[1] = Fraction(1)
    for p in primes_3mod4(Q):
        if B is not None and B % p == 0:
            continue
        for n in range(Q // p, 0, -1):
            if values[n]:
                values[n * p] += values[n] * weight(p)
    return sum(values)


def factor_F(B):
    result = Fraction(1)
    for p in primes_3mod4(B):
        if B % p == 0:
            result *= 1 + weight(p)
    return result


def locally_admissible(A, B, primes):
    return all(A % p not in {B * k % p for k in (-3, -1, 1, 3)}
               for p in primes if B % p != 0)


def four_factors_ok(A, B, primes):
    return all(n % p for p in primes
               for n in (A - B, A + B, A - 3 * B, A + 3 * B))


def audit(H):
    Q = isqrt(H)
    ps = primes_3mod4(Q)
    primitive = local_survivors = 0
    max_ratio = Fraction(0)
    base_G = sieve_G(Q)
    for B in range(1, H + 1):
        gb = sieve_G(Q, B)
        assert base_G <= factor_F(B) * gb, ('multiplicative bound', H, B)
        local_count = sum(locally_admissible(A, B, ps) for A in range(1, H + 1))
        # Classical one-dimensional large sieve bound; numerically audit its inequality.
        assert local_count * gb <= H + Q * Q, ('large sieve', H, B)
        max_ratio = max(max_ratio, Fraction(local_count) * gb / (H + Q * Q))
        for A in range(3 * B + 1, H + 1):
            if gcd(A, B) != 1:
                continue
            primitive += 1
            x = locally_admissible(A, B, ps)
            assert x == four_factors_ok(A, B, ps), ('factorization', A, B)
            local_survivors += x
    return {'H': H, 'Q': Q, 'primitive_candidates': primitive,
            'survivors_mod_primes_at_most_Q': local_survivors,
            'G_Q': str(base_G), 'max_sieve_ratio': round(float(max_ratio), 8)}


def main():
    for p in (7, 11, 19, 23, 31):
        for B in range(1, p):
            assert len({B * k % p for k in (-3, -1, 1, 3)}) == 4
    # Known nonlocal slope 9/1 is not excluded by any local obstruction.
    assert four_factors_ok(9, 1, primes_3mod4(1000))
    for a,b,c,d in ((35,51,63,73),(1331,1935,2391,2773)):
        assert a*a-2*b*b+c*c == -8 == b*b-2*c*c+d*d
        s,v=(a+d)//2,(c-b)//2
        g0=gcd(s,v)
        A,B=s//g0,v//g0
        g=gcd(A,3)
        L=g0
        M=((d-a)//2)*g//(3*B)
        assert (d-a)//2 == 3*B*M//g
        assert (b+c)//2 == A*M//g
        P=A*A-B*B
        Q=(A*A-9*B*B)//(g*g)
        assert Q*M*M-P*L*L == 8
    result = {'status': 'PASS', 'finite_audits': [audit(H) for H in (80, 160, 320, 640)],
              'scope': 'finite checks only; analytic large sieve and asymptotic require proofs'}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
