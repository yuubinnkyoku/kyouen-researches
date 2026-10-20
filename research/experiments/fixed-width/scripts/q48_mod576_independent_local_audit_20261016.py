#!/usr/bin/env python3
"""Separate arithmetic audit: factorization and modular norm solubility.

This does not prove the unbounded large-sieve asymptotic.
"""
from math import gcd, isqrt


def has_inert_factor(n):
    assert n > 0
    d=2
    while d*d <= n:
        if n%d==0:
            if d%4==3:
                return True
            while n%d==0:
                n//=d
        d+=1
    return n>1 and n%4==3


def norm_soluble_mod64(P,Q):
    squares={k*k%64 for k in range(64)}
    q={Q*s%64 for s in squares}
    return any((8+P*t)%64 in q for t in squares)


def main():
    # Check the stronger four-class conclusion independently by factoring P,Q
    # and brute-forcing all square residues of the Pell norm modulo 64.
    total=0
    checked=0
    bad=0
    for B in range(1,101,2):
        for A in range(3*B+1,501):
            if gcd(A,B)!=1:
                continue
            g=gcd(A,3)
            P=A*A-B*B
            Q=(A*A-9*B*B)//(g*g)
            total+=1
            if has_inert_factor(P) or has_inert_factor(Q):
                continue
            checked+=1
            if norm_soluble_mod64(P,Q):
                if A%2==0 or (A*pow(B,-1,64))%64 not in (9,23,41,55):
                    bad+=1
    assert bad==0
    print('B odd, 1<=B<=99, 3B<A<=500, gcd(A,B)=1:')
    print('  primitive pairs:',total)
    print('  pairs with no 3(mod4) prime factor of P or Q:',checked)
    print('  violations among mod64 norm-soluble pairs:',bad)
    print('PASS: independent factorization + modular square residues')

if __name__=='__main__':
    main()
