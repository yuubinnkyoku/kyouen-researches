#!/usr/bin/env python3
"""Finite certificate for N=2q+1 two-carrier classes, q>=8.

Checks all local mex identities and independently recomputes occupied-count
states. The accompanying proof explains why these finite checks imply the
unbounded statement.
"""
from functools import lru_cache


def specs():
    return [(a,b,c,1+c-a-b)
            for a in range(4) for b in range(a+1)
            for c in range(3) if 1+c-a-b >= 0]


def mex(values):
    seen = set(values)
    result = 0
    while result in seen:
        result += 1
    return result


def valid(u,v,t,e,a,b,c,z):
    return (u >= 0 and v >= 0 and 0 <= t <= c and 0 <= e <= z
            and u+a+1-t >= 0 and v+b+1-t >= 0)


def residual_children(u,v,t,e,a,b,c,z):
    if u and u+a+1-t > 0:
        yield u-1,v,t,e
    if v and v+b+1-t > 0:
        yield u,v-1,t,e
    if t and u and v:
        yield u-1,v-1,t-1,e
    if e:
        yield u,v,t,e-1


def projection(n):
    return n if n <= 5 else 4+(n % 2)


def certificate(spec):
    a,b,c,z=spec
    @lru_cache(None)
    def small(u,v,t,e):
        assert 0 <= u <= 5 and 0 <= v <= 5
        assert valid(u,v,t,e,*spec)
        cs=list(residual_children(u,v,t,e,*spec))
        if not cs:
            return (0,1)
        vals=[small(*child) for child in cs]
        return mex(pair[0] for pair in vals),mex(pair[1] for pair in vals)

    def projected(u,v,t,e):
        return small(projection(u),projection(v),t,e)

    count=0
    for t in range(c+1):
        for e in range(z+1):
            for u in range(8):
                for v in range(8):
                    if not valid(u,v,t,e,*spec):
                        continue
                    cs=list(residual_children(u,v,t,e,*spec))
                    expected=((mex(projected(*child)[0] for child in cs),
                               mex(projected(*child)[1] for child in cs))
                              if cs else (0,1))
                    assert projected(u,v,t,e)==expected, (spec,u,v,t,e,expected)
                    count+=1
    assert projected(6,6,c,z)==projected(7,7,c,z),spec
    root=projected(7,7,c,z)
    for n in (6,7):
        initial_children=list(residual_children(n,n,c,z,*spec))
        assert initial_children
        assert all(projected(*child)==(1-root[0],1-root[1])
                   for child in initial_children),spec
    return count,projected


def independent_occupied(q,spec):
    """Separate occupied-count recursion; no residual transition routine."""
    a,b,c,z=spec
    x,y=q+a-c,q+b-c
    @lru_cache(None)
    def solve(i,j,t,e):
        values=[]
        if i<x and i+t<q-1:
            values.append(solve(i+1,j,t,e))
        if j<y and j+t<q-1:
            values.append(solve(i,j+1,t,e))
        if t<c and i+t<q-1 and j+t<q-1:
            values.append(solve(i,j,t+1,e))
        if e<z:
            values.append(solve(i,j,t,e+1))
        if not values:
            return 0,1
        return mex(x[0] for x in values),mex(x[1] for x in values)
    return solve


def run():
    classes=specs()
    assert len(classes)==12
    certificate_total=0
    independent_total=0
    wins=[]
    losses=[]
    exceptions=[]
    for spec in classes:
        checked,f=certificate(spec)
        certificate_total+=checked
        root=f(7,7,spec[2],spec[3])
        (wins if root[0] else losses).append(spec)
        a,b,c,z=spec
        pairs={f(u,v,t,e) for u in range(6) for v in range(6)
               for t in range(c+1) for e in range(z+1)
               if valid(u,v,t,e,*spec)}
        if any(h != (1-g if g<2 else g) for g,h in pairs):
            exceptions.append(spec)
        direct_count=0
        for q in (8,9,12,25,60):
            a,b,c,z=spec
            x,y=q+a-c,q+b-c
            exact=independent_occupied(q,spec)
            for t in range(c+1):
                for e in range(z+1):
                    for i in range(x+1):
                        for j in range(y+1):
                            if i+t>=q or j+t>=q:
                                continue
                            u,v=q-1-i-t,q-1-j-t
                            assert exact(i,j,t,e)==f(u,v,c-t,z-e),(spec,q,i,j,t,e)
                            direct_count+=1
            assert exact(0,0,0,0)==root
        independent_total+=direct_count
        print(f'{spec}: certificate={checked}, independent={direct_count}, root={root}')
    assert certificate_total==3476,certificate_total
    assert independent_total==241080,independent_total
    assert len(wins)==7 and len(losses)==5
    assert exceptions==[(1,1,2,1),(2,1,2,0)],exceptions
    for spec,state in [((1,1,2,1),(0,5,0,0)),
                       ((2,1,2,0),(1,5,0,0))]:
        assert independent_occupied(8,spec)(*state)==(0,0)
    print('CERTIFICATE TOTAL',certificate_total)
    print('INDEPENDENT TOTAL',independent_total)
    print('WIN TYPES',wins)
    print('LOSE TYPES',losses)
    print('SWAP EXCEPTIONS',exceptions)
    print('PASS (finite certificate + separate occupied-count checks)')


if __name__=='__main__':
    run()
