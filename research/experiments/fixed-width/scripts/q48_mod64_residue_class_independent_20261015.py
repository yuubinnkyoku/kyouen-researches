#!/usr/bin/env python3
"""Independent arithmetic audit for odd-denominator q48 nonlocal slopes."""
from math import gcd

ROOTS = {9, 23, 41, 55}


def inert_free(n):
    assert n > 0
    p = 2
    while p * p <= n:
        if n % p == 0:
            if p % 4 == 3:
                return False
            while n % p == 0:
                n //= p
        p += 1
    return n % 4 != 3


def norm64(P, Q):
    squares = {i * i % 64 for i in range(64)}
    return 8 in {(Q * u - P * v) % 64 for u in squares for v in squares}


def known_circle(a, b, c, d):
    # Each chord has the same midpoint, and square chord differences -8.
    assert all(t % 2 for t in (a,b,c,d))
    assert a*a - 2*b*b + c*c == -8
    assert b*b - 2*c*c + d*d == -8
    s, v = (a+d)//2, (c-b)//2
    k = gcd(s,v)
    A,B = s//k, v//k
    assert A>3*B and gcd(A,B)==1
    return A,B


def run():
    for b in range(1,64,2):
        roots = {a * pow(b,-1,64) % 64 for a in range(1,64,2)
                 if (a*a-b*b)%64 == 16}
        assert roots == ROOTS, (b,roots)
    checked = passed = rejected = 0
    for B in range(1,201):
        for A in range(3*B+1,1001):
            if gcd(A,B)!=1 or A**4-18*A*A*B*B+9*B**4 <= 0:
                continue
            if not (A%9==0 or B%3==0):
                continue
            g=gcd(A,3)
            P=A*A-B*B
            Q=(A*A-9*B*B)//(g*g)
            if not (inert_free(P) and inert_free(Q)):
                continue
            checked+=1
            if B%2:
                assert A%2
                admissible=(A*pow(B,-1,64))%64 in ROOTS
                # A solution modulo 64 need not exist when the residue fails.
                assert norm64(P,Q)==admissible, (A,B,P,Q)
                if admissible:
                    passed+=1
                else:
                    rejected+=1
    assert (checked, passed, rejected)==(735,39,60), (checked,passed,rejected)
    for c in [(35,51,63,73),(1331,1935,2391,2773),
              (50543,73479,90795,105301),
              (445465,715719,908883,1067653),
              (98119,1096275,1547259,1893727)]:
        A,B=known_circle(*c)
        if B%2:
            assert A*pow(B,-1,64)%64 in ROOTS
    A,B=63,5
    assert inert_free(A*A-B*B) and inert_free((A*A-9*B*B)//gcd(A,3)**2)
    assert A*pow(B,-1,64)%64 not in ROOTS
    print('PASS: four mod-64 slope classes; all 32 odd B residues checked')
    print('PASS: 735 inert-prime survivors, 99 odd-B; 60 excluded, 39 retained')
    print('PASS: all five known nonlocal chord types and 63/5 exclusion')

if __name__=='__main__':
    run()
