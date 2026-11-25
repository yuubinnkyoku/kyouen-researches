#!/usr/bin/env python3
"""Independent recursive exact check for arbitrary three x-columns, lambda=0."""
from functools import lru_cache
from itertools import combinations, permutations
from math import comb

def det4(rows):
    ans=0
    for p in permutations(range(4)):
        inv=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        t=1
        for i in range(4): t*=rows[i][p[i]]
        ans+=(-1 if inv&1 else 1)*t
    return ans

def check(columns):
    points=[(x,y) for x,ys in columns for y in ys]
    caps=[len(ys) for _,ys in columns]
    n=len(points)
    assert len(columns)==3 and len({x for x,_ in columns})==3 and all(len(set(ys))==len(ys) and ys for _,ys in columns)
    forbidden=set()
    for ids in combinations(range(n),4):
        rows=[(points[i][0]**2,points[i][0],points[i][1],1) for i in ids]
        if det4(rows)==0:forbidden.add(sum(1<<i for i in ids))
    @lru_cache(None)
    def g(s):
        if any(s&f==f for f in forbidden):raise AssertionError('unsafe input')
        options=set()
        for i in range(n):
            t=s|(1<<i)
            if t!=s and not any(t&f==f for f in forbidden):options.add(g(t))
        ans=0
        while ans in options:ans+=1
        return ans
    safe=0;maximal={3:0,4:0};by_size=[0]*5
    for s in range(1<<n):
        if any(s&f==f for f in forbidden):continue
        safe+=1;k=s.bit_count();assert k<=4;by_size[k]+=1
        occ=[sum((s>>i)&1 for i,(x,y) in enumerate(points) if x==columns[j][0]) for j in range(3)]
        if caps==[1,1,1]:expected=(3-k)&1
        elif k==0:expected=0
        elif k==1:expected=1
        elif k==2:expected=2 if any(occ[j]==2 and caps[j]>=3 for j in range(3)) else 0
        elif k==3:expected=0 if 3 in occ else 1
        else:expected=0
        actual=g(s)
        assert actual==expected,(columns,s,occ,actual,expected)
        if k in maximal and not any(s&(1<<i)==0 and not any((s|(1<<i))&f==f for f in forbidden) for i in range(n)):maximal[k]+=1
    a,b,c=caps
    safe4=comb(a,2)*b*c+comb(b,2)*a*c+comb(c,2)*a*b
    terminal3=sum(comb(z,3) if z>=3 else 0 for z in caps)+(1 if caps==[1,1,1] else 0)
    assert by_size[4]==safe4 and maximal[3]==terminal3 and maximal[4]==safe4
    return dict(caps=caps,safe=safe,root=g(0),terminal3=maximal[3],terminal4=maximal[4])

if __name__=='__main__':
    cases=[[(0,[0]),(2,[1]),(7,[4])],[(0,[0,9]),(2,[1]),(7,[4])],[(0,[0,2,8]),(2,[1]),(7,[4])],[(0,[0,2,8]),(2,[1,5]),(7,[4,13])],[(0,[0,2,8]),(2,[1,5,11]),(7,[4,13,17])],[(0,[0,2]),(2,[1,5,11,12]),(7,[4,13,17])]]
    for case in cases:print(check(case))
