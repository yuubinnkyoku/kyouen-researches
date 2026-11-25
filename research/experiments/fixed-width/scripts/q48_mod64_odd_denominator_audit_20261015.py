#!/usr/bin/env python3
"""Independent finite audit for the all-length q48 mod-64 obstruction.

This checks exact integer square residues; it does not use the proof's
case distinction to determine whether the norm equation is solvable.
"""
from math import gcd, isqrt
from collections import Counter

CHORDS=[(35,51,63,73),(1331,1935,2391,2773),
        (50543,73479,90795,105301),
        (445465,715719,908883,1067653),
        (98119,1096275,1547259,1893727)]

def inert_prime_factor(n):
    assert n>0
    d=2
    while d*d<=n:
        if n%d==0:
            if d%4==3:return d
            while n%d==0:n//=d
        d=3 if d==2 else d+2
    return n if n%4==3 else None

def mod64_norm(P,Q):
    squares={x*x%64 for x in range(64)}
    return bool({Q*m%64 for m in squares} & {(8+P*l)%64 for l in squares})

def slope_from_chords(ch):
    a,b,c,d=ch
    assert a*a-2*b*b+c*c==b*b-2*c*c+d*d==-8
    s=(a+d)//2;v=(c-b)//2
    h=gcd(s,v);return s//h,v//h

def audit(H,Bmax):
    cnt=Counter();samples=[]
    for A in range(1,H+1,2):
        for B in range(1,min(Bmax,A//4)+1):
            if gcd(A,B)!=1 or A**4-18*A*A*B*B+9*B**4<=0:continue
            if not(A%9==0 or B%3==0):continue
            g=gcd(A,3)
            P=A*A-B*B;Q=(A*A-9*B*B)//(g*g)
            if inert_prime_factor(P) or inert_prime_factor(Q):continue
            cnt['passed_previous_necessary_conditions']+=1
            if B%2:
                cnt['odd_B']+=1
                necessary=(P%64==16 and Q%64==8)
                # A genuinely independent finite modular check
                actual_mod64=mod64_norm(P,Q)
                assert necessary==actual_mod64,(A,B,P,Q)
                if not necessary:
                    cnt['excluded_by_new_mod64']+=1
                    if len(samples)<10:samples.append((A,B,P,Q))
            else:
                # For even B, there is no new 2-adic obstruction.
                assert mod64_norm(P,Q)
            if B%2==0 or necessary:
                cnt['remaining_after_mod64']+=1
    return dict(cnt),samples

def all_small_odd_residue_pairs():
    # This verification does not assume the inert-prime condition:
    # exact 2-adic criterion is q=P/8 mod 8 in {1,6}.
    checked=0
    for A in range(5,160,2):
        for B in range(1,A//3+1,2):
            if gcd(A,B)!=1:continue
            g=gcd(A,3);P=A*A-B*B;Q=(A*A-9*B*B)//(g*g)
            if Q<=0:continue
            assert P%8==Q%8==0
            assert mod64_norm(P,Q)==((Q//8)%8 in (1,6))
            checked+=1
    return checked

def main():
    assert not mod64_norm(3944,416)
    for ch in CHORDS:
        A,B=slope_from_chords(ch)
        g=gcd(A,3);P=A*A-B*B;Q=(A*A-9*B*B)//(g*g)
        assert mod64_norm(P,Q)
        if B%2:assert P%64==16 and Q%64==8
    print('odd residue pairs checked:',all_small_odd_residue_pairs())
    for H,Bmax in [(500,100),(1000,200)]:
        counts,examples=audit(H,Bmax)
        print('H,Bmax=',H,Bmax,'counts=',counts)
        print('newly excluded examples:',examples)
    print('known circles:',len(CHORDS),'PASS')
    print('counterexample A/B=63/5: norm-8 equation impossible modulo 64')
    print('PASS: finite modular audits only')

if __name__=='__main__':main()
