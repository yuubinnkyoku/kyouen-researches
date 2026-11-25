from itertools import combinations
from collections import Counter
from math import comb

def U(r,t):
    return sum(min(2*r-4*i-3,2*t-4*j-3)
               for i in range(r//2) for j in range(t//2))

def cross(A,B):
    return sum(a+b==c+d for a,b in combinations(A,2)
               for c,d in combinations(B,2))

def determinant(a):
    if len(a)==1: return a[0][0]
    return sum((-1)**j*a[0][j]*determinant([row[:j]+row[j+1:] for row in a[1:]])
               for j in range(len(a)))

checked=0
for r in range(7):
    for t in range(r,7):
        for A in combinations(range(9),r):
            for B in combinations(range(9),t):
                assert cross(A,B)<=U(r,t)
                checked+=1
        A=[2*i+t for i in range(r)]
        B=[2*j+r for j in range(t)]
        assert cross(A,B)==U(r,t)
assert checked==132199
for m in range(2,9):
    points=[(x,y) for y in range(2) for x in range(m)]
    actual=sum(determinant([[x*x+y*y,x,y,1] for x,y in q])==0
               for q in combinations(points,4))
    assert actual==2*comb(m,4)+U(m,m)
print('PASS',checked,'pair-of-sets, all 2xm quadruples m=2..8')
