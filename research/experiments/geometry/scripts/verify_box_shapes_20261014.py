#!/usr/bin/env python3
"""Exact, independent full-box and normalized-span enumeration for q=4."""
from itertools import combinations
from collections import Counter

def det(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])

def bad_lift(Q):
    x,y=Q[0]
    return det(*[(u-x,v-y,u*u+v*v-x*x-y*y) for u,v in Q[1:]])==0

def bad_circle(Q):
    (x,y),(a,b),(c,d),(u,v)=Q
    p,q=a-x,b-y; r,s=c-x,d-y
    cross=p*s-q*r
    if not cross:
        return p*(v-y)==q*(u-x)
    f=a*a+b*b-x*x-y*y
    g=c*c+d*d-x*x-y*y
    return 2*cross*(u*u+v*v-x*x-y*y)==2*((f*s-q*g)*(u-x)+(p*g-f*r)*(v-y))

def good(S,bad):
    return all(not bad(Q) for Q in combinations(S,4))

def points(m,n):
    return [(x,y) for x in range(m) for y in range(n)]

def audit(side=5, max_k=5):
    for Q in combinations(points(side,side),4):
        assert bad_lift(Q)==bad_circle(Q),Q
    A={}; C=Counter()
    for m in range(1,side+1):
        for n in range(1,side+1):
            P=points(m,n)
            for k in range(1,min(max_k,len(P))+1):
                A[m,n,k]=sum(good(S,bad_lift) for S in combinations(P,k))
    for s in range(side):
        for t in range(side):
            P=points(s+1,t+1)
            for k in range(1,min(max_k,len(P))+1):
                C[k,s,t]=sum(good(S,bad_circle) for S in combinations(P,k)
                             if min(x for x,y in S)==0 and max(x for x,y in S)==s
                             and min(y for x,y in S)==0 and max(y for x,y in S)==t)
    for (m,n,k),count in A.items():
        assert count==sum(c*max(0,m-s)*max(0,n-t) for (j,s,t),c in C.items() if j==k)
    def a(m,n,k): return A.get((m,n,k),0)
    for k in range(1,max_k+1):
        for s in range(1,side-1):
            for t in range(1,side-1):
                assert sum((1 if i else -2)*(1 if j else -2)*a(s+i,t+j,k)
                           for i in (-1,0,1) for j in (-1,0,1))==C[k,s,t]
    return {'geometry_quads':12650,'reconstructed_cases':len(A),
            'difference_cases':max_k*(side-2)**2,
            'A_4_3x3':A[3,3,4], 'C_4_span2x2':C[4,2,2], 'A_5_5x5':A[5,5,5]}

if __name__=='__main__': print(audit())
