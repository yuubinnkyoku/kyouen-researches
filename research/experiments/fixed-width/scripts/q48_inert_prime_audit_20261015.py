#!/usr/bin/env python3
"""Finite independent audit for the 4-row 8-point circle inert-prime obstruction.

Proof is in q48-inert-prime-slope-obstruction-20261015.md.
All enumeration ranges here are finite; the proof is not inferred from them.
"""
from math import gcd, isqrt
from collections import Counter

CHORDS = [
    (35, 51, 63, 73),
    (1331, 1935, 2391, 2773),
    (50543, 73479, 90795, 105301),
    (445465, 715719, 908883, 1067653),
    (98119, 1096275, 1547259, 1893727),
]


def inert_prime_factors(n):
    assert n > 0
    factors = []
    k = 2
    while k*k <= n:
        if n % k == 0:
            if k % 4 == 3:
                factors.append(k)
            while n % k == 0:
                n //= k
        k = 3 if k == 2 else k+2
    if n > 1 and n % 4 == 3:
        factors.append(n)
    return factors


def normalized(ch):
    a,b,c,d = ch
    assert a*a-2*b*b+c*c == b*b-2*c*c+d*d == -8
    s=(a+d)//2; v=(c-b)//2; u=(b+c)//2
    h=gcd(s,v); A=s//h; B=v//h; g=gcd(A,3)
    assert u*g % A == 0
    L=h; M=u*g//A
    P=A*A-B*B; Q=(A*A-9*B*B)//(g*g)
    assert Q*M*M-P*L*L == 8
    assert A%2 == 1
    assert A%9 == 0 or B%3 == 0
    assert not inert_prime_factors(P) and not inert_prime_factors(Q)
    return (A,B,L,M,P,Q)


def primes_upto(n):
    return [p for p in range(2,n+1) if all(p%d for d in range(2,isqrt(p)+1))]


def prime_local_audit():
    # The two g choices are checked separately: modulo p, g is independent
    # of the residue of A (CRT with the condition modulo 3).
    out=[]
    for p in primes_upto(71):
        if p < 7 or p%4 != 3:continue
        bad = set()
        for B in range(1,p):
            for k in (1,-1,3,-3):
                bad.add((k*B%p,B))
        assert len(bad)==4*(p-1)
        squares={x*x%p for x in range(p)}
        for A,B in bad:
            P=(A*A-B*B)%p
            for g in (1,3):
                Q=(A*A-9*B*B)*pow(g*g,-1,p)%p
                # independent QR-set test of the complete norm equation
                residues={(Q*x-P*y)%p for x in squares for y in squares}
                assert 8%p not in residues, (p,A,B,g)
        # Independent direct enumeration (no QR-set shortcut) for small p.
        if p <= 31:
            for A,B in bad:
                for g in (1,3):
                    P=(A*A-B*B)%p
                    Q=(A*A-9*B*B)*pow(g*g,-1,p)%p
                    for L in range(p):
                        for M in range(p):
                            assert (Q*M*M-P*L*L-8)%p != 0
        # Count admissible primitive residue pairs (0,0 is excluded).
        admissible=sum((A,B) not in bad and (A,B)!=(0,0)
                       for A in range(p) for B in range(p))
        assert admissible==(p-1)*(p-3)
        out.append((p,len(bad),admissible,p*p))
    return out


def mod3_audit():
    checked=0
    for A in range(1,28):
        for B in range(1,28):
            if A%3==0 and B%3==0:continue
            g=gcd(A,3)
            P=A*A-B*B; Q=(A*A-9*B*B)//(g*g)
            valid=[]
            for L in range(3):
                for M in range(3):
                    if (Q*M*M-P*L*L-8)%3==0:
                        valid.append((L,M))
            if A%9==0:
                assert B%3 and valid and all(L%3==0 and M%3 for L,M in valid)
            elif B%3==0:
                assert A%3 and valid and all(M%3==0 and L%3 for L,M in valid)
            else:
                assert not valid
            checked+=1
    return checked


def finite_slope_sieve(Amax=500, Bmax=100):
    counts=Counter(); examples=[]
    for A in range(1,Amax+1):
        for B in range(1,min(Bmax,A//4)+1):
            if A**4-18*A*A*B*B+9*B**4 <= 0:continue
            if gcd(A,B)!=1:continue
            counts['primitive_above_gap']+=1
            if not (A%9==0 or B%3==0):continue
            counts['after_mod3']+=1
            if A%2==0:continue
            counts['after_odd_A']+=1
            g=gcd(A,3)
            P=A*A-B*B;Q=(A*A-9*B*B)//(g*g)
            if inert_prime_factors(P) or inert_prime_factors(Q):continue
            counts['after_all_inert_primes']+=1
            if len(examples)<20:examples.append((A,B,P,Q))
    return counts,examples


def main():
    print('mod3 residue pairs checked:',mod3_audit())
    print('local p, forbidden nonzero pairs, admissible pairs, all pairs:')
    for row in prime_local_audit():print(' ',*row)
    print('five known nonlocal circles:')
    for ch in CHORDS:print(' ',normalized(ch))
    counts,examples=finite_slope_sieve()
    print('bounded primitive slopes 1<=A<=500, 1<=B<=100, A/B>sqrt(9+6sqrt(2)):')
    print(' ',dict(counts))
    print('first surviving necessary-condition candidates:',examples)

if __name__=='__main__':main()
