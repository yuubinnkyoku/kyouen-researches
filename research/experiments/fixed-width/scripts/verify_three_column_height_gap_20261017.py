#!/usr/bin/env python3
"""Independent finite checks for 3-column 5/6-circle height-gap family."""
from itertools import combinations
from math import gcd
from functools import reduce


def determinant3(rows):
    (a,b,c),(d,e,f),(g,h,i)=rows
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)


def circles_from_triples(a,b,d,k):
    assert a*b==d*d*k*(k+1)
    xs=(0,a,a+b); m=2*k+2
    points=[(x,d*y) for x in xs for y in range(m)]
    circles=set()
    for triple in combinations(points,3):
        a=[(x,y,1) for x,y in triple]
        den=determinant3(a)
        if not den: continue
        vals=[x*x+y*y for x,y in triple]
        an=determinant3([(-v,y,1) for (x,y),v in zip(triple,vals)])
        bn=determinant3([(x,-v,1) for (x,y),v in zip(triple,vals)])
        cn=determinant3([(x,y,-v) for (x,y),v in zip(triple,vals)])
        common=reduce(gcd,(den,an,bn,cn))
        if den<0: common=-common
        circles.add(tuple(v//common for v in (den,an,bn,cn)))
    mins={5:10**9,6:10**9}; counts={5:0,6:0}
    for D,A,B,C in circles:
        ys=sorted(y//d for x,y in points if D*(x*x+y*y)+A*x+B*y+C==0)
        for q in (5,6):
            if len(ys)>=q:
                counts[q]+=1
                mins[q]=min(mins[q],min(ys[i+q-1]-ys[i]+1 for i in range(len(ys)-q+1)))
    return mins,counts,len(circles)


def circles_from_chords(a,b,d,k):
    assert a*b==d*d*k*(k+1)
    m=2*k+2
    maxD=2*(m-1)
    mins={5:10**9,6:10**9}; candidates=0
    for d0 in range(maxD+1):
        for d2 in range(maxD+1):
            numerator=b*d0*d0+a*d2*d2+4*(a+b)*k*(k+1)
            if numerator%(a+b):continue
            sq=numerator//(a+b)
            d1=__import__('math').isqrt(sq)
            if d1*d1!=sq or d1>maxD or (d0-d1)%2 or (d2-d1)%2:continue
            candidates+=1
            s=d1%2
            ys=[]
            for D in (d0,d1,d2):
                ys.append((s+D)//2)
                if D:ys.append((s-D)//2)
            ys.sort()
            for q in (5,6):
                if len(ys)>=q:
                    mins[q]=min(mins[q],min(ys[i+q-1]-ys[i]+1 for i in range(len(ys)-q+1)))
    return mins,candidates


if __name__=='__main__':
    cases=[(1,k*(k+1),1,k) for k in range(1,11)]
    cases += [(2,3,1,2),(2,12,2,2),(3,8,2,2),(4,5,1,4),
              (4,20,2,4),(6,20,2,5),(9,20,3,4)]
    for a,b,d,k in cases:
        m1,cnt,ncir=circles_from_triples(a,b,d,k)
        m2,nch=circles_from_chords(a,b,d,k)
        expected={5:k+2,6:2*k+2}
        assert m1==expected,(a,b,d,k,m1,expected)
        assert m2==expected,(a,b,d,k,m2,expected)
        print(f'a={a:3d} b={b:3d} d={d:2d} k={k:2d} H5={m1[5]:2d} H6={m1[6]:2d} determinant_circles={ncir:6d} chord_solutions={nch:3d} agreement=OK')
