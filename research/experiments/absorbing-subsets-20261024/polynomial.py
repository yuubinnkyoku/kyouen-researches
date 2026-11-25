"""Exact determinant and all-safe-position audits of the polynomial-lift corollary.

The rule includes degenerate determinant-zero sets. It is not the strict rule
that only distinct-x points lying on a function graph are forbidden.
"""
from collections import Counter
from fractions import Fraction
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def bareiss(rows):
    a=[list(r) for r in rows];n=len(a);previous=1;sign=1
    for k in range(n-1):
        if a[k][k]==0:
            pivot=next((i for i in range(k+1,n) if a[i][k]),None)
            if pivot is None:return 0
            a[k],a[pivot]=a[pivot],a[k];sign=-sign
        p=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                value=a[i][j]*p-a[i][k]*a[k][j]
                assert value%previous==0
                a[i][j]=value//previous
        for i in range(k+1,n):a[i][k]=0
        previous=p
    return sign*a[-1][-1]


def rational_elimination(rows):
    a=[[Fraction(v) for v in row] for row in rows];ans=Fraction(1);n=len(a)
    for k in range(n):
        pivot=next((i for i in range(k,n) if a[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];ans=-ans
        p=a[k][k];ans*=p
        for i in range(k+1,n):
            factor=a[i][k]/p
            for j in range(k,n):a[i][j]-=factor*a[k][j]
    assert ans.denominator==1
    return ans.numerator


def load_games():
    path=ROOT/'research/experiments/quadratic-lambda-20261024/verify.py'
    spec=importlib.util.spec_from_file_location('finite_games',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def main():
    engine=load_games();cases=[]
    for d,w,h in ((2,3,3),(3,4,3),(3,5,3),(4,5,3),(5,3,3),(6,3,3)):
        cases.append((f'degree-{d}-{w}-by-{h}',d,[(x,y) for x in range(w) for y in range(h)]))
    cases.extend([
        ('odd-irregular-covered',3,[(x,y) for x,ys in [(0,[0,2,8]),(2,[1,3,5]),(7,[-2,4,11])]
                                  for y in ys]),
        ('even-one-covered-column',4,[(0,y) for y in (0,2,5)]+[(x,x*x+1) for x in range(1,7)]),
        ('odd-uncovered-boundary',3,[(0,y) for y in (0,1,2)]+[(1,0),(2,1),(3,3)]),
    ])
    rows=[]
    for name,d,points in cases:
        q=d+2;n=len(points);assert n>=d+1
        edges=[];checked=0
        lifted=[[x**k for k in range(d,0,-1)]+[y,1] for x,y in points]
        for ids in combinations(range(n),q):
            matrix=[lifted[i] for i in ids]
            a,b=bareiss(matrix),rational_elimination(matrix)
            assert a==b,(name,ids,a,b)
            if a==0:edges.append(sum(1<<i for i in ids))
            checked+=1
        values,report=engine.occupied_game(n,edges)
        root,independent=engine.residual_game(n,edges)
        assert root==values[0] and len(independent)==report['safe_count']
        assert all(values[s]==g for s,g in independent.items())
        capacities=Counter(x for x,y in points)
        covered=[i for i,(x,y) in enumerate(points) if capacities[x]>=3]
        theorem_applies=(d>=4 and d%2==0 and bool(covered)) or (d>=3 and d%2==1 and len(covered)==n)
        if theorem_applies:
            assert bool(root)==(d%2==0),(name,root)
            if d%2==0:assert all(values[1<<i]==0 for i in covered)
            else:assert all(values[1<<i]!=0 for i in range(n))
        if d==2:assert root==0
        row={'case':name,'degree':d,'q':q,'points':points,'q_subsets_checked':checked,
             'theorem_applies':theorem_applies,'covered_point_indices':covered,
             'individually_compared_states':len(independent),**report}
        rows.append(row)
        print(name,'scope',theorem_applies,'root',root,'safe',report['safe_count'],flush=True)
    (HERE/'polynomial.json').write_text(json.dumps({'cases':rows},separators=(',',':'))+'\n',encoding='utf-8',newline='\n')


if __name__=='__main__':main()
