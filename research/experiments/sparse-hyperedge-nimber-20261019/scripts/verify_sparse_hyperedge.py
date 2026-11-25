#!/usr/bin/env python3
"""Independent count-state and subset-state exact tests for sparse forbidden hypergraphs."""
from functools import lru_cache
from itertools import combinations
from collections import Counter
import json
from pathlib import Path

POINTS = [(3,4),(-5,0),(-4,-3),(-4,3),(1,0),(2,-3),(6,-5)]
E1 = (0,1,2,3)
E2 = (0,4,5,6)
EDGES = tuple(sum(1 << v for v in edge) for edge in (E1,E2))

def det(matrix):
    if len(matrix) == 1: return matrix[0][0]
    return sum((-1)**j*matrix[0][j]*det([row[:j]+row[j+1:] for row in matrix[1:]]) for j in range(len(matrix)))

def four_cocircular_or_collinear(ids):
    return det([[x*x+y*y,x,y,1] for i in ids for x,y in [POINTS[i]]]) == 0

@lru_cache(None)
def grundy(mask):
    opts=[]
    for i in range(7):
        bit=1<<i
        if mask & bit:continue
        after=mask|bit
        if any((after&e)==e for e in EDGES):continue
        opts.append(grundy(after))
    return next(i for i in range(8) if i not in opts)


def class_count(q, overlap):
    exclusive=q-overlap
    @lru_cache(None)
    def g(a,b,c):
        opts=[]
        if a<overlap and a+1+b<q and a+1+c<q:opts.append(g(a+1,b,c))
        if b<exclusive and a+b+1<q:opts.append(g(a,b+1,c))
        if c<exclusive and a+c+1<q:opts.append(g(a,b,c+1))
        return next(i for i in range(5) if i not in opts)
    return g


def verify_all_small_two_edge_hypergraphs(n=6):
    subsets=[sum(1<<i for i in s) for r in range(2,n+1) for s in combinations(range(n),r)]
    tested=0
    max_grundy=0
    @lru_cache(None)
    def g(mask,edge1,edge2):
        vals=[]
        for v in range(n):
            if mask>>v&1:continue
            t=mask|(1<<v)
            if t&edge1==edge1 or t&edge2==edge2:continue
            vals.append(g(t,edge1,edge2))
        return next(i for i in range(5) if i not in vals)
    for e1,e2 in combinations(subsets,2):
        if e1&e2==e1 or e1&e2==e2:continue
        tested+=1
        for mask in range(1<<n):
            if mask&e1==e1 or mask&e2==e2:continue
            z=g(mask,e1,e2)
            assert z<=3,(e1,e2,mask,z)
            max_grundy=max(max_grundy,z)
    return {"vertices":n,"distinct_incomparable_edge_pairs":tested,"max_grundy":max_grundy}


def main():
    assert [tuple(x) for x in combinations(range(7),4) if four_cocircular_or_collinear(x)]==[E1,E2]
    states=[s for s in range(128) if all((s&e)!=e for e in EDGES)]
    vals=Counter(grundy(s) for s in states)
    witness_mask=(1<<1)|(1<<4)|(1<<5)
    witness_children={str(i):grundy(witness_mask|1<<i) for i in range(7) if not witness_mask>>i&1 and all(((witness_mask|1<<i)&e)!=e for e in EDGES)}
    assert grundy(witness_mask)==3
    assert set(witness_children.values())=={0,1,2}
    # Count-state recurrence uses only cardinalities, not bitsets or geometry.
    f=class_count(4,1)
    for s in states:
        a=bool(s&1)
        b=(s&0b1110).bit_count()
        c=(s&0b1110000).bit_count()
        assert grundy(s)==f(int(a),b,c)
    report={"points":POINTS,"forbidden_4sets":[E1,E2],"safe_states":len(states),"grundy_histogram":dict(sorted(vals.items())),"empty_grundy":grundy(0),"nimber3_witness_mask":witness_mask,"nimber3_witness_points":[POINTS[i] for i in range(7) if witness_mask>>i&1],"witness_child_grundy":witness_children,"small_hypergraph_audit":verify_all_small_two_edge_hypergraphs()}
    output=Path(__file__).resolve().parents[1]/'output/verification.json'
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
