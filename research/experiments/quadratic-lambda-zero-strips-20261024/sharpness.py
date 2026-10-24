"""Construct and independently check the all-width sharpness family on integer points."""
from fractions import Fraction
from itertools import combinations
import importlib.util
import json
from math import comb,lcm
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def interpolate(triple,x):
    total=Fraction(0)
    for i,(xi,yi) in enumerate(triple):
        term=Fraction(yi)
        for j,(xj,yj) in enumerate(triple):
            if i!=j:term*=Fraction(x-xj,xi-xj)
        total+=term
    return total


def coefficient(points):
    x0,y0=points[-1];r=[(x*x-x0*x0,x-x0,y-y0) for x,y in points[:-1]]
    a,b,c=r
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])


def construct(w):
    count=comb(w-2,3)+2*comb(w-2,2)
    forms=1+comb(w,4)+comb(count,2)
    maximum_t=forms*(w-1)+1
    for t in range(1,maximum_t+1):
        s=[(0,1),(0,t)]+[(x,t**(x+1)) for x in range(1,w-1)]
        if len(set(s))!=w or any(coefficient(q)==0 for q in combinations(s,4)):
            continue
        completions={}
        for ids in combinations(range(w),3):
            tri=[s[i] for i in ids]
            if len({x for x,y in tri})==3:
                y=interpolate(tri,w-1)
                completions[y]=ids
        if len(completions)==count:break
    else:raise AssertionError('finite polynomial avoidance bound failed')
    scale=lcm(*(y.denominator for y in completions))
    s=[(x,y*scale) for x,y in s]
    completion_ids={int(y*scale):ids for y,ids in completions.items()}
    columns=[]
    for x in range(w-1):
        values={y for xx,y in s if x==xx}
        candidate=0
        while len(values)<count:
            values.add(candidate);candidate+=1
        columns.append(sorted(values))
    columns.append(sorted(completion_ids))
    assert all(len(values)==count for values in columns)
    return s,columns,completion_ids,t,scale


def main():
    path=ROOT/'research/experiments/quadratic-lambda-20261024/verify.py'
    spec=importlib.util.spec_from_file_location('independent_determinant',path)
    geom=importlib.util.module_from_spec(spec);spec.loader.exec_module(geom)
    rows=[]
    for w in range(4,11):
        s,columns,completion_ids,t,scale=construct(w)
        safe_quads=0
        for q in combinations(s,4):
            a,b=geom.coefficients(q);assert b==coefficient(q)!=0;safe_quads+=1
        occupied=set(s);checked=0
        for x,ys in enumerate(columns):
            for y in ys:
                q=(x,y)
                if q in occupied:continue
                if x==0:tri=s[:3]
                elif x<w-1:tri=[s[0],s[1],s[x+1]]
                else:tri=[s[i] for i in completion_ids[y]]
                quad=tri+[q]
                assert len(set(quad))==4
                a,b=geom.coefficients(quad);assert b==coefficient(quad)==0
                checked+=1
        row={'width':w,'candidate_count_per_column':len(columns[0]),'occupied':s,
             'candidate_heights':columns,'t':t,'scale':scale,'checked_empty_points':checked,
             'checked_safe_quadruples':safe_quads,'actual_terminal_grundy':0,'formula_prediction':1}
        rows.append(row)
        print('width',w,'points/column',len(columns[0]),'t',t,'verified maximal',len(s),'stones',flush=True)
    standard=[(3,1),(3,3),(1,1),(2,1),(4,4)]
    assert all(geom.coefficients(q)[1]!=0 for q in combinations(standard,4))
    blocked=[]
    for x in range(5):
        for y in range(5):
            q=(x,y)
            if q in standard:continue
            for ids in combinations(range(5),3):
                if geom.coefficients([standard[i] for i in ids]+[q])[1]==0:
                    blocked.append({'point':q,'triple_indices':ids});break
            else:raise AssertionError(('standard 5x5 witness not maximal',q))
    data={'integer_counterexamples':rows,'standard_five_by_five_terminal':
          {'occupied':standard,'empty_point_blockers':blocked,'actual_grundy':0,'formula_prediction':1}}
    (HERE/'sharpness.json').write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8')


if __name__=='__main__':main()
