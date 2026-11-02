#!/usr/bin/env python3
"""Exact audit of polynomial-bit integer realization of graph-star games.

Construction: bounded integer slopes, exact rational arithmetic.
Audit: independent 4x4 integer circle determinants and direct terminal enumeration.
"""
from fractions import Fraction
from itertools import combinations
from math import comb
from collections import Counter


def line(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def det3(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])


def circle(a,b,c,d):
    x0,y0=a
    def row(p):
        x,y=p
        return (x-x0,y-y0,x*x+y*y-x0*x0-y0*y0)
    return det3(row(b),row(c),row(d))==0


def on_circle(p,a,b):
    x,y=p
    A=a*b*(a+b)
    B=-(1+a*a+a*b+b*b)
    return x*x+y*y+A*x+B*y==0


def construct(t,edges,q):
    assert q>=4 and t>=2 and edges
    edges=sorted(tuple(sorted(e)) for e in edges)
    assert all(1<=a<b<=t for a,b in edges)
    r=q-3
    n=1+t+r*len(edges)
    M=2*comb(n,3)+2*comb(n,2)+n+2*len(edges)+3
    points=[(Fraction(0),Fraction(0))]+[(Fraction(i),Fraction(i*i)) for i in range(1,t+1)]
    labels=[('O',0)]+[('V',i) for i in range(1,t+1)]
    max_slope=0
    denominators=[]
    for a,b in edges:
        A=a*b*(a+b)
        B=-(1+a*a+a*b+b*b)
        for j in range(r):
            for s in range(1,M+1):
                x=Fraction(-(A+B*s),1+s*s)
                p=(x,s*x)
                if p in points: continue
                if any(on_circle(p,c,d) for c,d in edges if (c,d)!=(a,b)): continue
                if any(line(v,w,p)==0 for v,w in combinations(points,2)): continue
                if any(circle(v,w,z,p) for v,w,z in combinations(points,3)
                       if not all(on_circle(pt,a,b) for pt in (v,w,z))): continue
                points.append(p)
                labels.append(('P',a,b,j))
                max_slope=max(max_slope,s)
                denominators.append(1+s*s)
                break
            else:
                raise AssertionError(('No slope',t,edges,q,a,b,j,M))
    D=1
    for d in denominators:
        D*=d
    integer=[(int(x*D),int(y*D)) for x,y in points]
    return integer,labels,max_slope,M,D


def circle4(a,b,c,d):
    # Bareiss 4x4 determinant, independent of the construction's 3x3 test.
    rows=[[x*x+y*y,x,y,1] for x,y in (a,b,c,d)]
    mat=[row[:] for row in rows]
    sign=1
    last=1
    for k in range(3):
        if mat[k][k]==0:
            pivot=next((i for i in range(k+1,4) if mat[i][k]!=0),None)
            if pivot is None: return True
            mat[k],mat[pivot]=mat[pivot],mat[k]
            sign=-sign
        p=mat[k][k]
        for i in range(k+1,4):
            for j in range(k+1,4):
                num=mat[i][j]*p-mat[i][k]*mat[k][j]
                assert num%last==0
                mat[i][j]=num//last
        for i in range(k+1,4):mat[i][k]=0
        last=p
    return sign*mat[3][3]==0


def audit(t,edges,q,full=False):
    edges=set(tuple(sorted(e)) for e in edges)
    pts,labels,used,bound,D=construct(t,edges,q)
    n=len(pts)
    assert len(set(pts))==n
    assert all(line(*[pts[i] for i in ids])!=0 for ids in combinations(range(n),3))
    for ids in combinations(range(n),4):
        is_target=any(set(ids)<=({0,a,b}|{i for i,l in enumerate(labels) if l[0]=='P' and l[1:3]==(a,b)}) for a,b in edges)
        assert circle4(*[pts[i] for i in ids])==is_target,(t,edges,q,ids,labels)
    if q>4:
        target={frozenset([0,a,b]+[i for i,l in enumerate(labels) if l[0]=='P' and l[1:3]==(a,b)]) for a,b in edges}
        actual={frozenset(ids) for ids in combinations(range(n),q) if
                all(circle4(*[pts[i] for i in subset]) for subset in combinations(ids,4))}
        assert target==actual,(target,actual)
    if full:
        hyperedges=[]
        for a,b in edges:
            ids={0,a,b}|{i for i,l in enumerate(labels) if l[0]=='P' and l[1:3]==(a,b)}
            hyperedges.append(sum(1<<i for i in ids))
        counts=Counter()
        for S in range(1<<n):
            if any((S&h)==h for h in hyperedges): continue
            if all(any(((S|(1<<i))&h)==h for h in hyperedges) for i in range(n) if not (S>>i&1)):
                counts[S.bit_count()]+=1
        r=q-3
        expected=Counter({n-1:1})
        for X in range(1<<t):
            if any((X>>(v-1)&1) and not any(not (X>>(w-1)&1) for a,b in edges for w in ([b] if a==v else ([a] if b==v else []))) for v in range(1,t+1)):
                continue
            e_rest=sum(not (X>>(a-1)&1) and not (X>>(b-1)&1) for a,b in edges)
            expected[n-X.bit_count()-e_rest]+=r**e_rest
        assert counts==expected,(t,edges,q,counts,expected)
    return n,used,bound,max(max(abs(x),abs(y)).bit_length() for x,y in pts)


def run():
    cases=0; fulls=0; max_bits=0; max_slope=0
    for t in range(2,5):
        possible=list(combinations(range(1,t+1),2))
        for mask in range(1,1<<len(possible)):
            edges=[e for j,e in enumerate(possible) if mask>>j&1]
            for q in (4,5):
                n,used,bound,bits=audit(t,edges,q,full=(1+t+(q-3)*len(edges)<=12))
                cases+=1; max_bits=max(max_bits,bits);max_slope=max(max_slope,used)
                fulls+=int(n<=12)
    for t in (2,3):
        possible=list(combinations(range(1,t+1),2))
        for mask in range(1,1<<len(possible)):
            edges=[e for j,e in enumerate(possible) if mask>>j&1]
            for q in (6,7):
                n,used,bound,bits=audit(t,edges,q,full=(1+t+(q-3)*len(edges)<=12))
                cases+=1; max_bits=max(max_bits,bits);max_slope=max(max_slope,used)
                fulls+=int(n<=12)
    for t,edges,q in [(5,[(1,2),(2,3),(3,4),(4,5)],4),
                      (5,[(1,2),(1,3),(1,4),(1,5)],5),
                      (5,[(1,2),(2,3),(3,4),(4,5),(1,5)],4)]:
        n,used,bound,bits=audit(t,edges,q,full=(1+t+(q-3)*len(edges)<=12))
        cases+=1;max_bits=max(max_bits,bits);max_slope=max(max_slope,used)
        fulls+=int(n<=12)
    print({'graphs_and_q':cases,'full_terminal_checks':fulls,'max_coordinate_bits':max_bits,'max_used_slope':max_slope,'mismatches':0})


if __name__=='__main__':run()
