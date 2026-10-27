"""Independent check: enumerate glued witnesses and compute occupied-set mex.

The full C++ run covers 0..3 bridges. This independent Python program checks
all 0/1-bridge cases and independently checks all 91 gluing alpha classifications.
"""
from collections import Counter
from functools import cache
from itertools import combinations

H8 = [(0,2),(0,7),(0,8),(0,9),(1,3),(1,4),(1,5),(1,7),
      (2,4),(2,5),(2,7),(3,4),(3,6),(4,11),(8,11),(10,11),(11,12)]
H4 = [(0,3),(0,6),(1,4),(1,5),(1,6),(2,3),(2,4),(2,5),(2,6)]

def glued(u,v):
    others = iter(range(13,19))
    rename = [u if k==v else next(others) for k in range(7)]
    edges = set(tuple(sorted(e)) for e in H8)
    edges.update(tuple(sorted((rename[a],rename[b]))) for a,b in H4)
    return edges

def independent_twelves(edges):
    adj=[0]*19
    for a,b in edges:
        adj[a] |= 1<<b
        adj[b] |= 1<<a
    result=[]
    for chosen in combinations(range(19),12):
        mask=sum(1<<v for v in chosen)
        if all(not (adj[v]&mask) for v in chosen):
            result.append(mask)
    return result

def occupied_mex(edges):
    adj=[1<<v for v in range(19)]
    for a,b in edges:
        adj[a] |= 1<<b
        adj[b] |= 1<<a
    @cache
    def rec(selected, blocked):
        options=set()
        available=((1<<19)-1) & ~blocked
        while available:
            bit=available & -available
            available ^= bit
            v=bit.bit_length()-1
            options.add(rec(selected|bit,blocked|adj[v]))
        k=0
        while k in options:k+=1
        return k
    return rec(0,0)

def main():
    hist0=Counter();hist1=Counter();good=[]
    for u in range(13):
        for v in range(7):
            edges=glued(u,v)
            sets=independent_twelves(edges)
            if not sets:continue
            assert len(sets)==1
            good.append((u,v))
            hist0[occupied_mex(edges)] += 1
            for a in range(13):
                if a==u:continue
                for b in range(13,19):
                    if (sets[0]&(1<<a)) and (sets[0]&(1<<b)):
                        continue
                    assert tuple(sorted((a,b))) not in edges
                    hist1[occupied_mex(edges | {tuple(sorted((a,b)))})] += 1
    # An excluded alpha-11 gluing can in fact attain Grundy 11.
    excluded = glued(2,4) | {(5,15)}
    assert not independent_twelves(excluded)
    assert occupied_mex(excluded)==11
    assert good==[(u,v) for u in (0,1,2,3,11) for v in (0,1,2)]
    assert [hist0[k] for k in range(11)] == [3,0,0,0,1,0,4,2,4,0,1]
    assert [hist1[k] for k in range(11)] == [166,22,10,17,101,64,82,38,69,14,17]
    print('independent gluing classification:',len(good),'of 91')
    print('0 bridge histogram:',dict(sorted(hist0.items())))
    print('1 bridge histogram:',dict(sorted(hist1.items())))
    print('all 615 Python occupied-mex values match C++')
    print('excluded alpha-11 gluing (2,4) plus bridge (5,15): Grundy 11')

if __name__=='__main__':main()
