#!/usr/bin/env python3
"""Exact symbolic classification of 3 columns x 4 rows, forbidden 4-point circles/lines.
Pure standard library. Produces machine-checkable summary.
"""
import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product

N=12
FULL=(1<<N)-1

def mask(points):
    return sum(1 << (4*x+y) for x,y in points)

def geometry():
    base={mask([(x,y) for y in range(4)]) for x in range(3)}
    for x,z in combinations(range(3),2):
        for p,q in product(combinations(range(4),2),repeat=2):
            if sum(p)==sum(q):
                base.add(mask([(x,y) for y in p]+[(z,y) for y in q]))
    assert len(base)==27
    groups=defaultdict(set)
    for i in range(3):
        j,k=[x for x in range(3) if x!=i]
        for r,s in combinations(range(4),2):
            for t,u in product(range(4),repeat=2):
                T=(t-r)*(t-s)
                U=(u-r)*(u-s)
                coeff=((T-U,T),(-U,-T),(U,U-T))[i]
                groups[coeff].add(mask([(i,r),(i,s),(j,t),(k,u)]))
    assert sum(map(len,groups.values()))==288
    assert len(groups)==37
    return base,groups

def signatures(groups):
    # Every actual positive spacing yields either no equality, one equality,
    # or an intersection of >=2 distinct lines in coefficient space.
    good=sorted(p for p in groups if max(p)>0)
    assert len(good)==20
    result={frozenset():None}
    for p in good:
        result[frozenset((p,))]=None
    for (A,B),(C,D) in combinations(good,2):
        if A==C:continue
        t=Fraction(D-B,A-C) # a/b
        if t<=0:continue
        k=A*t+B
        if k<=0:continue
        v2=k/(t*(t+1)) # (b/d)^2
        assert v2>0
        signature=frozenset(p for p in good if p[0]*t+p[1]==k)
        assert len(signature)>=2
        result[signature]=(t,v2)
    assert len(result)==65
    assert Counter(map(len,result))==Counter({0:1,1:20,2:38,3:6})
    return result

def is_square_rational(x):
    from math import isqrt
    return isqrt(x.numerator)**2==x.numerator and isqrt(x.denominator)**2==x.denominator

def solve(forbidden):
    by_point=[[] for _ in range(N)]
    for f in forbidden:
        for i in range(N):
            if f>>i&1:by_point[i].append(f)
    safe=bytearray(1<<N)
    safe[0]=1
    for state in range(1,1<<N):
        bit=state&-state
        safe[state]=safe[state^bit] and all((state&f)!=f for f in by_point[bit.bit_length()-1])
    grundy=[-1]*(1<<N)
    for state in range(FULL,-1,-1):
        if not safe[state]:continue
        options=set()
        rem=FULL^state
        while rem:
            bit=rem&-rem
            rem-=bit
            if safe[state|bit]:options.add(grundy[state|bit])
        value=0
        while value in options:value+=1
        grundy[state]=value
    return grundy[0],sum(grundy[1<<i]==0 for i in range(N)),sum(safe)

def main():
    base,groups=geometry()
    sigs=signatures(groups)
    rows=[]
    for sig,parameter in sigs.items():
        forbidden=set(base)
        for p in sig:forbidden.update(groups[p])
        root,winning,safe=solve(forbidden)
        integral_possible=None if parameter is None else is_square_rational(parameter[1])
        rows.append({'coefficients':[list(p) for p in sorted(sig)],
                     'a_over_b':str(parameter[0]) if parameter else None,
                     'b_over_d_squared':str(parameter[1]) if parameter else None,
                     'rational_spacing_possible':integral_possible,
                     'forbidden_quads':len(forbidden),'safe_positions':safe,
                     'root_grundy':root,'winning_first_moves':winning})
    assert Counter(row['root_grundy'] for row in rows)=={0:58,2:7}
    winning=[row for row in rows if row['root_grundy']]
    assert Counter(row['winning_first_moves'] for row in winning)=={2:4,4:2,6:1}
    rational=[row for row in winning if row['rational_spacing_possible']]
    assert len(rational)==3
    assert {(row['a_over_b'],row['b_over_d_squared']) for row in rational}=={('1','1'),('1/2','4'),('2','1')}
    summary={'scope':'positive real a,b,d; integer classification from rational ratios',
             'coefficients':len(groups),'feasible_coefficients':20,
             'signatures':len(rows),'root_0':58,'root_2':7,
             'integer_root_2_ratios':[[1,1,1],[1,2,1],[2,1,1]],
             'records':rows}
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
