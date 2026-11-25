#!/usr/bin/env python3
"""Independent exact-integer audit of fundamental (not squared) Pell reduction."""
from math import gcd, isqrt

def fundamental(D):
    a0 = isqrt(D)
    assert a0*a0 != D
    m, den, a = 0, 1, a0
    p0, p1, q0, q1 = 1, a, 0, 1
    while p1*p1-D*q1*q1 != 1:
        m = den*a-m
        den = (D-m*m)//den
        a = (a0+m)//den
        p0,p1 = p1,a*p1+p0
        q0,q1 = q1,a*q1+q0
    return p1,q1

def params(A,B):
    assert gcd(A,B)==1 and A>3*B
    g=gcd(A,3)
    return A*A-B*B,(A*A-9*B*B)//(g*g),g

def chords(A,B,L,M):
    g=gcd(A,3)
    return (A*L-(3*B//g)*M,(A//g)*M-B*L,(A//g)*M+B*L,A*L+(3*B//g)*M)

def audit(A,B,L,M):
    P,Q,g=params(A,B)
    assert Q*M*M-P*L*L==8
    U,V=fundamental(P*Q)
    assert U*U-P*Q*V*V==1
    assert (P&1)==(Q&1)
    old=(L&1,M&1)
    initial=chords(A,B,L,M)
    assert all(x>0 and x%2 for x in initial) and list(initial)==sorted(initial)
    samples=[]
    for j in range(3):
        ds=chords(A,B,L,M)
        assert all(x>0 and x%2 for x in ds) and list(ds)==sorted(ds)
        assert ds[0]**2-2*ds[1]**2+ds[2]**2==-8
        assert ds[1]**2-2*ds[2]**2+ds[3]**2==-8
        d=ds[3]
        C=(ds[0]**2-ds[1]**2)//4-1
        E=(d*d-ds[0]**2)//4
        for y,span in enumerate(ds):
            for x in ((d-span)//2,(d+span)//2):
                assert x*x+y*y-d*x+C*y+E==0
        samples.append(len(str(d)))
        Ln=U*L+Q*V*M
        Mn=U*M+P*V*L
        assert (Ln&1,Mn&1)==old
        assert Q*Mn*Mn-P*Ln*Ln==8
        assert Ln>L and Mn>M
        L,M=Ln,Mn
    return U,V,samples

if __name__=='__main__':
    seeds=[(9,1,6,19),(9,1,228,721),(9,1,8658,27379),
           (47,6,0,0),(53,12,0,0)]
    # Recover L,M for the two other known chord patterns independently.
    for i,ds in [(3,(445465,715719,908883,1067653)),(4,(98119,1096275,1547259,1893727))]:
        A,B,_,_=seeds[i];g=gcd(A,3)
        s=(ds[3]+ds[0])//2;v=(ds[2]-ds[1])//2
        u=(ds[2]+ds[1])//2
        assert s%A==0 and v%B==0 and s//A==v//B
        assert (u*g)%A==0
        seeds[i]=(A,B,s//A,(u*g)//A)
    for A,B,L,M in seeds:
        U,V,widths=audit(A,B,L,M)
        print('slope',A,B,'seed',L,M,'unit_digits',len(str(U)),len(str(V)),
              'width_digits',widths,'reduction_bound_factor',str(2*U))
    # General parity lemma for all norm-8 solutions in a finite independent sample.
    checked=0
    for P in range(1,61):
        for Q in range(1,61):
            D=P*Q
            if isqrt(D)**2==D or P%2!=Q%2:continue
            for L in range(1,150):
                rhs=8+P*L*L
                if rhs%Q:continue
                M=isqrt(rhs//Q)
                if M==0 or Q*M*M!=rhs:continue
                U,V=fundamental(D)
                Ln=U*L+Q*V*M;Mn=U*M+P*V*L
                assert (Ln&1,Mn&1)==(L&1,M&1)
                checked+=1
    print('independent parity checks:',checked)
    # An unrelated small norm-8 example exercises the *inverse* bound.
    P,Q,U,V=1,3,2,1
    reductions=[]
    for L in range(1,1000):
        rhs=8+P*L*L
        if rhs%Q:continue
        M=isqrt(rhs//Q)
        if M==0 or Q*M*M!=rhs or L*L<=8*Q*V*V:continue
        l=U*L-Q*V*M;m=U*M-P*V*L
        assert 0<l<L and m>0 and Q*m*m-P*l*l==8
        reductions.append((L,M,l,m))
    assert len(reductions)==4
    print('independent inverse reductions:',reductions)
    assert checked>100
    print('PASS')
