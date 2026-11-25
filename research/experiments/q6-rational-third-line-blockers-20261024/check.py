"""Independent certificate audit: Gaussian elimination and radical-axis vertices.

Does not import the generator or use its discriminant/root enumeration.
"""
from collections import Counter
import copy
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def circles(b,c):
    bs={};cs={}
    for x,y in combinations(b,2):bs.setdefault(x+y,[]).append(x*y)
    for x,y in combinations(c,2):cs.setdefault(x+y,[]).append(x*y)
    result=[(s,q-p,p) for s in sorted(bs.keys()&cs.keys()) for p in bs[s] for q in cs[s]]
    assert len(result)==len(set(result))
    return result


def solve_three(triple,stats):
    # Unknowns T,a,u, where T=d^2*u*(u-1)+a^2.
    matrix=[[F(1),F(-s),F(delta),F(-p)] for s,delta,p in triple]
    rank=0;pivots=[]
    for column in range(3):
        pivot=next((i for i in range(rank,3) if matrix[i][column]),None)
        if pivot is None:continue
        matrix[rank],matrix[pivot]=matrix[pivot],matrix[rank]
        divisor=matrix[rank][column];matrix[rank]=[x/divisor for x in matrix[rank]]
        for i in range(3):
            if i==rank:continue
            divisor=matrix[i][column]
            matrix[i]=[x-divisor*y for x,y in zip(matrix[i],matrix[rank])]
        pivots.append(column);rank+=1
    if any(all(x==0 for x in r[:3]) and r[3]!=0 for r in matrix):
        stats['singular-inconsistent']+=1;return None
    if rank==3:
        t,a,u=[matrix[i][3] for i in range(3)]
        if u in (0,1):stats['boundary']+=1;return None
        d2=(t-a*a)/(u*(u-1))
        if d2<=0:stats['nonpositive-distance']+=1;return None
        stats['positive-triple']+=1;return u,d2
    # Singular families must be excluded for all real free parameters.
    s,d,p=triple[0]
    rows=[(s-q[0],q[1]-d,q[2]-p) for q in triple[1:]]
    A,B,C=next(r for r in rows if r[0] or r[1])
    if A:
        h,m=F(-C,A),F(-B,A)
        assert h*h-s*h+p==0
        assert (m+h)**2-s*(m+h)+d+p==0
        # Residual = m^2*u*(u-1), requiring d^2=-m^2.
    else:
        u=F(-C,B)
        if u not in (0,1):
            assert u<0 or u>1
            assert d*u+p-F(s*s,4)>=0
    stats['singular-no-exterior-point']+=1;return None


def graph_bound(catalog,u,d2):
    quadratics=[(F(s),delta*u+p+d2*u*(u-1)) for s,delta,p in catalog]
    vertices=set()
    # All rational vertices of degree >=2 are found at radical-axis
    # intersections of two nonidentical monic quadratics.
    for (s,k),(t,h) in combinations(quadratics,2):
        if s==t:continue
        a=(k-h)/(s-t)
        if a*a-s*a+k==0 and a*a-t*a+h==0:vertices.add(a)
    graph={}
    for a in vertices:
        neighbors={s-a for s,k in quadratics if a*a-s*a+k==0 and s-a!=a}
        if len(neighbors)>=2:graph[a]=neighbors
    # Include every adjacent degree-one vertex. Unseen components contribute
    # at most one neighbor per selected stone, so four free ones are safe.
    for a in list(graph):
        for b in graph[a]:graph.setdefault(b,set()).add(a)
    high=sorted([len(n) for n in graph.values()]+[1]*4,reverse=True)
    degree_bound=sum(high[:4])
    if degree_bound<=8:return degree_bound,'degree-sum'
    maximum=4
    for k in range(1,5):
        for occupied in combinations(graph,k):
            if any(b in graph[a] for a,b in combinations(occupied,2)):continue
            neighbors=set()
            for a in occupied:neighbors.update(graph[a])
            maximum=max(maximum,len(neighbors)+4-k)
    assert maximum<=8
    return maximum,'independent-neighborhood'


def verify(data):
    assert data['pool']==list(range(9)) and data['claimed_bound']==8 and data['occupied_third_line_points']==4
    points=list(combinations(range(9),5));expected={(b,c) for i,b in enumerate(points) for c in points[i:]}
    supplied={(tuple(r['B']),tuple(r['C'])):r for r in data['records']}
    assert len(supplied)==len(data['records'])==data['prototype_pairs']==8001 and set(supplied)==expected
    stats=Counter();linear=Counter()
    for b,c in sorted(expected):
        row=supplied[b,c];catalog=circles(b,c);assert len(catalog)==row['energy']
        parameters=set()
        for triple in combinations(catalog,3):
            result=solve_three(triple,linear)
            if result is not None:parameters.add(result)
        claimed={(F(p['u']),F(p['d2'])):p for p in row['parameters']}
        assert len(claimed)==len(row['parameters']) and set(claimed)==parameters
        stats['energy_'+str(len(catalog))]+=1
        for (u,d2),claim in claimed.items():
            bound,method=graph_bound(catalog,u,d2)
            assert bound<=claim['upper']<=8
            # The checker omits isolated degree-one rational edges, so its
            # bound may be smaller, but a nontrivial refinement must agree.
            assert claim['method'] in ('degree-sum','independent-neighborhood')
            if claim['method']=='independent-neighborhood':assert method=='independent-neighborhood'
            stats['parameters']+=1;stats[claim['method']]+=1
    assert dict(sorted(stats.items()))==data['stats']
    return {'prototype_pairs':8001,'positive_parameters':stats['parameters'],
            'linear_triple_classifications':dict(sorted(linear.items())),
            'all_real_third_line_bound':8,'status':'all complete finite parameter sets and blocker bounds verified'}


def main():
    data=json.loads((HERE/'certificate.json').read_text(encoding='utf-8'))
    receipt=verify(data)
    rejected=[]
    for kind in ('missing-prototype','missing-parameter','false-upper-bound'):
        damaged=copy.deepcopy(data)
        if kind=='missing-prototype':damaged['records'].pop()
        else:
            row=next(r for r in damaged['records'] if r['parameters'])
            if kind=='missing-parameter':row['parameters'].pop()
            else:row['parameters'][0]['upper']=0
        try:verify(damaged)
        except AssertionError:rejected.append(kind)
        else:raise AssertionError('damaged certificate accepted: '+kind)
    receipt['negative_controls_rejected']=rejected
    (HERE/'audit.json').write_text(json.dumps(receipt,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(receipt),flush=True)


if __name__=='__main__':main()
