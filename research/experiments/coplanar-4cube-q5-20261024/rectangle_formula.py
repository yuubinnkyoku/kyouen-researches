#!/usr/bin/env python3
"""Independent exact 3x3 minors for binary coplanar quadruples."""
from itertools import combinations
def det3(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def coplanar(p,d):
    v=[[((p[j]>>k)&1)-((p[0]>>k)&1) for k in range(d)] for j in range(1,4)]
    for i,j,k in combinations(range(d),3):
        if det3([v[0][i],v[0][j],v[0][k]],
                [v[1][i],v[1][j],v[1][k]],
                [v[2][i],v[2][j],v[2][k]]):return False
    return True
for d in range(2,7):
    n=sum(coplanar(p,d) for p in combinations(range(1<<d),4))
    expected=(1<<d)*(3**d-2**(d+1)+1)//8
    assert n==expected,(d,n,expected)
    print(d,n)
