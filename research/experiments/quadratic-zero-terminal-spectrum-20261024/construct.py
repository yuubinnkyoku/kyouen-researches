"""Exact integer witnesses for every permitted terminal size in a finite audit grid.

The nonexistence direction is mathematical (proof.md), not inferred from this grid.
Every constructed safe set and every blocked empty point is checked by an
independent four-by-four determinant implementation.
"""
from fractions import Fraction
from itertools import combinations
import importlib.util
import json
from math import comb,factorial
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def B(r):return (r-2)*(r-3)*(r+2)//6


def permitted(w,m):
    sizes=([3] if m>=3 else [])+[r for r in range(4,w+1) if m<=B(r)]+[w+1]
    return sorted(set(sizes))


def interpolation(triple,target):
    ans=Fraction(0)
    for i,(xi,yi) in enumerate(triple):
        term=Fraction(yi)
        for j,(xj,yj) in enumerate(triple):
            if i!=j:term*=Fraction(target-xj,xi-xj)
        ans+=term
    return ans


def fill(required,m):
    values=set(required)
    for candidate in range(m):
        if len(values)==m:break
        values.add(candidate)
    assert len(values)==m
    return sorted(values)


def construct(w,m,r):
    assert r in permitted(w,m)
    if r==3:
        return [(0,0),(0,1),(0,2)],[list(range(m)) for _ in range(w)],{},1,1
    if r==w+1:
        t=(w-1)**3+2;scale=1
        occupied=[(0,1),(0,t)]+[(x,t**(x+1)) for x in range(1,w)]
        columns=[fill([y for xx,y in occupied if xx==x],m) for x in range(w)]
        return occupied,columns,{},t,scale
    scale=factorial(r-2)**2
    t=2*scale*(w-1)**2+(r-2)**3+2
    occupied=[(0,scale),(0,scale*t)]+[(x,scale*t**(x+1)) for x in range(1,r-1)]
    columns=[];origins={}
    for x in range(w):
        if x<r-1:
            columns.append(fill([y for xx,y in occupied if xx==x],m))
            continue
        completions={}
        for ids in combinations(range(r),3):
            triple=[occupied[i] for i in ids]
            if len({xx for xx,yy in triple})!=3:continue
            height=interpolation(triple,x)
            assert height.denominator==1
            assert height.numerator not in completions
            completions[height.numerator]=ids
        assert len(completions)==B(r)
        columns.append(sorted(completions)[:m])
        for y in columns[-1]:origins[x,y]=completions[y]
    return occupied,columns,origins,t,scale


def coefficient(quad):
    x0,y0=quad[-1];rows=[(x*x-x0*x0,x-x0,y-y0) for x,y in quad[:-1]]
    a,b,c=rows
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])


def load_independent():
    path=ROOT/'research/experiments/quadratic-lambda-20261024/verify.py'
    spec=importlib.util.spec_from_file_location('independent_geometry',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def audit(w,m,r,independent):
    occupied,columns,origins,t,scale=construct(w,m,r)
    assert all(len(ys)==m for ys in columns)
    assert len(set(occupied))==r
    for q in occupied:assert q[1] in columns[q[0]]
    quad_count=0
    for quad in combinations(occupied,4):
        a,b=independent.coefficients(quad)
        assert coefficient(quad)==b!=0
        quad_count+=1
    empty_count=0
    for x,ys in enumerate(columns):
        for y in ys:
            point=(x,y)
            if point in occupied:continue
            if r==3:triple=occupied
            elif x==0:triple=occupied[:3]
            elif x<r-1:triple=[occupied[0],occupied[1],occupied[x+1]]
            else:triple=[occupied[i] for i in origins[point]]
            quad=triple+[point]
            assert len(set(quad))==4
            a,b=independent.coefficients(quad)
            assert coefficient(quad)==b==0
            empty_count+=1
    assert empty_count==w*m-r
    return {'width':w,'points_per_column':m,'terminal_size':r,'t':t,'scale':scale,
            'occupied':occupied,'candidate_heights':columns,'safe_quadruples_checked':quad_count,
            'empty_points_checked':empty_count,
            'max_coordinate_bits':max(abs(v).bit_length() for x,ys in enumerate(columns) for v in [x,*ys])}


def main():
    independent=load_independent();cases=[]
    for w in range(3,10):
        for m in (2,3,5,8,17,31):
            sizes=permitted(w,m)
            for r in sizes:cases.append(audit(w,m,r,independent))
            print('width',w,'candidates',m,'all realized sizes',sizes,flush=True)
    # Necessity audit on already-completed exact finite game calculations.
    source=ROOT/'research/experiments/quadratic-lambda-zero-strips-20261024/results.json'
    finite=json.loads(source.read_text(encoding='utf-8'))
    finite_receipts=[]
    for row in finite['cases']:
        counts=[row['column_labels'].count(i) for i in range(row['width'])]
        if row['width']<3:continue
        minimum=min(counts);allowed=set(permitted(row['width'],minimum))
        if max(counts)>=3:allowed.add(3)
        actual={i for i,v in enumerate(row['terminal_sizes']) if v}
        assert actual<=allowed,(row['name'],actual,allowed)
        finite_receipts.append({'case':row['name'],'observed_terminal_sizes':sorted(actual),
                                'permitted_by_lower_bound':sorted(allowed)})
    data={'rule':'det[x*x,x,y,1]=0','constructed_cases':cases,
          'finite_necessity_audits':finite_receipts}
    (HERE/'results.json').write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    print('Constructed and independently verified',len(cases),'integer terminal witnesses.',flush=True)


if __name__=='__main__':main()
