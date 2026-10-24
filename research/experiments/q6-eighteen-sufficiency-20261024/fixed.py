"""Exact four-circle exclusion for every fixed E=14 type and the E=16 regression.

All arithmetic is Fraction/integer; the unknown third-line coordinate and
line separation remain arbitrary real numbers. No geometric sampling is used.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
AP=(0,2,4,6,8)
CASES={
    'equal-ap-regression':AP,
    'half-step-ap':(1,3,5,7,9),
    'near-ap-left':(-2,2,4,6,8),
    'near-ap-right':(0,2,4,6,10),
}


def sums(points):return Counter(x+y for x,y in combinations(points,2))


def near_ap():
    target=sums(AP);found=[];tested=0
    # In these doubled coordinates every point lies in [-5,13] intersect Z.
    for c in combinations(range(-5,14),5):
        tested+=1;r=sums(c)
        if sum(v*v for v in r.values())==14 and sum(v*r[s] for s,v in target.items())==14:
            found.append(list(c))
    assert tested==11628 and found==[[-2,2,4,6,8],[0,2,4,6,10]]
    return {'tested':tested,'solutions':found}


def catalog(b,c):
    result=[]
    for x,y in combinations(b,2):
        for z,w in combinations(c,2):
            if x+y==z+w:result.append((x+y,z*w-x*y,x*y))
    assert len(set(result))==len(result)
    return sorted(result)


def exclude(cs):
    counts=Counter()
    for four in combinations(cs,4):
        s,delta,p=four[0]
        rows=[(s-z[0],z[1]-delta,z[2]-p) for z in four[1:]]
        independent=next(((r,v) for r,v in combinations(rows,2) if r[0]*v[1]!=r[1]*v[0]),None)
        if independent:
            (a,b,c),(d,e,f)=independent
            det=a*e-b*d
            y=F(-c*e+b*f,det);u=F(-a*f+c*d,det)
            if any(a*y+b*u+c for a,b,c in rows):kind='inconsistent'
            elif u in (0,1):kind='rank-two-boundary'
            else:
                distance=-(y*y-s*y+delta*u+p)/(u*(u-1))
                assert distance<=0,(four,y,u,distance)
                kind='rank-two-zero' if distance==0 else 'rank-two-negative'
        else:
            pivot=next((r for r in rows if r[0] or r[1]),None)
            assert pivot is not None
            a,b,c=pivot
            if any(a*z[2]!=c*z[0] or b*z[2]!=c*z[1] for z in rows):kind='inconsistent-parallel'
            elif a:
                # y=m*u+h; the residual equals m^2*u*(u-1), hence d^2=-m^2.
                m,h=F(-b,a),F(-c,a)
                assert h*h-s*h+p==0
                assert (m+h)**2-s*(m+h)+delta+p==0
                kind='rank-one-nonpositive'
            else:
                u=F(-c,b)
                if u in (0,1):kind='rank-one-boundary'
                else:
                    assert u<0 or u>1
                    assert delta*u+p-F(s*s,4)>=0
                    kind='rank-one-nonpositive'
        counts[kind]+=1
    return dict(sorted(counts.items()))


def main():
    result={'near_ap':near_ap(),'cases':[]}
    for name,c in CASES.items():
        cs=catalog(AP,c);expected=16 if name=='equal-ap-regression' else 14
        assert len(cs)==expected
        counts=exclude(cs)
        result['cases'].append({'name':name,'B':list(AP),'C':list(c),'circles':cs,
                                'four_subsets':sum(counts.values()),'classifications':counts})
    assert sum(row['four_subsets'] for row in result['cases'])==4823
    (HERE/'fixed-audit.json').write_text(json.dumps(result,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result),flush=True)


if __name__=='__main__':main()
