"""Generate the finite third-line parameter certificate for 8001 rational prototypes."""
from collections import Counter,defaultdict
from fractions import Fraction as F
from itertools import combinations
import json
from math import isqrt
from pathlib import Path

HERE=Path(__file__).resolve().parent


def catalog(b,c):
    return sorted((x+y,z*w-x*y,x*y) for x,y in combinations(b,2)
                  for z,w in combinations(c,2) if x+y==z+w)


def parameters(circles):
    result=set()
    for first,second,third in combinations(circles,3):
        s,d,p=first
        (A,B,C),(D,E,G)=[(s-v[0],v[1]-d,v[2]-p) for v in (second,third)]
        determinant=A*E-B*D
        if not determinant:continue
        a=F(-C*E+B*G,determinant);u=F(-A*G+C*D,determinant)
        if u in (0,1):continue
        distance=-(a*a-s*a+d*u+p)/(u*(u-1))
        if distance>0:result.add((u,distance))
    return sorted(result)


def bound(circles,u,distance):
    graph=defaultdict(set)
    for s,d,p in circles:
        constant=d*u+p+distance*u*(u-1)
        discriminant=s*s-4*constant
        if discriminant<=0:continue
        x,y=isqrt(discriminant.numerator),isqrt(discriminant.denominator)
        if x*x!=discriminant.numerator or y*y!=discriminant.denominator:continue
        root=F(x,y);a,b=(s-root)/2,(s+root)/2
        graph[a].add(b);graph[b].add(a)
    # Any irrational root has only one distinct neighbor; allow four free
    # external singleton components, even when the actual graph has fewer.
    upper=sum(sorted([len(v) for v in graph.values()]+[1]*4,reverse=True)[:4])
    if upper<=8:return upper,'degree-sum'
    maximum=4
    for k in range(1,5):
        for occupied in combinations(graph,k):
            if any(y in graph[x] for x,y in combinations(occupied,2)):continue
            neighbors=set().union(*(graph[x] for x in occupied))
            maximum=max(maximum,len(neighbors)+4-k)
    assert maximum<=8
    return maximum,'independent-neighborhood'


def main():
    points=list(combinations(range(9),5));records=[];stats=Counter()
    for i,b in enumerate(points):
        for c in points[i:]:
            circles=catalog(b,c);rows=[]
            stats['energy_'+str(len(circles))]+=1
            for u,distance in parameters(circles):
                upper,method=bound(circles,u,distance)
                rows.append({'u':str(u),'d2':str(distance),'upper':upper,'method':method})
                stats['parameters']+=1;stats[method]+=1
            records.append({'B':b,'C':c,'energy':len(circles),'parameters':rows})
    assert len(records)==8001 and stats['parameters']==11624
    data={'pool':list(range(9)),'occupied_third_line_points':4,'claimed_bound':8,
          'prototype_pairs':len(records),'stats':dict(sorted(stats.items())),'records':records}
    (HERE/'certificate.json').write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in data.items() if k!='records'}),flush=True)


if __name__=='__main__':main()
