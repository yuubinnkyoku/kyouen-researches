#!/usr/bin/env python3
"""Exact forbidden-four overlap census via integer curve carriers.

No floating point; independently brute-forces four-subsets and edge pairs on small boards.
"""
import argparse
import json
from collections import defaultdict, Counter
from itertools import combinations
from math import comb, gcd
from functools import reduce


def key_line(p,q):
    x,y=p; u,v=q
    a=v-y; b=x-u; c=-(a*x+b*y)
    g=reduce(gcd,(abs(a),abs(b),abs(c)))
    a,b,c=a//g,b//g,c//g
    if next(t for t in (a,b,c) if t)!=abs(next(t for t in (a,b,c) if t)):
        a,b,c=-a,-b,-c
    return a,b,c


def key_circle(p,q,r):
    x,y=p; u,v=q; s,t=r
    ux=u-x; vy=v-y; sx=s-x; ty=t-y
    d=ux*ty-vy*sx
    if d==0: return None
    h=ux*ux+vy*vy; j=sx*sx+ty*ty
    # d * (x^2+y^2) + A*x + B*y + C = 0, with A,B,C integral
    a=(vy*j-ty*h) - 2*x*d
    b=(sx*h-ux*j) - 2*y*d
    c=-d*(x*x+y*y)-a*x-b*y
    g=reduce(gcd,(abs(d),abs(a),abs(b),abs(c)))
    d,a,b,c=d//g,a//g,b//g,c//g
    if d<0: d,a,b,c=-d,-a,-b,-c
    return d,a,b,c


def carriers(w,h):
    pts=[(x,y) for y in range(h) for x in range(w)]
    lines=defaultdict(set)
    circles=defaultdict(set)
    for i,j in combinations(range(len(pts)),2):
        L=lines[key_line(pts[i],pts[j])]
        L.add(i);L.add(j)
    for i,j,k in combinations(range(len(pts)),3):
        key=key_circle(pts[i],pts[j],pts[k])
        if key is not None:
            C=circles[key];C.add(i);C.add(j);C.add(k)
    return pts,[("line",s) for s in lines.values() if len(s)>=4]+[("circle",s) for s in circles.values() if len(s)>=4]


def census(w,h):
    pts,cs=carriers(w,h)
    n=len(pts)
    F=0;O3=0;O2in=0
    d1=[0]*n
    d2=defaultdict(list)
    types=Counter()
    spectrum=defaultdict(Counter)
    for typ,s in cs:
        k=len(s)
        types[typ]+=comb(k,4)
        spectrum[typ][k]+=1
        F+=comb(k,4)
        O3+=10*comb(k,5)
        O2in+=45*comb(k,6)
        for p in s:d1[p]+=comb(k-1,3)
        weight=comb(k-2,2)
        for p in combinations(sorted(s),2):d2[p].append((typ,weight))
    cross=Counter()
    pairinc=0
    for groups in d2.values():
        pairinc+=comb(sum(v for t,v in groups),2)
        for i in range(len(groups)):
            for j in range(i):
                typ=tuple(sorted((groups[i][0],groups[j][0])))
                cross['+'.join(typ)]+=groups[i][1]*groups[j][1]
    O2=O2in+sum(cross.values())
    # Alternative independent incidence formula; any shared triple contributes 3 pairs.
    assert O2==pairinc-3*O3,(O2,pairinc,O3)
    O1=sum(comb(v,2) for v in d1)-2*O2-3*O3
    O0=comb(F,2)-O1-O2-O3
    assert min(O0,O1,O2,O3)>=0
    return {'w':w,'h':h,'points':n,'carriers':len(cs),'carrier_spectrum':{t:dict(sorted(c.items())) for t,c in spectrum.items()},'forbidden':F,'forbidden_by_type':dict(types),'overlap_0':O0,'overlap_1':O1,'overlap_2':O2,'overlap_3':O3,'overlap_2_same_carrier':O2in,'overlap_2_cross_carrier':dict(cross),'max_point_degree':max(d1,default=0),'max_pair_degree':max((sum(v for _,v in groups) for groups in d2.values()),default=0)}


def brute(w,h):
    pts=[(x,y) for y in range(h) for x in range(w)]
    def bad(ids):
        x,y=pts[ids[0]]
        vv=[(pts[j][0]-x,pts[j][1]-y,(pts[j][0]-x)**2+(pts[j][1]-y)**2) for j in ids[1:]]
        a,b,c=vv
        return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])==0
    edges=[sum(1<<j for j in Q) for Q in combinations(range(len(pts)),4) if bad(Q)]
    overlap=Counter((a&b).bit_count() for a,b in combinations(edges,2))
    return len(edges),[overlap[j] for j in range(4)]

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--max-n',type=int,default=11);ap.add_argument('--brute-max',type=int,default=5);ap.add_argument('--output',default=None)
    args=ap.parse_args();res=[]
    for n in range(2,args.max_n+1):
        r=census(n,n)
        if n<=args.brute_max:
            b=brute(n,n)
            assert (r['forbidden'],[r[f'overlap_{j}'] for j in range(4)])==b,(r,b)
            r['brute_checked']=True
        res.append(r)
        print(n,r['forbidden'],*[r[f'overlap_{j}'] for j in range(4)],r['overlap_2_cross_carrier'],flush=True)
    if args.output:
        with open(args.output,'w',encoding='utf-8') as f:json.dump(res,f,ensure_ascii=False,indent=2)
