#!/usr/bin/env python3
"""Exact constructive finite-point graph-to-kyouen residual embedding.

Usage: python verify_graph_realization.py
All geometry is rational; final common-denominator scaling gives integers.
"""
from fractions import Fraction as F
from itertools import combinations
from math import lcm, comb


def det3(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            -a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))


def forbidden(points):
    (x0,y0), *tail = points
    rows = [(x-x0,y-y0,x*x+y*y-x0*x0-y0*y0) for x,y in tail]
    return det3(*rows)==0


def new_bad_quads(points, newpoint):
    return [tuple(t) for t in combinations(range(len(points)),3)
            if forbidden([points[i] for i in t]+[newpoint])]


def circle_center(a,b,t):
    x,y=a; u,v=b
    return ((x+u)/2-t*(v-y), (y+v)/2+t*(u-x))


def point_on_circle(a,center,slope):
    x,y=a; h,k=center; m=F(slope)
    delta=-2*((x-h)+m*(y-k))/(1+m*m)
    return (x+delta,y+m*delta)


def on_circle(p,center,r2):
    return (p[0]-center[0])**2+(p[1]-center[1])**2==r2


def realize(n, edges):
    """Returns vertices, anchors, exact forbidden 4-tuples (all rational)."""
    edges = sorted({tuple(sorted(e)) for e in edges})
    assert all(0<=u<v<n for u,v in edges)
    vertices=[(F(i),F(i*i)) for i in range(1,n+1)]
    points=vertices[:]
    anchor_indices=[]
    for u,v in edges:
        a,b=vertices[u],vertices[v]
        center=None
        for t in range(1,len(points)+4):
            cc=circle_center(a,b,F(t))
            r2=(a[0]-cc[0])**2+(a[1]-cc[1])**2
            if all(not on_circle(p,cc,r2) for i,p in enumerate(points) if i not in (u,v)):
                center=cc; break
        if center is None: raise RuntimeError(f'no center for {u,v}')
        ai=None
        for m in range(1,2*comb(len(points),3)+len(points)+6):
            p=point_on_circle(a,center,m)
            if p not in points and not new_bad_quads(points,p):
                ai=len(points); points.append(p); break
        if ai is None: raise RuntimeError(f'no first anchor for {u,v}')
        bi=None
        for m in range(1,2*comb(len(points),3)+len(points)+6):
            p=point_on_circle(a,center,m)
            if p not in points and new_bad_quads(points,p)==[(u,v,ai)]:
                bi=len(points); points.append(p); break
        if bi is None: raise RuntimeError(f'no second anchor for {u,v}')
        anchor_indices.append((ai,bi))
    all_bad=[q for q in combinations(range(len(points)),4) if forbidden([points[i] for i in q])]
    expected=[tuple(sorted((u,v,*ab))) for (u,v),ab in zip(edges,anchor_indices)]
    assert sorted(all_bad)==sorted(expected), (all_bad,expected)
    scale=lcm(*(z.denominator for p in points for z in p))
    ints=[tuple(int(z*scale) for z in p) for p in points]
    assert len(set(ints))==len(ints)
    assert sorted(q for q in combinations(range(len(ints)),4) if forbidden([ints[i] for i in q]))==sorted(expected)
    return ints,anchor_indices,expected,scale


def grundy_independence(n,edges):
    from functools import lru_cache
    edges=[(1<<u)|(1<<v) for u,v in edges]
    @lru_cache(None)
    def g(s):
        opts=[]
        for v in range(n):
            m=s|(1<<v)
            if not s>>v&1 and all(m&e!=e for e in edges):opts.append(g(m))
        return next(i for i in range(n+1) if i not in opts)
    return g(0)


def grundy_geometric(n,anchors,quads):
    from functools import lru_cache
    vmask=(1<<n)-1
    occupied=sum((1<<i)|(1<<j) for i,j in anchors)
    forbidden_masks=[sum(1<<i for i in q) for q in quads]
    @lru_cache(None)
    def g(s):
        opts=[]
        for v in range(n):
            m=s|(1<<v)
            if not s>>v&1 and all((m&e)!=e for e in forbidden_masks):opts.append(g(m))
        return next(i for i in range(n+1) if i not in opts)
    return g(occupied)


def main():
    graphs=[('P4',4,[(0,1),(1,2),(2,3)]),
            ('C5',5,[(0,1),(1,2),(2,3),(3,4),(0,4)]),
            ('K4',4,list(combinations(range(4),2))),
            ('edgeless5',5,[])]
    for name,n,edges in graphs:
        pts,anchors,quads,scale=realize(n,edges)
        expected=grundy_independence(n,edges)
        actual=grundy_geometric(n,anchors,quads)
        assert expected==actual
        print(name,'vertices',n,'edges',len(edges),'points',len(pts),
              'forbidden',len(quads),'grundy',actual,'scale_digits',len(str(scale)))
        if name=='P4':
            print('P4_integer_points=',pts)
            print('P4_occupied_indices=',[i for a in anchors for i in a])
            print('P4_forbidden_quads=',quads)

if __name__=='__main__':main()
