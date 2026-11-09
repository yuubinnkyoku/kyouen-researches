#!/usr/bin/env python3
"""Check coplanar quadruples by integer minors and triple/codegree formulas."""
from collections import Counter, defaultdict
from itertools import combinations
import json


def det3(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])


def classify(d):
    points = [tuple((v >> k) & 1 for k in range(d)) for v in range(1 << d)]
    edges=[]
    for q in combinations(range(len(points)), 4):
        vectors = [[points[v][i]-points[q[0]][i] for i in range(d)] for v in q[1:]]
        if all(det3(*[[row[i] for i in cols] for row in vectors]) == 0
               for cols in combinations(range(d),3)):
            edges.append(q)
    pairs=Counter()
    triples=defaultdict(list)
    for edge in edges:
        pairs.update(combinations(edge,2))
        for tri in combinations(edge,3):
            triples[tri].append(next(v for v in edge if v not in tri))
    assert len(edges)==(6**d-2*4**d+2**d)//8
    for a,b in combinations(range(len(points)),2):
        distance=(a^b).bit_count()
        assert pairs[a,b]==2**(distance-1)+2**(d-distance)-2
    for tri in combinations(range(len(points)),3):
        completions=triples.get(tri, [])
        assert len(completions)<=1
        minority=set()
        for k in range(d):
            bits=[points[v][k] for v in tri]
            if sum(bits) in (1,2):
                minority.add(bits.index(1 if sum(bits)==1 else 0))
        assert bool(completions)==(len(minority)<=2)
        if completions:
            assert completions[0] == (tri[0]^tri[1]^tri[2])
    assert len(triples)==(6**d-2*4**d+2**d)//2
    return {'dimension':d,'vertices':len(points),'forbidden_quadruples':len(edges),
            'completable_triples':len(triples),'all_pairs_checked':len(points)*(len(points)-1)//2,
            'all_triples_checked':len(points)*(len(points)-1)*(len(points)-2)//6}


if __name__=='__main__':
    print(json.dumps([classify(d) for d in range(2,6)],indent=2))
