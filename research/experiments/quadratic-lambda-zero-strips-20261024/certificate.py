"""Generate/check a terminal-complete Grundy certificate for one 6x6 lambda=0 state.

Generation uses residual forbidden edges from the earlier independent geometry.
Checking reconstructs every legal move from a separate 4x4 permutation determinant.
"""
import argparse
import copy
from functools import lru_cache
import importlib.util
from itertools import combinations,permutations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PERMS=[(p,(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4)))
       for p in permutations(range(4))]


def geometry():
    path=ROOT/'research/experiments/quadratic-lambda-20261024/verify.py'
    spec=importlib.util.spec_from_file_location('generation_geometry',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def generate():
    geom=geometry();points=[(x,y) for x in range(6) for y in range(6)];full=(1<<36)-1
    row=next(r for r in json.loads((HERE/'results.json').read_text())['cases'] if r['name']=='regular-6-by-6')
    root=row['grundy_three_witness'];edges=[]
    for ids in combinations(range(36),4):
        if geom.coefficients([points[i] for i in ids])[1]==0:edges.append(sum(1<<i for i in ids))
    values={}
    @lru_cache(None)
    def oracle(available):
        family=[edge & available for edge in edges]
        assert 0 not in family
        blocked=0
        for edge in family:
            if edge & (edge-1)==0:blocked|=edge
        options=set();bits=available & ~blocked
        while bits:
            bit=bits & -bits;bits^=bit;options.add(oracle(available ^ bit))
        value=0
        while value in options:value+=1
        values[full ^ available]=value
        return value
    assert oracle(full ^ root)==3
    return {'side':6,'point_index':'i=6*x+y','rule':'det[x*x,x,y,1]=0',
            'root':root,'root_grundy':3,'states':sorted(values.items())}


def verify(data):
    assert data['side']==6 and data['point_index']=='i=6*x+y' and data['rule']=='det[x*x,x,y,1]=0'
    points=[(x,y) for x in range(6) for y in range(6)]
    lifted=[(x*x,x,y,1) for x,y in points];full=(1<<36)-1
    values=dict(data['states']);assert len(values)==len(data['states'])
    assert all(isinstance(s,int) and 0<=s<=full and isinstance(g,int) and 0<=g<=36 for s,g in values.items())
    @lru_cache(None)
    def determinant(ids):
        rows=[lifted[i] for i in ids];ans=0
        for p,sign in PERMS:
            term=sign
            for i in range(4):term*=rows[i][p[i]]
            ans+=term
        return ans
    children={};edges_checked=0;terminal=0
    for state,claimed in values.items():
        occupied=[i for i in range(36) if state>>i&1]
        assert all(determinant(ids)!=0 for ids in combinations(occupied,4))
        options=set();legal=[]
        for p in range(36):
            if state>>p&1:continue
            if all(determinant(tuple(sorted((*tri,p))))!=0 for tri in combinations(occupied,3)):
                child=state | (1<<p)
                assert child in values,('missing child',state,p)
                options.add(values[child]);legal.append(child);edges_checked+=1
        expected=0
        while expected in options:expected+=1
        assert claimed==expected,('wrong mex',state,claimed,expected)
        children[state]=legal
        terminal+=not legal
    root=data['root'];assert root in values and values[root]==data['root_grundy']==3
    reached=set();stack=[root]
    while stack:
        state=stack.pop()
        if state not in reached:reached.add(state);stack.extend(children[state])
    assert reached==set(values)
    return {'nodes':len(values),'edges_checked':edges_checked,'terminal_nodes':terminal,
            'distinct_determinants':determinant.cache_info().currsize,'root_grundy':3,
            'root_points':[points[i] for i in range(36) if root>>i&1]}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--generate',action='store_true')
    args=parser.parse_args();path=HERE/'n6-grundy-three-certificate.json'
    if args.generate:path.write_text(json.dumps(generate(),separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    data=json.loads(path.read_text(encoding='utf-8'));receipt=verify(data)
    rejected=0
    for mode in ('wrong-value','missing-state'):
        damaged=copy.deepcopy(data)
        if mode=='wrong-value':damaged['states'][0][1]+=1
        else:damaged['states'].pop()
        try:verify(damaged)
        except AssertionError:rejected+=1
        else:raise AssertionError(('negative control accepted',mode))
    assert rejected==2;receipt['negative_controls_rejected']=rejected
    (HERE/'n6-certificate-verification.json').write_text(json.dumps(receipt,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(receipt),flush=True)


if __name__=='__main__':main()
