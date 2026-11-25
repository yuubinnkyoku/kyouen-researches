#!/usr/bin/env python3
"""Independent integer geometry and mod-9 audit for five anisotropic rows.

No third-party dependencies.  No finite check is used as a proof of unboundedness.
"""
from collections import defaultdict
from itertools import combinations
from math import gcd

Q = {i*i % 9 for i in range(9)}
assert Q == {0,1,4,7}
valid4, valid5 = [], []
for a in Q:
    for b in Q:
        z = [a,b]
        for _ in range(3):
            z.append((2*z[-1]-z[-2]-8) % 9)
        if all(v in Q for v in z[:4]):
            valid4.append(z[:4])
        if all(v in Q for v in z):
            valid5.append(z)
assert valid4 == [[1,0,0,1]] and valid5 == []
print('mod9: 16 pairs, one valid four-term prefix, no five-term square sequence')


def det3(p,q,r):
    (x,y),(u,v),(a,b)=p,q,r
    return x*(v-b)+u*(b-y)+a*(y-v)


def circle_key(p,q,r):
    """Primitive signed integer coefficients A,B,C,D of A(x²+y²)+Bx+Cy+D=0."""
    pts=[p,q,r]
    d=det3(*pts)
    if not d:
        return None
    sq=[x*x+y*y for x,y in pts]
    # Cramer's rule for [x y 1][B C D]^T = -sq.
    bn=det3((-sq[0],p[1]),(-sq[1],q[1]),(-sq[2],r[1]))
    cn=det3((p[0],-sq[0]),(q[0],-sq[1]),(r[0],-sq[2]))
    dn=(p[0]*(q[1]*(-sq[2])-(-sq[1])*r[1])
       -p[1]*(q[0]*(-sq[2])-(-sq[1])*r[0])
       +(-sq[0])*(q[0]*r[1]-q[1]*r[0]))
    vals=(d,bn,cn,dn)
    g=gcd(*vals)
    vals=tuple(x//g for x in vals)
    return vals if vals[0]>0 else tuple(-x for x in vals)


def direct_audit(h,d,m,t=0,x0=0):
    pts=[(x0+h*j,t+d*i) for i in range(5) for j in range(m)]
    groups=defaultdict(set)
    for i,j,k in combinations(range(len(pts)),3):
        key=circle_key(pts[i],pts[j],pts[k])
        if key is not None:
            groups[key].update((i,j,k))
    maximum=0
    counts=defaultdict(int)
    for (a,b,c,e),indices in groups.items():
        full={i for i,(x,y) in enumerate(pts) if a*(x*x+y*y)+b*x+c*y+e==0}
        assert indices==full, ('triple circle key collision or bug',h,d,m)
        maximum=max(maximum,len(full))
        counts[len(full)]+=1
    return maximum,counts.get(9,0),counts.get(10,0),len(groups)


cases=[(1,1,10),(1,2,10),(1,3,10),(1,6,10),(1,9,10),
       (2,3,10),(3,1,10),(3,3,10),(3,6,10),(3,9,10),
       (6,3,10),(9,3,10),(9,9,10),(2,2,13)]
for h,d,m in cases:
    maximum,nine,ten,circles=direct_audit(h,d,m,t=17,x0=-23)
    def v3(z):
        k=0
        while z%3==0:
            k+=1;z//=3
        return k
    if v3(d)<=v3(h):
        assert maximum<=8, (h,d,maximum)
    else:
        assert nine==0, (h,d,nine)
    print(f'h={h:2} d={d:2} m={m:2} v3(h)={v3(h)} v3(d)={v3(d)} max={maximum} nine={nine} ten={ten} circles={circles}')
print('PASS: exact rational-circle grouping and five-row 3-adic predictions')
