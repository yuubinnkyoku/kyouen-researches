#!/usr/bin/env python3
"""Exact residue audit and independent triple-determinant circle census."""
from itertools import combinations
from math import gcd

Q={x*x%9 for x in range(9)}

def mod9_audit():
    valid=[]
    for a in Q:
        for b in Q:
            z=[(a+i*(b-a)-4*i*(i-1))%9 for i in range(5)]
            if all(v in Q for v in z[:4]): valid.append(tuple(z))
    assert valid==[(1,0,0,1,3)]
    for d in (1,2,4,5,7,8):
        inv=pow((d*d)%9,-1,9)
        count=0
        for a in Q:
            for b in Q:
                z=[a,b]
                for _ in range(3):z.append((2*z[-1]-z[-2]-8*d*d)%9)
                if all(v in Q for v in z):count+=1
                normalized=[v*inv%9 for v in z]
                assert all(v in Q for v in z)==all(v in Q for v in normalized)
        assert count==0,(d,count)
    for d in (3,6,9):
        seq=[]
        for a in Q:
            for b in Q:
                z=[a,b]
                for _ in range(3):z.append((2*z[-1]-z[-2]-8*d*d)%9)
                if all(v in Q for v in z):seq.append(z)
        assert seq and all(not (0 in z and any(x!=0 for x in z)) for z in seq)
    print('PASS modular: d units 1,2,4,5,7,8; 3|d zero-propagation')

def det3(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])

def circle(p,q,r):
    x=[p[0],q[0],r[0]];y=[p[1],q[1],r[1]]
    z=[xx*xx+yy*yy for xx,yy in zip(x,y)]
    o=[1,1,1]
    def d(a,b,c):return det3((a[0],b[0],c[0]),(a[1],b[1],c[1]),(a[2],b[2],c[2]))
    A=d(x,y,o)
    if A==0:return None
    B,C,D=-d(z,y,o),-d(x,z,o),-d(x,y,z)
    if A<0:A,B,C,D=-A,-B,-C,-D
    g=gcd(gcd(A,abs(B)),gcd(abs(C),abs(D)))
    return A//g,B//g,C//g,D//g

def census(m,d,t=0):
    pts=[(x,t+i*d) for i in range(5) for x in range(m)]
    circles={c for p,q,r in combinations(pts,3) if (c:=circle(p,q,r)) is not None}
    largest=0
    for A,B,C,D in circles:
        count=sum(A*(x*x+y*y)+B*x+C*y+D==0 for x,y in pts)
        assert (count<=8 if d%3 else count!=9),(m,d,t,A,B,C,D,count)
        largest=max(largest,count)
    return len(circles),largest

if __name__=='__main__':
    mod9_audit()
    for d in (1,2,3,4,5,6,7,8,9,12):
        for m in (4,6,8):
            n,k=census(m,d)
            print(f'd={d} m={m} circles={n} max={k}')
    for t in (1,7,-5):
        n,k=census(8,2,t)
        print(f'd=2 m=8 t={t} circles={n} max={k}')
    print('PASS: finite exact determinant census; universal claim uses modular proof')
