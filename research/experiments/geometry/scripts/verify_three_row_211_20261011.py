#!/usr/bin/env python3
"""Independent determinant audit of three-row (2,1,1) circle equations.
Standard library only. Run: python verify_three_row_211_20261011.py
"""
from itertools import combinations
from collections import Counter
from math import isqrt


def incircle(pts):
    # Exact determinant of the 4x4 matrix [x^2+y^2,x,y,1].
    # Translate the fourth point to the origin, then use the 3x3 determinant.
    p = pts[-1]
    rows = []
    for x,y in pts[:-1]:
        X,Y = x-p[0],y-p[1]
        rows.append((X*X+Y*Y,X,Y))
    (a,b,c),(d,e,f),(g,h,i) = rows
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g) == 0


def eq_count(m, base):
    ans = 0
    # base=0 or 2: y=0,1,2 under reflection. base=1: symmetric rows.
    for a in range(m):
        for b in range(a+1,m):
            d,s=b-a,a+b
            for u in range(m):
                for v in range(m):
                    X,Y=2*u-s,2*v-s
                    if base == 1:
                        ok = X*X+Y*Y == 2*d*d-8
                    else:
                        ok = 2*X*X-Y*Y == d*d+8
                    ans += ok
    return ans


def det_count(m):
    pts=[(x,y) for y in range(3) for x in range(m)]
    bytype=Counter()
    for quad in combinations(pts,4):
        counts=Counter(y for x,y in quad)
        if not incircle(quad):
            continue
        if sorted(counts.values()) == [1,1,2]:
            base=next(y for y,n in counts.items() if n==2)
            bytype[base]+=1
    return [bytype[i] for i in range(3)]


def direct_eq(m,base):
    # Direct substitution in circle polynomial, distinct from Pell/sum-of-squares test.
    out=0
    for a,b in combinations(range(m),2):
        s=a+b
        for u in range(m):
            for v in range(m):
                if base == 0:
                    # D = -((u-a)(u-b)+1) for y=1; evaluate at y=2
                    D=-(u-a)*(u-b)-1
                    ok=(v-a)*(v-b)+4+2*D==0
                elif base == 1:
                    # shifted middle y=0, outer y=-1 and +1
                    # at -1: f(u)+1-D=0 => D=f(u)+1; at +1: f(v)+1+D=0
                    D=(u-a)*(u-b)+1
                    ok=(v-a)*(v-b)+1+D==0
                else:
                    D=-(u-a)*(u-b)-1
                    ok=(v-a)*(v-b)+4+2*D==0
                out+=ok
    return out


def reps(n):
    if n<0: return 0
    total=0
    for x in range(-isqrt(n),isqrt(n)+1):
        y2=n-x*x
        y=isqrt(y2)
        if y*y==y2:
            total+=1 if y==0 else 2
    return total


def middle_infinite_check():
    for h in range(1,6):
        for d in range(1,101):
            n=2*d*d-8*h*h
            direct=0
            if n>=0:
                for x in range(-isqrt(n),isqrt(n)+1):
                    yy=n-x*x
                    y=isqrt(yy)
                    if y*y!=yy: continue
                    for z in ({y,-y}):
                        if x%2 == d%2 and z%2==d%2: direct+=1
            assert direct==reps(n),(h,d,direct,reps(n))


def pell_check():
    x,y=3,3
    vals=[]
    for k in range(12):
        assert 2*x*x-y*y==9 and x%2==1 and y%2==1
        a,b,u,v=0,1,(1+x)//2,(1+y)//2
        assert incircle([(a,0),(b,0),(u,1),(v,2)])
        vals.append((k,u,v))
        x,y=3*x+2*y,4*x+3*y
    return vals



def span_formula(m,base):
    """Number-theoretic weighted representation sum; no quadruple loops."""
    total=0
    for d in range(1,m):
        n=(2*d*d-8) if base==1 else (d*d+8)
        for X in range(-3*m,3*m+1):
            if X%2!=d%2: continue
            if base==1:
                Y2=n-X*X
            else:
                Y2=2*X*X-n
            if Y2<0: continue
            Y=isqrt(Y2)
            if Y*Y!=Y2: continue
            for Z in ({Y,-Y}):
                if Z%2!=d%2: continue
                alpha,beta=(d+X)//2,(d+Z)//2
                offsets=(0,d,alpha,beta)
                span=max(offsets)-min(offsets)
                total+=max(0,m-span)
    return total


def equal_row_energy(m):
    return sum(sum(1 for a,b in combinations(range(m),2) if a+b==s)**2
               for s in range(2*m-1))


def all_forbidden_direct(m):
    pts=[(x,y) for y in range(3) for x in range(m)]
    return sum(incircle(quad) or len({y for x,y in quad})==1
               for quad in combinations(pts,4))


def main():
    middle_infinite_check()
    vals=pell_check()
    print('Pell witnesses (k,u,v):',vals[:6])
    for m in range(2,16):
        eq=[eq_count(m,i) for i in range(3)]
        direct=[direct_eq(m,i) for i in range(3)]
        det=det_count(m)
        weighted=[span_formula(m,i) for i in range(3)]
        assert eq==direct==det==weighted,(m,eq,direct,det,weighted)
        E=equal_row_energy(m)
        forbidden=3*__import__('math').comb(m,4) if m>=4 else 0
        forbidden+=3*E+sum(eq)
        if m<=12:
            assert all_forbidden_direct(m)==forbidden,(m,forbidden)
        print('m=%2d 2+1+1 bottom/middle/top=%s total=%d all_forbidden=%d'%(m,eq,sum(eq),forbidden))
    print('PASS: 4 independent counts, m=2..15; all forbidden m=2..12; middle row representation parity h=1..5,d=1..100; 12 Pell witnesses')

if __name__=='__main__':main()
