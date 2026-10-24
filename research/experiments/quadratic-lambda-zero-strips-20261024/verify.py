"""Finite audits of the all-state lambda=0 strip theorem; no floating point."""
import importlib.util
from itertools import combinations
import json
from math import comb
import os
from pathlib import Path
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def geometry():
    path=ROOT/'research/experiments/quadratic-lambda-20261024/verify.py'
    spec=importlib.util.spec_from_file_location('quadratic_geometry',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def native_build():
    directory=Path(tempfile.gettempdir())/'kyouen-quadratic-zero-strips-20261024'
    directory.mkdir(exist_ok=True)
    outputs=[]
    for stem in ('audit','column_audit'):
        exe=directory/(stem+('.exe' if os.name=='nt' else ''))
        subprocess.run([os.environ.get('CXX','g++'),'-std=c++17','-O3','-Wall','-Wextra',str(HERE/(stem+'.cpp')),'-o',str(exe)],check=True)
        outputs.append(exe)
    return outputs


def main():
    module=geometry();exe,independent=native_build();results=[]
    cases=[]
    for w,m in ((2,2),(2,3),(2,5),(3,2),(3,3),(3,5),(4,2),(4,3),(4,4),(4,5),(5,5),(5,6),(5,7),(5,8),(5,9)):
        cases.append((f'regular-{w}-by-{m}',list(range(w)),[list(range(m)) for _ in range(w)]))
    cases.extend([
        ('irregular-three',[0,2,7],[[0,3,9],[-2,1,4,8],[1,5,12]]),
        ('irregular-four',[-3,0,4,11],[[0,2,6],[1,4,9,15],[-5,0,8],[2,3,5,12,20]]),
        ('irregular-five',[-5,-1,2,8,15],[[i*i+3*j for i in range(8)] for j in range(5)]),
    ])
    for name,xs,ys in cases:
        w=len(xs);points=[];cols=[]
        for j,(x,values) in enumerate(zip(xs,ys)):
            points.extend((x,y) for y in values);cols.extend([j]*len(values))
        assert len(points)<=63
        edges=[]
        for ids in combinations(range(len(points)),4):
            a,b=module.coefficients([points[i] for i in ids])
            if b==0:edges.append(sum(1<<i for i in ids))
        raw=f'{w} {len(points)} {len(edges)}\n'+' '.join(map(str,cols))+'\n'+' '.join(map(str,edges))+'\n'
        row=json.loads(subprocess.check_output([str(exe)],input=raw.encode('ascii')))
        second=json.loads(subprocess.check_output([str(independent)],input=raw.encode('ascii')))
        for key,value in second.items():
            assert row[key]==value,(name,key)
        row['independent_column_dp']=True
        bound=max(3,1+(w-2)*(w-3)*(w+2)//6)
        in_scope=all(len(y)>=bound for y in ys)
        if in_scope or name in ('regular-5-by-6','regular-5-by-7'):
            assert row['formula_mismatches']==row['terminal_outside']==0,(name,row)
        if len(points)<=20:
            _,reference=module.occupied_game(len(points),edges)
            for key in ('empty_grundy','safe_count'):
                assert row[key]==reference[key]
            for key in ('safe_layers','grundy_histogram','terminal_sizes'):
                assert {i:v for i,v in enumerate(row[key]) if v}==reference[key],(name,key)
            row['independent_subset_dp']=True
        else:row['independent_subset_dp']=False
        row.update(name=name,width=w,points=points,column_labels=cols,edge_count=len(edges),
                   sufficient_minimum=bound,in_theorem_scope=in_scope)
        results.append(row)
        print(name,'scope',in_scope,'states',row['safe_count'],'root',row['empty_grundy'],
              'mismatch',row['formula_mismatches'],'terminal outside',row['terminal_outside'],flush=True)
    data={'rule':'lambda=0: det[x*x,x,y,1]=0','cases':results}
    (HERE/'results.json').write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8')


if __name__=='__main__':main()
