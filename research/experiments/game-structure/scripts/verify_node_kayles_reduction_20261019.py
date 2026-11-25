#!/usr/bin/env python3
"""Independent exact audit of Node Kayles -> q=4 finite integer board.
Uses the already-proved cubic inversion geometry of K0348 but audits
ALL forbidden quadruples and ALL residual states by fresh recursion.
"""
from functools import lru_cache
from itertools import combinations
from math import lcm
import json
import random


def cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def lifted_det(a,b,c,d):
    def row(p):
        x=p[0]-a[0];y=p[1]-a[1]
        z=p[0]**2+p[1]**2-a[0]**2-a[1]**2
        return x,y,z
    x,y,z=row(b),row(c),row(d)
    return (x[0]*(y[1]*z[2]-y[2]*z[1])
           -x[1]*(y[0]*z[2]-y[2]*z[0])
           +x[2]*(y[0]*z[1]-y[1]*z[0]))


def make_board(n, edges):
    edges=sorted(tuple(sorted(e)) for e in edges)
    ts=[10**v for v in range(n)]+[-10**u-10**v for u,v in edges]
    scale=lcm(*(abs(t)*(1+4*t**4) for t in ts))
    points=[(0,0)]+[(scale//(t*(1+4*t**4)),2*scale*t//(1+4*t**4)) for t in ts]
    occupied=(1<<0)|sum(1<<(1+n+i) for i in range(len(edges)))
    return points,occupied


def audit(n,edges,geometry=True):
    edges=sorted(tuple(sorted(e)) for e in edges)
    pts,S=make_board(n,edges)
    expected={tuple(sorted((0,u+1,v+1,n+1+j))) for j,(u,v) in enumerate(edges)}
    bad=[]
    if geometry:
        for q in combinations(range(len(pts)),4):
            if lifted_det(*(pts[i] for i in q))==0:bad.append(q)
        assert set(bad)==expected,(n,edges,bad,expected)
        assert all(cross(*(pts[i] for i in tri))!=0
                   for tri in combinations(range(len(pts)),3))
    edge_masks=[(1<<u)|(1<<v) for u,v in edges]
    @lru_cache(None)
    def graph_g(mask):
        opts=[]
        for i in range(n):
            child=mask|1<<i
            if not mask>>i&1 and all(child&e!=e for e in edge_masks):
                opts.append(graph_g(child))
        return next(i for i in range(n+1) if i not in opts)
    # Geometry computed from the actual integer forbidden quadruples,
    # not from the intended graph edge list.
    if geometry:
        forbidden_masks=[sum(1<<i for i in q) for q in bad]
        @lru_cache(None)
        def geo_g(mask):
            opts=[]
            for i in range(1,n+1):
                child=mask|1<<i
                if not mask>>i&1 and all(child&e!=e for e in forbidden_masks):
                    opts.append(geo_g(child))
            return next(i for i in range(n+1) if i not in opts)
    safe=0
    for mask in range(1<<n):
        if all(mask&e!=e for e in edge_masks):
            safe+=1
            if geometry:assert graph_g(mask)==geo_g(S|(mask<<1))
    return {'n':n,'edges':len(edges),'points':len(pts),'safe_residual_states':safe,
            'root_grundy':graph_g(0),'four_sets_checked':len(list(combinations(range(len(pts)),4))) if geometry else 0}


def main():
    records=[]
    for n in range(5):
        possible=list(combinations(range(n),2))
        for m in range(1<<len(possible)):
            edges=[e for i,e in enumerate(possible) if m>>i&1]
            records.append(audit(n,edges))
    rng=random.Random(1019)
    possible=list(combinations(range(5),2))
    for m in rng.sample(range(1<<len(possible)),12):
        records.append(audit(5,[e for i,e in enumerate(possible) if m>>i&1]))
    summary={'graphs':len(records),'geometry_four_sets':sum(x['four_sets_checked'] for x in records),
             'residual_states':sum(x['safe_residual_states'] for x in records),
             'max_root_grundy':max(x['root_grundy'] for x in records),
             'P3':audit(3,[(0,1),(1,2)])}
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
