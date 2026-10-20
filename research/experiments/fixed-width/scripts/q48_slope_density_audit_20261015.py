#!/usr/bin/env python3
"""Independent finite audit of four-row eight-point-circle slope sparsity.

All tests are bounded; they do not establish the asymptotic theorem.
"""
from math import gcd, isqrt

def no_inert_factor_table(n):
    good = bytearray(b'\x01') * (n + 1)
    good[0] = 0
    sieve = bytearray(b'\x01') * (n + 1)
    sieve[:2] = b'\x00\x00'
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            for k in range(p * p, n + 1, p):
                sieve[k] = 0
    for p in range(3, n + 1, 4):
        if sieve[p]:
            for k in range(p, n + 1, p):
                good[k] = 0
    return good

def sum_two_squares_table(n):
    values = bytearray(n + 1)
    squares = [k*k for k in range(isqrt(n)+1)]
    for x in squares:
        for y in squares:
            if x+y > n: break
            values[x+y] = 1
    return values

def audit(H, good, sos):
    cnt_primitive = cnt_inert = cnt_all_four = 0
    for A in range(1,H+1):
        for B in range(1,(A-1)//3+1):
            if gcd(A,B)!=1: continue
            cnt_primitive += 1
            g = gcd(A,3)
            P=A*A-B*B
            Q=(A*A-9*B*B)//(g*g)
            if not (good[P] and good[Q]): continue
            cnt_inert += 1
            f1,f2=A-B,A+B
            f3,f4=(A-3*B)//g,(A+3*B)//g
            assert all(sos[z] for z in (f1,f2,f3,f4)), (A,B)
            cnt_all_four += 1
    r=sum(sos[1:2*H+1])
    return H,cnt_primitive,cnt_inert,cnt_all_four,r,r*r

def main():
    Hmax=1200
    good=no_inert_factor_table(Hmax*Hmax)
    sos=sum_two_squares_table(2*Hmax)
    for H in (100,200,400,800,1200):
        print(*audit(H,good,sos))
    for n in range(1,2*Hmax+1):
        if good[n]: assert sos[n],n
    print('verified every inert-free integer <=',2*Hmax,'is a sum of two squares')

if __name__=='__main__': main()
